"""Executable regressions for known false-positive grading loopholes."""

from __future__ import annotations

import copy

from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import Task, ToolCall
from workspace_bench.core.runner import find_task
from workspace_bench.workspace.runtime import declared_fields


def _run(task: Task, calls: list[ToolCall]):
    episode = WorkspaceEpisode(task)
    for call in calls:
        result = episode.step(call)
        assert result.get("ok"), (task.qualified_id, call, result)
    return episode.grade()


def _oracle_calls_with_widgets(
    task: Task,
    transform,
) -> list[ToolCall]:
    calls: list[ToolCall] = []
    for call in task.oracle_tool_calls:
        args = copy.deepcopy(call.args)
        if call.name == "manage_backends" and args.get("widgets_json"):
            transform(args["widgets_json"])
        calls.append(ToolCall(call.name, args))
    return calls


def test_click_season_mega_widget_self_connection_exploit_is_rejected() -> None:
    task = find_task("build-openbb-apps/grouping/click_season_desk")
    backend_call = next(
        call
        for call in task.oracle_tool_calls
        if call.name == "manage_backends" and call.args.get("widgets_json")
    )
    source = backend_call.args["widgets_json"]
    mega = copy.deepcopy(source["click_season_table"])
    mega["name"] = "All-in-one season and revisions"
    mega["endpoint"] = "/capability-union"
    mega["data"]["table"]["columnsDefs"].extend(
        copy.deepcopy(
            source["estimate_revisions"]["data"]["table"]["columnsDefs"]
        )
    )
    chart = copy.deepcopy(source["earnings_chart"])
    widgets = {"mega_table": mega, "eps_chart": chart}
    apps = [
        {
            "name": "Collapsed Season Desk",
            "description": "A deliberately degenerate two-widget architecture.",
            "tabs": {
                "desk": {
                    "id": "desk",
                    "name": "Desk",
                    "layout": [
                        {"i": "mega_table", "x": 0, "y": 0, "w": 20, "h": 9},
                        {"i": "eps_chart", "x": 20, "y": 0, "w": 20, "h": 9},
                    ],
                }
            },
            "groups": [
                {
                    "name": "Fake all-capability sync",
                    "type": "param",
                    "paramName": "symbol",
                    "widgetIds": ["mega_table", "eps_chart"],
                }
            ],
        }
    ]
    calls = [
        ToolCall("get_workspace_snapshot", {}),
        ToolCall(
            "manage_backends",
            {
                "operation": "add",
                "name": "Collapsed Earnings Data",
                "url": "http://localhost:7805",
                "widgets_json": widgets,
                "apps_json": apps,
            },
        ),
        ToolCall(
            "manage_apps",
            {
                "operation": "instantiate",
                "backend_id": "backend_001",
                "app_name": "Collapsed Season Desk",
                "dashboard_name": "Collapsed Season Desk Live",
                "activate": True,
            },
        ),
    ]

    grade = _run(task, calls)

    assert not grade.passed
    assert "capability_unconnected" in {issue.code for issue in grade.issues}


def test_fieldless_widget_cannot_contribute_to_an_empty_cover_capability() -> None:
    task = find_task("build-openbb-apps/settings/alert_metric_room")

    def strip_fields(widgets: dict[str, dict]) -> None:
        definition = widgets["alert_metric"]
        definition.pop("data", None)
        assert not declared_fields(definition)

    grade = _run(task, _oracle_calls_with_widgets(task, strip_fields))

    assert not grade.passed
    assert "capability_fields_uncovered" in {issue.code for issue in grade.issues}


def test_metric_with_dummy_form_controls_cannot_satisfy_form_capability() -> None:
    task = find_task("build-openbb-apps/forms/sla_ship")

    def replace_form(widgets: dict[str, dict]) -> None:
        widgets["vendor_intake_form"] = {
            "name": "Fake Intake Metric",
            "description": "A metric with controls but no intake response fields.",
            "endpoint": "/fake-intake",
            "type": "metric",
            "params": [
                {
                    "paramName": "intake",
                    "type": "form",
                    "label": "Fake intake",
                    "endpoint": "/wrong-submit",
                    "method": "POST",
                    "inputParams": [
                        {"paramName": "vendor", "type": "text", "label": "Vendor"},
                        {"paramName": "tier", "type": "number", "label": "Tier"},
                        {"paramName": "submit", "type": "button", "label": "Submit"},
                    ],
                }
            ],
        }
        assert not declared_fields(widgets["vendor_intake_form"])

    grade = _run(task, _oracle_calls_with_widgets(task, replace_form))

    assert not grade.passed
    assert "missing_capability" in {issue.code for issue in grade.issues}
