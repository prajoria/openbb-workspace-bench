"""Deterministic state and trace graders for Workspace Bench."""

from __future__ import annotations

import json
import re
from collections import defaultdict

from workspace_bench.core.grading.backend import (
    definition_param_kinds as _definition_param_kinds,
    grade_app_structure as _grade_app_structure,
    grade_backend_building as _grade_backend_building,
    grade_business_names as _grade_business_names,
    grade_capabilities as _grade_capabilities,
    grade_capability_connections as _grade_capability_connections,
    grade_polish as _grade_polish,
)
from workspace_bench.core.grading.matching import (
    normalized_text as _normalized_text,
    phrase_matches as _phrase_matches,
)
from workspace_bench.core.grading.preservation import (
    grade_workspace_preservation as _grade_workspace_preservation,
)
from workspace_bench.core.grading.state import (
    declared_backend_widgets as _declared_backend_widgets,
    lookup_path as _lookup_path,
)
from workspace_bench.core.grading.trace import (
    grade_trace as _grade_trace,
    max_consecutive_snapshots as _max_consecutive_snapshots,
)
from workspace_bench.core.models import (
    GradeIssue,
    GradeResult,
    JsonDict,
    RequiredGeneratedWidget,
    RequiredLayout,
    RequiredResourceRead,
    RequiredToolCall,
    RequiredToolResult,
    RequiredWidget,
    Task,
    ToolTraceEvent,
)
from workspace_bench.workspace.geometry import rects_overlap
from workspace_bench.workspace.runtime import grade_runtime
from workspace_bench.workspace.widget_params import flatten_params


STATE_CHANGING_TOOLS = {
    "manage_dashboard",
    "manage_navigation_bar",
    "navigate_workspace",
    "create_widget",
    "update_widget",
    "delete_widget",
    "update_widget_layout",
    "add_generative_widget",
    "manage_apps",
}

__all__ = [
    "GradeBuilder",
    "grade_task",
    "flatten_params",
    "_declared_backend_widgets",
    "_definition_param_kinds",
    "_lookup_path",
    "_max_consecutive_snapshots",
]

TEXT_ALIASES = {
    "price_performance": ("price performance",),
    "latest_news": ("latest news",),
    "estimate_history": ("estimate history",),
    "fundamental_metrics": ("fundamental metrics",),
    "macro_timeseries": ("macro timeseries", "macro time series"),
    "yield_curve": ("yield curve",),
    "holdings_table": ("holdings", "holdings table"),
    "sector_exposure": ("sector exposure",),
    "risk_metrics": ("risk metrics",),
}


class GradeBuilder:
    """Accumulates pass/fail checks into one score."""

    def __init__(self, task_id: str):
        self.task_id = task_id
        self.passed = 0
        self.total = 0
        self.issues: list[GradeIssue] = []
        self.by_code: dict[str, list[int]] = defaultdict(lambda: [0, 0])

    def check(self, condition: bool, code: str, message: str) -> None:
        self.total += 1
        self.by_code[code][1] += 1
        if condition:
            self.passed += 1
            self.by_code[code][0] += 1
        else:
            self.issues.append(GradeIssue(code=code, message=message))

    @property
    def score(self) -> float:
        if not self.by_code:
            return 1.0
        # Each semantic rubric dimension has equal influence. Repeated widget
        # or layout instances refine that dimension instead of silently giving
        # long tasks more partial-credit weight.
        return sum(passed / total for passed, total in self.by_code.values()) / len(self.by_code)

    @property
    def passed_all(self) -> bool:
        return not self.issues


