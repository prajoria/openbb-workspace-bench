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
    task = find_task("price_performance_aapl")
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
    task = find_task("price_performance_aapl")
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
    task = find_task("fact_top_holding")
    snapshot = {
        "dashboard_composition": {
            "name": "Existing Portfolio Review",
            "tabs": [{"id": "overview", "name": "Overview", "layout": []}],
            "widgets": [
                {
                    "widget_uuid": "widget_001",
                    "widget_id": "holdings_table",
                    "origin": "Bench Portfolio",
                    "generated": False,
                    "data_args": {},
                    "layout": {"tab_id": "overview", "x": 0, "y": 2, "w": 24, "h": 12},
                },
                {
                    "widget_uuid": "widget_002",
                    "widget_id": "sector_exposure",
                    "origin": "Bench Portfolio",
                    "generated": False,
                    "data_args": {},
                    "layout": {"tab_id": "overview", "x": 24, "y": 2, "w": 16, "h": 10},
                },
                {
                    "widget_uuid": "widget_003",
                    "widget_id": "generated_note",
                    "origin": "generated",
                    "generated": True,
                    "type": "note",
                    "generated_data": "MSFT is largest at 34%. Technology is largest at 86%.",
                    "layout": {"tab_id": "overview", "x": 0, "y": 14, "w": 20, "h": 8},
                },
            ],
        }
    }

    grade = grade_task(task, snapshot, ())

    assert grade.passed is True


def test_grader_requires_tool_results_for_skill_task() -> None:
    task = find_task("core/skills/read_the_finance_earnings_prep_skill")
    result = TaskRunner().run(task, "oracle")

    assert result.grade.passed is True
    assert any(event.call.name == "get_skill_content" for event in result.trace)


def test_grader_matches_generated_widget_display_alias() -> None:
    task = find_task("price_performance_aapl")
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
    task = find_task("price_performance_aapl")
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
    task = find_task("price_performance_aapl")
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
    task = find_task("price_performance_aapl")
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
