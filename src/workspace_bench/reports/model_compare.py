"""Run and chart Workspace Bench performance for local model adapters."""

from __future__ import annotations

import argparse
import copy
from collections import Counter
import html
import json
import os
import shutil
import subprocess
import shlex
import ssl
import sys
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

from workspace_bench.agents.model_adapter_helpers import (
    TOOL_REFERENCE,
    fixture_origin_hints,
    fixture_widget_hints,
    strip_code_fence,
)
from workspace_bench.agents.agent_command import (
    AgentCommandRun,
    build_task_envelope,
    run_agent_command,
)
from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import (
    BENCHMARK_NAME,
    BENCHMARK_RELEASE_ID,
    BENCHMARK_VERSION,
    JsonDict,
    RunResult,
    Scenario,
    ToolCall,
    VALID_SCENARIO_SPLITS,
)
from workspace_bench.reports.metrics import compute_reliability_metrics
from workspace_bench.core.runner import BUILTIN_SCENARIO_PACK_ORDER
from workspace_bench.core.runner import load_builtin_scenarios, load_scenario_directory
from workspace_bench.core.runner import load_builtin_task_pack_manifest, load_task_pack_manifest


INTERACTIVE_PROVIDERS = {"openai", "ollama"}
REPO_ROOT = Path.cwd()


def resolve_repo_root(start: Path | None = None) -> Path:
    """Find the checkout root used for repo-local example adapters."""

    start = start or Path.cwd()
    candidates = [start, *start.parents, *Path(__file__).resolve().parents]
    for candidate in candidates:
        if (
            (candidate / "pyproject.toml").exists()
            and (candidate / "examples" / "openai_gpt4_1.py").exists()
            and (candidate / "examples" / "ollama_agent.py").exists()
        ):
            return candidate
    return Path.cwd()


