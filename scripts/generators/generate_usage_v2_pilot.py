"""Generate and certify the 36-task enterprise-apps-usage-v2 pilot.

The pilot is deliberately small but complete: three operating families, two
monotonic spines per family, and the six usage-v2 difficulty levels.  Every
task starts from the same lived-in workspace and the full four-catalog tool
surface.  The generator owns the private ``pilots/enterprise_apps_usage_v2``
directory and no other generated artifacts.
"""

from __future__ import annotations

import copy
import json
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))

from workspace_bench.agents.base import NoopAgent, OracleAgent  # noqa: E402
from workspace_bench.core.episode import WorkspaceEpisode  # noqa: E402
from workspace_bench.core.models import (  # noqa: E402
    FINAL_ANSWER_TOOL,
    WORKSPACE_TOOL_NAMES,
    JsonDict,
)
from workspace_bench.core.runner import load_task_directory  # noqa: E402
from workspace_bench.core.suite_checks import task_payload_digest  # noqa: E402
from workspace_bench.workspace.simulated_workspace import WORKSPACE_SKILLS  # noqa: E402

OUTPUT_DIR = REPO / "pilots" / "enterprise_apps_usage_v2"
RELATIVE_OUTPUT_DIR = Path("pilots/enterprise_apps_usage_v2")

STARK = "Bench Stark Enterprise"
DALOOPA = "Bench Daloopa"
GETTING_STARTED = "Getting Started"
WIDGET_EXAMPLES = "Widget Examples"

BACKEND_FILES = {
    "stark-enterprise-x": REPO / "src/workspace_bench/data/backends/stark_enterprise_x.json",
    "support-daloopa-skills": (
        REPO / "src/workspace_bench/data/backends/support_daloopa_skills.json"
    ),
    "getting-started": REPO / "src/workspace_bench/data/backends/getting_started.json",
    "widget-examples": REPO / "src/workspace_bench/data/backends/widget_examples.json",
}
BACKEND_ORIGINS = {
    "stark-enterprise-x": STARK,
    "support-daloopa-skills": DALOOPA,
    "getting-started": GETTING_STARTED,
    "widget-examples": WIDGET_EXAMPLES,
}
WORLD_BACKENDS = [
    "stark-enterprise-x",
    "support-daloopa-skills",
    "getting-started",
    "widget-examples",
]
SKILL_SLUGS = sorted(WORKSPACE_SKILLS)
LEVEL_CAPS = {
    "level0": 3,
    "level1": 3,
    "level2": 5,
    "level3": 7,
    "level4": 7,
    "level5": 10,
}

EARNINGS_WIDGET = "earnings_estimates_monitor_calendar_upcoming_earnings"
LIVE_GRID_WIDGET = "live_grid_example"
NAV_EXCEPTIONS_WIDGET = "fund_operations_control_tower_pricing_nav_exceptions"
MANUFACTURER_WIDGET = "company_performance"
TRADE_IDEAS_WIDGET = "portfolio_command_center_actions_trade_ideas"
WHITEPAPERS_WIDGET = "whitepapers"
FIRM_SNAPSHOT_WIDGET = "executive_investment_dashboard_firm_overview_firm_snapshot"
METRIC_WIDGET = "metric_widget"


@dataclass(frozen=True)
class TargetSpec:
    """Internal uniqueness proof for one prompt-targeted widget."""

    backend_slug: str | None
    widget_id: str
    exact_properties: tuple[tuple[str, Any], ...] = ()
    contains_tokens: tuple[str, ...] = ()
    context_terms: tuple[str, ...] = ()
    governed_skill: str | None = None
    custom_backend_name: str | None = None


@dataclass(frozen=True)
class TaskRecord:
    """One authored task plus certification-only metadata."""

    family: str
    payload: JsonDict
    targets: tuple[TargetSpec, ...]
    capability_driven: bool = False


def _call(
    tool: str,
    args: JsonDict,
    *,
    optional: bool = False,
    graded_args: list[str] | None = None,
) -> JsonDict:
    item: JsonDict = {"tool": tool, "args": args}
    if optional:
        item["optional"] = True
    if graded_args is not None:
        item["graded_args"] = graded_args
    return item


def _target(
    backend_slug: str,
    widget_id: str,
    *,
    exact: dict[str, Any] | None = None,
    contains: tuple[str, ...] = (),
    context: tuple[str, ...] = (),
    governed_skill: str | None = None,
) -> TargetSpec:
    return TargetSpec(
        backend_slug=backend_slug,
        widget_id=widget_id,
        exact_properties=tuple((exact or {}).items()),
        contains_tokens=contains,
        context_terms=context,
        governed_skill=governed_skill,
    )


def _custom_target(backend_name: str, widget_id: str, *context: str) -> TargetSpec:
    return TargetSpec(
        backend_slug=None,
        widget_id=widget_id,
        context_terms=tuple(context),
        custom_backend_name=backend_name,
    )


def _required_widget(
    origin: str,
    widget_id: str,
    data_args: JsonDict,
    *,
    tab_id: str | None = None,
) -> JsonDict:
    item: JsonDict = {
        "origin": origin,
        "widget_id": widget_id,
        "data_args": data_args,
    }
    if tab_id is not None:
        item["tab_id"] = tab_id
    return item


def _base_setup(
    *,
    selected_dashboard: str = "Home",
    answer_task: bool = False,
    initial_state: JsonDict | None = None,
) -> JsonDict:
    setup: JsonDict = {
        "workspace_baseline": "stark-workspace-a",
        "workspace_backends": list(WORLD_BACKENDS),
        "workspace_skills": list(SKILL_SLUGS),
        "default_selected_dashboard": selected_dashboard,
        "allowed_tools": [
            *WORKSPACE_TOOL_NAMES,
            *([FINAL_ANSWER_TOOL] if answer_task else []),
        ],
    }
    if initial_state:
        setup["initial_state"] = initial_state
    return setup


def _record(
    family: str,
    task_id: str,
    category: str,
    difficulty: str,
    prompt: str,
    required_tools: list[JsonDict],
    *,
    targets: tuple[TargetSpec, ...],
    required_widgets: list[JsonDict] | None = None,
    required_tabs: list[str] | None = None,
    required_values: list[str] | None = None,
    reference_answer: str | None = None,
    required_widget_defs: list[JsonDict] | None = None,
    required_app_defs: list[JsonDict] | None = None,
    runtime_checks: JsonDict | None = None,
    selected_dashboard: str = "Home",
    initial_state: JsonDict | None = None,
    capability_driven: bool = False,
) -> TaskRecord:
    evaluation: JsonDict = {}
    if required_widgets:
        evaluation["required_widgets"] = required_widgets
    if required_tabs:
        evaluation["required_tabs"] = required_tabs
    evaluation["required_tools"] = required_tools
    if required_values:
        evaluation["required_values_in_answer"] = required_values
    if required_widget_defs:
        evaluation["required_widget_defs"] = required_widget_defs
    if required_app_defs:
        evaluation["required_app_defs"] = required_app_defs
    if runtime_checks:
        evaluation["runtime_checks"] = runtime_checks
    if reference_answer:
        evaluation["reference_answer"] = reference_answer
    evaluation["max_turns"] = len(required_tools) + 3
    payload: JsonDict = {
        "id": task_id,
        "category": category,
        "difficulty": difficulty,
        "prompt": prompt,
        "setup": _base_setup(
            selected_dashboard=selected_dashboard,
            answer_task=bool(required_values),
            initial_state=initial_state,
        ),
        "eval": evaluation,
    }
    return TaskRecord(
        family=family,
        payload=payload,
        targets=targets,
        capability_driven=capability_driven,
    )


def _simple_app(
    name: str,
    tab_id: str,
    placements: list[tuple[str, int, int, int, int, JsonDict]],
) -> JsonDict:
    return {
        "name": name,
        "description": f"Pilot app for {name}.",
        "tabs": {
            tab_id: {
                "id": tab_id,
                "name": tab_id.replace("_", " ").title(),
                "layout": [
                    {
                        "i": widget_id,
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h,
                        "state": {"params": params},
                    }
                    for widget_id, x, y, w, h, params in placements
                ],
            }
        },
        "groups": [],
    }


