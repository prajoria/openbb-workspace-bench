#!/usr/bin/env python3
"""Generate and certify the Workspace MCP smoke task suite."""

from __future__ import annotations

import copy
import json
import shutil
import sys
from dataclasses import replace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from workspace_bench.core.episode import WorkspaceEpisode  # noqa: E402
from workspace_bench.core.models import (  # noqa: E402
    TASK_SPEC_FIELDS,
    JsonDict,
    Task,
    TaskSuiteManifest,
)
from workspace_bench.workspace.tool_surface import WORKSPACE_TOOL_NAMES  # noqa: E402


OUTPUT_DIR = SRC / "workspace_bench" / "task_suites" / "smoke"
ORIGIN = "Bench Stark Enterprise"
WIDGET_ID = "compliance_surveillance_hub_alerts_alert_trend"
DEFAULT_DATA_ARGS = {"severity": "High", "status": "Open", "period": "YTD"}
MANIFEST_PAYLOAD: JsonDict = {
    "suite_id": "workspace-bench-smoke",
    "visibility": "public",
    "workspace_baseline": "default-v1",
    "description": "One minimal round-trip task for every Workspace MCP tool and knowledge surface.",
}

READ_TOOLS = {
    "get_workspace_snapshot",
    "list_available_widgets",
    "get_widget_schema",
    "get_params_options",
    "get_widget_data",
    "read_widget",
    "get_skill_content",
    "read_workspace_resource",
    "get_workspace_prompt",
}
SINGLE_WIDGET_TOOLS = {
    "create_widget",
    "update_widget",
    "update_widget_layout",
    "delete_widget",
    "add_generative_widget",
}
PLATFORM_TOOLS = {"manage_backends", "assign_tasks_to_agents"}


def _category(tool_name: str) -> str:
    if tool_name in READ_TOOLS:
        return "read"
    if tool_name in SINGLE_WIDGET_TOOLS:
        return "single-widget"
    if tool_name in PLATFORM_TOOLS:
        return "platform"
    return "dashboard"


def _call(tool: str, args: JsonDict) -> JsonDict:
    return {"tool": tool, "args": args}


def _required_call(tool: str, args_contains: JsonDict) -> JsonDict:
    return {"required_tool_calls": [{"tool": tool, "args_contains": args_contains}]}


def _seed_dashboard(
    tool_name: str,
    *,
    with_widget: bool = False,
    tabs: list[JsonDict] | None = None,
) -> JsonDict:
    dashboard: JsonDict = {
        "name": f"Smoke {tool_name}",
        "tabs": tabs or [{"id": "overview", "name": "Overview"}],
        "widgets": [],
        "activate": True,
    }
    if with_widget:
        dashboard["widgets"] = [
            {
                "origin": ORIGIN,
                "widget_id": WIDGET_ID,
                "tab_id": "overview",
                "data_args": copy.deepcopy(DEFAULT_DATA_ARGS),
                "layout": {"x": 0, "y": 0, "w": 20, "h": 14},
            }
        ]
    return {"dashboard": dashboard}


def _task(
    tool_name: str,
    prompt: str,
    oracle_tool_calls: list[JsonDict],
    success: JsonDict,
    *,
    initial_state: JsonDict | None = None,
) -> JsonDict:
    allowed_tools = list(dict.fromkeys(str(call["tool"]) for call in oracle_tool_calls))
    payload: JsonDict = {
        "id": f"smoke_{tool_name}",
        "category": _category(tool_name),
        "family": tool_name,
        "specification_level": "explicit",
        "difficulty": "easy",
        "prompt": prompt,
        "business_terms": [],
        "fixtures": {},
        "initial_state": initial_state or {},
        "allowed_tools": allowed_tools,
        "success": success,
        "oracle_tool_calls": oracle_tool_calls,
        "limits": {"max_turns": len(oracle_tool_calls)},
    }
    unknown = set(payload) - TASK_SPEC_FIELDS
    if unknown:
        raise AssertionError(f"smoke task has non-slim fields: {sorted(unknown)}")
    return payload


