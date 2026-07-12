"""Compute uncertainty and pairwise significance for the published boards.

Reads the three complete 2026-07 build calibration runs, joins their repeated
per-task outcomes with the current build suite for split/difficulty slicing,
and writes runs/reports/significance.json with, per suite and model:

- strict pass counts with 95% Wilson confidence intervals
- the same for the held-out slice (validation + test splits) and test-only
- exact two-sided McNemar tests for every model pair (paired by task), so
  board ranks can be read with separability in mind

Retired core artifacts are marked historical/pre-rename and pending re-run;
they are never joined or pooled. No model calls are made.

Usage:
    uv run python scripts/compute_significance.py
"""

from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SUITE_DIRS = {
    "core": REPO / "src/workspace_bench/core/task_suites/core",
    "build-openbb-apps": (
        REPO / "src/workspace_bench/core/task_suites/build_openbb_apps"
    ),
}
BUILD_CALIBRATION_RUNS = (
    "openai-gpt-5.4-mini.json",
    "openai-gpt-5.1.json",
    "openai-gpt-5.5.json",
)
OUT = REPO / "runs/reports/significance.json"
Z = 1.959963984540054  # 95%


def wilson(passed: int, total: int) -> tuple[float, float]:
    if not total:
        return 0.0, 0.0
    phat = passed / total
    denom = 1 + Z * Z / total
    center = (phat + Z * Z / (2 * total)) / denom
    half = Z * math.sqrt(phat * (1 - phat) / total + Z * Z / (4 * total * total)) / denom
    return max(0.0, center - half), min(1.0, center + half)


def mcnemar_exact(b: int, c: int) -> float:
    """Exact two-sided McNemar p-value from discordant-pair counts."""

    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (2**n)
    return min(1.0, 2 * tail)


def load_task_fields(
    suite_dir: Path,
) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    """Return task split, difficulty, and family cluster maps."""

    splits: dict[str, str] = {}
    difficulties: dict[str, str] = {}
    clusters: dict[str, str] = {}
    for path in sorted(suite_dir.rglob("*.json"), key=lambda item: item.name):
        if path.name == "task_suite.json":
            continue
        task = json.loads(path.read_text())
        task_id = str(task["id"])
        family = str(task.get("family", "?"))
        suite = suite_dir.name.replace("_", "-")
        keys = (task_id, f"{suite}/{family}/{task_id}")
        for key in keys:
            splits[key] = task.get("split", "train")
            difficulties[key] = task.get("difficulty", "?")
            clusters[key] = family
    return splits, difficulties, clusters


def cluster_bootstrap_interval(
    values: dict[str, float],
    clusters: dict[str, str],
    *,
    iterations: int = 5000,
    seed: int = 20260711,
) -> tuple[float, float]:
    """Percentile interval resampling task families."""

    grouped: dict[str, list[float]] = defaultdict(list)
    for task_id, value in values.items():
        grouped[clusters.get(task_id, task_id)].append(value)
    names = sorted(grouped)
    if not names:
        return 0.0, 0.0
    rng = random.Random(seed)
    draws = []
    for _ in range(iterations):
        sampled = [grouped[rng.choice(names)] for _ in names]
        flat = [value for cluster in sampled for value in cluster]
        draws.append(sum(flat) / len(flat))
    draws.sort()
    return draws[int(0.025 * iterations)], draws[int(0.975 * iterations)]


def load_build_runs() -> tuple[dict[str, dict[str, bool]], dict[str, str]]:
    """Return per-model outcomes and each run's recorded Git commit."""

    outcomes: dict[str, dict[str, bool]] = {}
    commits: dict[str, str] = {}
    run_dir = REPO / "runs/comparison/build-calibration-202607-regraded"
    for filename in BUILD_CALIBRATION_RUNS:
        path = run_dir / filename
        payload = json.loads(path.read_text())
        slug = path.stem
        outcomes[slug] = {
            f"{row.get('qualified_id') or row['id']}#repeat-{int(row.get('repeat', 1))}": bool(
                row["passed"]
            )
            for row in payload.get("results", [])
        }
        commits[slug] = str((payload.get("benchmark") or {}).get("git_commit", "?"))
    return outcomes, commits


def task_ref(episode_ref: str) -> str:
    """Strip the repeat suffix used to keep paired attempts distinct."""

    return episode_ref.rsplit("#repeat-", 1)[0]


