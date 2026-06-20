from __future__ import annotations

from dataclasses import replace

from workspace_bench.core.graders import grade_scenario
from workspace_bench.core.models import LayoutChecks, SuccessCriteria
from workspace_bench.core.runner import ScenarioRunner, find_scenario


def test_grader_detects_missing_required_widget() -> None:
    scenario = find_scenario("l1_add_price_widget")
    snapshot = {
        "dashboard_composition": {
            "name": "Empty",
            "tabs": [{"id": "", "name": "", "layout": []}],
            "widgets": [],
        }
    }

    grade = grade_scenario(scenario, snapshot, ())

    assert grade.passed is False
    assert any(issue.code == "missing_widget" for issue in grade.issues)


def test_grader_detects_layout_overlap() -> None:
    scenario = find_scenario("l1_add_price_widget")
    scenario = replace(
        scenario,
        success=replace(
            scenario.success,
            required_widgets=(),
            required_layouts=(),
            layout=LayoutChecks(no_overlaps=True, within_grid=True, grid_width=40),
            trace=SuccessCriteria().trace,
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

    grade = grade_scenario(scenario, snapshot, ())

    assert grade.passed is False
    assert any(issue.code == "layout_overlap" for issue in grade.issues)


def test_grader_matches_generated_percent_equivalent() -> None:
    scenario = find_scenario("l0_portfolio_dashboard_note")
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

    grade = grade_scenario(scenario, snapshot, ())

    assert grade.passed is True


def test_grader_requires_tool_results_for_skill_scenario() -> None:
    scenario = find_scenario(
        "stark_l1_get_workspace_skill_content", pack="stark-enterprise-v0"
    )
    result = ScenarioRunner().run(scenario, "oracle")

    assert result.grade.passed is True
    assert any(event.call.name == "get_skill_content" for event in result.trace)


def test_grader_matches_generated_widget_display_alias() -> None:
    scenario = find_scenario("l3_app_template_summary")
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

    grade = grade_scenario(scenario, snapshot, ())

    assert grade.passed is True


def test_grader_dashboard_name_allows_stopwords_between_terms() -> None:
    scenario = find_scenario("l2_portfolio_macro_risk_dashboard")
    scenario = replace(
        scenario,
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

    grade = grade_scenario(scenario, snapshot, ())

    assert grade.passed is True