def _build_retrieve_tasks() -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    earnings_target = _target(
        "stark-enterprise-x",
        EARNINGS_WIDGET,
        exact={"name": "Upcoming Earnings"},
        contains=("Earnings & Estimates Monitor",),
        context=("Upcoming Earnings", "Earnings & Estimates Monitor"),
    )
    daloopa_consensus_target = _target(
        "support-daloopa-skills",
        "daloopa_consensus_estimates",
        exact={"name": "Consensus Estimates"},
        contains=("daloopa_consensus_estimates",),
        context=("earnings-review convention",),
        governed_skill="daloopa-earnings-review",
    )
    tasks.append(
        _record(
            "retrieve",
            "earnings_pulse_level0",
            "read",
            "level0",
            (
                "Give the Earnings & Estimates Monitor's Upcoming Earnings reading for LLY "
                "year to date. Report its exact score and change."
            ),
            [
                _call(
                    "get_widget_data",
                    {
                        "origin": STARK,
                        "widget_id": EARNINGS_WIDGET,
                        "data_args": {
                            "sector": "Healthcare",
                            "ticker": "LLY",
                            "period": "YTD",
                        },
                    },
                )
            ],
            targets=(earnings_target,),
            required_values=["27.63", "0.014"],
            reference_answer="LLY's year-to-date score is 27.63 and its change is 0.014.",
        )
    )
    tasks.append(
        _record(
            "retrieve",
            "earnings_pulse_level1",
            "read",
            "level1",
            (
                "Locate Upcoming Earnings in the Earnings & Estimates Monitor and read the "
                "quarter-to-date AAPL row. Return the exact score and change."
            ),
            [
                _call("list_available_widgets", {"origin": STARK}, optional=True),
                _call(
                    "get_widget_schema",
                    {"origin": STARK, "widget_id": EARNINGS_WIDGET},
                    optional=True,
                ),
                _call(
                    "get_widget_data",
                    {
                        "origin": STARK,
                        "widget_id": EARNINGS_WIDGET,
                        "data_args": {
                            "sector": "Technology",
                            "ticker": "AAPL",
                            "period": "QTD",
                        },
                    },
                ),
            ],
            targets=(earnings_target,),
            required_values=["6.52", "-0.0581"],
            reference_answer="The AAPL row has a score of 6.52 and a change of -0.0581.",
        )
    )
    tasks.append(
        _record(
            "retrieve",
            "earnings_pulse_level2",
            "read",
            "level2",
            (
                "For Apple's current-quarter earnings watch, find the Upcoming Earnings view "
                "in the Earnings & Estimates Monitor and report the exact score and workflow "
                "status. Use the view's declared period choices to interpret current quarter."
            ),
            [
                _call("list_available_widgets", {"origin": STARK}, optional=True),
                _call(
                    "get_widget_schema",
                    {"origin": STARK, "widget_id": EARNINGS_WIDGET},
                    optional=True,
                ),
                _call(
                    "get_params_options",
                    {
                        "origin": STARK,
                        "widget_id": EARNINGS_WIDGET,
                        "param_name": "period",
                    },
                    optional=True,
                ),
                _call(
                    "get_widget_data",
                    {
                        "origin": STARK,
                        "widget_id": EARNINGS_WIDGET,
                        "data_args": {
                            "sector": "Technology",
                            "ticker": "AAPL",
                            "period": "QTD",
                        },
                    },
                ),
            ],
            targets=(earnings_target,),
            required_values=["6.52", "In Review"],
            reference_answer="Apple's current-quarter score is 6.52 and the status is In Review.",
        )
    )
    tasks.append(
        _record(
            "retrieve",
            "earnings_pulse_level3",
            "read",
            "level3",
            (
                "Inspect the lived-in Earnings & Estimates Monitor already open in the "
                "workspace. Using its configured Upcoming Earnings view, report LLY's exact "
                "year-to-date score and status without changing the dashboard."
            ),
            [
                _call("get_workspace_snapshot", {}),
                _call(
                    "get_widget_data",
                    {
                        "origin": STARK,
                        "widget_id": EARNINGS_WIDGET,
                        "data_args": {
                            "sector": "Healthcare",
                            "ticker": "LLY",
                            "period": "YTD",
                        },
                    },
                ),
            ],
            targets=(earnings_target,),
            required_values=["27.63", "Open"],
            reference_answer="The configured LLY view shows a 27.63 score with status Open.",
            selected_dashboard="Earnings & Estimates Monitor",
        )
    )
    tasks.append(
        _record(
            "retrieve",
            "earnings_pulse_level4",
            "read",
            "level4",
            (
                "Apply the desk earnings-review convention for Apple and report the latest "
                "reported quarter's revenue actual and surprise percentage. Follow the "
                "convention's evidence source rather than a general market view."
            ),
            [
                _call("get_skill_content", {"slug": "daloopa-earnings-review"}),
                _call(
                    "get_widget_data",
                    {
                        "origin": DALOOPA,
                        "widget_id": "daloopa_consensus_estimates",
                        "data_args": {"ticker": "AAPL"},
                    },
                ),
            ],
            targets=(daloopa_consensus_target,),
            required_values=["2026Q1", "102070.1", "0.0268"],
            reference_answer=(
                "For 2026Q1, Apple's revenue actual is 102070.1 and the surprise percentage "
                "is 0.0268."
            ),
        )
    )

    earnings_backend = "Pilot Earnings Lookup"
    earnings_widget = "earnings_pulse_lookup"
    earnings_app_name = "Earnings Pulse App"
    earnings_widget_def: JsonDict = {
        "name": "Earnings Pulse Lookup",
        "description": "Latest reported earnings pulse by ticker and calendar period.",
        "endpoint": "/earnings-pulse",
        "type": "table",
        "gridData": {"w": 20, "h": 9},
        "params": [
            {
                "paramName": "ticker",
                "type": "text",
                "label": "Ticker",
                "value": "AAPL",
                "options": [
                    {"label": "Apple", "value": "AAPL"},
                    {"label": "Microsoft", "value": "MSFT"},
                ],
            },
            {
                "paramName": "period",
                "type": "text",
                "label": "Calendar Period",
                "value": "2026Q1",
                "options": [{"label": "2026 Q1", "value": "2026Q1"}],
            },
        ],
    }
    earnings_app = _simple_app(
        earnings_app_name,
        "lookup",
        [(earnings_widget, 0, 0, 20, 9, {"ticker": "AAPL", "period": "2026Q1"})],
    )
    tasks.append(
        _record(
            "retrieve",
            "earnings_pulse_level5",
            "platform",
            "level5",
            (
                "Build a small backend named Pilot Earnings Lookup with an Earnings Pulse "
                "Lookup table for ticker and calendar-period lookups. Wrap it in an Earnings "
                "Pulse App, open the app, read Apple for 2026 Q1, and report the quarter, "
                "actual revenue, and surprise percentage. Keep the definition free of sample "
                "rows."
            ),
            [
                _call(
                    "read_workspace_resource",
                    {"uri": "openbb://workspace/specs/widgets-json"},
                    optional=True,
                ),
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": earnings_backend,
                        "url": "http://127.0.0.1:9401",
                        "widgets_json": {earnings_widget: earnings_widget_def},
                        "apps_json": [earnings_app],
                    },
                    graded_args=["operation", "name"],
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": earnings_app_name,
                        "dashboard_name": "Earnings Pulse Live",
                        "activate": True,
                    },
                    graded_args=["operation", "app_name"],
                ),
                _call(
                    "get_widget_data",
                    {
                        "origin": earnings_backend,
                        "widget_id": earnings_widget,
                        "data_args": {"ticker": "AAPL", "period": "2026Q1"},
                    },
                ),
            ],
            targets=(
                _custom_target(
                    earnings_backend,
                    earnings_widget,
                    "Pilot Earnings Lookup",
                    "Earnings Pulse Lookup",
                ),
            ),
            required_widgets=[
                _required_widget(
                    earnings_backend,
                    earnings_widget,
                    {"ticker": "AAPL", "period": "2026Q1"},
                    tab_id="lookup",
                )
            ],
            required_values=["2026Q1", "102070.1", "0.0268"],
            reference_answer=(
                "The lookup returns 2026Q1, actual revenue 102070.1, and surprise 0.0268."
            ),
            required_widget_defs=[
                {
                    "backend_name": earnings_backend,
                    "widget_id": earnings_widget,
                    "expect": {"type": "table"},
                    "params_include": [
                        {"paramName": "ticker", "type": "text"},
                        {"paramName": "period", "value": "2026Q1"},
                    ],
                }
            ],
            required_app_defs=[
                {
                    "backend_name": earnings_backend,
                    "name_contains": earnings_app_name,
                    "tabs_include": ["lookup"],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [
                        {"tab_id": "lookup", "widget_id": earnings_widget}
                    ],
                }
            ],
            runtime_checks={
                "datasets": [
                    {
                        "name": "pilot-earnings-pulse",
                        "widget_id": earnings_widget,
                        "fields": ["ticker", "period", "actual", "surprise_pct"],
                        "path": "/earnings-pulse",
                        "payload": [
                            {
                                "ticker": "AAPL",
                                "period": "2026Q1",
                                "actual": 102070.1,
                                "surprise_pct": 0.0268,
                            }
                        ],
                    }
                ]
            },
        )
    )

    live_target = _target(
        "widget-examples",
        LIVE_GRID_WIDGET,
        exact={"name": "Live Grid", "wsEndpoint": "ws"},
        context=("live-updating grid", "'ws'"),
    )
    live_args = {"symbol": "MSFT"}
    tasks.append(
        _record(
            "retrieve",
            "negative_live_grid_level0",
            "read",
            "level0",
            (
                "Read Widget Examples' live-updating grid whose stream is labeled 'ws' for "
                "MSFT. State the exact price and change percentage."
            ),
            [
                _call(
                    "get_widget_data",
                    {
                        "origin": WIDGET_EXAMPLES,
                        "widget_id": LIVE_GRID_WIDGET,
                        "data_args": live_args,
                    },
                )
            ],
            targets=(live_target,),
            required_values=["300.0", "-0.12"],
            reference_answer="MSFT's price is 300.0 and its change percentage is -0.12.",
            capability_driven=True,
        )
    )
    tasks.append(
        _record(
            "retrieve",
            "negative_live_grid_level1",
            "read",
            "level1",
            (
                "Find the live-updating grid whose stream is labeled 'ws' and whose Microsoft "
                "sample is down, not the similarly named rising sample. Report Microsoft's "
                "exact price and change percentage."
            ),
            [
                _call("list_available_widgets", {}, optional=True),
                _call(
                    "get_widget_data",
                    {
                        "origin": WIDGET_EXAMPLES,
                        "widget_id": LIVE_GRID_WIDGET,
                        "data_args": live_args,
                    },
                ),
            ],
            targets=(live_target,),
            required_values=["300.0", "-0.12"],
            reference_answer="The down Microsoft sample shows price 300.0 and change -0.12.",
            capability_driven=True,
        )
    )
    tasks.append(
        _record(
            "retrieve",
            "negative_live_grid_level2",
            "read",
            "level2",
            (
                "For Microsoft, use the declared symbol choices to query the live-updating "
                "grid with the short 'ws' stream. Return the exact price and change percentage "
                "from the negative sample."
            ),
            [
                _call(
                    "get_params_options",
                    {
                        "origin": WIDGET_EXAMPLES,
                        "widget_id": LIVE_GRID_WIDGET,
                        "param_name": "symbol",
                    },
                    optional=True,
                ),
                _call(
                    "get_widget_data",
                    {
                        "origin": WIDGET_EXAMPLES,
                        "widget_id": LIVE_GRID_WIDGET,
                        "data_args": live_args,
                    },
                ),
            ],
            targets=(live_target,),
            required_values=["300.0", "-0.12"],
            reference_answer="Microsoft maps to MSFT; the price is 300.0 and change is -0.12.",
            capability_driven=True,
        )
    )
    live_stage: JsonDict = {
        "dashboard": {
            "name": "Live Grid Staging",
            "activate": False,
            "tabs": [{"id": "watch", "name": "Watch"}],
            "widgets": [
                {
                    "origin": WIDGET_EXAMPLES,
                    "widget_id": LIVE_GRID_WIDGET,
                    "tab_id": "watch",
                    "data_args": live_args,
                    "layout": {"x": 0, "y": 0, "w": 20, "h": 9},
                }
            ],
        }
    }
    tasks.append(
        _record(
            "retrieve",
            "negative_live_grid_level3",
            "read",
            "level3",
            (
                "Examine the Live Grid Staging board already configured in the workspace. The "
                "live-updating grid uses the short 'ws' stream; report the exact price and "
                "change percentage for its configured Microsoft sample without altering it."
            ),
            [
                _call("get_workspace_snapshot", {}),
                _call(
                    "get_widget_data",
                    {
                        "origin": WIDGET_EXAMPLES,
                        "widget_id": LIVE_GRID_WIDGET,
                        "data_args": live_args,
                    },
                ),
            ],
            targets=(live_target,),
            required_values=["300.0", "-0.12"],
            reference_answer="The staged Microsoft sample has price 300.0 and change -0.12.",
            selected_dashboard="Live Grid Staging",
            initial_state=live_stage,
            capability_driven=True,
        )
    )
    tasks.append(
        _record(
            "retrieve",
            "negative_live_grid_level4",
            "read",
            "level4",
            (
                "Use the workspace widget-type convention to select the live-updating grid "
                "with stream label 'ws'. For Microsoft, report the exact price and change "
                "percentage from its negative sample."
            ),
            [
                _call(
                    "read_workspace_resource",
                    {"uri": "openbb://workspace/specs/widget-types"},
                ),
                _call("list_available_widgets", {}, optional=True),
                _call(
                    "get_widget_data",
                    {
                        "origin": WIDGET_EXAMPLES,
                        "widget_id": LIVE_GRID_WIDGET,
                        "data_args": live_args,
                    },
                ),
            ],
            targets=(live_target,),
            required_values=["300.0", "-0.12"],
            reference_answer="The qualifying Microsoft row reports 300.0 and -0.12.",
            capability_driven=True,
        )
    )

    live_backend = "Pilot Streaming Lookup"
    live_widget = "msft_stream_lookup"
    live_app_name = "Streaming Pulse App"
    live_widget_def: JsonDict = {
        "name": "Microsoft Stream Lookup",
        "description": "A compact lookup for the requested Microsoft stream sample.",
        "endpoint": "/msft-stream",
        "type": "table",
        "gridData": {"w": 20, "h": 9},
        "params": [
            {
                "paramName": "symbol",
                "type": "text",
                "label": "Symbol",
                "value": "MSFT",
                "options": [{"label": "Microsoft", "value": "MSFT"}],
            }
        ],
    }
    live_app = _simple_app(
        live_app_name,
        "stream",
        [(live_widget, 0, 0, 20, 9, {"symbol": "MSFT"})],
    )
    tasks.append(
        _record(
            "retrieve",
            "negative_live_grid_level5",
            "platform",
            "level5",
            (
                "Author a Pilot Streaming Lookup backend with a Microsoft Stream Lookup table "
                "that serves the requested Microsoft sample, using the examples grid's row "
                "shape. Wrap it in a Streaming Pulse App, open it, read the lookup, and report "
                "the exact price and change percentage. Do not embed sample rows in the widget "
                "definition."
            ),
            [
                _call(
                    "list_available_widgets",
                    {"origin": WIDGET_EXAMPLES},
                    optional=True,
                ),
                _call(
                    "get_widget_schema",
                    {"origin": WIDGET_EXAMPLES, "widget_id": LIVE_GRID_WIDGET},
                    optional=True,
                ),
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": live_backend,
                        "url": "http://127.0.0.1:9402",
                        "widgets_json": {live_widget: live_widget_def},
                        "apps_json": [live_app],
                    },
                    graded_args=["operation", "name"],
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": live_app_name,
                        "dashboard_name": "Streaming Pulse Live",
                        "activate": True,
                    },
                    graded_args=["operation", "app_name"],
                ),
                _call(
                    "get_widget_data",
                    {
                        "origin": live_backend,
                        "widget_id": live_widget,
                        "data_args": {"symbol": "MSFT"},
                    },
                ),
            ],
            targets=(
                _custom_target(
                    live_backend,
                    live_widget,
                    "Pilot Streaming Lookup",
                    "Microsoft Stream Lookup",
                ),
            ),
            required_widgets=[
                _required_widget(
                    live_backend,
                    live_widget,
                    {"symbol": "MSFT"},
                    tab_id="stream",
                )
            ],
            required_values=["300.0", "-0.12"],
            reference_answer="The authored lookup returns price 300.0 and change -0.12.",
            required_widget_defs=[
                {
                    "backend_name": live_backend,
                    "widget_id": live_widget,
                    "expect": {"type": "table"},
                    "params_include": [{"paramName": "symbol", "value": "MSFT"}],
                }
            ],
            required_app_defs=[
                {
                    "backend_name": live_backend,
                    "name_contains": live_app_name,
                    "tabs_include": ["stream"],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [
                        {"tab_id": "stream", "widget_id": live_widget}
                    ],
                }
            ],
            runtime_checks={
                "datasets": [
                    {
                        "name": "pilot-msft-stream",
                        "widget_id": live_widget,
                        "fields": [
                            "symbol",
                            "price",
                            "change",
                            "change_percent",
                            "prev_close",
                            "volume",
                        ],
                        "path": "/msft-stream",
                        "payload": [
                            {
                                "symbol": "MSFT",
                                "price": 300.0,
                                "change": -95.0,
                                "change_percent": -0.12,
                                "prev_close": 305.0,
                                "volume": 1000000,
                            }
                        ],
                    }
                ]
            },
        )
    )
    return tasks


