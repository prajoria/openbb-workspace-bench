"""Run and chart Workspace Bench performance for local model adapters."""

from __future__ import annotations

import argparse
import copy
from collections import Counter
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
import html
import json
import os
import shutil
import subprocess
import ssl
import sys
import threading
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from functools import lru_cache
from typing import Any, Callable, Iterator, Literal, cast

from workspace_bench.agents.model_adapter_helpers import (
    TOOL_REFERENCE,
    envelope_origin_hints,
    strip_code_fence,
)
from workspace_bench.agents.agent_command import (
    AgentCommandRun,
    build_task_envelope,
    run_agent_command,
)
from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.graders import grade_task
from workspace_bench.core.judge import (
    JUDGE_TEMPLATE_SHA,
    JudgeConfig,
    JudgeVerdict,
    build_judge_context,
    judge_episode,
    stark_app_catalog_entry,
)
from workspace_bench.core.models import (
    final_answer_from_trace,
    BENCHMARK_NAME,
    JsonDict,
    RunResult,
    TASK_CATEGORIES,
    Task,
    ToolCall,
    ToolTraceEvent,
)
from workspace_bench.core.provenance import git_provenance
from workspace_bench.reports.metrics import (
    compute_reliability_metrics,
    result_row_metric_slices,
    summarize_result_rows,
    task_reliability_matrix,
)
from workspace_bench.reports.serialization import grade_summary
from workspace_bench.core.runner import (
    BUILTIN_TASK_SUITE_ORDER,
    load_builtin_task_suite_manifest,
    load_builtin_tasks,
    load_task_directory,
    load_task_suite_manifest,
    task_workspace_baseline,
    tasks_workspace_baseline,
)


INTERACTIVE_PROVIDERS = {"openai", "openrouter", "ollama", "concentrate"}
RESULT_SCHEMA_VERSION = "workspace-bench-model-result/v2"
RUN_MANIFEST_SCHEMA_VERSION = "workspace-bench-run-manifest/v1"


