"""Generate the Workspace MCP smoke suite as a four-level execution ladder.

Every canonical Workspace MCP tool family appears once per level:

- ``level0`` — only the target tool is allowed, no workspace baseline, and a
  declarative prompt: does the tool round-trip at all.
- ``level1`` — the full tool surface is allowed (distractors), still no
  baseline, same declarative prompt: does the agent pick the right tool.
- ``level2`` — full surface on the lived-in ``stark-onboard-a`` baseline:
  does the call survive a realistic workspace.
- ``level3`` — level2 with an open prompt that names business intent, never
  widget ids: can the agent discover the target before acting.

Each task declares its own workspace axes explicitly: the Stark data world
``stark-enterprise-x`` (plus ``getting-started`` in the second-origin family)
and the six Daloopa skills. Categories are derived from the family by the
loader and never written.
"""

from __future__ import annotations

import copy
import json
import shutil
import sys
from dataclasses import dataclass, field, replace
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

from workspace_bench.core.episode import WorkspaceEpisode  # noqa: E402
from workspace_bench.core.suite_checks import task_payload_digest  # noqa: E402
from workspace_bench.core.models import (  # noqa: E402
    TASK_SPEC_FIELDS,
    JsonDict,
    Task,
    TaskSuiteManifest,
)
from workspace_bench.core.models import WORKSPACE_TOOL_NAMES  # noqa: E402

OUTPUT_DIR = REPO / "src" / "workspace_bench" / "task_suites" / "smoke"

MANIFEST_PAYLOAD: JsonDict = {
    "suite_id": "workspace-bench-smoke",
    "visibility": "public",
    "description": (
        "A four-level execution ladder with one task per Workspace MCP tool "
        "and knowledge surface per level: level0 isolates the tool on a bare "
        "workspace, level1 adds the full 20-tool surface, level2 the "
        "lived-in stark-onboard-a workspace, and level3 an open prompt that "
        "requires discovery."
    ),
}

STARK = "Bench Stark Enterprise"
BASELINE = "stark-onboard-a"
DEFAULT_BACKENDS = ["stark-enterprise-x"]
SKILLS = [
    "daloopa-capital-allocation",
    "daloopa-earnings-review",
    "daloopa-guidance-tracker",
    "daloopa-industry",
    "daloopa-inflection",
    "daloopa-tearsheet",
]
LEVELS = ("level0", "level1", "level2", "level3")
# Tight smoke budgets: declarative levels get at most two turns (the
# listed-id discipline families need list-then-act); the open level gets
# discovery plus one misstep of slack.
LEVEL_TURNS = {"level0": 1, "level1": 2, "level2": 2, "level3": 4}

# Home plus the stark-onboard-a composition (3 opened apps + 3 personal
# dashboards) that certification must find untouched after every oracle on
# the baseline levels.
BASELINE_DASHBOARD_COUNT = 6


def _call(tool: str, args: JsonDict) -> JsonDict:
    return {"tool": tool, "args": args}


def _optional_call(tool: str, args: JsonDict) -> JsonDict:
    """A reference step agents may legitimately skip (not graded)."""

    return {"tool": tool, "args": args, "optional": True}


def _seed(
    family: str,
    *,
    widget_id: str | None = None,
    data_args: JsonDict | None = None,
    tabs: list[JsonDict] | None = None,
) -> JsonDict:
    dashboard: JsonDict = {
        "name": f"Smoke {family}",
        "tabs": tabs or [{"id": "overview", "name": "Overview"}],
        "activate": True,
        "widgets": [],
    }
    if widget_id is not None:
        dashboard["widgets"] = [
            {
                "origin": STARK,
                "widget_id": widget_id,
                "tab_id": "overview",
                "data_args": data_args or {},
                "layout": {"x": 0, "y": 0, "w": 20, "h": 14},
            }
        ]
    return {"dashboard": dashboard}


@dataclass(frozen=True)
class FamilySpec:
    """One tool family expanded into the four ladder levels."""

    tool: str
    prompt: str
    open_prompt: str
    oracle: list[JsonDict]
    success: JsonDict
    initial_state: JsonDict | None = None
    open_oracle: list[JsonDict] | None = None
    # Oracle for level1/level2, where the full tool surface activates the
    # listed-widget-id discipline (list the origin before using an id).
    listed_oracle: list[JsonDict] | None = None
    backends: list[str] = field(default_factory=lambda: list(DEFAULT_BACKENDS))