def _build_params_tasks() -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    nav_target = _target(
        "stark-enterprise-x",
        NAV_EXCEPTIONS_WIDGET,
        exact={"name": "NAV Exceptions"},
        contains=("Fund Operations Control Tower",),
        context=("NAV Exceptions", "Fund Operations Control Tower"),
    )
    nav_default = {
        "fund": "Flagship Long/Short",
        "status": "Open",
        "period": "YTD",
    }
    tasks.append(
        _record(
            "params",
            "nav_exception_policy_level0",
            "single-widget",
            "level0",
            (
                "Place Fund Operations Control Tower's NAV Exceptions on Home for Flagship "
                "Long/Short, Open status, and YTD."
            ),
            [
                _call("list_available_widgets", {"origin": STARK}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": NAV_EXCEPTIONS_WIDGET,
                        "data_args": nav_default,
                    },
                ),
            ],
            targets=(nav_target,),
            required_widgets=[
                _required_widget(STARK, NAV_EXCEPTIONS_WIDGET, nav_default)
            ],
        )
    )
    tasks.append(
        _record(
            "params",
            "nav_exception_policy_level1",
            "single-widget",
            "level1",
            (
                "Search the connected catalogs for the Fund Operations Control Tower view of "
                "NAV Exceptions, then add it to Home for Global Opportunities, In Review, "
                "quarter to date."
            ),
            [
                _call("list_available_widgets", {"origin": STARK}, optional=True),
                _call(
                    "get_widget_schema",
                    {"origin": STARK, "widget_id": NAV_EXCEPTIONS_WIDGET},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": NAV_EXCEPTIONS_WIDGET,
                        "data_args": {
                            "fund": "Global Opportunities",
                            "status": "In Review",
                            "period": "QTD",
                        },
                    },
                ),
            ],
            targets=(nav_target,),
            required_widgets=[
                _required_widget(
                    STARK,
                    NAV_EXCEPTIONS_WIDGET,
                    {
                        "fund": "Global Opportunities",
                        "status": "In Review",
                        "period": "QTD",
                    },
                )
            ],
        )
    )
    tasks.append(
        _record(
            "params",
            "nav_exception_policy_level2",
            "single-widget",
            "level2",
            (
                "Set up Fund Operations Control Tower's NAV Exceptions for the flagship book, "
                "limited to only open items for this year. Derive each control value from the "
                "view's available choices and place the result on Home."
            ),
            [
                _call("list_available_widgets", {"origin": STARK}, optional=True),
                _call(
                    "get_widget_schema",
                    {"origin": STARK, "widget_id": NAV_EXCEPTIONS_WIDGET},
                    optional=True,
                ),
                *[
                    _call(
                        "get_params_options",
                        {
                            "origin": STARK,
                            "widget_id": NAV_EXCEPTIONS_WIDGET,
                            "param_name": param,
                        },
                        optional=True,
                    )
                    for param in ("fund", "status", "period")
                ],
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": NAV_EXCEPTIONS_WIDGET,
                        "data_args": nav_default,
                    },
                ),
            ],
            targets=(nav_target,),
            required_widgets=[
                _required_widget(STARK, NAV_EXCEPTIONS_WIDGET, nav_default)
            ],
        )
    )
    tasks.append(
        _record(
            "params",
            "nav_exception_policy_level3",
            "repair",
            "level3",
            (
                "Review the existing NAV Exceptions view on Fund Operations Control Tower's "
                "Pricing tab. Re-scope that exact view for the Global Opportunities quarterly "
                "control meeting, with items still under review, while preserving every other "
                "workspace view."
            ),
            [
                _call("get_workspace_snapshot", {}),
                _call(
                    "update_widget",
                    {
                        "widget_uuid": "widget_206",
                        "data_args": {
                            "fund": "Global Opportunities",
                            "status": "In Review",
                            "period": "QTD",
                        },
                    },
                ),
            ],
            targets=(nav_target,),
            required_widgets=[
                _required_widget(
                    STARK,
                    NAV_EXCEPTIONS_WIDGET,
                    {
                        "fund": "Global Opportunities",
                        "status": "In Review",
                        "period": "QTD",
                    },
                    tab_id="pricing",
                )
            ],
            selected_dashboard="Fund Operations Control Tower",
        )
    )
    daloopa_fundamentals_target = _target(
        "support-daloopa-skills",
        "daloopa_company_fundamentals",
        exact={"name": "Company Fundamentals"},
        contains=("daloopa_company_fundamentals",),
        context=("capital-allocation convention",),
        governed_skill="daloopa-capital-allocation",
    )
    tasks.append(
        _record(
            "params",
            "nav_exception_policy_level4",
            "single-widget",
            "level4",
            (
                "Pair Fund Operations Control Tower's flagship, open, year-to-date NAV "
                "Exceptions with the Apple fundamentals source required by the desk "
                "capital-allocation convention. Use Apple's latest available calendar quarter "
                "and place both views on Home."
            ),
            [
                _call("get_skill_content", {"slug": "daloopa-capital-allocation"}),
                _call(
                    "get_widget_data",
                    {
                        "origin": DALOOPA,
                        "widget_id": "daloopa_company_directory",
                        "data_args": {},
                    },
                ),
                _call("list_available_widgets", {"origin": DALOOPA}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": DALOOPA,
                        "widget_id": "daloopa_company_fundamentals",
                        "data_args": {"ticker": "AAPL", "period": "2026Q1"},
                    },
                ),
                _call("list_available_widgets", {"origin": STARK}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": NAV_EXCEPTIONS_WIDGET,
                        "data_args": nav_default,
                    },
                ),
            ],
            targets=(nav_target, daloopa_fundamentals_target),
            required_widgets=[
                _required_widget(
                    DALOOPA,
                    "daloopa_company_fundamentals",
                    {"ticker": "AAPL", "period": "2026Q1"},
                ),
                _required_widget(STARK, NAV_EXCEPTIONS_WIDGET, nav_default),
            ],
        )
    )

    ops_backend = "Pilot Close Policy"
    ops_widget = "close_policy_exceptions"
    ops_app_name = "Close Policy App"
    ops_widget_def: JsonDict = {
        "name": "Close Policy Exceptions",
        "description": "Exception view whose controls encode the close-desk policy.",
        "endpoint": "/close-policy-exceptions",
        "type": "table",
        "gridData": {"w": 20, "h": 10},
        "params": [
            {
                "paramName": "fund",
                "type": "text",
                "label": "Fund",
                "value": "Flagship Long/Short",
                "options": [
                    {"label": "Flagship Long/Short", "value": "Flagship Long/Short"},
                    {"label": "Global Opportunities", "value": "Global Opportunities"},
                ],
            },
            {
                "paramName": "status",
                "type": "text",
                "label": "Status",
                "value": "Open",
                "options": [
                    {"label": "Open", "value": "Open"},
                    {"label": "In Review", "value": "In Review"},
                ],
            },
            {
                "paramName": "period",
                "type": "text",
                "label": "Period",
                "value": "YTD",
                "options": [
                    {"label": "Year to Date", "value": "YTD"},
                    {"label": "Quarter to Date", "value": "QTD"},
                ],
            },
        ],
    }
    ops_app = _simple_app(
        ops_app_name,
        "exceptions",
        [(ops_widget, 0, 0, 20, 10, nav_default)],
    )
    tasks.append(
        _record(
            "params",
            "nav_exception_policy_level5",
            "platform",
            "level5",
            (
                "Create a Pilot Close Policy backend whose Close Policy Exceptions table "
                "encodes the desk defaults: flagship book, only open items, and this year. "
                "Publish a Close Policy App with the table on an Exceptions tab and leave the "
                "instantiated app open. Use a compact definition with no sample rows."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": ops_backend,
                        "url": "http://127.0.0.1:9403",
                        "widgets_json": {ops_widget: ops_widget_def},
                        "apps_json": [ops_app],
                    },
                    graded_args=["operation", "name"],
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": ops_app_name,
                        "dashboard_name": "Close Policy Live",
                        "activate": True,
                    },
                    graded_args=["operation", "app_name"],
                ),
            ],
            targets=(
                _custom_target(
                    ops_backend,
                    ops_widget,
                    "Pilot Close Policy",
                    "Close Policy Exceptions",
                ),
            ),
            required_widgets=[
                _required_widget(
                    ops_backend,
                    ops_widget,
                    nav_default,
                    tab_id="exceptions",
                )
            ],
            required_widget_defs=[
                {
                    "backend_name": ops_backend,
                    "widget_id": ops_widget,
                    "expect": {"type": "table"},
                    "params_include": [
                        {"paramName": "fund", "value": "Flagship Long/Short"},
                        {"paramName": "status", "value": "Open"},
                        {"paramName": "period", "value": "YTD"},
                    ],
                }
            ],
            required_app_defs=[
                {
                    "backend_name": ops_backend,
                    "name_contains": ops_app_name,
                    "tabs_include": ["exceptions"],
                    "layout_refs_valid": True,
                }
            ],
        )
    )

    manufacturer_target = _target(
        "getting-started",
        MANUFACTURER_WIDGET,
        exact={"name": "Car Manufacturer Performance"},
        context=("performance",),
    )
    tasks.append(
        _record(
            "params",
            "manufacturer_compare_level0",
            "single-widget",
            "level0",
            "Add Car Manufacturer Performance to Home for Toyota and 2024.",
            [
                _call(
                    "list_available_widgets",
                    {"origin": GETTING_STARTED},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": MANUFACTURER_WIDGET,
                        "data_args": {"company": "TM", "year": "2024"},
                    },
                ),
            ],
            targets=(manufacturer_target,),
            required_widgets=[
                _required_widget(
                    GETTING_STARTED,
                    MANUFACTURER_WIDGET,
                    {"company": "TM", "year": "2024"},
                )
            ],
        )
    )
    tasks.append(
        _record(
            "params",
            "manufacturer_compare_level1",
            "single-widget",
            "level1",
            (
                "Browse the parameter-museum catalog for the car-manufacturer performance "
                "view, then place Ford's 2022 result on Home."
            ),
            [
                _call(
                    "list_available_widgets",
                    {"origin": GETTING_STARTED},
                    optional=True,
                ),
                _call(
                    "get_widget_schema",
                    {"origin": GETTING_STARTED, "widget_id": MANUFACTURER_WIDGET},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": MANUFACTURER_WIDGET,
                        "data_args": {"company": "F", "year": "2022"},
                    },
                ),
            ],
            targets=(manufacturer_target,),
            required_widgets=[
                _required_widget(
                    GETTING_STARTED,
                    MANUFACTURER_WIDGET,
                    {"company": "F", "year": "2022"},
                )
            ],
        )
    )
    tasks.append(
        _record(
            "params",
            "manufacturer_compare_level2",
            "single-widget",
            "level2",
            (
                "Configure the car-manufacturer performance view for Volkswagen and the year "
                "immediately before its default year. Resolve both selections from the "
                "declared choices and place it on Home."
            ),
            [
                _call(
                    "list_available_widgets",
                    {"origin": GETTING_STARTED},
                    optional=True,
                ),
                _call(
                    "get_widget_schema",
                    {"origin": GETTING_STARTED, "widget_id": MANUFACTURER_WIDGET},
                    optional=True,
                ),
                _call(
                    "get_params_options",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": MANUFACTURER_WIDGET,
                        "param_name": "company",
                    },
                    optional=True,
                ),
                _call(
                    "get_params_options",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": MANUFACTURER_WIDGET,
                        "param_name": "year",
                    },
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": MANUFACTURER_WIDGET,
                        "data_args": {"company": "VWAGY", "year": "2023"},
                    },
                ),
            ],
            targets=(manufacturer_target,),
            required_widgets=[
                _required_widget(
                    GETTING_STARTED,
                    MANUFACTURER_WIDGET,
                    {"company": "VWAGY", "year": "2023"},
                )
            ],
        )
    )
    manufacturer_stage: JsonDict = {
        "dashboard": {
            "name": "Manufacturer Parameter Staging",
            "activate": False,
            "tabs": [{"id": "comparison", "name": "Comparison"}],
            "widgets": [
                {
                    "origin": GETTING_STARTED,
                    "widget_id": MANUFACTURER_WIDGET,
                    "tab_id": "comparison",
                    "data_args": {"company": "TM", "year": "2024"},
                    "layout": {"x": 0, "y": 0, "w": 20, "h": 10},
                }
            ],
        }
    }
    tasks.append(
        _record(
            "params",
            "manufacturer_compare_level3",
            "repair",
            "level3",
            (
                "Inspect Manufacturer Parameter Staging and correct its existing performance "
                "view to General Motors at the oldest available year. Keep the board and all "
                "unrelated workspace content intact."
            ),
            [
                _call("get_workspace_snapshot", {}),
                _call(
                    "get_params_options",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": MANUFACTURER_WIDGET,
                        "param_name": "year",
                    },
                    optional=True,
                ),
                _call(
                    "update_widget",
                    {
                        "widget_uuid": "widget_333",
                        "data_args": {"company": "GM", "year": "2022"},
                    },
                ),
            ],
            targets=(manufacturer_target,),
            required_widgets=[
                _required_widget(
                    GETTING_STARTED,
                    MANUFACTURER_WIDGET,
                    {"company": "GM", "year": "2022"},
                    tab_id="comparison",
                )
            ],
            selected_dashboard="Manufacturer Parameter Staging",
            initial_state=manufacturer_stage,
        )
    )
    industry_target = _target(
        "support-daloopa-skills",
        "daloopa_company_fundamentals",
        exact={"name": "Company Fundamentals"},
        contains=("daloopa_company_fundamentals",),
        context=("industry-comparison convention",),
        governed_skill="daloopa-industry",
    )
    tasks.append(
        _record(
            "params",
            "manufacturer_compare_level4",
            "single-widget",
            "level4",
            (
                "Continue the manufacturer performance comparison with Toyota in 2024, then "
                "add Microsoft's normalized fundamentals source under the desk "
                "industry-comparison convention at its latest covered calendar quarter. Place "
                "both views on Home."
            ),
            [
                _call("get_skill_content", {"slug": "daloopa-industry"}),
                _call(
                    "get_widget_data",
                    {
                        "origin": DALOOPA,
                        "widget_id": "daloopa_company_directory",
                        "data_args": {},
                    },
                ),
                _call("list_available_widgets", {"origin": DALOOPA}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": DALOOPA,
                        "widget_id": "daloopa_company_fundamentals",
                        "data_args": {"ticker": "MSFT", "period": "2026Q1"},
                    },
                ),
                _call(
                    "list_available_widgets",
                    {"origin": GETTING_STARTED},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": MANUFACTURER_WIDGET,
                        "data_args": {"company": "TM", "year": "2024"},
                    },
                ),
            ],
            targets=(manufacturer_target, industry_target),
            required_widgets=[
                _required_widget(
                    DALOOPA,
                    "daloopa_company_fundamentals",
                    {"ticker": "MSFT", "period": "2026Q1"},
                ),
                _required_widget(
                    GETTING_STARTED,
                    MANUFACTURER_WIDGET,
                    {"company": "TM", "year": "2024"},
                ),
            ],
        )
    )

    compare_backend = "Pilot Manufacturer Policy"
    compare_widget = "manufacturer_policy"
    compare_app_name = "Manufacturer Policy App"
    compare_widget_def: JsonDict = {
        "name": "Manufacturer Policy",
        "description": "Company comparison view with governed manufacturer and year choices.",
        "endpoint": "/manufacturer-policy",
        "type": "table",
        "gridData": {"w": 20, "h": 10},
        "params": [
            {
                "paramName": "company",
                "type": "text",
                "label": "Company",
                "value": "VWAGY",
                "options": [
                    {"label": "Toyota", "value": "TM"},
                    {"label": "Volkswagen", "value": "VWAGY"},
                    {"label": "General Motors", "value": "GM"},
                ],
            },
            {
                "paramName": "year",
                "type": "text",
                "label": "Year",
                "value": "2023",
                "options": [
                    {"label": "2024", "value": "2024"},
                    {"label": "2023", "value": "2023"},
                    {"label": "2022", "value": "2022"},
                ],
            },
        ],
    }
    compare_app = _simple_app(
        compare_app_name,
        "comparison",
        [(compare_widget, 0, 0, 20, 10, {"company": "VWAGY", "year": "2023"})],
    )
    tasks.append(
        _record(
            "params",
            "manufacturer_compare_level5",
            "platform",
            "level5",
            (
                "Build a Pilot Manufacturer Policy backend whose Manufacturer Policy table "
                "offers explicit company and year choices and defaults to Volkswagen in 2023. "
                "Wrap it in a Manufacturer Policy App on a Comparison tab, instantiate it, and "
                "leave it open. The widget definition must not contain sample rows."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": compare_backend,
                        "url": "http://127.0.0.1:9404",
                        "widgets_json": {compare_widget: compare_widget_def},
                        "apps_json": [compare_app],
                    },
                    graded_args=["operation", "name"],
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": compare_app_name,
                        "dashboard_name": "Manufacturer Policy Live",
                        "activate": True,
                    },
                    graded_args=["operation", "app_name"],
                ),
            ],
            targets=(
                _custom_target(
                    compare_backend,
                    compare_widget,
                    "Pilot Manufacturer Policy",
                    "Manufacturer Policy",
                ),
            ),
            required_widgets=[
                _required_widget(
                    compare_backend,
                    compare_widget,
                    {"company": "VWAGY", "year": "2023"},
                    tab_id="comparison",
                )
            ],
            required_widget_defs=[
                {
                    "backend_name": compare_backend,
                    "widget_id": compare_widget,
                    "expect": {"type": "table"},
                    "params_include": [
                        {"paramName": "company", "value": "VWAGY"},
                        {"paramName": "year", "value": "2023"},
                    ],
                }
            ],
            required_app_defs=[
                {
                    "backend_name": compare_backend,
                    "name_contains": compare_app_name,
                    "tabs_include": ["comparison"],
                    "layout_refs_valid": True,
                }
            ],
        )
    )
    return tasks


