from workspace_bench.live_mcp import (
    bridge_command_to_simulator_call,
    execute_bridge_command,
)
from workspace_bench.models import FixtureBackendRef
from workspace_bench.simulated_workspace import SimulatedWorkspace


def test_bridge_command_maps_browser_data_source_shape() -> None:
    name, args = bridge_command_to_simulator_call(
        {
            "command": "get_widget_data",
            "request_id": "request-1",
            "data_sources": [
                {
                    "origin": "Bench Equities",
                    "id": "price_performance",
                    "input_args": {"symbol": "AAPL"},
                }
            ],
        }
    )

    assert name == "get_widget_data"
    assert args == {
        "origin": "Bench Equities",
        "widget_id": "price_performance",
        "data_args": {"symbol": "AAPL"},
        "widget_uuid": None,
        "ssm_request": None,
    }


def test_bridge_command_maps_browser_options_shape() -> None:
    name, args = bridge_command_to_simulator_call(
        {
            "command": "get_params_options",
            "param_options_queries": [
                {
                    "origin": "Bench Macro",
                    "id": "macro_timeseries",
                    "param": "series",
                    "options_endpoint_input_args": {},
                }
            ],
        }
    )

    assert name == "get_params_options"
    assert args == {
        "origin": "Bench Macro",
        "widget_id": "macro_timeseries",
        "param_name": "series",
        "data_args": {},
    }


def test_execute_bridge_command_preserves_real_command_name_for_layout() -> None:
    workspace = SimulatedWorkspace()
    workspace.reset(backends=[FixtureBackendRef(name="Bench Equities")])
    workspace.call_tool(
        "create_widget",
        {
            "origin": "Bench Equities",
            "widget_id": "price_performance",
            "data_args": {"symbol": "AAPL"},
        },
    )

    result = execute_bridge_command(
        workspace,
        {
            "command": "update_dashboard_layout",
            "request_id": "request-2",
            "widget_id": "price_performance",
            "x": 0,
            "y": 0,
            "w": 20,
            "h": 12,
        },
    )

    assert result["ok"] is True
    assert result["command"] == "update_dashboard_layout"
    assert result["request_id"] == "request-2"
    assert result["data"]["widget"]["layout"]["h"] == 12


def test_execute_bridge_snapshot_strips_simulator_only_fields() -> None:
    workspace = SimulatedWorkspace()
    workspace.reset(backends=[FixtureBackendRef(name="Bench Equities")])

    result = execute_bridge_command(
        workspace,
        {"command": "get_workspace_snapshot", "request_id": "request-3"},
    )

    assert result["ok"] is True
    assert result["request_id"] == "request-3"
    assert "dashboard_composition" in result["data"]
    assert "backends" not in result["data"]
