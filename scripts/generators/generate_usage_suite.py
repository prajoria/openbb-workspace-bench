"""Generate and certify the 192-task usage-v3 wave-1 through wave-3 suite.

The first two waves have one coherent spine per family; wave 3 adds two more
spines to each of eight job-shaped families.  Most
spines follow the level0 execute, level1 discover, level2 translate, level3
ambient, level4 governed/multi-intent, level5 build ladder exactly.  The
honest deviations required by the brief are:

* parameterize level5 is a three-widget surgery rather than fresh authoring,
  because every parameterize rung must mutate existing widgets;
* repair level5 rebuilds an already-authored backend through refresh rather
  than adding a new backend;
* handoff level5 builds and instantiates a minimal authored app before
  documenting and delegating its follow-up.

The generator owns the enterprise-apps-usage suite directory and this file.  Its static
certificate mechanically enforces F1-F11 and L1-L5 across all three waves,
including per-value provenance for every synthesized graded call argument and
every required-widget data value.
"""

from __future__ import annotations

import copy
import json
import re
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass, field
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
from workspace_bench.workspace.simulated_workspace import (  # noqa: E402
    LIVE_WORKSPACE_RESOURCES,
    WORKSPACE_PROMPTS,
    WORKSPACE_SKILLS,
)

OUTPUT_DIR = REPO / "src" / "workspace_bench" / "task_suites" / "enterprise_apps_usage"
RELATIVE_OUTPUT_DIR = Path("src/workspace_bench/task_suites/enterprise_apps_usage")

STARK = "Bench Stark Enterprise"
DALOOPA = "Bench Daloopa"
GETTING_STARTED = "Getting Started"
WIDGET_EXAMPLES = "Widget Examples"

BACKEND_FILES = {
    "stark-enterprise-x": (REPO / "src/workspace_bench/data/backends/stark_enterprise_x.json"),
    "support-daloopa-skills": (
        REPO / "src/workspace_bench/data/backends/support_daloopa_skills.json"
    ),
    "getting-started": (REPO / "src/workspace_bench/data/backends/getting_started.json"),
    "widget-examples": (REPO / "src/workspace_bench/data/backends/widget_examples.json"),
}
BACKEND_ORIGINS = {
    "stark-enterprise-x": STARK,
    "support-daloopa-skills": DALOOPA,
    "getting-started": GETTING_STARTED,
    "widget-examples": WIDGET_EXAMPLES,
}
ORIGIN_SLUGS = {origin: slug for slug, origin in BACKEND_ORIGINS.items()}
WORLD_BACKENDS = list(BACKEND_FILES)
SKILL_SLUGS = sorted(WORKSPACE_SKILLS)
LEVEL_CAPS = {
    "level0": 3,
    "level1": 3,
    "level2": 5,
    "level3": 7,
    "level4": 7,
    "level5": 10,
}
FAMILY_LEVELS = {
    "retrieve": tuple(f"level{level}" for level in range(6)),
    "curate": tuple(f"level{level}" for level in range(6)),
    "parameterize": tuple(f"level{level}" for level in range(6)),
    "organize": tuple(f"level{level}" for level in range(6)),
    "repair": tuple(f"level{level}" for level in range(6)),
    "platform": tuple(f"level{level}" for level in range(6)),
    "extend": tuple(f"level{level}" for level in range(6)),
    "handoff": tuple(f"level{level}" for level in range(6)),
}

EARNINGS_WIDGET = "earnings_estimates_monitor_calendar_upcoming_earnings"
TRADE_IDEAS_WIDGET = "portfolio_command_center_actions_trade_ideas"
NAV_EXCEPTIONS_WIDGET = "fund_operations_control_tower_pricing_nav_exceptions"
MANUFACTURER_WIDGET = "company_performance"
METRIC_WIDGET = "metric_widget"
DALOOPA_STOCK_PRICES_WIDGET = "daloopa_stock_prices"
DALOOPA_DIRECTORY_WIDGET = "daloopa_company_directory"
DALOOPA_GUIDANCE_WIDGET = "daloopa_management_guidance"
DALOOPA_FUNDAMENTALS_WIDGET = "daloopa_company_fundamentals"
LIVE_GRID_WIDGET = "live_grid_data"
SPARKLINE_WIDGET = "sparkline_line"
RATIO_TABS_WIDGET = "tabs_with_dropdown"
WHITEPAPERS_WIDGET = "whitepapers"
COINDESK_WIDGET = "coindesk_news"
MULTI_PDF_WIDGET = "multi_pdf_base64"
COMPANY_DETAILS_WIDGET = "company_details"
MARKDOWN_WIDGET = "markdown_widget"
NEWSFEED_WIDGET = "sample_newsfeed"

WAVE1_SPINES = {
    "earnings_lookup",
    "decision_briefing",
    "technology_decision_inputs",
    "committee_navigation",
    "nav_exception_station",
    "governed_earnings_brief",
    "risk_service_lifecycle",
    "earnings_handoff",
}
WAVE2_SPINES = {
    "closing_tape_lookup",
    "market_telemetry",
    "crypto_document_controls",
    "client_onboarding_flow",
    "manufacturer_details_repair",
    "cited_research_operations",
    "research_feed_lifecycle",
    "news_desk_handoff",
}
WAVE3_SPINES = {
    "operating_driver_lookup",
    "live_quote_lookup",
    "compliance_alert_review",
    "execution_quality_review",
    "client_intake_controls",
    "crypto_display_controls",
    "due_diligence_media_room",
    "visualization_gallery",
    "vendor_freshness_repair",
    "protocol_display_repair",
    "comps_governance",
    "investment_snapshot_governance",
    "inflection_service_lifecycle",
    "guidance_service_lifecycle",
    "segment_mix_handoff",
    "consensus_exception_handoff",
}
WAVE3_SPINE_FAMILIES = {
    "operating_driver_lookup": "retrieve",
    "live_quote_lookup": "retrieve",
    "compliance_alert_review": "curate",
    "execution_quality_review": "curate",
    "client_intake_controls": "parameterize",
    "crypto_display_controls": "parameterize",
    "due_diligence_media_room": "organize",
    "visualization_gallery": "organize",
    "vendor_freshness_repair": "repair",
    "protocol_display_repair": "repair",
    "comps_governance": "platform",
    "investment_snapshot_governance": "platform",
    "inflection_service_lifecycle": "extend",
    "guidance_service_lifecycle": "extend",
    "segment_mix_handoff": "handoff",
    "consensus_exception_handoff": "handoff",
}
WAVE3_BUSINESS_THEMES = {
    "operating_driver_lookup": "operating driver history",
    "live_quote_lookup": "live equity quote",
    "compliance_alert_review": "compliance alert triage",
    "execution_quality_review": "execution venue quality",
    "client_intake_controls": "client intake submission",
    "crypto_display_controls": "crypto display tuning",
    "due_diligence_media_room": "due diligence media room",
    "visualization_gallery": "visualization gallery",
    "vendor_freshness_repair": "vendor freshness incident",
    "protocol_display_repair": "protocol display recovery",
    "comps_governance": "comparable company review",
    "investment_snapshot_governance": "investment snapshot review",
    "inflection_service_lifecycle": "growth inflection service",
    "guidance_service_lifecycle": "guidance evidence service",
    "segment_mix_handoff": "segment mix escalation",
    "consensus_exception_handoff": "consensus exception escalation",
}
LEGACY_BUSINESS_THEMES = {
    "earnings lookup",
    "decision briefing",
    "technology decision inputs",
    "committee navigation",
    "nav exception station",
    "governed earnings brief",
    "risk service lifecycle",
    "earnings handoff",
    "closing tape lookup",
    "market telemetry",
    "crypto document controls",
    "client onboarding flow",
    "manufacturer details repair",
    "cited research operations",
    "research feed lifecycle",
    "news desk handoff",
}

DISCOVERY_TOOLS = {
    "get_workspace_snapshot",
    "list_available_widgets",
    "get_widget_schema",
    "get_params_options",
}
PROMPT_FORBIDDEN = {
    *WORKSPACE_TOOL_NAMES,
    "final_answer",
    "widget_id",
    "backend_id",
    "dashboard_id",
    "tab_id",
    "json payload",
}


@dataclass(frozen=True)
class PolicyMapping:
    """A prompt-stated policy phrase and the exact values it translates to."""

    words: str
    values: tuple[Any, ...]


@dataclass(frozen=True)
class TargetSpec:
    """One catalog or custom widget targeted by a task prompt."""

    origin: str
    widget_id: str
    display_name: str
    discriminators: tuple[str, ...]
    staged: bool = False
    custom: bool = False


@dataclass(frozen=True)
class GroundedGenerated:
    """A generated-widget fact set and its served catalog source."""

    backend_slug: str
    widget_id: str
    tokens: tuple[str, ...]


@dataclass(frozen=True)
class GovernanceSpec:
    """A named knowledge source and tokens that govern a graded outcome."""

    tool: str
    key: str
    label: str
    outcome_tokens: tuple[str, ...]


@dataclass(frozen=True)
class TaskRecord:
    """One task plus certification-only fairness metadata."""

    family: str
    payload: JsonDict
    targets: tuple[TargetSpec, ...] = ()
    policies: tuple[PolicyMapping, ...] = ()
    pinned_widget_args: dict[tuple[str, str], frozenset[str]] = field(default_factory=dict)
    answer_source: tuple[str, str] | None = None
    grounded_generated: tuple[GroundedGenerated, ...] = ()
    governance: GovernanceSpec | None = None


def _call(
    tool: str,
    args: JsonDict,
    *,
    optional: bool = False,
    graded_args: tuple[str, ...] | None = None,
) -> JsonDict:
    item: JsonDict = {"tool": tool, "args": args}
    if optional:
        item["optional"] = True
    elif graded_args is None:
        raise ValueError(f"graded call {tool} needs explicit non-empty graded_args")
    elif not graded_args:
        if tool != "assign_tasks_to_agents":
            raise ValueError(f"graded call {tool} needs explicit non-empty graded_args")
        # Level-5 handoffs grade that delegation happened, while the authored
        # artifact checks grade the durable handoff content. Agent routing is
        # intentionally not coupled to an echoed task-request payload.
        item["graded_args"] = []
    else:
        item["graded_args"] = list(graded_args)
    return item


def _snapshot() -> JsonDict:
    return _call("get_workspace_snapshot", {}, optional=True)


def _target(
    origin: str,
    widget_id: str,
    display_name: str,
    *discriminators: str,
    staged: bool = False,
) -> TargetSpec:
    return TargetSpec(
        origin=origin,
        widget_id=widget_id,
        display_name=display_name,
        discriminators=tuple(discriminators or (origin, display_name)),
        staged=staged,
    )


def _custom_target(
    origin: str,
    widget_id: str,
    display_name: str,
    *discriminators: str,
    staged: bool = False,
) -> TargetSpec:
    return TargetSpec(
        origin=origin,
        widget_id=widget_id,
        display_name=display_name,
        discriminators=tuple(discriminators or (origin, display_name)),
        staged=staged,
        custom=True,
    )


def _required_widget(
    origin: str,
    widget_id: str,
    data_args: JsonDict | None = None,
    *,
    tab_id: str | None = None,
    min_count: int | None = None,
    max_count: int | None = None,
) -> JsonDict:
    item: JsonDict = {"origin": origin, "widget_id": widget_id}
    if data_args:
        item["data_args"] = data_args
    if tab_id is not None:
        item["tab_id"] = tab_id
    if min_count is not None:
        item["min_count"] = min_count
    if max_count is not None:
        item["max_count"] = max_count
    return item


def _widget_def(
    name: str,
    endpoint: str,
    *,
    widget_type: str = "table",
    description: str | None = None,
    params: list[JsonDict] | None = None,
    grid: tuple[int, int] = (20, 10),
) -> JsonDict:
    definition: JsonDict = {
        "name": name,
        "description": description or f"Wave-1 view for {name}.",
        "endpoint": endpoint,
        "type": widget_type,
        "gridData": {"w": grid[0], "h": grid[1]},
    }
    if params:
        definition["params"] = params
    return definition


def _app(
    name: str,
    tabs: list[tuple[str, str, list[tuple[str, int, int, int, int, JsonDict | None]]]],
) -> JsonDict:
    return {
        "name": name,
        "description": f"Wave-1 authored app for {name}.",
        "tabs": {
            tab_id: {
                "id": tab_id,
                "name": tab_name,
                "layout": [
                    {
                        "i": widget_id,
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h,
                        **({"state": {"params": params}} if params else {}),
                    }
                    for widget_id, x, y, w, h, params in placements
                ],
            }
            for tab_id, tab_name, placements in tabs
        },
    }


def _staged_dashboard(
    name: str,
    widgets: list[JsonDict],
    *,
    tabs: list[JsonDict] | None = None,
    dashboard_id: str | None = None,
    generated_widgets: list[JsonDict] | None = None,
) -> JsonDict:
    dashboard: JsonDict = {
        "name": name,
        "activate": False,
        "tabs": tabs or [{"id": "review", "name": "Review"}],
        "widgets": widgets,
    }
    if dashboard_id:
        dashboard["dashboard_id"] = dashboard_id
    if generated_widgets:
        dashboard["generated_widgets"] = generated_widgets
    return {"dashboard": dashboard}


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
    spine: str,
    level: int,
    category: str,
    prompt: str,
    required_tools: list[JsonDict],
    *,
    targets: tuple[TargetSpec, ...] = (),
    policies: tuple[PolicyMapping, ...] = (),
    pinned_widget_args: dict[tuple[str, str], frozenset[str]] | None = None,
    required_widgets: list[JsonDict] | None = None,
    required_tabs: list[str] | None = None,
    required_dashboard_name: str | None = None,
    required_values: list[str] | None = None,
    required_generated_widgets: list[JsonDict] | None = None,
    required_widget_defs: list[JsonDict] | None = None,
    required_app_defs: list[JsonDict] | None = None,
    runtime_checks: JsonDict | None = None,
    reference_answer: str | None = None,
    answer_source: tuple[str, str] | None = None,
    grounded_generated: tuple[GroundedGenerated, ...] = (),
    governance: GovernanceSpec | None = None,
    selected_dashboard: str = "Home",
    initial_state: JsonDict | None = None,
) -> TaskRecord:
    difficulty = f"level{level}"
    evaluation: JsonDict = {"required_tools": required_tools}
    if required_widgets:
        evaluation["required_widgets"] = required_widgets
    if required_tabs:
        evaluation["required_tabs"] = required_tabs
    if required_dashboard_name:
        evaluation["required_dashboard_name_contains"] = required_dashboard_name
    if required_values:
        evaluation["required_values_in_answer"] = required_values
    if required_generated_widgets:
        evaluation["required_generated_widgets"] = required_generated_widgets
    if required_widget_defs:
        evaluation["required_widget_defs"] = required_widget_defs
    if required_app_defs:
        evaluation["required_app_defs"] = required_app_defs
    if runtime_checks:
        evaluation["runtime_checks"] = runtime_checks
    if reference_answer:
        evaluation["reference_answer"] = reference_answer
    if level >= 4:
        # Deep-rung chains carry legitimate overhead the graded reference
        # cannot model (orientation, template discovery before instantiate).
        # Optional steps keep the replay honest and grow the budget through
        # the same ref+3 rule; without them a real agent is turn-starved.
        if not (required_tools and required_tools[0]["tool"] == "get_workspace_snapshot"):
            required_tools = [_snapshot(), *required_tools]
        for index, step in enumerate(required_tools):
            if step["tool"] == "manage_apps" and not step.get("optional"):
                required_tools = [
                    *required_tools[:index],
                    _call("manage_apps", {"operation": "list"}, optional=True),
                    *required_tools[index:],
                ]
                break
        evaluation["required_tools"] = required_tools
    evaluation["max_turns"] = len(required_tools) + 3
    payload: JsonDict = {
        "id": f"{spine}_{difficulty}",
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
        policies=policies,
        pinned_widget_args=pinned_widget_args or {},
        answer_source=answer_source,
        grounded_generated=grounded_generated,
        governance=governance,
    )


def _earnings_target(*, staged: bool = False) -> TargetSpec:
    return _target(
        STARK,
        EARNINGS_WIDGET,
        "Upcoming Earnings",
        "Earnings & Estimates Monitor",
        "Upcoming Earnings",
        staged=staged,
    )


def _manufacturer_target(*, staged: bool = False) -> TargetSpec:
    return _target(
        GETTING_STARTED,
        MANUFACTURER_WIDGET,
        "Car Manufacturer Performance",
        staged=staged,
    )


def _trade_target(*, staged: bool = False) -> TargetSpec:
    return _target(
        STARK,
        TRADE_IDEAS_WIDGET,
        "Trade Ideas",
        "Portfolio Command Center",
        "Trade Ideas",
        staged=staged,
    )


def _nav_target(*, staged: bool = False) -> TargetSpec:
    return _target(
        STARK,
        NAV_EXCEPTIONS_WIDGET,
        "NAV Exceptions",
        "Fund Operations Control Tower",
        "NAV Exceptions",
        staged=staged,
    )


def _build_retrieve_tasks() -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    spine = "earnings_lookup"
    rows = (
        (
            0,
            "Read Upcoming Earnings in Bench Stark Enterprise's Earnings & Estimates "
            "Monitor for Healthcare, LLY, and YTD, and report the exact score and status.",
            {"sector": "Healthcare", "ticker": "LLY", "period": "YTD"},
            ["27.63", "Open"],
            "The LLY YTD score is 27.63 and its status is Open.",
        ),
        (
            1,
            "Find Upcoming Earnings in Bench Stark Enterprise's Earnings & Estimates "
            "Monitor, set the view to Technology, AAPL, and QTD, and give me the exact "
            "score and status.",
            {"sector": "Technology", "ticker": "AAPL", "period": "QTD"},
            ["6.52", "In Review"],
            "The AAPL QTD score is 6.52 and its status is In Review.",
        ),
    )
    for level, prompt, data_args, values, answer in rows:
        tools = [_snapshot()]
        if level == 1:
            tools.extend(
                [
                    _call(
                        "list_available_widgets",
                        {"origin": STARK},
                        optional=True,
                    ),
                    _call(
                        "get_widget_schema",
                        {"origin": STARK, "widget_id": EARNINGS_WIDGET},
                        optional=True,
                    ),
                ]
            )
        tools.append(
            _call(
                "get_widget_data",
                {
                    "origin": STARK,
                    "widget_id": EARNINGS_WIDGET,
                    "data_args": data_args,
                },
                graded_args=("origin", "widget_id"),
            )
        )
        tasks.append(
            _record(
                "retrieve",
                spine,
                level,
                "read",
                prompt,
                tools,
                targets=(_earnings_target(),),
                required_values=values,
                reference_answer=answer,
                answer_source=("stark-enterprise-x", EARNINGS_WIDGET),
            )
        )

    tasks.append(
        _record(
            "retrieve",
            spine,
            2,
            "read",
            (
                "I need MSFT's exact score and status from Upcoming Earnings in Bench "
                "Stark Enterprise's Earnings & Estimates Monitor. Use Technology for "
                "the coverage sector; the current-month policy means MTD."
            ),
            [
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
                            "ticker": "MSFT",
                            "period": "MTD",
                        },
                    },
                    graded_args=("origin", "widget_id"),
                ),
            ],
            targets=(_earnings_target(),),
            policies=(PolicyMapping("current-month policy", ("MTD",)),),
            required_values=["89.94", "Escalated"],
            reference_answer=("The MSFT MTD score is 89.94 and its status is Escalated."),
            answer_source=("stark-enterprise-x", EARNINGS_WIDGET),
        )
    )
    tasks.append(
        _record(
            "retrieve",
            spine,
            3,
            "read",
            (
                "On the open Earnings & Estimates Monitor board, read Bench Stark "
                "Enterprise's configured Upcoming Earnings view without changing it, and "
                "report LLY's exact YTD score and change."
            ),
            [
                _snapshot(),
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
                    graded_args=("origin", "widget_id"),
                ),
            ],
            targets=(_earnings_target(staged=True),),
            required_values=["27.63", "0.014"],
            reference_answer="LLY's YTD score is 27.63 and its change is 0.014.",
            answer_source=("stark-enterprise-x", EARNINGS_WIDGET),
            selected_dashboard="Earnings & Estimates Monitor",
        )
    )
    tasks.append(
        _record(
            "retrieve",
            spine,
            4,
            "read",
            (
                "Review Apple's earnings under Finance Earnings Prep governance. In "
                "Bench Stark Enterprise's Earnings & Estimates Monitor, use Upcoming "
                "Earnings for Technology, AAPL, and QTD, then report the exact score and "
                "status."
            ),
            [
                _call(
                    "get_skill_content",
                    {"slug": "finance-earnings-prep"},
                    graded_args=("slug",),
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
                    graded_args=("origin", "widget_id"),
                ),
            ],
            targets=(_earnings_target(),),
            policies=(
                PolicyMapping("Finance Earnings Prep governance", ("finance-earnings-prep",)),
            ),
            required_values=["6.52", "In Review"],
            reference_answer=("The governed AAPL QTD view shows 6.52 with status In Review."),
            answer_source=("stark-enterprise-x", EARNINGS_WIDGET),
        )
    )

    backend_name = "Wave One Earnings Lookup"
    widget_name = "Earnings Status Lookup"
    widget_id = "earnings_status_lookup"
    app_name = "Earnings Lookup App"
    params = [
        {
            "paramName": "ticker",
            "type": "text",
            "label": "Ticker",
            "value": "LLY",
            "options": [{"label": "LLY", "value": "LLY"}],
        },
        {
            "paramName": "period",
            "type": "text",
            "label": "Period",
            "value": "YTD",
            "options": [{"label": "YTD", "value": "YTD"}],
        },
    ]
    widget_def = _widget_def(
        widget_name,
        "/earnings-status",
        description="Lookup for a catalog capability not otherwise served.",
        params=params,
    )
    app_def = _app(
        app_name,
        [("lookup", "Lookup", [(widget_id, 0, 0, 20, 10, {"ticker": "LLY", "period": "YTD"})])],
    )
    tasks.append(
        _record(
            "retrieve",
            spine,
            5,
            "platform",
            (
                "The desk needs a Wave One Earnings Lookup backend with an Earnings Status "
                "Lookup table for LLY and YTD. Build and add it, instantiate its Earnings Lookup "
                "App, read the lookup, and report the exact score and status. Follow the "
                "widgets manifest specification. Widget ids are the snake_case of widget "
                "names; tab ids are the snake_case of tab names."
            ),
            [
                _call(
                    "read_workspace_resource",
                    {"uri": "openbb://workspace/specs/widgets-json"},
                    graded_args=("uri",),
                ),
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9501",
                        "widgets_json": {widget_id: widget_def},
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "Earnings Lookup Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
                _call(
                    "get_widget_data",
                    {
                        "origin": backend_name,
                        "widget_id": widget_id,
                        "data_args": {"ticker": "LLY", "period": "YTD"},
                    },
                    graded_args=("origin", "widget_id"),
                ),
            ],
            targets=(_custom_target(backend_name, widget_id, widget_name),),
            policies=(
                PolicyMapping(
                    "widgets manifest specification",
                    ("openbb://workspace/specs/widgets-json",),
                ),
            ),
            pinned_widget_args={(backend_name, widget_id): frozenset({"ticker", "period"})},
            required_widgets=[
                _required_widget(
                    backend_name,
                    widget_id,
                    {"ticker": "LLY", "period": "YTD"},
                    tab_id="lookup",
                )
            ],
            required_values=["27.63", "Open"],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": widget_id,
                    "expect": {"type": "table"},
                }
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["lookup"],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": "lookup", "widget_id": widget_id}],
                }
            ],
            runtime_checks={
                "datasets": [
                    {
                        "name": "wave1-earnings-status",
                        "widget_id": widget_id,
                        "fields": ["ticker", "period", "score", "status"],
                        "path": "/earnings-status",
                        "payload": [
                            {
                                "ticker": "LLY",
                                "period": "YTD",
                                "score": 27.63,
                                "status": "Open",
                            }
                        ],
                    }
                ]
            },
            reference_answer="The LLY YTD lookup returns score 27.63 and status Open.",
            answer_source=("stark-enterprise-x", EARNINGS_WIDGET),
        )
    )
    return tasks


def _build_curate_tasks() -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    spine = "decision_briefing"
    base_state = _staged_dashboard("Wave One Decision Brief", [])
    base_args = {"fund": "Flagship Long/Short", "period": "YTD"}

    tasks.append(
        _record(
            "curate",
            spine,
            0,
            "single-widget",
            (
                "The PM wants Bench Stark Enterprise's Portfolio Command Center, Trade "
                "Ideas, on the open Wave One Decision Brief board, with fund set to "
                "Flagship Long/Short and period set to YTD."
            ),
            [
                _snapshot(),
                _call(
                    "list_available_widgets",
                    {"origin": STARK},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": TRADE_IDEAS_WIDGET,
                        "data_args": base_args,
                    },
                    graded_args=("origin", "data_args"),
                ),
            ],
            targets=(_trade_target(),),
            pinned_widget_args={(STARK, TRADE_IDEAS_WIDGET): frozenset({"fund", "period"})},
            required_widgets=[_required_widget(STARK, TRADE_IDEAS_WIDGET, base_args)],
            selected_dashboard="Wave One Decision Brief",
            initial_state=base_state,
        )
    )
    tasks.append(
        _record(
            "curate",
            spine,
            1,
            "single-widget",
            (
                "On the open Wave One Decision Brief board, find Bench Stark Enterprise's "
                "Portfolio Command Center, Trade Ideas, and add it for Flagship Long/Short "
                "and YTD."
            ),
            [
                _snapshot(),
                _call(
                    "list_available_widgets",
                    {"origin": STARK},
                    optional=True,
                ),
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
                        "data_args": base_args,
                    },
                    graded_args=("origin", "data_args"),
                ),
            ],
            targets=(_trade_target(),),
            pinned_widget_args={(STARK, TRADE_IDEAS_WIDGET): frozenset({"fund", "period"})},
            required_widgets=[_required_widget(STARK, TRADE_IDEAS_WIDGET, base_args)],
            selected_dashboard="Wave One Decision Brief",
            initial_state=base_state,
        )
    )
    tasks.append(
        _record(
            "curate",
            spine,
            2,
            "single-widget",
            (
                "Prepare the open Wave One Decision Brief board under the quarterly PM "
                "briefing policy. Add Bench Stark Enterprise's Portfolio Command Center, "
                "Trade Ideas, for Flagship Long/Short; quarterly means QTD."
            ),
            [
                _call(
                    "list_available_widgets",
                    {"origin": STARK},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": TRADE_IDEAS_WIDGET,
                        "data_args": {
                            "fund": "Flagship Long/Short",
                            "period": "QTD",
                        },
                    },
                    graded_args=("origin", "data_args"),
                ),
            ],
            targets=(_trade_target(),),
            policies=(PolicyMapping("quarterly PM briefing policy", ("QTD",)),),
            pinned_widget_args={(STARK, TRADE_IDEAS_WIDGET): frozenset({"fund", "period"})},
            required_widgets=[
                _required_widget(
                    STARK,
                    TRADE_IDEAS_WIDGET,
                    {"fund": "Flagship Long/Short", "period": "QTD"},
                )
            ],
            selected_dashboard="Wave One Decision Brief",
            initial_state=base_state,
        )
    )

    cross_args = {"company": "TSLA", "year": 2024}
    for level in (3, 4):
        prefix = (
            "Set up the open Wave One Decision Brief board:"
            if level == 3
            else "Use Workspace session guidance to prepare the open Wave One Decision Brief board:"
        )
        prompt = (
            f"{prefix} place Bench Stark Enterprise's Portfolio Command Center, Trade "
            "Ideas, for Flagship Long/Short and QTD beside Getting Started's Car "
            "Manufacturer Performance for TSLA and 2024. Put Trade Ideas at x 0, y 0, "
            "width 20, height 14 and the manufacturer view at x 20, y 0, width 20, "
            "height 14."
        )
        tools: list[JsonDict] = []
        policies: tuple[PolicyMapping, ...] = ()
        if level == 4:
            tools.append(
                _call(
                    "get_workspace_prompt",
                    {"name": "workspace_session_context"},
                    graded_args=("name",),
                )
            )
            policies = (
                PolicyMapping(
                    "Workspace session guidance",
                    ("workspace_session_context",),
                ),
            )
        tools.extend(
            [
                _call(
                    "list_available_widgets",
                    {"origin": STARK},
                    optional=True,
                ),
                _call(
                    "list_available_widgets",
                    {"origin": GETTING_STARTED},
                    optional=True,
                ),
            ]
        )
        tools.extend(
            [
                _call(
                    "create_widget",
                    {
                        "origin": STARK,
                        "widget_id": TRADE_IDEAS_WIDGET,
                        "data_args": {
                            "fund": "Flagship Long/Short",
                            "period": "QTD",
                        },
                    },
                    graded_args=("origin", "data_args"),
                ),
                _call(
                    "create_widget",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": MANUFACTURER_WIDGET,
                        "data_args": cross_args,
                    },
                    graded_args=("origin", "data_args"),
                ),
                _call(
                    "update_widget_layout",
                    {
                        "widget_id": TRADE_IDEAS_WIDGET,
                        "x": 0,
                        "y": 0,
                        "w": 20,
                        "h": 14,
                    },
                    graded_args=("x", "y", "w", "h"),
                ),
                _call(
                    "update_widget_layout",
                    {
                        "widget_id": MANUFACTURER_WIDGET,
                        "x": 20,
                        "y": 0,
                        "w": 20,
                        "h": 14,
                    },
                    graded_args=("x", "y", "w", "h"),
                ),
            ]
        )
        tasks.append(
            _record(
                "curate",
                spine,
                level,
                "dashboard",
                prompt,
                tools,
                targets=(_trade_target(), _manufacturer_target()),
                policies=policies,
                pinned_widget_args={
                    (STARK, TRADE_IDEAS_WIDGET): frozenset({"fund", "period"}),
                    (GETTING_STARTED, MANUFACTURER_WIDGET): frozenset({"company", "year"}),
                },
                required_widgets=[
                    _required_widget(
                        STARK,
                        TRADE_IDEAS_WIDGET,
                        {"fund": "Flagship Long/Short", "period": "QTD"},
                    ),
                    _required_widget(
                        GETTING_STARTED,
                        MANUFACTURER_WIDGET,
                        cross_args,
                    ),
                ],
                selected_dashboard="Wave One Decision Brief",
                initial_state=base_state,
            )
        )

    backend_name = "Decision Tile Backend"
    custom_widget_name = "Decision Summary Tile"
    custom_widget_id = "decision_summary_tile"
    app_name = "Decision Briefing App"
    custom_def = _widget_def(
        custom_widget_name,
        "/decision-summary",
        widget_type="metric",
        grid=(40, 10),
    )
    app_def = _app(
        app_name,
        [("briefing", "Briefing", [(custom_widget_id, 0, 0, 40, 10, None)])],
    )
    tasks.append(
        _record(
            "curate",
            spine,
            5,
            "platform",
            (
                "The PM needs a Decision Tile Backend with a Decision Summary Tile metric. Author "
                "and add it, then instantiate its Decision Briefing App. On Briefing, place "
                "Bench Stark Enterprise's Portfolio Command Center, Trade Ideas, beside "
                "Getting Started's Car Manufacturer Performance at y 10, x 0 and x 20, "
                "each width 20 and height 14. Widget ids are the snake_case of widget names; "
                "tab ids are the snake_case of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9502",
                        "widgets_json": {custom_widget_id: custom_def},
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "Decision Briefing Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
                _call(
                    "list_available_widgets",
                    {"origin": STARK},
                    optional=True,
                ),
                _call(
                    "list_available_widgets",
                    {"origin": GETTING_STARTED},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {"origin": STARK, "widget_id": TRADE_IDEAS_WIDGET},
                    graded_args=("origin",),
                ),
                _call(
                    "create_widget",
                    {"origin": GETTING_STARTED, "widget_id": MANUFACTURER_WIDGET},
                    graded_args=("origin",),
                ),
                _call(
                    "update_widget_layout",
                    {
                        "widget_id": TRADE_IDEAS_WIDGET,
                        "x": 0,
                        "y": 10,
                        "w": 20,
                        "h": 14,
                        "tab_id": "briefing",
                    },
                    optional=True,
                ),
                _call(
                    "update_widget_layout",
                    {
                        "widget_id": MANUFACTURER_WIDGET,
                        "x": 20,
                        "y": 10,
                        "w": 20,
                        "h": 14,
                        "tab_id": "briefing",
                    },
                    optional=True,
                ),
            ],
            targets=(
                _custom_target(
                    backend_name,
                    custom_widget_id,
                    custom_widget_name,
                ),
                _trade_target(),
                _manufacturer_target(),
            ),
            required_widgets=[
                _required_widget(STARK, TRADE_IDEAS_WIDGET, tab_id="briefing"),
                _required_widget(
                    GETTING_STARTED,
                    MANUFACTURER_WIDGET,
                    tab_id="briefing",
                ),
                # Instantiation is a state outcome: the authored widget must
                # exist in the workspace, not merely be defined.
                _required_widget(backend_name, custom_widget_id),
            ],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": custom_widget_id,
                    "expect": {"type": "metric"},
                }
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["briefing"],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": "briefing", "widget_id": custom_widget_id}],
                }
            ],
        )
    )
    return tasks


def _parameter_stage() -> JsonDict:
    return _staged_dashboard(
        "Technology Decision Inputs",
        [
            {
                "origin": GETTING_STARTED,
                "widget_id": MANUFACTURER_WIDGET,
                "tab_id": "review",
                "data_args": {"company": "TM", "year": 2024},
                "layout": {"x": 0, "y": 0, "w": 20, "h": 12},
            },
            {
                "origin": STARK,
                "widget_id": EARNINGS_WIDGET,
                "tab_id": "review",
                "data_args": {
                    "sector": "Healthcare",
                    "ticker": "LLY",
                    "period": "YTD",
                },
                "layout": {"x": 20, "y": 0, "w": 20, "h": 14},
            },
            {
                "origin": STARK,
                "widget_id": TRADE_IDEAS_WIDGET,
                "tab_id": "review",
                "data_args": {"fund": "Flagship Long/Short", "period": "YTD"},
                "layout": {"x": 0, "y": 14, "w": 40, "h": 14},
            },
        ],
    )