def _build_curate_tasks() -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    trade_target = _target(
        "stark-enterprise-x",
        TRADE_IDEAS_WIDGET,
        exact={"name": "Trade Ideas"},
        contains=("Portfolio Command Center",),
        context=("Trade Ideas", "Portfolio Command Center"),
    )
    trade_args = {"fund": "Flagship Long/Short", "period": "YTD"}
    tasks.append(
        _record(
            "curate",
            "pm_research_view_level0",
            "dashboard",
            "level0",
            (
                "Put Portfolio Command Center's Trade Ideas on Home for Flagship Long/Short "
                "year to date."
            ),
            [
                _call("list_available_widgets", {"origin": STARK}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": TRADE_IDEAS_WIDGET,
                        "data_args": trade_args,
                    },
                ),
            ],
            targets=(trade_target,),
            required_widgets=[
                _required_widget(STARK, TRADE_IDEAS_WIDGET, trade_args)
            ],
        )
    )
    tasks.append(
        _record(
            "curate",
            "pm_research_view_level1",
            "dashboard",
            "level1",
            (
                "Identify the Portfolio Command Center view that carries actionable trade "
                "ideas, then place its Global Opportunities quarter-to-date configuration on "
                "Home."
            ),
            [
                _call("list_available_widgets", {"origin": STARK}, optional=True),
                _call(
                    "get_widget_schema",
                    {"origin": STARK, "widget_id": TRADE_IDEAS_WIDGET},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": TRADE_IDEAS_WIDGET,
                        "data_args": {
                            "fund": "Global Opportunities",
                            "period": "QTD",
                        },
                    },
                ),
            ],
            targets=(trade_target,),
            required_widgets=[
                _required_widget(
                    STARK,
                    TRADE_IDEAS_WIDGET,
                    {"fund": "Global Opportunities", "period": "QTD"},
                )
            ],
        )
    )
    whitepaper_target = _target(
        "widget-examples",
        WHITEPAPERS_WIDGET,
        exact={"name": "Whitepapers"},
        contains=("bitcoin.pdf", "l1"),
        context=("Bitcoin whitepaper", "layer-one"),
    )
    tasks.append(
        _record(
            "curate",
            "pm_research_view_level2",
            "dashboard",
            "level2",
            (
                "Compose a Home decision view with Portfolio Command Center's Trade Ideas for "
                "the flagship book this year and the multi-file viewer that can place the "
                "Bitcoin whitepaper in its layer-one category. Resolve the catalog controls."
            ),
            [
                _call("list_available_widgets", {"origin": STARK}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": TRADE_IDEAS_WIDGET,
                        "data_args": trade_args,
                    },
                ),
                _call(
                    "list_available_widgets",
                    {"origin": WIDGET_EXAMPLES},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": WIDGET_EXAMPLES,
                        "widget_id": WHITEPAPERS_WIDGET,
                        "data_args": {
                            "filenames": ["bitcoin.pdf"],
                            "category": "l1",
                        },
                    },
                ),
            ],
            targets=(trade_target, whitepaper_target),
            required_widgets=[
                _required_widget(STARK, TRADE_IDEAS_WIDGET, trade_args),
                _required_widget(
                    WIDGET_EXAMPLES,
                    WHITEPAPERS_WIDGET,
                    {"filenames": ["bitcoin.pdf"], "category": "l1"},
                ),
            ],
            capability_driven=True,
        )
    )
    tasks.append(
        _record(
            "curate",
            "pm_research_view_level3",
            "dashboard",
            "level3",
            (
                "Inspect IC Prep - Q3 Review and extend its Evidence tab with the flagship "
                "year-to-date Trade Ideas view from Portfolio Command Center. Preserve its "
                "agenda, evidence widgets, and every other dashboard."
            ),
            [
                _call("get_workspace_snapshot", {}),
                _call(
                    "navigate_workspace",
                    {"operation": "tab", "dashboard_id": "dash_026", "tab_id": "evidence"},
                ),
                _call("list_available_widgets", {"origin": STARK}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": TRADE_IDEAS_WIDGET,
                        "data_args": trade_args,
                    },
                ),
            ],
            targets=(trade_target,),
            required_widgets=[
                _required_widget(
                    STARK,
                    TRADE_IDEAS_WIDGET,
                    trade_args,
                    tab_id="evidence",
                )
            ],
            required_tabs=["evidence"],
            selected_dashboard="IC Prep - Q3 Review",
        )
    )
    guidance_target = _target(
        "support-daloopa-skills",
        "daloopa_management_guidance",
        exact={"name": "Management Guidance"},
        contains=("daloopa_management_guidance",),
        context=("guidance-tracker convention",),
        governed_skill="daloopa-guidance-tracker",
    )
    tasks.append(
        _record(
            "curate",
            "pm_research_view_level4",
            "dashboard",
            "level4",
            (
                "Arrange Home for an Apple review with Portfolio Command Center's flagship "
                "year-to-date Trade Ideas and the governing source required by the desk "
                "guidance-tracker convention. Preserve all unrelated workspace content."
            ),
            [
                _call("get_skill_content", {"slug": "daloopa-guidance-tracker"}),
                _call("list_available_widgets", {"origin": DALOOPA}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": DALOOPA,
                        "widget_id": "daloopa_management_guidance",
                        "data_args": {"ticker": "AAPL"},
                    },
                ),
                _call("list_available_widgets", {"origin": STARK}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": TRADE_IDEAS_WIDGET,
                        "data_args": trade_args,
                    },
                ),
            ],
            targets=(trade_target, guidance_target),
            required_widgets=[
                _required_widget(
                    DALOOPA,
                    "daloopa_management_guidance",
                    {"ticker": "AAPL"},
                ),
                _required_widget(STARK, TRADE_IDEAS_WIDGET, trade_args),
            ],
        )
    )

    pm_backend = "Pilot PM Research"
    pm_app_name = "PM Research Board"
    idea_widget = "idea_queue"
    risk_widget = "risk_snapshot"
    common_params = [
        {
            "paramName": "fund",
            "type": "text",
            "label": "Fund",
            "value": "Flagship Long/Short",
            "options": [
                {"label": "Flagship Long/Short", "value": "Flagship Long/Short"}
            ],
        },
        {
            "paramName": "period",
            "type": "text",
            "label": "Period",
            "value": "YTD",
            "options": [{"label": "Year to Date", "value": "YTD"}],
        },
    ]
    pm_widgets: JsonDict = {
        idea_widget: {
            "name": "Idea Queue",
            "description": "Actionable ideas for the portfolio manager.",
            "endpoint": "/idea-queue",
            "type": "table",
            "gridData": {"w": 24, "h": 10},
            "params": copy.deepcopy(common_params),
        },
        risk_widget: {
            "name": "Risk Snapshot",
            "description": "Compact risk posture for the selected fund and period.",
            "endpoint": "/risk-snapshot",
            "type": "metric",
            "gridData": {"w": 16, "h": 10},
            "params": copy.deepcopy(common_params),
        },
    }
    pm_app = _simple_app(
        pm_app_name,
        "decision",
        [
            (idea_widget, 0, 0, 24, 10, trade_args),
            (risk_widget, 24, 0, 16, 10, trade_args),
        ],
    )
    tasks.append(
        _record(
            "curate",
            "pm_research_view_level5",
            "platform",
            "level5",
            (
                "Author a Pilot PM Research backend with an Idea Queue table and a Risk "
                "Snapshot metric, both governed by flagship-book and year-to-date controls. "
                "Compose them side by side in a PM Research Board Decision tab, publish and "
                "instantiate the app, and leave it open without embedding sample rows."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": pm_backend,
                        "url": "http://127.0.0.1:9405",
                        "widgets_json": pm_widgets,
                        "apps_json": [pm_app],
                    },
                    graded_args=["operation", "name"],
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": pm_app_name,
                        "dashboard_name": "PM Research Live",
                        "activate": True,
                    },
                    graded_args=["operation", "app_name"],
                ),
            ],
            targets=(
                _custom_target(pm_backend, idea_widget, "Pilot PM Research", "Idea Queue"),
                _custom_target(pm_backend, risk_widget, "Risk Snapshot"),
            ),
            required_widgets=[
                _required_widget(
                    pm_backend,
                    idea_widget,
                    trade_args,
                    tab_id="decision",
                ),
                _required_widget(
                    pm_backend,
                    risk_widget,
                    trade_args,
                    tab_id="decision",
                ),
            ],
            required_widget_defs=[
                {
                    "backend_name": pm_backend,
                    "widget_id": idea_widget,
                    "expect": {"type": "table"},
                    "params_include": [{"paramName": "fund"}, {"paramName": "period"}],
                },
                {
                    "backend_name": pm_backend,
                    "widget_id": risk_widget,
                    "expect": {"type": "metric"},
                    "params_include": [{"paramName": "fund"}, {"paramName": "period"}],
                },
            ],
            required_app_defs=[
                {
                    "backend_name": pm_backend,
                    "name_contains": pm_app_name,
                    "tabs_include": ["decision"],
                    "layout_refs_valid": True,
                    "no_overlaps": True,
                }
            ],
        )
    )

    metric_target = _target(
        "getting-started",
        METRIC_WIDGET,
        exact={"name": "Metric Widget"},
        contains=("Total Users",),
        context=("single big-number card", "Total Users"),
    )
    tasks.append(
        _record(
            "curate",
            "capability_card_view_level0",
            "dashboard",
            "level0",
            (
                "Place Getting Started's single big-number card whose first sample is Total "
                "Users on Home."
            ),
            [
                _call(
                    "list_available_widgets",
                    {"origin": GETTING_STARTED},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": METRIC_WIDGET,
                        "data_args": {},
                    },
                ),
            ],
            targets=(metric_target,),
            required_widgets=[
                _required_widget(GETTING_STARTED, METRIC_WIDGET, {})
            ],
            capability_driven=True,
        )
    )
    tasks.append(
        _record(
            "curate",
            "capability_card_view_level1",
            "dashboard",
            "level1",
            (
                "Discover which connected catalog offers the single big-number card whose "
                "leading sample is Total Users, then add that card to Home."
            ),
            [
                _call("list_available_widgets", {}, optional=True),
                _call(
                    "list_available_widgets",
                    {"origin": GETTING_STARTED},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": METRIC_WIDGET,
                        "data_args": {},
                    },
                ),
            ],
            targets=(metric_target,),
            required_widgets=[
                _required_widget(GETTING_STARTED, METRIC_WIDGET, {})
            ],
            capability_driven=True,
        )
    )
    firm_target = _target(
        "stark-enterprise-x",
        FIRM_SNAPSHOT_WIDGET,
        exact={"name": "Firm Snapshot"},
        contains=("Executive Investment Dashboard",),
        context=("firm snapshot",),
    )
    tasks.append(
        _record(
            "curate",
            "capability_card_view_level2",
            "dashboard",
            "level2",
            (
                "Build a Home overview with the Total Users single big-number card beside the "
                "firm snapshot for the global equities strategy this year. Resolve the strategy "
                "and period from the snapshot's declared choices."
            ),
            [
                _call(
                    "list_available_widgets",
                    {"origin": GETTING_STARTED},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": METRIC_WIDGET,
                        "data_args": {},
                    },
                ),
                _call("list_available_widgets", {"origin": STARK}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": FIRM_SNAPSHOT_WIDGET,
                        "data_args": {"strategy": "Global Equities", "period": "YTD"},
                    },
                ),
            ],
            targets=(metric_target, firm_target),
            required_widgets=[
                _required_widget(GETTING_STARTED, METRIC_WIDGET, {}),
                _required_widget(
                    STARK,
                    FIRM_SNAPSHOT_WIDGET,
                    {"strategy": "Global Equities", "period": "YTD"},
                ),
            ],
            capability_driven=True,
        )
    )
    tasks.append(
        _record(
            "curate",
            "capability_card_view_level3",
            "dashboard",
            "level3",
            (
                "Inspect Morning Markets and extend its overview, including the firm snapshot, "
                "with the single big-number card led by Total Users. Keep all four market "
                "widgets, their settings, and every other dashboard unchanged."
            ),
            [
                _call("get_workspace_snapshot", {}),
                _call(
                    "list_available_widgets",
                    {"origin": GETTING_STARTED},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": METRIC_WIDGET,
                        "data_args": {},
                    },
                ),
            ],
            targets=(metric_target, firm_target),
            required_widgets=[
                _required_widget(
                    STARK,
                    FIRM_SNAPSHOT_WIDGET,
                    {"strategy": "Global Equities", "period": "1D"},
                    tab_id="overview",
                ),
                _required_widget(
                    GETTING_STARTED,
                    METRIC_WIDGET,
                    {},
                    tab_id="overview",
                ),
            ],
            selected_dashboard="Morning Markets",
            capability_driven=True,
        )
    )
    stock_target = _target(
        "support-daloopa-skills",
        "daloopa_stock_prices",
        exact={"name": "Stock Prices"},
        contains=("daloopa_stock_prices",),
        context=("tearsheet convention",),
        governed_skill="daloopa-tearsheet",
    )
    fundamentals_target = _target(
        "support-daloopa-skills",
        "daloopa_company_fundamentals",
        exact={"name": "Company Fundamentals"},
        contains=("daloopa_company_fundamentals",),
        context=("tearsheet convention",),
        governed_skill="daloopa-tearsheet",
    )
    tasks.append(
        _record(
            "curate",
            "capability_card_view_level4",
            "dashboard",
            "level4",
            (
                "Extend the Total Users single big-number card with Apple spot-and-revenue "
                "evidence under the desk tearsheet convention. Add the two convention-governed "
                "sources for latest price and latest-quarter fundamentals on Home."
            ),
            [
                _call("get_skill_content", {"slug": "daloopa-tearsheet"}),
                _call("list_available_widgets", {"origin": DALOOPA}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": DALOOPA,
                        "widget_id": "daloopa_stock_prices",
                        "data_args": {"ticker": "AAPL"},
                    },
                ),
                _call(
                    "create_widget",
                    {
                        "origin": DALOOPA,
                        "widget_id": "daloopa_company_fundamentals",
                        "data_args": {"ticker": "AAPL", "period": "2026Q1"},
                    },
                ),
                _call(
                    "list_available_widgets",
                    {"origin": GETTING_STARTED},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": METRIC_WIDGET,
                        "data_args": {},
                    },
                ),
            ],
            targets=(metric_target, stock_target, fundamentals_target),
            required_widgets=[
                _required_widget(
                    DALOOPA,
                    "daloopa_stock_prices",
                    {"ticker": "AAPL"},
                ),
                _required_widget(
                    DALOOPA,
                    "daloopa_company_fundamentals",
                    {"ticker": "AAPL", "period": "2026Q1"},
                ),
                _required_widget(GETTING_STARTED, METRIC_WIDGET, {}),
            ],
        )
    )

    card_backend = "Pilot Capability Cards"
    card_app_name = "Capability Card Board"
    user_card = "user_metric"
    session_card = "session_metric"
    card_widgets: JsonDict = {
        user_card: {
            "name": "User Metric",
            "description": "Single big-number user adoption card.",
            "endpoint": "/user-metric",
            "type": "metric",
            "gridData": {"w": 10, "h": 5},
            "params": [],
        },
        session_card: {
            "name": "Session Metric",
            "description": "Single big-number active-session card.",
            "endpoint": "/session-metric",
            "type": "metric",
            "gridData": {"w": 10, "h": 5},
            "params": [],
        },
    }
    card_app = _simple_app(
        card_app_name,
        "cards",
        [
            (user_card, 0, 0, 10, 5, {}),
            (session_card, 10, 0, 10, 5, {}),
        ],
    )
    tasks.append(
        _record(
            "curate",
            "capability_card_view_level5",
            "platform",
            "level5",
            (
                "Build a Pilot Capability Cards backend with two compact single big-number "
                "widgets: User Metric and Session Metric. Compose them without overlap on a "
                "Cards tab in a Capability Card Board, publish and instantiate the app, and "
                "leave it open. Keep both widget definitions minimal and free of sample rows."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": card_backend,
                        "url": "http://127.0.0.1:9406",
                        "widgets_json": card_widgets,
                        "apps_json": [card_app],
                    },
                    graded_args=["operation", "name"],
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": card_app_name,
                        "dashboard_name": "Capability Cards Live",
                        "activate": True,
                    },
                    graded_args=["operation", "app_name"],
                ),
            ],
            targets=(
                _custom_target(
                    card_backend,
                    user_card,
                    "Pilot Capability Cards",
                    "User Metric",
                ),
                _custom_target(card_backend, session_card, "Session Metric"),
            ),
            required_widgets=[
                _required_widget(card_backend, user_card, {}, tab_id="cards"),
                _required_widget(card_backend, session_card, {}, tab_id="cards"),
            ],
            required_widget_defs=[
                {
                    "backend_name": card_backend,
                    "widget_id": user_card,
                    "expect": {"type": "metric"},
                },
                {
                    "backend_name": card_backend,
                    "widget_id": session_card,
                    "expect": {"type": "metric"},
                },
            ],
            required_app_defs=[
                {
                    "backend_name": card_backend,
                    "name_contains": card_app_name,
                    "tabs_include": ["cards"],
                    "layout_refs_valid": True,
                    "no_overlaps": True,
                }
            ],
        )
    )
    return tasks


