"""Tests for the Part 2 build-openbb-apps surface: validation, simulator, graders."""

from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import Task, ToolCall
from workspace_bench.workspace.backend_validation import (
    CANONICAL_WIDGET_VIZ_TYPES,
    WIDGET_VIZ_TYPE_ALIASES,
    validate_apps_json,
    validate_widgets_json,
)
from workspace_bench.workspace.simulated_workspace import SimulatedWorkspace


VALID_WIDGET = {
    "name": "VIX History",
    "description": "Daily CBOE VIX closes.",
    "endpoint": "/vix-history",
    "type": "table",
    "gridData": {"w": 20, "h": 9},
    "params": [
        {"paramName": "window", "type": "number", "label": "Window", "value": 30}
    ],
    "data": {
        "table": {
            "columnsDefs": [
                {"field": "date", "headerName": "Date", "cellDataType": "dateString"},
                {
                    "field": "close",
                    "headerName": "Close",
                    "cellDataType": "number",
                    "renderFn": "greenRed",
                },
            ]
        }
    },
}

VALID_APP = {
    "name": "VIX Monitor",
    "description": "Vol desk landing page.",
    "allowCustomization": True,
    "tabs": {
        "main": {
            "id": "main",
            "name": "Main",
            "layout": [{"i": "vix_history", "x": 0, "y": 0, "w": 20, "h": 9}],
        }
    },
    "groups": [],
    "prompts": ["How is volatility trending?"],
}


# ---------------------------------------------------------------- validation


def test_widgets_json_accepts_valid_payload():
    errors, warnings, normalized = validate_widgets_json({"vix_history": VALID_WIDGET})
    assert errors == []
    assert warnings == []
    assert normalized["vix_history"]["type"] == "table"


def test_widget_type_catalog_matches_live_snapshot() -> None:
    import json
    from pathlib import Path

    snapshot = json.loads(
        Path("runs/hosted-surface/widget_types.json").read_text(encoding="utf-8")
    )
    assert snapshot["uri"] == "openbb://workspace/specs/widget-types"
    assert set(snapshot["types"]) == CANONICAL_WIDGET_VIZ_TYPES
    assert WIDGET_VIZ_TYPE_ALIASES == {"ssrm_table": "table_ssrm"}


def test_widgets_json_accepts_legacy_ssrm_alias() -> None:
    widget = {
        "name": "Legacy SSRM",
        "description": "Compatibility fixture.",
        "endpoint": "/legacy",
        "type": "ssrm_table",
    }
    errors, _, normalized = validate_widgets_json({"legacy": widget})
    assert errors == []
    assert normalized["legacy"]["type"] == "ssrm_table"


def test_missing_app_prompts_has_distinct_issue_code() -> None:
    from dataclasses import replace

    from workspace_bench.core.models import RequiredAppDef, SuccessCriteria
    from workspace_bench.core.runner import find_task
    from workspace_bench.core.graders import grade_task

    task = find_task("build-openbb-apps/apps/vol_morning")
    task = replace(
        task,
        success=SuccessCriteria(
            required_app_defs=(
                RequiredAppDef(
                    backend_name="Vol Desk Data",
                    name_contains="Vol Morning",
                    prompts_min_count=1,
                ),
            )
        ),
    )
    snapshot = {
        "custom_backends": {
            "backend_001": {
                "name": "Vol Desk Data",
                "widgets_json": {},
                "apps_json": [{"name": "Vol Morning", "tabs": {}}],
            }
        }
    }
    grade = grade_task(task, snapshot, ())
    assert "app_prompts_missing" in {issue.code for issue in grade.issues}


def test_widgets_json_rejects_array_and_bare_widget():
    errors, _, _ = validate_widgets_json([VALID_WIDGET])
    assert errors and "array" in errors[0]
    errors, _, _ = validate_widgets_json(VALID_WIDGET)
    assert errors and "bare widget" in errors[0]


def test_widgets_json_requires_name_description_endpoint():
    errors, _, _ = validate_widgets_json({"w": {"name": "W", "endpoint": "/w"}})
    assert any("'description' is required" in error for error in errors)


def test_widgets_json_rejects_unknown_type_and_bad_grid():
    errors, _, _ = validate_widgets_json({
        "w": {
            "name": "W", "description": "d", "endpoint": "/w",
            "type": "tablez", "gridData": {"w": 99, "h": 0},
        }
    })
    assert any("unsupported type 'tablez'" in error for error in errors)
    assert any("gridData.w must be between" in error for error in errors)
    assert any("gridData.h must be at least 1" in error for error in errors)