def build_tasks() -> list[JsonDict]:
    tasks = [
        _task(
            "get_workspace_snapshot",
            "Call get_workspace_snapshot once.",
            [_call("get_workspace_snapshot", {})],
            _required_call("get_workspace_snapshot", {}),
        ),
        _task(
            "manage_dashboard",
            "Use manage_dashboard operation='update' with dashboard_id 'dash_001' to rename the Home dashboard to 'Smoke Home Dashboard'.",
            [
                _call(
                    "manage_dashboard",
                    {
                        "operation": "update",
                        "dashboard_id": "dash_001",
                        "name": "Smoke Home Dashboard",
                    },
                )
            ],
            {"required_dashboard_name_contains": "Smoke Home Dashboard"},
        ),
        _task(
            "manage_navigation_bar",
            "Use manage_navigation_bar operation='create' on the current dashboard with tabs named 'Overview' and 'Details'.",
            [
                _call(
                    "manage_navigation_bar",
                    {
                        "operation": "create",
                        "tabs": [{"name": "Overview"}, {"name": "Details"}],
                    },
                )
            ],
            {"required_tabs": ["overview", "details"]},
        ),
        _task(
            "navigate_workspace",
            "Use navigate_workspace operation='tab' to switch to tab_id 'details', then use add_generative_widget to add a note named 'Navigation Marker' on that tab.",
            [
                _call("navigate_workspace", {"operation": "tab", "tab_id": "details"}),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "Navigation Marker",
                        "data": "Navigation round trip complete.",
                    },
                ),
            ],
            {
                "required_generated_widgets": [
                    {
                        "widget_type": "note",
                        "name_contains": "Navigation Marker",
                        "tab_id": "details",
                    }
                ]
            },
            initial_state=_seed_dashboard(
                "navigate_workspace",
                tabs=[
                    {"id": "overview", "name": "Overview"},
                    {"id": "details", "name": "Details"},
                ],
            ),
        ),
        _task(
            "list_available_widgets",
            "Call list_available_widgets for origin 'Bench Stark Enterprise'.",
            [_call("list_available_widgets", {"origin": ORIGIN})],
            _required_call("list_available_widgets", {"origin": ORIGIN}),
        ),
        _task(
            "get_widget_schema",
            "Call get_widget_schema for origin 'Bench Stark Enterprise' and widget_id 'compliance_surveillance_hub_alerts_alert_trend'.",
            [_call("get_widget_schema", {"origin": ORIGIN, "widget_id": WIDGET_ID})],
            _required_call(
                "get_widget_schema", {"origin": ORIGIN, "widget_id": WIDGET_ID}
            ),
        ),
        _task(
            "get_params_options",
            "Call get_params_options for param_name 'period' of widget_id 'compliance_surveillance_hub_alerts_alert_trend' from origin 'Bench Stark Enterprise'.",
            [
                _call(
                    "get_params_options",
                    {
                        "origin": ORIGIN,
                        "widget_id": WIDGET_ID,
                        "param_name": "period",
                        "data_args": {"severity": "High", "status": "Open"},
                    },
                )
            ],
            _required_call(
                "get_params_options",
                {
                    "origin": ORIGIN,
                    "widget_id": WIDGET_ID,
                    "param_name": "period",
                },
            ),
        ),
        _task(
            "get_widget_data",
            "Call get_widget_data for origin 'Bench Stark Enterprise' and widget_id 'compliance_surveillance_hub_alerts_alert_trend' with data_args severity 'High', status 'Open', period 'YTD'.",
            [
                _call(
                    "get_widget_data",
                    {
                        "origin": ORIGIN,
                        "widget_id": WIDGET_ID,
                        "data_args": copy.deepcopy(DEFAULT_DATA_ARGS),
                    },
                )
            ],
            _required_call(
                "get_widget_data",
                {
                    "origin": ORIGIN,
                    "widget_id": WIDGET_ID,
                    "data_args": copy.deepcopy(DEFAULT_DATA_ARGS),
                },
            ),
        ),
        _task(
            "create_widget",
            "Use create_widget to add widget_id 'compliance_surveillance_hub_alerts_alert_trend' from origin 'Bench Stark Enterprise' to the current dashboard with data_args severity 'High', status 'Open', period 'YTD'.",
            [
                _call(
                    "create_widget",
                    {
                        "origin": ORIGIN,
                        "widget_id": WIDGET_ID,
                        "data_args": copy.deepcopy(DEFAULT_DATA_ARGS),
                    },
                )
            ],
            {
                "required_widgets": [
                    {
                        "origin": ORIGIN,
                        "widget_id": WIDGET_ID,
                        "data_args": copy.deepcopy(DEFAULT_DATA_ARGS),
                    }
                ]
            },
        ),
        _task(
            "update_widget",
            "Use update_widget on the seeded widget_id 'compliance_surveillance_hub_alerts_alert_trend' from origin 'Bench Stark Enterprise' to set data_args period to 'MTD'.",
            [
                _call(
                    "update_widget",
                    {
                        "origin": ORIGIN,
                        "widget_id": WIDGET_ID,
                        "data_args": {"period": "MTD"},
                    },
                )
            ],
            {
                "required_widgets": [
                    {
                        "origin": ORIGIN,
                        "widget_id": WIDGET_ID,
                        "data_args": {"period": "MTD"},
                    }
                ]
            },
            initial_state=_seed_dashboard("update_widget", with_widget=True),
        ),
        _task(
            "update_widget_layout",
            "Use update_widget_layout on the seeded widget_id 'compliance_surveillance_hub_alerts_alert_trend' from origin 'Bench Stark Enterprise' to place it at x 0, y 0, w 20, h 10 on tab_id 'overview'.",
            [
                _call(
                    "update_widget_layout",
                    {
                        "origin": ORIGIN,
                        "widget_id": WIDGET_ID,
                        "x": 0,
                        "y": 0,
                        "w": 20,
                        "h": 10,
                        "tab_id": "overview",
                    },
                )
            ],
            {
                "required_layouts": [
                    {
                        "widget_id": WIDGET_ID,
                        "tab_id": "overview",
                        "x": 0,
                        "y": 0,
                        "w": 20,
                        "h": 10,
                    }
                ]
            },
            initial_state=_seed_dashboard("update_widget_layout", with_widget=True),
        ),
        _task(
            "delete_widget",
            "Use delete_widget to remove the seeded widget_id 'compliance_surveillance_hub_alerts_alert_trend' from origin 'Bench Stark Enterprise'.",
            [_call("delete_widget", {"origin": ORIGIN, "widget_id": WIDGET_ID})],
            {
                "required_widgets": [
                    {
                        "origin": ORIGIN,
                        "widget_id": WIDGET_ID,
                        "min_count": 0,
                        "max_count": 0,
                    }
                ]
            },
            initial_state=_seed_dashboard("delete_widget", with_widget=True),
        ),
        _task(
            "add_generative_widget",
            "Use add_generative_widget to add a note named 'Smoke Note' with any short text.",
            [
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "Smoke Note",
                        "data": "Smoke round trip complete.",
                    },
                )
            ],
            {
                "required_generated_widgets": [
                    {"widget_type": "note", "name_contains": "Smoke Note"}
                ]
            },
        ),
        _task(
            "read_widget",
            "Call read_widget for the seeded widget_id 'compliance_surveillance_hub_alerts_alert_trend' from origin 'Bench Stark Enterprise'.",
            [_call("read_widget", {"origin": ORIGIN, "widget_id": WIDGET_ID})],
            # The tool resolves widgets by widget_id alone; requiring origin
            # in the call args would fail semantically-correct calls.
            _required_call("read_widget", {"widget_id": WIDGET_ID}),
            initial_state=_seed_dashboard("read_widget", with_widget=True),
        ),
        _task(
            "manage_backends",
            "Call manage_backends operation='list' once.",
            [_call("manage_backends", {"operation": "list"})],
            _required_call("manage_backends", {"operation": "list"}),
        ),
        _task(
            "manage_apps",
            "Use manage_apps operation='instantiate' with backend_id 'backend_001', template_id 'portfolio-command-center', dashboard_name 'Smoke Instantiated App', and activate true.",
            [
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_001",
                        "template_id": "portfolio-command-center",
                        "dashboard_name": "Smoke Instantiated App",
                        "activate": True,
                    },
                )
            ],
            {
                "required_dashboard_name_contains": "Smoke Instantiated App",
                "layout": {"within_grid": False},
            },
        ),
        _task(
            "get_skill_content",
            "Call get_skill_content with slug 'finance-tearsheet'.",
            [_call("get_skill_content", {"slug": "finance-tearsheet"})],
            _required_call("get_skill_content", {"slug": "finance-tearsheet"}),
        ),
        _task(
            "read_workspace_resource",
            "Call read_workspace_resource with uri 'openbb://workspace/specs/widget-types'.",
            [
                _call(
                    "read_workspace_resource",
                    {"uri": "openbb://workspace/specs/widget-types"},
                )
            ],
            _required_call(
                "read_workspace_resource",
                {"uri": "openbb://workspace/specs/widget-types"},
            ),
        ),
        _task(
            "get_workspace_prompt",
            "Call get_workspace_prompt with name 'workspace_tool_usage'.",
            [_call("get_workspace_prompt", {"name": "workspace_tool_usage"})],
            _required_call("get_workspace_prompt", {"name": "workspace_tool_usage"}),
        ),
        _task(
            "assign_tasks_to_agents",
            "Call assign_tasks_to_agents with one task request having id 'smoke-envelope' and description 'Return the Workspace smoke envelope.'",
            [
                _call(
                    "assign_tasks_to_agents",
                    {
                        "task_requests": [
                            {
                                "id": "smoke-envelope",
                                "description": "Return the Workspace smoke envelope.",
                            }
                        ]
                    },
                )
            ],
            _required_call(
                "assign_tasks_to_agents",
                # The envelope echo accepts free-form request fields and the
                # args matcher compares lists exactly, so the round trip is
                # proven by the call itself.
                {},
            ),
        ),
    ]
    families = [str(task["family"]) for task in tasks]
    if tuple(families) != WORKSPACE_TOOL_NAMES:
        raise AssertionError(
            "smoke tasks must match WORKSPACE_TOOL_NAMES in canonical order: "
            f"observed={families} expected={list(WORKSPACE_TOOL_NAMES)}"
        )
    return tasks


