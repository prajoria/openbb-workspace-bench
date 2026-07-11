"""Compile v1 calibration results across all model runs into one JSON blob.

Reads every runs/comparison/v1-calib-*/<model>.json, joins tasks with
family/tier tags from the bundled pack, and writes
runs/reports/calibration.json with per-model strict totals, mean scores,
per-tier and per-family pass rates, and top issue codes. The blog chart is
rendered from this file.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACK = REPO / "src/workspace_bench/core/task_suites/workspace_bench_v1"
OUT = REPO / "runs/reports/calibration.json"

pack = {}
for f in PACK.glob("*.json"):
    if f.name == "task_suite.json":
        continue
    s = json.loads(f.read_text())
    pack[s["id"]] = (
        next(t[5:] for t in s["tags"] if t.startswith("tier-")),
        next(t[7:] for t in s["tags"] if t.startswith("family-")),
        s.get("difficulty", "medium"),
    )

models = []
per_task = defaultdict(dict)
for run_dir in sorted((REPO / "runs/comparison").glob("v1-calib-*")):
    result_files = [f for f in run_dir.glob("*.json") if f.name != "comparison.json"]
    if not result_files:
        continue
    d = json.loads(result_files[0].read_text())
    rows = d.get("results", [])
    if len(rows) != 300:
        continue
    slug = run_dir.name.removeprefix("v1-calib-")
    tiers = defaultdict(lambda: [0, 0])
    fams = defaultdict(lambda: [0, 0])
    diffs = defaultdict(lambda: [0, 0])
    codes = defaultdict(int)
    for r in rows:
        tier, fam, diff = pack[r["id"]]
        tiers[tier][0] += r["passed"]; tiers[tier][1] += 1
        fams[fam][0] += r["passed"]; fams[fam][1] += 1
        diffs[diff][0] += r["passed"]; diffs[diff][1] += 1
        for i in r["issues"]:
            codes[i["code"]] += 1
        per_task[r["id"]][slug] = {
            "passed": int(r["passed"]),
            "score": round(100 * r["score"]),
            "issue": r["issues"][0]["code"] if r["issues"] else None,
        }
    models.append({
        "slug": slug,
        "strict": sum(r["passed"] for r in rows),
        "mean_score": round(sum(r["score"] for r in rows) / 300, 4),
        "tiers": {t: [p, n] for t, (p, n) in sorted(tiers.items())},
        "families": {f: [p, n] for f, (p, n) in sorted(fams.items())},
        "difficulties": {d_: [p, n] for d_, (p, n) in sorted(diffs.items())},
        "top_issues": dict(sorted(codes.items(), key=lambda kv: -kv[1])[:6]),
    })

tasks = [
    {
        "id": sid,
        "tier": pack[sid][0],
        "family": pack[sid][1],
        "difficulty": pack[sid][2],
        "models": per_task[sid],
    }
    for sid in sorted(per_task)
]

OUT.write_text(json.dumps(
    {"release": "workspace-bench-v1", "models": models, "tasks": tasks},
    indent=1,
))
print(f"Wrote {OUT}: {len(models)} complete model runs")
for m in models:
    curve = " -> ".join(f"{t} {p}/{n}" for t, (p, n) in m["tiers"].items())
    print(f"  {m['slug']:16s} strict {m['strict']}/300 | {curve}")