def _build_parameterize_tasks() -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    spine = "technology_decision_inputs"
    stage = _parameter_stage()

    low_specs = (
        (
            0,
            "On the open Technology Decision Inputs board, switch Car Manufacturer "
            "Performance with company set to TSLA and year set to 2023, and leave every "
            "other view unchanged.",
            {"company": "TSLA", "year": 2023},
            (),
        ),
        (
            1,
            "Look over the open Technology Decision Inputs board, then change Car "
            "Manufacturer Performance to TSLA and 2022 while preserving everything else.",
            {"company": "TSLA", "year": 2022},
            (),
        ),
        (
            2,
            "Apply the current Tesla model-year policy on the open Technology Decision "
            "Inputs board. Set Car Manufacturer Performance to company TSLA and "
            "year 2024, the current model year, and preserve the rest of the board.",
            {"company": "TSLA", "year": 2024},
            (
                PolicyMapping(
                    "current Tesla model-year policy",
                    ("TSLA", 2024),
                ),
            ),
        ),
    )
    for level, prompt, data_args, policies in low_specs:
        tools: list[JsonDict] = []
        if level in {0, 1}:
            tools.append(_snapshot())
        if level == 1:
            tools.append(
                _call(
                    "read_widget",
                    {"widget_id": MANUFACTURER_WIDGET},
                    optional=True,
                )
            )
        tools.append(
            _call(
                "update_widget",
                {"widget_id": MANUFACTURER_WIDGET, "data_args": data_args},
                graded_args=("data_args",),
            )
        )
        tasks.append(
            _record(
                "parameterize",
                spine,
                level,
                "single-widget",
                prompt,
                tools,
                targets=(_manufacturer_target(staged=True),),
                policies=policies,
                pinned_widget_args={
                    (GETTING_STARTED, MANUFACTURER_WIDGET): frozenset({"company", "year"})
                },
                required_widgets=[
                    _required_widget(
                        GETTING_STARTED,
                        MANUFACTURER_WIDGET,
                        data_args,
                    )
                ],
                selected_dashboard="Technology Decision Inputs",
                initial_state=stage,
            )
        )

    earnings_args = {
        "sector": "Technology",
        "ticker": "AAPL",
        "period": "QTD",
    }
    tasks.append(
        _record(
            "parameterize",
            spine,
            3,
            "single-widget",
            (
                "Retune Upcoming Earnings on the open Technology Decision Inputs board to "
                "Technology, AAPL, and QTD. Keep Car Manufacturer Performance and every "
                "other view as they are."
            ),
            [
                _snapshot(),
                _call(
                    "update_widget",
                    {"widget_id": EARNINGS_WIDGET, "data_args": earnings_args},
                    graded_args=("data_args",),
                ),
            ],
            targets=(
                _earnings_target(staged=True),
                _manufacturer_target(staged=True),
            ),
            pinned_widget_args={
                (STARK, EARNINGS_WIDGET): frozenset({"sector", "ticker", "period"})
            },
            required_widgets=[
                _required_widget(STARK, EARNINGS_WIDGET, earnings_args),
                _required_widget(GETTING_STARTED, MANUFACTURER_WIDGET),
            ],
            selected_dashboard="Technology Decision Inputs",
            initial_state=stage,
        )
    )
    trade_args = {"fund": "Flagship Long/Short", "period": "QTD"}
    tasks.append(
        _record(
            "parameterize",
            spine,
            4,
            "single-widget",
            (
                "Prepare the open Technology Decision Inputs board for the quarterly review "
                "under Finance Earnings Prep governance. Set Upcoming Earnings to "
                "Technology, AAPL, and QTD, and Trade Ideas to Flagship Long/Short and QTD. "
                "Preserve Car Manufacturer Performance."
            ),
            [
                _call(
                    "get_skill_content",
                    {"slug": "finance-earnings-prep"},
                    graded_args=("slug",),
                ),
                _call(
                    "update_widget",
                    {"widget_id": EARNINGS_WIDGET, "data_args": earnings_args},
                    graded_args=("data_args",),
                ),
                _call(
                    "update_widget",
                    {"widget_id": TRADE_IDEAS_WIDGET, "data_args": trade_args},
                    graded_args=("data_args",),
                ),
            ],
            targets=(
                _earnings_target(staged=True),
                _trade_target(staged=True),
                _manufacturer_target(staged=True),
            ),
            policies=(
                PolicyMapping(
                    "Finance Earnings Prep governance",
                    ("finance-earnings-prep",),
                ),
            ),
            pinned_widget_args={
                (STARK, EARNINGS_WIDGET): frozenset({"sector", "ticker", "period"}),
                (STARK, TRADE_IDEAS_WIDGET): frozenset({"fund", "period"}),
            },
            required_widgets=[
                _required_widget(STARK, EARNINGS_WIDGET, earnings_args),
                _required_widget(STARK, TRADE_IDEAS_WIDGET, trade_args),
            ],
            selected_dashboard="Technology Decision Inputs",
            initial_state=stage,
        )
    )
    tasks.append(
        _record(
            "parameterize",
            spine,
            5,
            "single-widget",
            (
                "Finish the rebuild on the open Technology Decision Inputs board using "
                "only its existing views. Set Car Manufacturer Performance to TSLA and "
                "2024, Upcoming Earnings to Technology, AAPL, and QTD, and Trade Ideas to "
                "Flagship Long/Short and QTD. Preserve all layout and surrounding content."
            ),
            [
                _call(
                    "update_widget",
                    {
                        "widget_id": MANUFACTURER_WIDGET,
                        "data_args": {"company": "TSLA", "year": 2024},
                    },
                    graded_args=("data_args",),
                ),
                _call(
                    "update_widget",
                    {"widget_id": EARNINGS_WIDGET, "data_args": earnings_args},
                    graded_args=("data_args",),
                ),
                _call(
                    "update_widget",
                    {"widget_id": TRADE_IDEAS_WIDGET, "data_args": trade_args},
                    graded_args=("data_args",),
                ),
            ],
            targets=(
                _manufacturer_target(staged=True),
                _earnings_target(staged=True),
                _trade_target(staged=True),
            ),
            pinned_widget_args={
                (GETTING_STARTED, MANUFACTURER_WIDGET): frozenset({"company", "year"}),
                (STARK, EARNINGS_WIDGET): frozenset({"sector", "ticker", "period"}),
                (STARK, TRADE_IDEAS_WIDGET): frozenset({"fund", "period"}),
            },
            required_widgets=[
                _required_widget(
                    GETTING_STARTED,
                    MANUFACTURER_WIDGET,
                    {"company": "TSLA", "year": 2024},
                ),
                _required_widget(STARK, EARNINGS_WIDGET, earnings_args),
                _required_widget(STARK, TRADE_IDEAS_WIDGET, trade_args),
            ],
            selected_dashboard="Technology Decision Inputs",
            initial_state=stage,
        )
    )
    return tasks


def _build_organize_tasks() -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    spine = "committee_navigation"

    tasks.append(
        _record(
            "organize",
            spine,
            0,
            "dashboard",
            (
                "Create a dashboard named Wave One Committee Review for the committee and "
                "make it the active board."
            ),
            [
                _snapshot(),
                _call(
                    "manage_dashboard",
                    {
                        "operation": "create",
                        "name": "Wave One Committee Review",
                        "activate": True,
                    },
                    graded_args=("operation", "name"),
                ),
            ],
        )
    )
    tasks.append(
        _record(
            "organize",
            spine,
            1,
            "dashboard",
            (
                "Create Wave One Committee Review as the active committee board, with "
                "Agenda and Evidence tabs."
            ),
            [
                _snapshot(),
                _call(
                    "manage_dashboard",
                    {
                        "operation": "create",
                        "name": "Wave One Committee Review",
                        "activate": True,
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_navigation_bar",
                    {
                        "operation": "add_tabs",
                        "tabs": [{"name": "Agenda"}, {"name": "Evidence"}],
                    },
                    graded_args=("tabs",),
                ),
            ],
        )
    )
    tasks.append(
        _record(
            "organize",
            spine,
            2,
            "dashboard",
            (
                "The committee needs an active Wave One Committee Review board with Agenda "
                "and Evidence tabs. Create it, then open Evidence."
            ),
            [
                _call(
                    "manage_dashboard",
                    {
                        "operation": "create",
                        "name": "Wave One Committee Review",
                        "activate": True,
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_navigation_bar",
                    {
                        "operation": "create",
                        "tabs": [{"name": "Agenda"}, {"name": "Evidence"}],
                    },
                    optional=True,
                ),
                _call(
                    "navigate_workspace",
                    {"operation": "tab", "tab_id": "evidence"},
                    graded_args=("tab_id",),
                ),
            ],
            required_tabs=["agenda", "evidence"],
            required_dashboard_name="Wave One Committee Review",
        )
    )

    staging = _staged_dashboard(
        "Committee Review Staging",
        [],
        tabs=[
            {"id": "agenda", "name": "Agenda"},
            {"id": "evidence", "name": "Evidence"},
        ],
        dashboard_id="wave1_committee_staging",
    )
    tasks.append(
        _record(
            "organize",
            spine,
            3,
            "dashboard",
            (
                "On the open Committee Review Staging board, rename the dashboard to Wave "
                "One Committee Review and change its Agenda tab to Decision Agenda. Keep "
                "Evidence and all other workspace content intact."
            ),
            [
                _snapshot(),
                _call(
                    "manage_dashboard",
                    {
                        "operation": "update",
                        "dashboard_id": "wave1_committee_staging",
                        "name": "Wave One Committee Review",
                    },
                    graded_args=("name",),
                ),
                _call(
                    "manage_navigation_bar",
                    {
                        "operation": "rename_tabs",
                        "rename_map": {"agenda": "Decision Agenda"},
                        "dashboard_id": "wave1_committee_staging",
                    },
                    graded_args=("rename_map",),
                ),
            ],
            selected_dashboard="Committee Review Staging",
            initial_state=staging,
        )
    )
    tasks.append(
        _record(
            "organize",
            spine,
            4,
            "dashboard",
            (
                "Following Workspace session guidance, create and activate Wave One "
                "Committee Review with Decision Agenda, Evidence, and Sign-Off tabs in "
                "that order."
            ),
            [
                _call(
                    "get_workspace_prompt",
                    {"name": "workspace_session_context"},
                    graded_args=("name",),
                ),
                _call(
                    "manage_dashboard",
                    {
                        "operation": "create",
                        "name": "Wave One Committee Review",
                        "activate": True,
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_navigation_bar",
                    {
                        "operation": "create",
                        "tabs": [
                            {"name": "Decision Agenda"},
                            {"name": "Evidence"},
                            {"name": "Sign-Off"},
                        ],
                    },
                    graded_args=("operation", "tabs"),
                ),
            ],
            policies=(
                PolicyMapping(
                    "Workspace session guidance",
                    ("workspace_session_context",),
                ),
            ),
        )
    )

    backend_name = "Committee Navigation Backend"
    agenda_name = "Agenda Queue"
    evidence_name = "Evidence Register"
    agenda_id = "agenda_queue"
    evidence_id = "evidence_register"
    app_name = "Committee Review App"
    widgets = {
        agenda_id: _widget_def(agenda_name, "/agenda"),
        evidence_id: _widget_def(evidence_name, "/evidence"),
    }
    app_def = _app(
        app_name,
        [
            ("agenda", "Agenda", [(agenda_id, 0, 0, 40, 12, None)]),
            ("evidence", "Evidence", [(evidence_id, 0, 0, 40, 12, None)]),
        ],
    )
    tasks.append(
        _record(
            "organize",
            spine,
            5,
            "platform",
            (
                "The committee needs a Committee Navigation Backend with Agenda Queue and "
                "Evidence Register table views. Author and add it, publish a Committee Review App "
                "with Agenda and Evidence tabs, and instantiate it. Follow the apps manifest "
                "specification. Widget ids are the snake_case of widget names; tab ids are "
                "the snake_case of tab names."
            ),
            [
                _call(
                    "read_workspace_resource",
                    {"uri": "openbb://workspace/specs/apps-json"},
                    graded_args=("uri",),
                ),
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9503",
                        "widgets_json": widgets,
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "Committee Review Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=(
                _custom_target(backend_name, agenda_id, agenda_name),
                _custom_target(backend_name, evidence_id, evidence_name),
            ),
            policies=(
                PolicyMapping(
                    "apps manifest specification",
                    ("openbb://workspace/specs/apps-json",),
                ),
            ),
            required_widgets=[
                _required_widget(backend_name, agenda_id, tab_id="agenda"),
                _required_widget(backend_name, evidence_id, tab_id="evidence"),
            ],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": agenda_id,
                    "expect": {"type": "table"},
                },
                {
                    "backend_name": backend_name,
                    "widget_id": evidence_id,
                    "expect": {"type": "table"},
                },
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["agenda", "evidence"],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [
                        {"tab_id": "agenda", "widget_id": agenda_id},
                        {"tab_id": "evidence", "widget_id": evidence_id},
                    ],
                }
            ],
        )
    )
    return tasks


def _repair_stage(
    widgets: list[JsonDict],
    *,
    name: str = "NAV Repair Staging",
) -> JsonDict:
    return _staged_dashboard(
        name,
        widgets,
        tabs=[{"id": "exceptions", "name": "Exceptions"}],
    )


def _nav_widget(
    *,
    widget_uuid: str,
    status: str = "Open",
    period: str = "YTD",
    layout: JsonDict | None = None,
) -> JsonDict:
    return {
        "origin": STARK,
        "widget_id": NAV_EXCEPTIONS_WIDGET,
        "widget_uuid": widget_uuid,
        "tab_id": "exceptions",
        "data_args": {
            "fund": "Flagship Long/Short",
            "status": status,
            "period": period,
        },
        "layout": layout or {"x": 0, "y": 0, "w": 40, "h": 14},
    }


def _repair_preserved_widget() -> JsonDict:
    return {
        "origin": STARK,
        "widget_id": TRADE_IDEAS_WIDGET,
        "widget_uuid": "repair_trade_ideas",
        "tab_id": "exceptions",
        "data_args": {"fund": "Flagship Long/Short", "period": "YTD"},
        "layout": {"x": 0, "y": 14, "w": 40, "h": 14},
    }


def _build_repair_tasks() -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    spine = "nav_exception_station"
    correct_args = {
        "fund": "Flagship Long/Short",
        "status": "Open",
        "period": "YTD",
    }

    stated_fix_stage = _repair_stage(
        [
            _nav_widget(widget_uuid="nav_primary", period="QTD"),
            _repair_preserved_widget(),
        ]
    )
    tasks.append(
        _record(
            "repair",
            spine,
            0,
            "repair",
            (
                "NAV Exceptions on the open NAV Repair Staging board has fund set to "
                "Flagship Long/Short, status set to Open, and period set to QTD. Set fund "
                "to Flagship Long/Short, status to Open, and period back to YTD."
            ),
            [
                _snapshot(),
                _call(
                    "update_widget",
                    {
                        "widget_uuid": "nav_primary",
                        "data_args": correct_args,
                    },
                    graded_args=("data_args",),
                ),
            ],
            targets=(_nav_target(staged=True),),
            pinned_widget_args={
                (STARK, NAV_EXCEPTIONS_WIDGET): frozenset({"fund", "status", "period"})
            },
            required_widgets=[
                _required_widget(STARK, NAV_EXCEPTIONS_WIDGET, correct_args),
            ],
            selected_dashboard="NAV Repair Staging",
            initial_state=stated_fix_stage,
        )
    )

    bad_param_stage = _repair_stage(
        [
            _nav_widget(widget_uuid="nav_primary", status="Closed"),
            _repair_preserved_widget(),
        ]
    )
    tasks.append(
        _record(
            "repair",
            spine,
            1,
            "repair",
            (
                "On the open NAV Repair Staging board, fix the NAV Exceptions setting by "
                "restoring Flagship Long/Short, Open, and YTD. Preserve Trade Ideas and "
                "every other workspace item."
            ),
            [
                _snapshot(),
                _call(
                    "update_widget",
                    {
                        "widget_uuid": "nav_primary",
                        "data_args": correct_args,
                    },
                    graded_args=("data_args",),
                ),
            ],
            targets=(_nav_target(staged=True), _trade_target(staged=True)),
            pinned_widget_args={
                (STARK, NAV_EXCEPTIONS_WIDGET): frozenset({"fund", "status", "period"})
            },
            required_widgets=[
                _required_widget(STARK, NAV_EXCEPTIONS_WIDGET, correct_args),
                _required_widget(STARK, TRADE_IDEAS_WIDGET),
            ],
            selected_dashboard="NAV Repair Staging",
            initial_state=bad_param_stage,
        )
    )

    duplicate_stage = _repair_stage(
        [
            _nav_widget(widget_uuid="nav_primary"),
            _nav_widget(
                widget_uuid="nav_duplicate",
                layout={"x": 0, "y": 28, "w": 40, "h": 14},
            ),
            _repair_preserved_widget(),
        ]
    )
    tasks.append(
        _record(
            "repair",
            spine,
            2,
            "repair",
            (
                "The open NAV Repair Staging board has an extra NAV Exceptions copy. The "
                "duplicate-cleanup marker identifies it; remove that copy so exactly one "
                "remains, and preserve Trade Ideas and all other content."
            ),
            [
                _call(
                    "delete_widget",
                    {"widget_uuid": "nav_duplicate"},
                    graded_args=("widget_uuid",),
                )
            ],
            targets=(_nav_target(staged=True), _trade_target(staged=True)),
            policies=(PolicyMapping("duplicate-cleanup marker", ("nav_duplicate",)),),
            required_widgets=[
                _required_widget(
                    STARK,
                    NAV_EXCEPTIONS_WIDGET,
                    min_count=1,
                    max_count=1,
                ),
                _required_widget(STARK, TRADE_IDEAS_WIDGET),
            ],
            selected_dashboard="NAV Repair Staging",
            initial_state=duplicate_stage,
        )
    )

    misplaced_stage = _repair_stage(
        [
            _nav_widget(
                widget_uuid="nav_primary",
                layout={"x": 0, "y": 0, "w": 40, "h": 14},
            ),
            {
                **_repair_preserved_widget(),
                "layout": {"x": 0, "y": 0, "w": 40, "h": 14},
            },
        ]
    )
    tasks.append(
        _record(
            "repair",
            spine,
            3,
            "repair",
            (
                "Fix the overlap on the open NAV Repair Staging board without disturbing "
                "Trade Ideas. Move NAV Exceptions to x 0, y 14, width 40, and height 14 on "
                "Exceptions, preserving all parameters and remaining workspace content."
            ),
            [
                _snapshot(),
                _call(
                    "update_widget_layout",
                    {
                        "widget_uuid": "nav_primary",
                        "x": 0,
                        "y": 14,
                        "w": 40,
                        "h": 14,
                        "tab_id": "exceptions",
                    },
                    graded_args=("x", "y", "w", "h", "tab_id"),
                ),
            ],
            targets=(_nav_target(staged=True), _trade_target(staged=True)),
            required_widgets=[
                _required_widget(STARK, NAV_EXCEPTIONS_WIDGET),
                _required_widget(STARK, TRADE_IDEAS_WIDGET),
            ],
            selected_dashboard="NAV Repair Staging",
            initial_state=misplaced_stage,
        )
    )

    multi_stage = _repair_stage(
        [
            _nav_widget(
                widget_uuid="nav_primary",
                status="Closed",
                layout={"x": 0, "y": 0, "w": 40, "h": 14},
            ),
            _nav_widget(
                widget_uuid="nav_duplicate",
                status="Closed",
                layout={"x": 0, "y": 28, "w": 40, "h": 14},
            ),
            {
                **_repair_preserved_widget(),
                "layout": {"x": 0, "y": 0, "w": 40, "h": 14},
            },
        ]
    )
    tasks.append(
        _record(
            "repair",
            spine,
            4,
            "repair",
            (
                "Clean up the open NAV Repair Staging board. Restore the primary NAV "
                "Exceptions view to Flagship Long/Short, Open, and YTD; the "
                "duplicate-cleanup marker identifies the extra copy. Move the primary to "
                "x 0, y 14, width 40, height 14 on Exceptions, and preserve Trade Ideas."
            ),
            [
                _call(
                    "update_widget",
                    {
                        "widget_uuid": "nav_primary",
                        "data_args": correct_args,
                    },
                    graded_args=("data_args",),
                ),
                _call(
                    "delete_widget",
                    {"widget_uuid": "nav_duplicate"},
                    graded_args=("widget_uuid",),
                ),
                _call(
                    "update_widget_layout",
                    {
                        "widget_uuid": "nav_primary",
                        "x": 0,
                        "y": 14,
                        "w": 40,
                        "h": 14,
                        "tab_id": "exceptions",
                    },
                    graded_args=("x", "y", "w", "h", "tab_id"),
                ),
            ],
            targets=(_nav_target(staged=True), _trade_target(staged=True)),
            policies=(PolicyMapping("duplicate-cleanup marker", ("nav_duplicate",)),),
            pinned_widget_args={
                (STARK, NAV_EXCEPTIONS_WIDGET): frozenset({"fund", "status", "period"})
            },
            required_widgets=[
                _required_widget(
                    STARK,
                    NAV_EXCEPTIONS_WIDGET,
                    correct_args,
                    min_count=1,
                    max_count=1,
                ),
                _required_widget(STARK, TRADE_IDEAS_WIDGET),
            ],
            selected_dashboard="NAV Repair Staging",
            initial_state=multi_stage,
        )
    )

    backend_name = "Wave One NAV Repair"
    widget_name = "NAV Exception Queue"
    widget_id = "nav_exception_queue"
    app_name = "NAV Repair App"
    fixed_widget = _widget_def(
        widget_name,
        "/nav-exceptions",
        description="Refreshed NAV exception queue.",
    )
    fixed_app = _app(
        app_name,
        [("exceptions", "Exceptions", [(widget_id, 0, 0, 40, 12, None)])],
    )
    broken_widget = {
        "name": widget_name,
        "description": "Broken authored NAV queue.",
        "type": "table",
    }
    broken_app = {
        "name": app_name,
        "tabs": {
            "exceptions": {
                "id": "exceptions",
                "name": "Exceptions",
                "layout": [
                    {"i": widget_id, "x": 0, "y": 0, "w": 30, "h": 12},
                    {"i": widget_id, "x": 20, "y": 0, "w": 20, "h": 12},
                ],
            }
        },
    }
    custom_state = _repair_stage(
        [
            {
                "origin": backend_name,
                "widget_id": widget_id,
                "widget_uuid": "custom_nav_queue",
                "tab_id": "exceptions",
                "layout": {"x": 0, "y": 0, "w": 40, "h": 12},
            }
        ],
        name="Custom NAV Repair Staging",
    )
    custom_state["custom_backends"] = [
        {
            "backend_id": "backend_005",
            "name": backend_name,
            "url": "http://127.0.0.1:9504",
            "widgets_json": {widget_id: broken_widget},
            "apps_json": [broken_app],
            "warnings": ["missing endpoint and overlapping app layout"],
        }
    ]
    tasks.append(
        _record(
            "repair",
            spine,
            5,
            "repair",
            (
                "On the open Custom NAV Repair Staging board, refresh the authored Wave One "
                "NAV Repair backend so NAV Exception Queue serves /nav-exceptions and NAV "
                "Repair App has one non-overlapping placement on Exceptions. Keep the open "
                "view and all other workspace content. Widget ids are the snake_case of "
                "widget names; tab ids are the snake_case of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "refresh",
                        "backend_id": "backend_005",
                        "widgets_json": {widget_id: fixed_widget},
                        "apps_json": [fixed_app],
                    },
                    graded_args=("operation",),
                )
            ],
            targets=(
                _custom_target(
                    backend_name,
                    widget_id,
                    widget_name,
                    staged=True,
                ),
            ),
            required_widgets=[
                _required_widget(
                    backend_name,
                    widget_id,
                    tab_id="exceptions",
                )
            ],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": widget_id,
                    "expect": {},
                }
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["exceptions"],
                    "layout_refs_valid": True,
                    "no_overlaps": True,
                }
            ],
            selected_dashboard="Custom NAV Repair Staging",
            initial_state=custom_state,
        )
    )
    return tasks


def _platform_stage() -> JsonDict:
    return _staged_dashboard(
        "Governed Earnings Brief",
        [],
        tabs=[{"id": "overview", "name": "Overview"}],
    )


def _build_platform_tasks() -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    spine = "governed_earnings_brief"
    stage = _platform_stage()

    tasks.append(
        _record(
            "platform",
            spine,
            0,
            "platform",
            (
                "Read the Finance Earnings Prep skill (finance-earnings-prep) for the open "
                "Governed Earnings Brief board. Add an Earnings Prep Workflow note that "
                "records the workflow title and its first and fourth actions."
            ),
            [
                _snapshot(),
                _call(
                    "get_skill_content",
                    {"slug": "finance-earnings-prep"},
                    graded_args=("slug",),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "Earnings Prep Workflow",
                        "data": (
                            "Earnings prep workflow: compare internal estimates and inspect "
                            "transcript tone."
                        ),
                    },
                    graded_args=("widget_type", "name"),
                ),
            ],
            required_generated_widgets=[
                {
                    "widget_type": "note",
                    "name_contains": "Earnings Prep Workflow",
                    "data_contains": [
                        "Earnings prep workflow",
                        "internal estimates",
                        "transcript tone",
                    ],
                }
            ],
            selected_dashboard="Governed Earnings Brief",
            initial_state=stage,
        )
    )

    tasks.append(
        _record(
            "platform",
            spine,
            1,
            "platform",
            (
                "On the open Governed Earnings Brief board, consult Finance Earnings Prep "
                "governance and add an Earnings Governance Actions note that names internal "
                "estimates and transcript tone."
            ),
            [
                _snapshot(),
                _call(
                    "get_skill_content",
                    {"slug": "finance-earnings-prep"},
                    graded_args=("slug",),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "Earnings Governance Actions",
                        "data": (
                            "Governance actions: compare internal estimates and review "
                            "transcript tone."
                        ),
                    },
                    graded_args=("widget_type", "name"),
                ),
            ],
            policies=(
                PolicyMapping(
                    "Finance Earnings Prep governance",
                    ("finance-earnings-prep",),
                ),
            ),
            required_generated_widgets=[
                {
                    "widget_type": "note",
                    "name_contains": "Earnings Governance Actions",
                    "data_contains": ["internal estimates", "transcript tone"],
                }
            ],
            selected_dashboard="Governed Earnings Brief",
            initial_state=stage,
        )
    )
    tasks.append(
        _record(
            "platform",
            spine,
            2,
            "platform",
            (
                "Review the backend contract for the open Governed Earnings Brief board, "
                "then add a Backend Contract Actions note that names endpoints and CORS."
            ),
            [
                _call(
                    "read_workspace_resource",
                    {"uri": "openbb://workspace/contract/backend"},
                    graded_args=("uri",),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "Backend Contract Actions",
                        "data": "Backend contract actions: verify endpoints and CORS.",
                    },
                    graded_args=("widget_type", "name"),
                ),
            ],
            policies=(
                PolicyMapping(
                    "backend contract",
                    ("openbb://workspace/contract/backend",),
                ),
            ),
            required_generated_widgets=[
                {
                    "widget_type": "note",
                    "name_contains": "Backend Contract Actions",
                    "data_contains": ["endpoints", "CORS"],
                }
            ],
            selected_dashboard="Governed Earnings Brief",
            initial_state=stage,
        )
    )
    tasks.append(
        _record(
            "platform",
            spine,
            3,
            "dashboard",
            (
                "Use Workspace session guidance on the open Governed Earnings Brief board. "
                "Add an Actions tab and place a Session Grounding note there naming "
                "current-dashboard and current-tab."
            ),
            [
                _call(
                    "get_workspace_prompt",
                    {"name": "workspace_session_context"},
                    graded_args=("name",),
                ),
                _call(
                    "manage_navigation_bar",
                    {"operation": "add_tabs", "tabs": [{"name": "Actions"}]},
                    graded_args=("tabs",),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "Session Grounding",
                        "data": "Session grounding: current-dashboard and current-tab.",
                        "inner_tab": "actions",
                    },
                    graded_args=("widget_type", "name"),
                ),
            ],
            policies=(
                PolicyMapping(
                    "Workspace session guidance",
                    ("workspace_session_context",),
                ),
            ),
            required_generated_widgets=[
                {
                    "widget_type": "note",
                    "name_contains": "Session Grounding",
                    "data_contains": ["current-dashboard", "current-tab"],
                    "tab_id": "actions",
                }
            ],
            selected_dashboard="Governed Earnings Brief",
            initial_state=stage,
        )
    )
    tasks.append(
        _record(
            "platform",
            spine,
            4,
            "dashboard",
            (
                "For the open Governed Earnings Brief board, combine Finance Earnings Prep "
                "governance with Workspace session guidance. Add an Actions tab and an "
                "Earnings Session Actions note there naming action items and "
                "current-dashboard."
            ),
            [
                _call(
                    "get_skill_content",
                    {"slug": "finance-earnings-prep"},
                    graded_args=("slug",),
                ),
                _call(
                    "get_workspace_prompt",
                    {"name": "workspace_session_context"},
                    graded_args=("name",),
                ),
                _call(
                    "manage_navigation_bar",
                    {"operation": "add_tabs", "tabs": [{"name": "Actions"}]},
                    graded_args=("tabs",),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "Earnings Session Actions",
                        "data": "Governed action items tied to current-dashboard context.",
                        "inner_tab": "actions",
                    },
                    graded_args=("widget_type", "name"),
                ),
            ],
            policies=(
                PolicyMapping(
                    "Finance Earnings Prep governance",
                    ("finance-earnings-prep",),
                ),
                PolicyMapping(
                    "Workspace session guidance",
                    ("workspace_session_context",),
                ),
            ),
            required_generated_widgets=[
                {
                    "widget_type": "note",
                    "name_contains": "Earnings Session Actions",
                    "data_contains": ["action items", "current-dashboard"],
                    "tab_id": "actions",
                }
            ],
            selected_dashboard="Governed Earnings Brief",
            initial_state=stage,
        )
    )

    backend_name = "Governed Earnings Backend"
    widget_name = "Earnings Action Register"
    widget_id = "earnings_action_register"
    app_name = "Governed Earnings App"
    widget_def = _widget_def(widget_name, "/earnings-actions")
    app_def = _app(
        app_name,
        [("actions", "Actions", [(widget_id, 0, 0, 40, 12, None)])],
    )
    tasks.append(
        _record(
            "platform",
            spine,
            5,
            "platform",
            (
                "The desk wants a Governed Earnings Backend with an Earnings Action Register. "
                "Following the build-an-app guide, author and add it, publish a Governed "
                "Earnings App with an Actions tab, and instantiate it. Widget ids are the "
                "snake_case of widget names; tab ids are the snake_case of tab names."
            ),
            [
                _call(
                    "read_workspace_resource",
                    {"uri": "openbb://workspace/guides/build-an-app"},
                    graded_args=("uri",),
                ),
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9505",
                        "widgets_json": {widget_id: widget_def},
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "Governed Earnings Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=(_custom_target(backend_name, widget_id, widget_name),),
            policies=(
                PolicyMapping(
                    "build-an-app guide",
                    ("openbb://workspace/guides/build-an-app",),
                ),
            ),
            required_widgets=[_required_widget(backend_name, widget_id, tab_id="actions")],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": widget_id,
                    "expect": {},
                }
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["actions"],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": "actions", "widget_id": widget_id}],
                }
            ],
        )
    )
    return tasks


def _extend_seed(
    widgets_json: JsonDict,
    apps_json: list[JsonDict] | None = None,
) -> JsonDict:
    backend_name = "Wave One Risk Service"
    signal_id = "wave_one_risk_signal"
    state = _staged_dashboard(
        "Risk Service Staging",
        [
            {
                "origin": backend_name,
                "widget_id": signal_id,
                "widget_uuid": "seeded_risk_signal",
                "tab_id": "monitor",
                "layout": {"x": 0, "y": 0, "w": 40, "h": 10},
            }
        ],
        tabs=[{"id": "monitor", "name": "Monitor"}],
    )
    state["custom_backends"] = [
        {
            "backend_id": "backend_005",
            "name": backend_name,
            "url": "http://127.0.0.1:9506",
            "widgets_json": widgets_json,
            **({"apps_json": apps_json} if apps_json is not None else {}),
        }
    ]
    return state


