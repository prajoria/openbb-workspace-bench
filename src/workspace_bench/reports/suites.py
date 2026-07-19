"""Compile per-suite and aggregate results across task suites.

Suites stay separable — a new suite extends the report without touching
existing ones — and the aggregate pools current-era attempt counts per model
(never averages percentages). Historical inputs remain visible but are marked
ineligible for pooling; models without a current run are listed as pending.

Usage (one --run per model per suite; the suite name is free-form,
so a private suite joins the aggregate just by naming itself):
  uv run workspace-bench compile suites \
      --run core=runs/comparison/core-gpt-4.1-mini \
      --run my-desk-flows=runs/comparison/mydesk-gpt-4.1-mini \
      --output runs/reports/suites.json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from workspace_bench.core.runner import BUILTIN_TASK_SUITES, load_builtin_tasks
from workspace_bench.reports.metrics import (
    result_row_metric_slices,
    summarize_result_rows,
)


def load_model_results(source: Path) -> dict[str, dict[str, Any]]:
    """Read every per-model result JSON in an evaluator output directory."""

    models: dict[str, dict[str, Any]] = {}
    candidates = [source] if source.is_file() else sorted(source.glob("*.json"))
    for path in candidates:
        if path.name == "comparison.json":
            continue
        payload = json.loads(path.read_text())
        if not isinstance(payload, dict) or "results" not in payload:
            continue
        slug = path.stem
        models[slug] = payload
    return models


def summarize(
    rows: list[dict[str, Any]], task_metadata: dict[str, tuple[str, str]]
) -> dict[str, Any]:
    """Return the historical suite summary using the shared row metrics."""

    normalized_rows: list[dict[str, Any]] = []
    for row in rows:
        metadata = task_metadata.get(
            str(row.get("qualified_id")),
            task_metadata.get(str(row.get("id")), ("?", "?")),
        )
        family = str(metadata[0] if metadata[0] != "?" else row.get("family") or "?")
        difficulty = str(
            metadata[1] if metadata[1] != "?" else row.get("difficulty") or "?"
        )
        normalized_rows.append({**row, "family": family, "difficulty": difficulty})
    core = summarize_result_rows(normalized_rows)
    slices = result_row_metric_slices(normalized_rows)
    runtime_rows = [
        row
        for row in normalized_rows
        if int(row.get("runtime_checks_total") or 0) > 0
    ]
    issues: Counter[str] = Counter(
        str(issue.get("code", "?"))
        for row in normalized_rows
        if not bool(row.get("passed"))
        for issue in row.get("issues") or []
        if isinstance(issue, dict)
    )

    def bucket_rates(items: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
        return {
            key: {
                "passed": value["strict_passed"],
                "total": value["total"],
                "rate": round(value["strict_pass_rate"], 4),
            }
            for key, value in items.items()
        }

    total = len(normalized_rows)
    return {
        "passed": core["strict_passed"],
        "total": total,
        "unique_tasks": len(
            {str(row.get("qualified_id") or row.get("id")) for row in normalized_rows}
        ),
        "repeats": sorted({int(row.get("repeat", 1)) for row in normalized_rows}),
        "strict_pass_rate": round(core["strict_pass_rate"], 4) if total else None,
        "mean_score": (
            round(sum(float(row.get("score") or 0.0) for row in normalized_rows) / total, 4)
            if total
            else None
        ),
        "runtime_task_count": len(runtime_rows),
        "runtime_passed": core["runtime_passed"],
        "runtime_pass_rate": (
            round(float(core["runtime_pass_rate"]), 4) if runtime_rows else None
        ),
        "mean_runtime_score": (
            round(
                sum(float(row.get("runtime_score") or 0.0) for row in runtime_rows)
                / len(runtime_rows),
                4,
            )
            if runtime_rows
            else None
        ),
        "by_difficulty": bucket_rates(slices["by_difficulty"]),
        "by_family": bucket_rates(slices["by_family"]),
        "issue_codes": dict(issues.most_common()),
    }


def result_workspace_baseline(payload: dict[str, Any]) -> str:
    """Return the recorded baseline for one model result payload."""

    recorded = (payload.get("benchmark") or {}).get("workspace_baseline")
    if isinstance(recorded, str) and recorded:
        return recorded
    baselines = {
        str(row["workspace_baseline"])
        for row in payload.get("results", [])
        if isinstance(row, dict) and row.get("workspace_baseline")
    }
    if len(baselines) == 1:
        return baselines.pop()
    return "mixed" if baselines else "unknown"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run",
        action="append",
        required=True,
        metavar="SUITE=DIR",
        help="suite name = evaluator output directory (repeatable)",
    )
    parser.add_argument(
        "--historical-run",
        action="append",
        default=[],
        metavar="SUITE=FILE_OR_DIR",
        help="Pre-rename/pre-runtime result source retained for history but never pooled.",
    )
    parser.add_argument("--output", default="runs/reports/suites.json")
    args = parser.parse_args(argv)

    suites_map: dict[str, dict] = {}
    for spec in [*args.run, *args.historical_run]:
        name, _, directory = spec.partition("=")
        historical = spec in args.historical_run
        models = load_model_results(Path(directory))
        task_metadata = (
            {
                key: (task.family, task.difficulty)
                for task in load_builtin_tasks(name)
                for key in (task.id, task.qualified_id)
            }
            if name in BUILTIN_TASK_SUITES and not historical
            else {}
        )
        bucket = suites_map.setdefault(
            name,
            {
                "models": {},
                "status": (
                    "historical-pre-rename-pre-runtime"
                    if historical
                    else "current"
                ),
                "eligible_for_cross_suite_pooling": not historical,
            },
        )
        commits = set(bucket.get("git_commits", []))
        workspace_baselines = set(bucket.get("workspace_baselines", []))
        for slug, payload in models.items():
            commit = (payload.get("benchmark") or {}).get("git_commit")
            if commit:
                commits.add(str(commit))
            summary = summarize(payload["results"], task_metadata)
            workspace_baseline = result_workspace_baseline(payload)
            workspace_baselines.add(workspace_baseline)
            bucket["models"][slug] = {
                **summary,
                "workspace_baseline": workspace_baseline,
            }
            bucket["tasks"] = summary["unique_tasks"]
            bucket["attempts"] = summary["total"]
        bucket["git_commits"] = sorted(commits)
        bucket["workspace_baselines"] = sorted(workspace_baselines)

    current_suites = {
        name: bucket
        for name, bucket in suites_map.items()
        if bucket["eligible_for_cross_suite_pooling"]
    }
    historical_suites = [
        name
        for name, bucket in suites_map.items()
        if not bucket["eligible_for_cross_suite_pooling"]
    ]
    all_slugs = sorted(
        {slug for bucket in current_suites.values() for slug in bucket["models"]}
    )
    aggregate: dict[str, dict] = {}
    for slug in all_slugs:
        pooled_passed = pooled_total = 0
        included: list[str] = []
        pending = [f"{name} (pending re-run)" for name in historical_suites]
        for name, bucket in current_suites.items():
            summary = bucket["models"].get(slug)
            if summary:
                pooled_passed += summary["passed"]
                pooled_total += summary["total"]
                included.append(name)
            else:
                pending.append(name)
        aggregate[slug] = {
            "passed": pooled_passed,
            "total": pooled_total,
            "strict_pass_rate": round(pooled_passed / pooled_total, 4),
            "suites_included": included,
            "suites_pending": pending,
            "historical_suites_excluded": historical_suites,
        }

    report = {"suites": suites_map, "aggregate": aggregate}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Wrote {output}")
    for slug, agg in aggregate.items():
        pending_text = (
            f" (pending: {', '.join(agg['suites_pending'])})"
            if agg["suites_pending"]
            else ""
        )
        print(
            f"  {slug}: {agg['passed']}/{agg['total']} = "
            f"{100 * agg['strict_pass_rate']:.1f}%{pending_text}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
