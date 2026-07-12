"""Compile model result sets into calibration metrics and review matrices.

By default this preserves the historical behavior of reading complete
``runs/comparison/core-*`` result sets. Explicit paths may be files or
directories, which is useful for smoke runs and future build-suite calibration.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from workspace_bench.core.provenance import git_provenance
from workspace_bench.reports.metrics import (
    result_row_metric_slices,
    summarize_result_rows,
    task_reliability_matrix,
)

REPO = Path(__file__).resolve().parents[3]
DEFAULT_OUT = REPO / "runs/reports/calibration.json"


def result_files(inputs: list[str]) -> list[Path]:
    candidates: list[Path] = []
    if inputs:
        for raw in inputs:
            path = Path(raw)
            candidates.extend(path.rglob("*.json") if path.is_dir() else [path])
    else:
        for run_dir in sorted((REPO / "runs/comparison").glob("core-*")):
            candidates.extend(run_dir.glob("*.json"))
    selected = []
    for path in sorted(set(candidates)):
        if path.name in {"comparison.json"} or path.name.endswith(
            (".checkpoint.json", ".manifest.json")
        ):
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(payload, dict) and isinstance(payload.get("results"), list):
            selected.append(path)
    return selected


def compile_payload(
    paths: list[Path],
    *,
    expected_tasks: int = 0,
    current_metadata: dict[str, tuple[str, str]] | None = None,
) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    identities: dict[str, dict[str, Any]] = {}
    sources: dict[str, list[str]] = defaultdict(list)
    suite_hashes: set[str] = set()
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = [dict(row) for row in payload.get("results", [])]
        if current_metadata:
            for row in rows:
                task_ref = str(row.get("qualified_id") or row.get("id"))
                if task_ref in current_metadata:
                    row["family"], row["difficulty"] = current_metadata[task_ref]
        model = payload.get("model") or {}
        slug = str(model.get("slug") or path.stem)
        if expected_tasks and len({row.get("qualified_id") or row.get("id") for row in rows}) != expected_tasks:
            continue
        grouped[slug].extend(rows)
        identities[slug] = model
        sources[slug].append(str(path))
        content_hash = (payload.get("benchmark") or {}).get("content_sha256")
        if isinstance(content_hash, str):
            suite_hashes.add(content_hash)

    models = []
    per_task: dict[str, dict[str, Any]] = defaultdict(dict)
    task_metadata: dict[str, tuple[str, str]] = {}
    for slug, rows in sorted(grouped.items()):
        summary = summarize_result_rows(rows)
        process_failures = sum(bool(row.get("process_failed")) for row in rows)
        valid_rows = [row for row in rows if not row.get("process_failed")]
        summary["process_failure_count"] = process_failures
        summary["valid_attempt_count"] = len(valid_rows)
        summary["valid_attempt_strict_pass_rate"] = (
            sum(bool(row.get("passed")) for row in valid_rows) / len(valid_rows)
            if valid_rows
            else None
        )
        issues = Counter(
            str(issue.get("code"))
            for row in rows
            for issue in row.get("issues", [])
            if isinstance(issue, dict) and issue.get("code")
        )
        slices = result_row_metric_slices(rows)
        task_matrix = task_reliability_matrix(rows)
        for task in task_matrix:
            task_ref = str(task["task_ref"])
            task_metadata[task_ref] = (
                str(task.get("family") or "unknown"),
                str(task.get("difficulty") or "unknown"),
            )
            per_task[task_ref][slug] = task
        models.append(
            {
                "slug": slug,
                "label": identities[slug].get("label", slug),
                "provider": identities[slug].get("provider"),
                "model_id": identities[slug].get("id"),
                "sources": sorted(sources[slug]),
                "summary": summary,
                "families": slices["by_family"],
                "difficulties": slices["by_difficulty"],
                "family_difficulty_matrix": slices["family_difficulty_matrix"],
                "task_matrix": task_matrix,
                "top_issues": dict(issues.most_common(10)),
            }
        )

    tasks = [
        {
            "task_ref": task_ref,
            "family": task_metadata[task_ref][0],
            "difficulty": task_metadata[task_ref][1],
            "models": per_task[task_ref],
        }
        for task_ref in sorted(per_task)
    ]
    return {
        "schema_version": "workspace-bench-calibration/v2",
        **git_provenance(REPO),
        "suite_content_sha256": sorted(suite_hashes),
        "model_count": len(models),
        "task_count": len(tasks),
        "models": models,
        "tasks": tasks,
    }


def limitation_payload(paths: list[Path]) -> list[dict[str, Any]]:
    """Summarize excluded result sets without pooling their invalid attempts."""

    limitations = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows = payload.get("results") or []
        model = payload.get("model") or {}
        process_failures = [row for row in rows if row.get("process_failed")]
        valid_rows = [row for row in rows if not row.get("process_failed")]
        http_402 = sum("HTTP 402" in str(row.get("agent_stderr", "")) for row in rows)
        limitations.append(
            {
                "slug": str(model.get("slug") or path.stem),
                "label": str(model.get("label") or model.get("slug") or path.stem),
                "source": str(path),
                "attempts": len(rows),
                "process_failures": len(process_failures),
                "http_402_failures": http_402,
                "valid_attempts": len(valid_rows),
                "valid_attempt_summary": summarize_result_rows(valid_rows),
                "excluded_from_difficulty": True,
                "reason": "coverage is truncated and order-biased after provider credit exhaustion",
            }
        )
    return limitations


def render_markdown(payload: dict[str, Any]) -> str:
    """Render the canonical calibration evidence and exclusions."""

    lines = [
        "# Build-suite calibration — 2026-07",
        "",
        "The empirical difficulty labels use only the three complete guided-track "
        "runs below (236 tasks × 2 repeats). Process failures caused by malformed "
        "model output remain strict failures. Provider-credit failures are excluded.",
        "",
        "## Clean-run summary",
        "",
        "| Model | Strict | State | Runtime | Invalid calls | Median turns | Recovery | Flip | Cost |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in payload["models"]:
        summary = model["summary"]
        lines.append(
            f"| {model['label']} | {summary['strict_passed']}/{summary['total']} "
            f"({summary['strict_pass_rate']:.1%}) | {summary['state_pass_rate']:.1%} | "
            f"{summary['runtime_pass_rate']:.1%} | "
            f"{summary['invalid_tool_call_rate']:.1%} | {summary['median_turns']:.1f} | "
            f"{summary['recovery_after_failure_rate']:.1%} | {summary['flip_rate']:.1%} | "
            f"${summary['cost_usd']:.2f} |"
        )
    lines.extend(["", "## Family × measured difficulty", ""])
    for model in payload["models"]:
        lines.extend(
            [
                f"### {model['label']}",
                "",
                "| Family | Easy | Medium | Hard |",
                "| --- | ---: | ---: | ---: |",
            ]
        )
        for family, cells in model["family_difficulty_matrix"].items():
            rendered = []
            for difficulty in ("easy", "medium", "hard"):
                cell = cells.get(difficulty)
                rendered.append(
                    "—"
                    if not cell
                    else f"{cell['strict_passed']}/{cell['total']} ({cell['strict_pass_rate']:.0%})"
                )
            lines.append(f"| {family} | {' | '.join(rendered)} |")
        lines.append("")
    limitations = payload.get("limitations") or []
    if limitations:
        lines.extend(
            [
                "## Excluded OpenRouter incidents",
                "",
                "These slices are supplementary only and never feed labels; valid attempts "
                "cover an alphabet-biased prefix of the suite.",
                "",
                "| Model | Process failures | HTTP 402 | Valid attempts | Strict | State | Runtime |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for item in limitations:
            summary = item["valid_attempt_summary"]
            lines.append(
                f"| {item['label']} | {item['process_failures']}/{item['attempts']} | "
                f"{item['http_402_failures']} | {item['valid_attempts']} | "
                f"{summary['strict_passed']}/{summary['total']} "
                f"({summary['strict_pass_rate']:.1%}) | "
                f"{summary['state_pass_rate']:.1%} | "
                f"{summary['runtime_pass_rate']:.1%} |"
            )
        lines.extend(
            [
                "",
                "Once credits are restored, rerun exactly:",
                "",
                f"```bash\n{payload.get('openrouter_rerun_command', '')}\n```",
                "",
            ]
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "inputs",
        nargs="*",
        help="Result JSON files or directories. Defaults to runs/comparison/core-*.",
    )
    parser.add_argument(
        "--suite",
        help="Join family/difficulty from the current bundled suite by qualified task id.",
    )
    parser.add_argument(
        "--limitation-input",
        action="append",
        default=[],
        help="Excluded result file to summarize as a limitation (repeatable).",
    )
    parser.add_argument("--markdown", help="Optional canonical Markdown analysis path.")
    parser.add_argument(
        "--openrouter-rerun-command",
        default="",
        help="Exact rerun command shown in the limitation section.",
    )
    parser.add_argument("--output", default=str(DEFAULT_OUT))
    parser.add_argument(
        "--expected-tasks",
        type=int,
        default=0,
        help="Ignore sets whose distinct task count differs; 0 accepts any size.",
    )
    args = parser.parse_args(argv)
    paths = result_files(args.inputs)
    current_metadata = None
    if args.suite:
        from workspace_bench.core.runner import load_builtin_tasks

        current_metadata = {
            task.qualified_id: (task.family, task.difficulty)
            for task in load_builtin_tasks(args.suite)
        }
    payload = compile_payload(
        paths,
        expected_tasks=args.expected_tasks,
        current_metadata=current_metadata,
    )
    payload["limitations"] = limitation_payload(
        [Path(path) for path in args.limitation_input]
    )
    payload["openrouter_rerun_command"] = args.openrouter_rerun_command
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.markdown:
        markdown = Path(args.markdown)
        markdown.parent.mkdir(parents=True, exist_ok=True)
        markdown.write_text(render_markdown(payload), encoding="utf-8")
    print(
        f"Wrote {output}: {payload['model_count']} model run(s), "
        f"{payload['task_count']} task(s)"
    )
    for model in payload["models"]:
        summary = model["summary"]
        print(
            f"  {model['slug']:24s} strict "
            f"{summary['strict_passed']}/{summary['total']} "
            f"state={summary['state_pass_rate']:.1%} "
            f"runtime={summary['runtime_pass_rate']} "
            f"invalid={summary['invalid_tool_call_rate']:.1%} "
            f"median_turns={summary['median_turns']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
