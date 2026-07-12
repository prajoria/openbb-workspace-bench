"""Compile per-suite and aggregate results across task suites.

Suites stay separable — a new suite extends the report without touching
existing ones — and the aggregate pools current-era attempt counts per model
(never averages percentages). Historical inputs remain visible but are marked
ineligible for pooling; models without a current run are listed as pending.

Usage (one --run per model per suite; the suite name is free-form,
so a private suite joins the aggregate just by naming itself):
  uv run python scripts/compile_suites_report.py \
      --run core=runs/comparison/core-gpt-4.1-mini \
      --run build-openbb-apps=runs/comparison/build-gpt-4.1-mini \
      --run my-desk-flows=runs/comparison/mydesk-gpt-4.1-mini \
      --output runs/reports/suites.json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from workspace_bench.core.runner import BUILTIN_TASK_SUITES, load_builtin_tasks


def load_model_results(source: Path) -> dict[str, dict]:
    """Read every per-model result JSON in an evaluator output directory."""

    models: dict[str, dict] = {}
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


def summarize(rows: list[dict], task_metadata: dict[str, tuple[str, str]]) -> dict:
    by_difficulty: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    by_family: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    issues: Counter = Counter()
    passed = 0
    score_sum = 0.0
    runtime_scores: list[float] = []
    runtime_passed = 0
    for row in rows:
        metadata = task_metadata.get(
            str(row.get("qualified_id")),
            task_metadata.get(str(row.get("id")), ("?", "?")),
        )
        family = str(metadata[0] if metadata[0] != "?" else row.get("family") or "?")
        difficulty = str(
            metadata[1] if metadata[1] != "?" else row.get("difficulty") or "?"
        )
        ok = bool(row["passed"])
        passed += ok
        score_sum += float(row.get("score") or 0.0)
        if int(row.get("runtime_checks_total") or 0) > 0:
            runtime_scores.append(float(row.get("runtime_score") or 0.0))
            runtime_passed += bool(row.get("runtime_passed"))
        by_difficulty[difficulty][1] += 1
        by_difficulty[difficulty][0] += ok
        by_family[family][1] += 1
        by_family[family][0] += ok
        if not ok:
            for issue in row.get("issues") or []:
                if isinstance(issue, dict):
                    issues[issue.get("code", "?")] += 1
    total = len(rows)
    return {
        "passed": passed,
        "total": total,
        "unique_tasks": len(
            {str(row.get("qualified_id") or row.get("id")) for row in rows}
        ),
        "repeats": sorted({int(row.get("repeat", 1)) for row in rows}),
        "strict_pass_rate": round(passed / total, 4) if total else None,
        "mean_score": round(score_sum / total, 4) if total else None,
        "runtime_task_count": len(runtime_scores),
        "runtime_passed": runtime_passed,
        "runtime_pass_rate": (
            round(runtime_passed / len(runtime_scores), 4) if runtime_scores else None
        ),
        "mean_runtime_score": (
            round(sum(runtime_scores) / len(runtime_scores), 4) if runtime_scores else None
        ),
        "by_difficulty": {
            difficulty: {"passed": p, "total": t, "rate": round(p / t, 4)}
            for difficulty, (p, t) in sorted(by_difficulty.items())
        },
        "by_family": {
            family: {"passed": p, "total": t, "rate": round(p / t, 4)}
            for family, (p, t) in sorted(by_family.items())
        },
        "issue_codes": dict(issues.most_common()),
    }


def main() -> int:
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
    args = parser.parse_args()

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
        for slug, payload in models.items():
            commit = (payload.get("benchmark") or {}).get("git_commit")
            if commit:
                commits.add(str(commit))
            summary = summarize(payload["results"], task_metadata)
            bucket["models"][slug] = summary
            bucket["tasks"] = summary["unique_tasks"]
            bucket["attempts"] = summary["total"]
        bucket["git_commits"] = sorted(commits)

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