def grade_task(
    task: Task,
    final_snapshot: JsonDict,
    trace: tuple[ToolTraceEvent, ...],
    *,
    initial_snapshot: JsonDict | None = None,
) -> GradeResult:
    """Grade one task run against final state and trace checks."""

    state_builder = GradeBuilder(task.id)
    trace_builder = GradeBuilder(task.id)
    builder = state_builder
    composition = final_snapshot.get("dashboard_composition") or {}
    widgets = composition.get("widgets", [])
    tabs = composition.get("tabs", [])
    tab_ids = {tab.get("id") for tab in tabs}

    name_contains = task.success.required_dashboard_name_contains
    if name_contains:
        state_builder.check(
            _phrase_matches(str(composition.get("name", "")), name_contains),
            "dashboard_name",
            f"Active dashboard name should contain {name_contains!r}.",
        )

    for tab_id in task.success.required_tabs:
        state_builder.check(
            tab_id in tab_ids,
            "missing_tab",
            f"Expected tab {tab_id!r} in final dashboard.",
        )

    for required in task.success.required_widgets:
        matches = _matching_required_widgets(required, widgets)
        state_builder.check(
            len(matches) >= required.min_count,
            "missing_widget",
            (
                f"Expected at least {required.min_count} widget(s) "
                f"{required.origin}/{required.widget_id} with data_args "
                f"{required.data_args}, found {len(matches)}."
            ),
        )
        if required.max_count is not None:
            builder.check(
                len(matches) <= required.max_count,
                "too_many_widgets",
                (
                    f"Expected at most {required.max_count} widget(s) "
                    f"{required.origin}/{required.widget_id} with data_args "
                    f"{required.data_args}, found {len(matches)}."
                ),
            )

    for required_generated in task.success.required_generated_widgets:
        generated_matches = _matching_generated_widgets(required_generated, widgets)
        state_builder.check(
            len(generated_matches) >= required_generated.min_count,
            "missing_generated_widget",
            (
                f"Expected at least {required_generated.min_count} generated "
                f"{required_generated.widget_type} widget(s), "
                f"found {len(generated_matches)}."
            ),
        )

    for required_layout in task.success.required_layouts:
        layout_matches = _matching_layouts(required_layout, widgets)
        state_builder.check(
            bool(layout_matches),
            "layout_mismatch",
            f"No widget layout matched {required_layout}.",
        )

    for required_call in task.success.required_tool_calls:
        call_matches = _matching_tool_calls(required_call, trace)
        trace_builder.check(
            len(call_matches) >= required_call.min_count,
            "missing_tool_call",
            (
                f"Expected at least {required_call.min_count} "
                f"{required_call.name!r} call(s) with args containing "
                f"{required_call.args_contains}, found {len(call_matches)}."
            ),
        )

    for required_result in task.success.required_tool_results:
        result_matches = _matching_tool_results(required_result, trace)
        trace_builder.check(
            len(result_matches) >= required_result.min_count,
            "missing_tool_result",
            (
                f"Expected at least {required_result.min_count} "
                f"{required_result.name!r} result(s) containing "
                f"{required_result.data_contains}, found {len(result_matches)}."
            ),
        )

    for required_read in task.success.required_resource_reads:
        read_matches = _matching_resource_reads(required_read, trace)
        trace_builder.check(
            len(read_matches) >= required_read.min_count,
            "missing_resource_read",
            (
                f"Expected at least {required_read.min_count} resource read(s) "
                f"for {required_read.uri!r} containing "
                f"{required_read.data_contains}, found {len(read_matches)}."
            ),
        )

    if task.success.layout.within_grid:
        for widget in widgets:
            layout = widget.get("layout") or {}
            grid_width = task.success.layout.grid_width
            builder.check(
                _within_grid(layout, grid_width),
                "layout_out_of_grid",
                f"Widget {widget.get('widget_uuid')} is outside {grid_width}-column grid.",
            )

    if task.success.layout.no_overlaps:
        for tab_id, tab_widgets in _widgets_by_tab(widgets).items():
            overlaps = _find_overlaps(tab_widgets)
            builder.check(
                not overlaps,
                "layout_overlap",
                f"Tab {tab_id!r} has overlapping widgets: {overlaps}.",
            )

    runtime_grade = grade_runtime(task, final_snapshot)
    _grade_backend_building(builder, task, final_snapshot)
    capability_matches = _grade_capabilities(
        builder,
        task,
        final_snapshot,
        runtime_grade.deployment_receipt,
    )
    _grade_capability_connections(builder, task, final_snapshot, capability_matches)
    _grade_business_names(builder, task, final_snapshot)
    _grade_app_structure(builder, task, final_snapshot)
    _grade_workspace_preservation(
        builder,
        task,
        initial_snapshot=initial_snapshot,
        final_snapshot=final_snapshot,
    )

    _grade_trace(trace_builder, task, trace)
    polish_builder = GradeBuilder(task.id)
    _grade_polish(polish_builder, task, final_snapshot)
    issues = tuple(state_builder.issues + trace_builder.issues) + runtime_grade.issues
    outcome_score = (
        (state_builder.score + runtime_grade.score) / 2
        if task.success.runtime is not None
        else state_builder.score
    )
    return GradeResult(
        task_id=task.id,
        # Partial credit is outcome-based. Trace policy remains part of strict
        # pass/fail but cannot inflate or dilute state achievement.
        score=outcome_score,
        passed=(
            state_builder.passed_all
            and trace_builder.passed_all
            and runtime_grade.passed
        ),
        checks_passed=(
            state_builder.passed + trace_builder.passed + runtime_grade.checks_passed
        ),
        checks_total=state_builder.total + trace_builder.total + runtime_grade.checks_total,
        state_score=state_builder.score,
        state_passed=state_builder.passed_all,
        state_checks_passed=state_builder.passed,
        state_checks_total=state_builder.total,
        trace_score=trace_builder.score,
        trace_passed=trace_builder.passed_all,
        trace_checks_passed=trace_builder.passed,
        trace_checks_total=trace_builder.total,
        runtime_score=runtime_grade.score,
        runtime_passed=runtime_grade.passed,
        runtime_checks_passed=runtime_grade.checks_passed,
        runtime_checks_total=runtime_grade.checks_total,
        deployment_receipt=runtime_grade.deployment_receipt,
        polish_score=polish_builder.score,
        polish_checks_passed=polish_builder.passed,
        polish_checks_total=polish_builder.total,
        polish_issues=tuple(polish_builder.issues),
        issues=issues,
    )