def test_widgets_json_param_rules():
    errors, _, _ = validate_widgets_json({
        "w": {
            "name": "W", "description": "d", "endpoint": "/w",
            "params": [
                {"paramName": "a", "type": "number", "multiple": True},
                {"paramName": "a", "type": "text"},
                {"type": "text"},
                {"paramName": "b", "type": "dropdownz"},
            ],
        }
    })
    joined = " ".join(errors)
    assert "`multiple` can only be true" in joined
    assert "duplicate paramName 'a'" in joined
    assert "paramName is required" in joined
    assert "unsupported type 'dropdownz'" in joined


def test_widgets_json_columns_defs_rules():
    errors, _, _ = validate_widgets_json({
        "w": {
            "name": "W", "description": "d", "endpoint": "/w",
            "data": {"table": {"columnsDefs": [
                {"headerName": "No Field"},
                {"field": "x", "headerName": "X", "renderFn": "sparkle"},
                {
                    "field": "y", "headerName": "Y",
                    "renderFn": "cellOnClick",
                    "renderFnParams": {"actionType": "groupBy"},
                },
            ]}},
        }
    })
    joined = " ".join(errors)
    assert "field is required" in joined
    assert "unknown renderFn" in joined
    assert "`groupBy.paramName` is required" in joined


def test_widgets_json_default_type_and_defaultviz_fallback():
    _, _, normalized = validate_widgets_json({
        "plain": {"name": "P", "description": "d", "endpoint": "/p"},
        "viz": {
            "name": "V", "description": "d", "endpoint": "/v",
            "defaultViz": "markdown",
        },
    })
    assert normalized["plain"]["type"] == "table"
    assert normalized["viz"]["type"] == "markdown"


def test_widgets_json_unknown_keys_warn_not_reject():
    errors, warnings, _ = validate_widgets_json({
        "w": {
            "name": "W", "description": "d", "endpoint": "/w",
            "bogusKey": 1, "mcp_tool": {"mcp_server": "x", "tool_id": "y"},
        }
    })
    assert errors == []
    assert any("bogusKey" in warning for warning in warnings)
    assert not any("mcp_tool" in warning for warning in warnings)


def test_apps_json_schema_rules():
    errors, _, _ = validate_apps_json([{"description": "no name or tabs"}], set())
    joined = " ".join(errors)
    assert "'name' is required" in joined
    assert "'tabs' is required" in joined

    errors, _, _ = validate_apps_json(
        [{"name": "A", "tabs": {"t": {"id": "t", "name": "T",
                                       "layout": [{"i": "w", "x": 0, "y": 0}]}}}],
        {"w"},
    )
    assert any("'w' is required" in error or "'h' is required" in error for error in errors)


def test_apps_json_dangling_ref_and_overlap_warn():
    errors, warnings, normalized = validate_apps_json(
        [{
            "name": "A",
            "tabs": {"t": {"id": "t", "name": "T", "layout": [
                {"i": "known", "x": 0, "y": 0, "w": 10, "h": 5},
                {"i": "ghost", "x": 5, "y": 0, "w": 10, "h": 5},
            ]}},
        }],
        {"known"},
    )
    assert errors == []
    joined = " ".join(warnings)
    assert "Missing widgets used in tab `ghost`" in joined
    assert "overlap" in joined
    assert normalized[0]["template_id"] == "a"


# ---------------------------------------------------------------- simulator


def _workspace_with_custom_backend() -> tuple[SimulatedWorkspace, str]:
    workspace = SimulatedWorkspace()
    result = workspace.call_tool("manage_backends", {
        "operation": "add", "name": "VIX Desk", "url": "http://localhost:7779",
        "widgets_json": {"vix_history": VALID_WIDGET},
        "apps_json": [VALID_APP],
    })
    assert result["ok"], result
    return workspace, result["data"]["backend_id"]


def test_built_backend_full_round_trip():
    workspace, backend_id = _workspace_with_custom_backend()
    assert workspace.call_tool(
        "list_available_widgets", {"origin": "VIX Desk"}
    )["ok"]
    schema = workspace.call_tool(
        "get_widget_schema", {"origin": "VIX Desk", "widget_id": "vix_history"}
    )
    assert schema["ok"] and schema["data"]["schema"]["type"] == "table"
    created = workspace.call_tool("create_widget", {
        "origin": "VIX Desk", "widget_id": "vix_history",
        "data_args": {"window": 60},
    })
    assert created["ok"]
    instantiated = workspace.call_tool("manage_apps", {
        "operation": "instantiate", "backend_id": backend_id,
        "app_name": "VIX Monitor",
    })
    assert instantiated["ok"]
    snapshot = workspace.snapshot()
    assert backend_id in snapshot["custom_backends"]
    assert "vix_history" in snapshot["custom_backends"][backend_id]["widgets_json"]


