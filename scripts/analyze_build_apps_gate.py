"""Analyze a gpt-4.1-mini gating run over the Part 2 building pack.

Reads a the evaluator per-model result JSON and prints the level curve, per-family
pass rates, and the issue-code histogram — the calibration view used to accept or
reject the pack's difficulty ladder.

Usage:
    uv run python scripts/analyze_authoring_gate.py runs/comparison/<run>/<model>.json
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    payload = json.loads(open(sys.argv[1]).read())
    rows = payload["results"]
    levels = ["t0", "t1", "t2", "t3", "t4"]

    by_level: dict[str, list] = defaultdict(list)
    by_family: dict[str, list] = defaultdict(list)
    issues: Counter = Counter()
    failures: list[tuple[str, str]] = []
    for row in rows:
        match = re.match(r"auth_(t\d)_([a-z0-9]+)_", row["id"])
        if not match:
            continue
        level, family = match.group(1), match.group(2)
        passed = bool(row["passed"])
        by_level[level].append(passed)
        by_family[family].append(passed)
        if not passed:
            first = row["issues"][0] if row["issues"] else {}
            code = first.get("code", "?") if isinstance(first, dict) else str(first)
            for issue in row["issues"] or []:
                if isinstance(issue, dict):
                    issues[issue.get("code", "?")] += 1
            failures.append((row["id"], code))

    total = sum(len(v) for v in by_level.values())
    passed_total = sum(sum(v) for v in by_level.values())
    print(f"tasks: {total}  strict pass: {passed_total} "
          f"({100 * passed_total / max(total, 1):.1f}%)\n")

    print("level curve (pass %):")
    curve = []
    for level in levels:
        attempts = by_level.get(level, [])
        rate = 100 * sum(attempts) / max(len(attempts), 1)
        curve.append(rate)
        print(f"  {level}: {rate:5.1f}%  ({sum(attempts)}/{len(attempts)})")
    monotonic = all(curve[i] >= curve[i + 1] for i in range(len(curve) - 1))
    print(f"  monotonic: {monotonic}\n")

    print(f"{'family':10s} {'pass':>9s}  rate")
    for family in sorted(by_family):
        attempts = by_family[family]
        print(f"{family:10s} {sum(attempts):4d}/{len(attempts):<4d} "
              f"{100 * sum(attempts) / len(attempts):5.1f}%")

    # per-family ladder matrix — the instrument that catches misallocated level
    # material (a family whose t2 outpasses its t1 has its weight in the wrong
    # level even when the aggregate curve looks fine).
    by_cell: dict[tuple[str, str], list] = defaultdict(list)
    for row in rows:
        match = re.match(r"auth_(t\d)_([a-z0-9]+)_", row["id"])
        if match:
            by_cell[(match.group(2), match.group(1))].append(bool(row["passed"]))
    print(f"\n{'family':10s}" + "".join(f"{t:>7s}" for t in levels)
          + "   ladder")
    for family in sorted(by_family):
        cells = []
        rates = []
        for level in levels:
            attempts = by_cell.get((family, level), [])
            cells.append(f"{sum(attempts)}/{len(attempts)}" if attempts else "-")
            rates.append(
                sum(attempts) / len(attempts) if attempts else None
            )
        known = [rate for rate in rates if rate is not None]
        ladder = "ok" if all(a >= b for a, b in zip(known, known[1:])) else "BROKEN"
        if known and len(known) > 1 and max(known) - min(known) <= 0.25:
            ladder += " FLAT"
        print(f"{family:10s}" + "".join(f"{cell:>7s}" for cell in cells)
              + f"   {ladder}")

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
