"""Generate docs/task-catalog.md from the bundled task JSON files.

Reads every task in the unified workspace-bench-v1 pack and renders each
one's prompt, setup, novelty note, and exact pass/fail criteria as the grader
applies them. Regenerate after editing tasks so the catalog never drifts.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACK_DIR = REPO / "src/workspace_bench/core/task_suites/workspace_bench_v1"
BUILD_PACK_DIR = (
    REPO / "src/workspace_bench/core/task_suites/workspace_bench_v2_build_openbb_apps"
)
REPORT = REPO / "runs/reports/benchmark-report.md"
OUT = REPO / "docs/task-catalog.md"

LEVEL_NAMES = {
    "L0": "Inspect & answer",
    "L1": "Single-widget operations",
    "L2": "Dashboard construction",
    "L3": "Apps, skills & delegation",
    "L4": "Repair",
}


def load_noop_scores() -> dict[str, str]:
    """Parse the release report's task table for noop baseline scores."""
    scores: dict[str, str] = {}
    if not REPORT.exists():
        return scores
    for line in REPORT.read_text().splitlines():
        match = re.match(r"\| (\w+) \| \w+ \| L\d \|", line)
        if match:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            scores[cells[0]] = cells[-1]
    return scores


def fmt_args(args: dict) -> str:
    return json.dumps(args, separators=(", ", ": "))


def describe_initial_state(task: dict) -> list[str]:
    lines = []
    fixtures = [b.get("name") for b in task.get("fixtures", {}).get("backends", [])]
    if fixtures:
        lines.append(f"Fixture backends: {', '.join(fixtures)}")
    dash = task.get("initial_state", {}).get("dashboard")
    if not dash:
        lines.append("Initial workspace: empty (no seeded dashboard)")
        return lines
    tabs = dash.get("tabs", [])
    widgets = dash.get("widgets", [])
    generated = dash.get("generated_widgets", [])
    parts = [f"dashboard \"{dash.get('name', '')}\""]
    if tabs and any(t.get("id") for t in tabs):
        parts.append(f"{len(tabs)} tab(s): " + ", ".join(t.get("id") or "(unnamed)" for t in tabs))
    if widgets:
        parts.append(
            f"{len(widgets)} seeded widget(s): "
            + ", ".join(
                f"{w.get('widget_id')}({fmt_args(w.get('data_args', {}))})" for w in widgets
            )
        )
    if generated:
        parts.append(
            f"{len(generated)} seeded generated widget(s): "
            + ", ".join(f"{g.get('widget_type')} \"{g.get('name')}\"" for g in generated)
        )
    lines.append("Initial workspace: " + "; ".join(parts))
    return lines


def describe_success(success: dict) -> list[str]:
    """Translate a success block into the exact checks the grader runs."""
    checks: list[str] = []

    name_contains = success.get("required_dashboard_name_contains")
    if name_contains:
        checks.append(
            f"**Dashboard name** must contain \"{name_contains}\" "
            "(case-insensitive phrase or in-order word match, stopwords ignored) "
            "→ `dashboard_name`"
        )

    for tab in success.get("required_tabs", []):
        checks.append(f"**Tab** `{tab}` must exist (matched by tab id) → `missing_tab`")

    for req in success.get("required_widgets", []):
        min_count = req.get("min_count", 1)
        max_count = req.get("max_count")
        where = f" on tab `{req['tab_id']}`" if req.get("tab_id") else ""
        data = f" with data_args ⊇ {fmt_args(req['data_args'])}" if req.get("data_args") else ""
        line = (
            f"**Widget** ≥{min_count}× `{req.get('origin')}/{req.get('widget_id')}`"
            f"{data}{where} → `missing_widget`"
        )
        if max_count is not None:
            line += f"; and ≤{max_count} such widget(s) → `too_many_widgets`"
        checks.append(line)

    for req in success.get("required_generated_widgets", []):
        min_count = req.get("min_count", 1)
        where = f" on tab `{req['tab_id']}`" if req.get("tab_id") else ""
        name_part = (
            f" named ~\"{req['name_contains']}\"" if req.get("name_contains") else ""
        )
        content = req.get("data_contains", [])
        content_part = (
            " whose content mentions " + ", ".join(f"\"{c}\"" for c in content)
            if content
            else ""
        )
        checks.append(
            f"**Generated {req.get('widget_type')}** ≥{min_count}×{name_part}{content_part}{where} "
            "(case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) "
            "→ `missing_generated_widget`"
        )

    for req in success.get("required_layouts", []):
        target = req.get("widget_uuid") or req.get("widget_id")
        coords = ", ".join(
            f"{k}={req[k]}" for k in ("x", "y", "w", "h") if req.get(k) is not None
        )
        where = f" on tab `{req['tab_id']}`" if req.get("tab_id") else ""
        checks.append(
            f"**Layout** `{target}` must sit at exactly {coords}{where} → `layout_mismatch`"
        )

    for req in success.get("required_tool_calls", []):
        min_count = req.get("min_count", 1)
        args = (
            f" with args ⊇ {fmt_args(req['args_contains'])}"
            if req.get("args_contains")
            else ""
        )
        checks.append(
            f"**Tool call** ≥{min_count}× `{req.get('tool')}`{args} must appear in the trace "
            "→ `missing_tool_call`"
        )

    for req in success.get("required_tool_results", []):
        content = ", ".join(f"\"{c}\"" for c in req.get("data_contains", []))
        checks.append(
            f"**Tool result** of `{req.get('tool')}` must contain {content} "
            "(agent must actually retrieve the data) → `missing_tool_result`"
        )

    for req in success.get("required_resource_reads", []):
        content = ", ".join(f"\"{c}\"" for c in req.get("data_contains", []))
        checks.append(
            f"**Resource read** of `{req.get('uri')}` must contain {content} "
            "(agent must actually retrieve the resource) → `missing_resource_read`"
        )

    layout = success.get("layout", {})
    if layout.get("within_grid"):
        width = layout.get("grid_width", 40)
        checks.append(
            f"**Grid bounds**: every widget inside the {width}-column grid "
            "(x≥0, y≥0, w>0, h>0, x+w≤{0}) → `layout_out_of_grid`".format(width)
        )
    if layout.get("no_overlaps"):
        checks.append("**No overlaps**: no two widgets on the same tab intersect → `layout_overlap`")

    trace = success.get("trace_checks", {})
    max_invalid = trace.get("max_invalid_tool_calls")
    if max_invalid is not None:
        checks.append(
            f"**Trace**: ≤{max_invalid} invalid tool call(s) in the whole episode "
            "→ `too_many_invalid_calls`"
        )
    if trace.get("must_call_schema_before_create"):
        checks.append(
            "**Trace**: every `create_widget` must be preceded by a successful "
            "`get_widget_schema` for that same origin/widget → `schema_not_called_before_create`"
        )
    if trace.get("forbid_invented_widget_ids"):
        checks.append(
            "**Trace**: schema/create calls may only use widget ids previously returned by "
            "`list_available_widgets` → `unlisted_widget_id`"
        )
    if trace.get("max_repeated_snapshots") is not None:
        checks.append(
            f"**Trace**: ≤{trace['max_repeated_snapshots']} consecutive "
            "`get_workspace_snapshot` call(s) → `repeated_snapshots`"
        )
    return checks