def build_tasks() -> list[TaskRecord]:
    """Build the complete deterministic pilot lattice."""

    return [*_build_retrieve_tasks(), *_build_params_tasks(), *_build_curate_tasks()]


def _catalogs() -> dict[str, JsonDict]:
    return {
        slug: json.loads(path.read_text(encoding="utf-8"))
        for slug, path in BACKEND_FILES.items()
    }


def _walk_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        return [item for nested in value.values() for item in _walk_values(nested)]
    if isinstance(value, list):
        return [item for nested in value for item in _walk_values(nested)]
    return [str(value)]


def _semantic_check_count(payload: JsonDict) -> int:
    evaluation = payload["eval"]
    required_tools = evaluation.get("required_tools", [])
    count = sum(not bool(item.get("optional")) for item in required_tools)
    for key in (
        "required_widgets",
        "required_tabs",
        "required_values_in_answer",
        "required_widget_defs",
        "required_app_defs",
    ):
        count += len(evaluation.get(key, []))
    if evaluation.get("runtime_checks"):
        count += len(evaluation["runtime_checks"].get("datasets", []))
    return count


def _assert_target_uniqueness(records: list[TaskRecord], catalogs: dict[str, JsonDict]) -> None:
    all_catalog_ids = {
        widget_id
        for catalog in catalogs.values()
        for widget_id in catalog["widgets"]
    }
    all_origins = set(BACKEND_ORIGINS.values())
    for record in records:
        prompt = str(record.payload["prompt"])
        for target in record.targets:
            if target.backend_slug is None:
                if not target.custom_backend_name:
                    raise AssertionError(f"{record.payload['id']}: custom target lacks backend")
                if target.custom_backend_name in all_origins:
                    raise AssertionError(
                        f"{record.payload['id']}: custom backend collides with mounted origin"
                    )
                if target.widget_id in all_catalog_ids:
                    raise AssertionError(
                        f"{record.payload['id']}: custom widget id collides with mounted catalog"
                    )
                context = prompt.casefold()
                for term in target.context_terms:
                    if term.casefold() not in context:
                        raise AssertionError(
                            f"{record.payload['id']}: prompt omits custom discriminator {term!r}"
                        )
                continue

            catalog = catalogs[target.backend_slug]
            definition = catalog["widgets"].get(target.widget_id)
            if not isinstance(definition, dict):
                raise AssertionError(
                    f"{record.payload['id']}: missing target {target.backend_slug}/{target.widget_id}"
                )
            context = prompt
            if target.governed_skill:
                context += " " + str(WORKSPACE_SKILLS[target.governed_skill]["content"])
            for term in target.context_terms:
                if term.casefold() not in context.casefold():
                    raise AssertionError(
                        f"{record.payload['id']}: prompt/governance omits discriminator {term!r}"
                    )
            candidates: list[tuple[str, str]] = []
            for slug, candidate_catalog in catalogs.items():
                for widget_id, candidate in candidate_catalog["widgets"].items():
                    if not isinstance(candidate, dict):
                        continue
                    if any(candidate.get(key) != expected for key, expected in target.exact_properties):
                        continue
                    document = " ".join(
                        [widget_id, BACKEND_ORIGINS[slug], *_walk_values(candidate)]
                    ).casefold()
                    if all(token.casefold() in document for token in target.contains_tokens):
                        candidates.append((slug, widget_id))
            expected = (target.backend_slug, target.widget_id)
            if candidates != [expected]:
                raise AssertionError(
                    f"{record.payload['id']}: target {expected} is not unique; matches {candidates}"
                )