def _family_specs() -> list[FamilySpec]:
    return [
        FamilySpec(
            tool="get_workspace_snapshot",
            prompt="Call get_workspace_snapshot once.",
            open_prompt="Get a complete picture of what is currently in this workspace.",
            oracle=[_call("get_workspace_snapshot", {})],
            success={"calls_match_reference": True},
        ),
        FamilySpec(
            tool="manage_dashboard",
            prompt=(
                "Use manage_dashboard operation='update' with dashboard_id "
                "'dash_001' to rename the current dashboard to "
                "'Smoke Renamed Dashboard'."
            ),
            open_prompt=(
                "Rename the dashboard you are currently working in to "
                "'Smoke Renamed Dashboard'."
            ),
            oracle=[
                _call(
                    "manage_dashboard",
                    {
                        "operation": "update",
                        "dashboard_id": "dash_001",
                        "name": "Smoke Renamed Dashboard",
                    },
                )
            ],
            open_oracle=[
                _call("get_workspace_snapshot", {}),
                _call(
                    "manage_dashboard",
                    {
                        "operation": "update",
                        "dashboard_id": "dash_001",
                        "name": "Smoke Renamed Dashboard",
                    },
                ),
            ],
            success={"required_dashboard_name_contains": "Smoke Renamed Dashboard"},
        ),
        FamilySpec(
            tool="manage_navigation_bar",
            prompt=(
                "Use manage_navigation_bar operation='create' on the current "
                "dashboard with tabs named 'Overview' and 'Details'."
            ),
            open_prompt=(
                "Organize the current dashboard into two tabs called "
                "'Overview' and 'Details'."
            ),
            oracle=[
                _call(
                    "manage_navigation_bar",
                    {
                        "operation": "create",
                        "tabs": [{"name": "Overview"}, {"name": "Details"}],
                    },
                )
            ],
            success={"required_tabs": ["overview", "details"]},
        ),
        FamilySpec(
            tool="navigate_workspace",
            prompt="Use navigate_workspace operation='tab' to switch to tab_id 'details'.",
            open_prompt="Switch over to the Details tab of the current dashboard.",
            oracle=[_call("navigate_workspace", {"operation": "tab", "tab_id": "details"})],
            open_oracle=[
                _optional_call("get_workspace_snapshot", {}),
                _call("navigate_workspace", {"operation": "tab", "tab_id": "details"}),
            ],
            success={"calls_match_reference": True},
            initial_state=_seed(
                "navigate_workspace",
                tabs=[
                    {"id": "overview", "name": "Overview"},
                    {"id": "details", "name": "Details"},
                ],
            ),
        ),
        FamilySpec(
            tool="list_available_widgets",
            prompt="Call list_available_widgets for origin 'Getting Started'.",
            open_prompt="See which widgets the Getting Started backend offers.",
            oracle=[_call("list_available_widgets", {"origin": "Getting Started"})],
            success={"calls_match_reference": True},
            backends=["stark-enterprise-x", "getting-started"],
        ),
        FamilySpec(
            tool="get_widget_schema",
            prompt=(
                "Call get_widget_schema for origin 'Bench Stark Enterprise' and "
                "widget_id 'portfolio_command_center_actions_trade_ideas'."
            ),
            open_prompt=(
                "Look up the full schema of the Trade Ideas widget offered by "
                "Bench Stark Enterprise."
            ),
            oracle=[
                _call(
                    "get_widget_schema",
                    {
                        "origin": STARK,
                        "widget_id": "portfolio_command_center_actions_trade_ideas",
                    },
                )
            ],
            open_oracle=[
                _optional_call("list_available_widgets", {"origin": STARK}),
                _call(
                    "get_widget_schema",
                    {
                        "origin": STARK,
                        "widget_id": "portfolio_command_center_actions_trade_ideas",
                    },
                ),
            ],
            listed_oracle=[
                _optional_call("list_available_widgets", {"origin": STARK}),
                _call(
                    "get_widget_schema",
                    {
                        "origin": STARK,
                        "widget_id": "portfolio_command_center_actions_trade_ideas",
                    },
                ),
            ],
            success={"calls_match_reference": True},
        ),
        FamilySpec(
            tool="get_params_options",
            prompt=(
                "Call get_params_options for param_name 'period' of widget_id "
                "'earnings_estimates_monitor_calendar_upcoming_earnings' from "
                "origin 'Bench Stark Enterprise'."
            ),
            open_prompt=(
                "Find out which period choices the Upcoming Earnings widget "
                "from Bench Stark Enterprise supports."
            ),
            oracle=[
                _call(
                    "get_params_options",
                    {
                        "origin": STARK,
                        "widget_id": "earnings_estimates_monitor_calendar_upcoming_earnings",
                        "param_name": "period",
                    },
                )
            ],
            open_oracle=[
                _optional_call("list_available_widgets", {"origin": STARK}),
                _call(
                    "get_params_options",
                    {
                        "origin": STARK,
                        "widget_id": "earnings_estimates_monitor_calendar_upcoming_earnings",
                        "param_name": "period",
                    },
                ),
            ],
            success={"calls_match_reference": True},
        ),
        FamilySpec(
            tool="get_widget_data",
            prompt=(
                "Call get_widget_data for origin 'Bench Stark Enterprise' and "
                "widget_id 'risk_exposure_monitor_dashboard_var_trend' with "
                "data_args portfolio 'Global Equity' and period 'YTD'."
            ),
            open_prompt=(
                "Fetch the year-to-date VaR Trend numbers for the Global Equity "
                "portfolio from Bench Stark Enterprise."
            ),
            oracle=[
                _call(
                    "get_widget_data",
                    {
                        "origin": STARK,
                        "widget_id": "risk_exposure_monitor_dashboard_var_trend",
                        "data_args": {"portfolio": "Global Equity", "period": "YTD"},
                    },
                )
            ],
            open_oracle=[
                _optional_call("list_available_widgets", {"origin": STARK}),
                _call(
                    "get_widget_data",
                    {
                        "origin": STARK,
                        "widget_id": "risk_exposure_monitor_dashboard_var_trend",
                        "data_args": {"portfolio": "Global Equity", "period": "YTD"},
                    },
                ),
            ],
            success={"calls_match_reference": True},
        ),
        FamilySpec(
            tool="read_widget",
            prompt=(
                "Call read_widget for the seeded widget_id "
                "'client_360_client_book_client_accounts' from origin "
                "'Bench Stark Enterprise'."
            ),
            open_prompt=(
                "Read the configuration of the only widget on the "
                "'Smoke read_widget' dashboard."
            ),
            oracle=[
                {
                    **_call(
                        "read_widget",
                        {
                            "origin": STARK,
                            "widget_id": "client_360_client_book_client_accounts",
                        },
                    ),
                    "graded_args": ["widget_id"],
                }
            ],
            open_oracle=[
                _optional_call("get_workspace_snapshot", {}),
                {
                    **_call(
                        "read_widget",
                        {
                            "origin": STARK,
                            "widget_id": "client_360_client_book_client_accounts",
                        },
                    ),
                    "graded_args": ["widget_id"],
                },
            ],
            success={"calls_match_reference": True},
            initial_state=_seed(
                "read_widget",
                widget_id="client_360_client_book_client_accounts",
                data_args={"client": "Atlas Pension", "region": "Americas", "period": "YTD"},
            ),
        ),
        FamilySpec(
            tool="get_skill_content",
            prompt="Call get_skill_content with slug 'daloopa-tearsheet'.",
            open_prompt="Pull up the Daloopa tearsheet workflow skill.",
            oracle=[_call("get_skill_content", {"slug": "daloopa-tearsheet"})],
            success={"calls_match_reference": True},
        ),
        FamilySpec(
            tool="read_workspace_resource",
            prompt=(
                "Call read_workspace_resource with uri "
                "'openbb://workspace/specs/widget-types'."
            ),
            open_prompt=(
                "Open the workspace documentation resource that lists the "
                "supported widget types."
            ),
            oracle=[
                _call(
                    "read_workspace_resource",
                    {"uri": "openbb://workspace/specs/widget-types"},
                )
            ],
            success={"calls_match_reference": True},
        ),
        FamilySpec(
            tool="get_workspace_prompt",
            prompt="Call get_workspace_prompt with name 'workspace_tool_usage'.",
            open_prompt="Fetch the workspace guidance prompt about disciplined tool usage.",
            oracle=[_call("get_workspace_prompt", {"name": "workspace_tool_usage"})],
            success={"calls_match_reference": True},
        ),
        FamilySpec(
            tool="create_widget",
            prompt=(
                "Use create_widget to add widget_id "
                "'compliance_surveillance_hub_alerts_alert_trend' from origin "
                "'Bench Stark Enterprise' to the current dashboard with "
                "data_args severity 'High', status 'Open', period 'YTD'."
            ),
            open_prompt=(
                "Add the Alert Trend widget from Bench Stark Enterprise to the "
                "current dashboard, set up to track open high-severity alerts "
                "year-to-date."
            ),
            oracle=[
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": "compliance_surveillance_hub_alerts_alert_trend",
                        "data_args": {
                            "severity": "High",
                            "status": "Open",
                            "period": "YTD",
                        },
                    },
                )
            ],
            open_oracle=[
                _call("list_available_widgets", {"origin": STARK}),
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": "compliance_surveillance_hub_alerts_alert_trend",
                        "data_args": {
                            "severity": "High",
                            "status": "Open",
                            "period": "YTD",
                        },
                    },
                ),
            ],
            listed_oracle=[
                _call("list_available_widgets", {"origin": STARK}),
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": "compliance_surveillance_hub_alerts_alert_trend",
                        "data_args": {
                            "severity": "High",
                            "status": "Open",
                            "period": "YTD",
                        },
                    },
                ),
            ],
            success={
                "required_widgets": [
                    {
                        "origin": STARK,
                        "widget_id": "compliance_surveillance_hub_alerts_alert_trend",
                        "data_args": {
                            "severity": "High",
                            "status": "Open",
                            "period": "YTD",
                        },
                    }
                ]
            },
        ),
        FamilySpec(
            tool="update_widget",
            prompt=(
                "Use update_widget on the seeded widget_id "
                "'strategy_health_monitor_capacity_capacity_utilization' from "
                "origin 'Bench Stark Enterprise' to set data_args period to 'MTD'."
            ),
            open_prompt=(
                "On the 'Smoke update_widget' dashboard, switch the Capacity "
                "Utilization widget to show the month-to-date view."
            ),
            oracle=[
                _call(
                    "update_widget",
                    {
                        "origin": STARK,
                        "widget_id": "strategy_health_monitor_capacity_capacity_utilization",
                        "data_args": {"period": "MTD"},
                    },
                )
            ],
            open_oracle=[
                _call("get_workspace_snapshot", {}),
                _call(
                    "update_widget",
                    {
                        "origin": STARK,
                        "widget_id": "strategy_health_monitor_capacity_capacity_utilization",
                        "data_args": {"period": "MTD"},
                    },
                ),
            ],
            success={
                "required_widgets": [
                    {
                        "origin": STARK,
                        "widget_id": "strategy_health_monitor_capacity_capacity_utilization",
                        "data_args": {"period": "MTD"},
                    }
                ]
            },
            initial_state=_seed(
                "update_widget",
                widget_id="strategy_health_monitor_capacity_capacity_utilization",
                data_args={"strategy": "Global Equities", "period": "YTD"},
            ),
        ),
        FamilySpec(
            tool="update_widget_layout",
            prompt=(
                "Use update_widget_layout on the seeded widget_id "
                "'vendor_dataset_monitor_incidents_incident_log' from origin "
                "'Bench Stark Enterprise' to place it at x 0, y 0, w 20, h 10 "
                "on tab_id 'overview'."
            ),
            open_prompt=(
                "On the 'Smoke update_widget_layout' dashboard, resize the "
                "Incident Log widget to half width (20 columns) and 10 rows "
                "at the top-left of its tab."
            ),
            oracle=[
                _call(
                    "update_widget_layout",
                    {
                        "origin": STARK,
                        "widget_id": "vendor_dataset_monitor_incidents_incident_log",
                        "x": 0,
                        "y": 0,
                        "w": 20,
                        "h": 10,
                        "tab_id": "overview",
                    },
                )
            ],
            open_oracle=[
                _call("get_workspace_snapshot", {}),
                _call(
                    "update_widget_layout",
                    {
                        "origin": STARK,
                        "widget_id": "vendor_dataset_monitor_incidents_incident_log",
                        "x": 0,
                        "y": 0,
                        "w": 20,
                        "h": 10,
                        "tab_id": "overview",
                    },
                ),
            ],
            success={
                "required_layouts": [
                    {
                        "widget_id": "vendor_dataset_monitor_incidents_incident_log",
                        "tab_id": "overview",
                        "x": 0,
                        "y": 0,
                        "w": 20,
                        "h": 10,
                    }
                ]
            },
            initial_state=_seed(
                "update_widget_layout",
                widget_id="vendor_dataset_monitor_incidents_incident_log",
                data_args={"vendor": "FactSet", "status": "Open", "period": "YTD"},
            ),
        ),
        FamilySpec(
            tool="delete_widget",
            prompt=(
                "Use delete_widget to remove the seeded widget_id "
                "'nav_fees_close_dashboard_close_close_exceptions' from origin "
                "'Bench Stark Enterprise'."
            ),
            open_prompt="Clear out the only widget on the 'Smoke delete_widget' dashboard.",
            oracle=[
                _call(
                    "delete_widget",
                    {
                        "origin": STARK,
                        "widget_id": "nav_fees_close_dashboard_close_close_exceptions",
                    },
                )
            ],
            open_oracle=[
                _call("get_workspace_snapshot", {}),
                _call(
                    "delete_widget",
                    {
                        "origin": STARK,
                        "widget_id": "nav_fees_close_dashboard_close_close_exceptions",
                    },
                ),
            ],
            success={
                "required_widgets": [
                    {
                        "origin": STARK,
                        "widget_id": "nav_fees_close_dashboard_close_close_exceptions",
                        "min_count": 0,
                        "max_count": 0,
                    }
                ]
            },
            initial_state=_seed(
                "delete_widget",
                widget_id="nav_fees_close_dashboard_close_close_exceptions",
                data_args={"fund": "Flagship Long/Short", "status": "Open", "period": "YTD"},
            ),
        ),
        FamilySpec(
            tool="add_generative_widget",
            prompt=(
                "Use add_generative_widget to add a note named 'Smoke Note' "
                "with any short text."
            ),
            open_prompt="Leave a short note named 'Smoke Note' on the current dashboard.",
            oracle=[
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "Smoke Note",
                        "data": "Smoke round trip complete.",
                    },
                )
            ],
            success={
                "required_generated_widgets": [
                    {"widget_type": "note", "name_contains": "Smoke Note"}
                ]
            },
        ),
        FamilySpec(
            tool="manage_apps",
            prompt=(
                "Use manage_apps operation='instantiate' with backend_id "
                "'backend_001', template_id 'portfolio-command-center', "
                "dashboard_name 'Smoke Instantiated App', and activate true."
            ),
            open_prompt=(
                "Open a fresh copy of the Portfolio Command Center app as a "
                "new dashboard named 'Smoke Instantiated App' and switch to it."
            ),
            oracle=[
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
            success={
                "required_dashboard_name_contains": "Smoke Instantiated App",
                # Suppress the default-on grid check: the 20 instantiated
                # widgets would each add a graded check and breach the cap.
                "layout": {"within_grid": False},
            },
        ),
        FamilySpec(
            tool="manage_backends",
            prompt="Call manage_backends operation='list' once.",
            open_prompt="Check which data backends this workspace is connected to.",
            oracle=[_call("manage_backends", {"operation": "list"})],
            success={"calls_match_reference": True},
        ),
        FamilySpec(
            tool="assign_tasks_to_agents",
            prompt=(
                "Call assign_tasks_to_agents with one task request having id "
                "'smoke-envelope' and description 'Return the Workspace smoke "
                "envelope.'"
            ),
            open_prompt=(
                "Delegate one follow-up job to the agent fleet asking it to "
                "return the Workspace smoke envelope."
            ),
            oracle=[
                {
                    **_call(
                        "assign_tasks_to_agents",
                        {
                            "task_requests": [
                                {
                                    "id": "smoke-envelope",
                                    "description": "Return the Workspace smoke envelope.",
                                }
                            ]
                        },
                    ),
                    # The envelope echo accepts free-form request fields and
                    # the args matcher compares lists exactly, so the round
                    # trip is proven by the call itself.
                    "graded_args": [],
                }
            ],
            success={"calls_match_reference": True},
        ),
    ]