def test_add_requires_url_and_unique_name():
    workspace, _ = _workspace_with_custom_backend()
    no_url = workspace.call_tool("manage_backends", {
        "operation": "add", "name": "Another", "widgets_json": {},
    })
    assert not no_url["ok"]
    assert "requires name and url" in no_url["error"]["message"]
    duplicate = workspace.call_tool("manage_backends", {
        "operation": "add", "name": "VIX Desk", "url": "http://x",
        "widgets_json": {},
    })
    assert not duplicate["ok"]
    assert "already exists" in duplicate["error"]["message"]


def test_refresh_repairs_custom_backend():
    workspace, backend_id = _workspace_with_custom_backend()
    broken = workspace.call_tool("manage_backends", {
        "operation": "refresh", "backend_id": backend_id,
        "widgets_json": {"vix_history": {"name": "V", "endpoint": "/v"}},
    })
    assert not broken["ok"]
    assert "refresh failed" in broken["error"]["message"].lower()
    fixed_widget = dict(VALID_WIDGET, description="Fixed description.")
    fixed = workspace.call_tool("manage_backends", {
        "operation": "refresh", "backend_id": backend_id,
        "widgets_json": {"vix_history": fixed_widget},
    })
    assert fixed["ok"]
    snapshot = workspace.snapshot()
    stored = snapshot["custom_backends"][backend_id]["widgets_json"]["vix_history"]
    assert stored["description"] == "Fixed description."


def test_refresh_payload_rejected_for_fixture_backends():
    workspace = SimulatedWorkspace()
    workspace.call_tool("manage_backends", {"operation": "add", "name": "equities"})
    result = workspace.call_tool("manage_backends", {
        "operation": "refresh", "backend_id": "backend_001",
        "widgets_json": {},
    })
    assert not result["ok"]
    assert "only supported for custom backends" in result["error"]["message"]


def test_seeded_custom_backend_and_broken_instantiate():
    workspace = SimulatedWorkspace()
    workspace.reset(initial_state={
        "custom_backends": [{
            "name": "Seeded Desk", "url": "http://localhost:7779",
            "widgets_json": {"good": {
                "name": "Good", "description": "d", "endpoint": "/good",
            }},
            "apps_json": [{
                "name": "Broken App", "template_id": "broken-app",
                "tabs": {"t": {"id": "t", "name": "T", "layout": [
                    {"i": "ghost", "x": 0, "y": 0, "w": 10, "h": 5},
                ]}},
            }],
        }],
    })
    snapshot = workspace.snapshot()
    assert any(
        meta["name"] == "Seeded Desk"
        for meta in snapshot["custom_backends"].values()
    )
    result = workspace.call_tool("manage_apps", {
        "operation": "instantiate", "backend_id": "backend_001",
        "template_id": "broken-app",
    })
    assert not result["ok"]
    assert "widgets are unavailable" in result["error"]["message"]


def test_delete_reconciles_seeded_duplicate_custom_backend_names():
    workspace = SimulatedWorkspace()
    workspace.reset(
        initial_state={
            "custom_backends": [
                {
                    "backend_id": backend_id,
                    "name": "Duplicate Desk",
                    "url": "http://localhost:7779",
                    "widgets_json": {"vix_history": VALID_WIDGET},
                }
                for backend_id in ("keep_backend", "remove_backend")
            ]
        }
    )

    result = workspace.call_tool(
        "manage_backends",
        {"operation": "delete", "backend_id": "remove_backend"},
    )

    assert result["ok"]
    listed = workspace.call_tool("manage_backends", {"operation": "list"})
    assert [item["name"] for item in listed["data"]["backends"]] == ["Duplicate Desk"]
    assert workspace.call_tool(
        "get_widget_schema",
        {"origin": "Duplicate Desk", "widget_id": "vix_history"},
    )["ok"]


