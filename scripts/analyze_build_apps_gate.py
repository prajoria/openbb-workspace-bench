"""Analyze a gating run over the build-openbb-apps suite.

Reads an evaluator per-model result JSON and prints the difficulty curve,
per-family pass rates, and the issue-code histogram.

Usage:
    uv run python scripts/analyze_build_apps_gate.py runs/comparison/<run>/<model>.json
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict

from workspace_bench.core.runner import load_builtin_tasks


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    payload = json.loads(open(sys.argv[1]).read())
    rows = payload["results"]
    task_metadata = {
        key: (task.family, task.difficulty)
        for task in load_builtin_tasks("build-openbb-apps")
        for key in (task.id, task.qualified_id)
    }
    difficulties = ["easy", "medium", "hard"]

    by_difficulty: dict[str, list] = defaultdict(list)
    by_family: dict[str, list] = defaultdict(list)
    issues: Counter = Counter()
    failures: list[tuple[str, str]] = []
    runtime_rows = [row for row in rows if int(row.get("runtime_checks_total") or 0) > 0]
    for row in rows:
        metadata = task_metadata.get(
            str(row.get("qualified_id")),
            task_metadata.get(str(row.get("id")), (None, None)),
        )
        difficulty = metadata[1] or row.get("difficulty")
        family = metadata[0] or row.get("family")
        if not isinstance(difficulty, str) or not isinstance(family, str):
            continue
        passed = bool(row["passed"])
        by_difficulty[difficulty].append(passed)
        by_family[family].append(passed)
        if not passed:
            first = row["issues"][0] if row["issues"] else {}
            code = first.get("code", "?") if isinstance(first, dict) else str(first)
            for issue in row["issues"] or []:
                if isinstance(issue, dict):
                    issues[issue.get("code", "?")] += 1
            failures.append((row["id"], code))

    total = sum(len(v) for v in by_difficulty.values())
    passed_total = sum(sum(v) for v in by_difficulty.values())
    print(
        f"tasks: {total}  strict pass: {passed_total} ({100 * passed_total / max(total, 1):.1f}%)\n"
    )
    if runtime_rows:
        runtime_passed = sum(bool(row.get("runtime_passed")) for row in runtime_rows)
        mean_runtime = sum(float(row.get("runtime_score") or 0.0) for row in runtime_rows) / len(
            runtime_rows
        )
        print(
            f"runtime: {runtime_passed}/{len(runtime_rows)} passed; "
            f"mean score {mean_runtime:.3f}\n"
        )

    print("difficulty curve (pass %):")
    curve = []
    for difficulty in difficulties:
        attempts = by_difficulty.get(difficulty, [])
        rate = 100 * sum(attempts) / max(len(attempts), 1)
        curve.append(rate)
        print(f"  {difficulty}: {rate:5.1f}%  ({sum(attempts)}/{len(attempts)})")
    monotonic = all(curve[i] >= curve[i + 1] for i in range(len(curve) - 1))
    print(f"  monotonic: {monotonic}\n")

    print(f"{'family':10s} {'pass':>9s}  rate")
    for family in sorted(by_family):
        attempts = by_family[family]
        print(
            f"{family:10s} {sum(attempts):4d}/{len(attempts):<4d} "
            f"{100 * sum(attempts) / len(attempts):5.1f}%"
        )

    # Per-family difficulty matrix catches a family whose labels do not track
    # empirical outcomes even when the aggregate curve looks reasonable.
    by_cell: dict[tuple[str, str], list] = defaultdict(list)
    for row in rows:
        metadata = task_metadata.get(
            str(row.get("qualified_id")),
            task_metadata.get(str(row.get("id")), (None, None)),
        )
        difficulty = metadata[1] or row.get("difficulty")
        family = metadata[0] or row.get("family")
        if isinstance(difficulty, str) and isinstance(family, str):
            by_cell[(family, difficulty)].append(bool(row["passed"]))
    print(f"\n{'family':10s}" + "".join(f"{d:>9s}" for d in difficulties) + "   curve")
    for family in sorted(by_family):
        cells = []
        rates = []
        for difficulty in difficulties:
            attempts = by_cell.get((family, difficulty), [])
            cells.append(f"{sum(attempts)}/{len(attempts)}" if attempts else "-")
            rates.append(sum(attempts) / len(attempts) if attempts else None)
        known = [rate for rate in rates if rate is not None]
        ladder = "ok" if all(a >= b for a, b in zip(known, known[1:])) else "BROKEN"
        if known and len(known) > 1 and max(known) - min(known) <= 0.25:
            ladder += " FLAT"
        print(f"{family:10s}" + "".join(f"{cell:>9s}" for cell in cells) + f"   {ladder}")

    print("\nissue codes across failures:")
    for code, count in issues.most_common(12):
        print(f"  {count:4d}  {code}")

    print(f"\nfailed tasks ({len(failures)}):")
    for task_id, code in failures[:60]:
        print(f"  {task_id}  [{code}]")
    if len(failures) > 60:
        print(f"  ... and {len(failures) - 60} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
