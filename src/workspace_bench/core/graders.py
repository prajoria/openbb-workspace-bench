"""Deterministic state and trace graders for Workspace Bench."""

from __future__ import annotations

import json
import re
from collections import defaultdict

from workspace_bench.core.models import (
    DeploymentReceipt,
    GradeIssue,
    GradeResult,
    JsonDict,
    RequiredGeneratedWidget,
    RequiredLayout,
    RequiredResourceRead,
    RequiredToolCall,
    RequiredToolResult,
    RequiredWidget,
    RequiredCapability,
    Task,
    ToolTraceEvent,
)
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


def _grade_workspace_preservation(
    builder: GradeBuilder,
    task: Task,
    *,
    initial_snapshot: JsonDict | None,
    final_snapshot: JsonDict,
) -> None:
    checks = task.success.workspace
    if initial_snapshot is None:
        return

    initial_dashboards = initial_snapshot.get("dashboard_compositions") or {}
    final_dashboards = final_snapshot.get("dashboard_compositions") or {}
    if not isinstance(initial_dashboards, dict) or not isinstance(final_dashboards, dict):
        return

    if checks.preserve_other_dashboards:
        initial_active = str(
            (initial_snapshot.get("workspace_state") or {}).get("current_dashboard_uuid", "")
        )
        for dashboard_id, composition in initial_dashboards.items():
            if str(dashboard_id) == initial_active:
                continue
            builder.check(
                final_dashboards.get(dashboard_id) == composition,
                "collateral_dashboard_change",
                f"Unrelated dashboard {dashboard_id!r} changed or was deleted.",
            )

    initial_backends = initial_snapshot.get("custom_backends") or {}
    final_backends = final_snapshot.get("custom_backends") or {}
    if not isinstance(initial_backends, dict):
        initial_backends = {}
    if not isinstance(final_backends, dict):
        final_backends = {}

    if checks.preserve_custom_backend_ids:
        for backend_id, initial_backend in initial_backends.items():
            builder.check(
                backend_id in final_backends,
                "custom_backend_replaced",
                (
                    f"Existing custom backend {backend_id!r} "
                    f"({initial_backend.get('name')!r}) was replaced or deleted."
                ),
            )

    for backend_id in checks.required_custom_backend_ids:
        initial_backend = initial_backends.get(backend_id)
        builder.check(
            initial_backend is not None and backend_id in final_backends,
            "custom_backend_replaced",
            f"Required custom backend {backend_id!r} was replaced or deleted.",
        )

    if checks.unique_custom_backend_names:
        names = [
            str(backend.get("name", ""))
            for backend in final_backends.values()
            if isinstance(backend, dict)
        ]
        builder.check(
            len(names) == len(set(names)),
            "duplicate_custom_backend_name",
            "Custom backend names must be unique.",
        )

    if checks.require_no_backend_warnings:
        for backend_id, backend in final_backends.items():
            warnings = backend.get("warnings") or [] if isinstance(backend, dict) else []
            builder.check(
                not warnings,
                "backend_validation_warnings",
                f"Custom backend {backend_id!r} still has validation warnings: {warnings}.",
            )

    if checks.preserve_other_apps:
        mutable = set(checks.mutable_app_ids)
        for backend_id, initial_backend in initial_backends.items():
            if not isinstance(initial_backend, dict):
                continue
            final_backend = final_backends.get(backend_id)
            if not isinstance(final_backend, dict) and checks.unique_custom_backend_names:
                initial_name = str(initial_backend.get("name", ""))
                final_backend = next(
                    (
                        backend
                        for backend in final_backends.values()
                        if isinstance(backend, dict)
                        and str(backend.get("name", "")) == initial_name
                    ),
                    None,
                )
            initial_apps = initial_backend.get("apps_json") or []
            final_apps = (
                final_backend.get("apps_json") or []
                if isinstance(final_backend, dict)
                else []
            )
            final_by_id = {
                str(app.get("template_id") or app.get("id") or app.get("name")): app
                for app in final_apps
                if isinstance(app, dict)
            }
            for initial_app in initial_apps:
                if not isinstance(initial_app, dict):
                    continue
                app_id = str(
                    initial_app.get("template_id")
                    or initial_app.get("id")
                    or initial_app.get("name")
                )
                if app_id in mutable:
                    continue
                builder.check(
                    final_by_id.get(app_id) == initial_app,
                    "collateral_app_change",
                    f"Unrelated app {app_id!r} changed or was deleted.",
                )

    if checks.max_dashboard_delta is not None:
        delta = len(final_dashboards) - len(initial_dashboards)
        builder.check(
            delta <= checks.max_dashboard_delta,
            "unexpected_dashboard_created",
            (
                f"Expected at most {checks.max_dashboard_delta} new dashboard(s), "
                f"observed delta {delta}."
            ),
        )

    if checks.max_custom_backend_delta is not None:
        initial_count = len(initial_backends)
        final_count = len(final_backends)
        delta = final_count - initial_count
        builder.check(
            delta <= checks.max_custom_backend_delta,
            "unexpected_backend_created",
            (
                f"Expected at most {checks.max_custom_backend_delta} new custom "
                f"backend(s), observed delta {delta}."
            ),
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
    return [token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in STOPWORDS]


def _normalized_text(text: str) -> str:
    return " ".join(_meaningful_tokens(text.replace("_", " ")))


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


def _lookup_path(payload, dotted: str):
    """Resolve a dotted path inside nested dicts. Returns (found, value)."""

    current = payload
    for part in dotted.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False, None
    return True, current


def _normalized_render_fns(value) -> list[str]:
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    if isinstance(value, list):
        return [str(part).strip() for part in value]
    return []


def _subset_matches(spec: JsonDict, candidate: JsonDict) -> bool:
    for key, expected in spec.items():
        if key == "renderFn":
            expected_fns = set(_normalized_render_fns(expected))
            if expected_fns - set(_normalized_render_fns(candidate.get(key))):
                return False
            continue
        if candidate.get(key) != expected:
            return False
    return True


def _app_layout_items(app: JsonDict) -> list[tuple[str, JsonDict]]:
    items: list[tuple[str, JsonDict]] = []
    for tab_key, tab in (app.get("tabs") or {}).items():
        if not isinstance(tab, dict):
            continue
        for item in tab.get("layout", []) or []:
            if isinstance(item, dict):
                items.append((str(tab_key), item))
    return items


def _layout_items_overlap(first: JsonDict, second: JsonDict) -> bool:
    try:
        return (
            first["x"] < second["x"] + second["w"]
            and second["x"] < first["x"] + first["w"]
            and first["y"] < second["y"] + second["h"]
            and second["y"] < first["y"] + first["h"]
        )
    except (KeyError, TypeError):
        return False


def _find_custom_backend(snapshot: JsonDict, backend_name: str) -> JsonDict | None:
    for meta in (snapshot.get("custom_backends") or {}).values():
        if isinstance(meta, dict) and meta.get("name") == backend_name:
            return meta
    return None


def _widget_kinds(definition: JsonDict) -> set[str]:
    widget_type = str(definition.get("type", "table"))
    kinds: set[str] = set()
    if widget_type == "form" or any(
        str(param.get("type")) in {"form", "button"}
        for param in flatten_params(definition, recurse=True)
    ):
        kinds.add("form")
    if widget_type in {"ssrm_table", "live_grid"}:
        kinds.add("server-side-grid")
    elif widget_type == "table":
        kinds.add("table-like")
    elif widget_type in {
        "chart",
        "chart-highcharts",
        "chart-vegalite",
        "advanced_charting",
    }:
        kinds.add("chart-like")
    elif widget_type == "metric":
        kinds.add("metric")
    elif widget_type == "multi_file_viewer":
        kinds.add("multi-file")
    elif widget_type in {"html", "iframe", "markdown", "newsfeed", "pdf", "youtube"}:
        kinds.add(widget_type)
    return kinds or {"any"}


def _param_kind(param: JsonDict) -> str:
    name = str(param.get("paramName", "")).casefold()
    param_type = str(param.get("type", "text")).casefold()
    roles = {str(role).casefold() for role in param.get("roles", []) or []}
    if param_type == "ticker" or name in {"symbol", "ticker", "tickers"} or "ticker" in roles:
        return "ticker"
    if param_type == "date" or "date" in name:
        return "date"
    if param_type == "endpoint":
        return "endpoint"
    if param_type in {"number", "boolean", "tabs", "form", "button"}:
        return param_type
    return "text"


def _definition_param_kinds(definition: JsonDict) -> set[str]:
    return {
        _param_kind(param) for param in flatten_params(definition, recurse=True)
    }


def _declared_backend_widgets(
    final_snapshot: JsonDict,
) -> dict[tuple[str, str], JsonDict]:
    result: dict[tuple[str, str], JsonDict] = {}
    for backend in (final_snapshot.get("custom_backends") or {}).values():
        if not isinstance(backend, dict):
            continue
        backend_name = str(backend.get("name", ""))
        for widget_id, definition in (backend.get("widgets_json") or {}).items():
            if isinstance(definition, dict):
                result[(backend_name, str(widget_id))] = definition
    return result


def _instantiated_widget_keys(final_snapshot: JsonDict) -> set[tuple[str, str]]:
    dashboards = final_snapshot.get("dashboard_compositions") or {}
    keys: set[tuple[str, str]] = set()
    if isinstance(dashboards, dict):
        compositions = list(dashboards.values())
    else:
        compositions = [final_snapshot.get("dashboard_composition") or {}]
    for composition in compositions:
        if not isinstance(composition, dict):
            continue
        for widget in composition.get("widgets", []) or []:
            if isinstance(widget, dict) and not widget.get("generated"):
                keys.add((str(widget.get("origin", "")), str(widget.get("widget_id", ""))))
    return keys


def _runtime_valid_widget_datasets(
    receipt: DeploymentReceipt | None,
) -> dict[tuple[str, str], str]:
    if receipt is None:
        return {}
    return {
        (outcome.backend_name, outcome.widget_id): str(outcome.dataset_name)
        for outcome in receipt.widget_probes
        if outcome.passed and outcome.dataset_name is not None
    }


def _capability_candidates(
    capability: RequiredCapability,
    definitions: dict[tuple[str, str], JsonDict],
    instantiated: set[tuple[str, str]],
    runtime_valid: set[tuple[str, str]],
    task: Task,
) -> dict[tuple[str, str], JsonDict]:
    from workspace_bench.workspace.runtime import bind_dataset

    accepted: dict[tuple[str, str], JsonDict] = {}
    allowed_datasets = tuple(
        dataset
        for dataset in (task.success.runtime.datasets if task.success.runtime else ())
        if dataset.name in capability.datasets
    )
    for key, definition in definitions.items():
        if key not in instantiated or key not in runtime_valid:
            continue
        actual_kinds = _widget_kinds(definition)
        if capability.widget_kind != "any" and capability.widget_kind not in actual_kinds:
            continue
        if bind_dataset(definition, key[1], allowed_datasets) is None:
            continue
        accepted[key] = definition
    return accepted


def _grade_capabilities(
    builder: GradeBuilder,
    task: Task,
    final_snapshot: JsonDict,
    receipt: DeploymentReceipt | None,
) -> dict[str, set[tuple[str, str]]]:
    from workspace_bench.workspace.runtime import declared_fields

    definitions = _declared_backend_widgets(final_snapshot)
    instantiated = _instantiated_widget_keys(final_snapshot)
    runtime_valid = set(_runtime_valid_widget_datasets(receipt))
    contributors: dict[str, set[tuple[str, str]]] = {}
    for capability in task.success.required_capabilities:
        candidates = _capability_candidates(
            capability, definitions, instantiated, runtime_valid, task
        )
        builder.check(
            bool(candidates),
            "missing_capability",
            (
                f"Capability {capability.name!r} needs an instantiated, runtime-valid "
                f"{capability.widget_kind} widget bound to {list(capability.datasets)}."
            ),
        )
        required_fields = set(capability.must_cover_fields)
        contributing = {
            key
            for key, definition in candidates.items()
            if not required_fields or declared_fields(definition) & required_fields
        }
        covered = set().union(
            *(declared_fields(candidates[key]) for key in contributing)
        ) if contributing else set()
        builder.check(
            required_fields.issubset(covered),
            "capability_fields_uncovered",
            (
                f"Capability {capability.name!r} leaves fields "
                f"{sorted(required_fields - covered)} uncovered by runtime-valid widgets."
            ),
        )
        contributors[capability.name] = contributing
        param_kinds = set().union(
            *(_definition_param_kinds(candidates[key]) for key in contributors[capability.name])
        ) if contributors[capability.name] else set()
        for required_kind in capability.required_param_kinds:
            builder.check(
                required_kind in param_kinds,
                "capability_param_missing",
                (
                    f"Capability {capability.name!r} covering widgets do not expose a "
                    f"{required_kind!r} parameter."
                ),
            )
        for path, expected in capability.required_config.items():
            matches = []
            for key in contributors[capability.name]:
                found, actual = _lookup_path(candidates[key], path)
                matches.append(found and actual == expected)
            builder.check(
                any(matches),
                "capability_config_missing",
                (
                    f"Capability {capability.name!r} covering widgets do not provide "
                    f"required configuration {path}={expected!r}."
                ),
            )
    return contributors


def _shared_param_graph(
    final_snapshot: JsonDict,
    definitions: dict[tuple[str, str], JsonDict],
    param_kind: str,
) -> dict[tuple[str, str], set[tuple[str, str]]]:
    graph: dict[tuple[str, str], set[tuple[str, str]]] = defaultdict(set)
    for backend in (final_snapshot.get("custom_backends") or {}).values():
        if not isinstance(backend, dict):
            continue
        backend_name = str(backend.get("name", ""))
        for app in backend.get("apps_json", []) or []:
            if not isinstance(app, dict):
                continue
            for group in app.get("groups", []) or []:
                if not isinstance(group, dict) or group.get("type", "param") != "param":
                    continue
                param_name = str(group.get("paramName", ""))
                keys = [
                    (backend_name, str(widget_id))
                    for widget_id in group.get("widgetIds", []) or []
                ]
                eligible = [
                    key
                    for key in keys
                    if key in definitions
                    and any(
                        str(param.get("paramName", "")) == param_name
                        and _param_kind(param) == param_kind
                        for param in flatten_params(definitions[key], recurse=True)
                    )
                ]
                for key in eligible:
                    graph.setdefault(key, set())
                for index, left in enumerate(eligible):
                    for right in eligible[index + 1 :]:
                        graph[left].add(right)
                        graph[right].add(left)
    return graph


def _sets_connected(
    graph: dict[tuple[str, str], set[tuple[str, str]]],
    sources: set[tuple[str, str]],
    targets: set[tuple[str, str]],
) -> bool:
    return any(
        target != source and target in graph.get(source, set())
        for source in sources
        for target in targets
    )


def _grade_capability_connections(
    builder: GradeBuilder,
    task: Task,
    final_snapshot: JsonDict,
    contributors: dict[str, set[tuple[str, str]]],
) -> None:
    definitions = _declared_backend_widgets(final_snapshot)
    for connection in task.success.capability_connections:
        graph = _shared_param_graph(final_snapshot, definitions, connection.param_kind)
        connected = _sets_connected(
            graph,
            contributors.get(connection.source, set()),
            contributors.get(connection.target, set()),
        )
        builder.check(
            connected,
            "capability_unconnected",
            (
                f"Capabilities {connection.source!r} and {connection.target!r} are not "
                f"connected through a shared {connection.param_kind!r} parameter graph."
            ),
        )


def _grade_business_names(builder: GradeBuilder, task: Task, final_snapshot: JsonDict) -> None:
    composition = final_snapshot.get("dashboard_composition") or {}
    app_names: list[str] = []
    tab_names: list[str] = [
        str(tab.get("name", "")) for tab in composition.get("tabs", []) if isinstance(tab, dict)
    ]
    for backend in (final_snapshot.get("custom_backends") or {}).values():
        if not isinstance(backend, dict):
            continue
        for app in backend.get("apps_json", []) or []:
            if not isinstance(app, dict):
                continue
            app_names.append(str(app.get("name", "")))
            tab_names.extend(
                str(tab.get("name", ""))
                for tab in (app.get("tabs") or {}).values()
                if isinstance(tab, dict)
            )
    values = {
        "dashboard": [str(composition.get("name", ""))],
        "app": app_names,
        "tab": tab_names,
    }
    for requirement in task.success.business_names:
        builder.check(
            any(_phrase_matches(value, requirement.contains) for value in values[requirement.scope]),
            "business_name_missing",
            (
                f"No {requirement.scope} name satisfies business requirement "
                f"{requirement.contains!r}."
            ),
        )


def _grade_app_structure(builder: GradeBuilder, task: Task, final_snapshot: JsonDict) -> None:
    checks = task.success.app_structure
    apps: list[tuple[str, JsonDict, set[str]]] = []
    for backend in (final_snapshot.get("custom_backends") or {}).values():
        if not isinstance(backend, dict):
            continue
        widget_ids = set(backend.get("widgets_json") or {})
        for app in backend.get("apps_json", []) or []:
            if isinstance(app, dict):
                apps.append((str(app.get("name", "app")), app, widget_ids))
    if checks.required:
        builder.check(bool(apps), "missing_capability", "A published app is required.")
    for label, app, widget_ids in apps:
        items = _app_layout_items(app)
        if checks.layout_refs_valid:
            dangling = sorted(
                str(item.get("i"))
                for _, item in items
                if str(item.get("i")) not in widget_ids
                and str(item.get("i")) != "navigation_bar"
            )
            builder.check(
                not dangling,
                "app_layout_ref_invalid",
                f"App {label!r} has dangling widget references: {dangling}.",
            )
        if checks.no_overlaps:
            overlaps: list[tuple[str, str, str]] = []
            by_tab: dict[str, list[JsonDict]] = defaultdict(list)
            for tab_id, item in items:
                by_tab[tab_id].append(item)
            for tab_id, tab_items in by_tab.items():
                for index, first in enumerate(tab_items):
                    for second in tab_items[index + 1 :]:
                        if _layout_items_overlap(first, second):
                            overlaps.append((tab_id, str(first.get("i")), str(second.get("i"))))
            builder.check(
                not overlaps,
                "app_layout_overlap",
                f"App {label!r} has overlapping layout items: {overlaps}.",
            )


def _grade_polish(builder: GradeBuilder, task: Task, final_snapshot: JsonDict) -> None:
    for check in task.success.polish:
        backend = _find_custom_backend(final_snapshot, check.backend_name)
        definition = (
            (backend.get("widgets_json") or {}).get(check.widget_id)
            if backend is not None
            else None
        )
        found, actual = _lookup_path(definition, check.path) if isinstance(definition, dict) else (False, None)
        builder.check(
            found and actual == check.expected,
            check.code,
            (
                f"Polish check {check.backend_name}/{check.widget_id} {check.path} expected "
                f"{check.expected!r}, found {actual!r}."
            ),
        )


def _grade_backend_building(builder: GradeBuilder, task: Task, final_snapshot: JsonDict) -> None:
    backend_names = {required.backend_name for required in task.success.required_widget_defs} | {
        required.backend_name for required in task.success.required_app_defs
    }
    for backend_name in sorted(backend_names):
        backend = _find_custom_backend(final_snapshot, backend_name)
        if backend is not None:
            warnings = backend.get("warnings") or []
            builder.check(
                not warnings,
                "backend_validation_warnings",
                f"Custom backend {backend_name!r} has validation warnings: {warnings}.",
            )
    for required in task.success.required_widget_defs:
        backend = _find_custom_backend(final_snapshot, required.backend_name)
        if backend is None:
            builder.check(
                False,
                "missing_custom_backend",
                (
                    f"Expected custom backend {required.backend_name!r} to be "
                    "registered (manage_backends operation='add' with widgets_json)."
                ),
            )
            continue
        definition = (backend.get("widgets_json") or {}).get(required.widget_id)
        builder.check(
            definition is not None,
            "missing_widget_def",
            (
                f"Expected widget definition {required.widget_id!r} on custom "
                f"backend {required.backend_name!r}."
            ),
        )
        if definition is None:
            continue
        for path, expected in required.expect.items():
            found, actual = _lookup_path(definition, path)
            if found:
                message = (
                    f"Widget def {required.widget_id!r}: expected {path} == "
                    f"{expected!r}, found {actual!r}."
                )
            else:
                message = (
                    f"Widget def {required.widget_id!r}: missing {path} (expected {expected!r})."
                )
            builder.check(found and actual == expected, "widget_def_mismatch", message)
        params = flatten_params(definition, recurse=True)
        for spec in required.params_include:
            builder.check(
                any(_subset_matches(spec, param) for param in params),
                "widget_def_mismatch",
                f"Widget def {required.widget_id!r}: no param matching {spec}.",
            )
        found_cols, columns = _lookup_path(definition, "data.table.columnsDefs")
        column_entries = columns if found_cols and isinstance(columns, list) else []
        for spec in required.columns_include:
            builder.check(
                any(
                    isinstance(column, dict) and _subset_matches(spec, column)
                    for column in column_entries
                ),
                "widget_def_mismatch",
                (f"Widget def {required.widget_id!r}: no columnsDefs entry matching {spec}."),
            )

    for required_app in task.success.required_app_defs:
        backend = _find_custom_backend(final_snapshot, required_app.backend_name)
        if backend is None:
            builder.check(
                False,
                "missing_custom_backend",
                (
                    f"Expected custom backend {required_app.backend_name!r} to be "
                    "registered (manage_backends operation='add' with widgets_json)."
                ),
            )
            continue
        label = required_app.template_id or required_app.name_contains
        app = None
        for candidate in backend.get("apps_json") or []:
            if not isinstance(candidate, dict):
                continue
            if (
                required_app.template_id
                and candidate.get("template_id") == required_app.template_id
            ):
                app = candidate
                break
            if (
                required_app.name_contains
                and required_app.name_contains.lower() in str(candidate.get("name", "")).lower()
            ):
                app = candidate
                break
        builder.check(
            app is not None,
            "missing_app_def",
            (
                f"Expected app {label!r} in the apps.json of custom backend "
                f"{required_app.backend_name!r}."
            ),
        )
        if app is None:
            continue
        for path, expected in required_app.expect.items():
            found, actual = _lookup_path(app, path)
            if found:
                message = f"App {label!r}: expected {path} == {expected!r}, found {actual!r}."
            else:
                message = f"App {label!r}: missing {path} (expected {expected!r})."
            builder.check(found and actual == expected, "app_def_mismatch", message)
        tabs = app.get("tabs") or {}
        for tab_id in required_app.tabs_include:
            builder.check(
                tab_id in tabs,
                "app_def_mismatch",
                f"App {label!r}: expected tab {tab_id!r}, found {sorted(tabs)}.",
            )
        if required_app.tab_count is not None:
            builder.check(
                len(tabs) == required_app.tab_count,
                "app_def_mismatch",
                f"App {label!r}: expected {required_app.tab_count} tab(s), found {len(tabs)}.",
            )
        if required_app.prompts_min_count is not None:
            prompts = app.get("prompts") or []
            count = len(prompts) if isinstance(prompts, list) else 0
            builder.check(
                count >= required_app.prompts_min_count,
                "app_def_mismatch",
                (
                    f"App {label!r}: expected at least {required_app.prompts_min_count} "
                    f"prompt(s), found {count}."
                ),
            )
        items = _app_layout_items(app)
        if required_app.layout_refs_valid:
            widget_ids = set(backend.get("widgets_json") or {})
            dangling = sorted(
                {
                    str(item.get("i"))
                    for _, item in items
                    if str(item.get("i")) not in widget_ids
                    and str(item.get("i")) != "navigation_bar"
                }
            )
            builder.check(
                not dangling,
                "app_layout_ref_invalid",
                (
                    f"App {label!r}: layout references widgets the backend does "
                    f"not serve: {dangling}."
                ),
            )
        if required_app.no_overlaps:
            by_tab: dict[str, list[JsonDict]] = {}
            for tab_key, item in items:
                by_tab.setdefault(tab_key, []).append(item)
            overlaps = []
            for tab_key, tab_items in by_tab.items():
                for index, first in enumerate(tab_items):
                    for second in tab_items[index + 1 :]:
                        if _layout_items_overlap(first, second):
                            overlaps.append((tab_key, str(first.get("i")), str(second.get("i"))))
            builder.check(
                not overlaps,
                "app_layout_overlap",
                f"App {label!r}: overlapping layout items: {overlaps}.",
            )
        for placement in required_app.widgets_on_tab:
            tab_id = str(placement.get("tab_id"))
            widget_id = str(placement.get("widget_id"))
            present = any(
                tab_key == tab_id and str(item.get("i")) == widget_id for tab_key, item in items
            )
            builder.check(
                present,
                "app_def_mismatch",
                f"App {label!r}: expected widget {widget_id!r} on tab {tab_id!r}.",
            )
        groups = app.get("groups") or []
        for spec in required_app.groups_include:
            widget_ids_include = spec.get("widgetIds_include", [])
            base_spec = {key: value for key, value in spec.items() if key != "widgetIds_include"}
            matched = False
            for group in groups:
                if not isinstance(group, dict):
                    continue
                if not _subset_matches(base_spec, group):
                    continue
                group_widgets = group.get("widgetIds") or []
                if all(wid in group_widgets for wid in widget_ids_include):
                    matched = True
                    break
            builder.check(
                matched,
                "app_def_mismatch",
                f"App {label!r}: no group matching {spec}.",
            )


def _grade_trace(builder: GradeBuilder, task: Task, trace: tuple[ToolTraceEvent, ...]) -> None:
    checks = task.success.trace
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
        listed_origins: set[str] = set()
        listing_required = "list_available_widgets" in task.allowed_tools
        for event in trace:
            if event.call.name == "list_available_widgets" and event.ok:
                listed_origin = str(event.call.args.get("origin", ""))
                if listed_origin:
                    listed_origins.add(listed_origin)
                for widget in (event.result.get("data") or {}).get("widgets", []):
                    listed_widgets.add((widget.get("origin"), widget.get("widget_id")))
            if event.call.name in {"get_widget_schema", "create_widget"}:
                used_origin = str(
                    event.call.args.get("origin") or event.call.args.get("backend_name") or ""
                )
                used_widget_id = event.call.args.get("widget_id")
                if listing_required:
                    builder.check(
                        used_origin in listed_origins,
                        "widget_list_not_called_before_use",
                        (
                            f"{event.call.name} used {used_origin}/{used_widget_id} "
                            "before list_available_widgets for that origin."
                        ),
                    )
                if used_origin in listed_origins:
                    builder.check(
                        (used_origin, used_widget_id) in listed_widgets,
                        "unlisted_widget_id",
                        (f"{event.call.name} used unlisted widget {used_origin}/{used_widget_id}."),
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
        else:
            current = 0
    return max_seen
