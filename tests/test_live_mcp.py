import asyncio
from types import SimpleNamespace

from workspace_bench.core.models import ToolCall
from workspace_bench.workspace.live_mcp import (
    EXPECTED_MCP_PROMPTS,
    EXPECTED_MCP_RESOURCES,
    EXPECTED_MCP_TOOLS,
    _call_mcp_tool,
    _surface_issues,
    bridge_command_to_simulator_call,
    execute_bridge_command,
)
from workspace_bench.core.models import FixtureBackendRef
from workspace_bench.workspace.simulated_workspace import SimulatedWorkspace


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


def test_surface_issues_reports_missing_mcp_resources() -> None:
    issues = _surface_issues(
        tools=tuple(sorted(EXPECTED_MCP_TOOLS)),
        prompts=tuple(sorted(EXPECTED_MCP_PROMPTS)),
        resources=(),
    )

    assert issues == (
        f"missing resource(s): {', '.join(sorted(EXPECTED_MCP_RESOURCES))}",
    )


def test_synthetic_tools_translate_to_mcp_resources_and_prompts() -> None:
    class FakeSession:
        async def read_resource(self, uri: str):
            return SimpleNamespace(
                contents=[
                    SimpleNamespace(
                        uri=uri,
                        mimeType="text/plain",
                        text="Workspace app builder index",
                    )
                ]
            )

        async def get_prompt(self, name: str, arguments=None):
            return SimpleNamespace(
                description="fixture prompt",
                messages=[
                    SimpleNamespace(
                        role="user",
                        content=SimpleNamespace(text="Workspace tool usage guidance"),
                    )
                ],
            )

    resource = asyncio.run(
        _call_mcp_tool(
            FakeSession(),
            ToolCall(
                "read_workspace_resource",
                {"uri": "openbb://workspace/app-builder/index"},
            ),
        )
    )
    prompt = asyncio.run(
        _call_mcp_tool(
            FakeSession(),
            ToolCall("get_workspace_prompt", {"name": "workspace_tool_usage"}),
        )
    )

    assert resource["ok"] is True
    assert resource["command"] == "read_workspace_resource"
    assert resource["data"]["text"] == "Workspace app builder index"
    assert prompt["ok"] is True
    assert prompt["command"] == "get_workspace_prompt"
    assert prompt["data"]["messages"][0]["content"] == "Workspace tool usage guidance"
