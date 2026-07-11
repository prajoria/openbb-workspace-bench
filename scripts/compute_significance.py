"""Compute uncertainty and pairwise significance for the published boards.

Reads every committed run under runs/comparison/ (core-* and build-*), joins
per-task outcomes with the CURRENT bundled suites for split slicing, and
writes runs/reports/significance.json with, per suite and model:

- strict pass counts with 95% Wilson confidence intervals
- the same for the held-out slice (validation + test splits) and test-only
- exact two-sided McNemar tests for every model pair (paired by task), so
  board ranks can be read with separability in mind

Everything is computed from committed artifacts; no model calls are made.

Usage:
    uv run python scripts/compute_significance.py
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SUITE_DIRS = {
    "core": REPO / "src/workspace_bench/core/task_suites/workspace_bench_v1",
    "build-openbb-apps": (
        REPO / "src/workspace_bench/core/task_suites/workspace_bench_v2_build_openbb_apps"
    ),
}
RUN_PREFIX = {"core": "core-", "build-openbb-apps": "build-"}
OUT = REPO / "runs/reports/significance.json"
Z = 1.959963984540054  # 95%


def wilson(passed: int, total: int) -> tuple[float, float]:
    if not total:
        return 0.0, 0.0
    phat = passed / total
    denom = 1 + Z * Z / total
    center = (phat + Z * Z / (2 * total)) / denom
    half = (
        Z
        * math.sqrt(phat * (1 - phat) / total + Z * Z / (4 * total * total))
        / denom
    )
    return max(0.0, center - half), min(1.0, center + half)


def mcnemar_exact(b: int, c: int) -> float:
    """Exact two-sided McNemar p-value from discordant-pair counts."""

    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (2**n)
    return min(1.0, 2 * tail)


def load_task_fields(suite_dir: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Return (task_id -> split, task_id -> level) from the shipped suite."""

    splits: dict[str, str] = {}
    levels: dict[str, str] = {}
    for path in sorted(suite_dir.glob("*.json")):
        if path.name == "task_suite.json":
            continue
        task = json.loads(path.read_text())
        splits[task["id"]] = task.get("split", "train")
        levels[task["id"]] = task.get("level", "?")
    return splits, levels


def load_runs(prefix: str) -> dict[str, dict[str, bool]]:
    """slug -> {task_id: strict pass} for every committed run directory."""

    outcomes: dict[str, dict[str, bool]] = {}
    for run_dir in sorted((REPO / "runs/comparison").glob(f"{prefix}*")):
        result_files = [
            f for f in run_dir.glob("*.json") if f.name != "comparison.json"
        ]
        if not result_files:
            continue
        payload = json.loads(result_files[0].read_text())
        slug = result_files[0].stem
        outcomes[slug] = {
            row["id"]: bool(row["passed"]) for row in payload.get("results", [])
        }
    return outcomes


def slice_summary(
    outcomes: dict[str, bool],
    splits: dict[str, str],
    wanted: set[str] | None,
) -> dict:
    ids = [
        task_id
        for task_id in outcomes
        if wanted is None or splits.get(task_id) in wanted
    ]
    passed = sum(outcomes[task_id] for task_id in ids)
    total = len(ids)
    low, high = wilson(passed, total)
    return {
        "passed": passed,
        "total": total,
        "rate": round(passed / total, 4) if total else None,
        "wilson_95_low": round(low, 4),
        "wilson_95_high": round(high, 4),
    }


def holdout_levels(
    outcomes: dict[str, bool],
    splits: dict[str, str],
    levels: dict[str, str],
) -> dict[str, dict]:
    by_level: dict[str, list[bool]] = defaultdict(list)
    for task_id, ok in outcomes.items():
        if splits.get(task_id) in {"validation", "test"}:
            by_level[levels.get(task_id, "?")].append(ok)
    return {
        level: {"passed": sum(oks), "total": len(oks)}
        for level, oks in sorted(by_level.items())
    }


def main() -> int:
    report: dict = {"suites": {}}
    for suite, suite_dir in SUITE_DIRS.items():
        splits, levels = load_task_fields(suite_dir)
        outcomes = load_runs(RUN_PREFIX[suite])
        if not outcomes:
            continue
        models: dict[str, dict] = {}
        for slug, per_task in sorted(outcomes.items()):
            models[slug] = {
                "all": slice_summary(per_task, splits, None),
                "holdout": slice_summary(per_task, splits, {"validation", "test"}),
                "test_only": slice_summary(per_task, splits, {"test"}),
                "holdout_by_level": holdout_levels(per_task, splits, levels),
            }
        ranked = sorted(
            outcomes, key=lambda slug: -models[slug]["all"]["passed"]
        )
        pairs = []
        for i, a in enumerate(ranked):
            for b_slug in ranked[i + 1 :]:
                shared = set(outcomes[a]) & set(outcomes[b_slug])
                b_only = sum(
                    1 for t in shared if outcomes[a][t] and not outcomes[b_slug][t]
                )
                c_only = sum(
                    1 for t in shared if not outcomes[a][t] and outcomes[b_slug][t]
                )
                pairs.append(
                    {
                        "a": a,
                        "b": b_slug,
                        "a_pass_b_fail": b_only,
                        "a_fail_b_pass": c_only,
                        "mcnemar_p": round(mcnemar_exact(b_only, c_only), 4),
                    }
                )
        report["suites"][suite] = {"models": models, "pairs": pairs}

        print(f"== {suite} ==")
        for slug in ranked:
            m = models[slug]
            print(
                f"  {slug:24s} strict {m['all']['passed']:3d}/{m['all']['total']} "
                f"({100 * m['all']['rate']:.1f}%, 95% CI "
                f"{100 * m['all']['wilson_95_low']:.1f}-{100 * m['all']['wilson_95_high']:.1f}) | "
                f"holdout {m['holdout']['passed']:3d}/{m['holdout']['total']} | "
                f"test {m['test_only']['passed']:2d}/{m['test_only']['total']}"
            )
        for i in range(len(ranked) - 1):
            pair = next(
                p for p in pairs if p["a"] == ranked[i] and p["b"] == ranked[i + 1]
            )
            verdict = "separable" if pair["mcnemar_p"] < 0.05 else "NOT separable"
            print(
                f"    {pair['a']} vs {pair['b']}: "
                f"+{pair['a_pass_b_fail']}/-{pair['a_fail_b_pass']} discordant, "
                f"p={pair['mcnemar_p']} ({verdict})"
            )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