def render_task(task: dict, pack: str, noop: dict[str, str]) -> str:
    sid = task["id"]
    lines = [f"#### `{sid}` — {task.get('title', '')}", ""]
    meta = (
        f"**{task.get('level')}** · {task.get('capability')} · "
        f"workflow: {task.get('workflow')} · {task.get('subdomain')} · "
        f"difficulty: {task.get('difficulty')} · split: {task.get('split', '-')}"
    )
    noop_score = noop.get(sid)
    if noop_score:
        meta += f" · no-op baseline score: {noop_score}"
    lines.append(meta)
    lines.append("")
    lines.append(f"> {task.get('prompt', '').strip()}")
    lines.append("")
    novelty = task.get("novelty", "").strip()
    if novelty:
        lines.append(f"- Novelty: {novelty}")
    for line in describe_initial_state(task):
        lines.append(f"- {line}")
    tools = task.get("allowed_tools", [])
    lines.append(f"- Allowed tools ({len(tools)}): " + ", ".join(f"`{t}`" for t in tools))
    max_turns = task.get("limits", {}).get("max_turns")
    oracle_steps = len(task.get("oracle_tool_calls", []))
    lines.append(f"- Turn budget: {max_turns} · oracle reference trace: {oracle_steps} calls")
    lines.append("")
    lines.append("**Passes only if all of these checks hold** (each failure emits the issue code shown):")
    lines.append("")
    for check in describe_success(task.get("success", {})):
        lines.append(f"- {check}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    noop = load_noop_scores()
    packs = [(
        "core (workspace-bench-v1)",
        sorted(p for p in PACK_DIR.glob("*.json") if p.name != "task_suite.json"),
    ), (
        "build-openbb-apps (workspace-bench-v2-build-openbb-apps)",
        sorted(p for p in BUILD_PACK_DIR.glob("*.json") if p.name != "task_suite.json"),
    )]

    out = [
        "# WorkspaceBench Task Catalog",
        "",
        "Auto-generated from the bundled task JSON files — regenerate with",
        "`python scripts/generate_task_catalog.py` after editing tasks.",
        "",
        "## How grading works",
        "",
        "Every criterion below becomes one or more boolean checks in `grade_task`",
        "(`src/workspace_bench/core/graders.py`):",
        "",
        "- **Strict pass** requires *every* check to pass. One failed check fails the task.",
        "- **Score** is partial credit: `checks_passed / checks_total`.",
        "- Each failed check emits a stable **issue code** (shown per criterion below), so",
        "  failures aggregate meaningfully across runs.",
        "- For external agent runs, a **process failure** (non-zero exit, timeout, unparseable",
        "  tool-call output) also fails the attempt regardless of state.",
        "- Widget `data_args` use **nested subset matching**: extra args are fine, expected keys",
        "  must match exactly.",
        "- Generated-widget and tool-result content checks are **case-insensitive** and accept",
        "  widget-name aliases (\"price_performance\" ≈ \"price performance\") and numeric",
        "  equivalence (0.5 ≈ 50%).",
        "- The **no-op baseline score** shown per task is the partial credit an agent gets for",
        "  doing nothing — the gap to 1.0 is what the task actually demands. Release gates",
        "  require the no-op to *fail* every task and the oracle trace to *pass* every one.",
        "",
    ]

    total = 0
    for pack_name, files in packs:
        tasks = [json.loads(f.read_text()) for f in files]
        total += len(tasks)
        out.append(f"## Pack: {pack_name} ({len(tasks)} tasks)")
        out.append("")
        by_level: dict[str, list[dict]] = {}
        for task in tasks:
            by_level.setdefault(task.get("level", "?"), []).append(task)
        for level in sorted(by_level):
            group = by_level[level]
            out.append(f"### {level} — {LEVEL_NAMES.get(level, '')} ({len(group)})")
            out.append("")
            for task in group:
                out.append(render_task(task, pack_name, noop))
        out.append("")

    out.append(f"---\n\nTotal: {total} tasks.")
    OUT.write_text("\n".join(out))
    print(f"Wrote {OUT} ({total} tasks)")


if __name__ == "__main__":
    main()
