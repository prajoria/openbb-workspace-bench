"""Independent grader-sensitivity checks used by release validation."""

from __future__ import annotations

import copy
import re
from dataclasses import replace

from workspace_bench.core.graders import grade_task
from workspace_bench.core.models import JsonDict, RunResult, Task, ToolTraceEvent
from workspace_bench.workspace.default_setup import apply_workspace_baseline
from workspace_bench.workspace.simulated_workspace import SimulatedWorkspace


def grader_mutation_failures(task: Task, oracle: RunResult) -> list[str]:
    """Return rubric dimensions for which an adversarial mutation still passes."""

    fixtures, initial_state = apply_workspace_baseline(
        task.suite,
        task.fixtures,
        task.initial_state,
        baseline_override=task.workspace_baseline,
        backends_override=task.workspace_backends,
    )
    initial_workspace = SimulatedWorkspace()
    initial_workspace.reset(
        backends=fixtures,
        initial_state=initial_state,
        runtime_checks=task.success.runtime,
    )
    initial_snapshot = initial_workspace.snapshot()
    failures: list[str] = []

    def assert_rejected(
        label: str,
        *,
        snapshot: JsonDict | None = None,
        trace: tuple[ToolTraceEvent, ...] | None = None,
        required_code: str | None = None,
        include_runtime: bool = False,
    ) -> None:
        graded_task = task
        if task.success.runtime is not None and not include_runtime:
            graded_task = replace(task, success=replace(task.success, runtime=None))
        grade = grade_task(
            graded_task,
            snapshot if snapshot is not None else oracle.final_snapshot,
            trace if trace is not None else oracle.trace,
            initial_snapshot=initial_snapshot,
        )
        if grade.passed or (
            required_code is not None
            and required_code not in {issue.code for issue in grade.issues}
        ):
            failures.append(label)

    success = task.success
    composition = oracle.final_snapshot.get("dashboard_composition") or {}

    if success.required_dashboard_name_contains:
        snapshot = copy.deepcopy(oracle.final_snapshot)
        snapshot["dashboard_composition"]["name"] = "mutation"
        assert_rejected("dashboard_name", snapshot=snapshot)

    if success.required_tabs:
        snapshot = copy.deepcopy(oracle.final_snapshot)
        required_tabs = set(success.required_tabs)
        snapshot["dashboard_composition"]["tabs"] = [
            tab
            for tab in snapshot["dashboard_composition"].get("tabs", [])
            if tab.get("id") not in required_tabs
        ]
        assert_rejected("required_tabs", snapshot=snapshot)

    if success.required_widgets:
        snapshot = copy.deepcopy(oracle.final_snapshot)
        positive_pairs = {
            (required.origin, required.widget_id)
            for required in success.required_widgets
            if required.min_count > 0
        }
        snapshot["dashboard_composition"]["widgets"] = [
            widget
            for widget in snapshot["dashboard_composition"].get("widgets", [])
            if (widget.get("origin"), widget.get("widget_id")) not in positive_pairs
        ]
        initial_widgets = (initial_snapshot.get("dashboard_composition") or {}).get("widgets", [])
        for required in success.required_widgets:
            if required.max_count != 0:
                continue
            restored = next(
                (
                    copy.deepcopy(widget)
                    for widget in initial_widgets
                    if widget.get("origin") == required.origin
                    and widget.get("widget_id") == required.widget_id
                ),
                {
                    "origin": required.origin,
                    "widget_id": required.widget_id,
                    "generated": False,
                    "data_args": copy.deepcopy(required.data_args),
                    "layout": {"x": 0, "y": 0, "w": 10, "h": 5, "tab_id": ""},
                },
            )
            snapshot["dashboard_composition"]["widgets"].append(restored)
        assert_rejected("required_widgets", snapshot=snapshot)

    if success.required_generated_widgets:
        snapshot = copy.deepcopy(oracle.final_snapshot)
        snapshot["dashboard_composition"]["widgets"] = [
            widget
            for widget in snapshot["dashboard_composition"].get("widgets", [])
            if not widget.get("generated")
        ]
        assert_rejected("required_generated_widgets", snapshot=snapshot)

        semantic_requirement = next(
            (
                required
                for required in success.required_generated_widgets
                if required.data_contains
            ),
            None,
        )
        if semantic_requirement is not None:
            fragment = semantic_requirement.data_contains[0]
            snapshot = copy.deepcopy(oracle.final_snapshot)
            snapshot["dashboard_composition"]["widgets"] = [
                _replace_generated_fragment(widget, fragment)
                if widget.get("generated")
                else widget
                for widget in snapshot["dashboard_composition"].get("widgets", [])
            ]
            assert_rejected(
                "generated_widget_data_contains",
                snapshot=snapshot,
                required_code="missing_generated_widget",
            )

    if success.required_layouts or success.layout.within_grid:
        widgets = composition.get("widgets") or []
        if widgets:
            snapshot = copy.deepcopy(oracle.final_snapshot)
            snapshot["dashboard_composition"]["widgets"][0]["layout"]["x"] = 10_000
            assert_rejected("layout", snapshot=snapshot)

    if success.required_widget_defs or success.required_app_defs or success.required_capabilities:
        snapshot = copy.deepcopy(oracle.final_snapshot)
        snapshot["custom_backends"] = {}
        assert_rejected("backend_definitions", snapshot=snapshot)

    if success.required_capabilities:
        first_capability = next(
            (
                capability
                for capability in success.required_capabilities
                if capability.must_cover_fields
            ),
            success.required_capabilities[0],
        )
        snapshot = copy.deepcopy(oracle.final_snapshot)
        dataset_names = set(first_capability.datasets)
        dataset_widget_ids = {
            dataset.widget_id
            for dataset in (success.runtime.datasets if success.runtime else ())
            if dataset.name in dataset_names
        }
        removed: set[tuple[str, str]] = set()
        for backend in snapshot.get("custom_backends", {}).values():
            backend_name = str(backend.get("name", ""))
            widget_defs = backend.get("widgets_json") or {}
            if not first_capability.must_cover_fields:
                removed.update((backend_name, str(widget_id)) for widget_id in widget_defs)
                widget_defs.clear()
                continue
            for widget_id in list(widget_defs):
                if widget_id in dataset_widget_ids:
                    widget_defs.pop(widget_id)
                    removed.add((backend_name, str(widget_id)))
        for dashboard in snapshot.get("dashboard_compositions", {}).values():
            dashboard["widgets"] = [
                widget
                for widget in dashboard.get("widgets", [])
                if (str(widget.get("origin", "")), str(widget.get("widget_id", "")))
                not in removed
            ]
        assert_rejected(
            "capability_fields_uncovered",
            snapshot=snapshot,
            required_code=(
                "capability_fields_uncovered"
                if first_capability.must_cover_fields
                else "missing_capability"
            ),
            include_runtime=True,
        )

    if success.capability_connections:
        snapshot = copy.deepcopy(oracle.final_snapshot)
        for backend in snapshot.get("custom_backends", {}).values():
            for app in backend.get("apps_json", []) or []:
                app["groups"] = []
        assert_rejected(
            "capability_shared_param_graph",
            snapshot=snapshot,
            required_code="capability_unconnected",
            include_runtime=True,
        )

    if success.runtime is not None:
        custom_backends = oracle.final_snapshot.get("custom_backends") or {}
        first_backend = next(
            (backend for backend in custom_backends.values() if backend.get("widgets_json")),
            None,
        )
        if first_backend is not None:
            first_widget_id = next(iter(first_backend["widgets_json"]))
            snapshot = copy.deepcopy(oracle.final_snapshot)
            mutated_backend = next(
                backend
                for backend in snapshot["custom_backends"].values()
                if first_widget_id in (backend.get("widgets_json") or {})
            )
            definition = mutated_backend["widgets_json"][first_widget_id]
            if not isinstance(definition.get("data"), dict):
                definition["data"] = {}
            definition["data"].setdefault("table", {}).setdefault(
                "columnsDefs", []
            ).append({"field": "field_no_runtime_dataset_serves"})
            assert_rejected(
                "runtime_incompatible_field",
                snapshot=snapshot,
                required_code="endpoint_response_incompatible",
                include_runtime=True,
            )

            snapshot = copy.deepcopy(oracle.final_snapshot)
            mutated_backend = next(
                backend
                for backend in snapshot["custom_backends"].values()
                if first_widget_id in (backend.get("widgets_json") or {})
            )
            mutated_backend["widgets_json"][first_widget_id]["endpoint"] = ""
            assert_rejected(
                "runtime_unreachable_endpoint",
                snapshot=snapshot,
                required_code="endpoint_unreachable",
                include_runtime=True,
            )

    # Repairs graded through a required manage_backends call leave no
    # state-level signal, so the state-revert probe only applies to debug
    # tasks whose broken payload is outcome-visible.
    if task.family == "debug" and not any(
        required.name == "manage_backends" for required in success.required_tool_calls
    ):
        snapshot = copy.deepcopy(oracle.final_snapshot)
        snapshot["custom_backends"] = copy.deepcopy(
            initial_snapshot.get("custom_backends") or {}
        )
        assert_rejected(
            "debug_refresh_still_broken",
            snapshot=snapshot,
            include_runtime=True,
        )

    if success.required_tool_calls:
        names = {required.name for required in success.required_tool_calls}
        trace = tuple(event for event in oracle.trace if event.call.name not in names)
        assert_rejected("required_tool_calls", trace=trace)

    if success.required_tool_results:
        names = {required.name for required in success.required_tool_results}
        trace = tuple(event for event in oracle.trace if event.call.name not in names)
        assert_rejected("required_tool_results", trace=trace)

    if success.required_resource_reads:
        trace = tuple(
            event for event in oracle.trace if event.call.name != "read_workspace_resource"
        )
        assert_rejected("required_resource_reads", trace=trace)

    return failures


def _replace_generated_fragment(value: object, fragment: str) -> object:
    """Replace one required semantic fact throughout generated-widget metadata."""

    if isinstance(value, str):
        tokens = re.findall(r"[a-z0-9]+", fragment, flags=re.IGNORECASE)
        pattern = r"[\W_]+".join(re.escape(token) for token in tokens)
        if not pattern:
            pattern = re.escape(fragment)
        return re.sub(pattern, "mutation", value, flags=re.IGNORECASE)
    if isinstance(value, list):
        return [_replace_generated_fragment(item, fragment) for item in value]
    if isinstance(value, dict):
        return {
            key: _replace_generated_fragment(item, fragment)
            for key, item in value.items()
        }
    return value
