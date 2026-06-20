"""Deterministic state and trace graders for Workspace Bench."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from typing import Any

from workspace_bench.models import (
    GradeIssue,
    GradeResult,
    JsonDict,
    RequiredGeneratedWidget,
    RequiredLayout,
    RequiredToolCall,
    RequiredToolResult,
    RequiredWidget,
    Scenario,
    ToolTraceEvent,
)


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

STOPWORDS = {"a", "an", "and", "for", "of", "the"}


class GradeBuilder:
    """Accumulates pass/fail checks into one score."""

    def __init__(self, scenario_id: str):
        self.scenario_id = scenario_id
        self.passed = 0
        self.total = 0
        self.issues: list[GradeIssue] = []

    def check(self, condition: bool, code: str, message: str) -> None:
        self.total += 1
        if condition:
            self.passed += 1
        else:
            self.issues.append(GradeIssue(code=code, message=message))

    def result(self) -> GradeResult:
        score = self.passed / self.total if self.total else 1.0
        return GradeResult(
            scenario_id=self.scenario_id,
            score=score,
            passed=not self.issues,
            checks_passed=self.passed,
            checks_total=self.total,
            issues=tuple(self.issues),
        )


def grade_scenario(
    scenario: Scenario, final_snapshot: JsonDict, trace: tuple[ToolTraceEvent, ...]
) -> GradeResult:
    """Grade one scenario run against final state and trace checks."""

    builder = GradeBuilder(scenario.id)
    composition = final_snapshot.get("dashboard_composition") or {}
    widgets = composition.get("widgets", [])
    tabs = composition.get("tabs", [])
    tab_ids = {tab.get("id") for tab in tabs}

    name_contains = scenario.success.required_dashboard_name_contains
    if name_contains:
        builder.check(
            _phrase_matches(str(composition.get("name", "")), name_contains),
            "dashboard_name",
            f"Active dashboard name should contain {name_contains!r}.",
        )

    for tab_id in scenario.success.required_tabs:
        builder.check(
            tab_id in tab_ids,
            "missing_tab",
            f"Expected tab {tab_id!r} in final dashboard.",
        )

    for required in scenario.success.required_widgets:
        matches = _matching_required_widgets(required, widgets)
        builder.check(
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

    for required in scenario.success.required_generated_widgets:
        matches = _matching_generated_widgets(required, widgets)
        builder.check(
            len(matches) >= required.min_count,
            "missing_generated_widget",
            (
                f"Expected at least {required.min_count} generated "
                f"{required.widget_type} widget(s), found {len(matches)}."
            ),
        )

    for required_layout in scenario.success.required_layouts:
        matches = _matching_layouts(required_layout, widgets)
        builder.check(
            bool(matches),
            "layout_mismatch",
            f"No widget layout matched {required_layout}.",
        )

    for required_call in scenario.success.required_tool_calls:
        matches = _matching_tool_calls(required_call, trace)
        builder.check(
            len(matches) >= required_call.min_count,
            "missing_tool_call",
            (
                f"Expected at least {required_call.min_count} "
                f"{required_call.name!r} call(s) with args containing "
                f"{required_call.args_contains}, found {len(matches)}."
            ),
        )

    for required_result in scenario.success.required_tool_results:
        matches = _matching_tool_results(required_result, trace)
        builder.check(
            len(matches) >= required_result.min_count,
            "missing_tool_result",
            (
                f"Expected at least {required_result.min_count} "
                f"{required_result.name!r} result(s) containing "
                f"{required_result.data_contains}, found {len(matches)}."
            ),
        )

    if scenario.success.layout.within_grid:
        for widget in widgets:
            layout = widget.get("layout") or {}
            grid_width = scenario.success.layout.grid_width
            builder.check(
                _within_grid(layout, grid_width),
                "layout_out_of_grid",
                f"Widget {widget.get('widget_uuid')} is outside {grid_width}-column grid.",
            )

    if scenario.success.layout.no_overlaps:
        for tab_id, tab_widgets in _widgets_by_tab(widgets).items():
            overlaps = _find_overlaps(tab_widgets)
            builder.check(
                not overlaps,
                "layout_overlap",
                f"Tab {tab_id!r} has overlapping widgets: {overlaps}.",
            )

    _grade_trace(builder, scenario, trace)
    return builder.result()


def _matching_required_widgets(
    required: RequiredWidget, widgets: list[JsonDict]
) -> list[JsonDict]:
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
        if required.name_contains and required.name_contains.lower() not in str(
            widget.get("name", "")
        ).lower():
            continue
        data_blob = " ".join(
            [
                json.dumps(widget.get("generated_data"), sort_keys=True),
                str(widget.get("name", "")),
                str(widget.get("description", "")),
                str((widget.get("layout") or {}).get("tab_id", "")),
            ]
        )
        if any(
            not _generated_text_contains(data_blob, text)
            for text in required.data_contains
        ):
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


def _phrase_matches(actual: str, expected: str) -> bool:
    actual_lower = actual.lower()
    expected_lower = expected.lower()
    if expected_lower in actual_lower:
        return True
    actual_tokens = _meaningful_tokens(actual_lower)
    expected_tokens = _meaningful_tokens(expected_lower)
    if not expected_tokens:
        return False
    index = 0
    for token in actual_tokens:
        if index < len(expected_tokens) and token == expected_tokens[index]:
            index += 1
    return index == len(expected_tokens)


def _meaningful_tokens(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in STOPWORDS
    ]


def _normalized_text(text: str) -> str:
    return " ".join(_meaningful_tokens(text.replace("_", " ")))


def _matching_layouts(required: RequiredLayout, widgets: list[JsonDict]) -> list[JsonDict]:
    matches = []
    for widget in widgets:
        if required.widget_uuid and widget.get("widget_uuid") != required.widget_uuid:
            continue
        if required.widget_id and widget.get("widget_id") != required.widget_id:
            continue
        layout = widget.get("layout") or {}
        if required.tab_id is not None and layout.get("tab_id") != required.tab_id:
            continue
        if required.x is not None and float(layout.get("x")) != required.x:
            continue
        if required.y is not None and float(layout.get("y")) != required.y:
            continue
        if required.w is not None and float(layout.get("w")) != required.w:
            continue
        if required.h is not None and float(layout.get("h")) != required.h:
            continue
        matches.append(widget)
    return matches


def _dict_contains(actual: JsonDict, expected: JsonDict) -> bool:
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
        if event.call.name == required.name
        and _dict_contains(event.call.args, required.args_contains)
    ]


def _matching_tool_results(
    required: RequiredToolResult, trace: tuple[ToolTraceEvent, ...]
) -> list[ToolTraceEvent]:
    matches = []
    for event in trace:
        if event.call.name != required.name:
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
            if _rects_overlap(left.get("layout") or {}, right.get("layout") or {}):
                overlaps.append((str(left.get("widget_uuid")), str(right.get("widget_uuid"))))
    return overlaps


def _rects_overlap(left: JsonDict, right: JsonDict) -> bool:
    lx, ly, lw, lh = _rect(left)
    rx, ry, rw, rh = _rect(right)
    return lx < rx + rw and lx + lw > rx and ly < ry + rh and ly + lh > ry


def _rect(layout: JsonDict) -> tuple[float, float, float, float]:
    return (
        float(layout.get("x", 0)),
        float(layout.get("y", 0)),
        float(layout.get("w", 0)),
        float(layout.get("h", 0)),
    )


def _grade_trace(
    builder: GradeBuilder, scenario: Scenario, trace: tuple[ToolTraceEvent, ...]
) -> None:
    checks = scenario.success.trace
    invalid_count = sum(1 for event in trace if not event.ok)
    builder.check(
        invalid_count <= checks.max_invalid_tool_calls,
        "too_many_invalid_calls",
        (
            f"Expected <= {checks.max_invalid_tool_calls} invalid tool calls, "
            f"observed {invalid_count}."
        ),
    )

    if checks.must_call_schema_before_create:
        seen_schemas: set[tuple[str, str]] = set()
        for event in trace:
            args = event.call.args
            if event.call.name == "get_widget_schema" and event.ok:
                seen_schemas.add((str(args.get("origin")), str(args.get("widget_id"))))
            if event.call.name == "create_widget":
                origin = str(args.get("origin") or args.get("backend_name"))
                widget_id = str(args.get("widget_id"))
                builder.check(
                    (origin, widget_id) in seen_schemas,
                    "schema_not_called_before_create",
                    f"create_widget used {origin}/{widget_id} before get_widget_schema.",
                )

    if checks.forbid_invented_widget_ids:
        listed_widgets: set[tuple[str, str]] = set()
        for event in trace:
            if event.call.name == "list_available_widgets" and event.ok:
                for widget in (event.result.get("data") or {}).get("widgets", []):
                    listed_widgets.add((widget.get("origin"), widget.get("widget_id")))
            if event.call.name in {"get_widget_schema", "create_widget"}:
                origin = event.call.args.get("origin") or event.call.args.get("backend_name")
                widget_id = event.call.args.get("widget_id")
                if listed_widgets:
                    builder.check(
                        (origin, widget_id) in listed_widgets,
                        "unlisted_widget_id",
                        f"{event.call.name} used unlisted widget {origin}/{widget_id}.",
                    )

    if checks.max_repeated_snapshots is not None:
        max_seen = _max_consecutive_snapshots(trace)
        builder.check(
            max_seen <= checks.max_repeated_snapshots,
            "repeated_snapshots",
            (
                f"Expected <= {checks.max_repeated_snapshots} consecutive snapshots, "
                f"observed {max_seen}."
            ),
        )


def _max_consecutive_snapshots(trace: tuple[ToolTraceEvent, ...]) -> int:
    max_seen = 0
    current = 0
    for event in trace:
        if event.call.name == "get_workspace_snapshot":
            current += 1
            max_seen = max(max_seen, current)
            continue
        if event.call.name in STATE_CHANGING_TOOLS:
            current = 0
        else:
            current = 0
    return max_seen
