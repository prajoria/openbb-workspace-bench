"""Compile the workspace_tasks model board from stored runs.

Pools the reference model's per-persona calibration runs (3 repeats each)
and joins single-pass board runs into one canonical record:
per-model overall pass@1, per-level rates, and issue-code fingerprints.
"""
from __future__ import annotations
import json, glob, sys
from collections import defaultdict
from pathlib import Path

LEVELS = [f"level{i}" for i in range(5)]
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "runs" / "reports" / "workspace-tasks-board.json"

PERSONAS = ["portfolio_manager", "fund_operations", "research_analyst",
            "trading_desk", "compliance_risk", "client_advisor"]
# exact per-persona dirs only: suffixed variants are stale-era runs
REFERENCE_DIRS = [
    str(REPO / f"runs/comparison/workspace-tasks-openai-gpt-4.1-mini-{p}") for p in PERSONAS
]
BOARD_DIRS = sorted(glob.glob(str(REPO / "runs/comparison/workspace-tasks-board-*")))

def result_files(run_dir: str):
    for p in glob.glob(run_dir + "/*.json"):
        name = Path(p).name
        if any(k in name for k in ("manifest", "checkpoint", "comparison")):
            continue
        yield p

def row(model_label: str, results: list[dict]) -> dict:
    lv = defaultdict(lambda: [0, 0])
    codes = defaultdict(int)
    passes = 0
    proc = 0
    for r in results:
        lv[r["difficulty"]][0] += bool(r["passed"]); lv[r["difficulty"]][1] += 1
        passes += bool(r["passed"]); proc += bool(r.get("process_failed"))
        if not r["passed"]:
            for i in r.get("issues", []):
                codes[i.get("code", "unknown")] += 1
    return {
        "model": model_label,
        "episodes": len(results),
        "pass_at_1": round(passes / len(results), 4) if results else None,
        "process_failures": proc,
        "per_level": {
            lvl: {"passes": lv[lvl][0], "attempts": lv[lvl][1],
                  "rate": round(lv[lvl][0] / lv[lvl][1], 4) if lv[lvl][1] else None}
            for lvl in LEVELS
        },
        "issue_codes": dict(sorted(codes.items(), key=lambda kv: -kv[1])),
    }

def main() -> int:
    board = []
    # reference model: pool all persona calibration runs
    ref_results = []
    for d in REFERENCE_DIRS:
        for f in result_files(d):
            ref_results.extend(json.load(open(f))["results"])
    if ref_results:
        board.append(row("gpt-4.1-mini (reference, 3 repeats pooled)", ref_results))
    for d in BOARD_DIRS:
        complete_rows = []
        for f in result_files(d):
            payload = json.load(open(f))
            complete_rows.extend(payload["results"])
        if not complete_rows:
            continue
        label = Path(d).name.replace("workspace-tasks-board-", "")
        r = row(label, complete_rows)
        # exclude runs dominated by process failures (credit/provider outages)
        if r["process_failures"] > len(complete_rows) * 0.2:
            r["excluded"] = "process failures exceed 20% - provider outage or credit limit; resume before publishing"
        board.append(r)
    OUT.write_text(json.dumps({"suite": "workspace_tasks", "protocol": "closed-world",
                               "levels": LEVELS, "board": board}, indent=1))
    for r in board:
        flag = " [EXCLUDED]" if r.get("excluded") else ""
        rates = "/".join(f"{(r['per_level'][l]['rate'] or 0)*100:.0f}" for l in LEVELS)
        print(f"{r['model']}: pass@1={r['pass_at_1']:.1%} levels {rates}{flag}")
    print("written:", OUT)
    return 0

if __name__ == "__main__":
    sys.exit(main())