def _matching_required_widgets(required: RequiredWidget, widgets: list[JsonDict]) -> list[JsonDict]:
    matches = []
    for widget in widgets:
        if widget.get("generated"):
            continue
        if widget.get("origin") != required.origin:
            continue
        if widget.get("widget_id") != required.widget_id:
            continue
        if required.tab_id is not None:
            layout = widget.get("layout") or {}
            if layout.get("tab_id") != required.tab_id:
                continue
        data_args = widget.get("data_args") or {}
        if not _dict_contains(data_args, required.data_args):
            continue
        matches.append(widget)
    return matches


def _matching_generated_widgets(
    required: RequiredGeneratedWidget, widgets: list[JsonDict]
) -> list[JsonDict]:
    matches = []
    for widget in widgets:
        if not widget.get("generated"):
            continue
        if widget.get("type") != required.widget_type:
            continue
        if required.tab_id is not None:
            layout = widget.get("layout") or {}
            if layout.get("tab_id") != required.tab_id:
                continue
        if (
            required.name_contains
            and required.name_contains.lower() not in str(widget.get("name", "")).lower()
        ):
            continue
        if (
            required.data_equals is not None
            and widget.get("generated_data") != required.data_equals
        ):
            continue
        data_blob = " ".join(
            [
                json.dumps(widget.get("generated_data"), sort_keys=True),
                str(widget.get("name", "")),
                str(widget.get("description", "")),
                str((widget.get("layout") or {}).get("tab_id", "")),
            ]
        )
        if any(not _generated_text_contains(data_blob, text) for text in required.data_contains):
            continue
        matches.append(widget)
    return matches


def _generated_text_contains(data_blob: str, expected: str) -> bool:
    data_lower = data_blob.lower()
    expected_lower = expected.lower()
    if expected_lower in data_lower:
        return True
    for alias in TEXT_ALIASES.get(expected_lower, ()):
        if alias.lower() in data_lower:
            return True
    if _normalized_text(expected_lower) in _normalized_text(data_lower):
        return True
    return _numeric_equivalent_contains(data_blob, expected)