def _build_extend_tasks() -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    spine = "risk_service_lifecycle"
    backend_name = "Wave One Risk Service"
    signal_name = "Wave One Risk Signal"
    signal_id = "wave_one_risk_signal"
    limit_name = "Wave One Limit Alert"
    limit_id = "wave_one_limit_alert"
    stress_name = "Wave One Stress Watch"
    stress_id = "wave_one_stress_watch"
    app_name = "Wave One Risk App"

    stale_signal = _widget_def(
        signal_name,
        "/risk-signal",
        description="Stale risk signal feed.",
        grid=(40, 10),
    )
    refreshed_signal = _widget_def(
        signal_name,
        "/risk-signal",
        description="Refreshed risk signal feed.",
        grid=(40, 10),
    )
    tasks.append(
        _record(
            "extend",
            spine,
            0,
            "platform",
            (
                "On the open Risk Service Staging board, review the connected backends and "
                "refresh Wave One Risk Service so its Wave One Risk Signal description is "
                "Refreshed risk signal feed."
            ),
            [
                _snapshot(),
                _call(
                    "manage_backends",
                    {"operation": "list"},
                    optional=True,
                ),
                _call(
                    "manage_backends",
                    {
                        "operation": "refresh",
                        "backend_id": "backend_005",
                        "widgets_json": {signal_id: refreshed_signal},
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=(
                _custom_target(
                    backend_name,
                    signal_id,
                    signal_name,
                    staged=True,
                ),
            ),
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": signal_id,
                    "expect": {},
                }
            ],
            selected_dashboard="Risk Service Staging",
            initial_state=_extend_seed({signal_id: stale_signal}),
        )
    )

    broken_app = {
        "name": app_name,
        "tabs": {
            "monitor": {
                "id": "monitor",
                "name": "Monitor",
                "layout": [
                    {"i": signal_id, "x": 0, "y": 0, "w": 30, "h": 10},
                    {"i": signal_id, "x": 20, "y": 0, "w": 20, "h": 10},
                ],
            }
        },
    }
    single_app = _app(
        app_name,
        [("monitor", "Monitor", [(signal_id, 0, 0, 40, 10, None)])],
    )
    tasks.append(
        _record(
            "extend",
            spine,
            1,
            "platform",
            (
                "Review the connected backends on the open Risk Service Staging board, "
                "then refresh Wave One Risk Service so Wave One Risk App has "
                "one non-overlapping Wave One Risk Signal placement on Monitor."
            ),
            [
                _snapshot(),
                _call(
                    "manage_backends",
                    {"operation": "list"},
                    optional=True,
                ),
                _call(
                    "manage_backends",
                    {
                        "operation": "refresh",
                        "backend_id": "backend_005",
                        "widgets_json": {signal_id: refreshed_signal},
                        "apps_json": [single_app],
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=(
                _custom_target(
                    backend_name,
                    signal_id,
                    signal_name,
                    staged=True,
                ),
            ),
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["monitor"],
                    "layout_refs_valid": True,
                    "no_overlaps": True,
                }
            ],
            selected_dashboard="Risk Service Staging",
            initial_state=_extend_seed(
                {signal_id: stale_signal},
                [broken_app],
            ),
        )
    )

    tasks.append(
        _record(
            "extend",
            spine,
            2,
            "platform",
            (
                "Add a minimal Wave One Risk Service backend that serves a Wave One Risk "
                "Signal table at /risk-signal."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9506",
                        "widgets_json": {signal_id: refreshed_signal},
                    },
                    graded_args=("operation", "name"),
                )
            ],
            targets=(_custom_target(backend_name, signal_id, signal_name),),
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": signal_id,
                    "expect": {"type": "table"},
                }
            ],
        )
    )
    tasks.append(
        _record(
            "extend",
            spine,
            3,
            "platform",
            (
                "The risk desk needs Wave One Risk Service with its Wave One Risk Signal "
                "and a Wave One Risk App containing Monitor. Publish and add it. Widget ids "
                "are the snake_case of widget names; tab ids are the snake_case of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9506",
                        "widgets_json": {signal_id: refreshed_signal},
                        "apps_json": [single_app],
                    },
                    graded_args=("operation", "name"),
                )
            ],
            targets=(_custom_target(backend_name, signal_id, signal_name),),
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": signal_id,
                    "expect": {},
                }
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["monitor"],
                    "layout_refs_valid": True,
                }
            ],
        )
    )

    limit_def = _widget_def(limit_name, "/limit-alert", grid=(20, 10))
    two_widgets = {signal_id: refreshed_signal, limit_id: limit_def}
    two_app = _app(
        app_name,
        [
            (
                "monitor",
                "Monitor",
                [
                    (signal_id, 0, 0, 20, 10, None),
                    (limit_id, 20, 0, 20, 10, None),
                ],
            )
        ],
    )
    tasks.append(
        _record(
            "extend",
            spine,
            4,
            "platform",
            (
                "Set up Wave One Risk Service with Wave One Risk Signal and Wave One Limit "
                "Alert. Author and add the service, publish Wave One Risk App with both on "
                "Monitor, and instantiate it. Widget ids are the snake_case of widget names; "
                "tab ids are the snake_case of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9506",
                        "widgets_json": two_widgets,
                        "apps_json": [two_app],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "Wave One Risk Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=(
                _custom_target(backend_name, signal_id, signal_name),
                _custom_target(backend_name, limit_id, limit_name),
            ),
            required_widgets=[
                _required_widget(backend_name, signal_id, tab_id="monitor"),
                _required_widget(backend_name, limit_id, tab_id="monitor"),
            ],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": signal_id,
                    "expect": {},
                },
                {
                    "backend_name": backend_name,
                    "widget_id": limit_id,
                    "expect": {},
                },
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["monitor"],
                    "layout_refs_valid": True,
                    "no_overlaps": True,
                }
            ],
        )
    )

    stress_def = _widget_def(stress_name, "/stress-watch", grid=(40, 10))
    three_widgets = {**two_widgets, stress_id: stress_def}
    three_app = _app(
        app_name,
        [
            (
                "monitor",
                "Monitor",
                [
                    (signal_id, 0, 0, 20, 10, None),
                    (limit_id, 20, 0, 20, 10, None),
                ],
            ),
            ("stress", "Stress", [(stress_id, 0, 0, 40, 10, None)]),
        ],
    )
    tasks.append(
        _record(
            "extend",
            spine,
            5,
            "platform",
            (
                "Complete the risk desk build with Wave One Risk Service, Wave One Risk "
                "Signal, Wave One Limit Alert, and Wave One Stress Watch. Add the service, "
                "publish Wave One Risk App with Monitor and Stress tabs, and instantiate it. "
                "Widget ids are the snake_case of widget names; tab ids are the snake_case "
                "of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9506",
                        "widgets_json": three_widgets,
                        "apps_json": [three_app],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "Wave One Risk Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=(
                _custom_target(backend_name, signal_id, signal_name),
                _custom_target(backend_name, limit_id, limit_name),
                _custom_target(backend_name, stress_id, stress_name),
            ),
            required_widgets=[
                _required_widget(backend_name, signal_id, tab_id="monitor"),
                _required_widget(backend_name, limit_id, tab_id="monitor"),
                _required_widget(backend_name, stress_id, tab_id="stress"),
            ],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": signal_id,
                    "expect": {},
                },
                {
                    "backend_name": backend_name,
                    "widget_id": limit_id,
                    "expect": {},
                },
                {
                    "backend_name": backend_name,
                    "widget_id": stress_id,
                    "expect": {},
                },
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["monitor", "stress"],
                    "layout_refs_valid": True,
                    "no_overlaps": True,
                }
            ],
        )
    )
    return tasks


def _handoff_stage() -> JsonDict:
    return _staged_dashboard("Earnings Handoff", [])


def _build_handoff_tasks() -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    spine = "earnings_handoff"
    stage = _handoff_stage()
    source = ("stark-enterprise-x", EARNINGS_WIDGET)

    specs = (
        (
            0,
            "On the open Earnings Handoff board, read Bench Stark Enterprise's Earnings & "
            "Estimates Monitor, Upcoming Earnings, for Healthcare, LLY, and YTD. Add an LLY "
            "Earnings Handoff note with the exact score and status.",
            {"sector": "Healthcare", "ticker": "LLY", "period": "YTD"},
            "LLY Earnings Handoff",
            ("27.63", "Open"),
            (),
        ),
        (
            1,
            "Build the Apple note on the open Earnings Handoff board. Find "
            "Bench Stark Enterprise's Earnings & Estimates Monitor, Upcoming Earnings, for "
            "Technology, AAPL, and QTD, then add an Apple Earnings Handoff note with the "
            "exact score and status.",
            {"sector": "Technology", "ticker": "AAPL", "period": "QTD"},
            "Apple Earnings Handoff",
            ("6.52", "In Review"),
            (),
        ),
        (
            2,
            "Prepare a Microsoft note on the open Earnings Handoff board under the "
            "current-month handoff policy. Read Bench Stark Enterprise's Earnings & "
            "Estimates Monitor, Upcoming Earnings, for Technology and MSFT; current month "
            "means MTD. Add a Microsoft Earnings Handoff note with the exact score and status.",
            {"sector": "Technology", "ticker": "MSFT", "period": "MTD"},
            "Microsoft Earnings Handoff",
            ("89.94", "Escalated"),
            (PolicyMapping("current-month handoff policy", ("MTD",)),),
        ),
    )
    for level, prompt, data_args, note_name, tokens, policies in specs:
        tools: list[JsonDict] = []
        if level in {0, 1}:
            tools.append(_snapshot())
        if level == 1:
            tools.extend(
                [
                    _call(
                        "list_available_widgets",
                        {"origin": STARK},
                        optional=True,
                    ),
                    _call(
                        "get_widget_schema",
                        {"origin": STARK, "widget_id": EARNINGS_WIDGET},
                        optional=True,
                    ),
                ]
            )
        tools.extend(
            [
                _call(
                    "get_widget_data",
                    {
                        "origin": STARK,
                        "widget_id": EARNINGS_WIDGET,
                        "data_args": data_args,
                    },
                    graded_args=("origin", "widget_id"),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": note_name,
                        "data": f"Score {tokens[0]}; status {tokens[1]}.",
                    },
                    graded_args=("widget_type", "name"),
                ),
            ]
        )
        tasks.append(
            _record(
                "handoff",
                spine,
                level,
                "read",
                prompt,
                tools,
                targets=(_earnings_target(),),
                policies=policies,
                required_generated_widgets=[
                    {
                        "widget_type": "note",
                        "name_contains": note_name,
                        "data_contains": list(tokens),
                    }
                ],
                grounded_generated=(GroundedGenerated(source[0], source[1], tokens),),
                selected_dashboard="Earnings Handoff",
                initial_state=stage,
            )
        )

    tasks.append(
        _record(
            "handoff",
            spine,
            3,
            "platform",
            (
                "For the open Earnings Handoff board, follow Finance Earnings Prep "
                "governance and read Bench Stark Enterprise's Earnings & Estimates Monitor, "
                "Upcoming Earnings, for Technology, AAPL, and QTD. Add a Governed Apple "
                "Handoff note with the exact score and status."
            ),
            [
                _call(
                    "get_skill_content",
                    {"slug": "finance-earnings-prep"},
                    graded_args=("slug",),
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
                    graded_args=("origin", "widget_id"),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "Governed Apple Handoff",
                        "data": "Score 6.52; status In Review.",
                    },
                    graded_args=("widget_type", "name"),
                ),
            ],
            targets=(_earnings_target(),),
            policies=(
                PolicyMapping(
                    "Finance Earnings Prep governance",
                    ("finance-earnings-prep",),
                ),
            ),
            required_generated_widgets=[
                {
                    "widget_type": "note",
                    "name_contains": "Governed Apple Handoff",
                    "data_contains": ["6.52", "In Review"],
                }
            ],
            grounded_generated=(GroundedGenerated(source[0], source[1], ("6.52", "In Review")),),
            selected_dashboard="Earnings Handoff",
            initial_state=stage,
        )
    )

    task_request = {
        "id": "coverage_follow_up",
        "description": "Review LLY earnings risks and next actions.",
        "assigned_holder_url": "workspace://agents/coverage",
        "assigned_agent_id": "coverage-agent",
    }
    tasks.append(
        _record(
            "handoff",
            spine,
            4,
            "platform",
            (
                "Handle the coverage follow-up route from the open Earnings Handoff board "
                "under Finance Earnings Prep governance. Read Bench Stark Enterprise's "
                "Earnings & Estimates Monitor, Upcoming Earnings, for Healthcare, LLY, and "
                "YTD; add an LLY Delegation Handoff note with exact score and status, then "
                "delegate the coverage follow-up."
            ),
            [
                _call(
                    "get_skill_content",
                    {"slug": "finance-earnings-prep"},
                    graded_args=("slug",),
                ),
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
                    graded_args=("origin", "widget_id"),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "LLY Delegation Handoff",
                        "data": "Score 27.63; status Open.",
                    },
                    graded_args=("widget_type", "name"),
                ),
                _call(
                    "assign_tasks_to_agents",
                    {"task_requests": [task_request]},
                    graded_args=(),
                ),
            ],
            targets=(_earnings_target(),),
            policies=(
                PolicyMapping(
                    "Finance Earnings Prep governance",
                    ("finance-earnings-prep",),
                ),
                PolicyMapping(
                    "coverage follow-up route",
                    tuple(task_request.values()),
                ),
            ),
            required_generated_widgets=[
                {
                    "widget_type": "note",
                    "name_contains": "LLY Delegation Handoff",
                    "data_contains": ["27.63", "Open"],
                }
            ],
            grounded_generated=(GroundedGenerated(source[0], source[1], ("27.63", "Open")),),
            selected_dashboard="Earnings Handoff",
            initial_state=stage,
        )
    )

    backend_name = "Earnings Handoff Backend"
    widget_name = "Earnings Handoff Register"
    widget_id = "earnings_handoff_register"
    app_name = "Earnings Handoff App"
    note_name = "Earnings Build Handoff"
    widget_def = _widget_def(widget_name, "/earnings-handoff")
    app_def = _app(
        app_name,
        [("handoff", "Handoff", [(widget_id, 0, 0, 40, 10, None)])],
    )
    build_follow_up = {
        "id": "earnings_build_review",
        "description": "Review the Earnings Handoff App build and ownership.",
        "assigned_holder_url": "workspace://agents/coverage",
        "assigned_agent_id": "coverage-agent",
    }
    tasks.append(
        _record(
            "handoff",
            spine,
            5,
            "platform",
            (
                "From the open Earnings Handoff board, author and add a minimal custom "
                "Earnings Handoff Backend with one Earnings Handoff Register. Publish and "
                "instantiate Earnings Handoff App with one Handoff tab, add an Earnings "
                "Build Handoff note naming Earnings Handoff App and Earnings Handoff "
                "Register, then delegate the build-review follow-up. Widget ids are the "
                "snake_case of widget names; tab ids are the snake_case of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9508",
                        "widgets_json": {widget_id: widget_def},
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "Earnings Handoff Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": note_name,
                        "data": f"Built {app_name} with {widget_name}; review ownership.",
                    },
                    graded_args=("widget_type", "name"),
                ),
                # Grade delegation existence only; the authored artifacts and
                # durable note carry the exact handoff-content checks.
                _call(
                    "assign_tasks_to_agents",
                    {"task_requests": [build_follow_up]},
                    graded_args=(),
                ),
            ],
            targets=(_custom_target(backend_name, widget_id, widget_name),),
            required_widgets=[
                _required_widget(backend_name, widget_id, tab_id="handoff"),
            ],
            required_generated_widgets=[
                {
                    "widget_type": "note",
                    "name_contains": note_name,
                    "data_contains": [app_name, widget_name],
                }
            ],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": widget_id,
                    "expect": {},
                }
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["handoff"],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": "handoff", "widget_id": widget_id}],
                }
            ],
            selected_dashboard="Earnings Handoff",
            initial_state=stage,
        )
    )
    return tasks


def _build_retrieve_wave2_tasks() -> list[TaskRecord]:
    """Build the Daloopa closing-tape retrieval spine."""

    tasks: list[TaskRecord] = []
    spine = "closing_tape_lookup"
    target = _target(
        DALOOPA,
        DALOOPA_STOCK_PRICES_WIDGET,
        "Stock Prices",
        "daily OHLCV rows",
    )
    source = ("support-daloopa-skills", DALOOPA_STOCK_PRICES_WIDGET)
    low_specs = (
        (
            0,
            "Read the daily OHLCV rows in Bench Daloopa's Stock Prices with ticker set to "
            "NVDA, then report the latest date and exact close.",
            "NVDA",
            ["2026-07-10", "190.01"],
            "NVDA's latest row is dated 2026-07-10 with an exact close of 190.01.",
        ),
        (
            1,
            "Find the daily OHLCV rows in Bench Daloopa's Stock Prices for Netflix and give "
            "me the latest date and exact close.",
            "NFLX",
            ["2026-07-10", "1259.96"],
            "Netflix's latest row is dated 2026-07-10 with an exact close of 1259.96.",
        ),
    )
    for level, prompt, ticker, values, answer in low_specs:
        tools = [_snapshot()]
        if level == 1:
            tools.extend(
                [
                    _call("list_available_widgets", {"origin": DALOOPA}, optional=True),
                    _call(
                        "get_widget_schema",
                        {"origin": DALOOPA, "widget_id": DALOOPA_STOCK_PRICES_WIDGET},
                        optional=True,
                    ),
                ]
            )
        tools.append(
            _call(
                "get_widget_data",
                {
                    "origin": DALOOPA,
                    "widget_id": DALOOPA_STOCK_PRICES_WIDGET,
                    "data_args": {"ticker": ticker},
                },
                graded_args=("origin", "widget_id"),
            )
        )
        tasks.append(
            _record(
                "retrieve",
                spine,
                level,
                "read",
                prompt,
                tools,
                targets=(target,),
                required_values=values,
                reference_answer=answer,
                answer_source=source,
            )
        )

    tasks.append(
        _record(
            "retrieve",
            spine,
            2,
            "read",
            (
                "Pull the latest date and exact close from the daily OHLCV rows in Bench "
                "Daloopa's Stock Prices for the EV tape policy; that policy means the "
                "Tesla coverage name."
            ),
            [
                _call(
                    "get_params_options",
                    {
                        "origin": DALOOPA,
                        "widget_id": DALOOPA_STOCK_PRICES_WIDGET,
                        "param_name": "ticker",
                    },
                    optional=True,
                ),
                _call(
                    "get_widget_data",
                    {
                        "origin": DALOOPA,
                        "widget_id": DALOOPA_STOCK_PRICES_WIDGET,
                        "data_args": {"ticker": "TSLA"},
                    },
                    graded_args=("origin", "widget_id"),
                ),
            ],
            targets=(target,),
            policies=(PolicyMapping("EV tape policy", ("TSLA",)),),
            required_values=["2026-07-10", "325.5"],
            reference_answer="Tesla's latest row is dated 2026-07-10 with an exact close of 325.5.",
            answer_source=source,
        )
    )

    staged = _staged_dashboard(
        "Closing Tape Review",
        [
            {
                "origin": DALOOPA,
                "widget_id": DALOOPA_STOCK_PRICES_WIDGET,
                "tab_id": "review",
                "data_args": {"ticker": "MSFT"},
                "layout": {"x": 0, "y": 0, "w": 40, "h": 14},
            }
        ],
    )
    tasks.append(
        _record(
            "retrieve",
            spine,
            3,
            "read",
            (
                "On the open Closing Tape Review board, read the daily OHLCV rows in Bench "
                "Daloopa's configured Stock Prices view without changing it and report the "
                "latest date, exact close, and volume."
            ),
            [
                _snapshot(),
                _call(
                    "get_widget_data",
                    {
                        "origin": DALOOPA,
                        "widget_id": DALOOPA_STOCK_PRICES_WIDGET,
                        "data_args": {"ticker": "MSFT"},
                    },
                    graded_args=("origin", "widget_id"),
                ),
            ],
            targets=(_target(DALOOPA, DALOOPA_STOCK_PRICES_WIDGET, "Stock Prices", staged=True),),
            required_values=["2026-07-10", "542.46", "16457690"],
            reference_answer=(
                "The configured Microsoft view ends on 2026-07-10 at 542.46 with volume 16457690."
            ),
            answer_source=source,
            selected_dashboard="Closing Tape Review",
            initial_state=staged,
        )
    )
    tasks.append(
        _record(
            "retrieve",
            spine,
            4,
            "read",
            (
                "Use Daloopa Tearsheet governance to review the daily OHLCV rows in Bench "
                "Daloopa's Stock Prices for Apple, then report the latest date and exact "
                "close."
            ),
            [
                _call(
                    "get_skill_content",
                    {"slug": "daloopa-tearsheet"},
                    graded_args=("slug",),
                ),
                _call(
                    "get_widget_data",
                    {
                        "origin": DALOOPA,
                        "widget_id": DALOOPA_STOCK_PRICES_WIDGET,
                        "data_args": {"ticker": "AAPL"},
                    },
                    graded_args=("origin", "widget_id"),
                ),
            ],
            targets=(target,),
            policies=(PolicyMapping("Daloopa Tearsheet governance", ("daloopa-tearsheet",)),),
            required_values=["2026-07-10", "266.02"],
            reference_answer="Apple's governed latest row is dated 2026-07-10 at 266.02.",
            answer_source=source,
        )
    )

    backend_name = "Wave Two Closing Tape"
    widget_name = "Closing Tape Lookup"
    widget_id = "closing_tape_lookup"
    app_name = "Closing Tape App"
    widget_def = _widget_def(
        widget_name,
        "/closing-tape",
        description="Latest closing-tape lookup.",
        params=[
            {
                "paramName": "ticker",
                "type": "text",
                "label": "Ticker",
                "value": "NVDA",
                "options": [{"label": "NVDA", "value": "NVDA"}],
            }
        ],
    )
    app_def = _app(
        app_name,
        [("tape", "Tape", [(widget_id, 0, 0, 40, 10, {"ticker": "NVDA"})])],
    )
    tasks.append(
        _record(
            "retrieve",
            spine,
            5,
            "platform",
            (
                "Build and add a Wave Two Closing Tape backend with a Closing Tape Lookup "
                "table "
                "for NVDA, instantiate its Closing Tape App, read the result, and report "
                "the latest date and exact close. Follow the widgets manifest "
                "specification. Widget ids are the snake_case of widget names; tab ids are "
                "the snake_case of tab names."
            ),
            [
                _call(
                    "read_workspace_resource",
                    {"uri": "openbb://workspace/specs/widgets-json"},
                    graded_args=("uri",),
                ),
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9601",
                        "widgets_json": {widget_id: widget_def},
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "Closing Tape Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
                _call(
                    "get_widget_data",
                    {
                        "origin": backend_name,
                        "widget_id": widget_id,
                        "data_args": {"ticker": "NVDA"},
                    },
                    graded_args=("origin", "widget_id"),
                ),
            ],
            targets=(_custom_target(backend_name, widget_id, widget_name),),
            policies=(
                PolicyMapping(
                    "widgets manifest specification",
                    ("openbb://workspace/specs/widgets-json",),
                ),
            ),
            pinned_widget_args={(backend_name, widget_id): frozenset({"ticker"})},
            required_widgets=[
                _required_widget(
                    backend_name,
                    widget_id,
                    {"ticker": "NVDA"},
                    tab_id="tape",
                )
            ],
            required_values=["2026-07-10", "190.01"],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": widget_id,
                    "expect": {"type": "table"},
                }
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["tape"],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": "tape", "widget_id": widget_id}],
                }
            ],
            runtime_checks={
                "datasets": [
                    {
                        "name": "wave2-closing-tape",
                        "widget_id": widget_id,
                        "fields": ["ticker", "date", "close"],
                        "path": "/closing-tape",
                        "payload": [{"ticker": "NVDA", "date": "2026-07-10", "close": 190.01}],
                    }
                ]
            },
            reference_answer="The NVDA lookup ends on 2026-07-10 at 190.01.",
            answer_source=source,
        )
    )
    return tasks


def _build_curate_wave2_tasks() -> list[TaskRecord]:
    """Build the cross-catalog market-telemetry curation spine."""

    tasks: list[TaskRecord] = []
    spine = "market_telemetry"
    stage = _staged_dashboard("Wave Two Market Telemetry", [])
    spark_target = _target(
        GETTING_STARTED,
        SPARKLINE_WIDGET,
        "Stock Price Trends - Line Sparklines with First/Last Points",
    )
    ratio_target = _target(
        WIDGET_EXAMPLES, RATIO_TABS_WIDGET, "[MOCK DATA] Tabs + Dropdown Combined"
    )

    tasks.append(
        _record(
            "curate",
            spine,
            0,
            "single-widget",
            (
                "Add Getting Started's Stock Price Trends - Line Sparklines with First/Last "
                "Points to the open Wave Two Market Telemetry board."
            ),
            [
                _snapshot(),
                _call("list_available_widgets", {"origin": GETTING_STARTED}, optional=True),
                _call(
                    "create_widget",
                    {"origin": GETTING_STARTED, "widget_id": SPARKLINE_WIDGET},
                    graded_args=("origin",),
                ),
            ],
            targets=(spark_target,),
            required_widgets=[_required_widget(GETTING_STARTED, SPARKLINE_WIDGET)],
            selected_dashboard="Wave Two Market Telemetry",
            initial_state=stage,
        )
    )
    live_args = {"symbol": "AAPL"}
    tasks.append(
        _record(
            "curate",
            spine,
            1,
            "single-widget",
            (
                "On the open Wave Two Market Telemetry board, add Getting Started's "
                "live-updating grid with real-time WebSocket updates for AAPL."
            ),
            [
                _snapshot(),
                _call("list_available_widgets", {"origin": GETTING_STARTED}, optional=True),
                _call(
                    "get_widget_schema",
                    {"origin": GETTING_STARTED, "widget_id": LIVE_GRID_WIDGET},
                    optional=True,
                ),
                _call(
                    "create_widget",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": LIVE_GRID_WIDGET,
                        "data_args": live_args,
                    },
                    graded_args=("origin", "data_args"),
                ),
            ],
            targets=(
                _target(
                    GETTING_STARTED,
                    LIVE_GRID_WIDGET,
                    "Live Grid",
                    "Getting Started",
                    "real-time WebSocket updates",
                ),
            ),
            pinned_widget_args={(GETTING_STARTED, LIVE_GRID_WIDGET): frozenset({"symbol"})},
            required_widgets=[_required_widget(GETTING_STARTED, LIVE_GRID_WIDGET, live_args)],
            selected_dashboard="Wave Two Market Telemetry",
            initial_state=stage,
        )
    )
    ratio_args = {"period": "quarterly", "category": "liquidity"}
    tasks.append(
        _record(
            "curate",
            spine,
            2,
            "single-widget",
            (
                "Prepare the open Wave Two Market Telemetry board for the quarterly "
                "liquidity policy. Add Widget Examples' [MOCK DATA] Tabs + Dropdown "
                "Combined; quarterly liquidity means quarterly and liquidity. Place it at "
                "x 0, y 0, width 40, height 14."
            ),
            [
                _call("list_available_widgets", {"origin": WIDGET_EXAMPLES}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": WIDGET_EXAMPLES,
                        "widget_id": RATIO_TABS_WIDGET,
                        "data_args": ratio_args,
                    },
                    graded_args=("origin", "data_args"),
                ),
                _call(
                    "update_widget_layout",
                    {
                        "widget_id": RATIO_TABS_WIDGET,
                        "x": 0,
                        "y": 0,
                        "w": 40,
                        "h": 14,
                    },
                    graded_args=("x", "y", "w", "h"),
                ),
            ],
            targets=(ratio_target,),
            policies=(PolicyMapping("quarterly liquidity policy", ("quarterly", "liquidity")),),
            pinned_widget_args={(WIDGET_EXAMPLES, RATIO_TABS_WIDGET): frozenset(ratio_args)},
            required_widgets=[_required_widget(WIDGET_EXAMPLES, RATIO_TABS_WIDGET, ratio_args)],
            selected_dashboard="Wave Two Market Telemetry",
            initial_state=stage,
        )
    )

    for level in (3, 4):
        prompt = (
            "Build out the open Wave Two Market Telemetry board with Getting Started's "
            "Stock Price Trends - Line Sparklines with First/Last Points beside Widget "
            "Examples' [MOCK DATA] "
            "Tabs + Dropdown Combined for quarterly liquidity. Put the trends at x 0, y "
            "0, width 20, height 12 and the ratio view at x 20, y 0, width 20, height 12."
            if level == 3
            else "Using Workspace session guidance, finish the open Wave Two Market "
            "Telemetry board with Getting Started's Stock Price Trends - Line Sparklines "
            "with First/Last Points beside Widget Examples' [MOCK DATA] Tabs + Dropdown "
            "Combined for quarterly "
            "liquidity. Put them at x 0 and x 20, y 0, each width 20 and height 12."
        )
        tools: list[JsonDict] = []
        policies: tuple[PolicyMapping, ...] = ()
        if level == 4:
            tools.append(
                _call(
                    "get_workspace_prompt",
                    {"name": "workspace_session_context"},
                    graded_args=("name",),
                )
            )
            policies = (
                PolicyMapping("Workspace session guidance", ("workspace_session_context",)),
            )
        tools.extend(
            [
                _call("list_available_widgets", {"origin": GETTING_STARTED}, optional=True),
                _call("list_available_widgets", {"origin": WIDGET_EXAMPLES}, optional=True),
                _call(
                    "create_widget",
                    {"origin": GETTING_STARTED, "widget_id": SPARKLINE_WIDGET},
                    graded_args=("origin",),
                ),
                _call(
                    "create_widget",
                    {
                        "origin": WIDGET_EXAMPLES,
                        "widget_id": RATIO_TABS_WIDGET,
                        "data_args": ratio_args,
                    },
                    graded_args=("origin", "data_args"),
                ),
                _call(
                    "update_widget_layout",
                    {"widget_id": SPARKLINE_WIDGET, "x": 0, "y": 0, "w": 20, "h": 12},
                    graded_args=("x", "y", "w", "h"),
                ),
                _call(
                    "update_widget_layout",
                    {"widget_id": RATIO_TABS_WIDGET, "x": 20, "y": 0, "w": 20, "h": 12},
                    graded_args=("x", "y", "w", "h"),
                ),
            ]
        )
        tasks.append(
            _record(
                "curate",
                spine,
                level,
                "dashboard",
                prompt,
                tools,
                targets=(spark_target, ratio_target),
                policies=policies,
                pinned_widget_args={(WIDGET_EXAMPLES, RATIO_TABS_WIDGET): frozenset(ratio_args)},
                required_widgets=[
                    _required_widget(GETTING_STARTED, SPARKLINE_WIDGET),
                    _required_widget(WIDGET_EXAMPLES, RATIO_TABS_WIDGET, ratio_args),
                ],
                selected_dashboard="Wave Two Market Telemetry",
                initial_state=stage,
            )
        )

    backend_name = "Telemetry Summary Backend"
    custom_name = "Telemetry Summary Tile"
    custom_id = "telemetry_summary_tile"
    app_name = "Market Telemetry App"
    custom_def = _widget_def(custom_name, "/telemetry-summary", widget_type="metric", grid=(40, 10))
    app_def = _app(app_name, [("monitor", "Monitor", [(custom_id, 0, 0, 40, 10, None)])])
    tasks.append(
        _record(
            "curate",
            spine,
            5,
            "platform",
            (
                "Author and add a Telemetry Summary Backend with a Telemetry Summary Tile "
                "metric, "
                "then instantiate its Market Telemetry App. On Monitor, place Getting "
                "Started's Stock Price Trends - Line Sparklines with First/Last Points "
                "beside Widget Examples' "
                "[MOCK DATA] Tabs + Dropdown Combined at y 10, x 0 and x 20, each width 20 "
                "and height 12. Widget ids are the snake_case of widget names; tab ids are "
                "the snake_case of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9602",
                        "widgets_json": {custom_id: custom_def},
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "Market Telemetry Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
                _call("list_available_widgets", {"origin": GETTING_STARTED}, optional=True),
                _call("list_available_widgets", {"origin": WIDGET_EXAMPLES}, optional=True),
                _call(
                    "create_widget",
                    {"origin": GETTING_STARTED, "widget_id": SPARKLINE_WIDGET},
                    graded_args=("origin",),
                ),
                _call(
                    "create_widget",
                    {"origin": WIDGET_EXAMPLES, "widget_id": RATIO_TABS_WIDGET},
                    graded_args=("origin",),
                ),
                _call(
                    "update_widget_layout",
                    {
                        "widget_id": SPARKLINE_WIDGET,
                        "x": 0,
                        "y": 10,
                        "w": 20,
                        "h": 12,
                        "tab_id": "monitor",
                    },
                    optional=True,
                ),
                _call(
                    "update_widget_layout",
                    {
                        "widget_id": RATIO_TABS_WIDGET,
                        "x": 20,
                        "y": 10,
                        "w": 20,
                        "h": 12,
                        "tab_id": "monitor",
                    },
                    optional=True,
                ),
            ],
            targets=(
                _custom_target(backend_name, custom_id, custom_name),
                spark_target,
                ratio_target,
            ),
            required_widgets=[
                _required_widget(GETTING_STARTED, SPARKLINE_WIDGET, tab_id="monitor"),
                _required_widget(WIDGET_EXAMPLES, RATIO_TABS_WIDGET, tab_id="monitor"),
                # Instantiation is a state outcome: the authored widget must
                # exist in the workspace, not merely be defined.
                _required_widget(backend_name, custom_id),
            ],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": custom_id,
                    "expect": {"type": "metric"},
                }
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["monitor"],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": "monitor", "widget_id": custom_id}],
                }
            ],
        )
    )
    return tasks


def _crypto_document_stage() -> JsonDict:
    return _staged_dashboard(
        "Crypto Document Controls",
        [
            {
                "origin": WIDGET_EXAMPLES,
                "widget_id": WHITEPAPERS_WIDGET,
                "tab_id": "review",
                "data_args": {"filenames": "bitcoin.pdf", "category": "all"},
                "layout": {"x": 0, "y": 0, "w": 20, "h": 14},
            },
            {
                "origin": WIDGET_EXAMPLES,
                "widget_id": COINDESK_WIDGET,
                "tab_id": "review",
                "data_args": {"limit": 10, "lang": "EN"},
                "layout": {"x": 20, "y": 0, "w": 20, "h": 14},
            },
            {
                "origin": GETTING_STARTED,
                "widget_id": MULTI_PDF_WIDGET,
                "tab_id": "review",
                "data_args": {"pdf_name": "Bitcoin Whitepaper"},
                "layout": {"x": 0, "y": 14, "w": 40, "h": 14},
            },
        ],
    )


