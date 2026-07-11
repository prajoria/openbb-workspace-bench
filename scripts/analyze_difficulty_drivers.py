"""Root-cause analysis: what actually drives pass/fail in the building pack?

Tests three hypotheses against gate-run data:
H3  pass rate is governed by the number of graded leaf values NOT literally
    present in the prompt (the "derived-field count"), regardless of tier label.
HB  a material share of strict failures are budget/trace-only deaths
    (state checks all pass) or 1-check near-misses — mechanical, flaky mass.
HF  between-run flips on unchanged scenarios concentrate at t4 (borderline
    budget/turn edges), inflating apparent tier movement.

Usage:
  uv run python scripts/analyze_difficulty_drivers.py \
      runs/comparison/build-gpt-4.1-mini/openai-gpt-4.1-mini.json \
      [runs/comparison/build-gpt-oss-20b/ollama-gpt-oss-20b.json]
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

PACK = Path("src/workspace_bench/core/scenario_packs/workspace_bench_v2_build_openbb_apps")

TRACE_CODES = {
    "too_many_invalid_calls", "schema_not_called_before_create",
    "repeated_snapshots", "forbidden_tool_used", "unlisted_widget_id",
}


def leaf_values(payload) -> list:
    out = []
    if isinstance(payload, dict):
        for value in payload.values():
            out.extend(leaf_values(value))
    elif isinstance(payload, list):
        for value in payload:
            out.extend(leaf_values(value))
    else:
        out.append(payload)
    return out


def value_in_text(value, text: str) -> bool:
    if isinstance(value, bool):
        return str(value).lower() in text.lower()
    if isinstance(value, (int, float)):
        candidates = {json.dumps(value)}
        if isinstance(value, float) and value.is_integer():
            candidates.add(str(int(value)))
        return any(c in text for c in candidates)
    return str(value) in text


def scenario_loads(path: Path) -> tuple[int, int]:
    """Return (derived_count, stated_count) over graded widget/app def values.

    A graded leaf value is 'derived' when it appears neither in the prompt nor in
    the seeded custom-backend state (which the model can copy from)."""

    data = json.loads(path.read_text())
    prompt = data["prompt"]
    seeded = json.dumps(data.get("initial_state", {}).get("custom_backends", []))
    haystack = prompt + " " + seeded
    derived = stated = 0
    success = data.get("success", {})
    for req in success.get("required_widget_defs", []) + success.get("required_app_defs", []):
        graded: list = []
        graded += leaf_values(req.get("expect", {}))
        graded += leaf_values(req.get("params_include", []))
        graded += leaf_values(req.get("columns_include", []))
        graded += leaf_values(req.get("widgets_on_tab", []))
        graded += leaf_values(req.get("groups_include", []))
        for value in graded:
            if value_in_text(value, haystack):
                stated += 1
            else:
                derived += 1
    return derived, stated


def main() -> int:
    run_path = sys.argv[1]
    d = json.loads(Path(run_path).read_text())
    rows = {r["id"]: r for r in d["results"]}

    loads = {}
    for sid in rows:
        loads[sid] = scenario_loads(PACK / f"{sid}.json")

    # H3: pass rate by derived-count bucket, and per-tier mean derived count
    buckets = defaultdict(lambda: [0, 0])
    tier_derived = defaultdict(list)
    for sid, r in rows.items():
        derived, _ = loads[sid]
        bucket = min(derived // 4 * 4, 24)
        buckets[bucket][1] += 1
        buckets[bucket][0] += bool(r["passed"])
        tier = re.match(r"auth_(t\d)_", sid).group(1)
        tier_derived[tier].append((derived, bool(r["passed"])))

    print("H3 — pass rate by DERIVED-field bucket (tier-agnostic):")
    for b in sorted(buckets):
        passed, total = buckets[b]
        print(f"  derived {b:>2}-{b+3:>2}: {100*passed/total:5.1f}%  (n={total})")

    print("\nH3 — per-tier mean derived-field count vs pass rate:")
    for tier in ["t0", "t1", "t2", "t3", "t4"]:
        entries = tier_derived[tier]
        mean_derived = sum(e[0] for e in entries) / len(entries)
        rate = 100 * sum(e[1] for e in entries) / len(entries)
        print(f"  {tier}: mean derived={mean_derived:5.1f}  pass={rate:5.1f}%  (n={len(entries)})")

    # HB: failure anatomy
    print("\nHB — strict-failure anatomy per tier:")
    for tier in ["t0", "t1", "t2", "t3", "t4"]:
        fails = [r for sid, r in rows.items() if sid.startswith(f"auth_{tier}_") and not r["passed"]]
        trace_only = sum(
            1 for r in fails
            if r["issues"] and all(i["code"] in TRACE_CODES for i in r["issues"])
        )
        near = sum(1 for r in fails if r["score"] >= 0.9)
        print(f"  {tier}: fails={len(fails):3d}  trace-only={trace_only:2d}  score>=0.9 near-misses={near:2d}")

    # HF: run-to-run flips (optional second run)
    if len(sys.argv) > 2:
        d2 = json.loads(Path(sys.argv[2]).read_text())
        rows2 = {r["id"]: r["passed"] for r in d2["results"]}
        print("\nHF — flips between the two runs (same scenarios) per tier:")
        for tier in ["t0", "t1", "t2", "t3", "t4"]:
            ids = [sid for sid in rows if sid.startswith(f"auth_{tier}_") and sid in rows2]
            flips = sum(1 for sid in ids if bool(rows[sid]["passed"]) != bool(rows2[sid]))
            print(f"  {tier}: {flips}/{len(ids)} flipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