def _level_task(spec: FamilySpec, level: str) -> JsonDict:
    open_level = level == "level3"
    if open_level and spec.open_oracle:
        oracle = spec.open_oracle
    elif level in ("level1", "level2") and spec.listed_oracle:
        oracle = spec.listed_oracle
    else:
        oracle = spec.oracle
    oracle = copy.deepcopy(oracle)
    payload: JsonDict = {
        "id": f"smoke_{spec.tool}_{level}",
        "family": spec.tool,
        "difficulty": level,
        "prompt": spec.open_prompt if open_level else spec.prompt,
        "setup": {
            # "" declares explicitly that the episode starts on a bare
            # workspace.
            "workspace_baseline": BASELINE if level in ("level2", "level3") else "",
            "workspace_backends": list(spec.backends),
            "workspace_skills": list(SKILLS),
            **(
                {"initial_state": copy.deepcopy(spec.initial_state)}
                if spec.initial_state
                else {}
            ),
            "allowed_tools": (
                [spec.tool] if level == "level0" else list(WORKSPACE_TOOL_NAMES)
            ),
        },
        "eval": {
            **copy.deepcopy(spec.success),
            "reference_trace": oracle,
            "max_turns": LEVEL_TURNS[level],
        },
    }
    unknown = set(payload) - TASK_SPEC_FIELDS
    if unknown:
        raise AssertionError(f"smoke task has non-slim fields: {sorted(unknown)}")
    return payload