def resolve_repo_root(start: Path | None = None) -> Path:
    """Find the checkout root of the benchmark repository."""

    start = start or Path.cwd()
    candidates = [start, *start.parents, *Path(__file__).resolve().parents]
    for candidate in candidates:
        if (
            (candidate / "pyproject.toml").exists()
            and (candidate / "src" / "workspace_bench" / "task_suites").exists()
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
    input_cost_per_million: float | None = None
    cached_input_cost_per_million: float | None = None
    output_cost_per_million: float | None = None
    pricing_source: str | None = None


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
    provider_meta: JsonDict = field(default_factory=dict)
    usage: JsonDict = field(default_factory=dict)
    wall_time_seconds: float = 0.0
    resumed: bool = False
    judge_verdict: JudgeVerdict | None = None


class TransientModelError(RuntimeError):
    """Retryable model provider failure."""

    def __init__(self, message: str, *, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


# Last provider response metadata is thread-local because bounded concurrency
# can execute several episodes for one adapter at once.
_PROVIDER_LOCAL = threading.local()


def _record_provider_meta(**fields: Any) -> None:
    _PROVIDER_LOCAL.last = {key: value for key, value in fields.items() if value is not None}


def _last_provider_meta() -> JsonDict:
    return dict(getattr(_PROVIDER_LOCAL, "last", {}))


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def harness_metadata() -> JsonDict:
    """Best-effort harness identity for result provenance."""

    return git_provenance(Path(__file__).resolve())


def effective_settings(args: argparse.Namespace) -> JsonDict:
    """Snapshot the settings that shape model behavior for this run.

    Called inside the adapter's patched environment so per-adapter env
    overrides (base URLs, temperatures, format escape hatches) are recorded
    as they actually applied.
    """

    return {
        "runner": args.runner,
        "timeout": args.timeout,
        "episode_timeout": getattr(args, "episode_timeout", None),
        "concurrency": getattr(args, "concurrency", 1),
        "repeats": args.repeats,
        "model_retries": args.model_retries,
        "retry_backoff": args.retry_backoff,
        "max_turns_override": args.max_turns,
        "widget_hints": not getattr(args, "no_widget_hints", False),
        "track": getattr(args, "track", "guided"),
        "release_run": getattr(args, "release_run", False),
        "malformed_retries": getattr(args, "malformed_retries", 2),
        "openai_base_url": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "openrouter_base_url": os.environ.get(
            "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
        ),
        "ollama_base_url": os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
        "concentrate_base_url": os.environ.get(
            "CONCENTRATE_BASE_URL", "https://api.concentrate.ai/v1"
        ),
        "openai_temperature": os.environ.get("OPENAI_TEMPERATURE", "0"),
        "ollama_temperature": os.environ.get("OLLAMA_TEMPERATURE", "0"),
        "openai_response_format": os.environ.get("OPENAI_RESPONSE_FORMAT", "json_schema"),
        "initial_state_visible": os.environ.get("WORKSPACE_BENCH_SHOW_INITIAL_STATE") == "1",
        "ollama_format": os.environ.get("OLLAMA_FORMAT", "schema"),
        "judge_model": getattr(args, "judge_model", None)
        or os.environ.get("WORKSPACE_BENCH_JUDGE_MODEL"),
        "judge_base_url": getattr(args, "judge_base_url", None)
        or os.environ.get("WORKSPACE_BENCH_JUDGE_BASE_URL"),
    }


def default_adapters() -> dict[str, ModelAdapter]:
    # The bundled batch example adapters were removed with examples/; the
    # defaults now serve the interactive runner (provider/model), and batch
    # runs require an explicit --models-file.
    return {
        "openai-gpt-4.1": ModelAdapter(
            slug="openai-gpt-4.1",
            label="OpenAI GPT-4.1",
            command="",
            env={},
            provider="openai",
            model="gpt-4.1",
        ),
        "ollama-gpt-oss-20b": ModelAdapter(
            slug="ollama-gpt-oss-20b",
            label="Ollama gpt-oss:20b",
            command="",
            env={"OLLAMA_MODEL": "gpt-oss:20b"},
            provider="ollama",
            model="gpt-oss:20b",
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run selected Workspace Bench tasks against multiple model adapters."
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
        help="Task difficulty slice to run.",
    )
    parser.add_argument("--family", help="Optional task-family filter, e.g. create.")
    parser.add_argument("--category", help="Optional task-category filter, e.g. dashboard.")
    parser.add_argument(
        "--suite",
        dest="suite",
        default="enterprise-apps-usage",
        choices=list(BUILTIN_TASK_SUITE_ORDER),
        help="Bundled task suite. core = operating the workspace.",
    )
    parser.add_argument(
        "--task-dir",
        help="Directory of task JSON files. Defaults to the bundled benchmark.",
    )
    parser.add_argument(
        "--task",
        action="append",
        default=[],
        help="Run only these task id(s). Can be passed multiple times.",
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
        help="Override task max_turns for interactive runs.",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=1,
        help="Run each selected task this many times per model.",
    )
    parser.add_argument(
        "--model-retries",
        type=int,
        default=2,
        help="Retry transient model API failures this many times per turn.",
    )
    parser.add_argument(
        "--malformed-retries",
        type=int,
        default=2,
        help=(
            "Recovery turns granted for malformed model actions before the "
            "episode counts as a process failure. 0 disables the teaching "
            "turn (ablation)."
        ),
    )
    parser.add_argument(
        "--no-widget-hints",
        action="store_true",
        help=(
            "Omit the fixture widget-hint sheet from the first message "
            "(ablation; hints are on by default and identical for every model)."
        ),
    )
    parser.add_argument(
        "--track",
        choices=["guided", "cold"],
        default="guided",
        help=(
            "guided includes benchmark procedure and fixture hints; cold exposes "
            "only the task, tools, and raw observations. Scores from the two "
            "tracks must not be pooled."
        ),
    )
    parser.add_argument(
        "--release-run",
        action="store_true",
        help="Enforce release-quality settings, currently at least three repeats.",
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
        "--judge-model",
        help="OpenAI-compatible model used for required answer judgment.",
    )
    parser.add_argument("--judge-base-url")
    parser.add_argument("--judge-api-key")
    parser.add_argument("--judge-timeout", type=float, default=60.0)
    parser.add_argument(
        "--episode-timeout",
        type=float,
        default=900,
        help="Maximum wall-clock seconds for one task attempt, including all model turns.",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=1,
        help="Maximum task attempts per model to execute concurrently.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help=(
            "Reuse completed task run directories already present in the "
            "output directory (interactive runner only): replay their recorded "
            "tool calls through a fresh simulator to regrade, and only run "
            "tasks with no completed episode on disk."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print selected models and tasks without running agents.",
    )
    args = parser.parse_args(argv)
    if args.track == "cold":
        args.no_widget_hints = True
    if args.repeats < 1:
        print("--repeats must be >= 1", file=sys.stderr)
        return 2
    if args.release_run and args.repeats < 3:
        print("--release-run requires --repeats >= 3", file=sys.stderr)
        return 2
    if args.model_retries < 0:
        print("--model-retries must be >= 0", file=sys.stderr)
        return 2
    if args.malformed_retries < 0:
        print("--malformed-retries must be >= 0", file=sys.stderr)
        return 2
    if args.retry_backoff < 0:
        print("--retry-backoff must be >= 0", file=sys.stderr)
        return 2
    if args.timeout <= 0 or args.episode_timeout <= 0 or args.judge_timeout <= 0:
        print("--timeout, --episode-timeout, and --judge-timeout must be > 0", file=sys.stderr)
        return 2
    if args.concurrency < 1:
        print("--concurrency must be >= 1", file=sys.stderr)
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
            slug=slug,
            label=model_name,
            command="",
            env={"OLLAMA_MODEL": model_name} if provider == "ollama" else {},
            provider=provider,
            model=model_name,
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

    tasks = filter_tasks(
        load_task_source(args),
        difficulty=args.difficulty,
        family=args.family,
        category=args.category,
        task_ids=args.task,
    )
    if not tasks:
        print("No tasks matched the selected filters.", file=sys.stderr)
        return 2

    selected_adapters = [adapters[slug] for slug in selected_model_slugs]
    provider_error = validate_adapters_for_runner(selected_adapters, runner=args.runner)
    if provider_error:
        print(provider_error, file=sys.stderr)
        return 2
    output_dir = resolve_output_dir(args)
    if args.dry_run:
        print_dry_run(selected_adapters, tasks, args)
        print(f"Output directory would be: {output_dir}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    model_summaries = []

    for adapter in selected_adapters:
        total_attempts = len(tasks) * args.repeats
        print(
            f"Running {adapter.label} on {len(tasks)} task(s) "
            f"({total_attempts} attempt(s)) with {args.runner} runner...",
            file=sys.stderr,
        )
        with patched_env(adapter.env):
            manifest = build_run_manifest(adapter, tasks, args)
        manifest_path = output_dir / f"{adapter.slug}.manifest.json"
        try:
            ensure_run_manifest(manifest_path, manifest, resume=args.resume)
        except ValueError as error:
            print(str(error), file=sys.stderr)
            return 2
        runs, run_metadata = run_adapter(
            adapter,
            tasks,
            output_dir,
            timeout=args.timeout,
            episode_timeout=args.episode_timeout,
            runner=args.runner,
            max_turns_override=args.max_turns,
            repeats=args.repeats,
            model_retries=args.model_retries,
            retry_backoff=args.retry_backoff,
            color=should_colorize(args.color, sys.stderr),
            resume=args.resume,
            malformed_retries=args.malformed_retries,
            include_widget_hints=not args.no_widget_hints,
            concurrency=args.concurrency,
            manifest=manifest,
            args=args,
        )
        judge_config = configured_judge(args)
        if judge_config is not None:
            runs = [judge_comparison_run(run, judge_config) for run in runs]
        result_payload = model_result_payload(adapter, tasks, runs, args, run_metadata)
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
        "harness": harness_metadata(),
        "filters": selected_filters(args),
        "runner": args.runner,
        "max_turns_override": args.max_turns,
        "repeats": args.repeats,
        "model_retries": args.model_retries,
        "retry_backoff": args.retry_backoff,
        "episode_timeout": args.episode_timeout,
        "concurrency": args.concurrency,
        "malformed_retries": args.malformed_retries,
        "widget_hints": not args.no_widget_hints,
        "metric": args.metric,
        "models_file": args.models_file,
        "task_count": len(tasks),
        "attempt_count": len(tasks) * args.repeats,
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
    pricing = payload.get("pricing", {})
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
    if not isinstance(pricing, dict):
        raise ValueError(f"models[{index}].pricing must be an object when set")
    input_price = pricing.get("input_per_million")
    cached_input_price = pricing.get("cached_input_per_million")
    output_price = pricing.get("output_per_million")
    pricing_source = pricing.get("source")
    for field_name, value in (
        ("input_per_million", input_price),
        ("cached_input_per_million", cached_input_price),
        ("output_per_million", output_price),
    ):
        if value is not None and (not isinstance(value, (int, float)) or value < 0):
            raise ValueError(f"models[{index}].pricing.{field_name} must be non-negative")
    if pricing_source is not None and not isinstance(pricing_source, str):
        raise ValueError(f"models[{index}].pricing.source must be a string")
    return ModelAdapter(
        slug=slug,
        label=label,
        command=command,
        env={str(key): str(value) for key, value in env.items()},
        provider=provider,
        model=model,
        input_cost_per_million=float(input_price) if input_price is not None else None,
        cached_input_cost_per_million=(
            float(cached_input_price) if cached_input_price is not None else None
        ),
        output_cost_per_million=float(output_price) if output_price is not None else None,
        pricing_source=pricing_source,
    )


def validate_adapters_for_runner(
    adapters: list[ModelAdapter],
    *,
    runner: str,
) -> str | None:
    """Return a user-facing validation error for unsupported runner/provider combos."""

    if runner == "interactive":
        unsupported = [
            adapter for adapter in adapters if adapter.provider not in INTERACTIVE_PROVIDERS
        ]
        if unsupported:
            labels = ", ".join(f"{adapter.slug} ({adapter.provider})" for adapter in unsupported)
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
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        return completed.returncode == 0 and png_path.exists()

    return False


def filter_tasks(
    tasks: list[Task],
    *,
    difficulty: str,
    family: str | None,
    category: str | None,
    task_ids: list[str] | None = None,
) -> list[Task]:
    if task_ids:
        wanted = set(task_ids)
        tasks = [task for task in tasks if task.id in wanted or task.qualified_id in wanted]
    if difficulty != "all":
        tasks = [task for task in tasks if task.difficulty == difficulty]
    if family:
        tasks = [task for task in tasks if task.family == family]
    if category:
        tasks = [task for task in tasks if task.category == category]
    return tasks


def load_task_source(args: argparse.Namespace) -> list[Task]:
    task_dir = getattr(args, "task_dir", None)
    if task_dir:
        return load_task_directory(Path(task_dir))
    suite = getattr(args, "suite", "enterprise-apps-usage")
    # `--task <id>` should just work without naming the suite: when ids are
    # given and the suite was left at its default, search every bundled
    # suite for them.
    if getattr(args, "task", None) and suite == "enterprise-apps-usage":
        tasks = []
        seen: set[str] = set()
        for name in BUILTIN_TASK_SUITE_ORDER:
            for task in load_builtin_tasks(name):
                if task.qualified_id not in seen:
                    seen.add(task.qualified_id)
                    tasks.append(task)
        return tasks
    return load_builtin_tasks(suite)


def print_dry_run(
    adapters: list[ModelAdapter], tasks: list[Task], args: argparse.Namespace
) -> None:
    print(f"Runner: {args.runner}")
    print(f"Repeats: {args.repeats}")
    print(f"Model retries: {args.model_retries}")
    print("Models:")
    for adapter in adapters:
        print(f"  - {adapter.slug}: {adapter.label}")
    print(f"Tasks ({len(tasks)}) for filters {selected_filters(args)}:")
    for task in tasks:
        print(f"  - {task.qualified_id}\t{task.category}\t{task.difficulty}")


def build_run_manifest(
    adapter: ModelAdapter,
    tasks: list[Task],
    args: argparse.Namespace,
) -> JsonDict:
    """Build a stable identity for cells that may be resumed from disk."""

    benchmark = benchmark_metadata(args)
    temperature_key = (
        "OLLAMA_TEMPERATURE" if adapter.provider == "ollama" else "OPENAI_TEMPERATURE"
    )
    return {
        "schema_version": RUN_MANIFEST_SCHEMA_VERSION,
        "model": adapter.model,
        "model_slug": adapter.slug,
        "provider": adapter.provider,
        "temperature": float(os.environ.get(temperature_key, "0")),
        "harness_git_commit": harness_metadata().get("git_commit"),
        "harness_git_dirty": harness_metadata().get("git_dirty"),
        "suite_id": benchmark.get("suite_id"),
        "suite_content_sha256": benchmark.get("content_sha256"),
        "workspace_baseline": benchmark.get("workspace_baseline"),
        "runner": args.runner,
        "track": getattr(args, "track", "guided"),
        "repeats": args.repeats,
        "tasks": [task.qualified_id for task in tasks],
    }


def ensure_run_manifest(path: Path, manifest: JsonDict, *, resume: bool) -> None:
    """Write a manifest, rejecting incompatible resume attempts."""

    if path.exists() and resume:
        existing = json.loads(path.read_text(encoding="utf-8"))
        comparable_existing = dict(existing)
        comparable_existing.pop("pricing", None)
        comparable_manifest = dict(manifest)
        comparable_manifest.pop("pricing", None)
        if comparable_existing != comparable_manifest:
            raise ValueError(
                f"Cannot resume {path}: run manifest differs from the requested run."
            )
        write_json_atomic(path, manifest)
        return
    write_json_atomic(path, manifest)


def write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def run_adapter(
    adapter: ModelAdapter,
    tasks: list[Task],
    output_dir: Path,
    *,
    timeout: float,
    episode_timeout: float = 900,
    runner: str,
    max_turns_override: int | None,
    repeats: int,
    model_retries: int,
    retry_backoff: float,
    color: bool,
    resume: bool = False,
    malformed_retries: int = 2,
    include_widget_hints: bool = True,
    concurrency: int = 1,
    manifest: JsonDict | None = None,
    args: argparse.Namespace | None = None,
) -> tuple[list[ComparisonRun], JsonDict]:
    indexed_runs: dict[int, ComparisonRun] = {}
    total_attempts = len(tasks) * repeats
    resumed_count = 0
    started_at = _utc_now()
    settings: JsonDict = {}
    checkpoint_path = output_dir / f"{adapter.slug}.checkpoint.json"
    cells = [
        (index, task, repeat)
        for index, (repeat, task) in enumerate(
            (
                (repeat, task)
                for repeat in range(1, repeats + 1)
                for task in tasks
            ),
            start=1,
        )
    ]

    def execute_cell(task: Task, repeat: int) -> ComparisonRun:
        cell_started = time.monotonic()
        run_dir = task_run_dir(
            output_dir / adapter.slug,
            task.qualified_id.replace("/", "__"),
            repeat=repeat,
            repeats=repeats,
        )
        if resume and runner == "interactive":
            replayed = replay_completed_run(
                adapter, task, run_dir, repeat=repeat, max_turns_override=max_turns_override
            )
            if replayed is not None:
                return replayed
        if runner == "batch":
            run = batch_comparison_run(
                run_agent_command(
                    task=task,
                    command=adapter.command,
                    timeout_seconds=episode_timeout,
                    run_dir=run_dir,
                ),
                repeat=repeat,
            )
        else:
            run = run_interactive_agent(
                adapter=adapter,
                task=task,
                run_dir=run_dir,
                timeout=timeout,
                episode_timeout=episode_timeout,
                max_turns_override=max_turns_override,
                model_retries=model_retries,
                retry_backoff=retry_backoff,
                repeat=repeat,
                malformed_retries=malformed_retries,
                include_widget_hints=include_widget_hints,
            )
        if run.wall_time_seconds == 0.0:
            run = replace(run, wall_time_seconds=time.monotonic() - cell_started)
        return run

    def record(index: int, task: Task, repeat: int, run: ComparisonRun) -> None:
        nonlocal resumed_count
        indexed_runs[index] = run
        if run.resumed:
            resumed_count += 1
        write_json_atomic(
            checkpoint_path,
            {
                "schema_version": RESULT_SCHEMA_VERSION,
                "manifest": manifest or {},
                "completed_cells": [
                    agent_run_summary(indexed_runs[cell_index])
                    for cell_index in sorted(indexed_runs)
                ],
                "completed_count": len(indexed_runs),
                "requested_count": total_attempts,
            },
        )
        repeat_label = f" repeat {repeat}/{repeats}" if repeats > 1 else ""
        resume_label = " (resumed from disk)" if run.resumed else ""
        print(
            f"  [{index}/{total_attempts}] {task.id}{repeat_label} "
            f"{run_status(run, color=color)} "
            f"score={run.run_result.grade.score:.2f} "
            f"checks={run.run_result.grade.checks_passed}/"
            f"{run.run_result.grade.checks_total} "
            f"exit={run.exit_code} timeout={run.timed_out}{resume_label}",
            file=sys.stderr,
            flush=True,
        )

    with patched_env(adapter.env):
        if args is not None:
            settings = effective_settings(args)
        if concurrency == 1:
            for index, task, repeat in cells:
                record(index, task, repeat, execute_cell(task, repeat))
        else:
            with ThreadPoolExecutor(max_workers=concurrency) as executor:
                futures: dict[Future[ComparisonRun], tuple[int, Task, int]] = {
                    executor.submit(execute_cell, task, repeat): (index, task, repeat)
                    for index, task, repeat in cells
                }
                for future in as_completed(futures):
                    index, task, repeat = futures[future]
                    record(index, task, repeat, future.result())
    runs = [indexed_runs[index] for index in sorted(indexed_runs)]
    if resumed_count:
        print(
            f"  resume summary: resumed={resumed_count} "
            f"new={total_attempts - resumed_count} total={total_attempts}",
            file=sys.stderr,
            flush=True,
        )
    run_metadata: JsonDict = {
        "started_at": started_at,
        "finished_at": _utc_now(),
        "harness": harness_metadata(),
        "workspace_baseline": tasks_workspace_baseline(tasks),
        "settings": settings,
        "requested_cells": total_attempts,
        "completed_cells": len(runs),
        "resumed_cells": resumed_count,
        "new_cells": total_attempts - resumed_count,
        "provider_observed": {
            "models": sorted(
                {model for run in runs for model in run.provider_meta.get("models", [])}
            ),
            "system_fingerprints": sorted(
                {
                    fingerprint
                    for run in runs
                    for fingerprint in run.provider_meta.get("system_fingerprints", [])
                }
            ),
        },
    }
    return runs, run_metadata


def replay_completed_run(
    adapter: ModelAdapter,
    task: Task,
    run_dir: Path,
    *,
    repeat: int = 1,
    max_turns_override: int | None = None,
) -> ComparisonRun | None:
    """Rebuild a ComparisonRun from a completed episode already on disk.

    conversation.json is written only after the turn loop finishes, so its
    presence marks a completed episode; a run killed mid-task lacks it and
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
    episode = WorkspaceEpisode(
        task=task,
        max_turns_override=max_turns_override or int(task.limits.get("max_turns", 12)),
    )
    if output_path.exists():
        for line in output_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            payload = json.loads(line)
            episode.step(ToolCall(payload["tool"], payload["args"]))
    return ComparisonRun(
        run_result=RunResult(
            task=task,
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
        provider_meta=dict(meta.get("provider", {})),
        usage=reprice_usage(adapter, dict(meta.get("usage", {}))),
        wall_time_seconds=float(meta.get("wall_time_seconds", 0.0)),
        resumed=True,
    )


def task_run_dir(base_dir: Path, task_id: str, *, repeat: int, repeats: int) -> Path:
    if repeats == 1:
        return base_dir / task_id
    return base_dir / task_id / f"repeat_{repeat:02d}"


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
    task: Task,
    run_dir: Path,
    timeout: float,
    episode_timeout: float = 900,
    max_turns_override: int | None,
    model_retries: int,
    retry_backoff: float,
    repeat: int = 1,
    malformed_retries: int = 2,
    include_widget_hints: bool = True,
) -> ComparisonRun:
    episode_started = time.monotonic()
    run_dir.mkdir(parents=True, exist_ok=True)
    task_path = run_dir / "task.json"
    output_path = run_dir / "tool_calls.jsonl"
    conversation_path = run_dir / "conversation.json"
    responses_path = run_dir / "model_responses.jsonl"
    task_payload = build_task_envelope(task)
    origin_hints = envelope_origin_hints(
        {**task_payload.get("benchmark", {}), **task_payload["task"]}
    )
    task_path.write_text(
        json.dumps(task_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if output_path.exists():
        output_path.unlink()
    if responses_path.exists():
        responses_path.unlink()

    max_turns = max_turns_override or int(task.limits.get("max_turns", 12))
    episode = WorkspaceEpisode(task=task, max_turns_override=max_turns)
    messages = build_interactive_messages(task_payload, include_widget_hints=include_widget_hints)
    stdout_lines: list[str] = []
    stderr = ""
    exit_code: int | None = 0
    timed_out = False
    observed_models: set[str] = set()
    observed_fingerprints: set[str] = set()
    usage_totals: JsonDict = {
        "api_calls": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "cached_tokens": 0,
        "provider_cost_usd": 0.0,
        "provider_cost_reported": False,
    }

    malformed_recoveries = 0
    for turn in range(1, max_turns + 1):
        remaining = episode_timeout - (time.monotonic() - episode_started)
        if remaining <= 0:
            timed_out = True
            exit_code = None
            stderr = f"episode exceeded {episode_timeout:.1f}s wall-clock timeout"
            break
        try:
            content = call_model_with_retries(
                adapter,
                messages,
                timeout=min(timeout, remaining),
                retries=model_retries,
                backoff_seconds=retry_backoff,
                retry_log=stdout_lines,
                turn=turn,
                deadline=episode_started + episode_timeout,
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
        call_meta = _last_provider_meta()
        if call_meta.get("model"):
            observed_models.add(str(call_meta["model"]))
        if call_meta.get("system_fingerprint"):
            observed_fingerprints.add(str(call_meta["system_fingerprint"]))
        accumulate_usage(usage_totals, call_meta.get("usage"))
        try:
            action = parse_interactive_action(content)
        except Exception as error:  # noqa: BLE001 - malformed model action.
            # Teaching turn, mirroring invalid-tool-call rejections: a malformed
            # action costs a turn (and patience), not the episode. Two strikes
            # by default; --malformed-retries 0 disables the recovery.
            malformed_recoveries += 1
            if malformed_recoveries > malformed_retries:
                exit_code = 1
                stderr = str(error)
                break
            stdout_lines.append(f"turn {turn}: malformed action recovered ({error})")
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
            # Models often send their final action and done together
            # ({"done": true, "tool": ..., "args": ...}); honoring done while
            # discarding the call would silently drop the final mutation, so
            # execute it first.
            final_tool = action.get("tool")
            final_args = action.get("args", {})
            if isinstance(final_tool, str) and final_tool and isinstance(final_args, dict):
                final_call = ToolCall(
                    normalize_tool_name(final_tool),
                    normalize_interactive_args(final_args, origin_hints),
                )
                episode.step(final_call)
                append_jsonl(
                    output_path, {"tool": final_call.name, "args": final_call.args}
                )
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
        if episode.answered:
            break
        done_rule = None
        if task.success.required_answer_judgment or task.success.required_values_in_answer:
            done_rule = (
                "Choose the next single tool call. The task completes when you "
                "call final_answer with your full answer text, quoting exact "
                "figures from the data you read."
            )
        messages.append(
            {
                "role": "user",
                "content": tool_result_prompt(turn, call, result, done_rule=done_rule),
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
    provider_meta: JsonDict = {
        "models": sorted(observed_models),
        "system_fingerprints": sorted(observed_fingerprints),
    }
    usage = finalize_usage(adapter, usage_totals)
    wall_time_seconds = time.monotonic() - episode_started
    meta_path = run_dir / "run_meta.json"
    meta_path.write_text(
        json.dumps(
            {
                "exit_code": exit_code,
                "timed_out": timed_out,
                "stdout": "\n".join(stdout_lines),
                "stderr": stderr,
                "provider": provider_meta,
                "usage": usage,
                "wall_time_seconds": wall_time_seconds,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return ComparisonRun(
        run_result=RunResult(
            task=task,
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
        provider_meta=provider_meta,
        usage=usage,
        wall_time_seconds=wall_time_seconds,
    )


def build_interactive_messages(
    task: JsonDict, *, include_widget_hints: bool = True
) -> list[JsonDict]:
    benchmark = task.get("benchmark", {})
    task = task["task"]
    allowed_tools = task["allowed_tools"]
    origin_hints = (
        envelope_origin_hints({**benchmark, **task}) if include_widget_hints else {}
    )
    tool_reference = {
        name: TOOL_REFERENCE[name] for name in allowed_tools if name in TOOL_REFERENCE
    }
    public_task = {
        "id": task["id"],
        "qualified_id": task["qualified_id"],
        "family": task.get("family", "general"),
        "specification_level": task.get("specification_level"),
        "difficulty": task["difficulty"],
        "prompt": task["prompt"],
        "business_terms": task.get("business_terms", []),
        "fixtures": task["fixtures"],
        "origin_hints": origin_hints,
        # Closed-world by default: a real MCP agent discovers workspace state
        # through get_workspace_snapshot rather than receiving the dashboard
        # JSON for free, so discovery is part of every exam. The legacy flag
        # restores the old open-world behavior for historical comparisons.
        "initial_state": (
            task["initial_state"]
            if os.environ.get("WORKSPACE_BENCH_SHOW_INITIAL_STATE") == "1"
            else {"hidden": "call get_workspace_snapshot to inspect the workspace"}
        ),
        "allowed_tools": allowed_tools,
    }
    base_instructions = [
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
        "Use IDs returned by tool results exactly. Do not use placeholders like {{dashboard_id}}.",
        'When the final Workspace state satisfies the task, return {"done": true}.',
    ]
    guided_instructions = [
        "When a tool asks for origin, use the display origin from origin_hints, not the fixture slug.",
        "If dashboard_id is optional and you do not know the UUID, omit it instead of using a dashboard name.",
        "Never invent widget_id values. Use exact widget_id values from list_available_widgets or prior tool results.",
        "Before create_widget, you MUST call list_available_widgets for the same origin when that tool is allowed.",
        "Before create_widget, you MUST call get_widget_schema for the same origin and widget_id when that tool is allowed.",
        "Calling create_widget before list_available_widgets and get_widget_schema will fail the benchmark.",
        "For tabbed dashboards, navigate to the target tab before creating widgets or set layout tab_id correctly.",
        "For app templates, call manage_backends list, then use the returned backend id in manage_apps.",
        "For generated notes/charts, include concrete task facts from tool data and put the widget on the required tab when applicable.",
        "Generated widget text is checked literally. Copy exact numbers and identifiers from observations: write 0.86, not 86%; write price_performance, not only Price Performance.",
        "Use update_widget_layout for layout changes, not update_widget.",
    ]
    system = "\n".join(base_instructions + (guided_instructions if include_widget_hints else []))
    user = "\n".join(
        [
            "Available tool reference:",
            json.dumps(tool_reference, indent=2, sort_keys=True),
            "",
            "Task:",
            json.dumps(public_task, indent=2, sort_keys=True),
            "",
            *(
                [
                    "Completion rule for this task: you must submit your answer "
                    "through the final_answer tool. After reading the relevant "
                    "widget data, call final_answer with your full answer text, "
                    "quoting exact figures copied from the data. Calling "
                    "final_answer completes the episode.",
                    "",
                ]
                # The allow-listed answer channel IS the announcement that a
                # reply is expected — true for judge-graded and deterministic
                # answer tasks alike.
                if "final_answer" in allowed_tools
                else []
            ),
            "Choose the first tool call.",
        ]
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def tool_result_prompt(
    turn: int, call: ToolCall, result: JsonDict, *, done_rule: str | None = None
) -> str:
    # The closing line sits in the recency position models weight most, so
    # judged tasks restate their completion criterion here instead of only in
    # the opening message.
    closing = done_rule or (
        'Choose the next single tool call, or return {"done": true} if the task is complete.'
    )
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
            closing,
        ]
    )


def call_model(adapter: ModelAdapter, messages: list[JsonDict], timeout: float) -> str:
    if adapter.provider == "openai":
        return call_openai_chat(adapter.model, messages, timeout)
    if adapter.provider == "openrouter":
        return call_openai_chat(
            adapter.model,
            messages,
            timeout,
            api_key_env="OPENROUTER_API_KEY",
            default_base_url="https://openrouter.ai/api/v1",
            base_url_env="OPENROUTER_BASE_URL",
        )
    if adapter.provider == "ollama":
        return call_ollama_chat(adapter.model, messages, timeout)
    if adapter.provider == "concentrate":
        return call_concentrate_responses(adapter.model, messages, timeout)
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
    deadline: float | None = None,
) -> str:
    attempt = 0
    while True:
        try:
            request_timeout = timeout
            if deadline is not None:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("episode wall-clock timeout exhausted")
                request_timeout = min(request_timeout, remaining)
            return call_model(adapter, messages, timeout=request_timeout)
        except TransientModelError as error:
            if attempt >= retries:
                raise
            attempt += 1
            wait_seconds = backoff_seconds * (2 ** (attempt - 1))
            retry_log.append(
                f"turn {turn} retry {attempt}/{retries} after transient model error: {error}"
            )
            if deadline is not None and time.monotonic() + wait_seconds >= deadline:
                raise TimeoutError("episode wall-clock timeout exhausted") from error
            if wait_seconds:
                time.sleep(wait_seconds)
        except TimeoutError as error:
            if attempt >= retries:
                raise
            attempt += 1
            wait_seconds = backoff_seconds * (2 ** (attempt - 1))
            retry_log.append(f"turn {turn} retry {attempt}/{retries} after model timeout: {error}")
            if deadline is not None and time.monotonic() + wait_seconds >= deadline:
                raise TimeoutError("episode wall-clock timeout exhausted") from error
            if wait_seconds:
                time.sleep(wait_seconds)


def call_openai_chat(
    model: str,
    messages: list[JsonDict],
    timeout: float,
    *,
    api_key_env: str = "OPENAI_API_KEY",
    default_base_url: str = "https://api.openai.com/v1",
    base_url_env: str = "OPENAI_BASE_URL",
) -> str:
    load_dotenv()
    api_key = os.environ.get(api_key_env)
    if not api_key:
        raise RuntimeError(f"{api_key_env} is not set in the environment or .env")
    base_url = os.environ.get(base_url_env, default_base_url).rstrip("/")
    payload = {
        "model": model,
        "temperature": float(os.environ.get("OPENAI_TEMPERATURE", "0")),
        # One next-action JSON per turn: cap the completion so providers'
        # affordability prechecks (e.g. OpenRouter multiplies max_tokens by
        # price) reflect real usage. Reasoning models keep ample headroom.
        "max_tokens": int(os.environ.get("OPENAI_MAX_TOKENS", "4096")),
        "messages": messages,
    }
    # OpenRouter can route one model through several upstream providers with
    # different serving behavior (e.g. Anthropic models on the Bedrock route
    # return thinking-only turns whose message content is empty). Pinning the
    # provider order keeps every episode on one serving path.
    provider_order = os.environ.get("OPENROUTER_PROVIDER_ORDER")
    if provider_order and "openrouter" in base_url:
        payload["provider"] = {
            "order": [entry.strip() for entry in provider_order.split(",") if entry.strip()],
            "allow_fallbacks": False,
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
    # Reasoning-family OpenAI models reject max_tokens (use
    # max_completion_tokens) and non-default temperature - and the API
    # reports one offending param per response, so adapt-and-retry loops
    # until the payload is accepted or the error is something else.
    for _ in range(3):
        try:
            body = post_json(
                f"{base_url}/chat/completions",
                payload,
                timeout,
                headers={"Authorization": f"Bearer {api_key}"},
            )
            break
        except Exception as error:
            message = str(error)
            if "max_completion_tokens" in message and "max_tokens" in payload:
                payload["max_completion_tokens"] = payload.pop("max_tokens")
                continue
            if (
                "temperature" in message
                and "unsupported_value" in message
                and "temperature" in payload
            ):
                payload.pop("temperature")
                continue
            raise
    _record_provider_meta(
        model=body.get("model"),
        system_fingerprint=body.get("system_fingerprint"),
        usage=openai_usage(body),
    )
    try:
        content = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError(f"OpenAI returned no message content: {body!r}") from error
    if not isinstance(content, str) or not content.strip():
        raise ValueError(f"OpenAI returned empty message content: {body!r}")
    return content


def call_concentrate_responses(model: str, messages: list[JsonDict], timeout: float) -> str:
    """Call Concentrate's Responses-shaped API (POST {base}/responses/).

    Concentrate normalizes many upstream providers behind one OpenAI
    Responses-shaped endpoint. Chat system messages travel in
    ``instructions``, the remaining turns in ``input``, and the reply text
    comes back in the ``output`` array's message items. Temperature, token
    cap, and the structured-output escape hatch reuse the OPENAI_* env
    knobs so a model swap never changes run semantics.
    """

    load_dotenv()
    api_key = os.environ.get("CONCENTRATE_API_KEY")
    if not api_key:
        raise RuntimeError("CONCENTRATE_API_KEY is not set in the environment or .env")
    base_url = os.environ.get("CONCENTRATE_BASE_URL", "https://api.concentrate.ai/v1").rstrip("/")
    instructions = "\n\n".join(
        message["content"]
        for message in messages
        if message.get("role") == "system" and isinstance(message.get("content"), str)
    )
    payload: JsonDict = {
        "model": model,
        "temperature": float(os.environ.get("OPENAI_TEMPERATURE", "0")),
        "max_output_tokens": int(os.environ.get("OPENAI_MAX_TOKENS", "4096")),
        "input": [
            {"role": message.get("role", "user"), "content": message.get("content", "")}
            for message in messages
            if message.get("role") != "system"
        ],
    }
    if instructions:
        payload["instructions"] = instructions
    reasoning_effort = os.environ.get("CONCENTRATE_REASONING_EFFORT")
    if reasoning_effort:
        payload["reasoning"] = {"effort": reasoning_effort}
    if os.environ.get("OPENAI_RESPONSE_FORMAT", "json_schema") != "none":
        payload["text"] = {
            "format": {
                "type": "json_schema",
                "name": "workspace_next_action",
                "schema": interactive_action_schema(),
                "strict": False,
            }
        }
    # The docs publish the path with a trailing slash; keep it verbatim so a
    # framework-level redirect never downgrades the POST.
    body = post_json(
        f"{base_url}/responses/",
        payload,
        timeout,
        # Concentrate sits behind Cloudflare, which rejects urllib's default
        # user-agent (error 1010); a real product UA passes.
        headers={
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "workspace-bench/1.0",
        },
    )
    status = body.get("status")
    if status in {"failed", "cancelled", "incomplete"}:
        raise ValueError(f"Concentrate returned status {status!r}: {body.get('error') or body!r}")
    _record_provider_meta(model=body.get("model"), usage=openai_usage(body))
    # Concentrate echoes the request's assistant input items back into the
    # output array ahead of the new generation; only the LAST message item is
    # the model's reply. Concatenating them would resurface the previous
    # turn's action JSON and trap the episode in a loop.
    message_items = [
        item
        for item in body.get("output") or []
        if isinstance(item, dict) and item.get("type") == "message"
    ]
    parts: list[str] = []
    if message_items:
        for chunk in message_items[-1].get("content") or []:
            if isinstance(chunk, dict) and chunk.get("type") in {"output_text", "text"}:
                text_value = chunk.get("text")
                if isinstance(text_value, str):
                    parts.append(text_value)
    content = "".join(parts)
    if not content.strip():
        raise ValueError(f"Concentrate returned no output text: {body!r}")
    return content


def call_ollama_chat(model: str, messages: list[JsonDict], timeout: float) -> str:
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    options: JsonDict = {"temperature": float(os.environ.get("OLLAMA_TEMPERATURE", "0"))}
    if os.environ.get("OLLAMA_NUM_CTX"):
        options["num_ctx"] = int(os.environ["OLLAMA_NUM_CTX"])
    payload = {
        "model": os.environ.get("OLLAMA_MODEL", model),
        "stream": False,
        "options": options,
        "messages": messages,
    }
    # Same escape hatch as OPENAI_RESPONSE_FORMAT: some generations 500 inside
    # ollama's schema-grammar sampler; format=none falls back to unconstrained
    # JSON (the teaching-turn recovery backstops malformed output).
    if os.environ.get("OLLAMA_FORMAT", "schema") != "none":
        payload["format"] = interactive_action_schema()
    # Reasoning models occasionally spend the whole generation in the thinking
    # channel and return empty content; at temperature 0 that repeats forever.
    # One same-request retry with sampling jitter breaks the deterministic loop.
    for attempt in range(2):
        if attempt:
            payload["options"] = {**options, "temperature": max(0.3, options["temperature"])}
        body = post_json(f"{base_url}/api/chat", payload, timeout)
        _record_provider_meta(
            model=body.get("model"),
            usage={
                "input_tokens": int(body.get("prompt_eval_count") or 0),
                "output_tokens": int(body.get("eval_count") or 0),
                "total_tokens": int(body.get("prompt_eval_count") or 0)
                + int(body.get("eval_count") or 0),
            },
        )
        message = body.get("message") or {}
        content = message.get("content")
        if isinstance(content, str) and content.strip():
            return content
        tool_calls = message.get("tool_calls")
        if isinstance(tool_calls, list) and tool_calls:
            return json.dumps(native_tool_call_to_action(tool_calls[0]), sort_keys=True)
    raise ValueError(f"Ollama returned no message content: {body!r}")


def openai_usage(body: JsonDict) -> JsonDict:
    """Normalize OpenAI-compatible usage, including OpenRouter cost fields."""

    raw = body.get("usage")
    usage = raw if isinstance(raw, dict) else {}
    input_tokens = int(usage.get("prompt_tokens") or usage.get("input_tokens") or 0)
    output_tokens = int(usage.get("completion_tokens") or usage.get("output_tokens") or 0)
    details = usage.get("prompt_tokens_details") or usage.get("input_tokens_details") or {}
    cached_tokens = int(details.get("cached_tokens") or 0) if isinstance(details, dict) else 0
    raw_cost = usage.get("cost", body.get("cost"))
    try:
        cost = float(raw_cost) if raw_cost is not None else None
    except (TypeError, ValueError):
        cost = None
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": int(usage.get("total_tokens") or input_tokens + output_tokens),
        "cached_tokens": cached_tokens,
        "provider_cost_usd": cost,
    }


def accumulate_usage(total: JsonDict, usage: Any) -> None:
    if not isinstance(usage, dict):
        return
    total["api_calls"] = int(total.get("api_calls", 0)) + 1
    for key in ("input_tokens", "output_tokens", "total_tokens", "cached_tokens"):
        total[key] = int(total.get(key, 0)) + int(usage.get(key) or 0)
    cost = usage.get("provider_cost_usd")
    if isinstance(cost, (int, float)):
        total["provider_cost_usd"] = float(total.get("provider_cost_usd", 0.0)) + float(cost)
        total["provider_cost_reported"] = True


def finalize_usage(adapter: ModelAdapter, usage: JsonDict) -> JsonDict:
    """Attach provider-reported or configured token-price cost to an episode."""

    result = dict(usage)
    if result.pop("provider_cost_reported", False):
        result["cost_usd"] = round(float(result.get("provider_cost_usd", 0.0)), 10)
        result["cost_source"] = "provider"
    elif (
        adapter.input_cost_per_million is not None
        and adapter.output_cost_per_million is not None
    ):
        cached_tokens = int(result.get("cached_tokens", 0))
        input_tokens = int(result.get("input_tokens", 0))
        uncached_tokens = max(0, input_tokens - cached_tokens)
        cached_price = (
            adapter.cached_input_cost_per_million
            if adapter.cached_input_cost_per_million is not None
            else adapter.input_cost_per_million
        )
        result["cost_usd"] = round(
            uncached_tokens * adapter.input_cost_per_million / 1_000_000
            + cached_tokens * cached_price / 1_000_000
            + int(result.get("output_tokens", 0))
            * adapter.output_cost_per_million
            / 1_000_000,
            10,
        )
        result["cost_source"] = adapter.pricing_source or "configured_token_prices"
    else:
        result["cost_usd"] = None
        result["cost_source"] = None
    result.pop("provider_cost_usd", None)
    return result


def reprice_usage(adapter: ModelAdapter, usage: JsonDict) -> JsonDict:
    """Reapply configured pricing when replaying a completed episode."""

    if usage.get("cost_source") == "provider":
        return usage
    raw = {
        key: usage.get(key, 0)
        for key in (
            "api_calls",
            "input_tokens",
            "output_tokens",
            "total_tokens",
            "cached_tokens",
        )
    }
    raw["provider_cost_reported"] = False
    return finalize_usage(adapter, raw)


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
        raise TransientModelError(f"could not reach model API at {url}: {error.reason}") from error
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
        # Preserve a final action sent together with done so the loop can
        # execute it before terminating.
        action: JsonDict = {"done": True}
        if isinstance(payload.get("tool"), str) and payload["tool"]:
            final_args = payload.get("args", payload.get("arguments", {}))
            if isinstance(final_args, str):
                final_args = json.loads(final_args)
            action["tool"] = payload["tool"]
            action["args"] = final_args if isinstance(final_args, dict) else {}
        return action
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
    tasks: list[Task],
    runs: list[ComparisonRun],
    args: argparse.Namespace,
    run_metadata: JsonDict | None = None,
) -> dict:
    for run in runs:
        persist_judge_input(run)
    result_rows = [agent_run_summary(run) for run in runs]
    return {
        "schema_version": RESULT_SCHEMA_VERSION,
        "benchmark": benchmark_metadata(args),
        "model": {
            "slug": adapter.slug,
            "label": adapter.label,
            "provider": adapter.provider,
            "id": adapter.model,
            "pricing": {
                "input_per_million": adapter.input_cost_per_million,
                "cached_input_per_million": adapter.cached_input_cost_per_million,
                "output_per_million": adapter.output_cost_per_million,
                "source": adapter.pricing_source,
            },
        },
        "filters": selected_filters(args),
        "runner": args.runner,
        "repeats": args.repeats,
        "model_retries": args.model_retries,
        "run_metadata": run_metadata or {},
        "summary": summarize_runs(runs, result_rows=result_rows),
        "results": result_rows,
        "task_matrix": task_reliability_matrix(result_rows),
        "tasks": [task.qualified_id for task in tasks],
    }


def configured_judge(args: argparse.Namespace) -> JudgeConfig | None:
    """Resolve a judge only when its model was explicitly configured."""

    model = getattr(args, "judge_model", None)
    if not model and not os.environ.get("WORKSPACE_BENCH_JUDGE_MODEL"):
        return None
    return JudgeConfig.resolve(
        model=model,
        base_url=getattr(args, "judge_base_url", None),
        api_key=getattr(args, "judge_api_key", None),
        timeout=getattr(args, "judge_timeout", None),
    )


def judge_comparison_run(
    run: ComparisonRun,
    config: JudgeConfig,
    *,
    judge_callable: Callable[[JudgeConfig, str], JudgeVerdict] = judge_episode,
) -> ComparisonRun:
    """Judge a completed required episode and replace its cached grade."""

    result = run.run_result
    if not result.task.success.required_answer_judgment:
        return run
    cached = load_cached_judge_verdict(run.run_dir) if run.resumed else None
    if cached is not None:
        grade = grade_task(
            result.task,
            result.final_snapshot,
            result.trace,
            judge_verdict=cached.passed if cached.passed is not None else False,
        )
        return replace(
            run,
            run_result=replace(result, grade=grade),
            judge_verdict=cached,
        )
    try:
        context = build_judge_context(
            result.task,
            stark_app_catalog_entry(result.task),
            result.trace,
            final_answer_from_trace(result.trace) or "",
        )
        verdict = judge_callable(config, context)
    except Exception as error:  # noqa: BLE001 - surfaced in the result row.
        verdict = JudgeVerdict(
            passed=None,
            status="error",
            raw=f"{type(error).__name__}: {error}",
            model=config.model,
            template_sha=JUDGE_TEMPLATE_SHA,
            attempts=0,
        )
    write_json_atomic(
        run.run_dir / "judge_verdict.json",
        {
            "passed": verdict.passed,
            "status": verdict.status,
            "raw": verdict.raw,
            "model": verdict.model,
            "template_sha": verdict.template_sha,
            "attempts": verdict.attempts,
        },
    )
    grade = grade_task(
        result.task,
        result.final_snapshot,
        result.trace,
        judge_verdict=verdict.passed if verdict.passed is not None else False,
    )
    return replace(
        run,
        run_result=replace(result, grade=grade),
        judge_verdict=verdict,
    )


def load_cached_judge_verdict(run_dir: Path) -> JudgeVerdict | None:
    path = run_dir / "judge_verdict.json"
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        status = str(payload["status"])
        if status not in {"pass", "fail", "error"}:
            return None
        return JudgeVerdict(
            passed=payload.get("passed"),
            status=cast(Literal["pass", "fail", "error"], status),
            raw=str(payload.get("raw", "")),
            model=str(payload["model"]),
            template_sha=str(payload["template_sha"]),
            attempts=int(payload["attempts"]),
        )
    except (KeyError, OSError, TypeError, ValueError):
        return None


def judge_reason_line(verdict: JudgeVerdict) -> str:
    lines = [line.strip() for line in verdict.raw.splitlines() if line.strip()]
    if verdict.status in {"pass", "fail"} and lines and lines[0].casefold() in {
        "pass",
        "fail",
    }:
        lines = lines[1:]
    return lines[0] if lines else ""


def _bounded_judge_result(event: "ToolTraceEvent") -> JsonDict | None:
    """Persist the rows a read actually returned, bounded like the judge digest.

    The judge verifies citations against retrieved rows; a stored trace
    without them makes every honest figure look fabricated.
    """

    if event.call.name not in {"get_widget_data", "read_widget"} or not event.ok:
        return None
    data = (event.result or {}).get("data")
    if isinstance(data, list):
        return {"data": data[:6]}
    if isinstance(data, dict):
        series = data.get("series")
        if isinstance(series, list):
            return {"data": {"series": series[:6]}}
        return {"data": data}
    return None


def persist_judge_input(run: ComparisonRun) -> None:
    """Store the bounded inputs needed to judge without replaying an agent."""

    task = run.run_result.task
    if not task.success.required_answer_judgment:
        return
    setup: JsonDict = {
        "initial_state": task.initial_state,
        "allowed_tools": list(task.allowed_tools),
    }
    if task.workspace_baseline is not None:
        setup["workspace_baseline"] = task.workspace_baseline
    if task.workspace_backends:
        setup["workspace_backends"] = list(task.workspace_backends)
    if task.workspace_skills:
        setup["workspace_skills"] = list(task.workspace_skills)
    if task.fixtures:
        setup["fixtures"] = {
            "backends": [
                {
                    "name": backend.name,
                    "backend_id": backend.backend_id,
                    "url": backend.url,
                }
                for backend in task.fixtures
            ]
        }
    payload = {
        "task": {
            "id": task.id,
            "category": task.category,
            "family": task.family,
            "difficulty": task.difficulty,
            "prompt": task.prompt,
            "setup": setup,
            "eval": {
                "judge_evaluation": True,
                "reference_trace": [
                    {"tool": call.name, "args": call.args}
                    for call in task.oracle_tool_calls
                ],
                **(
                    {"reference_answer": task.reference_answer}
                    if task.reference_answer
                    else {}
                ),
                **(
                    {"max_turns": task.limits["max_turns"]}
                    if task.limits.get("max_turns")
                    else {}
                ),
            },
        },
        "trace": [
            {
                "index": event.index,
                "tool": event.call.name,
                "args": event.call.args,
                "ok": event.ok,
                **(
                    {"result": _bounded_judge_result(event)}
                    if _bounded_judge_result(event) is not None
                    else {}
                ),
            }
            for event in run.run_result.trace
        ],
        "final_answer": final_answer_from_trace(run.run_result.trace) or "",
    }
    write_json_atomic(run.run_dir / "judge_input.json", payload)


def render_analysis_report(comparison: dict, output_dir: Path) -> str:
    model_payloads = []
    for model in comparison["models"]:
        result_path = Path(model["result_path"])
        if not result_path.is_absolute():
            result_path = Path.cwd() / result_path
        model_payloads.append(json.loads(result_path.read_text(encoding="utf-8")))

    lines = [
        "# Workspace Bench Model Comparison",
        "",
        f"- Benchmark: `{comparison['benchmark']['name']}`",
        f"- Git commit: `{comparison['benchmark']['git_commit']}`",
        f"- Git dirty: `{comparison['benchmark']['git_dirty']}`",
        f"- Workspace baseline: `{comparison['benchmark']['workspace_baseline']}`",
        f"- Tasks: `{comparison['task_count']}`",
        f"- Attempts: `{comparison.get('attempt_count', comparison['task_count'])}`",
        f"- Filters: `{json.dumps(comparison['filters'], sort_keys=True)}`",
        f"- Runner: `{comparison['runner']}`",
        f"- Repeats: `{comparison.get('repeats', 1)}`",
        "",
        "## How To Read This",
        "",
        "`pass_rate` is strict task success: a task counts as passed only when every grader check passes; process health is reported separately.",
        "`task_pass_rate` excludes provider/process failures and asks whether valid attempts satisfied the grader.",
        "`mean_score` is partial credit: it averages each task's fraction of passed checks.",
        "`pass@k` counts a task when at least one repeat passes. `pass^k` counts it only when every repeat passes.",
        "Two models can therefore have the same pass rate but different mean scores when they pass the same number of tasks but fail with different severity.",
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
                "| Model | pass@k | pass^k | Tasks | k Range |",
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
                f"{model.get('reliability_task_count', 0)} | "
                f"{k_range} |"
            )

    lines.extend(
        [
            "",
            "## By Difficulty",
            "",
            "| Model | Easy | Medium | Hard |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for model in comparison["models"]:
        by_difficulty = model.get("by_difficulty", {})
        lines.append(
            "| "
            f"{model['model']} | "
            f"{format_bucket(by_difficulty.get('easy'))} | "
            f"{format_bucket(by_difficulty.get('medium'))} | "
            f"{format_bucket(by_difficulty.get('hard'))} |"
        )

    lines.extend(
        [
            "",
            "## By Category",
            "",
            "| Model | " + " | ".join(TASK_CATEGORIES) + " |",
            "| --- | " + " | ".join("---:" for _ in TASK_CATEGORIES) + " |",
        ]
    )
    for model in comparison["models"]:
        by_category = model.get("by_category", {})
        category_cells = " | ".join(
            format_bucket(by_category.get(category)) for category in TASK_CATEGORIES
        )
        lines.append(f"| {model['model']} | {category_cells} |")

    lines.extend(["", "## Task Issue Counts", ""])
    for payload in model_payloads:
        label = payload["model"]["label"]
        issue_counts = Counter(
            issue["code"] for result in payload["results"] for issue in result["issues"]
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
            "| Model | Task | Repeat | Exit Code | Timed Out | Stderr Preview |",
            "| --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    process_rows = process_failure_rows(model_payloads)
    if process_rows:
        for row in process_rows:
            lines.append(
                "| "
                f"{row['model']} | "
                f"{row['task']} | "
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
            "## Task Matrix",
            "",
            "| Task | Category | Difficulty | "
            + " | ".join(payload["model"]["label"] for payload in model_payloads)
            + " |",
            "| --- | --- | --- | "
            + " | ".join("---:" for _ in model_payloads)
            + " |",
        ]
    )
    task_ids = model_payloads[0]["tasks"] if model_payloads else []
    results_by_model = [results_grouped_by_task(payload) for payload in model_payloads]
    for task_id in task_ids:
        first = results_by_model[0][task_id][0]
        cells = []
        for results in results_by_model:
            cells.append(format_result_cell(results[task_id]))
        lines.append(
            "| "
            f"{task_id} | "
            f"{first['category']} | "
            f"{first['difficulty']} | " + " | ".join(cells) + " |"
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


def results_grouped_by_task(payload: dict) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for result in payload["results"]:
        identity = result.get("qualified_id") or result["id"]
        grouped.setdefault(identity, []).append(result)
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
                    "task": result["id"],
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
    issue_counts = Counter(issue["code"] for result in results for issue in result["issues"])
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


def summarize_runs(
    runs: list[ComparisonRun], *, result_rows: list[dict] | None = None
) -> dict:
    total = len(runs)
    passed = sum(agent_run_passed(run) for run in runs)
    process_failures = sum(agent_run_process_failed(run) for run in runs)
    valid_runs = [run for run in runs if not agent_run_process_failed(run)]
    task_passed = sum(run.run_result.grade.passed for run in valid_runs)
    task_failures = len(valid_runs) - task_passed
    mean_score = sum(run.run_result.grade.score for run in runs) / total if total else 0.0
    state_passed = sum(run.run_result.grade.state_passed for run in valid_runs)
    trace_passed = sum(run.run_result.grade.trace_passed for run in valid_runs)
    preservation_runs = [
        run
        for run in valid_runs
        if run.run_result.grade.preservation_checks_total > 0
    ]
    preservation_passed = sum(
        run.run_result.grade.preservation_passed for run in preservation_runs
    )
    runtime_runs = [run for run in valid_runs if run.run_result.task.success.runtime is not None]
    runtime_passed = sum(run.run_result.grade.runtime_passed for run in runtime_runs)
    deterministic_passed = sum(
        run.run_result.grade.state_passed
        and run.run_result.grade.trace_passed
        and run.run_result.grade.preservation_passed
        and run.run_result.grade.runtime_passed
        for run in valid_runs
    )
    judged_runs = [
        run
        for run in valid_runs
        if run.run_result.task.success.required_answer_judgment
        and run.judge_verdict is not None
    ]
    judged_passed = sum(
        run.judge_verdict is not None and run.judge_verdict.passed is True
        for run in judged_runs
    )
    by_category: dict[str, dict[str, int]] = {}
    by_difficulty: dict[str, dict[str, int]] = {}
    outcomes_by_task: dict[str, list[bool]] = {}
    for run in runs:
        task = run.run_result.task
        outcomes_by_task.setdefault(task.qualified_id, []).append(agent_run_passed(run))
        for bucket, key in (
            (by_category, task.category),
            (by_difficulty, task.difficulty),
        ):
            item = bucket.setdefault(key, {"passed": 0, "total": 0})
            item["total"] += 1
            if agent_run_passed(run):
                item["passed"] += 1
    summary: dict[str, Any] = {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total if total else 0.0,
        "valid_attempts": len(valid_runs),
        "task_passed": task_passed,
        "task_failures": task_failures,
        "task_pass_rate": task_passed / len(valid_runs) if valid_runs else 0.0,
        "mean_score": mean_score,
        "state_passed": state_passed,
        "state_pass_rate": state_passed / len(valid_runs) if valid_runs else 0.0,
        "trace_passed": trace_passed,
        "trace_pass_rate": trace_passed / len(valid_runs) if valid_runs else 0.0,
        "mean_state_score": (
            sum(run.run_result.grade.state_score for run in runs) / total if total else 0.0
        ),
        "mean_trace_score": (
            sum(run.run_result.grade.trace_score for run in runs) / total if total else 0.0
        ),
        "preservation_task_count": len(preservation_runs),
        "preservation_passed": preservation_passed,
        "preservation_pass_rate": (
            preservation_passed / len(preservation_runs) if preservation_runs else 1.0
        ),
        "mean_preservation_score": (
            sum(run.run_result.grade.preservation_score for run in preservation_runs)
            / len(preservation_runs)
            if preservation_runs
            else 1.0
        ),
        "runtime_task_count": len(runtime_runs),
        "runtime_passed": runtime_passed,
        "runtime_pass_rate": (runtime_passed / len(runtime_runs) if runtime_runs else 1.0),
        "deterministic_passed": deterministic_passed,
        "deterministic_pass_rate": (
            deterministic_passed / len(valid_runs) if valid_runs else 0.0
        ),
        "judged_task_count": len(judged_runs),
        "judged_passed": judged_passed,
        "judged_pass_rate": (
            judged_passed / len(judged_runs) if judged_runs else 1.0
        ),
        "mean_runtime_score": (
            sum(run.run_result.grade.runtime_score for run in runtime_runs) / len(runtime_runs)
            if runtime_runs
            else 1.0
        ),
        "process_failures": process_failures,
        "by_category": by_category,
        "by_difficulty": by_difficulty,
        **compute_reliability_metrics(outcomes_by_task),
    }
    rows = result_rows or [agent_run_summary(run) for run in runs]
    calibration = summarize_result_rows(rows)
    summary.update(calibration)
    summary["pass_rate"] = calibration["strict_pass_rate"]
    slices = result_row_metric_slices(rows)
    summary["by_family_metrics"] = slices["by_family"]
    summary["by_difficulty_metrics"] = slices["by_difficulty"]
    summary["family_difficulty_matrix"] = slices["family_difficulty_matrix"]
    return summary


def agent_run_passed(run: ComparisonRun) -> bool:
    # Outcome-first: a task passes when every grader check passes. Completion
    # is already check-gated (answer tasks require final_answer; state and
    # trajectory checks require the work), so a process failure after the
    # outcome is achieved - a trailing malformed turn, a timeout during
    # wrap-up - does not void the pass. Process health stays reported
    # separately via agent_run_process_failed.
    return run.run_result.grade.passed


def agent_run_process_failed(run: ComparisonRun) -> bool:
    return run.exit_code != 0 or run.timed_out


def agent_run_summary(run: ComparisonRun) -> dict:
    result = run.run_result
    tool_call_count = len(result.trace)
    failed_tool_call_count = sum(not event.ok for event in result.trace)
    browser = browser_verdict_for_task(result.task.qualified_id)
    verdict = run.judge_verdict
    judge_status: str
    if result.task.success.required_answer_judgment:
        judge_status = verdict.status if verdict is not None else "pending"
    else:
        judge_status = "not_required"
    return {
        "id": result.task.id,
        "qualified_id": result.task.qualified_id,
        "repeat": run.repeat,
        "category": result.task.category,
        "family": result.task.family,
        "specification_level": result.task.specification_level,
        "difficulty": result.task.difficulty,
        "workspace_baseline": task_workspace_baseline(result.task),
        "passed": agent_run_passed(run),
        "process_failed": agent_run_process_failed(run),
        "task_failed": not agent_run_process_failed(run) and not result.grade.passed,
        "grade_passed": result.grade.passed,
        **grade_summary(result.grade, include_passed=False),
        "judge_passed": result.grade.judge_passed,
        "judge_pending": result.grade.judge_pending,
        "judge_checks_passed": result.grade.judge_checks_passed,
        "judge_checks_total": result.grade.judge_checks_total,
        "judge_status": judge_status,
        "judge_model": verdict.model if verdict is not None else None,
        "judge_template_sha": verdict.template_sha if verdict is not None else None,
        "judge_raw_reason": judge_reason_line(verdict) if verdict is not None else "",
        "tool_call_count": tool_call_count,
        "failed_tool_call_count": failed_tool_call_count,
        "browser_verdict": browser,
        "wall_time_seconds": round(run.wall_time_seconds, 6),
        "input_tokens": int(run.usage.get("input_tokens") or 0),
        "output_tokens": int(run.usage.get("output_tokens") or 0),
        "total_tokens": int(run.usage.get("total_tokens") or 0),
        "cached_tokens": int(run.usage.get("cached_tokens") or 0),
        "api_calls": int(run.usage.get("api_calls") or 0),
        "cost_usd": run.usage.get("cost_usd"),
        "cost_source": run.usage.get("cost_source"),
        "resumed": run.resumed,
        "agent_exit_code": run.exit_code,
        "agent_timed_out": run.timed_out,
        "agent_stdout": run.stdout,
        "agent_stderr": run.stderr,
        "runner": run.runner,
        "run_dir": str(run.run_dir),
        "task_path": str(run.task_path),
        "output_path": str(run.output_path),
    }


@lru_cache(maxsize=1)
def browser_verdict_index() -> dict[str, str]:
    """Index completed browser verdicts; missing task entries remain pending."""

    verdicts: dict[str, str] = {}
    root = resolve_repo_root() / "runs" / "browser-cert"
    if not root.exists():
        return verdicts
    for path in sorted(root.rglob("verdict.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        task_ref = payload.get("task_ref")
        if isinstance(task_ref, str) and isinstance(payload.get("passed"), bool):
            verdicts[task_ref] = "pass" if payload["passed"] else "fail"
    return verdicts


def browser_verdict_for_task(task_ref: str) -> str:
    return browser_verdict_index().get(task_ref, "pending")


def selected_filters(args: argparse.Namespace) -> dict:
    return {
        "track": getattr(args, "track", "guided"),
        "difficulty": args.difficulty,
        "family": args.family,
        "category": getattr(args, "category", None),
        "suite": getattr(args, "suite", "enterprise-apps-usage"),
        "task_dir": getattr(args, "task_dir", None),
    }


def benchmark_metadata(args: argparse.Namespace) -> dict:
    task_suite = None
    if getattr(args, "task_dir", None):
        task_suite = load_task_suite_manifest(Path(args.task_dir))
    else:
        task_suite = load_builtin_task_suite_manifest(
            getattr(args, "suite", "enterprise-apps-usage")
        )
    return {
        "name": BENCHMARK_NAME,
        "suite_id": task_suite.suite_id if task_suite else "local",
        "content_sha256": task_suite.content_sha256 if task_suite else None,
        "workspace_baseline": (
            task_suite.workspace_baseline
            if task_suite and task_suite.workspace_baseline is not None
            else "minimal"
        ),
        **git_provenance(Path(__file__).resolve()),
    }


def resolve_output_dir(args: argparse.Namespace) -> Path:
    if args.output_dir:
        return Path(args.output_dir)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    slice_name = args.run_name or args.difficulty
    safe_slice_name = "".join(
        char if char.isalnum() or char in {"-", "_"} else "-" for char in slice_name.lower()
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
    colors = ["#2563eb", "#16a34a", "#f97316", "#7c3aed", "#dc2626", "#0891b2"]

    title = (
        f"Workspace Bench {metric_label} "
        f"({comparison['filters']['difficulty']} difficulty, "
        f"{comparison['task_count']} tasks)"
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