def test_debug_episode_exposes_fault_then_returns_data_after_refresh():
    from workspace_bench.core.runner import find_task

    task = find_task("build-openbb-apps/debug/execution_data_mismatch")
    episode = WorkspaceEpisode(task)
    probe = ToolCall(
        "get_widget_data",
        {"origin": "Execution Repair Data", "widget_id": "review_queue"},
    )

    broken = episode.step(probe)
    assert not broken["ok"]
    assert "missing declared fields" in broken["error"]["message"]

    refresh = next(
        call
        for call in task.oracle_tool_calls
        if call.name == "manage_backends" and call.args.get("operation") == "refresh"
    )
    assert episode.step(refresh)["ok"]
    repaired = episode.step(probe)
    assert repaired["ok"]
    assert repaired["data"]["data"][0]["order_id"] == "order_id-1"


def test_debug_read_widget_surfaces_custom_backend_data_preview():
    from workspace_bench.core.runner import find_task

    task = find_task("build-openbb-apps/debug/vendor_wrong_form_endpoint")
    episode = WorkspaceEpisode(task)
    for call in task.oracle_tool_calls:
        episode.step(call)
        if call.name == "manage_apps":
            break

    result = episode.step(ToolCall("read_widget", {"widget_id": "review_queue"}))

    assert result["ok"]
    assert result["data"]["widget"]["data_preview"][0]["record_id"] == "record_id-1"


def test_debug_episode_surfaces_form_route_and_live_row_identity_faults():
    from workspace_bench.core.runner import find_task

    cases = (
        ("vendor_wrong_form_endpoint", "form submission route"),
        ("execution_wrong_live_row_id", "live-grid row identifier"),
    )
    for task_id, expected in cases:
        episode = WorkspaceEpisode(find_task(f"build-openbb-apps/debug/{task_id}"))
        result = episode.step(
            ToolCall(
                "get_widget_data",
                {
                    "origin": (
                        "Vendor Repair Data"
                        if task_id.startswith("vendor")
                        else "Execution Repair Data"
                    ),
                    "widget_id": "review_queue",
                },
            )
        )
        assert not result["ok"]
        assert expected in result["error"]["message"]
        assert set(episode.initial_snapshot["dashboard_compositions"]) == {
            "incident_triage",
            "archive_workspace",
        }


# ---------------------------------------------------------------- grading


def _building_task() -> Task:
    return Task.from_dict({
        "id": "auth_test_task",
        "category": "platform",
        "family": "backend-building",
        "difficulty": "medium",
        "split": "dev",
        "prompt": "Author the VIX backend.",
        "fixtures": {},
        "initial_state": {},
        "allowed_tools": ["get_workspace_snapshot", "manage_backends", "manage_apps"],
        "success": {
            "required_widget_defs": [{
                "backend_name": "VIX Desk",
                "widget_id": "vix_history",
                "expect": {"type": "table", "endpoint": "/vix-history",
                           "gridData.w": 20},
                "params_include": [{"paramName": "window", "type": "number"}],
                "columns_include": [{"field": "close", "renderFn": "greenRed"}],
            }],
            "required_app_defs": [{
                "backend_name": "VIX Desk",
                "template_id": "vix-monitor",
                "tabs_include": ["main"],
                "layout_refs_valid": True,
                "no_overlaps": True,
                "prompts_min_count": 1,
                "widgets_on_tab": [{"tab_id": "main", "widget_id": "vix_history"}],
            }],

        },
        "oracle_tool_calls": [
            {"tool": "get_workspace_snapshot", "args": {}},
            {"tool": "manage_backends", "args": {
                "operation": "add", "name": "VIX Desk",
                "url": "http://localhost:7779",
                "widgets_json": {"vix_history": VALID_WIDGET},
                "apps_json": [VALID_APP],
            }},
        ],
        "limits": {"max_turns": 6},
    })


def test_building_task_oracle_passes_and_noop_fails():
    task = _building_task()
    episode = WorkspaceEpisode(task)
    for call in task.oracle_tool_calls:
        result = episode.step(call)
        assert result.get("ok"), result
    grade = episode.grade()
    assert grade.passed, [issue.message for issue in grade.issues]

    noop = WorkspaceEpisode(task)
    noop_grade = noop.grade()
    assert not noop_grade.passed
    assert any(
        issue.code == "missing_custom_backend" for issue in noop_grade.issues
    )


def test_building_grader_catches_wrong_definition():
    task = _building_task()
    episode = WorkspaceEpisode(task)
    wrong_widget = dict(VALID_WIDGET, endpoint="/wrong")
    episode.step(ToolCall(name="manage_backends", args={
        "operation": "add", "name": "VIX Desk", "url": "http://localhost:7779",
        "widgets_json": {"vix_history": wrong_widget},
        "apps_json": [VALID_APP],
    }))
    grade = episode.grade()
    assert not grade.passed
    assert any(issue.code == "widget_def_mismatch" for issue in grade.issues)