def _build_parameterize_wave2_tasks() -> list[TaskRecord]:
    """Build the crypto-document parameter-surgery spine."""

    tasks: list[TaskRecord] = []
    spine = "crypto_document_controls"
    stage = _crypto_document_stage()
    white_target = _target(
        WIDGET_EXAMPLES,
        WHITEPAPERS_WIDGET,
        "Whitepapers",
        staged=True,
    )
    news_target = _target(WIDGET_EXAMPLES, COINDESK_WIDGET, "CoinDesk News", staged=True)
    pdf_target = _target(
        GETTING_STARTED,
        MULTI_PDF_WIDGET,
        "Multi PDF Viewer - Base64",
        staged=True,
    )

    low_specs = (
        (
            0,
            (
                "On the open Crypto Document Controls board, set Whitepapers with "
                "filenames set to ethereum.pdf and category set to l1, preserving every "
                "other view."
            ),
            {"filenames": "ethereum.pdf", "category": "l1"},
            (),
        ),
        (
            1,
            (
                "Use the whitepaper PDF on the open Crypto Document Controls board to "
                "show Solana's solana.pdf from the l1 collection, leaving the rest alone."
            ),
            {"filenames": "solana.pdf", "category": "l1"},
            (),
        ),
        (
            2,
            (
                "Apply the DeFi research set to Whitepapers on the open Crypto Document "
                "Controls board and preserve the surrounding document views."
            ),
            {"filenames": "solana.pdf", "category": "defi"},
            (PolicyMapping("DeFi research set", ("solana.pdf", "defi")),),
        ),
    )
    for level, prompt, data_args, policies in low_specs:
        tools: list[JsonDict] = []
        if level in {0, 1}:
            tools.append(_snapshot())
        if level == 1:
            tools.append(_call("read_widget", {"widget_id": WHITEPAPERS_WIDGET}, optional=True))
        tools.append(
            _call(
                "update_widget",
                {"widget_id": WHITEPAPERS_WIDGET, "data_args": data_args},
                graded_args=("data_args",),
            )
        )
        tasks.append(
            _record(
                "parameterize",
                spine,
                level,
                "single-widget",
                prompt,
                tools,
                targets=(white_target,),
                policies=policies,
                pinned_widget_args={(WIDGET_EXAMPLES, WHITEPAPERS_WIDGET): frozenset(data_args)},
                required_widgets=[_required_widget(WIDGET_EXAMPLES, WHITEPAPERS_WIDGET, data_args)],
                selected_dashboard="Crypto Document Controls",
                initial_state=stage,
            )
        )

    ethereum_args = {"filenames": "ethereum.pdf", "category": "l1"}
    tasks.append(
        _record(
            "parameterize",
            spine,
            3,
            "single-widget",
            (
                "Retune Whitepapers on the open Crypto Document Controls board to "
                "ethereum.pdf from l1. Keep CoinDesk News and every other view unchanged."
            ),
            [
                _snapshot(),
                _call(
                    "update_widget",
                    {"widget_id": WHITEPAPERS_WIDGET, "data_args": ethereum_args},
                    graded_args=("data_args",),
                ),
            ],
            targets=(white_target, news_target),
            pinned_widget_args={(WIDGET_EXAMPLES, WHITEPAPERS_WIDGET): frozenset(ethereum_args)},
            required_widgets=[
                _required_widget(WIDGET_EXAMPLES, WHITEPAPERS_WIDGET, ethereum_args),
                _required_widget(WIDGET_EXAMPLES, COINDESK_WIDGET),
            ],
            selected_dashboard="Crypto Document Controls",
            initial_state=stage,
        )
    )
    news_args = {"limit": 6, "lang": "ES"}
    tasks.append(
        _record(
            "parameterize",
            spine,
            4,
            "single-widget",
            (
                "Using Workspace session guidance, prepare the open Crypto Document "
                "Controls board with Whitepapers on ethereum.pdf from l1 and CoinDesk News "
                "limited to 6 in ES. Preserve the PDF viewer."
            ),
            [
                _call(
                    "get_workspace_prompt",
                    {"name": "workspace_session_context"},
                    graded_args=("name",),
                ),
                _call(
                    "update_widget",
                    {"widget_id": WHITEPAPERS_WIDGET, "data_args": ethereum_args},
                    graded_args=("data_args",),
                ),
                _call(
                    "update_widget",
                    {"widget_id": COINDESK_WIDGET, "data_args": news_args},
                    graded_args=("data_args",),
                ),
            ],
            targets=(white_target, news_target, pdf_target),
            policies=(PolicyMapping("Workspace session guidance", ("workspace_session_context",)),),
            pinned_widget_args={
                (WIDGET_EXAMPLES, WHITEPAPERS_WIDGET): frozenset(ethereum_args),
                (WIDGET_EXAMPLES, COINDESK_WIDGET): frozenset(news_args),
            },
            required_widgets=[
                _required_widget(WIDGET_EXAMPLES, WHITEPAPERS_WIDGET, ethereum_args),
                _required_widget(WIDGET_EXAMPLES, COINDESK_WIDGET, news_args),
            ],
            selected_dashboard="Crypto Document Controls",
            initial_state=stage,
        )
    )
    pdf_args = {"pdf_name": "Bitcoin Whitepaper"}
    tasks.append(
        _record(
            "parameterize",
            spine,
            5,
            "single-widget",
            (
                "Finish the existing views on the open Crypto Document Controls board. "
                "Set Whitepapers to solana.pdf from l1, CoinDesk News to 8 in EN, and Multi "
                "PDF Viewer - Base64 to Bitcoin Whitepaper. Preserve all layout and other "
                "workspace content."
            ),
            [
                _call(
                    "update_widget",
                    {
                        "widget_id": WHITEPAPERS_WIDGET,
                        "data_args": {"filenames": "solana.pdf", "category": "l1"},
                    },
                    graded_args=("data_args",),
                ),
                _call(
                    "update_widget",
                    {
                        "widget_id": COINDESK_WIDGET,
                        "data_args": {"limit": 8, "lang": "EN"},
                    },
                    graded_args=("data_args",),
                ),
                _call(
                    "update_widget",
                    {"widget_id": MULTI_PDF_WIDGET, "data_args": pdf_args},
                    graded_args=("data_args",),
                ),
            ],
            targets=(white_target, news_target, pdf_target),
            pinned_widget_args={
                (WIDGET_EXAMPLES, WHITEPAPERS_WIDGET): frozenset({"filenames", "category"}),
                (WIDGET_EXAMPLES, COINDESK_WIDGET): frozenset({"limit", "lang"}),
                (GETTING_STARTED, MULTI_PDF_WIDGET): frozenset(pdf_args),
            },
            required_widgets=[
                _required_widget(
                    WIDGET_EXAMPLES,
                    WHITEPAPERS_WIDGET,
                    {"filenames": "solana.pdf", "category": "l1"},
                ),
                _required_widget(
                    WIDGET_EXAMPLES,
                    COINDESK_WIDGET,
                    {"limit": 8, "lang": "EN"},
                ),
                _required_widget(GETTING_STARTED, MULTI_PDF_WIDGET, pdf_args),
            ],
            selected_dashboard="Crypto Document Controls",
            initial_state=stage,
        )
    )
    return tasks


def _build_organize_wave2_tasks() -> list[TaskRecord]:
    """Build the client-onboarding navigation spine."""

    tasks: list[TaskRecord] = []
    spine = "client_onboarding_flow"
    board_name = "Wave Two Client Onboarding"
    tasks.append(
        _record(
            "organize",
            spine,
            0,
            "dashboard",
            (
                "For client operations, create a dashboard named Wave Two Client "
                "Onboarding and make it the active board."
            ),
            [
                _snapshot(),
                _call(
                    "manage_dashboard",
                    {"operation": "create", "name": board_name, "activate": True},
                    graded_args=("operation", "name"),
                ),
            ],
        )
    )
    tasks.append(
        _record(
            "organize",
            spine,
            1,
            "dashboard",
            (
                "Create and activate Wave Two Client Onboarding with Intake and Review "
                "tabs for the operations team."
            ),
            [
                _snapshot(),
                _call(
                    "manage_dashboard",
                    {"operation": "create", "name": board_name, "activate": True},
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_navigation_bar",
                    {"operation": "add_tabs", "tabs": [{"name": "Intake"}, {"name": "Review"}]},
                    graded_args=("tabs",),
                ),
            ],
        )
    )
    tasks.append(
        _record(
            "organize",
            spine,
            2,
            "dashboard",
            (
                "Operations needs you to create and activate Wave Two Client Onboarding "
                "with Intake, Review, and Approval tabs, then open Review."
            ),
            [
                _call(
                    "manage_dashboard",
                    {"operation": "create", "name": board_name, "activate": True},
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_navigation_bar",
                    {
                        "operation": "create",
                        "tabs": [
                            {"name": "Intake"},
                            {"name": "Review"},
                            {"name": "Approval"},
                        ],
                    },
                    optional=True,
                ),
                _call(
                    "navigate_workspace",
                    {"operation": "tab", "tab_id": "review"},
                    graded_args=("tab_id",),
                ),
            ],
            required_tabs=["intake", "review", "approval"],
            required_dashboard_name=board_name,
        )
    )
    staging = _staged_dashboard(
        "Client Onboarding Staging",
        [],
        tabs=[
            {"id": "intake", "name": "Intake"},
            {"id": "review", "name": "Review"},
        ],
        dashboard_id="wave2_client_staging",
    )
    tasks.append(
        _record(
            "organize",
            spine,
            3,
            "dashboard",
            (
                "On the open Client Onboarding Staging board, rename the dashboard to "
                "Wave Two Client Onboarding and change Intake to Client Intake. Preserve "
                "Review and every other workspace item."
            ),
            [
                _snapshot(),
                _call(
                    "manage_dashboard",
                    {
                        "operation": "update",
                        "dashboard_id": "wave2_client_staging",
                        "name": board_name,
                    },
                    graded_args=("name",),
                ),
                _call(
                    "manage_navigation_bar",
                    {
                        "operation": "rename_tabs",
                        "rename_map": {"intake": "Client Intake"},
                        "dashboard_id": "wave2_client_staging",
                    },
                    graded_args=("rename_map",),
                ),
            ],
            selected_dashboard="Client Onboarding Staging",
            initial_state=staging,
        )
    )
    tasks.append(
        _record(
            "organize",
            spine,
            4,
            "dashboard",
            (
                "Client operations needs a governed setup: following Workspace session "
                "guidance, create and activate Wave Two Client Onboarding with Client "
                "Intake, Due Diligence, and Approval tabs in that order."
            ),
            [
                _call(
                    "get_workspace_prompt",
                    {"name": "workspace_session_context"},
                    graded_args=("name",),
                ),
                _call(
                    "manage_dashboard",
                    {"operation": "create", "name": board_name, "activate": True},
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_navigation_bar",
                    {
                        "operation": "create",
                        "tabs": [
                            {"name": "Client Intake"},
                            {"name": "Due Diligence"},
                            {"name": "Approval"},
                        ],
                    },
                    graded_args=("operation", "tabs"),
                ),
            ],
            policies=(PolicyMapping("Workspace session guidance", ("workspace_session_context",)),),
        )
    )

    backend_name = "Client Onboarding Backend"
    intake_name = "Client Intake Queue"
    approval_name = "Approval Log"
    intake_id = "client_intake_queue"
    approval_id = "approval_log"
    app_name = "Client Onboarding App"
    widgets = {
        intake_id: _widget_def(intake_name, "/client-intake"),
        approval_id: _widget_def(approval_name, "/approval-log"),
    }
    app_def = _app(
        app_name,
        [
            ("intake", "Intake", [(intake_id, 0, 0, 40, 12, None)]),
            ("approvals", "Approvals", [(approval_id, 0, 0, 40, 12, None)]),
        ],
    )
    tasks.append(
        _record(
            "organize",
            spine,
            5,
            "platform",
            (
                "Author and add a Client Onboarding Backend with Client Intake Queue and "
                "Approval Log table views, then publish and instantiate a Client Onboarding App "
                "with Intake and Approvals tabs. Follow the apps manifest specification. "
                "Widget ids are the snake_case of widget names; tab ids are the snake_case "
                "of tab names."
            ),
            [
                _call(
                    "read_workspace_resource",
                    {"uri": "openbb://workspace/specs/apps-json"},
                    graded_args=("uri",),
                ),
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9603",
                        "widgets_json": widgets,
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "Client Onboarding Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=(
                _custom_target(backend_name, intake_id, intake_name),
                _custom_target(backend_name, approval_id, approval_name),
            ),
            policies=(
                PolicyMapping(
                    "apps manifest specification", ("openbb://workspace/specs/apps-json",)
                ),
            ),
            required_widgets=[
                _required_widget(backend_name, intake_id, tab_id="intake"),
                _required_widget(backend_name, approval_id, tab_id="approvals"),
            ],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": intake_id,
                    "expect": {"type": "table"},
                },
                {
                    "backend_name": backend_name,
                    "widget_id": approval_id,
                    "expect": {"type": "table"},
                },
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["intake", "approvals"],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [
                        {"tab_id": "intake", "widget_id": intake_id},
                        {"tab_id": "approvals", "widget_id": approval_id},
                    ],
                }
            ],
        )
    )
    return tasks


def _manufacturer_repair_stage(
    widgets: list[JsonDict],
    *,
    name: str = "Manufacturer Detail Repair",
) -> JsonDict:
    return _staged_dashboard(
        name,
        widgets,
        tabs=[{"id": "details", "name": "Details"}],
    )


def _manufacturer_detail_widget(
    *,
    widget_uuid: str,
    year: int = 2024,
    layout: JsonDict | None = None,
) -> JsonDict:
    return {
        "origin": GETTING_STARTED,
        "widget_id": COMPANY_DETAILS_WIDGET,
        "widget_uuid": widget_uuid,
        "tab_id": "details",
        "data_args": {"company": "F", "year": year},
        "layout": layout or {"x": 0, "y": 0, "w": 40, "h": 14},
    }


def _manufacturer_preserved_widget() -> JsonDict:
    return {
        "origin": GETTING_STARTED,
        "widget_id": MARKDOWN_WIDGET,
        "widget_uuid": "manufacturer_repair_notes",
        "tab_id": "details",
        "layout": {"x": 0, "y": 14, "w": 40, "h": 10},
    }


def _build_repair_wave2_tasks() -> list[TaskRecord]:
    """Build the manufacturer-detail defect-repair spine."""

    tasks: list[TaskRecord] = []
    spine = "manufacturer_details_repair"
    correct_args = {"company": "F", "year": 2024}
    detail_target = _target(
        GETTING_STARTED,
        COMPANY_DETAILS_WIDGET,
        "Car Manufacturer Details",
        staged=True,
    )
    notes_target = _target(
        GETTING_STARTED,
        MARKDOWN_WIDGET,
        "Markdown Widget",
        staged=True,
    )

    stated_fix_stage = _manufacturer_repair_stage(
        [
            _manufacturer_detail_widget(widget_uuid="detail_primary", year=2022),
            _manufacturer_preserved_widget(),
        ]
    )
    tasks.append(
        _record(
            "repair",
            spine,
            0,
            "repair",
            (
                "Car Manufacturer Details on the open Manufacturer Detail Repair board "
                "has company set to F and year set to 2022. Set company to F and year back "
                "to 2024."
            ),
            [
                _snapshot(),
                _call(
                    "update_widget",
                    {"widget_uuid": "detail_primary", "data_args": correct_args},
                    graded_args=("data_args",),
                ),
            ],
            targets=(detail_target,),
            pinned_widget_args={(GETTING_STARTED, COMPANY_DETAILS_WIDGET): frozenset(correct_args)},
            required_widgets=[
                _required_widget(GETTING_STARTED, COMPANY_DETAILS_WIDGET, correct_args),
            ],
            selected_dashboard="Manufacturer Detail Repair",
            initial_state=stated_fix_stage,
        )
    )

    bad_stage = _manufacturer_repair_stage(
        [
            _manufacturer_detail_widget(widget_uuid="detail_primary", year=2022),
            _manufacturer_preserved_widget(),
        ]
    )
    tasks.append(
        _record(
            "repair",
            spine,
            1,
            "repair",
            (
                "On the open Manufacturer Detail Repair board, restore Car Manufacturer "
                "Details to company F and year 2024. Preserve Markdown Widget and every "
                "other workspace item."
            ),
            [
                _snapshot(),
                _call(
                    "update_widget",
                    {"widget_uuid": "detail_primary", "data_args": correct_args},
                    graded_args=("data_args",),
                ),
            ],
            targets=(detail_target, notes_target),
            pinned_widget_args={(GETTING_STARTED, COMPANY_DETAILS_WIDGET): frozenset(correct_args)},
            required_widgets=[
                _required_widget(GETTING_STARTED, COMPANY_DETAILS_WIDGET, correct_args),
                _required_widget(GETTING_STARTED, MARKDOWN_WIDGET),
            ],
            selected_dashboard="Manufacturer Detail Repair",
            initial_state=bad_stage,
        )
    )

    duplicate_stage = _manufacturer_repair_stage(
        [
            _manufacturer_detail_widget(widget_uuid="detail_primary"),
            _manufacturer_detail_widget(
                widget_uuid="detail_duplicate",
                layout={"x": 0, "y": 24, "w": 40, "h": 14},
            ),
            _manufacturer_preserved_widget(),
        ]
    )
    tasks.append(
        _record(
            "repair",
            spine,
            2,
            "repair",
            (
                "The open Manufacturer Detail Repair board has an extra Car Manufacturer "
                "Details copy. The manufacturer-duplicate marker identifies it; remove "
                "that copy so exactly one remains, and preserve Markdown Widget."
            ),
            [
                _call(
                    "delete_widget",
                    {"widget_uuid": "detail_duplicate"},
                    graded_args=("widget_uuid",),
                )
            ],
            targets=(detail_target, notes_target),
            policies=(PolicyMapping("manufacturer-duplicate marker", ("detail_duplicate",)),),
            required_widgets=[
                _required_widget(
                    GETTING_STARTED,
                    COMPANY_DETAILS_WIDGET,
                    min_count=1,
                    max_count=1,
                ),
                _required_widget(GETTING_STARTED, MARKDOWN_WIDGET),
            ],
            selected_dashboard="Manufacturer Detail Repair",
            initial_state=duplicate_stage,
        )
    )

    overlap_stage = _manufacturer_repair_stage(
        [
            _manufacturer_detail_widget(
                widget_uuid="detail_primary",
                layout={"x": 0, "y": 0, "w": 40, "h": 14},
            ),
            {**_manufacturer_preserved_widget(), "layout": {"x": 0, "y": 0, "w": 40, "h": 10}},
        ]
    )
    tasks.append(
        _record(
            "repair",
            spine,
            3,
            "repair",
            (
                "Car Manufacturer Details overlaps Markdown Widget on the open Manufacturer "
                "Detail Repair board. Move Car Manufacturer Details to x 0, y 10, width "
                "40, height 14 on Details while preserving its settings."
            ),
            [
                _snapshot(),
                _call(
                    "update_widget_layout",
                    {
                        "widget_uuid": "detail_primary",
                        "x": 0,
                        "y": 10,
                        "w": 40,
                        "h": 14,
                        "tab_id": "details",
                    },
                    graded_args=("x", "y", "w", "h", "tab_id"),
                ),
            ],
            targets=(detail_target, notes_target),
            required_widgets=[
                _required_widget(GETTING_STARTED, COMPANY_DETAILS_WIDGET),
                _required_widget(GETTING_STARTED, MARKDOWN_WIDGET),
            ],
            selected_dashboard="Manufacturer Detail Repair",
            initial_state=overlap_stage,
        )
    )

    multi_stage = _manufacturer_repair_stage(
        [
            _manufacturer_detail_widget(widget_uuid="detail_primary", year=2022),
            _manufacturer_detail_widget(
                widget_uuid="detail_duplicate",
                year=2022,
                layout={"x": 0, "y": 24, "w": 40, "h": 14},
            ),
            {**_manufacturer_preserved_widget(), "layout": {"x": 0, "y": 0, "w": 40, "h": 10}},
        ]
    )
    tasks.append(
        _record(
            "repair",
            spine,
            4,
            "repair",
            (
                "Clean up the open Manufacturer Detail Repair board. Restore the primary "
                "Car Manufacturer Details to F and 2024; the manufacturer-duplicate marker "
                "identifies the extra copy. Move the primary to x 0, y 10, width 40, height "
                "14 on Details, and preserve Markdown Widget."
            ),
            [
                _call(
                    "update_widget",
                    {"widget_uuid": "detail_primary", "data_args": correct_args},
                    graded_args=("data_args",),
                ),
                _call(
                    "delete_widget",
                    {"widget_uuid": "detail_duplicate"},
                    graded_args=("widget_uuid",),
                ),
                _call(
                    "update_widget_layout",
                    {
                        "widget_uuid": "detail_primary",
                        "x": 0,
                        "y": 10,
                        "w": 40,
                        "h": 14,
                        "tab_id": "details",
                    },
                    graded_args=("x", "y", "w", "h", "tab_id"),
                ),
            ],
            targets=(detail_target, notes_target),
            policies=(PolicyMapping("manufacturer-duplicate marker", ("detail_duplicate",)),),
            pinned_widget_args={(GETTING_STARTED, COMPANY_DETAILS_WIDGET): frozenset(correct_args)},
            required_widgets=[
                _required_widget(
                    GETTING_STARTED,
                    COMPANY_DETAILS_WIDGET,
                    correct_args,
                    min_count=1,
                    max_count=1,
                ),
                _required_widget(GETTING_STARTED, MARKDOWN_WIDGET),
            ],
            selected_dashboard="Manufacturer Detail Repair",
            initial_state=multi_stage,
        )
    )

    backend_name = "Wave Two Detail Repair"
    widget_name = "Manufacturer Detail Queue"
    widget_id = "manufacturer_detail_queue"
    app_name = "Detail Repair App"
    fixed_widget = _widget_def(
        widget_name,
        "/manufacturer-details",
        description="Refreshed manufacturer detail queue.",
    )
    fixed_app = _app(
        app_name,
        [("details", "Details", [(widget_id, 0, 0, 40, 12, None)])],
    )
    broken_widget = {"name": widget_name, "description": "Broken detail queue.", "type": "table"}
    broken_app = {
        "name": app_name,
        "tabs": {
            "details": {
                "id": "details",
                "name": "Details",
                "layout": [
                    {"i": widget_id, "x": 0, "y": 0, "w": 30, "h": 12},
                    {"i": widget_id, "x": 20, "y": 0, "w": 20, "h": 12},
                ],
            }
        },
    }
    custom_state = _manufacturer_repair_stage(
        [
            {
                "origin": backend_name,
                "widget_id": widget_id,
                "widget_uuid": "custom_detail_queue",
                "tab_id": "details",
                "layout": {"x": 0, "y": 0, "w": 40, "h": 12},
            }
        ],
        name="Custom Detail Repair",
    )
    custom_state["custom_backends"] = [
        {
            "backend_id": "backend_005",
            "name": backend_name,
            "url": "http://127.0.0.1:9604",
            "widgets_json": {widget_id: broken_widget},
            "apps_json": [broken_app],
            "warnings": ["missing endpoint and overlapping app layout"],
        }
    ]
    tasks.append(
        _record(
            "repair",
            spine,
            5,
            "repair",
            (
                "On the open Custom Detail Repair board, refresh the authored Wave Two "
                "Detail Repair backend so Manufacturer Detail Queue serves "
                "/manufacturer-details and Detail Repair App has one non-overlapping "
                "placement on Details. Keep the open view and all other content. Widget "
                "ids are the snake_case of widget names; tab ids are the snake_case of tab "
                "names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "refresh",
                        "backend_id": "backend_005",
                        "widgets_json": {widget_id: fixed_widget},
                        "apps_json": [fixed_app],
                    },
                    graded_args=("operation",),
                )
            ],
            targets=(_custom_target(backend_name, widget_id, widget_name, staged=True),),
            required_widgets=[_required_widget(backend_name, widget_id, tab_id="details")],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": widget_id,
                    "expect": {},
                }
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["details"],
                    "layout_refs_valid": True,
                    "no_overlaps": True,
                }
            ],
            selected_dashboard="Custom Detail Repair",
            initial_state=custom_state,
        )
    )
    return tasks


def _build_platform_wave2_tasks() -> list[TaskRecord]:
    """Build the Daloopa-and-skills governed research spine."""

    tasks: list[TaskRecord] = []
    spine = "cited_research_operations"
    stage = _staged_dashboard(
        "Cited Research Operations",
        [],
        tabs=[{"id": "research", "name": "Research"}],
    )

    tasks.append(
        _record(
            "platform",
            spine,
            0,
            "platform",
            (
                "From the open Cited Research Operations board, read the Daloopa "
                "Tearsheet skill (daloopa-tearsheet). Add a Daloopa Tearsheet Workflow "
                "note that records the workflow title and its period-math anchor."
            ),
            [
                _snapshot(),
                _call(
                    "get_skill_content",
                    {"slug": "daloopa-tearsheet"},
                    graded_args=("slug",),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "Daloopa Tearsheet Workflow",
                        "data": (
                            "Daloopa tearsheet workflow: anchor period math on "
                            "latest_calendar_quarter."
                        ),
                    },
                    graded_args=("widget_type", "name"),
                ),
            ],
            required_generated_widgets=[
                {
                    "widget_type": "note",
                    "name_contains": "Daloopa Tearsheet Workflow",
                    "data_contains": [
                        "Daloopa tearsheet workflow",
                        "latest_calendar_quarter",
                    ],
                }
            ],
            selected_dashboard="Cited Research Operations",
            initial_state=stage,
        )
    )

    directory_target = _target(DALOOPA, DALOOPA_DIRECTORY_WIDGET, "Company Directory")
    tasks.append(
        _record(
            "platform",
            spine,
            1,
            "platform",
            (
                "On the open Cited Research Operations board, follow Daloopa Tearsheet "
                "governance and add Bench Daloopa's Company Directory."
            ),
            [
                _snapshot(),
                _call(
                    "get_skill_content",
                    {"slug": "daloopa-tearsheet"},
                    graded_args=("slug",),
                ),
                _call("list_available_widgets", {"origin": DALOOPA}, optional=True),
                _call(
                    "create_widget",
                    {"origin": DALOOPA, "widget_id": DALOOPA_DIRECTORY_WIDGET},
                    graded_args=("origin",),
                ),
            ],
            targets=(directory_target,),
            policies=(PolicyMapping("Daloopa Tearsheet governance", ("daloopa-tearsheet",)),),
            required_widgets=[_required_widget(DALOOPA, DALOOPA_DIRECTORY_WIDGET)],
            selected_dashboard="Cited Research Operations",
            initial_state=stage,
        )
    )

    guidance_args = {"ticker": "NVDA"}
    guidance_target = _target(DALOOPA, DALOOPA_GUIDANCE_WIDGET, "Management Guidance")
    tasks.append(
        _record(
            "platform",
            spine,
            2,
            "platform",
            (
                "Use Daloopa Guidance Tracker governance on the open Cited Research "
                "Operations board and add Bench Daloopa's Management Guidance for NVDA."
            ),
            [
                _call(
                    "get_skill_content",
                    {"slug": "daloopa-guidance-tracker"},
                    graded_args=("slug",),
                ),
                _call("list_available_widgets", {"origin": DALOOPA}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": DALOOPA,
                        "widget_id": DALOOPA_GUIDANCE_WIDGET,
                        "data_args": guidance_args,
                    },
                    graded_args=("origin", "data_args"),
                ),
            ],
            targets=(guidance_target,),
            policies=(
                PolicyMapping("Daloopa Guidance Tracker governance", ("daloopa-guidance-tracker",)),
            ),
            pinned_widget_args={(DALOOPA, DALOOPA_GUIDANCE_WIDGET): frozenset(guidance_args)},
            required_widgets=[_required_widget(DALOOPA, DALOOPA_GUIDANCE_WIDGET, guidance_args)],
            selected_dashboard="Cited Research Operations",
            initial_state=stage,
        )
    )

    fundamentals_target = _target(
        DALOOPA,
        DALOOPA_FUNDAMENTALS_WIDGET,
        "Company Fundamentals",
    )
    msft_args = {"ticker": "MSFT", "period": "2025Q4"}
    nvda_args = {"ticker": "NVDA", "period": "2025Q4"}
    tasks.append(
        _record(
            "platform",
            spine,
            3,
            "dashboard",
            (
                "For the open Cited Research Operations board, use Daloopa Industry "
                "governance to place two Bench Daloopa Company Fundamentals views, one for "
                "MSFT in 2025Q4 and one for NVDA in 2025Q4."
            ),
            [
                _call(
                    "get_skill_content",
                    {"slug": "daloopa-industry"},
                    graded_args=("slug",),
                ),
                _call("list_available_widgets", {"origin": DALOOPA}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": DALOOPA,
                        "widget_id": DALOOPA_FUNDAMENTALS_WIDGET,
                        "data_args": msft_args,
                    },
                    graded_args=("origin", "data_args"),
                ),
                _call(
                    "create_widget",
                    {
                        "origin": DALOOPA,
                        "widget_id": DALOOPA_FUNDAMENTALS_WIDGET,
                        "data_args": nvda_args,
                    },
                    graded_args=("origin", "data_args"),
                ),
            ],
            targets=(fundamentals_target,),
            policies=(PolicyMapping("Daloopa Industry governance", ("daloopa-industry",)),),
            pinned_widget_args={(DALOOPA, DALOOPA_FUNDAMENTALS_WIDGET): frozenset(msft_args)},
            required_widgets=[
                _required_widget(DALOOPA, DALOOPA_FUNDAMENTALS_WIDGET, msft_args),
                _required_widget(DALOOPA, DALOOPA_FUNDAMENTALS_WIDGET, nvda_args),
            ],
            selected_dashboard="Cited Research Operations",
            initial_state=stage,
        )
    )

    amazon_args = {"ticker": "AMZN", "period": "2026Q1"}
    tasks.append(
        _record(
            "platform",
            spine,
            4,
            "dashboard",
            (
                "Combine Daloopa Capital Allocation governance with Workspace session "
                "guidance on the open Cited Research Operations board. Add Bench Daloopa's "
                "Company Fundamentals for AMZN in 2026Q1 and a Citation Protocol note "
                "naming source_url and calendar_period."
            ),
            [
                _call(
                    "get_skill_content",
                    {"slug": "daloopa-capital-allocation"},
                    graded_args=("slug",),
                ),
                _call(
                    "get_workspace_prompt",
                    {"name": "workspace_session_context"},
                    graded_args=("name",),
                ),
                _call("list_available_widgets", {"origin": DALOOPA}, optional=True),
                _call(
                    "create_widget",
                    {
                        "origin": DALOOPA,
                        "widget_id": DALOOPA_FUNDAMENTALS_WIDGET,
                        "data_args": amazon_args,
                    },
                    graded_args=("origin", "data_args"),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "Citation Protocol",
                        "data": "Citation protocol: retain source_url and calendar_period.",
                    },
                    graded_args=("widget_type", "name"),
                ),
            ],
            targets=(fundamentals_target,),
            policies=(
                PolicyMapping(
                    "Daloopa Capital Allocation governance",
                    ("daloopa-capital-allocation",),
                ),
                PolicyMapping("Workspace session guidance", ("workspace_session_context",)),
            ),
            pinned_widget_args={(DALOOPA, DALOOPA_FUNDAMENTALS_WIDGET): frozenset(amazon_args)},
            required_widgets=[_required_widget(DALOOPA, DALOOPA_FUNDAMENTALS_WIDGET, amazon_args)],
            required_generated_widgets=[
                {
                    "widget_type": "note",
                    "name_contains": "Citation Protocol",
                    "data_contains": ["source_url", "calendar_period"],
                }
            ],
            selected_dashboard="Cited Research Operations",
            initial_state=stage,
        )
    )

    backend_name = "Cited Research Backend"
    widget_name = "Citation Review Queue"
    widget_id = "citation_review_queue"
    app_name = "Cited Research App"
    widget_def = _widget_def(widget_name, "/citation-review")
    app_def = _app(
        app_name,
        [("research", "Research", [(widget_id, 0, 0, 40, 12, None)])],
    )
    tasks.append(
        _record(
            "platform",
            spine,
            5,
            "platform",
            (
                "Following Daloopa Tearsheet governance, author and add a Cited Research "
                "Backend with a Citation Review Queue, then publish and instantiate a Cited "
                "Research App with a Research tab. Widget ids are the snake_case of widget "
                "names; tab ids are the snake_case of tab names."
            ),
            [
                _call(
                    "get_skill_content",
                    {"slug": "daloopa-tearsheet"},
                    graded_args=("slug",),
                ),
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9605",
                        "widgets_json": {widget_id: widget_def},
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "Cited Research Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=(_custom_target(backend_name, widget_id, widget_name),),
            policies=(PolicyMapping("Daloopa Tearsheet governance", ("daloopa-tearsheet",)),),
            required_widgets=[_required_widget(backend_name, widget_id, tab_id="research")],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": widget_id,
                    "expect": {},
                }
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["research"],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": "research", "widget_id": widget_id}],
                }
            ],
        )
    )
    return tasks


def _research_feed_seed(
    widgets_json: JsonDict,
    apps_json: list[JsonDict] | None = None,
) -> JsonDict:
    backend_name = "Wave Two Research Feed"
    pulse_id = "research_feed_pulse"
    state = _staged_dashboard(
        "Research Feed Staging",
        [
            {
                "origin": backend_name,
                "widget_id": pulse_id,
                "widget_uuid": "seeded_research_feed",
                "tab_id": "feed",
                "layout": {"x": 0, "y": 0, "w": 40, "h": 10},
            }
        ],
        tabs=[{"id": "feed", "name": "Feed"}],
    )
    state["custom_backends"] = [
        {
            "backend_id": "backend_005",
            "name": backend_name,
            "url": "http://127.0.0.1:9606",
            "widgets_json": widgets_json,
            **({"apps_json": apps_json} if apps_json is not None else {}),
        }
    ]
    return state