def _enterprise_compositions(snapshot: JsonDict) -> dict[str, JsonDict]:
    compositions = snapshot.get("dashboard_compositions") or {}
    return {
        str(dashboard_id): copy.deepcopy(composition)
        for dashboard_id, composition in compositions.items()
        if composition.get("name") != "Home"
        and not str(composition.get("name", "")).startswith("Smoke ")
    }


def certify(tasks: list[JsonDict]) -> None:
    manifest = TaskSuiteManifest.from_dict(MANIFEST_PAYLOAD)
    failures: list[str] = []
    for payload in tasks:
        task_id = str(payload["id"])
        try:
            task = replace(Task.from_dict(payload), suite=manifest)
            episode = WorkspaceEpisode(task)
            enterprise_before = _enterprise_compositions(episode.initial_snapshot)
            if len(enterprise_before) != 23:
                failures.append(
                    f"{task_id}: expected 23 enterprise-app dashboards, "
                    f"found {len(enterprise_before)}"
                )
            for call in task.oracle_tool_calls:
                episode.step(call)
            oracle_grade = episode.grade()
            enterprise_after = _enterprise_compositions(episode.snapshot())
            noop_grade = WorkspaceEpisode(task).grade()
        except Exception as error:  # noqa: BLE001 - report every certification failure.
            failures.append(f"{task_id}: certification raised {error!r}")
            continue
        target_calls = sum(call.name == task.family for call in task.oracle_tool_calls)
        if target_calls != 1:
            failures.append(f"{task_id}: expected one target tool call, found {target_calls}")
        if not oracle_grade.passed:
            issues = "; ".join(
                f"{issue.code}: {issue.message}" for issue in oracle_grade.issues[:3]
            )
            failures.append(f"{task_id}: oracle failed: {issues}")
        if noop_grade.passed:
            failures.append(f"{task_id}: no-op passed")
        if oracle_grade.checks_total > 4:
            failures.append(
                f"{task_id}: {oracle_grade.checks_total} graded checks exceeds cap 4"
            )
        if enterprise_after != enterprise_before:
            failures.append(f"{task_id}: oracle mutated an enterprise-app dashboard")
    if failures:
        raise RuntimeError("Smoke certification failed:\n" + "\n".join(failures))


def write_suite(tasks: list[JsonDict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for child in OUTPUT_DIR.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
    (OUTPUT_DIR / "__init__.py").write_text(
        '"""Generated Workspace MCP smoke task suite."""\n', encoding="utf-8"
    )
    (OUTPUT_DIR / "task_suite.json").write_text(
        json.dumps(MANIFEST_PAYLOAD, indent=2) + "\n", encoding="utf-8"
    )
    for task in tasks:
        family = str(task["family"])
        family_dir = OUTPUT_DIR / family
        family_dir.mkdir(parents=True, exist_ok=True)
        path = family_dir / f"{task['id']}.json"
        path.write_text(json.dumps(task, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    tasks = build_tasks()
    certify(tasks)
    write_suite(tasks)
    print(f"Generated and certified {len(tasks)} smoke tasks in {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