def build_tasks() -> list[JsonDict]:
    specs = _family_specs()
    if {spec.tool for spec in specs} != set(WORKSPACE_TOOL_NAMES):
        raise AssertionError("smoke families must cover WORKSPACE_TOOL_NAMES exactly")
    specs.sort(key=lambda spec: WORKSPACE_TOOL_NAMES.index(spec.tool))
    return [_level_task(spec, level) for spec in specs for level in LEVELS]


def _baseline_compositions(snapshot: JsonDict) -> dict[str, JsonDict]:
    compositions = snapshot.get("dashboard_compositions", {})
    return {
        dashboard_id: composition
        for dashboard_id, composition in compositions.items()
        # Home and the bare-workspace default are legitimate mutation targets;
        # task-seeded dashboards carry the "Smoke " prefix.
        if composition.get("name") not in ("Home", "Workspace Bench")
        and not str(composition.get("name", "")).startswith("Smoke ")
    }


def certify(tasks: list[JsonDict]) -> None:
    manifest = TaskSuiteManifest.from_dict(MANIFEST_PAYLOAD)
    failures: list[str] = []
    for payload in tasks:
        task_id = str(payload["id"])
        level = str(payload["difficulty"])
        try:
            task = replace(Task.from_dict(payload), suite=manifest)
            episode = WorkspaceEpisode(task)
            baseline_before = _baseline_compositions(episode.initial_snapshot)
            expected_baseline = (
                BASELINE_DASHBOARD_COUNT if level in ("level2", "level3") else 0
            )
            if len(baseline_before) != expected_baseline:
                failures.append(
                    f"{task_id}: expected {expected_baseline} baseline "
                    f"dashboards, found {len(baseline_before)}"
                )
            for call in task.oracle_tool_calls:
                episode.step(call)
            oracle_grade = episode.grade()
            baseline_after = _baseline_compositions(episode.snapshot())
            noop_grade = WorkspaceEpisode(task).grade()
        except Exception as error:  # noqa: BLE001 - report every certification failure.
            failures.append(f"{task_id}: certification raised {error!r}")
            continue
        target_calls = sum(call.name == task.family for call in task.oracle_tool_calls)
        if target_calls != 1:
            failures.append(f"{task_id}: expected one target tool call, found {target_calls}")
        if level == "level0" and len(task.allowed_tools) != 1:
            failures.append(f"{task_id}: level0 must allow exactly the target tool")
        if level != "level0" and set(task.allowed_tools) != set(WORKSPACE_TOOL_NAMES):
            failures.append(f"{task_id}: {level} must allow the full tool surface")
        if not oracle_grade.passed:
            issues = "; ".join(
                f"{issue.code}: {issue.message}" for issue in oracle_grade.issues[:3]
            )
            failures.append(f"{task_id}: oracle failed: {issues}")
        if noop_grade.passed:
            failures.append(f"{task_id}: no-op passed")
        if oracle_grade.checks_total > 6:
            failures.append(
                f"{task_id}: {oracle_grade.checks_total} graded checks exceeds cap 6"
            )
        if baseline_after != baseline_before:
            failures.append(f"{task_id}: oracle mutated a baseline dashboard")
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
        json.dumps(
            {**MANIFEST_PAYLOAD, "content_sha256": task_payload_digest(tasks)},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
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