def load_dotenv(path: str | Path = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


@dataclass(frozen=True)
class ModelAdapter:
    slug: str
    label: str
    command: str
    env: dict[str, str]
    provider: str
    model: str


@dataclass(frozen=True)
class ComparisonRun:
    run_result: RunResult
    command: str
    exit_code: int | None
    timed_out: bool
    stdout: str
    stderr: str
    run_dir: Path
    task_path: Path
    output_path: Path
    runner: str
    repeat: int = 1


class TransientModelError(RuntimeError):
    """Retryable model provider failure."""

    def __init__(self, message: str, *, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


def default_adapters() -> dict[str, ModelAdapter]:
    repo_root = resolve_repo_root()
    python = shlex.quote(sys.executable)
    return {
        "openai-gpt-4.1": ModelAdapter(
            slug="openai-gpt-4.1",
            label="OpenAI GPT-4.1",
            command=f"{python} {shlex.quote(str(repo_root / 'examples' / 'openai_gpt4_1.py'))}",
            env={},
            provider="openai",
            model="gpt-4.1",
        ),
        "ollama-gpt-oss-20b": ModelAdapter(
            slug="ollama-gpt-oss-20b",
            label="Ollama gpt-oss:20b",
            command=f"{python} {shlex.quote(str(repo_root / 'examples' / 'ollama_agent.py'))}",
            env={"OLLAMA_MODEL": "gpt-oss:20b"},
            provider="ollama",
            model="gpt-oss:20b",
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run selected Workspace Bench scenarios against multiple model adapters."
    )
    parser.add_argument(
        "--models-file",
        help=(
            "JSON file defining model adapters. When provided without --models, "
            "all models in the file are run."
        ),
    )
    parser.add_argument(
        "--models",
        nargs="+",
        help=(
            "Model adapter slugs to run. Defaults to both built-in adapters, "
            "or all adapters in --models-file when that option is set."
        ),
    )
    parser.add_argument(
        "--model",
        action="append",
        default=[],
        metavar="PROVIDER:MODEL",
        help=(
            "Inline model shorthand, e.g. openai:gpt-4.1-mini or "
            "ollama:qwen3:8b — no models file needed. Repeatable. API keys "
            "come from the environment or .env."
        ),
    )
    parser.add_argument(
        "--difficulty",
        choices=["all", "easy", "medium", "hard"],
        default="all",
        help="Scenario difficulty slice to run.",
    )
    parser.add_argument("--level", help="Optional level filter, e.g. L1 or L2.")
    parser.add_argument("--capability", help="Optional capability filter.")
    parser.add_argument("--workflow", help="Optional workflow filter.")
    parser.add_argument("--domain", help="Optional domain filter.")
    parser.add_argument("--subdomain", help="Optional subdomain filter.")
    parser.add_argument(
        "--pack", "--collection",
        dest="pack",
        default="core",
        choices=["all", *BUILTIN_SCENARIO_PACK_ORDER],
        help=(
            "Bundled scenario collection. core = operating the workspace; "
            "build-openbb-apps = building custom backend apps; all is a "
            "deprecated alias for core."
        ),
    )
    parser.add_argument(
        "--split",
        choices=sorted(VALID_SCENARIO_SPLITS),
        help="Optional scenario split filter.",
    )
    parser.add_argument(
        "--scenario-dir",
        help="Directory of scenario JSON files. Defaults to the bundled benchmark.",
    )
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Optional tag filter. Can be passed multiple times.",
    )
    parser.add_argument(
        "--scenario",
        action="append",
        default=[],
        help="Run only these scenario id(s). Can be passed multiple times.",
    )
    parser.add_argument(
        "--metric",
        choices=[
            "pass-rate",
            "task-pass-rate",
            "mean-score",
            "pass-at-k",
            "pass-power-k",
        ],
        default="pass-rate",
        help="Bar chart metric.",
    )
    parser.add_argument(
        "--runner",
        choices=["interactive", "batch"],
        default="interactive",
        help="Execution mode. interactive gives the model each tool result before the next call.",
    )
    parser.add_argument(
        "--color",
        choices=["auto", "always", "never"],
        default="auto",
        help="Colorize live PASS/FAIL output. Defaults to auto.",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        help="Override scenario max_turns for interactive runs.",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=1,
        help="Run each selected scenario this many times per model.",
    )
    parser.add_argument(
        "--model-retries",
        type=int,
        default=2,
        help="Retry transient model API failures this many times per turn.",
    )
    parser.add_argument(
        "--retry-backoff",
        type=float,
        default=1.0,
        help="Initial seconds to wait before retrying a transient model API failure.",
    )
    parser.add_argument(
        "--output-dir",
        help=(
            "Directory for raw model results, summary JSON, and charts. "
            "Defaults to runs/comparison/<timestamp>-<difficulty>."
        ),
    )
    parser.add_argument(
        "--run-name",
        help="Optional label used in the default timestamped output directory.",
    )
    parser.add_argument("--timeout", type=float, default=240)
    parser.add_argument(
        "--resume",
        action="store_true",
        help=(
            "Reuse completed scenario run directories already present in the "
            "output directory (interactive runner only): replay their recorded "
            "tool calls through a fresh simulator to regrade, and only run "
            "scenarios with no completed episode on disk."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print selected models and scenarios without running agents.",
    )
    args = parser.parse_args(argv)
    if args.repeats < 1:
        print("--repeats must be >= 1", file=sys.stderr)
        return 2
    if args.model_retries < 0:
        print("--model-retries must be >= 0", file=sys.stderr)
        return 2
    if args.retry_backoff < 0:
        print("--retry-backoff must be >= 0", file=sys.stderr)
        return 2

    try:
        adapters, configured_model_slugs = load_model_adapters(args.models_file)
    except (OSError, ValueError) as error:
        print(f"Invalid model adapter config: {error}", file=sys.stderr)
        return 2

    for spec in args.model:
        provider, _, model_name = spec.partition(":")
        if provider not in INTERACTIVE_PROVIDERS or not model_name:
            print(
                f"--model expects PROVIDER:MODEL with provider one of "
                f"{sorted(INTERACTIVE_PROVIDERS)}, got: {spec}",
                file=sys.stderr,
            )
            return 2
        slug = f"{provider}-{model_name}".replace(":", "-").replace("/", "-")
        adapters[slug] = ModelAdapter(
            slug=slug, label=model_name, command="",
            env={"OLLAMA_MODEL": model_name} if provider == "ollama" else {},
            provider=provider, model=model_name,
        )
        configured_model_slugs.append(slug)

    selected_model_slugs = args.models
    if selected_model_slugs is None:
        selected_model_slugs = (
            configured_model_slugs
            if configured_model_slugs
            else ["openai-gpt-4.1", "ollama-gpt-oss-20b"]
        )

    unknown_models = [slug for slug in selected_model_slugs if slug not in adapters]
    if unknown_models:
        print(
            f"Unknown model adapter(s): {', '.join(unknown_models)}. "
            f"Available: {', '.join(sorted(adapters))}",
            file=sys.stderr,
        )
        return 2

    scenarios = filter_scenarios(
        load_scenario_source(args),
        difficulty=args.difficulty,
        level=args.level,
        capability=args.capability,
        workflow=args.workflow,
        domain=args.domain,
        subdomain=args.subdomain,
        split=args.split,
        tags=args.tag,
        scenario_ids=args.scenario,
    )
    if not scenarios:
        print("No scenarios matched the selected filters.", file=sys.stderr)
        return 2

    selected_adapters = [adapters[slug] for slug in selected_model_slugs]
    provider_error = validate_adapters_for_runner(selected_adapters, runner=args.runner)
    if provider_error:
        print(provider_error, file=sys.stderr)
        return 2
    output_dir = resolve_output_dir(args)
    if args.dry_run:
        print_dry_run(selected_adapters, scenarios, args)
        print(f"Output directory would be: {output_dir}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    model_summaries = []

    for adapter in selected_adapters:
        total_attempts = len(scenarios) * args.repeats
        print(
            f"Running {adapter.label} on {len(scenarios)} scenario(s) "
            f"({total_attempts} attempt(s)) with {args.runner} runner...",
            file=sys.stderr,
        )
        runs = run_adapter(
            adapter,
            scenarios,
            output_dir,
            timeout=args.timeout,
            runner=args.runner,
            max_turns_override=args.max_turns,
            repeats=args.repeats,
            model_retries=args.model_retries,
            retry_backoff=args.retry_backoff,
            color=should_colorize(args.color, sys.stderr),
            resume=args.resume,
        )
        result_payload = model_result_payload(adapter, scenarios, runs, args)
        result_path = output_dir / f"{adapter.slug}.json"
        result_path.write_text(
            json.dumps(result_payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        summary = result_payload["summary"]
        summary["result_path"] = str(result_path)
        model_summaries.append({"model": adapter.label, "slug": adapter.slug, **summary})

    comparison = {
        "benchmark": benchmark_metadata(args),
        "filters": selected_filters(args),
        "runner": args.runner,
        "max_turns_override": args.max_turns,
        "repeats": args.repeats,
        "model_retries": args.model_retries,
        "retry_backoff": args.retry_backoff,
        "metric": args.metric,
        "models_file": args.models_file,
        "scenario_count": len(scenarios),
        "attempt_count": len(scenarios) * args.repeats,
        "models": model_summaries,
    }
    comparison_path = output_dir / "comparison.json"
    comparison_path.write_text(
        json.dumps(comparison, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    analysis_path = output_dir / "analysis.md"
    analysis_path.write_text(
        render_analysis_report(comparison, output_dir),
        encoding="utf-8",
    )

    chart_path = output_dir / "chart.svg"
    chart_path.write_text(render_svg_chart(comparison), encoding="utf-8")
    png_path = output_dir / "chart.png"
    png_result = export_png(chart_path, png_path)

    print(f"Wrote comparison summary: {comparison_path}")
    print(f"Wrote analysis report: {analysis_path}")
    print(f"Wrote chart: {chart_path}")
    if png_result:
        print(f"Wrote PNG chart: {png_path}")
    else:
        print(
            "PNG chart was not generated. Install ImageMagick or run "
            f"`qlmanage -t -s 1200 -o {output_dir} {chart_path}`."
        )
    for model in model_summaries:
        print(
            f"{model['model']}: {model['passed']}/{model['total']} passed, "
            f"pass_rate={model['pass_rate']:.1%}, "
            f"task_pass_rate={model['task_pass_rate']:.1%}, "
            f"mean_score={model['mean_score']:.1%}, "
            f"task_failures={model['task_failures']}, "
            f"process_failures={model['process_failures']}"
        )
    return 0


def load_model_adapters(
    models_file: str | None = None,
) -> tuple[dict[str, ModelAdapter], list[str]]:
    """Load built-in adapters plus optional adapters from a JSON config file."""

    adapters = default_adapters()
    configured_slugs: list[str] = []
    if not models_file:
        return adapters, configured_slugs

    path = Path(models_file)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("top-level config must be a JSON object")
    models = payload.get("models")
    if not isinstance(models, list) or not models:
        raise ValueError("config requires a non-empty models list")

    for index, item in enumerate(models, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"models[{index}] must be an object")
        adapter = model_adapter_from_config(item, index=index)
        adapters[adapter.slug] = adapter
        configured_slugs.append(adapter.slug)
    return adapters, configured_slugs


def model_adapter_from_config(payload: JsonDict, *, index: int) -> ModelAdapter:
    slug = payload.get("slug")
    label = payload.get("label", slug)
    provider = payload.get("provider")
    model = payload.get("model")
    command = payload.get("command", "")
    env = payload.get("env", {})
    if not isinstance(slug, str) or not slug:
        raise ValueError(f"models[{index}].slug must be a non-empty string")
    if not isinstance(label, str) or not label:
        raise ValueError(f"models[{index}].label must be a non-empty string")
    if not isinstance(provider, str) or not provider:
        raise ValueError(f"models[{index}].provider must be a non-empty string")
    if not isinstance(model, str) or not model:
        raise ValueError(f"models[{index}].model must be a non-empty string")
    if not isinstance(command, str):
        raise ValueError(f"models[{index}].command must be a string when set")
    if not isinstance(env, dict):
        raise ValueError(f"models[{index}].env must be an object")
    return ModelAdapter(
        slug=slug,
        label=label,
        command=command,
        env={str(key): str(value) for key, value in env.items()},
        provider=provider,
        model=model,
    )


def validate_adapters_for_runner(
    adapters: list[ModelAdapter],
    *,
    runner: str,
) -> str | None:
    """Return a user-facing validation error for unsupported runner/provider combos."""

    if runner == "interactive":
        unsupported = [
            adapter
            for adapter in adapters
            if adapter.provider not in INTERACTIVE_PROVIDERS
        ]
        if unsupported:
            labels = ", ".join(
                f"{adapter.slug} ({adapter.provider})" for adapter in unsupported
            )
            return (
                "Interactive runner only supports provider values "
                f"{', '.join(sorted(INTERACTIVE_PROVIDERS))}; unsupported: {labels}"
            )
    if runner == "batch":
        missing_command = [adapter.slug for adapter in adapters if not adapter.command]
        if missing_command:
            return (
                "Batch runner requires command for every adapter; missing command for "
                f"{', '.join(missing_command)}"
            )
    return None


def export_png(svg_path: Path, png_path: Path) -> bool:
    """Export SVG to PNG with available local tools."""

    if shutil.which("qlmanage"):
        thumbnail_path = svg_path.parent / f"{svg_path.name}.png"
        completed = subprocess.run(
            [
                "qlmanage",
                "-t",
                "-s",
                "1400",
                "-o",
                str(svg_path.parent),
                str(svg_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode == 0 and thumbnail_path.exists():
            if png_path.exists():
                png_path.unlink()
            thumbnail_path.replace(png_path)
            return True

    magick = shutil.which("magick") or shutil.which("convert")
    if magick:
        command = [magick, str(svg_path), str(png_path)]
        if Path(magick).name == "convert":
            command = [magick, str(svg_path), str(png_path)]
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        return completed.returncode == 0 and png_path.exists()

    return False


def filter_scenarios(
    scenarios: list[Scenario],
    *,
    difficulty: str,
    level: str | None,
    capability: str | None,
    workflow: str | None,
    domain: str | None,
    subdomain: str | None,
    split: str | None,
    tags: list[str],
    scenario_ids: list[str] | None = None,
) -> list[Scenario]:
    if scenario_ids:
        wanted = set(scenario_ids)
        scenarios = [scenario for scenario in scenarios if scenario.id in wanted]
    if difficulty != "all":
        scenarios = [scenario for scenario in scenarios if scenario.difficulty == difficulty]
    if level:
        scenarios = [scenario for scenario in scenarios if scenario.level == level]
    if capability:
        scenarios = [scenario for scenario in scenarios if scenario.capability == capability]
    if workflow:
        scenarios = [scenario for scenario in scenarios if scenario.workflow == workflow]
    if domain:
        scenarios = [scenario for scenario in scenarios if scenario.domain == domain]
    if subdomain:
        scenarios = [scenario for scenario in scenarios if scenario.subdomain == subdomain]
    if split:
        scenarios = [scenario for scenario in scenarios if scenario.split == split]
    for tag in tags:
        scenarios = [scenario for scenario in scenarios if tag in scenario.tags]
    return scenarios


def load_scenario_source(args: argparse.Namespace) -> list[Scenario]:
    scenario_dir = getattr(args, "scenario_dir", None)
    if scenario_dir:
        return load_scenario_directory(Path(scenario_dir))
    pack = getattr(args, "pack", "core")
    # `--scenario <id>` should just work without naming the collection:
    # when ids are given and the pack was left at its default, search every
    # bundled collection for them.
    if getattr(args, "scenario", None) and pack == "core":
        scenarios: list[Scenario] = []
        seen: set[str] = set()
        for name in BUILTIN_SCENARIO_PACK_ORDER:
            for scenario in load_builtin_scenarios(name):
                if scenario.id not in seen:
                    seen.add(scenario.id)
                    scenarios.append(scenario)
        return scenarios
    return load_builtin_scenarios(pack)


def print_dry_run(
    adapters: list[ModelAdapter], scenarios: list[Scenario], args: argparse.Namespace
) -> None:
    print(f"Runner: {args.runner}")
    print(f"Repeats: {args.repeats}")
    print(f"Model retries: {args.model_retries}")
    print("Models:")
    for adapter in adapters:
        print(f"  - {adapter.slug}: {adapter.label}")
    print(f"Scenarios ({len(scenarios)}) for filters {selected_filters(args)}:")
    for scenario in scenarios:
        print(
            f"  - {scenario.id}\t{scenario.level}\t"
            f"{scenario.difficulty}\t{scenario.split}\t"
            f"{scenario.capability}\t{scenario.workflow}\t"
            f"{scenario.domain}\t{scenario.subdomain}"
        )


def run_adapter(
    adapter: ModelAdapter,
    scenarios: list[Scenario],
    output_dir: Path,
    *,
    timeout: float,
    runner: str,
    max_turns_override: int | None,
    repeats: int,
    model_retries: int,
    retry_backoff: float,
    color: bool,
    resume: bool = False,
) -> list[ComparisonRun]:
    runs = []
    total_attempts = len(scenarios) * repeats
    attempt_index = 0
    resumed_count = 0
    with patched_env(adapter.env):
        for repeat in range(1, repeats + 1):
            for scenario in scenarios:
                attempt_index += 1
                repeat_label = f" repeat {repeat}/{repeats}" if repeats > 1 else ""
                print(
                    f"  [{attempt_index}/{total_attempts}] {scenario.id}{repeat_label} ...",
                    file=sys.stderr,
                    flush=True,
                )
                run_dir = scenario_run_dir(
                    output_dir / adapter.slug,
                    scenario.id,
                    repeat=repeat,
                    repeats=repeats,
                )
                if resume and runner == "interactive":
                    run = replay_completed_run(
                        adapter, scenario, run_dir, repeat=repeat
                    )
                    if run is not None:
                        runs.append(run)
                        resumed_count += 1
                        print(
                            "    "
                            f"{run_status(run, color=color)} "
                            f"score={run.run_result.grade.score:.2f} "
                            f"checks={run.run_result.grade.checks_passed}/"
                            f"{run.run_result.grade.checks_total} "
                            "(resumed from disk)",
                            file=sys.stderr,
                            flush=True,
                        )
                        continue
                if runner == "batch":
                    run = batch_comparison_run(
                        run_agent_command(
                            scenario=scenario,
                            command=adapter.command,
                            timeout_seconds=timeout,
                            run_dir=run_dir,
                        ),
                        repeat=repeat,
                    )
                else:
                    run = run_interactive_agent(
                        adapter=adapter,
                        scenario=scenario,
                        run_dir=run_dir,
                        timeout=timeout,
                        max_turns_override=max_turns_override,
                        model_retries=model_retries,
                        retry_backoff=retry_backoff,
                        repeat=repeat,
                    )
                runs.append(run)
                print(
                    "    "
                    f"{run_status(run, color=color)} "
                    f"score={run.run_result.grade.score:.2f} "
                    f"checks={run.run_result.grade.checks_passed}/"
                    f"{run.run_result.grade.checks_total} "
                    f"exit={run.exit_code} timeout={run.timed_out}",
                    file=sys.stderr,
                    flush=True,
                )
    if resumed_count:
        print(
            f"  resumed {resumed_count}/{total_attempts} attempt(s) from disk",
            file=sys.stderr,
            flush=True,
        )
    return runs


def replay_completed_run(
    adapter: ModelAdapter,
    scenario: Scenario,
    run_dir: Path,
    *,
    repeat: int = 1,
) -> ComparisonRun | None:
    """Rebuild a ComparisonRun from a completed episode already on disk.

    conversation.json is written only after the turn loop finishes, so its
    presence marks a completed episode; a run killed mid-scenario lacks it and
    re-runs live. tool_calls.jsonl records each executed call after
    normalization, and the simulator is deterministic, so replaying the calls
    into a fresh episode reproduces the exact final state, trace, and grade.
    """

    conversation_path = run_dir / "conversation.json"
    task_path = run_dir / "task.json"
    output_path = run_dir / "tool_calls.jsonl"
    meta_path = run_dir / "run_meta.json"
    if not conversation_path.exists() or not task_path.exists():
        return None
    # strict pass folds in exit_code/timed_out, which only run_meta.json
    # records — without it a crashed-but-graded episode would silently flip
    # to a pass on resume, so re-run live instead.
    if not meta_path.exists():
        return None
    try:
        meta: JsonDict = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    episode = WorkspaceEpisode(scenario=scenario)
    if output_path.exists():
        for line in output_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            payload = json.loads(line)
            episode.step(ToolCall(payload["tool"], payload["args"]))
    return ComparisonRun(
        run_result=RunResult(
            scenario=scenario,
            grade=episode.grade(),
            trace=tuple(episode.trace),
            final_snapshot=episode.snapshot(),
        ),
        command=f"interactive:{adapter.provider}:{adapter.model}",
        exit_code=meta.get("exit_code", 0),
        timed_out=bool(meta.get("timed_out", False)),
        stdout=str(meta.get("stdout", "")),
        stderr=str(meta.get("stderr", "")),
        run_dir=run_dir,
        task_path=task_path,
        output_path=output_path,
        runner="interactive",
        repeat=repeat,
    )


def scenario_run_dir(base_dir: Path, scenario_id: str, *, repeat: int, repeats: int) -> Path:
    if repeats == 1:
        return base_dir / scenario_id
    return base_dir / scenario_id / f"repeat_{repeat:02d}"


def batch_comparison_run(run: AgentCommandRun, *, repeat: int = 1) -> ComparisonRun:
    return ComparisonRun(
        run_result=run.run_result,
        command=run.command,
        exit_code=run.exit_code,
        timed_out=run.timed_out,
        stdout=run.stdout,
        stderr=run.stderr,
        run_dir=run.run_dir,
        task_path=run.task_path,
        output_path=run.output_path,
        runner="batch",
        repeat=repeat,
    )


def run_interactive_agent(
    *,
    adapter: ModelAdapter,
    scenario: Scenario,
    run_dir: Path,
    timeout: float,
    max_turns_override: int | None,
    model_retries: int,
    retry_backoff: float,
    repeat: int = 1,
) -> ComparisonRun:
    run_dir.mkdir(parents=True, exist_ok=True)
    task_path = run_dir / "task.json"
    output_path = run_dir / "tool_calls.jsonl"
    conversation_path = run_dir / "conversation.json"
    responses_path = run_dir / "model_responses.jsonl"
    task_payload = build_task_envelope(scenario)
    origin_hints = fixture_origin_hints(task_payload["scenario"]["fixtures"])
    task_path.write_text(
        json.dumps(task_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if output_path.exists():
        output_path.unlink()
    if responses_path.exists():
        responses_path.unlink()

    episode = WorkspaceEpisode(scenario=scenario)
    messages = build_interactive_messages(task_payload)
    max_turns = max_turns_override or int(scenario.limits.get("max_turns", 12))
    stdout_lines: list[str] = []
    stderr = ""
    exit_code: int | None = 0
    timed_out = False

    malformed_recoveries = 0
    for turn in range(1, max_turns + 1):
        try:
            content = call_model_with_retries(
                adapter,
                messages,
                timeout=timeout,
                retries=model_retries,
                backoff_seconds=retry_backoff,
                retry_log=stdout_lines,
                turn=turn,
            )
        except TimeoutError as error:
            timed_out = True
            exit_code = None
            stderr = str(error)
            break
        except Exception as error:  # noqa: BLE001 - model API failure is run output.
            exit_code = 1
            stderr = str(error)
            break
        try:
            action = parse_interactive_action(content)
        except Exception as error:  # noqa: BLE001 - malformed model action.
            # Teaching turn, mirroring invalid-tool-call rejections: a malformed
            # action costs a turn (and patience), not the episode. Two strikes.
            malformed_recoveries += 1
            if malformed_recoveries > 2:
                exit_code = 1
                stderr = str(error)
                break
            stdout_lines.append(
                f"turn {turn}: malformed action recovered ({error})"
            )
            messages.append({"role": "assistant", "content": content})
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "Your last response could not be parsed as a single "
                        f"JSON action ({error}). Reply with exactly one JSON "
                        'object: {"tool": "<name>", "args": {...}} or '
                        '{"done": true} — no prose, no second object.'
                    ),
                }
            )
            continue

        append_jsonl(
            responses_path,
            {
                "turn": turn,
                "content": content,
                "action": action,
            },
        )
        messages.append({"role": "assistant", "content": content})

        if action.get("done") is True:
            stdout_lines.append(f"done at turn {turn}")
            break

        tool_name = action.get("tool")
        args = action.get("args", {})
        if not isinstance(tool_name, str) or not tool_name:
            exit_code = 1
            stderr = f"turn {turn} did not include a tool name"
            break
        if not isinstance(args, dict):
            exit_code = 1
            stderr = f"turn {turn} args must be an object"
            break
        tool_name = normalize_tool_name(tool_name)
        args = normalize_interactive_args(args, origin_hints)

        call = ToolCall(tool_name, args)
        result = episode.step(call)
        append_jsonl(output_path, {"tool": call.name, "args": call.args})
        messages.append(
            {
                "role": "user",
                "content": tool_result_prompt(turn, call, result),
            }
        )
    else:
        stdout_lines.append(f"reached max_turns={max_turns}")

    final_snapshot = episode.snapshot()
    grade = episode.grade()
    conversation_path.write_text(
        json.dumps(messages, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    meta_path = run_dir / "run_meta.json"
    meta_path.write_text(
        json.dumps(
            {
                "exit_code": exit_code,
                "timed_out": timed_out,
                "stdout": "\n".join(stdout_lines),
                "stderr": stderr,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return ComparisonRun(
        run_result=RunResult(
            scenario=scenario,
            grade=grade,
            trace=tuple(episode.trace),
            final_snapshot=final_snapshot,
        ),
        command=f"interactive:{adapter.provider}:{adapter.model}",
        exit_code=exit_code,
        timed_out=timed_out,
        stdout="\n".join(stdout_lines),
        stderr=stderr,
        run_dir=run_dir,
        task_path=task_path,
        output_path=output_path,
        runner="interactive",
        repeat=repeat,
    )


def build_interactive_messages(task: JsonDict) -> list[JsonDict]:
    scenario = task["scenario"]
    allowed_tools = scenario["allowed_tools"]
    origin_hints = fixture_origin_hints(scenario["fixtures"])
    widget_tool_names = {
        "list_available_widgets",
        "get_widget_schema",
        "get_widget_data",
        "get_params_options",
        "create_widget",
    }
    widget_hints = (
        fixture_widget_hints(origin_hints)
        if widget_tool_names.intersection(allowed_tools)
        else {}
    )
    tool_reference = {
        name: TOOL_REFERENCE[name]
        for name in allowed_tools
        if name in TOOL_REFERENCE
    }
    public_task = {
        "id": scenario["id"],
        "title": scenario["title"],
        "level": scenario["level"],
        "capability": scenario["capability"],
        "workflow": scenario["workflow"],
        "domain": scenario["domain"],
        "subdomain": scenario["subdomain"],
        "difficulty": scenario["difficulty"],
        "prompt": scenario["prompt"],
        "fixtures": scenario["fixtures"],
        "origin_hints": origin_hints,
        "widget_hints": widget_hints,
        "initial_state": scenario["initial_state"],
        "allowed_tools": allowed_tools,
        "limits": scenario.get("limits", {}),
    }
    system = "\n".join(
        [
            "You are controlling OpenBB Workspace through tool calls.",
            "This is an interactive eval. You will choose one tool call at a time.",
            "After each tool call, you will receive the real tool result.",
            "Return only valid JSON. Do not use Markdown or prose.",
            "",
            "Response schema:",
            '{"done": false, "tool": "tool_name", "args": {}}',
            "or",
            '{"done": true}',
            "",
            "Use only allowed tools.",
            "Tool names must exactly match allowed_tools. Do not call shell, container, browser, or developer tools.",
            "When a tool asks for origin, use the display origin from origin_hints, not the fixture slug.",
            "Use IDs returned by tool results exactly. Do not use placeholders like {{dashboard_id}}.",
            "If dashboard_id is optional and you do not know the UUID, omit it instead of using a dashboard name.",
            "Never invent widget_id values. Use exact widget_id values from list_available_widgets, widget_hints, or prior tool results.",
            "Before create_widget, you MUST call list_available_widgets for the same origin when that tool is allowed.",
            "Before create_widget, you MUST call get_widget_schema for the same origin and widget_id when that tool is allowed.",
            "Calling create_widget before list_available_widgets and get_widget_schema will fail the benchmark.",
            "For tabbed dashboards, navigate to the target tab before creating widgets or set layout tab_id correctly.",
            "For app templates, call manage_backends list, then use the returned backend id in manage_apps.",
            "For generated notes/charts, include concrete task facts from tool data and put the widget on the required tab when applicable.",
            "Generated widget text is checked literally. Copy exact numbers and identifiers from observations: write 0.86, not 86%; write price_performance, not only Price Performance.",
            "Use update_widget_layout for layout changes, not update_widget.",
            "When the final Workspace state satisfies the task, return {\"done\": true}.",
        ]
    )
    user = "\n".join(
        [
            "Available tool reference:",
            json.dumps(tool_reference, indent=2, sort_keys=True),
            "",
            "Task:",
            json.dumps(public_task, indent=2, sort_keys=True),
            "",
            "Choose the first tool call.",
        ]
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def tool_result_prompt(turn: int, call: ToolCall, result: JsonDict) -> str:
    return "\n".join(
        [
            f"Tool result for turn {turn}:",
            json.dumps(
                {
                    "tool": call.name,
                    "args": call.args,
                    "result": result,
                },
                indent=2,
                sort_keys=True,
            ),
            "",
            "Choose the next single tool call, or return {\"done\": true} if the task is complete.",
        ]
    )


def call_model(adapter: ModelAdapter, messages: list[JsonDict], timeout: float) -> str:
    if adapter.provider == "openai":
        return call_openai_chat(adapter.model, messages, timeout)
    if adapter.provider == "ollama":
        return call_ollama_chat(adapter.model, messages, timeout)
    raise ValueError(f"Unsupported provider {adapter.provider!r}")


def call_model_with_retries(
    adapter: ModelAdapter,
    messages: list[JsonDict],
    *,
    timeout: float,
    retries: int,
    backoff_seconds: float,
    retry_log: list[str],
    turn: int,
) -> str:
    attempt = 0
    while True:
        try:
            return call_model(adapter, messages, timeout=timeout)
        except TransientModelError as error:
            if attempt >= retries:
                raise
            attempt += 1
            wait_seconds = backoff_seconds * (2 ** (attempt - 1))
            retry_log.append(
                f"turn {turn} retry {attempt}/{retries} after transient model error: {error}"
            )
            if wait_seconds:
                time.sleep(wait_seconds)
        except TimeoutError as error:
            if attempt >= retries:
                raise
            attempt += 1
            wait_seconds = backoff_seconds * (2 ** (attempt - 1))
            retry_log.append(
                f"turn {turn} retry {attempt}/{retries} after model timeout: {error}"
            )
            if wait_seconds:
                time.sleep(wait_seconds)


def call_openai_chat(model: str, messages: list[JsonDict], timeout: float) -> str:
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in the environment or .env")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    payload = {
        "model": model,
        "temperature": float(os.environ.get("OPENAI_TEMPERATURE", "0")),
        "messages": messages,
    }
    # Some OpenAI-compatible providers (e.g. Anthropic models behind
    # OpenRouter/Bedrock) degrade to schema-minimal outputs under
    # json_schema response_format; allow opting out per adapter.
    if os.environ.get("OPENAI_RESPONSE_FORMAT", "json_schema") != "none":
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "workspace_next_action",
                "schema": interactive_action_schema(),
                "strict": False,
            },
        }
    body = post_json(
        f"{base_url}/chat/completions",
        payload,
        timeout,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    try:
        content = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError(f"OpenAI returned no message content: {body!r}") from error
    if not isinstance(content, str) or not content.strip():
        raise ValueError(f"OpenAI returned empty message content: {body!r}")
    return content


def call_ollama_chat(model: str, messages: list[JsonDict], timeout: float) -> str:
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    payload = {
        "model": os.environ.get("OLLAMA_MODEL", model),
        "stream": False,
        "options": {"temperature": float(os.environ.get("OLLAMA_TEMPERATURE", "0"))},
        "messages": messages,
    }
    # Same escape hatch as OPENAI_RESPONSE_FORMAT: some generations 500 inside
    # ollama's schema-grammar sampler; format=none falls back to unconstrained
    # JSON (the teaching-turn recovery backstops malformed output).
    if os.environ.get("OLLAMA_FORMAT", "schema") != "none":
        payload["format"] = interactive_action_schema()
    body = post_json(f"{base_url}/api/chat", payload, timeout)
    message = body.get("message") or {}
    content = message.get("content")
    if isinstance(content, str) and content.strip():
        return content
    tool_calls = message.get("tool_calls")
    if isinstance(tool_calls, list) and tool_calls:
        return json.dumps(native_tool_call_to_action(tool_calls[0]), sort_keys=True)
    if not isinstance(content, str) or not content.strip():
        raise ValueError(f"Ollama returned no message content: {body!r}")
    return content


def post_json(
    url: str,
    payload: JsonDict,
    timeout: float,
    headers: dict[str, str] | None = None,
) -> JsonDict:
    data = json.dumps(payload).encode("utf-8")
    request_headers = {"Content-Type": "application/json"}
    request_headers.update(headers or {})
    request = urllib.request.Request(
        url,
        data=data,
        headers=request_headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except TimeoutError:
        raise
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        message = f"model API request failed: HTTP {error.code}: {detail}"
        if is_transient_http_status(error.code):
            raise TransientModelError(message, status_code=error.code) from error
        raise RuntimeError(message) from error
    except urllib.error.URLError as error:
        raise TransientModelError(
            f"could not reach model API at {url}: {error.reason}"
        ) from error
    except (ConnectionError, OSError, ssl.SSLError) as error:
        raise TransientModelError(
            f"transient model API transport error at {url}: {error}"
        ) from error


def is_transient_http_status(status_code: int) -> bool:
    return status_code in {408, 409, 425, 429, 500, 502, 503, 504, 520, 529}


def parse_interactive_action(content: str) -> JsonDict:
    text = strip_code_fence(content.strip())
    # Lenient parse: accept the FIRST JSON object and tolerate trailing data
    # (models sometimes emit a second object or prose after the action; the
    # protocol takes one action per turn, so extra data is ignored, not fatal).
    payload, end = json.JSONDecoder().raw_decode(text)
    if not isinstance(payload, dict):
        raise ValueError("model output must be a JSON object")
    if payload.get("done") is True:
        return {"done": True}
    if "tool_calls" in payload and isinstance(payload["tool_calls"], list):
        if not payload["tool_calls"]:
            raise ValueError("tool_calls must not be empty")
        return native_tool_call_to_action(payload["tool_calls"][0])
    if "tool_call" in payload and isinstance(payload["tool_call"], dict):
        payload = payload["tool_call"]
    if "function" in payload and isinstance(payload["function"], dict):
        return native_tool_call_to_action(payload)
    args = payload.get("args", payload.get("arguments", {}))
    if isinstance(args, str):
        args = json.loads(args)
    tool_name = normalize_tool_name(payload.get("tool") or payload.get("name"))
    if (
        isinstance(args, dict)
        and tool_name not in TOOL_REFERENCE
        and (args.get("tool") or args.get("name"))
    ):
        payload = args
        if payload.get("done") is True:
            return {"done": True}
        args = payload.get("args", payload.get("arguments", {}))
        if isinstance(args, str):
            args = json.loads(args)
        tool_name = normalize_tool_name(payload.get("tool") or payload.get("name"))
    return {
        "done": False,
        "tool": tool_name,
        "args": args,
    }


def native_tool_call_to_action(tool_call: JsonDict) -> JsonDict:
    function = tool_call.get("function")
    if isinstance(function, dict):
        tool_name = function.get("name")
        args = function.get("arguments", {})
    else:
        tool_name = tool_call.get("tool") or tool_call.get("name")
        args = tool_call.get("args", tool_call.get("arguments", {}))
    if isinstance(args, str):
        args = json.loads(args)
    return {
        "done": False,
        "tool": normalize_tool_name(tool_name),
        "args": args,
    }


def normalize_tool_name(tool_name: Any) -> Any:
    if not isinstance(tool_name, str):
        return tool_name
    tool_name = tool_name.strip().strip("`\"'“”‘’")
    for prefix in ("tool.", "function.", "functions."):
        if tool_name.startswith(prefix):
            return tool_name[len(prefix) :]
    if tool_name.startswith("tool_"):
        suffix = tool_name[len("tool_") :]
        if suffix in TOOL_REFERENCE:
            return suffix
    if "." in tool_name:
        suffix = tool_name.rsplit(".", 1)[1]
        if suffix in TOOL_REFERENCE:
            return suffix
    return tool_name


def normalize_interactive_args(
    args: JsonDict,
    origin_hints: dict[str, str],
) -> JsonDict:
    normalized = copy.deepcopy(args)
    origin_lookup = dict(origin_hints)
    origin_lookup.update({display: display for display in origin_hints.values()})
    origin_lookup.update({key.lower(): value for key, value in origin_lookup.items()})
    for key in ("origin", "backend_name"):
        value = normalized.get(key)
        if isinstance(value, str):
            normalized[key] = origin_lookup.get(value, origin_lookup.get(value.lower(), value))
    return normalized


def interactive_action_schema() -> JsonDict:
    return {
        "type": "object",
        "properties": {
            "done": {"type": "boolean"},
            "tool": {"type": "string"},
            "args": {"type": "object"},
        },
        "required": ["done"],
        "additionalProperties": False,
    }


def append_jsonl(path: Path, payload: JsonDict) -> None:
    # No sort_keys: tool-call args are replayed through the simulator on
    # --resume, and dict order is semantic there (app tabs/layout iteration
    # assigns widget uuids in order) — sorting keys breaks replay fidelity.
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def run_status(run: ComparisonRun, *, color: bool = False) -> str:
    if agent_run_passed(run):
        return colorize("[PASS]", "green", enabled=color)
    return colorize("[FAIL]", "red", enabled=color)


def colorize(text: str, color: str, *, enabled: bool) -> str:
    if not enabled:
        return text
    codes = {"green": "32", "red": "31"}
    return f"\033[{codes[color]}m{text}\033[0m"


def should_colorize(mode: str, stream: Any) -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if mode == "always":
        return True
    if mode == "never":
        return False
    return bool(getattr(stream, "isatty", lambda: False)())


@contextmanager
def patched_env(env: dict[str, str]) -> Iterator[None]:
    previous = {key: os.environ.get(key) for key in env}
    os.environ.update(env)
    try:
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def model_result_payload(
    adapter: ModelAdapter,
    scenarios: list[Scenario],
    runs: list[ComparisonRun],
    args: argparse.Namespace,
) -> dict:
    return {
        "benchmark": benchmark_metadata(args),
        "model": {"slug": adapter.slug, "label": adapter.label},
        "filters": selected_filters(args),
        "runner": args.runner,
        "repeats": args.repeats,
        "model_retries": args.model_retries,
        "summary": summarize_runs(runs),
        "results": [agent_run_summary(run) for run in runs],
        "scenarios": [scenario.id for scenario in scenarios],
    }


def render_analysis_report(comparison: dict, output_dir: Path) -> str:
    model_payloads = []
    for model in comparison["models"]:
        result_path = Path(model["result_path"])
        if not result_path.is_absolute():
            result_path = REPO_ROOT / result_path
        model_payloads.append(json.loads(result_path.read_text(encoding="utf-8")))

    lines = [
        "# Workspace Bench Model Comparison",
        "",
        f"- Benchmark: `{comparison['benchmark']['name']}`",
        f"- Release: `{comparison['benchmark']['release_id']}`",
        f"- Scenarios: `{comparison['scenario_count']}`",
        f"- Attempts: `{comparison.get('attempt_count', comparison['scenario_count'])}`",
        f"- Filters: `{json.dumps(comparison['filters'], sort_keys=True)}`",
        f"- Runner: `{comparison['runner']}`",
        f"- Repeats: `{comparison.get('repeats', 1)}`",
        "",
        "## How To Read This",
        "",
        "`pass_rate` is strict scenario success: a scenario counts as passed only when every grader check passes and the agent process exits cleanly.",
        "`task_pass_rate` excludes provider/process failures and asks whether valid attempts satisfied the grader.",
        "`mean_score` is partial credit: it averages each scenario's fraction of passed checks.",
        "`pass@k` counts a scenario when at least one repeat passes. `pass^k` counts it only when every repeat passes.",
        "Two models can therefore have the same pass rate but different mean scores when they pass the same number of scenarios but fail with different severity.",
        "",
        "## Summary",
        "",
        "| Model | Strict Passed | Attempts | Strict Pass Rate | Task Pass Rate | Mean Score | Task Failures | Process Failures |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in comparison["models"]:
        lines.append(
            "| "
            f"{model['model']} | "
            f"{model['passed']} | "
            f"{model['total']} | "
            f"{model['pass_rate']:.1%} | "
            f"{model.get('task_pass_rate', model['pass_rate']):.1%} | "
            f"{model['mean_score']:.1%} | "
            f"{model.get('task_failures', model['failed'])} | "
            f"{model['process_failures']} |"
        )

    if comparison.get("repeats", 1) > 1:
        lines.extend(
            [
                "",
                "## Reliability",
                "",
                "| Model | pass@k | pass^k | Scenarios | k Range |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for model in comparison["models"]:
            k_min = model.get("reliability_min_k", 0)
            k_max = model.get("reliability_max_k", 0)
            k_range = str(k_min) if k_min == k_max else f"{k_min}-{k_max}"
            lines.append(
                "| "
                f"{model['model']} | "
                f"{model.get('pass_at_k', 0.0):.1%} | "
                f"{model.get('pass_power_k', 0.0):.1%} | "
                f"{model.get('reliability_scenario_count', 0)} | "
                f"{k_range} |"
            )

    lines.extend(["", "## By Difficulty", "", "| Model | Easy | Medium | Hard |", "| --- | ---: | ---: | ---: |"])
    for model in comparison["models"]:
        by_difficulty = model.get("by_difficulty", {})
        lines.append(
            "| "
            f"{model['model']} | "
            f"{format_bucket(by_difficulty.get('easy'))} | "
            f"{format_bucket(by_difficulty.get('medium'))} | "
            f"{format_bucket(by_difficulty.get('hard'))} |"
        )

    lines.extend(["", "## By Level", "", "| Model | L0 | L1 | L2 | L3 | L4 |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
    for model in comparison["models"]:
        by_level = model.get("by_level", {})
        lines.append(
            "| "
            f"{model['model']} | "
            f"{format_bucket(by_level.get('L0'))} | "
            f"{format_bucket(by_level.get('L1'))} | "
            f"{format_bucket(by_level.get('L2'))} | "
            f"{format_bucket(by_level.get('L3'))} | "
            f"{format_bucket(by_level.get('L4'))} |"
        )

    lines.extend(["", "## Task Issue Counts", ""])
    for payload in model_payloads:
        label = payload["model"]["label"]
        issue_counts = Counter(
            issue["code"]
            for result in payload["results"]
            for issue in result["issues"]
        )
        lines.append(f"### {label}")
        if not issue_counts:
            lines.append("")
            lines.append("No grader issues.")
            lines.append("")
            continue
        lines.extend(["", "| Issue Code | Count |", "| --- | ---: |"])
        for code, count in issue_counts.most_common():
            lines.append(f"| `{code}` | {count} |")
        lines.append("")

    lines.extend(
        [
            "## Process Failures",
            "",
            "| Model | Scenario | Repeat | Exit Code | Timed Out | Stderr Preview |",
            "| --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    process_rows = process_failure_rows(model_payloads)
    if process_rows:
        for row in process_rows:
            lines.append(
                "| "
                f"{row['model']} | "
                f"{row['scenario']} | "
                f"{row['repeat']} | "
                f"{row['exit_code']} | "
                f"{row['timed_out']} | "
                f"{row['stderr_preview']} |"
            )
    else:
        lines.append("| - | - | - | - | - | No provider or process failures. |")
    lines.append("")

    lines.extend(
        [
            "## Scenario Matrix",
            "",
            "| Scenario | Level | Difficulty | Capability | Workflow | Domain | Subdomain | "
            + " | ".join(payload["model"]["label"] for payload in model_payloads)
            + " |",
            "| --- | --- | --- | --- | --- | --- | --- | "
            + " | ".join("---:" for _ in model_payloads)
            + " |",
        ]
    )
    scenario_ids = model_payloads[0]["scenarios"] if model_payloads else []
    results_by_model = [results_grouped_by_scenario(payload) for payload in model_payloads]
    for scenario_id in scenario_ids:
        first = results_by_model[0][scenario_id][0]
        cells = []
        for results in results_by_model:
            cells.append(format_result_cell(results[scenario_id]))
        lines.append(
            "| "
            f"{scenario_id} | "
            f"{first['level']} | "
            f"{first['difficulty']} | "
            f"{first['capability']} | "
            f"{first['workflow']} | "
            f"{first['domain']} | "
            f"{first['subdomain']} | "
            + " | ".join(cells)
            + " |"
        )

    lines.extend(
        [
            "",
            "## Common Interpretation",
            "",
            "- Missing generated-widget failures often mean the model added no note/chart, added it to the wrong tab, or wrote placeholder text that did not include required task facts.",
            "- Missing-widget and missing-tab failures are common on multi-widget dashboard tasks when the model chooses the wrong widget, tab, or data arguments.",
            "- Invalid-call failures usually mean the model emitted a malformed tool name, used unresolved placeholders, or ignored an ID returned by an earlier observation.",
            "- In batch mode, app-template tasks are especially sensitive to backend IDs because the model cannot read `manage_backends` output before calling `manage_apps`.",
            "",
            f"Raw outputs are under `{output_dir}`.",
            "",
        ]
    )
    return "\n".join(lines)


def results_grouped_by_scenario(payload: dict) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for result in payload["results"]:
        grouped.setdefault(result["id"], []).append(result)
    return grouped


def process_failure_rows(model_payloads: list[dict]) -> list[dict]:
    rows = []
    for payload in model_payloads:
        label = payload["model"]["label"]
        for result in payload["results"]:
            if not result.get("process_failed"):
                continue
            stderr = str(result.get("agent_stderr") or "").replace("\n", " ")
            rows.append(
                {
                    "model": label,
                    "scenario": result["id"],
                    "repeat": result.get("repeat", 1),
                    "exit_code": result.get("agent_exit_code"),
                    "timed_out": result.get("agent_timed_out"),
                    "stderr_preview": html.escape(stderr[:120] or "-"),
                }
            )
    return rows


def format_result_cell(results: list[dict]) -> str:
    if len(results) == 1:
        result = results[0]
        status = "PASS" if result["passed"] else "FAIL"
        codes = ",".join(issue["code"] for issue in result["issues"][:3])
        suffix = f" ({codes})" if codes else ""
        return f"{status} {result['score']:.3f}{suffix}"
    passed = sum(result["passed"] for result in results)
    process_failed = sum(result.get("process_failed", False) for result in results)
    mean_score = sum(result["score"] for result in results) / len(results)
    issue_counts = Counter(
        issue["code"]
        for result in results
        for issue in result["issues"]
    )
    codes = ",".join(code for code, _ in issue_counts.most_common(3))
    suffix = f" ({codes})" if codes else ""
    process_suffix = f", proc={process_failed}" if process_failed else ""
    return f"{passed}/{len(results)} avg={mean_score:.3f}{process_suffix}{suffix}"


def format_bucket(bucket: dict | None) -> str:
    if not bucket:
        return "-"
    total = bucket["total"]
    passed = bucket["passed"]
    rate = passed / total if total else 0
    return f"{passed}/{total} ({rate:.0%})"


def summarize_runs(runs: list[ComparisonRun]) -> dict:
    total = len(runs)
    passed = sum(agent_run_passed(run) for run in runs)
    process_failures = sum(agent_run_process_failed(run) for run in runs)
    valid_runs = [run for run in runs if not agent_run_process_failed(run)]
    task_passed = sum(run.run_result.grade.passed for run in valid_runs)
    task_failures = len(valid_runs) - task_passed
    mean_score = (
        sum(run.run_result.grade.score for run in runs) / total if total else 0.0
    )
    by_level: dict[str, dict[str, int]] = {}
    by_difficulty: dict[str, dict[str, int]] = {}
    outcomes_by_scenario: dict[str, list[bool]] = {}
    for run in runs:
        scenario = run.run_result.scenario
        outcomes_by_scenario.setdefault(scenario.id, []).append(agent_run_passed(run))
        for bucket, key in ((by_level, scenario.level), (by_difficulty, scenario.difficulty)):
            item = bucket.setdefault(key, {"passed": 0, "total": 0})
            item["total"] += 1
            if agent_run_passed(run):
                item["passed"] += 1
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total if total else 0.0,
        "valid_attempts": len(valid_runs),
        "task_passed": task_passed,
        "task_failures": task_failures,
        "task_pass_rate": task_passed / len(valid_runs) if valid_runs else 0.0,
        "mean_score": mean_score,
        "process_failures": process_failures,
        "by_level": by_level,
        "by_difficulty": by_difficulty,
        **compute_reliability_metrics(outcomes_by_scenario),
    }


def agent_run_passed(run: ComparisonRun) -> bool:
    return run.run_result.grade.passed and run.exit_code == 0 and not run.timed_out


def agent_run_process_failed(run: ComparisonRun) -> bool:
    return run.exit_code != 0 or run.timed_out


def agent_run_summary(run: ComparisonRun) -> dict:
    result = run.run_result
    return {
        "id": result.scenario.id,
        "repeat": run.repeat,
        "level": result.scenario.level,
        "difficulty": result.scenario.difficulty,
        "split": result.scenario.split,
        "capability": result.scenario.capability,
        "workflow": result.scenario.workflow,
        "domain": result.scenario.domain,
        "subdomain": result.scenario.subdomain,
        "passed": agent_run_passed(run),
        "process_failed": agent_run_process_failed(run),
        "task_failed": not agent_run_process_failed(run) and not result.grade.passed,
        "grade_passed": result.grade.passed,
        "score": result.grade.score,
        "checks_passed": result.grade.checks_passed,
        "checks_total": result.grade.checks_total,
        "issues": [
            {"code": issue.code, "message": issue.message}
            for issue in result.grade.issues
        ],
        "agent_exit_code": run.exit_code,
        "agent_timed_out": run.timed_out,
        "agent_stdout": run.stdout,
        "agent_stderr": run.stderr,
        "runner": run.runner,
        "run_dir": str(run.run_dir),
        "task_path": str(run.task_path),
        "output_path": str(run.output_path),
    }


def selected_filters(args: argparse.Namespace) -> dict:
    return {
        "difficulty": args.difficulty,
        "level": args.level,
        "capability": args.capability,
        "workflow": args.workflow,
        "domain": args.domain,
        "subdomain": args.subdomain,
        "pack": getattr(args, "pack", "core"),
        "split": getattr(args, "split", None),
        "scenario_dir": getattr(args, "scenario_dir", None),
        "tags": args.tag,
    }


def benchmark_metadata(args: argparse.Namespace) -> dict:
    task_pack = None
    if getattr(args, "scenario_dir", None):
        task_pack = load_task_pack_manifest(Path(args.scenario_dir))
    else:
        task_pack = load_builtin_task_pack_manifest(getattr(args, "pack", "core"))
    return {
        "name": BENCHMARK_NAME,
        "version": task_pack.version if task_pack else BENCHMARK_VERSION,
        "release_id": task_pack.release_id if task_pack else BENCHMARK_RELEASE_ID,
    }


def resolve_output_dir(args: argparse.Namespace) -> Path:
    if args.output_dir:
        return Path(args.output_dir)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    slice_name = args.run_name or args.difficulty
    safe_slice_name = "".join(
        char if char.isalnum() or char in {"-", "_"} else "-"
        for char in slice_name.lower()
    ).strip("-")
    return Path("runs") / "comparison" / f"{timestamp}-{safe_slice_name}"


def render_svg_chart(comparison: dict) -> str:
    models = comparison["models"]
    metric = comparison["metric"]
    metric_key = {
        "pass-rate": "pass_rate",
        "task-pass-rate": "task_pass_rate",
        "mean-score": "mean_score",
        "pass-at-k": "pass_at_k",
        "pass-power-k": "pass_power_k",
    }[metric]
    metric_label = {
        "pass-rate": "Strict Pass Rate",
        "task-pass-rate": "Task Pass Rate",
        "mean-score": "Mean Score",
        "pass-at-k": "pass@k",
        "pass-power-k": "pass^k",
    }[metric]
    values = [model[metric_key] * 100 for model in models]

    width = max(520, 180 * len(models) + 180)
    height = 360
    margin_left = 70
    margin_bottom = 86
    margin_top = 52
    chart_height = height - margin_top - margin_bottom
    baseline_y = margin_top + chart_height
    bar_width = 88
    slot_width = (width - margin_left - 60) / max(len(models), 1)
    colors = ["#2563eb", "#16a34a", "#f97316", "#7c3aed", "#dc2626"]

    title = (
        f"Workspace Bench {metric_label} "
        f"({comparison['filters']['difficulty']} difficulty, "
        f"{comparison['scenario_count']} scenarios)"
    )
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{width / 2}" y="28" text-anchor="middle" '
        'font-family="Arial, sans-serif" font-size="18" font-weight="700" '
        f'fill="#111827">{html.escape(title)}</text>',
        f'<line x1="{margin_left}" y1="{baseline_y}" x2="{width - 40}" y2="{baseline_y}" '
        'stroke="#111827" stroke-width="1"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{baseline_y}" '
        'stroke="#111827" stroke-width="1"/>',
    ]

    for tick in range(0, 101, 25):
        y = baseline_y - (tick / 100) * chart_height
        parts.append(
            f'<line x1="{margin_left - 5}" y1="{y}" x2="{width - 40}" y2="{y}" '
            'stroke="#e5e7eb" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{margin_left - 12}" y="{y + 4}" text-anchor="end" '
            'font-family="Arial, sans-serif" font-size="12" fill="#4b5563">'
            f"{tick}%</text>"
        )

    for index, (model, value) in enumerate(zip(models, values)):
        x_center = margin_left + slot_width * index + slot_width / 2
        x = x_center - bar_width / 2
        bar_height = (value / 100) * chart_height
        y = baseline_y - bar_height
        color = colors[index % len(colors)]
        label = html.escape(model["model"])
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" '
                f'fill="{color}" rx="4"/>',
                f'<text x="{x_center}" y="{y - 8}" text-anchor="middle" '
                'font-family="Arial, sans-serif" font-size="13" font-weight="700" '
                f'fill="#111827">{value:.1f}%</text>',
                f'<text x="{x_center}" y="{baseline_y + 22}" text-anchor="middle" '
                'font-family="Arial, sans-serif" font-size="12" fill="#111827">'
                f"{label}</text>",
                f'<text x="{x_center}" y="{baseline_y + 42}" text-anchor="middle" '
                'font-family="Arial, sans-serif" font-size="11" fill="#4b5563">'
                f"{model['passed']}/{model['total']} passed</text>",
            ]
        )

    parts.append("</svg>\n")
    return "\n".join(parts)


if __name__ == "__main__":
    raise SystemExit(main())
