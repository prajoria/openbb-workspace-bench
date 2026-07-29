from __future__ import annotations

from workspace_bench.core.models import FixtureBackendRef, ToolCall
from workspace_bench.workspace.simulated_workspace import SimulatedWorkspace


def test_simulator_runs_schema_first_widget_creation_flow() -> None:
    workspace = SimulatedWorkspace()
    workspace.reset(backends=(FixtureBackendRef(name="getting-started"),), initial_state={})

    listed = workspace.call_tool(
        ToolCall("list_available_widgets", {"origin": "Getting Started"})
    )
    assert listed["ok"] is True
    assert any(
        widget["widget_id"] == "table_widget_with_grouping_by_cell_click"
        for widget in listed["data"]["widgets"]
    )

    schema = workspace.call_tool(
        ToolCall(
            "get_widget_schema",
            {
                "origin": "Getting Started",
                "widget_id": "table_widget_with_grouping_by_cell_click",
            },
        )
    )
    assert schema["data"]["schema"]["grid_data"]["w"] == 20

    created = workspace.call_tool(
        ToolCall(
            "create_widget",
            {
                "origin": "Getting Started",
                "widget_id": "table_widget_with_grouping_by_cell_click",
                "data_args": {"symbol": "AAPL"},
            },
        )
    )
    assert created["ok"] is True
    assert created["data"]["widget"]["data_args"] == {"symbol": "AAPL"}


def test_simulator_rejects_layout_changes_via_update_widget() -> None:
    workspace = SimulatedWorkspace()
    workspace.reset(backends=(FixtureBackendRef(name="getting-started"),), initial_state={})
    workspace.call_tool(
        ToolCall(
            "create_widget",
            {
                "origin": "Getting Started",
                "widget_id": "table_widget_with_grouping_by_cell_click",
                "data_args": {"symbol": "AAPL"},
            },
        )
    )

    result = workspace.call_tool(
        ToolCall(
            "update_widget",
            {
                "widget_id": "table_widget_with_grouping_by_cell_click",
                "config": {"ui_args": {"x": 0, "w": 20}},
            },
        )
    )

    assert result["ok"] is False
    assert result["error"]["code"] == "invalid_request"


def test_simulator_reads_workspace_resources_and_prompts() -> None:
    workspace = SimulatedWorkspace()
    workspace.reset(backends=(FixtureBackendRef(name="getting-started"),), initial_state={})

    index = workspace.call_tool(
        ToolCall(
            "read_workspace_resource",
            {"uri": "openbb://workspace/app-builder/index"},
        )
    )
    skill = workspace.call_tool(
        ToolCall(
            "read_workspace_resource",
            {"uri": "openbb://workspace/skills/finance-earnings-prep"},
        )
    )
    prompt = workspace.call_tool(
        ToolCall("get_workspace_prompt", {"name": "workspace_tool_usage"})
    )
    missing = workspace.call_tool(
        ToolCall("read_workspace_resource", {"uri": "openbb://workspace/missing"})
    )

    assert index["ok"] is True
    assert index["data"]["uri"] == "openbb://workspace/app-builder/index"
    assert "Workspace app builder index" in index["data"]["text"]
    assert any(app["name"] == "Onboarding App for Devs" for app in index["data"]["apps"])
    assert skill["ok"] is True
    assert "Earnings prep workflow" in skill["data"]["content"]
    assert skill["data"]["content"] in skill["data"]["text"]
    assert prompt["ok"] is True
    assert "schema-before-create workspace tool discipline" in prompt["data"]["text"]
    assert missing["ok"] is False
    assert "openbb://workspace/app-builder/index" in missing["message"]
    assert "openbb://workspace/skills/finance-comps" in missing["message"]
