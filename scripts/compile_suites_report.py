"""Compile per-suite and aggregate results across task suites.

Suites stay separable — a new suite extends the report without touching
existing ones — and the aggregate POOLS task counts per model (never averages
percentages), so models that have not run a suite are listed as pending there
and excluded from its pool.

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
import re
from collections import Counter, defaultdict
from pathlib import Path

ID_SHAPE = re.compile(r"^(?:gen|auth)_(t\d)_([a-z0-9]+)_")


def load_model_results(comparison_dir: Path) -> dict[str, dict]:
    """Read every per-model result JSON in an evaluator output directory."""

    models: dict[str, dict] = {}
    for path in sorted(comparison_dir.glob("*.json")):
        if path.name == "comparison.json":
            continue
        payload = json.loads(path.read_text())
        if not isinstance(payload, dict) or "results" not in payload:
            continue
        slug = path.stem
        models[slug] = payload
    return models


def summarize(rows: list[dict]) -> dict:
    by_level: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    by_family: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    issues: Counter = Counter()
    passed = 0
    score_sum = 0.0
    for row in rows:
        match = ID_SHAPE.match(row["id"])
        level = match.group(1) if match else "?"
        family = match.group(2) if match else "?"
        ok = bool(row["passed"])
        passed += ok
        score_sum += float(row.get("score") or 0.0)
        by_level[level][1] += 1
        by_level[level][0] += ok
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
        "strict_pass_rate": round(passed / total, 4) if total else None,
        "mean_score": round(score_sum / total, 4) if total else None,
        "by_level": {
            level: {"passed": p, "total": t, "rate": round(p / t, 4)}
            for level, (p, t) in sorted(by_level.items())
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
        "--run", action="append", required=True, metavar="SUITE=DIR",
        help="suite name = evaluator output directory (repeatable)",
    )
    parser.add_argument("--output", default="runs/reports/suites.json")
    args = parser.parse_args()

    suites_map: dict[str, dict] = {}
    for spec in args.run:
        name, _, directory = spec.partition("=")
        models = load_model_results(Path(directory))
        bucket = suites_map.setdefault(name, {"models": {}})
        for slug, payload in models.items():
            summary = summarize(payload["results"])
            bucket["models"][slug] = summary
            bucket["tasks"] = summary["total"]

    all_slugs = sorted({
        slug for bucket in suites_map.values() for slug in bucket["models"]
    })
    aggregate: dict[str, dict] = {}
    for slug in all_slugs:
        pooled_passed = pooled_total = 0
        included, pending = [], []
        for name, bucket in suites_map.items():
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
        }

    report = {"suites": suites_map, "aggregate": aggregate}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Wrote {output}")
    for slug, agg in aggregate.items():
        pending = f" (pending: {', '.join(agg['suites_pending'])})" if agg["suites_pending"] else ""
        print(f"  {slug}: {agg['passed']}/{agg['total']} = "
              f"{100 * agg['strict_pass_rate']:.1f}%{pending}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