def _numeric_equivalent_contains(data_blob: str, expected: str) -> bool:
    if not re.fullmatch(r"-?\d+(?:\.\d+)?", expected.strip()):
        return False
    expected_value = float(expected)
    for match in re.finditer(r"-?\d+(?:\.\d+)?\s*%?", data_blob):
        raw = match.group(0)
        observed = float(raw.rstrip("%").strip())
        if raw.strip().endswith("%"):
            observed /= 100
        if abs(observed - expected_value) <= 1e-9:
            return True
    return False


def _matching_layouts(required: RequiredLayout, widgets: list[JsonDict]) -> list[JsonDict]:
    matches = []
    expected_values = (
        ("x", required.x),
        ("y", required.y),
        ("w", required.w),
        ("h", required.h),
    )
    for widget in widgets:
        if required.widget_uuid and widget.get("widget_uuid") != required.widget_uuid:
            continue
        if required.widget_id and widget.get("widget_id") != required.widget_id:
            continue
        layout = widget.get("layout") or {}
        if required.tab_id is not None and layout.get("tab_id") != required.tab_id:
            continue
        if any(
            expected is not None and not _layout_value_equals(layout, key, expected)
            for key, expected in expected_values
        ):
            continue
        matches.append(widget)
    return matches


def _layout_value_equals(layout: JsonDict, key: str, expected: float) -> bool:
    value = layout.get(key)
    try:
        return value is not None and float(value) == expected
    except (TypeError, ValueError):
        return False


def _dict_contains(actual: JsonDict, expected: JsonDict) -> bool:
    # Required widget data_args and tool args are nested request payloads, so
    # expected dictionaries intentionally match recursively with exact leaves.
    for key, value in expected.items():
        observed = actual.get(key)
        if isinstance(observed, dict) and isinstance(value, dict):
            if not _dict_contains(observed, value):
                return False
            continue
        if observed != value:
            return False
    return True


def _matching_tool_calls(
    required: RequiredToolCall, trace: tuple[ToolTraceEvent, ...]
) -> list[ToolTraceEvent]:
    return [
        event
        for event in trace
        if event.ok
        and event.call.name == required.name
        and _dict_contains(event.call.args, required.args_contains)
    ]


def _matching_tool_results(
    required: RequiredToolResult, trace: tuple[ToolTraceEvent, ...]
) -> list[ToolTraceEvent]:
    matches = []
    for event in trace:
        if event.call.name != required.name or not event.ok:
            continue
        data_blob = json.dumps(event.result, sort_keys=True)
        if all(_generated_text_contains(data_blob, text) for text in required.data_contains):
            matches.append(event)
    return matches


def _matching_resource_reads(
    required: RequiredResourceRead, trace: tuple[ToolTraceEvent, ...]
) -> list[ToolTraceEvent]:
    matches = []
    for event in trace:
        if event.call.name != "read_workspace_resource" or not event.ok:
            continue
        if event.call.args.get("uri") != required.uri:
            continue
        data_blob = json.dumps(event.result, sort_keys=True)
        if all(_generated_text_contains(data_blob, text) for text in required.data_contains):
            matches.append(event)
    return matches


def _within_grid(layout: JsonDict, grid_width: int) -> bool:
    try:
        x = float(layout.get("x", 0))
        y = float(layout.get("y", 0))
        w = float(layout.get("w", 0))
        h = float(layout.get("h", 0))
    except (TypeError, ValueError):
        return False
    return x >= 0 and y >= 0 and w > 0 and h > 0 and x + w <= grid_width


def _widgets_by_tab(widgets: list[JsonDict]) -> dict[str, list[JsonDict]]:
    grouped: dict[str, list[JsonDict]] = defaultdict(list)
    for widget in widgets:
        layout = widget.get("layout") or {}
        grouped[str(layout.get("tab_id", ""))].append(widget)
    return grouped


def _find_overlaps(widgets: list[JsonDict]) -> list[tuple[str, str]]:
    overlaps = []
    for index, left in enumerate(widgets):
        for right in widgets[index + 1 :]:
            if rects_overlap(left.get("layout") or {}, right.get("layout") or {}):
                overlaps.append((str(left.get("widget_uuid")), str(right.get("widget_uuid"))))
    return overlaps