def _build_extend_wave2_tasks() -> list[TaskRecord]:
    """Build the research-feed backend lifecycle spine."""

    tasks: list[TaskRecord] = []
    spine = "research_feed_lifecycle"
    backend_name = "Wave Two Research Feed"
    pulse_name = "Research Feed Pulse"
    pulse_id = "research_feed_pulse"
    freshness_name = "Source Freshness Alert"
    freshness_id = "source_freshness_alert"
    archive_name = "Archive Coverage Watch"
    archive_id = "archive_coverage_watch"
    app_name = "Research Feed App"

    stale_pulse = _widget_def(
        pulse_name,
        "/research-feed",
        description="Stale research feed.",
        grid=(40, 10),
    )
    refreshed_pulse = _widget_def(
        pulse_name,
        "/research-feed",
        description="Refreshed research feed.",
        grid=(40, 10),
    )
    tasks.append(
        _record(
            "extend",
            spine,
            0,
            "platform",
            (
                "On the open Research Feed Staging board, review the connected backends "
                "and refresh Wave Two Research Feed so Research Feed Pulse has the "
                "description Refreshed research feed."
            ),
            [
                _snapshot(),
                _call("manage_backends", {"operation": "list"}, optional=True),
                _call(
                    "manage_backends",
                    {
                        "operation": "refresh",
                        "backend_id": "backend_005",
                        "widgets_json": {pulse_id: refreshed_pulse},
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=(_custom_target(backend_name, pulse_id, pulse_name, staged=True),),
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": pulse_id,
                    "expect": {},
                }
            ],
            selected_dashboard="Research Feed Staging",
            initial_state=_research_feed_seed({pulse_id: stale_pulse}),
        )
    )

    broken_app = {
        "name": app_name,
        "tabs": {
            "feed": {
                "id": "feed",
                "name": "Feed",
                "layout": [
                    {"i": pulse_id, "x": 0, "y": 0, "w": 30, "h": 10},
                    {"i": pulse_id, "x": 20, "y": 0, "w": 20, "h": 10},
                ],
            }
        },
    }
    single_app = _app(
        app_name,
        [("feed", "Feed", [(pulse_id, 0, 0, 40, 10, None)])],
    )
    tasks.append(
        _record(
            "extend",
            spine,
            1,
            "platform",
            (
                "From the open Research Feed Staging board, review the connected backends, "
                "then refresh Wave Two Research Feed so Research Feed App has one "
                "non-overlapping Research Feed Pulse placement on Feed."
            ),
            [
                _snapshot(),
                _call("manage_backends", {"operation": "list"}, optional=True),
                _call(
                    "manage_backends",
                    {
                        "operation": "refresh",
                        "backend_id": "backend_005",
                        "widgets_json": {pulse_id: refreshed_pulse},
                        "apps_json": [single_app],
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=(_custom_target(backend_name, pulse_id, pulse_name, staged=True),),
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["feed"],
                    "layout_refs_valid": True,
                    "no_overlaps": True,
                }
            ],
            selected_dashboard="Research Feed Staging",
            initial_state=_research_feed_seed({pulse_id: stale_pulse}, [broken_app]),
        )
    )
    tasks.append(
        _record(
            "extend",
            spine,
            2,
            "platform",
            (
                "Add a minimal Wave Two Research Feed backend serving a Research Feed "
                "Pulse table at /research-feed."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9606",
                        "widgets_json": {pulse_id: refreshed_pulse},
                    },
                    graded_args=("operation", "name"),
                )
            ],
            targets=(_custom_target(backend_name, pulse_id, pulse_name),),
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": pulse_id,
                    "expect": {"type": "table"},
                }
            ],
        )
    )
    tasks.append(
        _record(
            "extend",
            spine,
            3,
            "platform",
            (
                "Publish and add Wave Two Research Feed with Research Feed Pulse and a "
                "Research Feed App containing Feed. Widget ids are the snake_case of "
                "widget names; tab ids are the snake_case of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9606",
                        "widgets_json": {pulse_id: refreshed_pulse},
                        "apps_json": [single_app],
                    },
                    graded_args=("operation", "name"),
                )
            ],
            targets=(_custom_target(backend_name, pulse_id, pulse_name),),
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": pulse_id,
                    "expect": {},
                }
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["feed"],
                    "layout_refs_valid": True,
                }
            ],
        )
    )

    freshness_def = _widget_def(freshness_name, "/source-freshness", grid=(20, 10))
    two_widgets = {pulse_id: refreshed_pulse, freshness_id: freshness_def}
    two_app = _app(
        app_name,
        [
            (
                "feed",
                "Feed",
                [
                    (pulse_id, 0, 0, 20, 10, None),
                    (freshness_id, 20, 0, 20, 10, None),
                ],
            )
        ],
    )
    tasks.append(
        _record(
            "extend",
            spine,
            4,
            "platform",
            (
                "Set up and add Wave Two Research Feed with Research Feed Pulse and Source "
                "Freshness Alert, publish Research Feed App with both on Feed, and "
                "instantiate it. Widget ids are the snake_case of widget names; tab ids are "
                "the snake_case of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9606",
                        "widgets_json": two_widgets,
                        "apps_json": [two_app],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "Research Feed Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=(
                _custom_target(backend_name, pulse_id, pulse_name),
                _custom_target(backend_name, freshness_id, freshness_name),
            ),
            required_widgets=[
                _required_widget(backend_name, pulse_id, tab_id="feed"),
                _required_widget(backend_name, freshness_id, tab_id="feed"),
            ],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": pulse_id,
                    "expect": {},
                },
                {
                    "backend_name": backend_name,
                    "widget_id": freshness_id,
                    "expect": {},
                },
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["feed"],
                    "layout_refs_valid": True,
                    "no_overlaps": True,
                }
            ],
        )
    )

    archive_def = _widget_def(archive_name, "/archive-coverage", grid=(40, 10))
    three_widgets = {**two_widgets, archive_id: archive_def}
    three_app = _app(
        app_name,
        [
            (
                "feed",
                "Feed",
                [
                    (pulse_id, 0, 0, 20, 10, None),
                    (freshness_id, 20, 0, 20, 10, None),
                ],
            ),
            ("archive", "Archive", [(archive_id, 0, 0, 40, 10, None)]),
        ],
    )
    tasks.append(
        _record(
            "extend",
            spine,
            5,
            "platform",
            (
                "Complete the research service with Wave Two Research Feed, Research Feed "
                "Pulse, Source Freshness Alert, and Archive Coverage Watch. Add the backend, "
                "publish Research Feed App with Feed and Archive tabs, and instantiate it. "
                "Widget ids are the snake_case of widget names; tab ids are the snake_case "
                "of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9606",
                        "widgets_json": three_widgets,
                        "apps_json": [three_app],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "Research Feed Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=(
                _custom_target(backend_name, pulse_id, pulse_name),
                _custom_target(backend_name, freshness_id, freshness_name),
                _custom_target(backend_name, archive_id, archive_name),
            ),
            required_widgets=[
                _required_widget(backend_name, pulse_id, tab_id="feed"),
                _required_widget(backend_name, freshness_id, tab_id="feed"),
                _required_widget(backend_name, archive_id, tab_id="archive"),
            ],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": pulse_id,
                    "expect": {},
                },
                {
                    "backend_name": backend_name,
                    "widget_id": freshness_id,
                    "expect": {},
                },
                {
                    "backend_name": backend_name,
                    "widget_id": archive_id,
                    "expect": {},
                },
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["feed", "archive"],
                    "layout_refs_valid": True,
                    "no_overlaps": True,
                }
            ],
        )
    )
    return tasks


def _build_handoff_wave2_tasks() -> list[TaskRecord]:
    """Build the catalog-grounded news-desk handoff spine."""

    tasks: list[TaskRecord] = []
    spine = "news_desk_handoff"
    stage = _staged_dashboard("News Desk Handoff", [])
    target = _target(GETTING_STARTED, NEWSFEED_WIDGET, "Sample News Feed")
    source = ("getting-started", NEWSFEED_WIDGET)
    specs = (
        (
            0,
            (
                "On the open News Desk Handoff board, read Getting Started's Sample News "
                "Feed with category set to business and limit set to 2. Add a Markets News "
                "Handoff note with the exact lead title and author."
            ),
            {"category": "business", "limit": 2},
            "Markets News Handoff",
            ("Global Markets Rally on Positive Economic Data", "Robert Williams"),
            (),
        ),
        (
            1,
            (
                "Find Getting Started's Sample News Feed from the open News Desk Handoff "
                "board for technology, limited to 2, then add a Technology News Handoff "
                "note with the exact lead title and author."
            ),
            {"category": "tech", "limit": 2},
            "Technology News Handoff",
            ("AI Breakthrough: New Model Achieves Human-Level Reasoning", "Sarah Johnson"),
            (),
        ),
        (
            2,
            (
                "Prepare a Science News Handoff note on the open News Desk Handoff board "
                "under the science route. Read Getting Started's Sample News Feed for that "
                "route, limited to 2, and pin the exact lead title and author."
            ),
            {"category": "science", "limit": 2},
            "Science News Handoff",
            (
                "Scientists Discover New Earth-like Exoplanet in Habitable Zone",
                "Dr. Emily Rogers",
            ),
            (PolicyMapping("science route", ("science",)),),
        ),
    )
    for level, prompt, data_args, note_name, tokens, policies in specs:
        tools: list[JsonDict] = []
        if level in {0, 1}:
            tools.append(_snapshot())
        if level == 1:
            tools.extend(
                [
                    _call("list_available_widgets", {"origin": GETTING_STARTED}, optional=True),
                    _call(
                        "get_widget_schema",
                        {"origin": GETTING_STARTED, "widget_id": NEWSFEED_WIDGET},
                        optional=True,
                    ),
                ]
            )
        tools.extend(
            [
                _call(
                    "get_widget_data",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": NEWSFEED_WIDGET,
                        "data_args": data_args,
                    },
                    graded_args=("origin", "widget_id"),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": note_name,
                        "data": f"Lead: {tokens[0]}; author: {tokens[1]}.",
                    },
                    graded_args=("widget_type", "name"),
                ),
            ]
        )
        tasks.append(
            _record(
                "handoff",
                spine,
                level,
                "read",
                prompt,
                tools,
                targets=(target,),
                policies=policies,
                required_generated_widgets=[
                    {
                        "widget_type": "note",
                        "name_contains": note_name,
                        "data_contains": list(tokens),
                    }
                ],
                grounded_generated=(GroundedGenerated(source[0], source[1], tokens),),
                selected_dashboard="News Desk Handoff",
                initial_state=stage,
            )
        )

    business_tokens = (
        "E-commerce Giant Announces Major Expansion into Southeast Asia",
        "Lisa Anderson",
    )
    tasks.append(
        _record(
            "handoff",
            spine,
            3,
            "platform",
            (
                "Using Workspace session guidance on the open News Desk Handoff board, "
                "read Getting Started's Sample News Feed for business, limited to 2. Add a "
                "Governed Expansion Handoff note with the exact second title and author."
            ),
            [
                _call(
                    "get_workspace_prompt",
                    {"name": "workspace_session_context"},
                    graded_args=("name",),
                ),
                _call(
                    "get_widget_data",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": NEWSFEED_WIDGET,
                        "data_args": {"category": "business", "limit": 2},
                    },
                    graded_args=("origin", "widget_id"),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "Governed Expansion Handoff",
                        "data": f"Second item: {business_tokens[0]}; author: {business_tokens[1]}.",
                    },
                    graded_args=("widget_type", "name"),
                ),
            ],
            targets=(target,),
            policies=(PolicyMapping("Workspace session guidance", ("workspace_session_context",)),),
            required_generated_widgets=[
                {
                    "widget_type": "note",
                    "name_contains": "Governed Expansion Handoff",
                    "data_contains": list(business_tokens),
                }
            ],
            grounded_generated=(GroundedGenerated(source[0], source[1], business_tokens),),
            selected_dashboard="News Desk Handoff",
            initial_state=stage,
        )
    )

    task_request = {
        "id": "science_editor_follow_up",
        "description": "Review the exoplanet story and next editorial actions.",
        "assigned_holder_url": "workspace://agents/science-editor",
        "assigned_agent_id": "science-editor-agent",
    }
    science_tokens = (
        "Scientists Discover New Earth-like Exoplanet in Habitable Zone",
        "Dr. Emily Rogers",
    )
    tasks.append(
        _record(
            "handoff",
            spine,
            4,
            "platform",
            (
                "Handle the science follow-up route from the open News Desk Handoff board "
                "under Workspace session guidance. Read Getting Started's Sample News Feed "
                "for science, limited to 2; add a Science Delegation Handoff note with the "
                "exact lead title and author, then delegate the editorial follow-up."
            ),
            [
                _call(
                    "get_workspace_prompt",
                    {"name": "workspace_session_context"},
                    graded_args=("name",),
                ),
                _call(
                    "get_widget_data",
                    {
                        "origin": GETTING_STARTED,
                        "widget_id": NEWSFEED_WIDGET,
                        "data_args": {"category": "science", "limit": 2},
                    },
                    graded_args=("origin", "widget_id"),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": "Science Delegation Handoff",
                        "data": f"Lead: {science_tokens[0]}; author: {science_tokens[1]}.",
                    },
                    graded_args=("widget_type", "name"),
                ),
                _call(
                    "assign_tasks_to_agents",
                    {"task_requests": [task_request]},
                    graded_args=(),
                ),
            ],
            targets=(target,),
            policies=(
                PolicyMapping("Workspace session guidance", ("workspace_session_context",)),
                PolicyMapping("science follow-up route", tuple(task_request.values())),
            ),
            required_generated_widgets=[
                {
                    "widget_type": "note",
                    "name_contains": "Science Delegation Handoff",
                    "data_contains": list(science_tokens),
                }
            ],
            grounded_generated=(GroundedGenerated(source[0], source[1], science_tokens),),
            selected_dashboard="News Desk Handoff",
            initial_state=stage,
        )
    )

    backend_name = "News Handoff Backend"
    widget_name = "News Handoff Register"
    widget_id = "news_handoff_register"
    app_name = "News Handoff App"
    note_name = "News Build Handoff"
    widget_def = _widget_def(widget_name, "/news-handoff")
    app_def = _app(
        app_name,
        [("handoff", "Handoff", [(widget_id, 0, 0, 40, 10, None)])],
    )
    build_follow_up = {
        "id": "news_build_review",
        "description": "Review the News Handoff App build and ownership.",
        "assigned_holder_url": "workspace://agents/science-editor",
        "assigned_agent_id": "science-editor-agent",
    }
    tasks.append(
        _record(
            "handoff",
            spine,
            5,
            "platform",
            (
                "Starting from the open News Desk Handoff board, author and add a minimal "
                "custom News Handoff Backend with one News Handoff Register. Publish and "
                "instantiate News Handoff App with one Handoff tab, add a News Build "
                "Handoff note naming News Handoff App and News Handoff Register, then "
                "delegate the build-review follow-up. Widget ids are the snake_case of "
                "widget names; tab ids are the snake_case of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": "http://127.0.0.1:9608",
                        "widgets_json": {widget_id: widget_def},
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": "News Handoff Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
                _call(
                    "add_generative_widget",
                    {
                        "widget_type": "note",
                        "name": note_name,
                        "data": f"Built {app_name} with {widget_name}; review ownership.",
                    },
                    graded_args=("widget_type", "name"),
                ),
                # Grade delegation existence only; the authored artifacts and
                # durable note carry the exact handoff-content checks.
                _call(
                    "assign_tasks_to_agents",
                    {"task_requests": [build_follow_up]},
                    graded_args=(),
                ),
            ],
            targets=(_custom_target(backend_name, widget_id, widget_name),),
            required_widgets=[
                _required_widget(backend_name, widget_id, tab_id="handoff"),
            ],
            required_generated_widgets=[
                {
                    "widget_type": "note",
                    "name_contains": note_name,
                    "data_contains": [app_name, widget_name],
                }
            ],
            required_widget_defs=[
                {
                    "backend_name": backend_name,
                    "widget_id": widget_id,
                    "expect": {},
                }
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["handoff"],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": "handoff", "widget_id": widget_id}],
                }
            ],
            selected_dashboard="News Desk Handoff",
            initial_state=stage,
        )
    )
    return tasks


def _note_phrase(name: str) -> str:
    """Phrase a generated-note mention without doubling the word "note"."""
    return name if name.lower().endswith("note") else f"{name} note"


def _wave3_catalog_target(
    origin: str,
    widget_id: str,
    display_name: str,
    *discriminators: str,
    staged: bool = False,
) -> TargetSpec:
    return _target(
        origin,
        widget_id,
        display_name,
        *(discriminators or (origin, display_name)),
        staged=staged,
    )


def _wave3_governance_call(spec: GovernanceSpec) -> JsonDict:
    key_name = {
        "get_skill_content": "slug",
        "read_workspace_resource": "uri",
        "get_workspace_prompt": "name",
    }[spec.tool]
    return _call(spec.tool, {key_name: spec.key}, graded_args=(key_name,))


def _wave3_target_words(target: TargetSpec) -> str:
    words = [target.origin, *target.discriminators]
    return "'s ".join(words[:1]) + " — " + ", ".join(words[1:])


def _wave3_place_call(target: TargetSpec, data_args: JsonDict | None = None) -> JsonDict:
    args: JsonDict = {"origin": target.origin, "widget_id": target.widget_id}
    if data_args:
        args["data_args"] = data_args
    return _call("create_widget", args, graded_args=("origin", "widget_id"))


def _wave3_discover_targets(targets: tuple[TargetSpec, ...]) -> list[JsonDict]:
    return [
        _call("list_available_widgets", {"origin": origin}, optional=True)
        for origin in dict.fromkeys(target.origin for target in targets)
    ]


def _wave3_read_call(
    target: TargetSpec,
    data_args: JsonDict,
    *,
    optional: bool = False,
) -> JsonDict:
    return _call(
        "get_widget_data",
        {
            "origin": target.origin,
            "widget_id": target.widget_id,
            "data_args": data_args,
        },
        optional=optional,
        graded_args=("origin", "widget_id"),
    )


def _wave3_generated_call(name: str, data: str) -> JsonDict:
    return _call(
        "add_generative_widget",
        {"widget_type": "note", "name": name, "data": data},
        graded_args=("widget_type", "name"),
    )


def _wave3_required_generated(name: str, *tokens: str) -> JsonDict:
    return {
        "widget_type": "note",
        "name_contains": name,
        "data_contains": list(tokens),
    }


def _build_wave3_retrieve_spine(
    *,
    spine: str,
    title: str,
    target: TargetSpec,
    source_slug: str,
    data_args: JsonDict,
    tokens: tuple[str, str],
    read_value_words: str,
    served_columns: tuple[str, str],
    governance: GovernanceSpec,
    backend_name: str,
    widget_name: str,
    app_name: str,
    tab_name: str,
    url: str,
) -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    subject = f"{target.origin}'s {target.display_name}"
    openings = (
        f"{title} morning request:",
        f"{title} discovery request:",
        f"{title} analyst request:",
        f"{title} desk request:",
    )
    for level in range(4):
        prompt = (
            f"{openings[level]} read {subject} with "
            + ", ".join(f"{key} {value}" for key, value in data_args.items())
            + f", then report {read_value_words}."
        )
        tools: list[JsonDict] = []
        if level in {0, 1}:
            tools.append(_snapshot())
        tools.extend(_wave3_discover_targets((target,)))
        tools.append(_wave3_read_call(target, data_args))
        tasks.append(
            _record(
                "retrieve",
                spine,
                level,
                "read",
                prompt,
                tools,
                targets=(target,),
                required_values=list(tokens),
                reference_answer=f"The requested view reports {tokens[0]} and {tokens[1]}.",
                answer_source=(source_slug, target.widget_id),
            )
        )

    note_name = f"{title} Governance Note"
    governance_token = governance.outcome_tokens[0]
    tasks.append(
        _record(
            "retrieve",
            spine,
            4,
            "read",
            (
                f"{title} governed request: follow the {governance.label}, read {subject} "
                + "with "
                + ", ".join(f"{key} {value}" for key, value in data_args.items())
                + f", report {read_value_words}, and add a {_note_phrase(note_name)} "
                f"that records {governance_token}."
            ),
            [
                _wave3_governance_call(governance),
                *_wave3_discover_targets((target,)),
                _wave3_read_call(target, data_args),
                _wave3_generated_call(note_name, governance_token),
            ],
            targets=(target,),
            required_values=list(tokens),
            required_generated_widgets=[_wave3_required_generated(note_name, governance_token)],
            reference_answer=f"The governed view reports {tokens[0]} and {tokens[1]}.",
            answer_source=(source_slug, target.widget_id),
            governance=governance,
        )
    )

    widget_id = _snake_case(widget_name)
    tab_id = _snake_case(tab_name)
    params = [
        {
            "paramName": key,
            "type": "text",
            "label": key.replace("_", " ").title(),
            "value": value,
            "options": [{"label": str(value), "value": value}],
        }
        for key, value in data_args.items()
    ]
    widget_def = _widget_def(
        widget_name,
        f"/{widget_id}",
        description=f"Runtime-backed table for {title}.",
        params=params,
        grid=(40, 10),
    )
    app_def = _app(
        app_name,
        [(tab_id, tab_name, [(widget_id, 0, 0, 40, 10, data_args)])],
    )
    payload = dict(zip(served_columns, tokens, strict=True))
    tasks.append(
        _record(
            "retrieve",
            spine,
            5,
            "platform",
            (
                f"{title} build request: add {backend_name} with a {widget_name} table, "
                f"carrying {served_columns[0]} and {served_columns[1]} columns; "
                f"publish and instantiate {app_name} on {tab_name}, read it with "
                + ", ".join(f"{key} {value}" for key, value in data_args.items())
                + f", and report the exact {served_columns[0]} and {served_columns[1]} "
                "values shown. Follow the widgets manifest "
                "specification. Widget ids are the snake_case of widget names; tab ids are "
                "the snake_case of tab names."
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
                        "name": backend_name,
                        "url": url,
                        "widgets_json": {widget_id: widget_def},
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": f"{title} Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
                _call(
                    "get_widget_data",
                    {"origin": backend_name, "widget_id": widget_id, "data_args": data_args},
                    graded_args=("origin", "widget_id"),
                ),
            ],
            targets=(_custom_target(backend_name, widget_id, widget_name),),
            policies=(
                PolicyMapping(
                    "widgets manifest specification",
                    ("openbb://workspace/specs/widgets-json",),
                ),
            ),
            pinned_widget_args={(backend_name, widget_id): frozenset(data_args)},
            required_widgets=[_required_widget(backend_name, widget_id, data_args, tab_id=tab_id)],
            required_values=list(tokens),
            required_widget_defs=[
                {"backend_name": backend_name, "widget_id": widget_id, "expect": {"type": "table"}}
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": [tab_id],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": tab_id, "widget_id": widget_id}],
                }
            ],
            runtime_checks={
                "datasets": [
                    {
                        "name": f"wave3-{spine}",
                        "widget_id": widget_id,
                        "fields": list(served_columns),
                        "path": f"/{widget_id}",
                        "payload": [payload],
                    }
                ]
            },
            reference_answer=f"The built lookup reports {tokens[0]} and {tokens[1]}.",
            answer_source=(source_slug, target.widget_id),
        )
    )
    return tasks


def _build_wave3_retrieve_tasks() -> list[TaskRecord]:
    kpi = _wave3_catalog_target(DALOOPA, "daloopa_kpi_metrics", "Operating KPIs")
    live = _wave3_catalog_target(WIDGET_EXAMPLES, "live_grid_example", "Live Grid")
    return [
        *_build_wave3_retrieve_spine(
            spine="operating_driver_lookup",
            title="Operating-driver",
            target=kpi,
            source_slug="support-daloopa-skills",
            data_args={"ticker": "AAPL", "period": "2026Q1"},
            tokens=("2026Q1", "2420.9"),
            read_value_words=(
                "the exact calendar_period and Installed Base Active Devices value shown"
            ),
            served_columns=("fiscal_period", "driver_value"),
            governance=GovernanceSpec(
                "get_skill_content",
                "daloopa-inflection",
                "Daloopa Inflection skill (daloopa-inflection)",
                ("growth-rate reversals",),
            ),
            backend_name="Wave Three Operating Drivers",
            widget_name="Operating Driver Lookup",
            app_name="Operating Driver App",
            tab_name="Drivers",
            url="http://127.0.0.1:9701",
        ),
        *_build_wave3_retrieve_spine(
            spine="live_quote_lookup",
            title="Live-quote",
            target=live,
            source_slug="widget-examples",
            data_args={"symbol": "AAPL"},
            tokens=("AAPL", "150.0"),
            read_value_words="the exact symbol and price shown",
            served_columns=("symbol", "last_price"),
            governance=GovernanceSpec(
                "get_skill_content",
                "finance-tearsheet",
                "Finance Tearsheet skill (finance-tearsheet)",
                ("price action",),
            ),
            backend_name="Wave Three Live Quote",
            widget_name="Live Quote Lookup",
            app_name="Live Quote App",
            tab_name="Quotes",
            url="http://127.0.0.1:9702",
        ),
    ]


def _build_wave3_curate_spine(
    *,
    spine: str,
    title: str,
    primary: TargetSpec,
    same_app: TargetSpec,
    cross_catalog: TargetSpec,
    governance: GovernanceSpec,
    backend_name: str,
    widget_name: str,
    app_name: str,
    tab_name: str,
    url: str,
) -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    level_targets = (
        (primary,),
        (same_app,),
        (primary, same_app),
        (primary, cross_catalog),
    )
    level_words = ("opening", "discovery", "paired", "cross-catalog")
    for level, targets in enumerate(level_targets):
        names = "; ".join(_wave3_target_words(target) for target in targets)
        tools: list[JsonDict] = []
        if level in {0, 1}:
            tools.append(_snapshot())
        if level == 1:
            tools.append(
                _call("list_available_widgets", {"origin": targets[0].origin}, optional=True)
            )
        tools.extend(_wave3_discover_targets(targets))
        tools.extend(_wave3_place_call(target) for target in targets)
        tasks.append(
            _record(
                "curate",
                spine,
                level,
                "dashboard",
                f"{title} {level_words[level]} board: add {names} to the current board.",
                tools,
                targets=targets,
                required_widgets=[
                    _required_widget(target.origin, target.widget_id) for target in targets
                ],
            )
        )

    note_name = f"{title} Governance"
    governed_token = governance.outcome_tokens[0]
    governed_targets = (primary, cross_catalog)
    governed_names = "; ".join(_wave3_target_words(target) for target in governed_targets)
    tasks.append(
        _record(
            "curate",
            spine,
            4,
            "dashboard",
            (
                f"{title} governed board: follow the {governance.label}, add {governed_names}, "
                f"and add a {_note_phrase(note_name)} naming {governed_token}."
            ),
            [
                _wave3_governance_call(governance),
                *_wave3_discover_targets(governed_targets),
                *(_wave3_place_call(target) for target in governed_targets),
                _wave3_generated_call(note_name, governed_token),
            ],
            targets=governed_targets,
            required_widgets=[
                _required_widget(target.origin, target.widget_id) for target in governed_targets
            ],
            required_generated_widgets=[_wave3_required_generated(note_name, governed_token)],
            governance=governance,
        )
    )

    widget_id = _snake_case(widget_name)
    tab_id = _snake_case(tab_name)
    widget_def = _widget_def(widget_name, f"/{widget_id}", grid=(40, 10))
    app_def = _app(app_name, [(tab_id, tab_name, [(widget_id, 0, 0, 40, 10, None)])])
    build_targets = (primary, cross_catalog)
    build_names = "; ".join(_wave3_target_words(target) for target in build_targets)
    tasks.append(
        _record(
            "curate",
            spine,
            5,
            "platform",
            (
                f"{title} build board: add {backend_name} with a {widget_name} table and "
                f"publish and instantiate {app_name} on {tab_name}; also add {build_names}. "
                "Widget ids are the snake_case of widget names; tab ids are the snake_case "
                "of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": url,
                        "widgets_json": {widget_id: widget_def},
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": f"{title} Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
                *_wave3_discover_targets(build_targets),
                *(_wave3_place_call(target) for target in build_targets),
            ],
            targets=(
                _custom_target(backend_name, widget_id, widget_name),
                *build_targets,
            ),
            required_widgets=[
                _required_widget(backend_name, widget_id, tab_id=tab_id),
                *(_required_widget(target.origin, target.widget_id) for target in build_targets),
            ],
            required_widget_defs=[
                {"backend_name": backend_name, "widget_id": widget_id, "expect": {"type": "table"}}
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": [tab_id],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": tab_id, "widget_id": widget_id}],
                }
            ],
        )
    )
    return tasks


def _build_wave3_curate_tasks() -> list[TaskRecord]:
    compliance_alerts = _wave3_catalog_target(
        STARK,
        "compliance_surveillance_hub_alerts_open_alert_metrics",
        "Open Alert Metrics",
        "Compliance Surveillance Hub",
        "Open Alert Metrics",
    )
    policy_breaches = _wave3_catalog_target(
        STARK,
        "compliance_surveillance_hub_personal_trading_policy_breaches",
        "Policy Breaches",
        "Compliance Surveillance Hub",
        "Policy Breaches",
    )
    basic_table = _wave3_catalog_target(
        GETTING_STARTED,
        "markdown_widget_with_number_input",
        "Markdown Widget with Number Input",
    )
    live_orders = _wave3_catalog_target(
        STARK,
        "execution_desk_blotter_live_orders",
        "Live Orders",
        "Execution Desk",
        "Live Orders",
    )
    broker_scorecard = _wave3_catalog_target(
        STARK,
        "execution_desk_fills_broker_scorecard",
        "Broker Scorecard",
        "Execution Desk",
        "Broker Scorecard",
    )
    pdfs = _wave3_catalog_target(
        GETTING_STARTED,
        "multi_pdf_url",
        "Multi PDF Viewer - URL",
    )
    return [
        *_build_wave3_curate_spine(
            spine="compliance_alert_review",
            title="Compliance-alert",
            primary=compliance_alerts,
            same_app=policy_breaches,
            cross_catalog=basic_table,
            governance=GovernanceSpec(
                "get_skill_content",
                "finance-guidance-tracker",
                "Finance Guidance Tracker skill (finance-guidance-tracker)",
                ("evidence gaps",),
            ),
            backend_name="Wave Three Compliance Review",
            widget_name="Compliance Review Register",
            app_name="Compliance Review App",
            tab_name="Review",
            url="http://127.0.0.1:9703",
        ),
        *_build_wave3_curate_spine(
            spine="execution_quality_review",
            title="Execution-quality",
            primary=live_orders,
            same_app=broker_scorecard,
            cross_catalog=pdfs,
            governance=GovernanceSpec(
                "get_skill_content",
                "finance-comps",
                "Finance Comps skill (finance-comps)",
                ("outliers",),
            ),
            backend_name="Wave Three Execution Review",
            widget_name="Execution Review Register",
            app_name="Execution Review App",
            tab_name="Quality",
            url="http://127.0.0.1:9704",
        ),
    ]


def _wave3_stage(
    name: str,
    targets: tuple[TargetSpec, ...],
    initial_args: tuple[JsonDict, ...],
) -> JsonDict:
    return _staged_dashboard(
        name,
        [
            {
                "origin": target.origin,
                "widget_id": target.widget_id,
                "widget_uuid": f"wave3_{_snake_case(name)}_{index}",
                "tab_id": "review",
                "data_args": data_args,
                "layout": {"x": 0, "y": index * 12, "w": 40, "h": 12},
            }
            for index, (target, data_args) in enumerate(zip(targets, initial_args, strict=True))
        ],
    )


def _wave3_update_call(widget_uuid: str, data_args: JsonDict) -> JsonDict:
    return _call(
        "update_widget",
        {"widget_uuid": widget_uuid, "data_args": data_args},
        graded_args=("data_args",),
    )


def _wave3_args_words(data_args: JsonDict, *, level0: bool = False) -> str:
    if level0:
        return ", ".join(f"{key} set to {value}" for key, value in data_args.items())
    return ", ".join(f"{key} {value}" for key, value in data_args.items())


def _build_wave3_parameterize_spine(
    *,
    spine: str,
    title: str,
    board_name: str,
    targets: tuple[TargetSpec, TargetSpec, TargetSpec],
    initial_args: tuple[JsonDict, JsonDict, JsonDict],
    final_args: tuple[JsonDict, JsonDict, JsonDict],
    governance: GovernanceSpec,
    governed_index: int,
    governed_args: JsonDict,
) -> list[TaskRecord]:
    stage = _wave3_stage(board_name, targets, initial_args)
    uuids = tuple(f"wave3_{_snake_case(board_name)}_{index}" for index in range(len(targets)))
    tasks: list[TaskRecord] = []
    low_specs = (
        (0, 0, final_args[0]),
        (1, 0, final_args[0]),
        (2, 1, final_args[1]),
    )
    for level, target_index, data_args in low_specs:
        target = targets[target_index]
        tools: list[JsonDict] = []
        if level in {0, 1}:
            tools.append(_snapshot())
        if level == 1:
            tools.append(_call("read_widget", {"widget_id": target.widget_id}, optional=True))
        tools.append(_wave3_update_call(uuids[target_index], data_args))
        tasks.append(
            _record(
                "parameterize",
                spine,
                level,
                "single-widget",
                (
                    f"{title} level-{level} change: on the open {board_name} board, set "
                    f"{target.display_name} with {_wave3_args_words(data_args, level0=level == 0)} "
                    "and preserve the other views."
                ),
                tools,
                targets=(target,),
                pinned_widget_args={(target.origin, target.widget_id): frozenset(data_args)},
                required_widgets=[_required_widget(target.origin, target.widget_id, data_args)],
                selected_dashboard=board_name,
                initial_state=stage,
            )
        )

    pair = targets[:2]
    tasks.append(
        _record(
            "parameterize",
            spine,
            3,
            "single-widget",
            (
                f"{title} paired change: on the open {board_name} board, set "
                f"{pair[0].display_name} with {_wave3_args_words(final_args[0])}; set "
                f"{pair[1].display_name} with {_wave3_args_words(final_args[1])}; preserve "
                "the last view."
            ),
            [
                _wave3_update_call(uuids[0], final_args[0]),
                _wave3_update_call(uuids[1], final_args[1]),
            ],
            targets=pair,
            pinned_widget_args={
                (target.origin, target.widget_id): frozenset(args)
                for target, args in zip(pair, final_args[:2], strict=True)
            },
            required_widgets=[
                _required_widget(target.origin, target.widget_id, args)
                for target, args in zip(pair, final_args[:2], strict=True)
            ],
            selected_dashboard=board_name,
            initial_state=stage,
        )
    )

    governed_target = targets[governed_index]
    tasks.append(
        _record(
            "parameterize",
            spine,
            4,
            "single-widget",
            (
                f"{title} governed change: follow the {governance.label} on the open "
                f"{board_name} board, then set {governed_target.display_name} with "
                f"{_wave3_args_words(governed_args)} and preserve the other views. "
                f"The governing concepts are {', '.join(governance.outcome_tokens)}."
            ),
            [
                _wave3_governance_call(governance),
                _wave3_update_call(uuids[governed_index], governed_args),
            ],
            targets=(governed_target,),
            pinned_widget_args={
                (governed_target.origin, governed_target.widget_id): frozenset(governed_args)
            },
            required_widgets=[
                _required_widget(
                    governed_target.origin,
                    governed_target.widget_id,
                    governed_args,
                )
            ],
            governance=governance,
            selected_dashboard=board_name,
            initial_state=stage,
        )
    )

    tasks.append(
        _record(
            "parameterize",
            spine,
            5,
            "single-widget",
            (
                f"{title} full reset: on the open {board_name} board, set "
                + "; set ".join(
                    f"{target.display_name} with {_wave3_args_words(args)}"
                    for target, args in zip(targets, final_args, strict=True)
                )
                + "; preserve all layout and surrounding content."
            ),
            [
                _wave3_update_call(widget_uuid, args)
                for widget_uuid, args in zip(uuids, final_args, strict=True)
            ],
            targets=targets,
            pinned_widget_args={
                (target.origin, target.widget_id): frozenset(args)
                for target, args in zip(targets, final_args, strict=True)
            },
            required_widgets=[
                _required_widget(target.origin, target.widget_id, args)
                for target, args in zip(targets, final_args, strict=True)
            ],
            selected_dashboard=board_name,
            initial_state=stage,
        )
    )
    return tasks


