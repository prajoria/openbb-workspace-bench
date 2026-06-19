from __future__ import annotations

from workspace_bench.models import FixtureBackendRef, ToolCall
from workspace_bench.simulated_workspace import SimulatedWorkspace


def test_simulator_runs_schema_first_widget_creation_flow() -> None:
    workspace = SimulatedWorkspace()
    workspace.reset(backends=(FixtureBackendRef(name="equities"),), initial_state={})

    listed = workspace.call_tool(
        ToolCall("list_available_widgets", {"origin": "Bench Equities"})
    )
    assert listed["ok"] is True
    assert any(
        widget["widget_id"] == "price_performance"
        for widget in listed["data"]["widgets"]
    )

    schema = workspace.call_tool(
        ToolCall(
            "get_widget_schema",
            {"origin": "Bench Equities", "widget_id": "price_performance"},
        )
    )
    assert schema["data"]["schema"]["grid_data"]["w"] == 20

    created = workspace.call_tool(
        ToolCall(
            "create_widget",
            {
                "origin": "Bench Equities",
                "widget_id": "price_performance",
                "data_args": {"symbol": "AAPL"},
            },
        )
    )
    assert created["ok"] is True
    assert created["data"]["widget"]["data_args"] == {"symbol": "AAPL"}


def test_simulator_rejects_layout_changes_via_update_widget() -> None:
    workspace = SimulatedWorkspace()
    workspace.reset(backends=(FixtureBackendRef(name="equities"),), initial_state={})
    workspace.call_tool(
        ToolCall(
            "create_widget",
            {
                "origin": "Bench Equities",
                "widget_id": "price_performance",
                "data_args": {"symbol": "AAPL"},
            },
        )
    )

    result = workspace.call_tool(
        ToolCall(
            "update_widget",
            {
                "widget_id": "price_performance",
                "config": {"ui_args": {"x": 0, "w": 20}},
            },
        )
    )

    assert result["ok"] is False
    assert result["error"]["code"] == "invalid_request"