def _assert_answer_groundedness(
    records: list[TaskRecord], catalogs: dict[str, JsonDict]
) -> None:
    answer_sources = {
        "earnings_pulse_level0": ("stark-enterprise-x", EARNINGS_WIDGET),
        "earnings_pulse_level1": ("stark-enterprise-x", EARNINGS_WIDGET),
        "earnings_pulse_level2": ("stark-enterprise-x", EARNINGS_WIDGET),
        "earnings_pulse_level3": ("stark-enterprise-x", EARNINGS_WIDGET),
        "earnings_pulse_level4": (
            "support-daloopa-skills",
            "daloopa_consensus_estimates",
        ),
        "earnings_pulse_level5": (
            "support-daloopa-skills",
            "daloopa_consensus_estimates",
        ),
        **{
            f"negative_live_grid_level{level}": ("widget-examples", LIVE_GRID_WIDGET)
            for level in range(6)
        },
    }
    for record in records:
        evaluation = record.payload["eval"]
        values = evaluation.get("required_values_in_answer", [])
        if not values:
            continue
        task_id = str(record.payload["id"])
        source_slug, widget_id = answer_sources[task_id]
        definition = catalogs[source_slug]["widgets"][widget_id]
        rows = definition.get("sampleDataByArgs")
        if rows is None:
            rows = definition.get("sampleData")
        if rows is None:
            rows = definition.get("data")
        row_text = json.dumps(rows, ensure_ascii=False)
        reference = str(evaluation.get("reference_answer", ""))
        for token in values:
            if token not in row_text:
                raise AssertionError(
                    f"{task_id}: answer token {token!r} is absent from {source_slug}/{widget_id}"
                )
            if token not in reference:
                raise AssertionError(
                    f"{task_id}: answer token {token!r} is absent from reference_answer"
                )