def _build_wave3_parameterize_tasks() -> list[TaskRecord]:
    client_targets = (
        _wave3_catalog_target(
            WIDGET_EXAMPLES,
            "form_submit_widget",
            "Financial Entry Form",
            staged=True,
        ),
        _wave3_catalog_target(GETTING_STARTED, "all_forms", "Entry Form", staged=True),
        _wave3_catalog_target(
            GETTING_STARTED,
            "markdown_widget_with_text_input",
            "Markdown Widget with Text Input",
            staged=True,
        ),
    )
    client_initial = (
        {
            "client_first_name": "Alex",
            "client_last_name": "Rivera",
            "risk_profile": "Conservative",
            "add_record": False,
        },
        {
            "client_first_name": "Taylor",
            "client_last_name": "Morgan",
            "risk_profile": "Balanced",
            "add_record": False,
        },
        {"name": "Pending"},
    )
    client_final = (
        {
            "client_first_name": "Maya",
            "client_last_name": "Chen",
            "risk_profile": "Moderate",
            "add_record": True,
        },
        {
            "client_first_name": "Noah",
            "client_last_name": "Patel",
            "risk_profile": "Balanced",
            "add_record": True,
        },
        {"name": "Intake Ready"},
    )
    crypto_targets = (
        _wave3_catalog_target(
            WIDGET_EXAMPLES,
            "html_binance_ohlc",
            "Binance OHLC",
            staged=True,
        ),
        _wave3_catalog_target(GETTING_STARTED, "omni_sql_widget", "SQL Query Widget", staged=True),
        _wave3_catalog_target(
            WIDGET_EXAMPLES,
            "moving_parameters_example",
            "Moving Parameters Example",
            staged=True,
        ),
    )
    crypto_initial = (
        {"symbol": "BTCUSDT", "interval": "30m", "exchange": "BinanceUS"},
        {"prompt": "SELECT * FROM DATA LIMIT 5"},
        {
            "datePicker1": "$currentDate-1d",
            "textBox1": "Hello!",
            "TrueFalse": True,
            "daysPicker1": "1",
        },
    )
    crypto_final = (
        {"symbol": "ethusdt", "interval": "1m", "exchange": "binancef"},
        {"prompt": "SELECT * FROM DATA LIMIT 3"},
        {
            "datePicker1": "$currentDate-1d",
            "textBox1": "Ready",
            "TrueFalse": True,
            "daysPicker1": "1",
        },
    )
    governed_sql = {"prompt": "SELECT * FROM DATA LIMIT 3 -- growth-rate reversals"}
    return [
        *_build_wave3_parameterize_spine(
            spine="client_intake_controls",
            title="Client-intake",
            board_name="Client Intake Controls",
            targets=client_targets,
            initial_args=client_initial,
            final_args=client_final,
            governance=GovernanceSpec(
                "read_workspace_resource",
                "openbb://workspace/specs/widget-parameters",
                "Widget Parameters resource (openbb://workspace/specs/widget-parameters)",
                ("form", "button"),
            ),
            governed_index=0,
            governed_args=client_final[0],
        ),
        *_build_wave3_parameterize_spine(
            spine="crypto_display_controls",
            title="Crypto-display",
            board_name="Crypto Display Controls",
            targets=crypto_targets,
            initial_args=crypto_initial,
            final_args=crypto_final,
            governance=GovernanceSpec(
                "get_skill_content",
                "daloopa-inflection",
                "Daloopa Inflection skill (daloopa-inflection)",
                ("growth-rate reversals",),
            ),
            governed_index=1,
            governed_args=governed_sql,
        ),
    ]


def _build_wave3_organize_spine(
    *,
    spine: str,
    title: str,
    board_name: str,
    targets: tuple[TargetSpec, TargetSpec, TargetSpec],
    governance: GovernanceSpec,
    governed_tabs: tuple[str, str],
    backend_name: str,
    widget_name: str,
    app_name: str,
    tab_name: str,
    url: str,
) -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    tasks.append(
        _record(
            "organize",
            spine,
            0,
            "dashboard",
            f"{title} board start: create and open {board_name}.",
            [
                _snapshot(),
                _call(
                    "manage_dashboard",
                    {"operation": "create", "name": board_name, "activate": True},
                    graded_args=("operation", "name"),
                ),
            ],
            required_dashboard_name=board_name,
        )
    )
    basic_tabs = ("Overview", "Review")
    tasks.append(
        _record(
            "organize",
            spine,
            1,
            "dashboard",
            f"{title} tab setup: create and open {board_name}, then add Overview and Review tabs.",
            [
                _snapshot(),
                _call(
                    "manage_dashboard",
                    {"operation": "create", "name": board_name, "activate": True},
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_navigation_bar",
                    {"operation": "add_tabs", "tabs": [{"name": name} for name in basic_tabs]},
                    graded_args=("tabs",),
                ),
            ],
            required_dashboard_name=board_name,
            required_tabs=[_snake_case(name) for name in basic_tabs],
        )
    )
    for level, chosen in ((2, targets[:1]), (3, targets[:2])):
        names = ", ".join(f"{target.origin}'s {target.display_name}" for target in chosen)
        tasks.append(
            _record(
                "organize",
                spine,
                level,
                "dashboard",
                (
                    f"{title} level-{level} layout: create and open {board_name}, add Overview "
                    f"and Review tabs, then add {names}."
                ),
                [
                    _call(
                        "manage_dashboard",
                        {"operation": "create", "name": board_name, "activate": True},
                        graded_args=("operation", "name"),
                    ),
                    _call(
                        "manage_navigation_bar",
                        {"operation": "add_tabs", "tabs": [{"name": name} for name in basic_tabs]},
                        graded_args=("tabs",),
                    ),
                    *_wave3_discover_targets(chosen),
                    *(_wave3_place_call(target) for target in chosen),
                ],
                targets=chosen,
                required_dashboard_name=board_name,
                required_tabs=[_snake_case(name) for name in basic_tabs],
                required_widgets=[
                    _required_widget(target.origin, target.widget_id) for target in chosen
                ],
            )
        )

    governed_targets = (targets[0], targets[2])
    governed_names = ", ".join(
        f"{target.origin}'s {target.display_name}" for target in governed_targets
    )
    tasks.append(
        _record(
            "organize",
            spine,
            4,
            "dashboard",
            (
                f"{title} governed layout: follow the {governance.label}; create and open "
                f"{board_name}, add {governed_tabs[0]} and {governed_tabs[1]} tabs, and add "
                f"{governed_names}."
            ),
            [
                _wave3_governance_call(governance),
                _call(
                    "manage_dashboard",
                    {"operation": "create", "name": board_name, "activate": True},
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_navigation_bar",
                    {
                        "operation": "add_tabs",
                        "tabs": [{"name": name} for name in governed_tabs],
                    },
                    graded_args=("tabs",),
                ),
                *_wave3_discover_targets(governed_targets),
                *(_wave3_place_call(target) for target in governed_targets),
            ],
            targets=governed_targets,
            required_dashboard_name=board_name,
            required_tabs=[name.casefold().replace(" ", "-") for name in governed_tabs],
            required_widgets=[
                _required_widget(target.origin, target.widget_id) for target in governed_targets
            ],
            governance=governance,
        )
    )

    widget_id = _snake_case(widget_name)
    tab_id = _snake_case(tab_name)
    widget_def = _widget_def(widget_name, f"/{widget_id}", grid=(40, 10))
    app_def = _app(app_name, [(tab_id, tab_name, [(widget_id, 0, 0, 40, 10, None)])])
    build_targets = targets[1:]
    build_names = ", ".join(f"{target.origin}'s {target.display_name}" for target in build_targets)
    tasks.append(
        _record(
            "organize",
            spine,
            5,
            "platform",
            (
                f"{title} navigation build: add {backend_name} with a {widget_name} table, "
                f"publish and instantiate {app_name} on {tab_name}, then add {build_names}. "
                "Widget ids are the snake_case of widget names; tab ids are the snake_case "
                "of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": url,
                        "widgets_json": {widget_id: widget_def},
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": f"{title} Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
                *_wave3_discover_targets(build_targets),
                *(_wave3_place_call(target) for target in build_targets),
            ],
            targets=(_custom_target(backend_name, widget_id, widget_name), *build_targets),
            required_widgets=[
                _required_widget(backend_name, widget_id, tab_id=tab_id),
                *(_required_widget(target.origin, target.widget_id) for target in build_targets),
            ],
            required_widget_defs=[
                {"backend_name": backend_name, "widget_id": widget_id, "expect": {"type": "table"}}
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": [tab_id],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": tab_id, "widget_id": widget_id}],
                }
            ],
        )
    )
    return tasks


def _build_wave3_organize_tasks() -> list[TaskRecord]:
    media_targets = (
        _wave3_catalog_target(
            GETTING_STARTED,
            "get_video_with_transcript",
            "Video Library with Transcript",
        ),
        _wave3_catalog_target(GETTING_STARTED, "pdf_widget_url", "PDF Widget with URL"),
        _wave3_catalog_target(WIDGET_EXAMPLES, "url_pdf", "URL PDF files"),
    )
    chart_targets = (
        _wave3_catalog_target(GETTING_STARTED, "chains_highchart", "Chains TVL Highcharts"),
        _wave3_catalog_target(GETTING_STARTED, "vega_bar", "Vega-Lite Bar Demo"),
        _wave3_catalog_target(WIDGET_EXAMPLES, "vega_scatter_demo", "Vega-Lite Scatter Demo"),
    )
    return [
        *_build_wave3_organize_spine(
            spine="due_diligence_media_room",
            title="Media-room",
            board_name="Due Diligence Media Room",
            targets=media_targets,
            governance=GovernanceSpec(
                "get_skill_content",
                "finance-tearsheet",
                "Finance Tearsheet skill (finance-tearsheet)",
                ("catalysts", "risks"),
            ),
            governed_tabs=("Catalysts", "Risks"),
            backend_name="Wave Three Media Room",
            widget_name="Media Review Register",
            app_name="Media Room App",
            tab_name="Media",
            url="http://127.0.0.1:9705",
        ),
        *_build_wave3_organize_spine(
            spine="visualization_gallery",
            title="Visualization-gallery",
            board_name="Visualization Gallery",
            targets=chart_targets,
            governance=GovernanceSpec(
                "get_skill_content",
                "finance-comps",
                "Finance Comps skill (finance-comps)",
                ("valuation multiples", "outliers"),
            ),
            governed_tabs=("Valuation Multiples", "Outliers"),
            backend_name="Wave Three Visualization Gallery",
            widget_name="Visualization Review Register",
            app_name="Visualization Gallery App",
            tab_name="Gallery",
            url="http://127.0.0.1:9706",
        ),
    ]


def _wave3_repair_stage(
    board_name: str,
    primary: TargetSpec,
    secondary: TargetSpec,
    primary_args: JsonDict,
    secondary_args: JsonDict,
    *,
    duplicate: bool = False,
    overlap: bool = False,
) -> JsonDict:
    widgets: list[JsonDict] = [
        {
            "origin": primary.origin,
            "widget_id": primary.widget_id,
            "widget_uuid": f"{_snake_case(board_name)}_primary",
            "tab_id": "review",
            "data_args": primary_args,
            "layout": {"x": 0, "y": 0, "w": 40, "h": 12},
        },
        {
            "origin": secondary.origin,
            "widget_id": secondary.widget_id,
            "widget_uuid": f"{_snake_case(board_name)}_preserved",
            "tab_id": "review",
            "data_args": secondary_args,
            "layout": {"x": 0, "y": 0 if overlap else 12, "w": 40, "h": 12},
        },
    ]
    if duplicate:
        widgets.append(
            {
                "origin": primary.origin,
                "widget_id": primary.widget_id,
                "widget_uuid": f"{_snake_case(board_name)}_duplicate",
                "tab_id": "review",
                "data_args": primary_args,
                "layout": {"x": 0, "y": 24, "w": 40, "h": 12},
            }
        )
    return _staged_dashboard(board_name, widgets)


def _build_wave3_repair_spine(
    *,
    spine: str,
    title: str,
    board_name: str,
    primary: TargetSpec,
    secondary: TargetSpec,
    wrong_args: JsonDict,
    correct_args: JsonDict,
    secondary_args: JsonDict,
    governance: GovernanceSpec,
    backend_name: str,
    widget_name: str,
    app_name: str,
    tab_name: str,
    url: str,
) -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    primary_uuid = f"{_snake_case(board_name)}_primary"
    preserved_uuid = f"{_snake_case(board_name)}_preserved"
    bad_stage = _wave3_repair_stage(
        board_name,
        primary,
        secondary,
        wrong_args,
        secondary_args,
    )
    tasks.append(
        _record(
            "repair",
            spine,
            0,
            "repair",
            (
                f"{title} direct fix: on the open {board_name} board, set "
                f"{primary.display_name} with {_wave3_args_words(correct_args, level0=True)}."
            ),
            [_snapshot(), _wave3_update_call(primary_uuid, correct_args)],
            targets=(primary,),
            pinned_widget_args={(primary.origin, primary.widget_id): frozenset(correct_args)},
            required_widgets=[_required_widget(primary.origin, primary.widget_id, correct_args)],
            selected_dashboard=board_name,
            initial_state=bad_stage,
        )
    )
    tasks.append(
        _record(
            "repair",
            spine,
            1,
            "repair",
            (
                f"{title} preserved fix: on the open {board_name} board, restore "
                f"{primary.display_name} with {_wave3_args_words(correct_args)} and preserve "
                f"{secondary.display_name}."
            ),
            [_snapshot(), _wave3_update_call(primary_uuid, correct_args)],
            targets=(primary, secondary),
            pinned_widget_args={(primary.origin, primary.widget_id): frozenset(correct_args)},
            required_widgets=[
                _required_widget(primary.origin, primary.widget_id, correct_args),
                _required_widget(secondary.origin, secondary.widget_id),
            ],
            selected_dashboard=board_name,
            initial_state=bad_stage,
        )
    )

    duplicate_stage = _wave3_repair_stage(
        board_name,
        primary,
        secondary,
        correct_args,
        secondary_args,
        duplicate=True,
    )
    duplicate_uuid = f"{_snake_case(board_name)}_duplicate"
    tasks.append(
        _record(
            "repair",
            spine,
            2,
            "repair",
            (
                f"{title} duplicate cleanup: the open {board_name} board has an extra "
                f"{primary.display_name}; the {title.casefold()} duplicate marker identifies "
                f"it. Remove that copy and preserve {secondary.display_name}."
            ),
            [
                _call(
                    "delete_widget",
                    {"widget_uuid": duplicate_uuid},
                    graded_args=("widget_uuid",),
                )
            ],
            targets=(primary, secondary),
            policies=(PolicyMapping(f"{title.casefold()} duplicate marker", (duplicate_uuid,)),),
            required_widgets=[
                _required_widget(primary.origin, primary.widget_id, min_count=1, max_count=1),
                _required_widget(secondary.origin, secondary.widget_id),
            ],
            selected_dashboard=board_name,
            initial_state=duplicate_stage,
        )
    )

    overlap_stage = _wave3_repair_stage(
        board_name,
        primary,
        secondary,
        correct_args,
        secondary_args,
        overlap=True,
    )
    tasks.append(
        _record(
            "repair",
            spine,
            3,
            "repair",
            (
                f"{title} overlap fix: on the open {board_name} board, move "
                f"{secondary.display_name} to x 0, y 12, width 40, height 12 on Review; "
                f"preserve {primary.display_name}."
            ),
            [
                _call(
                    "update_widget_layout",
                    {
                        "widget_uuid": preserved_uuid,
                        "x": 0,
                        "y": 12,
                        "w": 40,
                        "h": 12,
                        "tab_id": "review",
                    },
                    graded_args=("x", "y", "w", "h", "tab_id"),
                )
            ],
            targets=(primary, secondary),
            required_widgets=[
                _required_widget(primary.origin, primary.widget_id),
                _required_widget(secondary.origin, secondary.widget_id),
            ],
            selected_dashboard=board_name,
            initial_state=overlap_stage,
        )
    )

    note_name = f"{title} Governance Note"
    governed_token = governance.outcome_tokens[0]
    tasks.append(
        _record(
            "repair",
            spine,
            4,
            "repair",
            (
                f"{title} governed repair: follow the {governance.label} on the open "
                f"{board_name} board, restore {primary.display_name} with "
                f"{_wave3_args_words(correct_args)}, preserve {secondary.display_name}, and "
                f"add a {_note_phrase(note_name)} naming {governed_token}."
            ),
            [
                _wave3_governance_call(governance),
                _wave3_update_call(primary_uuid, correct_args),
                _wave3_generated_call(note_name, governed_token),
            ],
            targets=(primary, secondary),
            pinned_widget_args={(primary.origin, primary.widget_id): frozenset(correct_args)},
            required_widgets=[
                _required_widget(primary.origin, primary.widget_id, correct_args),
                _required_widget(secondary.origin, secondary.widget_id),
            ],
            required_generated_widgets=[_wave3_required_generated(note_name, governed_token)],
            governance=governance,
            selected_dashboard=board_name,
            initial_state=bad_stage,
        )
    )

    widget_id = _snake_case(widget_name)
    tab_id = _snake_case(tab_name)
    fixed_widget = _widget_def(widget_name, f"/{widget_id}", grid=(40, 10))
    fixed_app = _app(app_name, [(tab_id, tab_name, [(widget_id, 0, 0, 40, 10, None)])])
    custom_board = f"{title} Backend Repair"
    custom_state = _staged_dashboard(
        custom_board,
        [
            {
                "origin": backend_name,
                "widget_id": widget_id,
                "widget_uuid": f"{spine}_custom",
                "tab_id": tab_id,
                "layout": {"x": 0, "y": 0, "w": 40, "h": 10},
            }
        ],
        tabs=[{"id": tab_id, "name": tab_name}],
    )
    custom_state["custom_backends"] = [
        {
            "backend_id": "backend_005",
            "name": backend_name,
            "url": url,
            "widgets_json": {widget_id: {"name": widget_name, "type": "table"}},
            "apps_json": [{"name": app_name, "tabs": {}}],
            "warnings": ["missing endpoint and app layout"],
        }
    ]
    tasks.append(
        _record(
            "repair",
            spine,
            5,
            "repair",
            (
                f"{title} backend rebuild: on the open {custom_board} board, refresh "
                f"{backend_name} so its {widget_name} table is published through {app_name} "
                f"on {tab_name}. Widget ids are the snake_case of widget names; tab ids are "
                "the snake_case of tab names."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "refresh",
                        "backend_id": "backend_005",
                        "widgets_json": {widget_id: fixed_widget},
                        "apps_json": [fixed_app],
                    },
                    graded_args=("operation",),
                )
            ],
            targets=(_custom_target(backend_name, widget_id, widget_name, staged=True),),
            required_widgets=[_required_widget(backend_name, widget_id, tab_id=tab_id)],
            required_widget_defs=[
                {"backend_name": backend_name, "widget_id": widget_id, "expect": {"type": "table"}}
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": [tab_id],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": tab_id, "widget_id": widget_id}],
                }
            ],
            selected_dashboard=custom_board,
            initial_state=custom_state,
        )
    )
    return tasks


def _build_wave3_repair_tasks() -> list[TaskRecord]:
    vendor_primary = _wave3_catalog_target(
        STARK,
        "vendor_dataset_monitor_vendors_sla_metrics",
        "SLA Metrics",
        staged=True,
    )
    vendor_secondary = _wave3_catalog_target(
        STARK,
        "vendor_dataset_monitor_vendors_vendor_contract_terms",
        "Vendor Contract Terms",
        staged=True,
    )
    protocol_primary = _wave3_catalog_target(
        WIDGET_EXAMPLES,
        "defi_llama_protocol_details",
        "Defi Llama Protocol Details",
        staged=True,
    )
    server_grid = _wave3_catalog_target(
        WIDGET_EXAMPLES,
        "demo_data_ssrm",
        "Demo Financial Data (SSRM)",
        staged=True,
    )
    return [
        *_build_wave3_repair_spine(
            spine="vendor_freshness_repair",
            title="Vendor-freshness",
            board_name="Vendor Freshness Repair",
            primary=vendor_primary,
            secondary=vendor_secondary,
            wrong_args={"vendor": "FactSet", "status": "Closed", "period": "1Y"},
            correct_args={"vendor": "Bloomberg", "status": "Open", "period": "QTD"},
            secondary_args={"vendor": "FactSet", "status": "Open", "period": "YTD"},
            governance=GovernanceSpec(
                "get_skill_content",
                "finance-guidance-tracker",
                "Finance Guidance Tracker skill (finance-guidance-tracker)",
                ("evidence gaps",),
            ),
            backend_name="Wave Three Vendor Repair",
            widget_name="Vendor Repair Queue",
            app_name="Vendor Repair App",
            tab_name="Incidents",
            url="http://127.0.0.1:9707",
        ),
        *_build_wave3_repair_spine(
            spine="protocol_display_repair",
            title="Protocol-display",
            board_name="Protocol Display Repair",
            primary=protocol_primary,
            secondary=server_grid,
            wrong_args={"protocol_id": "aave"},
            correct_args={"protocol_id": "uniswap"},
            secondary_args={},
            governance=GovernanceSpec(
                "get_skill_content",
                "daloopa-inflection",
                "Daloopa Inflection skill (daloopa-inflection)",
                ("growth-rate reversals",),
            ),
            backend_name="Wave Three Protocol Repair",
            widget_name="Protocol Repair Queue",
            app_name="Protocol Repair App",
            tab_name="Protocols",
            url="http://127.0.0.1:9708",
        ),
    ]


def _build_wave3_platform_spine(
    *,
    spine: str,
    title: str,
    skill_slug: str,
    skill_label: str,
    governed_token: str,
    targets: tuple[TargetSpec, TargetSpec],
    backend_name: str,
    widget_name: str,
    app_name: str,
    tab_name: str,
    url: str,
) -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    governance = GovernanceSpec(
        "get_skill_content",
        skill_slug,
        skill_label,
        (governed_token,),
    )
    for level in (0, 1):
        note_name = f"{title} {('Starter', 'Discovery')[level]} Note"
        tasks.append(
            _record(
                "platform",
                spine,
                level,
                "platform",
                (
                    f"{title} level-{level} workflow: read the {skill_label} and add a "
                    f"{_note_phrase(note_name)} containing {governed_token}."
                ),
                [
                    _snapshot(),
                    _wave3_governance_call(governance),
                    _wave3_generated_call(note_name, governed_token),
                ],
                required_generated_widgets=[_wave3_required_generated(note_name, governed_token)],
            )
        )

    primary = targets[0]
    tasks.append(
        _record(
            "platform",
            spine,
            2,
            "platform",
            (
                f"{title} governed placement: read the {skill_label}, then add "
                f"{primary.origin}'s {primary.display_name} for {governed_token}."
            ),
            [
                _wave3_governance_call(governance),
                *_wave3_discover_targets((primary,)),
                _wave3_place_call(primary),
            ],
            targets=(primary,),
            required_widgets=[_required_widget(primary.origin, primary.widget_id)],
        )
    )
    names = ", ".join(f"{target.origin}'s {target.display_name}" for target in targets)
    tasks.append(
        _record(
            "platform",
            spine,
            3,
            "platform",
            (
                f"{title} paired workflow: read the {skill_label}, then add {names} to "
                f"support {governed_token}."
            ),
            [
                _wave3_governance_call(governance),
                *_wave3_discover_targets(targets),
                *(_wave3_place_call(t) for t in targets),
            ],
            targets=targets,
            required_widgets=[_required_widget(t.origin, t.widget_id) for t in targets],
        )
    )
    note_name = f"{title} Governed Note"
    tasks.append(
        _record(
            "platform",
            spine,
            4,
            "platform",
            (
                f"{title} governed synthesis: follow the {skill_label}, add {names}, and "
                f"add a {_note_phrase(note_name)} containing {governed_token}."
            ),
            [
                _wave3_governance_call(governance),
                *_wave3_discover_targets(targets),
                *(_wave3_place_call(t) for t in targets),
                _wave3_generated_call(note_name, governed_token),
            ],
            targets=targets,
            required_widgets=[_required_widget(t.origin, t.widget_id) for t in targets],
            required_generated_widgets=[_wave3_required_generated(note_name, governed_token)],
            governance=governance,
        )
    )

    widget_id = _snake_case(widget_name)
    tab_id = _snake_case(tab_name)
    widget_def = _widget_def(widget_name, f"/{widget_id}", grid=(40, 10))
    app_def = _app(app_name, [(tab_id, tab_name, [(widget_id, 0, 0, 40, 10, None)])])
    build_note = f"{title} Build Note"
    tasks.append(
        _record(
            "platform",
            spine,
            5,
            "platform",
            (
                f"{title} governed build: read the {skill_label}, add {backend_name} with "
                f"a {widget_name} table, publish and instantiate {app_name} on {tab_name}, "
                f"and add a {_note_phrase(build_note)} containing {governed_token}. Widget ids are "
                "the snake_case of widget names; tab ids are the snake_case of tab names."
            ),
            [
                _wave3_governance_call(governance),
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": url,
                        "widgets_json": {widget_id: widget_def},
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": f"{title} Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
                _wave3_generated_call(build_note, governed_token),
            ],
            targets=(_custom_target(backend_name, widget_id, widget_name),),
            required_widgets=[_required_widget(backend_name, widget_id, tab_id=tab_id)],
            required_generated_widgets=[_wave3_required_generated(build_note, governed_token)],
            required_widget_defs=[
                {"backend_name": backend_name, "widget_id": widget_id, "expect": {"type": "table"}}
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": [tab_id],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": tab_id, "widget_id": widget_id}],
                }
            ],
        )
    )
    return tasks


def _build_wave3_platform_tasks() -> list[TaskRecord]:
    comps_targets = (
        _wave3_catalog_target(
            GETTING_STARTED,
            "plotly_chart_with_theme_and_toolbar_using_config_file",
            "Plotly Chart with Theme and Toolbar using Config File",
        ),
        _wave3_catalog_target(
            WIDGET_EXAMPLES,
            "chains_plotly",
            "Chains chart example Plotly with raw data",
        ),
    )
    snapshot_targets = (
        _wave3_catalog_target(GETTING_STARTED, "udf", "TradingView Chart"),
        _wave3_catalog_target(GETTING_STARTED, "html_widget", "HTML Widget"),
    )
    return [
        *_build_wave3_platform_spine(
            spine="comps_governance",
            title="Comps-governance",
            skill_slug="finance-comps",
            skill_label="Finance Comps skill (finance-comps)",
            governed_token="valuation multiples",
            targets=comps_targets,
            backend_name="Wave Three Comps Governance",
            widget_name="Comps Governance Register",
            app_name="Comps Governance App",
            tab_name="Comparables",
            url="http://127.0.0.1:9709",
        ),
        *_build_wave3_platform_spine(
            spine="investment_snapshot_governance",
            title="Investment-snapshot",
            skill_slug="finance-tearsheet",
            skill_label="Finance Tearsheet skill (finance-tearsheet)",
            governed_token="price action",
            targets=snapshot_targets,
            backend_name="Wave Three Investment Snapshot",
            widget_name="Investment Snapshot Register",
            app_name="Investment Snapshot App",
            tab_name="Snapshot",
            url="http://127.0.0.1:9710",
        ),
    ]


def _wave3_service_parts(
    names: tuple[str, ...],
    app_name: str,
    tab_names: tuple[str, ...],
) -> tuple[dict[str, JsonDict], JsonDict]:
    widgets = {
        _snake_case(name): _widget_def(name, f"/{_snake_case(name)}", grid=(40, 10))
        for name in names
    }
    tabs: list[tuple[str, str, list[tuple[str, int, int, int, int, JsonDict | None]]]] = [
        (
            _snake_case(tab_name),
            tab_name,
            [
                (
                    _snake_case(name),
                    0,
                    index * 10,
                    40,
                    10,
                    None,
                )
                for index, name in enumerate(
                    names
                    if len(tab_names) == 1
                    else names[:2]
                    if tab_name == tab_names[0]
                    else names[2:]
                )
            ],
        )
        for tab_name in tab_names
    ]
    return widgets, _app(app_name, tabs)


def _build_wave3_extend_spine(
    *,
    spine: str,
    title: str,
    backend_name: str,
    app_name: str,
    widget_names: tuple[str, str, str],
    governance: GovernanceSpec,
    url: str,
) -> list[TaskRecord]:
    tasks: list[TaskRecord] = []
    widget_ids = tuple(_snake_case(name) for name in widget_names)
    two_widgets, two_app = _wave3_service_parts(widget_names[:2], app_name, ("Review",))
    three_widgets, three_app = _wave3_service_parts(
        widget_names,
        app_name,
        ("Review", "Archive"),
    )

    for level in (0, 1):
        name = widget_names[level]
        widget_id = widget_ids[level]
        widgets = {widget_id: _widget_def(name, f"/{widget_id}", grid=(40, 10))}
        tasks.append(
            _record(
                "extend",
                spine,
                level,
                "platform",
                (
                    f"{title} level-{level} service: add a custom backend "
                    f"{backend_name} with the {name} table."
                ),
                [
                    _snapshot(),
                    _call(
                        "read_workspace_resource",
                        {"uri": "openbb://workspace/specs/widgets-json"},
                        optional=True,
                    ),
                    _call(
                        "manage_backends",
                        {
                            "operation": "add",
                            "name": backend_name,
                            "url": url,
                            "widgets_json": widgets,
                            "apps_json": [],
                        },
                        graded_args=("operation", "name"),
                    ),
                ],
                targets=(_custom_target(backend_name, widget_id, name),),
                required_widget_defs=[
                    {"backend_name": backend_name, "widget_id": widget_id, "expect": {}}
                ],
            )
        )

    first_two_targets = tuple(
        _custom_target(backend_name, widget_id, name)
        for widget_id, name in zip(widget_ids[:2], widget_names[:2], strict=True)
    )
    tasks.append(
        _record(
            "extend",
            spine,
            2,
            "platform",
            (
                f"{title} paired service: add a custom backend {backend_name} "
                f"with {widget_names[0]} and {widget_names[1]} tables."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": url,
                        "widgets_json": two_widgets,
                        "apps_json": [],
                    },
                    graded_args=("operation", "name"),
                )
            ],
            targets=first_two_targets,
            required_widget_defs=[
                {"backend_name": backend_name, "widget_id": widget_id, "expect": {}}
                for widget_id in widget_ids[:2]
            ],
        )
    )
    tasks.append(
        _record(
            "extend",
            spine,
            3,
            "platform",
            (
                f"{title} app service: add a custom backend {backend_name} with "
                f"{widget_names[0]} and {widget_names[1]} tables, publish {app_name} on "
                "Review, and instantiate it."
            ),
            [
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": url,
                        "widgets_json": two_widgets,
                        "apps_json": [two_app],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": f"{title} Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=first_two_targets,
            required_widgets=[
                _required_widget(backend_name, widget_id, tab_id="review")
                for widget_id in widget_ids[:2]
            ],
            required_widget_defs=[
                {"backend_name": backend_name, "widget_id": widget_id, "expect": {}}
                for widget_id in widget_ids[:2]
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["review"],
                    "layout_refs_valid": True,
                }
            ],
        )
    )
    tasks.append(
        _record(
            "extend",
            spine,
            4,
            "platform",
            (
                f"{title} governed service: follow the {governance.label}; add a "
                f"custom backend {backend_name} with {widget_names[0]} and "
                f"{widget_names[1]} tables, "
                f"publish {app_name} on Review, and instantiate it. Widget ids are the "
                "snake_case of widget names; tab ids are the snake_case of tab names."
            ),
            [
                _wave3_governance_call(governance),
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": url,
                        "widgets_json": two_widgets,
                        "apps_json": [two_app],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": f"{title} Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=first_two_targets,
            required_widgets=[
                _required_widget(backend_name, widget_id, tab_id="review")
                for widget_id in widget_ids[:2]
            ],
            required_widget_defs=[
                {"backend_name": backend_name, "widget_id": widget_id, "expect": {}}
                for widget_id in widget_ids[:2]
            ],
            governance=governance,
        )
    )

    all_targets = tuple(
        _custom_target(backend_name, widget_id, name)
        for widget_id, name in zip(widget_ids, widget_names, strict=True)
    )
    tasks.append(
        _record(
            "extend",
            spine,
            5,
            "platform",
            (
                f"{title} complete service: follow the widgets manifest specification; "
                f"add a custom backend {backend_name} with "
                f"{', '.join(widget_names)} tables, publish {app_name} "
                "with Review and Archive tabs, and instantiate it. Widget ids are the "
                "snake_case of widget names; tab ids are the snake_case of tab names."
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
                        "name": backend_name,
                        "url": url,
                        "widgets_json": three_widgets,
                        "apps_json": [three_app],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": f"{title} Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
            ],
            targets=all_targets,
            policies=(
                PolicyMapping(
                    "widgets manifest specification",
                    ("openbb://workspace/specs/widgets-json",),
                ),
            ),
            required_widgets=[
                _required_widget(
                    backend_name,
                    widget_id,
                    tab_id="review" if index < 2 else "archive",
                )
                for index, widget_id in enumerate(widget_ids)
            ],
            required_widget_defs=[
                {"backend_name": backend_name, "widget_id": widget_id, "expect": {}}
                for widget_id in widget_ids
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": ["review", "archive"],
                    "layout_refs_valid": True,
                    "no_overlaps": True,
                }
            ],
        )
    )
    return tasks


def _build_wave3_extend_tasks() -> list[TaskRecord]:
    return [
        *_build_wave3_extend_spine(
            spine="inflection_service_lifecycle",
            title="Inflection-service",
            backend_name="Wave Three Inflection Service",
            app_name="Inflection Service App",
            widget_names=(
                "Growth-Rate Reversals",
                "Quarterly Series Monitor",
                "Inflection Evidence Log",
            ),
            governance=GovernanceSpec(
                "get_skill_content",
                "daloopa-inflection",
                "Daloopa Inflection skill (daloopa-inflection)",
                ("growth-rate reversals",),
            ),
            url="http://127.0.0.1:9711",
        ),
        *_build_wave3_extend_spine(
            spine="guidance_service_lifecycle",
            title="Guidance-service",
            backend_name="Wave Three Guidance Service",
            app_name="Guidance Service App",
            widget_names=("Evidence Gaps", "Changed Assumptions", "Management Claims"),
            governance=GovernanceSpec(
                "get_skill_content",
                "finance-guidance-tracker",
                "Finance Guidance Tracker skill (finance-guidance-tracker)",
                ("evidence gaps",),
            ),
            url="http://127.0.0.1:9712",
        ),
    ]


