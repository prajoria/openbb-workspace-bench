"""Real-episode proofs that behavioral rubrics accept non-oracle architectures."""

from __future__ import annotations

import copy
from dataclasses import dataclass

import pytest

from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.graders import grade_task
from workspace_bench.core.models import Task, ToolCall
from workspace_bench.core.prompt_openness import task_prompt_openness_issues
from workspace_bench.core.runner import load_builtin_tasks


@dataclass(frozen=True)
class AlternativeCase:
    family: str
    task_id: str
    mode: str


CASES = (
    AlternativeCase("aggrid", "case_aging", "merge"),
    AlternativeCase("forms", "vendor_intake_room", "rename"),
    AlternativeCase("grouping", "click_season_desk", "rename"),
    AlternativeCase("apps", "earnings_desk", "split"),
    AlternativeCase("charts", "earnings_chart_room", "split"),
    AlternativeCase("settings", "healthcare_ship", "rename"),
    AlternativeCase("advanced", "live_orders_grid_ship", "rename"),
    AlternativeCase("params", "earnings_param_review", "rename"),
    AlternativeCase("e2e", "case_triage", "split"),
    AlternativeCase("e2e", "vol_cockpit", "split"),
)


def _task(case: AlternativeCase) -> Task:
    return next(
        task
        for task in load_builtin_tasks("build-openbb-apps")
        if task.family == case.family and task.id == case.task_id
    )


def _table_fields(definition: dict) -> list[dict]:
    return list((((definition.get("data") or {}).get("table") or {}).get("columnsDefs") or []))


def _merge_definitions(definitions: list[dict], new_id: str) -> dict:
    merged = copy.deepcopy(definitions[0])
    merged["name"] = f"Combined capability {new_id}"
    merged["endpoint"] = f"/alternative/{new_id}"
    columns: list[dict] = []
    seen_fields: set[str] = set()
    params: list = []
    seen_params: set[str] = set()
    for definition in definitions:
        for column in _table_fields(definition):
            field = str(column.get("field", ""))
            if field and field not in seen_fields:
                columns.append(copy.deepcopy(column))
                seen_fields.add(field)
        for entry in definition.get("params", []) or []:
            entries = entry if isinstance(entry, list) else [entry]
            for param in entries:
                name = str(param.get("paramName", "")) if isinstance(param, dict) else ""
                if name and name not in seen_params:
                    params.append(copy.deepcopy(param))
                    seen_params.add(name)
    merged.setdefault("data", {}).setdefault("table", {})["columnsDefs"] = columns
    if params:
        merged["params"] = params
    return merged