def validate_payloads(records: list[TaskRecord]) -> dict[str, int]:
    """Run all static design and ownership gates before writing output."""

    if len(records) != 36:
        raise AssertionError(f"expected 36 tasks, built {len(records)}")
    expected_top_keys = {"id", "category", "difficulty", "prompt", "setup", "eval"}
    forbidden = {
        "family",
        "specification_level",
        "fixtures",
        "limits",
        "layout",
        "trace_checks",
        "workspace_checks",
    }
    ids: set[str] = set()
    opening_five: set[tuple[str, ...]] = set()
    levels_by_spine: dict[str, set[str]] = {}
    cap_counts: dict[str, int] = {}
    for record in records:
        payload = record.payload
        task_id = str(payload["id"])
        if set(payload) != expected_top_keys:
            raise AssertionError(f"{task_id}: top-level keys are {sorted(payload)}")
        if forbidden & set(payload):
            raise AssertionError(f"{task_id}: forbidden top-level fields present")
        if task_id in ids:
            raise AssertionError(f"duplicate task id {task_id}")
        ids.add(task_id)
        prompt = str(payload["prompt"])
        if len(prompt.split()) > 120:
            raise AssertionError(f"{task_id}: prompt exceeds 120 words")
        opening = tuple(prompt.casefold().split()[:5])
        if opening in opening_five:
            raise AssertionError(f"{task_id}: duplicate opening five-gram {opening}")
        opening_five.add(opening)
        if any(term in prompt.casefold() for term in ("call ", "widget_id", "json", "tool ")):
            raise AssertionError(f"{task_id}: prompt violates business-language bar")
        setup = payload["setup"]
        if setup["workspace_baseline"] != "stark-workspace-a":
            raise AssertionError(f"{task_id}: wrong baseline")
        if setup["workspace_backends"] != WORLD_BACKENDS:
            raise AssertionError(f"{task_id}: wrong backend world")
        if setup["workspace_skills"] != SKILL_SLUGS:
            raise AssertionError(f"{task_id}: skill slugs are not the sorted full set")
        has_values = bool(payload["eval"].get("required_values_in_answer"))
        expected_tools = [*WORKSPACE_TOOL_NAMES, *([FINAL_ANSWER_TOOL] if has_values else [])]
        if setup["allowed_tools"] != expected_tools:
            raise AssertionError(f"{task_id}: allowed tool surface mismatch")
        required_tools = payload["eval"]["required_tools"]
        if any(item.get("tool") == FINAL_ANSWER_TOOL for item in required_tools):
            raise AssertionError(f"{task_id}: required_tools contains final_answer")
        if payload["eval"]["max_turns"] != len(required_tools) + 3:
            raise AssertionError(f"{task_id}: turn budget mismatch")
        if "sampleData" in json.dumps(payload["eval"], ensure_ascii=False):
            raise AssertionError(f"{task_id}: level payload embeds sampleData")
        level = str(payload["difficulty"])
        check_count = _semantic_check_count(payload)
        cap_counts[task_id] = check_count
        if check_count > LEVEL_CAPS[level]:
            raise AssertionError(
                f"{task_id}: {check_count} authored graded checks exceed {LEVEL_CAPS[level]}"
            )
        spine, parsed_level = task_id.rsplit("_", 1)
        if parsed_level != level:
            raise AssertionError(f"{task_id}: id/difficulty level mismatch")
        levels_by_spine.setdefault(spine, set()).add(level)
    expected_levels = set(LEVEL_CAPS)
    if len(levels_by_spine) != 6 or any(
        levels != expected_levels for levels in levels_by_spine.values()
    ):
        raise AssertionError(f"spine coverage mismatch: {levels_by_spine}")

    family_counts = Counter(record.family for record in records)
    if family_counts != {"retrieve": 12, "params": 12, "curate": 12}:
        raise AssertionError(f"family counts mismatch: {family_counts}")
    non_stark_tasks = sum(
        any(target.backend_slug in {"getting-started", "widget-examples"} for target in record.targets)
        for record in records
    )
    daloopa_tasks = sum(
        any(target.backend_slug == "support-daloopa-skills" for target in record.targets)
        for record in records
    )
    capability_tasks = sum(record.capability_driven for record in records)
    cross_catalog_tasks = sum(
        len({target.backend_slug for target in record.targets if target.backend_slug}) >= 2
        for record in records
    )
    if non_stark_tasks < 10:
        raise AssertionError(f"only {non_stark_tasks} tasks target getting-started/examples")
    if daloopa_tasks < 4:
        raise AssertionError(f"only {daloopa_tasks} tasks target Daloopa")
    if capability_tasks < 3:
        raise AssertionError(f"only {capability_tasks} capability-driven tasks")
    if cross_catalog_tasks < 2:
        raise AssertionError(f"only {cross_catalog_tasks} cross-catalog compositions")

    catalogs = _catalogs()
    _assert_target_uniqueness(records, catalogs)
    _assert_answer_groundedness(records, catalogs)
    return {
        "getting_started_or_examples": non_stark_tasks,
        "daloopa": daloopa_tasks,
        "capability_driven": capability_tasks,
        "cross_catalog": cross_catalog_tasks,
        "max_authored_checks": max(cap_counts.values()),
    }


