"""Render blog charts from runs/reports/workspace-tasks-board.json."""
import json, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]
BOARD = json.load(open(REPO / "runs/reports/workspace-tasks-board.json"))
OUTDIR = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "runs/reports"
LEVELS = BOARD["levels"]
LABELS = ["Execute", "Find", "Derive", "Ground", "Compose"]
COLORS = {"gpt-4.1-mini": "#4A72B8", "gpt-5.5": "#2F855A", "glm": "#A8721C",
          "opus": "#C0504D", "kimi": "#7B5EA7", "gpt-oss": "#5E646D", "qwen3": "#9C27B0"}

def color_for(name):
    for k, v in COLORS.items():
        if k in name: return v
    return "#888888"

rows = [r for r in BOARD["board"] if not r.get("excluded")]

# staircase chart
fig, ax = plt.subplots(figsize=(8, 4.6))
for r in rows:
    rates = [ (r["per_level"][l]["rate"] or 0) * 100 for l in LEVELS ]
    label = r["model"].split(" (")[0].replace("-r3","")
    ax.plot(LABELS, rates, marker="o", lw=2.2, color=color_for(r["model"]), label=label)
ax.set_ylabel("pass@1 (%)"); ax.set_ylim(-3, 103)
ax.grid(alpha=0.25); ax.legend(frameon=False, fontsize=9)
ax.spines[["top","right"]].set_visible(False)
fig.tight_layout(); fig.savefig(OUTDIR / "wt-staircase.svg"); plt.close(fig)

# failure-code chart (top codes across models)
codes = {}
for r in rows:
    for c, n in r["issue_codes"].items():
        codes[c] = codes.get(c, 0) + n
top = [c for c, _ in sorted(codes.items(), key=lambda kv: -kv[1])[:6]]
fig, ax = plt.subplots(figsize=(8, 4.2))
width = 0.8 / max(len(rows), 1)
for i, r in enumerate(rows):
    total = r["episodes"]
    vals = [100 * r["issue_codes"].get(c, 0) / total for c in top]
    label = r["model"].split(" (")[0].replace("-r3","")
    ax.bar([x + i * width for x in range(len(top))], vals, width=width,
           color=color_for(r["model"]), label=label)
ax.set_xticks([x + width * (len(rows)-1)/2 for x in range(len(top))])
ax.set_xticklabels([c.replace("_","\n") for c in top], fontsize=8)
ax.set_ylabel("% of episodes with issue"); ax.grid(alpha=0.25, axis="y")
ax.legend(frameon=False, fontsize=9); ax.spines[["top","right"]].set_visible(False)
fig.tight_layout(); fig.savefig(OUTDIR / "wt-failure-codes.svg"); plt.close(fig)
print("charts written to", OUTDIR)
