"""Generate runs/reports/task-catalog.md from the simulator task JSON files.

Reads every task in the three bundled simulator tasksets and renders each one's prompt,
setup, and exact pass/fail criteria as the grader applies them.
Regenerate after editing tasks so the catalog never drifts.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from workspace_bench.core.models import task_payload_conditions

REPO = Path(__file__).resolve().parents[2]
SMOKE_DIR = REPO / "src/workspace_bench/tasksets/smoke"
APPS_DEFAULT_DIR = REPO / "src/workspace_bench/tasksets/enterprise_apps_default"
PACK_DIR = REPO / "src/workspace_bench/tasksets/workspace_tasks"
REPORT = REPO / "runs/reports/benchmark-report.md"
OUT = REPO / "runs/reports/task-catalog.md"


def load_noop_scores() -> dict[str, str]:
    """Parse the release report's task table for noop baseline scores."""
    scores: dict[str, str] = {}
    if not REPORT.exists():
        return scores
    for line in REPORT.read_text().splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.fullmatch(r"\d+\.\d+", cells[-1]):
            scores[cells[0]] = cells[-1]
    return scores


def fmt_args(args: dict) -> str:
    return json.dumps(args, separators=(", ", ": "))


def evaluation_of(task: dict) -> dict:
    """Return a task's evaluation fields from either supported schema."""
    evaluation = task.get("eval")
    if isinstance(evaluation, dict):
        return evaluation
    return {
        **task.get("success", {}),
        "reference": task.get("oracle_tool_calls", []),
        "limits": task.get("limits", {}),
    }


def describe_initial_state(task: dict) -> list[str]:
    lines = []
    conditions = task_payload_conditions(task)
    fixtures = [
        backend.get("name")
        for backend in conditions.get("fixtures", {}).get("backends", [])
    ]
    if fixtures:
        lines.append(f"Fixture backends: {', '.join(fixtures)}")
    dash = conditions.get("initial_state", {}).get("dashboard")
    if not dash:
        baseline = conditions.get("workspace_baseline")
        backends = conditions.get("workspace_backends", [])
        selected = conditions.get("default_selected_dashboard")
        if baseline is not None or backends or selected:
            parts = []
            if baseline:
                parts.append(f"baseline `{baseline}`")
            elif baseline == "":
                parts.append("bare workspace")
            if backends:
                parts.append("backends " + ", ".join(f"`{name}`" for name in backends))
            if selected:
                parts.append(f'active dashboard "{selected}"')
            lines.append("Initial workspace: " + "; ".join(parts))
            return lines
        lines.append("Initial workspace: empty (no seeded dashboard)")
        return lines
    tabs = dash.get("tabs", [])
    widgets = dash.get("widgets", [])
    generated = dash.get("generated_widgets", [])
    parts = [f'dashboard "{dash.get("name", "")}"']
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
            + ", ".join(f'{g.get("widget_type")} "{g.get("name")}"' for g in generated)
        )
    lines.append("Initial workspace: " + "; ".join(parts))
    return lines