def _manifest(records: list[TaskRecord]) -> JsonDict:
    payloads = [record.payload for record in records]
    return {
        "suite_id": "enterprise-apps-usage-v2",
        "visibility": "private",
        "task_defaults": {
            "eval": {
                "layout": {"within_grid": True, "no_overlaps": True, "grid_width": 40},
                "trace_checks": {
                    "max_invalid_tool_calls": 1,
                    "forbid_invented_widget_ids": True,
                },
                "workspace_checks": {"preserve_other_dashboards": True},
            }
        },
        "content_sha256": task_payload_digest(payloads),
        "description": (
            "A 36-task pilot for operating, governing, and authoring in a lived-in "
            "multi-catalog enterprise workspace."
        ),
    }


def _readme() -> str:
    return """# Enterprise Apps Usage v2 Pilot

This pilot measures operating a lived-in, four-catalog enterprise workspace through six
contained levels: execute, discover, translate, ambient state, governed knowledge, and build.

| Level | Driver | Proof |
| --- | --- | --- |
| level0 | Execute | Perform the stated business action. |
| level1 | Discover | Find the business object among all mounted catalogs. |
| level2 | Translate | Convert business policy into declared parameter values. |
| level3 | Ambient | Inspect and safely extend or repair lived-in state. |
| level4 | Knowledge-governed | Follow a workspace skill or resource. |
| level5 | Build | Author, wrap, instantiate, and use a custom backend. |

Tasks: 36
"""


def write_suite(records: list[TaskRecord]) -> None:
    """Write only the pilot-owned output directory."""

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    for family in ("retrieve", "params", "curate"):
        (OUTPUT_DIR / family).mkdir(parents=True, exist_ok=True)
    for record in records:
        task_id = str(record.payload["id"])
        path = OUTPUT_DIR / record.family / f"{task_id}.json"
        path.write_text(json.dumps(record.payload, indent=2) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "task_suite.json").write_text(
        json.dumps(_manifest(records), indent=2) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / "README.md").write_text(_readme(), encoding="utf-8")


def certify_loaded_suite(records: list[TaskRecord]) -> dict[str, int]:
    """Replay the loaded suite with the oracle and prove every no-op fails."""

    if Path.cwd().resolve() != REPO:
        raise RuntimeError(f"run this generator from repository root {REPO}")
    tasks = load_task_directory(RELATIVE_OUTPUT_DIR)
    if len(tasks) != len(records):
        raise AssertionError(f"loader returned {len(tasks)} tasks, expected {len(records)}")
    oracle = OracleAgent()
    noop = NoopAgent()
    oracle_pass = 0
    noop_fail = 0
    for index, task in enumerate(tasks, start=1):
        print(f"[certify {index:02d}/36] {task.family}/{task.id}", flush=True)
        oracle_episode = WorkspaceEpisode(task)
        for call in oracle.tool_calls(task):
            oracle_episode.step(call)
        oracle_grade = oracle_episode.grade()
        if not oracle_grade.passed:
            issues = "; ".join(
                f"{issue.code}: {issue.message}" for issue in oracle_grade.issues[:5]
            )
            raise RuntimeError(f"{task.id}: oracle failed: {issues}")
        oracle_pass += 1

        noop_episode = WorkspaceEpisode(task)
        for call in noop.tool_calls(task):
            noop_episode.step(call)
        if noop_episode.grade().passed:
            raise RuntimeError(f"{task.id}: no-op agent passed")
        noop_fail += 1
    return {"oracle_pass": oracle_pass, "noop_fail": noop_fail}


def main() -> int:
    print("[1/4] Authoring the 3-family x 2-spine x 6-level pilot", flush=True)
    records = build_tasks()
    print("[2/4] Running static caps, coverage, uniqueness, and groundedness gates", flush=True)
    static_summary = validate_payloads(records)
    print("[3/4] Writing the private pilot and loading it through the harness", flush=True)
    write_suite(records)
    print("[4/4] Replaying oracle and no-op certification", flush=True)
    replay_summary = certify_loaded_suite(records)
    print(
        "PILOT DONE — "
        f"{replay_summary['oracle_pass']}/36 oracle pass, "
        f"{replay_summary['noop_fail']}/36 noop fail; "
        f"caps pass (max authored checks {static_summary['max_authored_checks']}/10); "
        "uniqueness pass; groundedness pass; "
        f"targets: {static_summary['getting_started_or_examples']} getting-started/examples, "
        f"{static_summary['daloopa']} Daloopa, "
        f"{static_summary['capability_driven']} capability-driven, "
        f"{static_summary['cross_catalog']} cross-catalog.",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