def slice_summary(
    outcomes: dict[str, bool],
    splits: dict[str, str],
    wanted: set[str] | None,
    clusters: dict[str, str],
) -> dict:
    ids = [
        episode_ref
        for episode_ref in outcomes
        if wanted is None or splits.get(task_ref(episode_ref)) in wanted
    ]
    passed = sum(outcomes[task_id] for task_id in ids)
    total = len(ids)
    low, high = wilson(passed, total)
    cluster_low, cluster_high = cluster_bootstrap_interval(
        {episode_ref: float(outcomes[episode_ref]) for episode_ref in ids},
        {
            episode_ref: clusters.get(task_ref(episode_ref), task_ref(episode_ref))
            for episode_ref in ids
        },
    )
    return {
        "passed": passed,
        "total": total,
        "rate": round(passed / total, 4) if total else None,
        "wilson_95_low": round(low, 4),
        "wilson_95_high": round(high, 4),
        "cluster_bootstrap_95_low": round(cluster_low, 4),
        "cluster_bootstrap_95_high": round(cluster_high, 4),
    }


def holdout_difficulties(
    outcomes: dict[str, bool],
    splits: dict[str, str],
    difficulties: dict[str, str],
) -> dict[str, dict]:
    by_difficulty: dict[str, list[bool]] = defaultdict(list)
    for episode_ref, ok in outcomes.items():
        ref = task_ref(episode_ref)
        if splits.get(ref) in {"validation", "test"}:
            by_difficulty[difficulties.get(ref, "?")].append(ok)
    return {
        difficulty: {"passed": sum(oks), "total": len(oks)}
        for difficulty, oks in sorted(by_difficulty.items())
    }


def main() -> int:
    report: dict = {"suites": {}}
    for suite, suite_dir in SUITE_DIRS.items():
        splits, difficulties, clusters = load_task_fields(suite_dir)
        if suite == "core":
            historical_dirs = sorted(
                str(path.relative_to(REPO))
                for path in (REPO / "runs/comparison").glob("core-*")
            )
            report["suites"][suite] = {
                "status": "pending-re-run",
                "era": "historical-pre-rename-pre-runtime",
                "models": {},
                "pairs": [],
                "historical_run_directories": historical_dirs,
                "note": (
                    "Historical core rows use retired pre-rename task ids and predate "
                    "the runtime dimension. They are not joined to current metadata or "
                    "pooled with 2026-07 build results."
                ),
            }
            continue
        outcomes, run_commits = load_build_runs()
        models: dict[str, dict] = {}
        for slug, per_task in sorted(outcomes.items()):
            models[slug] = {
                "all": slice_summary(per_task, splits, None, clusters),
                "holdout": slice_summary(per_task, splits, {"validation", "test"}, clusters),
                "test_only": slice_summary(per_task, splits, {"test"}, clusters),
                "holdout_by_difficulty": holdout_difficulties(
                    per_task, splits, difficulties
                ),
            }
        ranked = sorted(outcomes, key=lambda slug: -models[slug]["all"]["passed"])
        pairs: list[dict[str, object]] = []
        for i, a in enumerate(ranked):
            for b_slug in ranked[i + 1 :]:
                shared = set(outcomes[a]) & set(outcomes[b_slug])
                b_only = sum(1 for t in shared if outcomes[a][t] and not outcomes[b_slug][t])
                c_only = sum(1 for t in shared if not outcomes[a][t] and outcomes[b_slug][t])
                pairs.append(
                    {
                        "a": a,
                        "b": b_slug,
                        "a_pass_b_fail": b_only,
                        "a_fail_b_pass": c_only,
                        "mcnemar_p": round(mcnemar_exact(b_only, c_only), 4),
                        "task_iid_test": "McNemar (descriptive; sibling tasks are clustered)",
                        "cluster_bootstrap_difference_95": [
                            round(value, 4)
                            for value in cluster_bootstrap_interval(
                                {
                                    task_id: float(outcomes[a][task_id])
                                    - float(outcomes[b_slug][task_id])
                                    for task_id in shared
                                },
                                {
                                    episode_ref: clusters.get(
                                        task_ref(episode_ref), task_ref(episode_ref)
                                    )
                                    for episode_ref in shared
                                },
                            )
                        ],
                    }
                )
        manifest = json.loads((suite_dir / "task_suite.json").read_text())
        report["suites"][suite] = {
            "models": models,
            "pairs": pairs,
            "git_commits": sorted(set(run_commits.values())),
            "task_content_sha256": manifest.get("content_sha256"),
            "attempts_per_model": 472,
            "tasks_per_model": 236,
            "repeats": 2,
            "note": (
                "Intervals describe the three replay-regraded complete 2026-07 "
                "guided-track runs. "
                "Current measured difficulty and split metadata are joined by qualified "
                "task id; repeats remain distinct paired episodes."
            ),
        }

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
            pair = next(p for p in pairs if p["a"] == ranked[i] and p["b"] == ranked[i + 1])
            p_value_raw = pair["mcnemar_p"]
            assert isinstance(p_value_raw, (int, float))
            p_value = float(p_value_raw)
            verdict = "separable" if p_value < 0.05 else "NOT separable"
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