def _build_wave3_handoff_spine(
    *,
    spine: str,
    title: str,
    board_name: str,
    source_slug: str,
    target: TargetSpec,
    data_args: JsonDict,
    tokens: tuple[str, str],
    fact_words: str,
    governance: GovernanceSpec,
    backend_name: str,
    widget_name: str,
    app_name: str,
    tab_name: str,
    url: str,
) -> list[TaskRecord]:
    stage = _staged_dashboard(board_name, [])
    tasks: list[TaskRecord] = []
    for level, rung in enumerate(("direct", "discovered", "analyst", "desk")):
        note_name = f"{title} {rung.title()} Note"
        tools: list[JsonDict] = []
        if level in {0, 1}:
            tools.append(_snapshot())
        tools.extend(_wave3_discover_targets((target,)))
        tools.extend(
            [
                _wave3_read_call(target, data_args),
                _wave3_generated_call(
                    note_name,
                    f"Observed {tokens[0]} and {tokens[1]} for follow-up.",
                ),
            ]
        )
        tasks.append(
            _record(
                "handoff",
                spine,
                level,
                "read",
                (
                    f"{title} {rung} handoff: on the open {board_name} board, read "
                    f"{target.origin}'s {target.display_name} with "
                    + ", ".join(f"{key} {value}" for key, value in data_args.items())
                    + f", then add a {_note_phrase(note_name)} recording {fact_words}."
                ),
                tools,
                targets=(target,),
                required_generated_widgets=[_wave3_required_generated(note_name, *tokens)],
                grounded_generated=(GroundedGenerated(source_slug, target.widget_id, tokens),),
                selected_dashboard=board_name,
                initial_state=stage,
            )
        )

    note_name = f"{title} Governed Handoff"
    governed_token = governance.outcome_tokens[0]
    assignment = {
        "task_requests": [
            {
                "id": f"{spine}_follow_up",
                "description": f"Review the {title} follow-up.",
                "assigned_holder_url": f"workspace://agents/{spine}",
                "assigned_agent_id": f"{spine}-agent",
            }
        ]
    }
    tasks.append(
        _record(
            "handoff",
            spine,
            4,
            "dashboard",
            (
                f"{title} governed handoff: follow the {governance.label} on the open "
                f"{board_name} board, read {target.origin}'s {target.display_name} with "
                + ", ".join(f"{key} {value}" for key, value in data_args.items())
                + f", add a {_note_phrase(note_name)} recording {fact_words} and "
                f"{governed_token}, then delegate the follow-up."
            ),
            [
                _wave3_governance_call(governance),
                *_wave3_discover_targets((target,)),
                _wave3_read_call(target, data_args),
                _wave3_generated_call(
                    note_name,
                    f"{governed_token}: observed {tokens[0]} and {tokens[1]}.",
                ),
                _call("assign_tasks_to_agents", assignment, graded_args=()),
            ],
            targets=(target,),
            required_generated_widgets=[
                _wave3_required_generated(note_name, governed_token, *tokens)
            ],
            grounded_generated=(GroundedGenerated(source_slug, target.widget_id, tokens),),
            governance=governance,
            selected_dashboard=board_name,
            initial_state=stage,
        )
    )

    widget_id = _snake_case(widget_name)
    tab_id = _snake_case(tab_name)
    widget_def = _widget_def(widget_name, f"/{widget_id}", grid=(40, 10))
    app_def = _app(app_name, [(tab_id, tab_name, [(widget_id, 0, 0, 40, 10, None)])])
    build_note = f"{title} Build Handoff"
    tasks.append(
        _record(
            "handoff",
            spine,
            5,
            "platform",
            (
                f"{title} build handoff: add {backend_name} with a {widget_name} table, "
                f"publish and instantiate {app_name} with one {tab_name} tab, add a "
                f"{_note_phrase(build_note)} grounded in {target.origin}'s "
                f"{target.display_name} with {fact_words}, then delegate. Widget ids are "
                "the snake_case of widget names; tab ids are the snake_case of tab names."
            ),
            [
                *_wave3_discover_targets((target,)),
                _wave3_read_call(target, data_args, optional=True),
                _call(
                    "manage_backends",
                    {
                        "operation": "add",
                        "name": backend_name,
                        "url": url,
                        "widgets_json": {widget_id: widget_def},
                        "apps_json": [app_def],
                    },
                    graded_args=("operation", "name"),
                ),
                _call(
                    "manage_apps",
                    {
                        "operation": "instantiate",
                        "backend_id": "backend_005",
                        "app_name": app_name,
                        "dashboard_name": f"{title} Live",
                        "activate": True,
                    },
                    graded_args=("operation",),
                ),
                _wave3_generated_call(
                    build_note,
                    f"Catalog facts: {tokens[0]} and {tokens[1]}.",
                ),
                _call("assign_tasks_to_agents", assignment, graded_args=()),
            ],
            targets=(
                _custom_target(backend_name, widget_id, widget_name),
                target,
            ),
            required_widgets=[_required_widget(backend_name, widget_id, tab_id=tab_id)],
            required_generated_widgets=[_wave3_required_generated(build_note, *tokens)],
            required_widget_defs=[
                {"backend_name": backend_name, "widget_id": widget_id, "expect": {"type": "table"}}
            ],
            required_app_defs=[
                {
                    "backend_name": backend_name,
                    "name_contains": app_name,
                    "tabs_include": [tab_id],
                    "layout_refs_valid": True,
                    "widgets_on_tab": [{"tab_id": tab_id, "widget_id": widget_id}],
                }
            ],
            grounded_generated=(GroundedGenerated(source_slug, target.widget_id, tokens),),
        )
    )
    return tasks


def _build_wave3_handoff_tasks() -> list[TaskRecord]:
    segment = _wave3_catalog_target(DALOOPA, "daloopa_segment_breakdown", "Segment Breakdown")
    consensus = _wave3_catalog_target(
        DALOOPA,
        "daloopa_consensus_estimates",
        "Consensus Estimates",
    )
    return [
        *_build_wave3_handoff_spine(
            spine="segment_mix_handoff",
            title="Segment-mix",
            board_name="Segment Mix Handoff",
            source_slug="support-daloopa-skills",
            target=segment,
            data_args={"ticker": "AAPL", "period": "2026Q1"},
            tokens=("iPhone", "52365.6"),
            fact_words="the top segment and its exact revenue_musd",
            governance=GovernanceSpec(
                "get_skill_content",
                "daloopa-tearsheet",
                "Daloopa Tearsheet skill (daloopa-tearsheet)",
                ("mix",),
            ),
            backend_name="Wave Three Segment Handoff",
            widget_name="Segment Handoff Register",
            app_name="Segment Handoff App",
            tab_name="Handoff",
            url="http://127.0.0.1:9713",
        ),
        *_build_wave3_handoff_spine(
            spine="consensus_exception_handoff",
            title="Consensus-exception",
            board_name="Consensus Exception Handoff",
            source_slug="support-daloopa-skills",
            target=consensus,
            data_args={"ticker": "AAPL"},
            tokens=("102070.1", "99404.2"),
            fact_words="the exact Total Revenue actual and consensus for 2026Q1",
            governance=GovernanceSpec(
                "get_skill_content",
                "daloopa-earnings-review",
                "Daloopa Earnings Review skill (daloopa-earnings-review)",
                ("consensus",),
            ),
            backend_name="Wave Three Consensus Handoff",
            widget_name="Consensus Handoff Register",
            app_name="Consensus Handoff App",
            tab_name="Handoff",
            url="http://127.0.0.1:9714",
        ),
    ]


def build_tasks() -> list[TaskRecord]:
    """Build the complete deterministic three-wave task lattice."""

    return [
        *_build_retrieve_tasks(),
        *_build_retrieve_wave2_tasks(),
        *_build_wave3_retrieve_tasks(),
        *_build_curate_tasks(),
        *_build_curate_wave2_tasks(),
        *_build_wave3_curate_tasks(),
        *_build_parameterize_tasks(),
        *_build_parameterize_wave2_tasks(),
        *_build_wave3_parameterize_tasks(),
        *_build_organize_tasks(),
        *_build_organize_wave2_tasks(),
        *_build_wave3_organize_tasks(),
        *_build_repair_tasks(),
        *_build_repair_wave2_tasks(),
        *_build_wave3_repair_tasks(),
        *_build_platform_tasks(),
        *_build_platform_wave2_tasks(),
        *_build_wave3_platform_tasks(),
        *_build_extend_tasks(),
        *_build_extend_wave2_tasks(),
        *_build_wave3_extend_tasks(),
        *_build_handoff_tasks(),
        *_build_handoff_wave2_tasks(),
        *_build_wave3_handoff_tasks(),
    ]


def _catalogs() -> dict[str, JsonDict]:
    return {
        slug: json.loads(path.read_text(encoding="utf-8")) for slug, path in BACKEND_FILES.items()
    }


def _walk_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        return [item for nested in value.values() for item in _walk_values(nested)]
    if isinstance(value, list):
        return [item for nested in value for item in _walk_values(nested)]
    return [str(value)]


def _walk_leaves(value: Any, path: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], Any]]:
    if isinstance(value, dict):
        return [
            leaf
            for key, nested in value.items()
            for leaf in _walk_leaves(nested, (*path, str(key)))
        ]
    if isinstance(value, list):
        return [
            leaf
            for index, nested in enumerate(value)
            for leaf in _walk_leaves(nested, (*path, str(index)))
        ]
    return [(path, value)]


def _contains_forbidden_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, (dict, list)):
        if not value:
            return True
        nested = value.values() if isinstance(value, dict) else value
        return any(_contains_forbidden_empty(item) for item in nested)
    return False


def _literal_in_prompt(value: Any, prompt: str) -> bool:
    if isinstance(value, bool):
        rendered = "true" if value else "false"
    else:
        rendered = str(value)
    return rendered.casefold() in prompt.casefold()


def _param_defaults(definition: JsonDict) -> dict[str, Any]:
    defaults: dict[str, Any] = {}

    def visit(value: Any) -> None:
        if isinstance(value, list):
            for item in value:
                visit(item)
        elif isinstance(value, dict):
            name = value.get("paramName")
            if isinstance(name, str) and "value" in value:
                defaults[name] = value["value"]
            for nested in value.values():
                if isinstance(nested, (dict, list)):
                    visit(nested)

    visit(definition.get("params", []))
    return defaults


def _value_has_provenance(
    value: Any,
    *,
    prompt: str,
    policies: tuple[PolicyMapping, ...],
    default: Any = ...,  # type: ignore[assignment]
) -> bool:
    if _literal_in_prompt(value, prompt):
        return True
    if any(value in policy.values for policy in policies):
        return True
    return default is not ... and value == default


def _synthesized_contract(call: JsonDict) -> JsonDict | None:
    if call.get("optional"):
        return None
    args = call["args"]
    graded_args = call.get("graded_args")
    if graded_args == [] and call["tool"] == "assign_tasks_to_agents":
        return {}
    if not isinstance(graded_args, list) or not graded_args:
        raise AssertionError(f"{call['tool']}: missing explicit graded_args")
    missing = sorted(set(graded_args) - set(args))
    if missing:
        raise AssertionError(f"{call['tool']}: graded args absent from call: {missing}")
    return {key: args[key] for key in graded_args}


def _semantic_check_count(payload: JsonDict) -> int:
    evaluation = payload["eval"]
    count = sum(not bool(item.get("optional")) for item in evaluation.get("required_tools", []))
    for key in (
        "required_widgets",
        "required_values_in_answer",
        "required_generated_widgets",
        "required_widget_defs",
        "required_app_defs",
    ):
        count += len(evaluation.get(key, []))
    runtime = evaluation.get("runtime_checks")
    if runtime:
        count += len(runtime.get("datasets", []))
    return count


def _baseline_dashboard_specs(payload: JsonDict) -> list[JsonDict]:
    baseline_path = REPO / "src/workspace_bench/data/initial_states/stark_workspace_a.json"
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))["initial_state"]
    dashboards = copy.deepcopy(baseline["dashboards"])
    initial = payload["setup"].get("initial_state", {})
    if isinstance(initial.get("dashboard"), dict):
        dashboards.append(initial["dashboard"])
    if isinstance(initial.get("dashboards"), list):
        dashboards.extend(item for item in initial["dashboards"] if isinstance(item, dict))
    return dashboards


def _selected_dashboard_specs(payload: JsonDict) -> list[JsonDict]:
    dashboards = _baseline_dashboard_specs(payload)
    selected = payload["setup"]["default_selected_dashboard"]
    return [item for item in dashboards if item.get("name") == selected]


def _stages_target(payload: JsonDict, target: TargetSpec) -> bool:
    return any(
        widget.get("origin") == target.origin and widget.get("widget_id") == target.widget_id
        for dashboard in _selected_dashboard_specs(payload)
        for widget in dashboard.get("widgets", [])
    )


def _assert_f1_f3(records: list[TaskRecord], catalogs: dict[str, JsonDict]) -> None:
    """Assert F1-F3: contracts, value provenance, and pinned widget args."""

    for record in records:
        payload = record.payload
        task_id = str(payload["id"])
        prompt = str(payload["prompt"])
        for policy in record.policies:
            if policy.words.casefold() not in prompt.casefold():
                raise AssertionError(
                    f"{task_id}: policy words {policy.words!r} are absent from prompt"
                )
        for call in payload["eval"]["required_tools"]:
            contract = _synthesized_contract(call)
            if contract is None:
                continue
            existence_only_delegation = (
                call["tool"] == "assign_tasks_to_agents"
                and call.get("graded_args") == []
                and contract == {}
            )
            if _contains_forbidden_empty(contract) and not existence_only_delegation:
                raise AssertionError(
                    f"{task_id}: F1 empty value in {call['tool']} contract {contract!r}"
                )
            defaults: dict[str, Any] = {}
            args = call["args"]
            origin = args.get("origin")
            widget_id = args.get("widget_id")
            if origin in ORIGIN_SLUGS and isinstance(widget_id, str):
                definition = catalogs[ORIGIN_SLUGS[str(origin)]]["widgets"].get(widget_id, {})
                if isinstance(definition, dict):
                    defaults = _param_defaults(definition)
            for path, value in _walk_leaves(contract):
                default = ...
                if len(path) >= 2 and path[0] == "data_args":
                    default = defaults.get(path[1], ...)
                if path and path[0] == "widget_id" and isinstance(value, str):
                    # A graded widget_id is a handle, readable from the
                    # workspace: fair whenever the prompt states the widget's
                    # display name (discovery resolves name -> id).
                    definition = {}
                    if origin in ORIGIN_SLUGS:
                        definition = catalogs[ORIGIN_SLUGS[str(origin)]]["widgets"].get(value, {})
                    display = definition.get("name") if isinstance(definition, dict) else None
                    if isinstance(display, str) and display.casefold() in prompt.casefold():
                        continue
                    # Authored widgets (level5): the id derives from a
                    # prompt-stated name via the stated snake_case convention.
                    convention_name = value.replace("_", " ")
                    if convention_name.casefold() in prompt.casefold():
                        continue
                if not _value_has_provenance(
                    value,
                    prompt=prompt,
                    policies=record.policies,
                    default=default,
                ):
                    raise AssertionError(
                        f"{task_id}: F2 ungrounded graded value {value!r} "
                        f"at {call['tool']}:{'.'.join(path)}"
                    )

        # F2 covers authored-definition expectations too: any graded expect
        # field value (e.g. the widget type) must be stated in the prompt.
        for widget_def in payload["eval"].get("required_widget_defs", []):
            for field_name, expected in (widget_def.get("expect") or {}).items():
                if isinstance(expected, str) and expected.casefold() not in prompt.casefold():
                    raise AssertionError(
                        f"{task_id}: F2 unstated expect value {expected!r} for "
                        f"{widget_def.get('widget_id')}.{field_name}"
                    )

        for required in payload["eval"].get("required_widgets", []):
            data_args = required.get("data_args")
            key = (str(required["origin"]), str(required["widget_id"]))
            if data_args is None:
                if key in record.pinned_widget_args:
                    raise AssertionError(
                        f"{task_id}: pinned arg metadata exists without required data_args"
                    )
                continue
            if not isinstance(data_args, dict) or not data_args:
                raise AssertionError(f"{task_id}: F3 empty required-widget data_args")
            expected_keys = record.pinned_widget_args.get(key)
            if expected_keys != frozenset(data_args):
                raise AssertionError(
                    f"{task_id}: F3 keys {sorted(data_args)} != pinned {expected_keys}"
                )
            for path, value in _walk_leaves(data_args):
                if not _value_has_provenance(
                    value,
                    prompt=prompt,
                    policies=record.policies,
                ):
                    raise AssertionError(
                        f"{task_id}: F2 ungrounded required-widget value "
                        f"{value!r} at {'.'.join(path)}"
                    )


def _assert_f4(records: list[TaskRecord]) -> None:
    """Assert F4's exact-origin/display or selected-stage rule for level0."""

    for record in records:
        if record.payload["difficulty"] != "level0":
            continue
        prompt = str(record.payload["prompt"])
        for target in record.targets:
            explicit = target.origin in prompt and target.display_name in prompt
            staged = target.staged and _stages_target(record.payload, target)
            if not (explicit or staged):
                raise AssertionError(
                    f"{record.payload['id']}: F4 target {target.display_name!r} "
                    "is neither explicit nor revealed by selected staging"
                )


