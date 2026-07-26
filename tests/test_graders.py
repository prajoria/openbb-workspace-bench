from __future__ import annotations

from dataclasses import replace

from workspace_bench.core.graders import grade_task
from workspace_bench.core.models import (
    LayoutChecks,
    RequiredGeneratedWidget,
    RequiredResourceRead,
    SuccessCriteria,
    ToolCall,
    ToolTraceEvent,
)
from workspace_bench.core.runner import TaskRunner, find_task


def test_grader_detects_missing_required_widget() -> None:
    task = find_task("morning_briefing_level0")
    snapshot = {
        "dashboard_composition": {
            "name": "Empty",
            "tabs": [{"id": "", "name": "", "layout": []}],
            "widgets": [],
        }
    }

    grade = grade_task(task, snapshot, ())

    assert grade.passed is False
    assert any(issue.code == "missing_widget" for issue in grade.issues)


def test_grader_detects_layout_overlap() -> None:
    task = find_task("morning_briefing_level0")
    task = replace(
        task,
        success=replace(
            task.success,
            required_widgets=(),
            required_layouts=(),
            layout=LayoutChecks(no_overlaps=True, within_grid=True, grid_width=40),
        ),
    )
    snapshot = {
        "dashboard_composition": {
            "name": "Overlap",
            "tabs": [{"id": "", "name": "", "layout": []}],
            "widgets": [
                {
                    "widget_uuid": "widget_001",
                    "widget_id": "a",
                    "origin": "generated",
                    "generated": True,
                    "layout": {"tab_id": "", "x": 0, "y": 0, "w": 20, "h": 10},
                },
                {
                    "widget_uuid": "widget_002",
                    "widget_id": "b",
                    "origin": "generated",
                    "generated": True,
                    "layout": {"tab_id": "", "x": 10, "y": 0, "w": 20, "h": 10},
                },
            ],
        }
    }

    grade = grade_task(task, snapshot, ())

    assert grade.passed is False
    assert any(issue.code == "layout_overlap" for issue in grade.issues)


def test_grader_matches_generated_percent_equivalent() -> None:
    task = find_task("morning_briefing_level0")
    task = replace(
        task,
        success=SuccessCriteria(
            required_generated_widgets=(
                RequiredGeneratedWidget(
                    widget_type="note",
                    data_contains=("largest weight", "0.34"),
                ),
            )
        ),
    )
    snapshot = {
        "dashboard_composition": {
            "name": "Existing Review",
            "tabs": [{"id": "overview", "name": "Overview", "layout": []}],
            "widgets": [
                {
                    "widget_uuid": "widget_001",
                    "widget_id": "generated_note",
                    "origin": "generated",
                    "generated": True,
                    "type": "note",
                    "generated_data": "The largest weight is 34%.",
                    "layout": {"tab_id": "overview", "x": 0, "y": 14, "w": 20, "h": 8},
                },
            ],
        }
    }

    grade = grade_task(task, snapshot, ())

    assert grade.passed is True


def test_grader_requires_tool_results_for_skill_task() -> None:
    task = find_task("workspace-tasks/research_analyst/guidance_tracker_level3")
    result = TaskRunner().run(task, "oracle")

    assert result.grade.passed is True
    assert any(event.call.name == "get_skill_content" for event in result.trace)


def test_grader_matches_generated_widget_display_alias() -> None:
    task = find_task("morning_briefing_level0")
    task = replace(
        task,
        success=SuccessCriteria(
            required_generated_widgets=(
                RequiredGeneratedWidget(
                    widget_type="note",
                    data_contains=("price_performance",),
                ),
            )
        ),
    )
    snapshot = {
        "dashboard_composition": {
            "name": "Workspace Bench",
            "tabs": [{"id": "", "name": "", "layout": []}],
            "widgets": [
                {
                    "widget_uuid": "widget_001",
                    "widget_id": "generated_note",
                    "origin": "generated",
                    "generated": True,
                    "type": "note",
                    "generated_data": (
                        "Equity Earnings Review has overview and estimates tabs, "
                        "Price Performance, and suggested prompts."
                    ),
                    "layout": {"tab_id": "", "x": 0, "y": 0, "w": 20, "h": 8},
                }
            ],
        }
    }

    grade = grade_task(task, snapshot, ())

    assert grade.passed is True


def test_grader_dashboard_name_allows_stopwords_between_terms() -> None:
    task = find_task("morning_briefing_level0")
    task = replace(
        task,
        success=SuccessCriteria(
            required_dashboard_name_contains="Portfolio Macro Risk",
        ),
    )
    snapshot = {
        "dashboard_composition": {
            "name": "Portfolio and Macro Risk Dashboard",
            "tabs": [{"id": "", "name": "", "layout": []}],
            "widgets": [],
        }
    }

    grade = grade_task(task, snapshot, ())

    assert grade.passed is True


def test_grader_detects_missing_required_resource_read() -> None:
    task = find_task("morning_briefing_level0")
    task = replace(
        task,
        success=SuccessCriteria(
            required_resource_reads=(
                RequiredResourceRead(
                    uri="openbb://workspace/app-builder/index",
                    data_contains=("Workspace app builder index",),
                ),
            )
        ),
    )
    snapshot = {
        "dashboard_composition": {
            "name": "Workspace Bench",
            "tabs": [{"id": "", "name": "", "layout": []}],
            "widgets": [],
        }
    }

    grade = grade_task(task, snapshot, ())

    assert grade.passed is False
    assert any(issue.code == "missing_resource_read" for issue in grade.issues)


def test_grader_matches_required_resource_read() -> None:
    task = find_task("morning_briefing_level0")
    task = replace(
        task,
        success=SuccessCriteria(
            required_resource_reads=(
                RequiredResourceRead(
                    uri="openbb://workspace/app-builder/index",
                    data_contains=("Equity Earnings Review",),
                ),
            )
        ),
    )
    snapshot = {
        "dashboard_composition": {
            "name": "Workspace Bench",
            "tabs": [{"id": "", "name": "", "layout": []}],
            "widgets": [],
        }
    }
    trace = (
        ToolTraceEvent(
            index=1,
            call=ToolCall(
                "read_workspace_resource",
                {"uri": "openbb://workspace/app-builder/index"},
            ),
            ok=True,
            result={
                "ok": True,
                "data": {"text": "Workspace app builder index: Equity Earnings Review"},
            },
        ),
    )

    grade = grade_task(task, snapshot, trace)

    assert grade.passed is True


def test_missing_widget_split_absent_vs_misconfigured() -> None:
    from workspace_bench.core.graders import _matching_required_widgets, _same_identity_widgets
    from workspace_bench.core.models import RequiredWidget

    required = RequiredWidget(
        origin="Getting Started", widget_id="live_grid_data",
        data_args={"symbol": "TSLA"}, min_count=1,
    )
    absent_world = [
        {"origin": "Getting Started", "widget_id": "sparkline_line", "data_args": {}},
    ]
    misconfigured_world = [
        {"origin": "Getting Started", "widget_id": "live_grid_data", "data_args": {"symbol": "AAPL"}},
    ]
    correct_world = [
        {"origin": "Getting Started", "widget_id": "live_grid_data", "data_args": {"symbol": "TSLA"}},
    ]
    assert _matching_required_widgets(required, absent_world) == []
    assert _same_identity_widgets(required, absent_world) == []
    assert _matching_required_widgets(required, misconfigured_world) == []
    assert len(_same_identity_widgets(required, misconfigured_world)) == 1
    assert len(_matching_required_widgets(required, correct_world)) == 1