def _split_definition(definition: dict, new_ids: tuple[str, str]) -> dict[str, dict]:
    columns = _table_fields(definition)
    assert len(columns) >= 2
    midpoint = max(1, len(columns) // 2)
    result: dict[str, dict] = {}
    for new_id, selected in zip(new_ids, (columns[:midpoint], columns[midpoint:])):
        split = copy.deepcopy(definition)
        split["name"] = f"Specialized capability {new_id}"
        split["endpoint"] = f"/alternative/{new_id}"
        split.setdefault("data", {}).setdefault("table", {})["columnsDefs"] = selected
        result[new_id] = split
    return result


def _transform_payload(
    task: Task, mode: str
) -> tuple[dict[str, dict], list[dict], dict[str, list[str]]]:
    backend_call = next(
        call
        for call in task.oracle_tool_calls
        if call.name == "manage_backends" and call.args.get("widgets_json")
    )
    source_widgets = copy.deepcopy(backend_call.args["widgets_json"])
    source_apps = copy.deepcopy(backend_call.args.get("apps_json") or [])
    behavioral_widget_ids = {
        dataset.widget_id
        for capability in task.success.required_capabilities
        for dataset in (task.success.runtime.datasets if task.success.runtime else ())
        if dataset.name == capability.datasets[0]
    }
    source_widgets = {
        widget_id: definition
        for widget_id, definition in source_widgets.items()
        if widget_id in behavioral_widget_ids
    }
    field_widget_ids = [
        dataset.widget_id
        for capability in task.success.required_capabilities
        if capability.must_cover_fields
        for dataset in (task.success.runtime.datasets if task.success.runtime else ())
        if dataset.name == capability.datasets[0]
    ]
    assert field_widget_ids

    mapping: dict[str, list[str]] = {
        widget_id: [f"alternative_{index}_{widget_id}"]
        for index, widget_id in enumerate(source_widgets, start=1)
    }
    transformed: dict[str, dict] = {}
    if mode == "merge":
        merge_ids = [
            widget_id
            for widget_id in field_widget_ids
            if str(source_widgets[widget_id].get("type", "table")) == "table"
        ][:2]
        if len(merge_ids) < 2:
            merge_ids = [
                widget_id
                for widget_id, definition in source_widgets.items()
                if str(definition.get("type", "table")) == "table"
            ][:2]
        assert len(merge_ids) == 2
        merged_id = "alternative_combined_table"
        for widget_id in merge_ids:
            mapping[widget_id] = [merged_id]
        transformed[merged_id] = _merge_definitions(
            [source_widgets[widget_id] for widget_id in merge_ids], merged_id
        )
        for widget_id, definition in source_widgets.items():
            if widget_id in merge_ids:
                continue
            new_id = mapping[widget_id][0]
            transformed[new_id] = copy.deepcopy(definition)
            transformed[new_id]["endpoint"] = f"/alternative/{new_id}"
    elif mode == "split":
        split_id = next(
            widget_id
            for widget_id in field_widget_ids
            if len(_table_fields(source_widgets[widget_id])) >= 2
        )
        new_ids = (f"alternative_{split_id}_left", f"alternative_{split_id}_right")
        mapping[split_id] = list(new_ids)
        transformed.update(_split_definition(source_widgets[split_id], new_ids))
        for widget_id, definition in source_widgets.items():
            if widget_id == split_id:
                continue
            new_id = mapping[widget_id][0]
            transformed[new_id] = copy.deepcopy(definition)
            transformed[new_id]["endpoint"] = f"/alternative/{new_id}"
    else:
        for widget_id, definition in source_widgets.items():
            new_id = mapping[widget_id][0]
            transformed[new_id] = copy.deepcopy(definition)
            transformed[new_id]["endpoint"] = f"/alternative/{new_id}"

    transformed_apps: list[dict] = []
    for app_index, source_app in enumerate(source_apps, start=1):
        app = copy.deepcopy(source_app)
        app.pop("template_id", None)
        app["name"] = f"Alternative Workspace {task.id} {app_index}"
        new_tabs: dict[str, dict] = {}
        for tab_index, tab in enumerate((app.get("tabs") or {}).values(), start=1):
            tab_id = f"alternative_tab_{app_index}_{tab_index}"
            items: list[dict] = []
            for source_item in tab.get("layout", []) or []:
                source_id = str(source_item.get("i"))
                target_ids = mapping.get(source_id, [source_id])
                for target_id in target_ids:
                    if any(item["i"] == target_id for item in items):
                        continue
                    item_index = len(items)
                    items.append(
                        {
                            "i": target_id,
                            "x": 0,
                            "y": item_index * 7,
                            "w": 18 + (item_index % 2),
                            "h": 6,
                        }
                    )
            new_tabs[tab_id] = {
                "id": tab_id,
                "name": f"Alternative View {tab_index}",
                "layout": items,
            }
        app["tabs"] = new_tabs
        groups: list[dict] = []
        for group_index, group in enumerate(app.get("groups", []) or [], start=1):
            widget_ids = list(
                dict.fromkeys(
                    target_id
                    for source_id in group.get("widgetIds", []) or []
                    for target_id in mapping.get(str(source_id), [str(source_id)])
                )
            )
            rewritten = copy.deepcopy(group)
            rewritten["name"] = f"Alternative shared link {group_index}"
            rewritten["widgetIds"] = widget_ids
            groups.append(rewritten)
        app["groups"] = groups
        transformed_apps.append(app)
    return transformed, transformed_apps, mapping


def _alternative_calls(task: Task, mode: str, *, near_miss: bool) -> tuple[ToolCall, ...]:
    widgets, apps, mapping = _transform_payload(task, mode)
    if near_miss:
        table_fields = {
            str(column.get("field"))
            for definition in widgets.values()
            for column in _table_fields(definition)
        }
        capability = next(
            capability
            for capability in task.success.required_capabilities
            if set(capability.must_cover_fields) & table_fields
        )
        missing_field = capability.must_cover_fields[0]
        for definition in widgets.values():
            table = (definition.get("data") or {}).get("table") or {}
            if isinstance(table.get("columnsDefs"), list):
                table["columnsDefs"] = [
                    column
                    for column in table["columnsDefs"]
                    if column.get("field") != missing_field
                ]

    app_name = str(apps[0]["name"])
    calls: list[ToolCall] = []
    for original in task.oracle_tool_calls:
        args = copy.deepcopy(original.args)
        if original.name == "manage_backends" and args.get("widgets_json"):
            args["widgets_json"] = widgets
            args["apps_json"] = apps
        elif original.name == "manage_apps" and args.get("operation") == "instantiate":
            args["app_name"] = app_name
            if not task.success.business_names:
                args["dashboard_name"] = f"Alternative Dashboard {task.id}"
        elif original.name in {"get_widget_schema", "create_widget", "update_widget"}:
            source_id = str(args.get("widget_id", ""))
            if source_id in mapping:
                args["widget_id"] = mapping[source_id][0]
        calls.append(ToolCall(name=original.name, args=args))
    return tuple(calls)


def _run(task: Task, calls: tuple[ToolCall, ...]):
    episode = WorkspaceEpisode(task)
    for call in calls:
        result = episode.step(call)
        assert result.get("ok"), (task.qualified_id, call, result)
    return episode.grade()


@pytest.mark.parametrize("case", CASES, ids=lambda case: f"{case.family}-{case.task_id}")
def test_genuinely_different_full_solutions_pass_and_near_misses_fail(
    case: AlternativeCase,
) -> None:
    task = _task(case)
    alternative = _run(task, _alternative_calls(task, case.mode, near_miss=False))
    assert alternative.passed
    assert alternative.state_passed
    assert alternative.trace_passed
    assert alternative.runtime_passed
    if task.success.polish:
        assert alternative.polish_score < 1.0
        assert alternative.polish_issues

    near_miss = _run(task, _alternative_calls(task, case.mode, near_miss=True))
    assert not near_miss.passed
    assert near_miss.runtime_passed
    assert {issue.code for issue in near_miss.issues} == {"capability_fields_uncovered"}


def test_matrix_proves_merge_and_split_widget_count_freedom() -> None:
    merge_task = _task(CASES[0])
    merge_widgets, _, _ = _transform_payload(merge_task, "merge")
    oracle_widgets = next(
        call.args["widgets_json"]
        for call in merge_task.oracle_tool_calls
        if call.name == "manage_backends" and call.args.get("widgets_json")
    )
    assert len(oracle_widgets) == 3
    assert len(merge_widgets) == 2

    split_task = _task(CASES[8])
    split_widgets, _, _ = _transform_payload(split_task, "split")
    oracle_widgets = next(
        call.args["widgets_json"]
        for call in split_task.oracle_tool_calls
        if call.name == "manage_backends" and call.args.get("widgets_json")
    )
    assert len(oracle_widgets) == 2
    assert len(split_widgets) == 3


def test_matrix_covers_at_least_five_rewritten_hard_briefs() -> None:
    tasks = [
        _task(case)
        for case in CASES
        if _task(case).specification_level == "open-brief"
    ]
    assert len(tasks) >= 5
    assert all(not task_prompt_openness_issues(task) for task in tasks)


@pytest.mark.parametrize(
    ("task_id", "payload_key"),
    [
        ("execution_data_mismatch", "widgets_json"),
        ("execution_dangling_app", "apps_json"),
    ],
)
def test_debug_repairs_accept_targeted_alternative_refreshes(
    task_id: str,
    payload_key: str,
) -> None:
    task = next(
        task
        for task in load_builtin_tasks("build-openbb-apps")
        if task.family == "debug" and task.id == task_id
    )
    episode = WorkspaceEpisode(task)
    for call in task.oracle_tool_calls:
        args = copy.deepcopy(call.args)
        if call.name == "manage_backends" and args.get("operation") == "refresh":
            args = {
                "operation": "refresh",
                "backend_id": args["backend_id"],
                payload_key: args[payload_key],
            }
        episode.step(ToolCall(call.name, args))

    grade = episode.grade()
    assert grade.passed
    assert grade.runtime_passed
    assert grade.state_passed


def test_explicit_business_name_is_gating_but_free_tab_names_are_not() -> None:
    task = _task(CASES[8])
    episode = WorkspaceEpisode(task)
    for call in _alternative_calls(task, "split", near_miss=False):
        assert episode.step(call).get("ok")
    snapshot = episode.snapshot()
    snapshot["dashboard_composition"]["name"] = "Unrelated dashboard"
    active_id = snapshot["workspace_state"]["current_dashboard_uuid"]
    snapshot["dashboard_compositions"][active_id]["name"] = "Unrelated dashboard"
    grade = grade_task(
        task,
        snapshot,
        tuple(episode.trace),
        initial_snapshot=episode.initial_snapshot,
    )
    assert not grade.passed
    assert "business_name_missing" in {issue.code for issue in grade.issues}