def _snake_case(value: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", value.casefold())).strip("_")


def _assert_f5(records: list[TaskRecord]) -> None:
    """Assert explicit naming conventions and convention-derived authored ids."""

    convention = (
        "widget ids are the snake_case of widget names; tab ids are the snake_case of tab names"
    )
    for record in records:
        level = str(record.payload["difficulty"])
        is_authoring_top = level == "level5" or (
            record.family == "extend" and level in {"level4", "level5"}
        )
        if not is_authoring_top:
            continue
        evaluation = record.payload["eval"]
        if not (evaluation.get("required_widget_defs") or evaluation.get("required_app_defs")):
            continue
        prompt = str(record.payload["prompt"])
        if convention not in prompt.casefold():
            raise AssertionError(f"{record.payload['id']}: F5 convention absent")
        target_by_key = {(target.origin, target.widget_id): target for target in record.targets}
        for definition in evaluation.get("required_widget_defs", []):
            key = (definition["backend_name"], definition["widget_id"])
            target = target_by_key.get(key)
            if target is None:
                raise AssertionError(f"{record.payload['id']}: F5 target missing for {key}")
            if target.display_name not in prompt:
                raise AssertionError(
                    f"{record.payload['id']}: F5 prompt omits {target.display_name!r}"
                )
            if definition["widget_id"] != _snake_case(target.display_name):
                raise AssertionError(f"{record.payload['id']}: F5 widget id violates snake_case")
        for app in evaluation.get("required_app_defs", []):
            for tab_id in app.get("tabs_include", []):
                tab_name = str(tab_id).replace("_", " ").title()
                if tab_name.casefold() not in prompt.casefold():
                    raise AssertionError(
                        f"{record.payload['id']}: F5 prompt omits tab name {tab_name!r}"
                    )
                if tab_id != _snake_case(tab_name):
                    raise AssertionError(f"{record.payload['id']}: F5 tab id violates snake_case")


def _assert_f6_f7(records: list[TaskRecord]) -> dict[str, int]:
    """Assert F6 budgets/orientation/discovery and F7 semantic caps."""

    counts: dict[str, int] = {}
    for record in records:
        payload = record.payload
        task_id = str(payload["id"])
        tools = payload["eval"]["required_tools"]
        if payload["eval"]["max_turns"] != len(tools) + 3:
            raise AssertionError(f"{task_id}: F6 turn budget mismatch")
        if payload["difficulty"] in {"level0", "level1"}:
            first = tools[0] if tools else {}
            if first.get("tool") != "get_workspace_snapshot" or not first.get("optional"):
                raise AssertionError(f"{task_id}: F6 orientation step is not first/optional")
        for call in tools:
            is_discovery = call.get("tool") in DISCOVERY_TOOLS or (
                call.get("tool") in {"manage_backends", "manage_apps"}
                and call.get("args", {}).get("operation") in {"list", "read"}
            )
            if is_discovery and not call.get("optional"):
                raise AssertionError(f"{task_id}: F6 discovery call {call['tool']} is graded")
        count = _semantic_check_count(payload)
        counts[task_id] = count
        cap = LEVEL_CAPS[str(payload["difficulty"])]
        if count > cap:
            raise AssertionError(f"{task_id}: F7 {count} graded checks exceed {cap}")
    return counts


def _catalog_rows(definition: JsonDict) -> Any:
    for key in ("sampleDataByArgs", "sampleData", "data"):
        if key in definition:
            return definition[key]
    return None


def _assert_f8(records: list[TaskRecord], catalogs: dict[str, JsonDict]) -> None:
    """Assert answer and handoff facts are literal catalog-row values."""

    for record in records:
        evaluation = record.payload["eval"]
        values = evaluation.get("required_values_in_answer", [])
        if values:
            if not 2 <= len(values) <= 3:
                raise AssertionError(f"{record.payload['id']}: F8 needs 2-3 answer tokens")
            if record.answer_source is None:
                raise AssertionError(f"{record.payload['id']}: F8 answer source absent")
            source_slug, widget_id = record.answer_source
            rows = _catalog_rows(catalogs[source_slug]["widgets"][widget_id])
            row_text = json.dumps(rows, ensure_ascii=False)
            reference = str(evaluation.get("reference_answer", ""))
            for token in values:
                if token not in row_text:
                    raise AssertionError(
                        f"{record.payload['id']}: F8 token {token!r} absent from rows"
                    )
                if token not in reference:
                    raise AssertionError(
                        f"{record.payload['id']}: F8 token {token!r} absent from answer"
                    )
        for grounded in record.grounded_generated:
            rows = _catalog_rows(catalogs[grounded.backend_slug]["widgets"][grounded.widget_id])
            row_text = json.dumps(rows, ensure_ascii=False)
            for token in grounded.tokens:
                if token not in row_text:
                    raise AssertionError(
                        f"{record.payload['id']}: handoff fact {token!r} is not served"
                    )
            generated_tokens = {
                token
                for item in evaluation.get("required_generated_widgets", [])
                for token in item.get("data_contains", [])
            }
            if not set(grounded.tokens).issubset(generated_tokens):
                raise AssertionError(
                    f"{record.payload['id']}: grounded handoff facts are not pinned"
                )


def _assert_target_coverage(record: TaskRecord) -> None:
    targets = {(target.origin, target.widget_id) for target in record.targets}
    target_ids = {target.widget_id for target in record.targets}
    evaluation = record.payload["eval"]
    for required in evaluation.get("required_widgets", []):
        key = (required["origin"], required["widget_id"])
        if key not in targets:
            raise AssertionError(f"{record.payload['id']}: F9 untracked required target {key}")
    for definition in evaluation.get("required_widget_defs", []):
        key = (definition["backend_name"], definition["widget_id"])
        if key not in targets:
            raise AssertionError(f"{record.payload['id']}: F9 untracked authored target {key}")
    for call in evaluation["required_tools"]:
        args = call.get("args", {})
        widget_id = args.get("widget_id")
        origin = args.get("origin")
        if isinstance(widget_id, str) and origin is not None:
            if (origin, widget_id) not in targets:
                raise AssertionError(
                    f"{record.payload['id']}: F9 untracked call target {(origin, widget_id)}"
                )
        elif isinstance(widget_id, str) and call.get("tool") in {
            "update_widget",
            "update_widget_layout",
            "read_widget",
        }:
            if widget_id not in target_ids:
                raise AssertionError(
                    f"{record.payload['id']}: F9 untracked staged target {widget_id}"
                )


def _assert_f9(records: list[TaskRecord], catalogs: dict[str, JsonDict]) -> None:
    """Assert every prompt target is uniquely discriminated across four catalogs."""

    catalog_ids = {widget_id for catalog in catalogs.values() for widget_id in catalog["widgets"]}
    for record in records:
        _assert_target_coverage(record)
        prompt = str(record.payload["prompt"])
        for target in record.targets:
            if target.staged:
                if not _stages_target(record.payload, target):
                    raise AssertionError(
                        f"{record.payload['id']}: staged F9 target is not snapshot-visible"
                    )
                continue
            for token in target.discriminators:
                if token.casefold() not in prompt.casefold():
                    raise AssertionError(f"{record.payload['id']}: F9 prompt omits {token!r}")
            if target.custom:
                if target.origin in BACKEND_ORIGINS.values():
                    raise AssertionError(
                        f"{record.payload['id']}: custom origin collides with catalog"
                    )
                if target.widget_id in catalog_ids:
                    raise AssertionError(
                        f"{record.payload['id']}: custom widget id collides with catalog"
                    )
                continue
            candidates: list[tuple[str, str]] = []
            for slug, catalog in catalogs.items():
                for widget_id, definition in catalog["widgets"].items():
                    document = " ".join(
                        [widget_id, BACKEND_ORIGINS[slug], *_walk_values(definition)]
                    ).casefold()
                    if all(token.casefold() in document for token in target.discriminators):
                        candidates.append((BACKEND_ORIGINS[slug], widget_id))
            expected = (target.origin, target.widget_id)
            if candidates != [expected]:
                raise AssertionError(
                    f"{record.payload['id']}: F9 target {expected} matches {candidates}"
                )


def _assert_f10(records: list[TaskRecord]) -> None:
    """Assert concise business prompts with unique opening five-grams."""

    openings: set[tuple[str, ...]] = set()
    for record in records:
        task_id = str(record.payload["id"])
        prompt = str(record.payload["prompt"])
        if len(prompt.split()) > 110:
            raise AssertionError(f"{task_id}: F10 prompt exceeds 110 words")
        opening = tuple(prompt.casefold().split()[:5])
        if opening in openings:
            raise AssertionError(f"{task_id}: F10 duplicate opening five-gram {opening}")
        openings.add(opening)
        lowered = prompt.casefold()
        forbidden = sorted(term for term in PROMPT_FORBIDDEN if term in lowered)
        if forbidden:
            raise AssertionError(f"{task_id}: F10 prompt contains implementation terms {forbidden}")


def _assert_f11(records: list[TaskRecord]) -> None:
    """Require discovery before opaque reads of unmounted catalog widgets."""

    for record in records:
        task_id = str(record.payload["id"])
        if task_id.rsplit("_level", 1)[0] not in WAVE3_SPINES:
            # Pre-wave-3 records are certified immutable content. F11 guards
            # every mutable ladder that can introduce this defect again.
            continue
        prompt = str(record.payload["prompt"])
        tools = record.payload["eval"]["required_tools"]
        targets = {(target.origin, target.widget_id): target for target in record.targets}
        mounted = {
            (str(widget.get("origin")), str(widget.get("widget_id")))
            for dashboard in _baseline_dashboard_specs(record.payload)
            for widget in dashboard.get("widgets", [])
            if widget.get("origin") is not None and widget.get("widget_id") is not None
        }
        for index, call in enumerate(tools):
            if call["tool"] != "get_widget_data" or call.get("optional"):
                continue
            args = call.get("args", {})
            key = (str(args.get("origin")), str(args.get("widget_id")))
            target = targets.get(key)
            if target is None or target.origin not in ORIGIN_SLUGS or key in mounted:
                continue
            if target.display_name.casefold() not in prompt.casefold():
                continue
            if target.widget_id == _snake_case(target.display_name):
                continue
            discovered = any(
                prior["tool"] == "list_available_widgets"
                and prior.get("args", {}).get("origin") == target.origin
                for prior in tools[:index]
            )
            if not discovered:
                raise AssertionError(f"F11 unmounted read without discovery: {task_id}")


def _assert_f12(records: list[TaskRecord]) -> None:
    """Forbid prompts from printing read-derived graded tokens (wave-3 scope)."""

    for record in records:
        task_id = str(record.payload["id"])
        if task_id.rsplit("_level", 1)[0] not in WAVE3_SPINES:
            # Pre-wave-3 records are certified immutable content.
            continue
        evaluation = record.payload["eval"]
        if not any(
            call["tool"] == "get_widget_data" for call in evaluation["required_tools"]
        ):
            continue
        prompt = str(record.payload["prompt"]).casefold()
        exempt: set[str] = set()
        for call in evaluation["required_tools"]:
            data_args = call.get("args", {}).get("data_args")
            if isinstance(data_args, dict):
                exempt.update(str(value).casefold() for value in data_args.values())
        for required in evaluation.get("required_widgets", []):
            if isinstance(required.get("data_args"), dict):
                exempt.update(
                    str(value).casefold() for value in required["data_args"].values()
                )
        tokens = {str(token) for token in evaluation.get("required_values_in_answer", [])}
        for grounded in record.grounded_generated:
            tokens.update(str(token) for token in grounded.tokens)
        for token in sorted(tokens):
            token_cf = token.casefold()
            if token_cf in exempt:
                continue
            if token_cf in prompt:
                raise AssertionError(
                    f"F12 prompt prints read-derived token: {task_id}: {token!r}"
                )


def _assert_l1_l5(records: list[TaskRecord]) -> None:
    """Assert the wave-2 learned rules across both waves."""

    for record in records:
        payload = record.payload
        task_id = str(payload["id"])
        prompt = str(payload["prompt"])
        evaluation = payload["eval"]
        for call in evaluation["required_tools"]:
            if call["tool"] == "get_widget_data" and not call.get("optional"):
                if set(call.get("graded_args", [])) != {"origin", "widget_id"}:
                    raise AssertionError(f"{task_id}: L1 read does not grade origin/widget_id")
                if "data_args" in call.get("graded_args", []):
                    raise AssertionError(f"{task_id}: L1 read grades data_args echo")
                if record.family == "retrieve" and not evaluation.get("required_values_in_answer"):
                    raise AssertionError(f"{task_id}: L1 retrieval lacks answer values")
                if record.family == "handoff" and not any(
                    item.get("data_contains")
                    for item in evaluation.get("required_generated_widgets", [])
                ):
                    raise AssertionError(f"{task_id}: L1 handoff lacks pinned note data")

            if payload["difficulty"] == "level0" and not call.get("optional"):
                contract = _synthesized_contract(call) or {}
                data_args = contract.get("data_args")
                if isinstance(data_args, dict):
                    for key in data_args:
                        if f"{key} set to" not in prompt.casefold():
                            raise AssertionError(
                                f"{task_id}: L2 level0 prompt omits parameter key {key!r}"
                            )

        selected = str(payload["setup"]["default_selected_dashboard"])
        if selected != "Home" and f"open {selected} board".casefold() not in prompt.casefold():
            raise AssertionError(
                f"{task_id}: L3 staged prompt does not say 'open {selected} board'"
            )
        if any(term in prompt.casefold() for term in ("explicit", "checkpoint")):
            raise AssertionError(f"{task_id}: L4 scaffolding register remains")


def _assert_wave2_requirements(records: list[TaskRecord]) -> None:
    """Assert wave identity, catalog balance, diversity, and designed selections."""

    by_spine: dict[str, list[TaskRecord]] = defaultdict(list)
    for record in records:
        spine = str(record.payload["id"]).rsplit("_level", 1)[0]
        by_spine[spine].append(record)
    if set(by_spine) != WAVE1_SPINES | WAVE2_SPINES | WAVE3_SPINES:
        raise AssertionError(f"spine set mismatch: {sorted(by_spine)}")

    wave1_catalog_targets = {
        (target.origin, target.widget_id)
        for spine in WAVE1_SPINES
        for record in by_spine[spine]
        for target in record.targets
        if target.origin in ORIGIN_SLUGS
    }
    wave2_catalog_targets = {
        (target.origin, target.widget_id)
        for spine in WAVE2_SPINES
        for record in by_spine[spine]
        for target in record.targets
        if target.origin in ORIGIN_SLUGS
    }
    reused = wave1_catalog_targets & wave2_catalog_targets
    if reused:
        raise AssertionError(f"wave2 reuses wave1 catalog targets: {sorted(reused)}")

    primary_catalog = {
        "closing_tape_lookup": DALOOPA,
        "market_telemetry": GETTING_STARTED,
        "crypto_document_controls": WIDGET_EXAMPLES,
        "manufacturer_details_repair": GETTING_STARTED,
        "cited_research_operations": DALOOPA,
        "news_desk_handoff": GETTING_STARTED,
    }
    shifted = sum(
        origin in {GETTING_STARTED, WIDGET_EXAMPLES} for origin in primary_catalog.values()
    )
    if shifted < 3:
        raise AssertionError(f"wave2 catalog-shift quota missed: {shifted}")

    daloopa_spine = by_spine["cited_research_operations"]
    if not all(
        any(target.origin == DALOOPA for target in record.targets)
        or record.payload["difficulty"] in {"level0", "level5"}
        for record in daloopa_spine
    ) or not all(
        any(
            call["tool"] == "get_skill_content" for call in record.payload["eval"]["required_tools"]
        )
        for record in daloopa_spine
    ):
        raise AssertionError("wave2 Daloopa spine does not lean on Daloopa plus skills")

    capability_phrases = {
        "market_telemetry": "live-updating grid",
        "crypto_document_controls": "whitepaper pdf",
    }
    for spine, phrase in capability_phrases.items():
        if not any(
            phrase in str(record.payload["prompt"]).casefold() for record in by_spine[spine]
        ):
            raise AssertionError(f"{spine}: capability-driven selection prompt missing")

    collisions = [
        (record, target)
        for record in records
        for target in record.targets
        if target.display_name == "Live Grid" and target.widget_id == LIVE_GRID_WIDGET
    ]
    if len(collisions) != 1:
        raise AssertionError(f"expected one Live Grid collision test, got {len(collisions)}")
    collision_record, collision_target = collisions[0]
    collision_prompt = str(collision_record.payload["prompt"])
    if (
        collision_target.widget_id != LIVE_GRID_WIDGET
        or "real-time WebSocket updates" not in collision_prompt
        or "Live Grid" in collision_prompt
    ):
        raise AssertionError("Live Grid collision is not disambiguated by property alone")


def _graded_catalog_targets(records: list[TaskRecord]) -> dict[str, set[str]]:
    graded: dict[str, set[str]] = {origin: set() for origin in ORIGIN_SLUGS}
    for record in records:
        for required in record.payload["eval"].get("required_widgets", []):
            origin = str(required["origin"])
            if origin in graded:
                graded[origin].add(str(required["widget_id"]))
        for call in record.payload["eval"]["required_tools"]:
            if call.get("optional"):
                continue
            args = call.get("args", {})
            origin = args.get("origin")
            widget_id = args.get("widget_id")
            if origin in graded and isinstance(widget_id, str):
                graded[str(origin)].add(widget_id)
    return graded


def _catalog_app_index(catalog: JsonDict) -> dict[str, str]:
    index: dict[str, str] = {}
    for app in catalog.get("apps", []):
        if not isinstance(app, dict):
            continue
        app_name = str(app.get("name", ""))
        for tab in app.get("tabs", {}).values():
            for item in tab.get("layout", []):
                widget_id = item.get("i")
                if isinstance(widget_id, str):
                    index[widget_id] = app_name
    return index


def _governance_content(spec: GovernanceSpec) -> str:
    if spec.tool == "get_skill_content":
        return str(WORKSPACE_SKILLS[spec.key]["content"])
    if spec.tool == "read_workspace_resource":
        return str(LIVE_WORKSPACE_RESOURCES[spec.key])
    if spec.tool == "get_workspace_prompt":
        return str(WORKSPACE_PROMPTS[spec.key])
    raise AssertionError(f"unsupported governance tool {spec.tool}")


def _assert_instantiation_and_expect_fairness(records: list[TaskRecord]) -> None:
    for record in records:
        evaluation = record.payload["eval"]
        authored_targets = {
            (target.origin, target.widget_id) for target in record.targets if target.custom
        }
        required_pairs = {
            (str(required["origin"]), str(required["widget_id"]))
            for required in evaluation.get("required_widgets", [])
        }
        for call in evaluation["required_tools"]:
            if (
                call["tool"] == "manage_apps"
                and call["args"].get("operation") == "instantiate"
                and not call.get("optional")
            ):
                if call.get("graded_args") != ["operation"]:
                    raise AssertionError(
                        f"{record.payload['id']}: instantiate must grade operation only"
                    )
                if not authored_targets & required_pairs:
                    raise AssertionError(
                        f"{record.payload['id']}: instantiate lacks authored-widget state check"
                    )
            if call["tool"] == "assign_tasks_to_agents" and not call.get("optional"):
                if call.get("graded_args") != []:
                    raise AssertionError(
                        f"{record.payload['id']}: delegation must grade that delegation happened"
                    )
        for required in evaluation.get("required_widget_defs", []):
            forbidden = {"endpoint", "description"} & set(required.get("expect", {}))
            if forbidden:
                raise AssertionError(
                    f"{record.payload['id']}: forbidden authored definition pins {sorted(forbidden)}"
                )


def _assert_wave3_requirements(
    records: list[TaskRecord],
    catalogs: dict[str, JsonDict],
) -> None:
    by_spine: dict[str, list[TaskRecord]] = defaultdict(list)
    for record in records:
        by_spine[str(record.payload["id"]).rsplit("_level", 1)[0]].append(record)
    if set(by_spine) != WAVE1_SPINES | WAVE2_SPINES | WAVE3_SPINES:
        raise AssertionError(f"wave3 spine set mismatch: {sorted(by_spine)}")

    if set(WAVE3_SPINE_FAMILIES) != WAVE3_SPINES:
        raise AssertionError("wave3 family metadata is incomplete")
    if len(set(WAVE3_BUSINESS_THEMES.values())) != len(WAVE3_SPINES):
        raise AssertionError("wave3 business themes are not unique")
    if set(WAVE3_BUSINESS_THEMES.values()) & LEGACY_BUSINESS_THEMES:
        raise AssertionError("wave3 reuses a legacy business theme")
    for spine in WAVE3_SPINES:
        spine_records = by_spine[spine]
        levels = {str(record.payload["difficulty"]) for record in spine_records}
        if levels != set(LEVEL_CAPS) or len(spine_records) != 6:
            raise AssertionError(f"{spine}: incomplete six-level wave3 ladder")
        if {record.family for record in spine_records} != {WAVE3_SPINE_FAMILIES[spine]}:
            raise AssertionError(f"{spine}: wrong family")

    legacy_catalog_targets = {
        (target.origin, target.widget_id)
        for spine in WAVE1_SPINES | WAVE2_SPINES
        for record in by_spine[spine]
        for target in record.targets
        if target.origin in ORIGIN_SLUGS
    }
    seen_wave3: dict[tuple[str, str], str] = {}
    for spine in WAVE3_SPINES:
        spine_targets = {
            (target.origin, target.widget_id)
            for record in by_spine[spine]
            for target in record.targets
            if target.origin in ORIGIN_SLUGS
        }
        reused_legacy = spine_targets & legacy_catalog_targets
        if reused_legacy:
            raise AssertionError(f"{spine}: reuses legacy targets {sorted(reused_legacy)}")
        for target_key in spine_targets:
            prior = seen_wave3.get(target_key)
            if prior is not None and prior != spine:
                raise AssertionError(f"{spine}: reuses {target_key} from wave3 spine {prior}")
            seen_wave3[target_key] = spine

    knowledge_tools = {
        "get_skill_content",
        "read_workspace_resource",
        "get_workspace_prompt",
    }
    for spine in WAVE3_SPINES:
        level4 = next(
            record for record in by_spine[spine] if record.payload["difficulty"] == "level4"
        )
        spec = level4.governance
        if spec is None:
            raise AssertionError(f"{level4.payload['id']}: level4 governance metadata missing")
        prompt = str(level4.payload["prompt"])
        if spec.label.casefold() not in prompt.casefold():
            raise AssertionError(f"{level4.payload['id']}: named governance absent from prompt")
        key_name = {
            "get_skill_content": "slug",
            "read_workspace_resource": "uri",
            "get_workspace_prompt": "name",
        }[spec.tool]
        graded_calls = [
            call for call in level4.payload["eval"]["required_tools"] if not call.get("optional")
        ]
        if not any(
            call["tool"] == spec.tool and call["args"].get(key_name) == spec.key
            for call in graded_calls
        ):
            raise AssertionError(f"{level4.payload['id']}: governance read is not graded")
        if not any(call["tool"] not in knowledge_tools for call in graded_calls):
            raise AssertionError(f"{level4.payload['id']}: governance has no graded outcome")
        content = _governance_content(spec)
        catalog_documents = []
        for target_spec in level4.targets:
            if target_spec.origin not in ORIGIN_SLUGS:
                continue
            definition = catalogs[ORIGIN_SLUGS[target_spec.origin]]["widgets"][
                target_spec.widget_id
            ]
            catalog_documents.append(definition)
        outcome_document = json.dumps(
            {
                "evaluation": level4.payload["eval"],
                "targets": [
                    {
                        "origin": target_spec.origin,
                        "widget_id": target_spec.widget_id,
                        "display_name": target_spec.display_name,
                    }
                    for target_spec in level4.targets
                ],
                "catalog_definitions": catalog_documents,
            },
            ensure_ascii=False,
        )
        for token in spec.outcome_tokens:
            if token.casefold() not in content.casefold():
                raise AssertionError(
                    f"{level4.payload['id']}: governed token {token!r} absent from source"
                )
            if token.casefold() not in outcome_document.casefold():
                raise AssertionError(
                    f"{level4.payload['id']}: governed token {token!r} absent from outcome"
                )

    used_skills = {
        str(call["args"]["slug"])
        for record in records
        for call in record.payload["eval"]["required_tools"]
        if call["tool"] == "get_skill_content" and not call.get("optional")
    }
    if used_skills != set(SKILL_SLUGS):
        raise AssertionError(f"skill coverage mismatch: {sorted(used_skills)}")
    legacy_used_skills = {
        str(call["args"]["slug"])
        for spine in WAVE1_SPINES | WAVE2_SPINES
        for record in by_spine[spine]
        for call in record.payload["eval"]["required_tools"]
        if call["tool"] == "get_skill_content" and not call.get("optional")
    }
    newly_used_skills = set(SKILL_SLUGS) - legacy_used_skills
    for spine in ("comps_governance", "investment_snapshot_governance"):
        spine_skills = {
            str(call["args"]["slug"])
            for record in by_spine[spine]
            for call in record.payload["eval"]["required_tools"]
            if call["tool"] == "get_skill_content" and not call.get("optional")
        }
        if not spine_skills or not spine_skills <= newly_used_skills:
            raise AssertionError(f"{spine}: platform spine is not governed by a new skill")

    legacy_records = [record for spine in WAVE1_SPINES | WAVE2_SPINES for record in by_spine[spine]]
    wave3_records = [record for spine in WAVE3_SPINES for record in by_spine[spine]]
    legacy_coverage = _graded_catalog_targets(legacy_records)
    wave3_coverage = _graded_catalog_targets(wave3_records)
    whole_coverage = _graded_catalog_targets(records)
    expected_legacy = {
        GETTING_STARTED: 7,
        WIDGET_EXAMPLES: 3,
        STARK: 3,
        DALOOPA: 4,
    }
    if {origin: len(ids) for origin, ids in legacy_coverage.items()} != expected_legacy:
        raise AssertionError("pre-wave3 coverage baseline changed")
    delta_floors = {
        GETTING_STARTED: 12,
        WIDGET_EXAMPLES: 8,
        STARK: 6,
        DALOOPA: 2,
    }
    for origin, floor in delta_floors.items():
        new_ids = wave3_coverage[origin] - legacy_coverage[origin]
        if len(new_ids) < floor:
            raise AssertionError(f"{origin}: wave3 graded coverage {len(new_ids)} is below {floor}")
        if len(whole_coverage[origin]) < expected_legacy[origin] + floor:
            raise AssertionError(f"{origin}: whole-suite coverage floor missed")

    new_definitions = [
        catalogs[ORIGIN_SLUGS[origin]]["widgets"][widget_id]
        for origin, widget_ids in wave3_coverage.items()
        for widget_id in widget_ids - legacy_coverage[origin]
    ]
    new_types = {str(definition.get("type", "")) for definition in new_definitions}
    if "live_grid" not in new_types:
        raise AssertionError("wave3 does not operate a live grid")
    if not any(widget_type.startswith("chart") for widget_type in new_types):
        raise AssertionError("wave3 does not operate a chart")
    if not new_types & {"pdf", "youtube", "iframe", "newsfeed", "multi_file_viewer"}:
        raise AssertionError("wave3 does not operate a media/content widget")

    def contains_form_param(value: Any) -> bool:
        if isinstance(value, dict):
            return value.get("type") == "form" or any(
                contains_form_param(item) for item in value.values()
            )
        if isinstance(value, list):
            return any(contains_form_param(item) for item in value)
        return False

    form_targets = {
        (origin, widget_id)
        for origin, widget_ids in wave3_coverage.items()
        for widget_id in widget_ids - legacy_coverage[origin]
        if contains_form_param(
            catalogs[ORIGIN_SLUGS[origin]]["widgets"][widget_id].get("params", [])
        )
    }
    form_operated = False
    for record in wave3_records:
        required_pairs = {
            (str(item["origin"]), str(item["widget_id"]))
            for item in record.payload["eval"].get("required_widgets", [])
        }
        if not form_targets & required_pairs:
            continue
        form_operated = form_operated or any(
            call["tool"] == "update_widget"
            and call["args"].get("data_args", {}).get("add_record") is True
            and {
                "client_first_name",
                "client_last_name",
            }.issubset(call["args"].get("data_args", {}))
            for call in record.payload["eval"]["required_tools"]
            if not call.get("optional")
        )
    if not form_operated:
        raise AssertionError("wave3 form target lacks graded inputs plus submit")

    stark_catalog = catalogs[ORIGIN_SLUGS[STARK]]
    stark_app_index = _catalog_app_index(stark_catalog)
    legacy_stark_apps = {
        stark_app_index[widget_id]
        for widget_id in legacy_coverage[STARK]
        if widget_id in stark_app_index
    }
    new_stark_ids = wave3_coverage[STARK] - legacy_coverage[STARK]
    new_stark_apps = {
        stark_app_index[widget_id] for widget_id in new_stark_ids if widget_id in stark_app_index
    }
    if len(new_stark_ids) < 6 or not 2 <= len(new_stark_apps) <= 3:
        raise AssertionError(
            f"wave3 Stark sweep has {len(new_stark_ids)} widgets across {len(new_stark_apps)} apps"
        )
    if new_stark_apps & legacy_stark_apps:
        raise AssertionError("wave3 Stark sweep reuses an app touched by earlier waves")


def _assert_wave3_repairs(records: list[TaskRecord]) -> dict[str, int]:
    """Certify the five live-run repairs and return their report counts."""

    wave3_records = [
        record
        for record in records
        if str(record.payload["id"]).rsplit("_level", 1)[0] in WAVE3_SPINES
    ]
    spec_uri = "openbb://workspace/specs/widgets-json"

    d1_refs: set[str] = set()
    for record in wave3_records:
        task_id = str(record.payload["id"])
        for call in record.payload["eval"]["required_tools"]:
            if (
                call["tool"] == "read_workspace_resource"
                and call.get("args", {}).get("uri") == spec_uri
            ):
                if not call.get("optional"):
                    raise AssertionError(f"{task_id}: D1 widgets spec read is required")
                if record.payload["difficulty"] == "level5":
                    d1_refs.add(task_id)
    if len(d1_refs) != 4:
        raise AssertionError(f"D1 expected 4 repaired sites, got {sorted(d1_refs)}")

    d2_refs: set[str] = set()
    for record in wave3_records:
        task_id = str(record.payload["id"])
        tools = record.payload["eval"]["required_tools"]
        for index, call in enumerate(tools):
            args = call.get("args", {})
            origin = args.get("origin")
            if call["tool"] != "get_widget_data" or origin not in ORIGIN_SLUGS:
                continue
            if not any(
                prior["tool"] == "list_available_widgets"
                and prior.get("optional")
                and prior.get("args", {}).get("origin") == origin
                for prior in tools[:index]
            ):
                raise AssertionError(f"{task_id}: D2 catalog read lacks prior discovery")
            if not call.get("optional") and record.payload["difficulty"] != "level1":
                d2_refs.add(task_id)
    if len(d2_refs) != 16:
        raise AssertionError(f"D2 expected 16 added discovery refs, got {sorted(d2_refs)}")

    d3_refs: set[str] = set()
    for record in wave3_records:
        if record.family != "extend" or record.payload["difficulty"] not in {
            "level0",
            "level1",
        }:
            continue
        task_id = str(record.payload["id"])
        tools = record.payload["eval"]["required_tools"]
        spec_indexes = [
            index
            for index, call in enumerate(tools)
            if call["tool"] == "read_workspace_resource"
            and call.get("args", {}).get("uri") == spec_uri
            and call.get("optional")
        ]
        backend_index = next(
            index for index, call in enumerate(tools) if call["tool"] == "manage_backends"
        )
        if len(spec_indexes) != 1 or spec_indexes[0] >= backend_index:
            raise AssertionError(f"{task_id}: D3 spec consultation is missing or misplaced")
        d3_refs.add(task_id)
    if len(d3_refs) != 4:
        raise AssertionError(f"D3 expected 4 extend refs, got {sorted(d3_refs)}")

    d4_tasks: set[str] = set()
    for record in wave3_records:
        if record.family != "retrieve" or record.payload["difficulty"] != "level5":
            continue
        task_id = str(record.payload["id"])
        datasets = record.payload["eval"].get("runtime_checks", {}).get("datasets", [])
        if len(datasets) != 1:
            raise AssertionError(f"{task_id}: D4 expected one runtime dataset")
        dataset = datasets[0]
        fields = dataset.get("fields", [])
        rows = dataset.get("payload", [])
        prompt = str(record.payload["prompt"])
        required_values = set(record.payload["eval"].get("required_values_in_answer", []))
        if (
            len(fields) != 2
            or any(str(field).casefold() not in prompt.casefold() for field in fields)
            or len(rows) != 1
            or set(rows[0]) != set(fields)
            or {str(value) for value in rows[0].values()} != required_values
            or {"reported_first", "reported_second"} & set(fields)
        ):
            raise AssertionError(f"{task_id}: D4 served columns are not fully stated")
        d4_tasks.add(task_id)
    if len(d4_tasks) != 2:
        raise AssertionError(f"D4 expected 2 stated-column tasks, got {sorted(d4_tasks)}")

    d5_refs: set[str] = set()
    for record in wave3_records:
        if record.family != "handoff" or record.payload["difficulty"] != "level5":
            continue
        task_id = str(record.payload["id"])
        if len(record.grounded_generated) != 1:
            raise AssertionError(f"{task_id}: D5 grounding metadata is missing")
        grounded = record.grounded_generated[0]
        target = next(
            (
                candidate
                for candidate in record.targets
                if not candidate.custom and candidate.widget_id == grounded.widget_id
            ),
            None,
        )
        if target is None:
            raise AssertionError(f"{task_id}: D5 grounding target is untracked")
        tools = record.payload["eval"]["required_tools"]
        discover_index = next(
            (
                index
                for index, call in enumerate(tools)
                if call["tool"] == "list_available_widgets"
                and call.get("optional")
                and call.get("args", {}).get("origin") == target.origin
            ),
            -1,
        )
        read_index = next(
            (
                index
                for index, call in enumerate(tools)
                if call["tool"] == "get_widget_data"
                and call.get("optional")
                and call.get("args", {}).get("origin") == target.origin
                and call.get("args", {}).get("widget_id") == target.widget_id
            ),
            -1,
        )
        note_index = next(
            index
            for index, call in enumerate(tools)
            if call["tool"] == "add_generative_widget"
        )
        if not 0 <= discover_index < read_index < note_index:
            raise AssertionError(f"{task_id}: D5 grounding reads are missing or misplaced")
        d5_refs.add(task_id)
    if len(d5_refs) != 2:
        raise AssertionError(f"D5 expected 2 grounding refs, got {sorted(d5_refs)}")

    return {
        "d1_optional_spec_reads": len(d1_refs),
        "d2_discovery_refs": len(d2_refs),
        "d3_extend_spec_reads": len(d3_refs),
        "d4_stated_column_tasks": len(d4_tasks),
        "d5_grounding_refs": len(d5_refs),
    }


def _assert_family_missions(records: list[TaskRecord]) -> None:
    by_family: dict[str, list[TaskRecord]] = defaultdict(list)
    for record in records:
        by_family[record.family].append(record)
    if set(by_family) != set(FAMILY_LEVELS):
        raise AssertionError(f"family set mismatch: {sorted(by_family)}")
    for family, expected_levels in FAMILY_LEVELS.items():
        actual_counts: dict[str, int] = defaultdict(int)
        for record in by_family[family]:
            actual_counts[str(record.payload["difficulty"])] += 1
        expected_counts = {level: 4 for level in expected_levels}
        if dict(actual_counts) != expected_counts:
            raise AssertionError(
                f"{family}: level counts {dict(actual_counts)} != {expected_counts}"
            )
        spines = {str(record.payload["id"]).rsplit("_level", 1)[0] for record in by_family[family]}
        if len(spines) != 4:
            raise AssertionError(f"{family}: expected four spines, got {spines}")

    if any(
        len({target.origin for target in record.targets if target.origin in ORIGIN_SLUGS}) < 2
        for record in by_family["curate"]
        if record.payload["difficulty"] in {"level3", "level4", "level5"}
    ):
        raise AssertionError("curate cross-catalog rungs missing")
    if any(
        call["tool"] in {"create_widget", "manage_backends", "manage_apps"}
        for record in by_family["parameterize"]
        for call in record.payload["eval"]["required_tools"]
    ):
        raise AssertionError("parameterize spine creates fresh content")
    if any(not record.payload["setup"].get("initial_state") for record in by_family["repair"]):
        raise AssertionError("repair task missing seeded defect")
    for low in (
        record for record in by_family["repair"] if record.payload["difficulty"] == "level0"
    ):
        graded = [
            call for call in low.payload["eval"]["required_tools"] if not call.get("optional")
        ]
        if [call["tool"] for call in graded] != ["update_widget"]:
            raise AssertionError(f"{low.payload['id']}: repair level0 is not one stated update")
        if len(low.payload["eval"].get("required_widgets", [])) != 1:
            raise AssertionError(f"{low.payload['id']}: repair level0 state check is not singular")
    knowledge_tools = {
        "get_skill_content",
        "read_workspace_resource",
        "get_workspace_prompt",
    }
    if any(
        not any(
            call["tool"] in knowledge_tools and not call.get("optional")
            for call in record.payload["eval"]["required_tools"]
        )
        for record in by_family["platform"]
    ):
        raise AssertionError("platform rung lacks graded knowledge read")
    for low in (
        record for record in by_family["platform"] if record.payload["difficulty"] == "level0"
    ):
        graded = [
            call for call in low.payload["eval"]["required_tools"] if not call.get("optional")
        ]
        knowledge = [call for call in graded if call["tool"] in knowledge_tools]
        follow_ups = [call for call in graded if call["tool"] not in knowledge_tools]
        if len(knowledge) != 1 or len(follow_ups) > 1:
            raise AssertionError(f"{low.payload['id']}: platform level0 is not read-then-act")
        if any(call["tool"] in DISCOVERY_TOOLS for call in graded):
            raise AssertionError(f"{low.payload['id']}: platform level0 grades discovery")
        knowledge_call = knowledge[0]
        if knowledge_call["tool"] == "get_skill_content":
            content = str(WORKSPACE_SKILLS[knowledge_call["args"]["slug"]]["content"])
            pinned = {
                token
                for item in low.payload["eval"].get("required_generated_widgets", [])
                for token in item.get("data_contains", [])
            }
            if not pinned or not all(token.casefold() in content.casefold() for token in pinned):
                raise AssertionError(
                    f"{low.payload['id']}: platform follow-up does not use skill content"
                )
    for record in by_family["extend"]:
        if record.payload["difficulty"] in {"level4", "level5"}:
            targets = [target for target in record.targets if target.custom]
            tools = record.payload["eval"]["required_tools"]
            if len(targets) < 2 or not any(
                call["tool"] == "manage_apps" and call["args"].get("operation") == "instantiate"
                for call in tools
            ):
                raise AssertionError(
                    f"{record.payload['id']}: extend top is not multi-widget instantiated"
                )
    handoff = by_family["handoff"]
    if any(
        not record.grounded_generated
        for record in handoff
        if record.payload["difficulty"] != "level5"
    ):
        raise AssertionError("handoff rung lacks catalog-grounded pinned facts")
    for top in (
        record for record in handoff if record.payload["difficulty"] in {"level4", "level5"}
    ):
        if not any(
            call["tool"] == "assign_tasks_to_agents"
            for call in top.payload["eval"]["required_tools"]
        ):
            raise AssertionError(f"{top.payload['id']}: handoff top lacks delegation")
    for build in (record for record in handoff if record.payload["difficulty"] == "level5"):
        evaluation = build.payload["eval"]
        if any(
            len(evaluation.get(key, [])) != 1
            for key in (
                "required_widget_defs",
                "required_app_defs",
                "required_widgets",
                "required_generated_widgets",
            )
        ):
            raise AssertionError(f"{build.payload['id']}: handoff build chain is not minimal")
        tools = evaluation["required_tools"]
        graded = [call["tool"] for call in tools if not call.get("optional")]
        if graded != [
            "manage_backends",
            "manage_apps",
            "add_generative_widget",
            "assign_tasks_to_agents",
        ]:
            raise AssertionError(f"{build.payload['id']}: handoff build chain is incomplete")
        backend_call = next(call for call in tools if call["tool"] == "manage_backends")
        widgets_json = backend_call["args"].get("widgets_json", {})
        apps_json = backend_call["args"].get("apps_json", [])
        if len(widgets_json) != 1 or len(apps_json) != 1:
            raise AssertionError(f"{build.payload['id']}: handoff backend is not one-widget/app")
        if "sampleData" in json.dumps(widgets_json, ensure_ascii=False):
            raise AssertionError(f"{build.payload['id']}: handoff widget embeds sampleData")
        app_tabs = apps_json[0].get("tabs", {})
        if len(app_tabs) != 1:
            raise AssertionError(f"{build.payload['id']}: handoff app is not one-tab")
        if tools[-1].get("graded_args") != []:
            raise AssertionError(f"{build.payload['id']}: delegation must be existence-only")


def validate_payloads(records: list[TaskRecord]) -> dict[str, int]:
    """Run task shape, mission, and complete F1-F11/L1-L5 certification."""

    if len(records) != 192:
        raise AssertionError(f"expected 192 tasks, built {len(records)}")
    expected_top_keys = {"id", "category", "difficulty", "prompt", "setup", "eval"}
    allowed_eval = {
        "required_widgets",
        "required_tabs",
        "required_dashboard_name_contains",
        "required_tools",
        "required_values_in_answer",
        "required_generated_widgets",
        "required_widget_defs",
        "required_app_defs",
        "runtime_checks",
        "reference_answer",
        "max_turns",
    }
    ids: set[str] = set()
    for record in records:
        payload = record.payload
        task_id = str(payload["id"])
        if set(payload) != expected_top_keys:
            raise AssertionError(f"{task_id}: wrong top-level shape {sorted(payload)}")
        if set(payload["eval"]) - allowed_eval:
            raise AssertionError(f"{task_id}: unsupported eval fields")
        if task_id in ids:
            raise AssertionError(f"duplicate task id {task_id}")
        ids.add(task_id)
        if not task_id.endswith(f"_{payload['difficulty']}"):
            raise AssertionError(f"{task_id}: id/difficulty mismatch")
        setup = payload["setup"]
        if setup["workspace_baseline"] != "stark-workspace-a":
            raise AssertionError(f"{task_id}: wrong workspace baseline")
        if setup["workspace_backends"] != WORLD_BACKENDS:
            raise AssertionError(f"{task_id}: wrong four-backend world")
        if setup["workspace_skills"] != SKILL_SLUGS:
            raise AssertionError(f"{task_id}: wrong ten-skill world")
        values = payload["eval"].get("required_values_in_answer", [])
        expected_tools = [
            *WORKSPACE_TOOL_NAMES,
            *([FINAL_ANSWER_TOOL] if values else []),
        ]
        if setup["allowed_tools"] != expected_tools:
            raise AssertionError(f"{task_id}: wrong allowed tool surface")
        if any(call["tool"] == FINAL_ANSWER_TOOL for call in payload["eval"]["required_tools"]):
            raise AssertionError(f"{task_id}: final_answer appears in required_tools")
        if "sampleData" in json.dumps(payload["eval"], ensure_ascii=False):
            raise AssertionError(f"{task_id}: task embeds catalog sampleData")

    _assert_family_missions(records)
    catalogs = _catalogs()
    _assert_f1_f3(records, catalogs)
    _assert_f4(records)
    _assert_f5(records)
    counts = _assert_f6_f7(records)
    _assert_f8(records, catalogs)
    _assert_f9(records, catalogs)
    _assert_f10(records)
    _assert_f11(records)
    _assert_f12(records)
    _assert_l1_l5(records)
    _assert_wave2_requirements(records)
    _assert_instantiation_and_expect_fairness(records)
    _assert_wave3_requirements(records, catalogs)
    repair_summary = _assert_wave3_repairs(records)
    return {
        "tasks": len(records),
        "max_checks": max(counts.values()),
        "answer_tasks": sum(
            bool(record.payload["eval"].get("required_values_in_answer")) for record in records
        ),
        "grounded_handoffs": sum(bool(record.grounded_generated) for record in records),
        **repair_summary,
    }


def _manifest(records: list[TaskRecord]) -> JsonDict:
    return {
        "suite_id": "enterprise-apps-usage",
        "visibility": "public",
        "workspace_baseline": "stark-workspace-a",
        "workspace_backends": list(WORLD_BACKENDS),
        "workspace_skills": list(SKILL_SLUGS),
        "task_defaults": {
            "eval": {
                "layout": {"within_grid": True, "no_overlaps": True, "grid_width": 40},
                "trace_checks": {
                    "max_invalid_tool_calls": 2,
                    "forbid_invented_widget_ids": True,
                },
                "workspace_checks": {"preserve_other_dashboards": True},
            }
        },
        "content_sha256": task_payload_digest([record.payload for record in records]),
        "description": (
            "Usage-v3 waves 1-3: eight job-shaped families, four level-ladder spines "
            "per family, and mechanically certified F1-F10/L1-L5 fairness plus wave-3 "
            "knowledge governance and catalog coverage."
        ),
    }


def write_suite(records: list[TaskRecord]) -> None:
    """Write the suite task files and finalize the manifest."""

    # Refresh family directories in place; never touch the suite README.
    for family in FAMILY_LEVELS:
        directory = OUTPUT_DIR / family
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)
    for record in records:
        path = OUTPUT_DIR / record.family / f"{record.payload['id']}.json"
        path.write_text(
            json.dumps(record.payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    (OUTPUT_DIR / "task_suite.json").write_text(
        json.dumps(_manifest(records), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _assert_loaded_contracts(records: list[TaskRecord], loaded: list[Any]) -> None:
    by_id = {str(record.payload["id"]): record for record in records}
    for task in loaded:
        record = by_id[task.id]
        expected = [
            (call["tool"], _synthesized_contract(call))
            for call in record.payload["eval"]["required_tools"]
            if not call.get("optional")
        ]
        actual = list(task.success.required_tool_calls)
        if len(actual) != len(expected):
            raise AssertionError(
                f"{task.id}: loaded contract count {len(actual)} != {len(expected)}"
            )
        for criterion, (tool, args_contains) in zip(actual, expected, strict=True):
            if criterion.name != tool or criterion.args_contains != args_contains:
                raise AssertionError(f"{task.id}: loaded F1 contract mismatch for {tool}")
            existence_only_delegation = (
                tool == "assign_tasks_to_agents"
                and criterion.args_contains == {}
                and args_contains == {}
            )
            if _contains_forbidden_empty(criterion.args_contains) and not existence_only_delegation:
                raise AssertionError(f"{task.id}: loaded F1 contract contains empties")
        if task.limits.get("max_turns") != len(task.oracle_tool_calls) + 3:
            raise AssertionError(f"{task.id}: loaded F6 budget mismatch")


def certify_loaded_suite(
    records: list[TaskRecord],
) -> tuple[dict[str, int], dict[tuple[str, str], tuple[int, int]]]:
    """Load the suite directory and replay oracle/no-op certification."""

    if Path.cwd().resolve() != REPO:
        raise RuntimeError(f"run this generator from repository root {REPO}")
    tasks = load_task_directory(RELATIVE_OUTPUT_DIR)
    if len(tasks) != len(records):
        raise AssertionError(f"loader returned {len(tasks)} tasks, expected {len(records)}")
    _assert_loaded_contracts(records, tasks)
    oracle = OracleAgent()
    noop = NoopAgent()
    oracle_pass = 0
    noop_fail = 0
    table: dict[tuple[str, str], tuple[int, int]] = {}
    total = len(tasks)
    for index, task in enumerate(tasks, start=1):
        print(f"[certify {index:03d}/{total}] {task.family}/{task.id}", flush=True)
        oracle_episode = WorkspaceEpisode(task)
        for call in oracle.tool_calls(task):
            oracle_episode.step(call)
        oracle_grade = oracle_episode.grade()
        if not oracle_grade.passed:
            issues = "; ".join(
                f"{issue.code}: {issue.message}" for issue in oracle_grade.issues[:8]
            )
            raise RuntimeError(f"{task.id}: oracle failed: {issues}")
        oracle_pass += 1

        noop_episode = WorkspaceEpisode(task)
        for call in noop.tool_calls(task):
            noop_episode.step(call)
        if noop_episode.grade().passed:
            raise RuntimeError(f"{task.id}: no-op agent passed")
        noop_fail += 1
        prior_oracle, prior_noop = table.get((task.family, task.difficulty), (0, 0))
        table[(task.family, task.difficulty)] = (prior_oracle + 1, prior_noop + 1)
    return {"oracle_pass": oracle_pass, "noop_fail": noop_fail}, table


def _print_certification_table(
    table: dict[tuple[str, str], tuple[int, int]],
) -> None:
    levels = tuple(LEVEL_CAPS)
    print("CERTIFICATION TABLE (cell = oracle pass / noop fail)")
    print("family       | " + " | ".join(f"{level:>7}" for level in levels) + " | total")
    print("-" * 83)
    for family, expected_levels in FAMILY_LEVELS.items():
        cells: list[str] = []
        oracle_total = 0
        noop_total = 0
        for level in levels:
            if level not in expected_levels:
                cells.append("      —")
                continue
            oracle_cell, noop_cell = table.get((family, level), (0, 0))
            oracle_total += oracle_cell
            noop_total += noop_cell
            cells.append(f"    {oracle_cell}/{noop_cell}")
        print(f"{family:<12} | " + " | ".join(cells) + f" | {oracle_total}/{noop_total}")


def _print_coverage_summary(records: list[TaskRecord]) -> None:
    catalogs = _catalogs()
    whole = _graded_catalog_targets(records)
    legacy_spines = WAVE1_SPINES | WAVE2_SPINES
    legacy_records = [
        record
        for record in records
        if str(record.payload["id"]).rsplit("_level", 1)[0] in legacy_spines
    ]
    legacy = _graded_catalog_targets(legacy_records)
    for slug, origin in BACKEND_ORIGINS.items():
        total_widgets = len(catalogs[slug]["widgets"])
        wave3_delta = len(whole[origin] - legacy[origin])
        print(
            f"COVERAGE {origin}: {len(whole[origin])}/{total_widgets} distinct graded "
            f"targets (+{wave3_delta} wave3)",
            flush=True,
        )


def main() -> int:
    print("[1/4] Building thirty-two usage-v3 spine ladders", flush=True)
    records = build_tasks()
    print("[2/4] Asserting task shape, missions, F1-F11, and L1-L5", flush=True)
    summary = validate_payloads(records)
    print(
        "[static] "
        f"{summary['tasks']} tasks; max {summary['max_checks']} graded checks; "
        f"{summary['answer_tasks']} grounded answers; "
        f"{summary['grounded_handoffs']} grounded handoffs",
        flush=True,
    )
    print("[3/4] Writing and loading pilots/usage_v3", flush=True)
    write_suite(records)
    print("[4/4] Replaying oracle and no-op certification", flush=True)
    replay, table = certify_loaded_suite(records)
    _print_certification_table(table)
    expected_cell = (4, 4)
    if any(
        table.get((family, level)) != expected_cell
        for family, levels in FAMILY_LEVELS.items()
        for level in levels
    ):
        raise AssertionError("family x level certification table is not uniformly 4/4")
    _print_coverage_summary(records)
    print(f"D1 optional spec-reads: {summary['d1_optional_spec_reads']} sites", flush=True)
    print(f"D2 discovery reads added: {summary['d2_discovery_refs']} refs", flush=True)
    print(f"D3 extend L0/L1 spec-reads: {summary['d3_extend_spec_reads']} refs", flush=True)
    print(f"D4 stated-column datasets: {summary['d4_stated_column_tasks']} tasks", flush=True)
    print(f"D5 grounding reads: {summary['d5_grounding_refs']} refs", flush=True)
    print("D6 read-derived tokens described, F12 assertion active", flush=True)
    print("D7 extend prompts state the backend surface", flush=True)
    print("F11 assertion active", flush=True)
    total = len(records)
    if replay != {"oracle_pass": total, "noop_fail": total}:
        raise AssertionError(f"incomplete certification: {replay}")
    print(
        f"WAVE3 REPAIR2 COMPLETE {total}/{total} oracle pass, "
        f"{total}/{total} noop fail",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