def describe_success(success: dict) -> list[str]:
    """Translate a success block into the exact checks the grader runs."""
    checks: list[str] = []

    name_contains = success.get("required_dashboard_name_contains")
    if name_contains:
        checks.append(
            f'**Dashboard name** must contain "{name_contains}" '
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
        name_part = f' named ~"{req["name_contains"]}"' if req.get("name_contains") else ""
        content = req.get("data_contains", [])
        content_part = (
            " whose content mentions " + ", ".join(f'"{c}"' for c in content) if content else ""
        )
        checks.append(
            f"**Generated {req.get('widget_type')}** ≥{min_count}×{name_part}{content_part}{where} "
            "(case-insensitive; widget-name aliases and numeric equivalence like 0.5 ≈ 50% accepted) "
            "→ `missing_generated_widget`"
        )

    for req in success.get("required_layouts", []):
        target = req.get("widget_uuid") or req.get("widget_id")
        coords = ", ".join(f"{k}={req[k]}" for k in ("x", "y", "w", "h") if req.get(k) is not None)
        where = f" on tab `{req['tab_id']}`" if req.get("tab_id") else ""
        checks.append(
            f"**Layout** `{target}` must sit at exactly {coords}{where} → `layout_mismatch`"
        )

    for req in success.get("required_tool_calls", []):
        min_count = req.get("min_count", 1)
        args = f" with args ⊇ {fmt_args(req['args_contains'])}" if req.get("args_contains") else ""
        checks.append(
            f"**Tool call** ≥{min_count}× `{req.get('tool')}`{args} must appear in the trace "
            "→ `missing_tool_call`"
        )

    for req in success.get("required_tool_results", []):
        content = ", ".join(f'"{c}"' for c in req.get("data_contains", []))
        checks.append(
            f"**Tool result** of `{req.get('tool')}` must contain {content} "
            "(agent must actually retrieve the data) → `missing_tool_result`"
        )

    for req in success.get("required_resource_reads", []):
        content = ", ".join(f'"{c}"' for c in req.get("data_contains", []))
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
        checks.append(
            "**No overlaps**: no two widgets on the same tab intersect → `layout_overlap`"
        )

    return checks


def render_task(task: dict, noop: dict[str, str]) -> str:
    sid = task["id"]
    lines = [f"#### `{sid}`", ""]
    meta = (
        f"**{task.get('difficulty')}** · category: {task.get('category', '-')} · "
        f"specification: {task.get('specification_level', '-')}"
    )
    noop_score = noop.get(sid)
    if noop_score:
        meta += f" · no-op baseline score: {noop_score}"
    lines.append(meta)
    lines.append("")
    lines.append(f"> {task.get('prompt', '').strip()}")
    lines.append("")
    for line in describe_initial_state(task):
        lines.append(f"- {line}")
    tools = task_payload_conditions(task).get("allowed_tools", [])
    lines.append(f"- Allowed tools ({len(tools)}): " + ", ".join(f"`{t}`" for t in tools))
    evaluation = evaluation_of(task)
    max_turns = evaluation.get("limits", {}).get("max_turns")
    oracle_steps = len(evaluation.get("reference_trace") or evaluation.get("reference") or [])
    lines.append(f"- Turn budget: {max_turns} · oracle reference trace: {oracle_steps} calls")
    lines.append("")
    lines.append(
        "**Passes only if all of these checks hold** (each failure emits the issue code shown):"
    )
    lines.append("")
    for check in describe_success(
        {key: value for key, value in evaluation.items() if key not in ("reference", "reference_trace")}
    ):
        lines.append(f"- {check}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    noop = load_noop_scores()
    packs = [
        (
            "smoke",
            sorted(
                (p for p in SMOKE_DIR.rglob("*.json") if p.parent != SMOKE_DIR),
                key=lambda path: path.name,
            ),
        ),
        (
            "enterprise-apps-default",
            sorted(
                (
                    p
                    for p in APPS_DEFAULT_DIR.rglob("*.json")
                    if p.parent != APPS_DEFAULT_DIR
                ),
                key=lambda path: path.name,
            ),
        ),
        (
            "workspace-tasks",
            sorted(
                (p for p in PACK_DIR.rglob("*.json") if p.parent != PACK_DIR),
                key=lambda path: path.name,
            ),
        ),
    ]

    out = [
        "# WorkspaceBench Task Catalog",
        "",
        "Auto-generated from the bundled task JSON files — regenerate with",
        "`python scripts/generators/generate_task_catalog.py` after editing tasks.",
        "All three deterministic simulator tasksets are included.",
        "",
        "## How grading works",
        "",
        "Every criterion below becomes one or more boolean checks in `grade_task`",
        "(`src/workspace_bench/core/graders.py`):",
        "",
        "- **Strict pass** requires *every* check to pass. One failed check fails the task.",
        "- **Score** is outcome partial credit: the mean pass fraction across semantic state-check codes.",
        "  Trace-policy checks are reported separately and join state success for strict pass/fail.",
        "- Each failed check emits a stable **issue code** (shown per criterion below), so",
        "  failures aggregate meaningfully across runs.",
        "- For external agent runs, a **process failure** (non-zero exit, timeout, unparseable",
        "  tool-call output) also fails the attempt regardless of state.",
        "- Widget `data_args` use **nested subset matching**: extra args are fine, expected keys",
        "  must match exactly.",
        "- Generated-widget and tool-result content checks are **case-insensitive** and accept",
        '  widget-name aliases ("price_performance" ≈ "price performance") and numeric',
        "  equivalence (0.5 ≈ 50%).",
        "- The **no-op baseline score** shown per task is the partial credit an agent gets for",
        "  doing nothing — the gap to 1.0 is what the task actually demands. Release gates",
        "  require the no-op to *fail* every task and the oracle trace to *pass* every one.",
        "",
    ]

    total = 0
    for suite_name, files in packs:
        tasks = []
        for f in files:
            task = json.loads(f.read_text())
            # Slim payloads omit family (the directory) and labels the suite
            # manifest defaults supply; hydrate them the way the loader does.
            task.setdefault("family", f.parent.name)
            manifest_path = f.parent.parent / "taskset.json"
            if manifest_path.is_file():
                defaults = json.loads(manifest_path.read_text()).get("task_defaults") or {}
                for key, value in defaults.items():
                    task.setdefault(key, value)
            tasks.append(task)
        total += len(tasks)
        out.append(f"## Taskset: {suite_name} ({len(tasks)} tasks)")
        out.append("")
        by_family: dict[str, list[dict]] = {}
        for task in tasks:
            by_family.setdefault(task["family"], []).append(task)
        for family in sorted(by_family):
            group = by_family[family]
            out.append(f"### {family} ({len(group)})")
            out.append("")
            for task in group:
                out.append(render_task(task, noop))
        out.append("")

    out.append(f"---\n\nTotal: {total} tasks.")
    OUT.write_text("\n".join(out))
    print(f"Wrote {OUT} ({total} tasks)")


if __name__ == "__main__":
    main()
