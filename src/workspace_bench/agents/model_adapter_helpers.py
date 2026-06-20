"""Shared prompt helpers for model comparison adapters."""

from __future__ import annotations

import re
from typing import Any


FIXTURE_ORIGINS = {
    "equities": "Bench Equities",
    "macro": "Bench Macro",
    "portfolio": "Bench Portfolio",
    "stark-enterprise": "Bench Stark Enterprise",
}
WIDGET_HINTS = {
    "Bench Equities": {
        "price_performance": {
            "data_args": {"symbol": "AAPL"},
            "note": "Use symbol, not ticker.",
        },
        "latest_news": {
            "data_args": {"symbol": "AAPL", "limit": 5},
            "note": "Use symbol for the company ticker.",
        },
        "estimate_history": {
            "data_args": {"symbol": "AAPL"},
            "note": "Use symbol for the company ticker.",
        },
        "fundamental_metrics": {
            "data_args": {"symbol": "AAPL"},
            "note": "Use symbol for the company ticker.",
        },
    },
    "Bench Macro": {
        "macro_timeseries": {
            "data_args": {"series": "DGS2"},
            "note": "Use series for macro identifiers such as FEDFUNDS, DGS2, DGS10, CPIAUCSL.",
        },
        "yield_curve": {"data_args": {}, "note": "No required data_args."},
    },
    "Bench Portfolio": {
        "holdings_table": {"data_args": {}, "note": "No required data_args."},
        "sector_exposure": {"data_args": {}, "note": "No required data_args."},
        "risk_metrics": {"data_args": {}, "note": "No required data_args."},
    },
    "Bench Stark Enterprise": {
        "client_360_meeting_prep_approved_talking_points": {
            "data_args": {"client": "Northstar Pension", "period": "YTD"},
            "note": "Client Meeting Prep tab.",
        },
        "client_360_meeting_prep_meeting_agenda": {
            "data_args": {"client": "Northstar Pension", "period": "YTD"},
            "note": "Client Meeting Prep tab.",
        },
        "client_360_portfolio_view_client_portfolio_summary": {
            "data_args": {"client": "Northstar Pension", "period": "YTD"},
            "note": "Portfolio tab.",
        },
        "compliance_surveillance_hub_alerts_surveillance_alerts": {
            "data_args": {"status": "Open", "period": "YTD"},
            "note": "Alerts tab.",
        },
        "compliance_surveillance_hub_restricted_list_restricted_and_watch_list": {
            "data_args": {"status": "Open", "period": "YTD"},
            "note": "Restricted List tab.",
        },
        "earnings_estimates_monitor_estimates_consensus_revisions": {
            "data_args": {"ticker": "LLY", "period": "YTD"},
            "note": "Estimates tab.",
        },
        "earnings_estimates_monitor_post_earnings_price_reaction": {
            "data_args": {"ticker": "LLY", "period": "YTD"},
            "note": "Price Reaction tab.",
        },
        "equity_research_workbench_company_company_tear_sheet": {
            "data_args": {"ticker": "LLY", "period": "YTD"},
            "note": "Company tab.",
        },
        "equity_research_workbench_valuation_comps_table": {
            "data_args": {"ticker": "LLY", "period": "YTD"},
            "note": "Valuation tab.",
        },
        "equity_research_workbench_valuation_dcf_sensitivity": {
            "data_args": {"ticker": "LLY", "period": "YTD"},
            "note": "Valuation tab.",
        },
        "execution_desk_blotter_live_orders": {
            "data_args": {"desk": "US Equities", "status": "Open", "period": "YTD"},
            "note": "Blotter tab.",
        },
        "execution_desk_exceptions_rejected_orders": {
            "data_args": {"desk": "US Equities", "status": "Open", "period": "YTD"},
            "note": "Exceptions tab.",
        },
        "execution_desk_exceptions_restricted_list_checks": {
            "data_args": {"desk": "US Equities", "status": "Open", "period": "YTD"},
            "note": "Exceptions tab.",
        },
        "healthcare_research_dashboard_clinical_trial_catalyst_calendar": {
            "data_args": {},
            "note": "Healthcare research app.",
        },
        "healthcare_research_dashboard_documents_sell_side_research_pdfs": {
            "data_args": {},
            "note": "Healthcare research app.",
        },
        "portfolio_command_center_actions_trade_ideas": {
            "data_args": {},
            "note": "Actions tab.",
        },
        "portfolio_command_center_holdings_holdings_table": {
            "data_args": {},
            "note": "Holdings tab.",
        },
        "rebalance_scenario_lab_drift_current_vs_target_weights": {
            "data_args": {"fund": "Flagship Long/Short", "period": "YTD"},
            "note": "Drift tab.",
        },
        "risk_exposure_monitor_dashboard_var_trend": {
            "data_args": {"fund": "Flagship Long/Short", "period": "YTD", "raw": True},
            "note": "Use get_widget_data for underlying risk data.",
        },
        "vendor_dataset_monitor_slas_vendor_sla_status": {
            "data_args": {"vendor": "FactSet", "status": "In Review", "period": "YTD"},
            "note": "Vendor SLA monitoring.",
        },
    },
}


TOOL_REFERENCE = {
    "get_workspace_snapshot": {
        "description": "Inspect current dashboard, tabs, widgets, layouts, and backends.",
        "args": {},
    },
    "manage_dashboard": {
        "description": "Create, read, or rename dashboards.",
        "args": {
            "operation": "create|read|update",
            "name": "string, required for create/update",
            "dashboard_id": "string, optional",
            "activate": "boolean, optional for create",
        },
    },
    "manage_navigation_bar": {
        "description": "Create, add, remove, or rename dashboard tabs.",
        "args": {
            "operation": "create|add_tabs|remove_tabs|rename_tabs",
            "tabs": [{"name": "Tab Name"}],
            "rename_map": {"old-tab-id": "New Name"},
            "dashboard_id": "string, optional",
        },
    },
    "navigate_workspace": {
        "description": "Switch active dashboard or tab.",
        "args": {
            "operation": "dashboard|tab",
            "dashboard_id": "string, optional for tab, required for dashboard",
            "tab_id": "string, optional for dashboard, required for tab",
        },
    },
    "list_available_widgets": {
        "description": "List widgets for a backend origin such as Bench Equities.",
        "args": {"origin": "string, optional", "backend_id": "string, optional"},
    },
    "get_widget_schema": {
        "description": "Get schema for one listed widget.",
        "args": {"origin": "string", "widget_id": "string"},
    },
    "get_params_options": {
        "description": "Fetch options for a schema parameter that requires lookup.",
        "args": {
            "origin": "string",
            "widget_id": "string",
            "param_name": "string",
            "data_args": "object, optional",
        },
    },
    "get_widget_data": {
        "description": "Fetch fixture data for one widget.",
        "args": {
            "origin": "string",
            "widget_id": "string",
            "data_args": "object, optional",
        },
    },
    "create_widget": {
        "description": "Create a regular Workspace widget.",
        "args": {
            "origin": "string",
            "widget_id": "string",
            "data_args": "object, optional",
            "ui_args": "object, optional",
            "dashboard_id": "string, optional",
        },
    },
    "update_widget": {
        "description": "Update widget data_args or ui_args. Do not use for layout.",
        "args": {
            "widget_uuid": "string, preferred when known",
            "widget_id": "string, only when exactly one exists",
            "data_args": "object, optional",
            "ui_args": "object, optional",
            "dashboard_id": "string, optional",
        },
    },
    "update_widget_layout": {
        "description": "Move or resize one widget.",
        "args": {
            "widget_uuid": "string, preferred when known",
            "widget_id": "string, only when exactly one exists",
            "x": "number",
            "y": "number",
            "w": "number",
            "h": "number",
            "tab_id": "string, optional",
            "dashboard_id": "string, optional",
        },
    },
    "delete_widget": {
        "description": "Delete one widget.",
        "args": {
            "widget_uuid": "string, preferred when known",
            "widget_id": "string, only when exactly one exists",
            "dashboard_id": "string, optional",
        },
    },
    "add_generative_widget": {
        "description": "Add generated note, table, chart, or HTML widget.",
        "args": {
            "widget_type": "note|table|chart|html",
            "name": "string, optional",
            "data": "string for note/html; array for table/chart",
            "description": "string, optional",
            "chart_params": "object with chartType, xKey, yKey for chart",
            "inner_tab": "string tab id, optional",
            "dashboard_id": "string UUID from tool result only, optional; omit for active dashboard",
        },
    },
    "read_widget": {
        "description": "Read one existing widget.",
        "args": {
            "widget_uuid": "string, preferred when known",
            "widget_id": "string, only when exactly one exists",
            "dashboard_id": "string, optional",
        },
    },
    "manage_backends": {
        "description": "List, add, or refresh fixture backends.",
        "args": {
            "operation": "list|add|refresh",
            "name": "string, required for add",
            "backend_id": "string, optional",
            "url": "string, optional",
        },
    },
    "manage_apps": {
        "description": "List, read, or instantiate app templates from a backend.",
        "args": {
            "operation": "list|read|instantiate",
            "backend_id": "string",
            "app_name": "string, optional",
            "template_id": "string, optional",
            "dashboard_name": "string, optional for instantiate",
            "activate": "boolean, optional",
        },
    },
    "get_skill_content": {
        "description": "Read deterministic Workspace skill content by exact skill slug.",
        "args": {
            "slug": "string, e.g. finance-earnings-prep",
            "reason": "string, optional",
        },
    },
    "assign_tasks_to_agents": {
        "description": "Delegate work to external Workspace agents.",
        "args": {
            "task_requests": [
                {
                    "id": "string task id",
                    "description": "string task description",
                    "assigned_holder_url": "string URL or workspace holder",
                    "assigned_agent_id": "string agent id",
                }
            ]
        },
    },
}


def fixture_origin_hints(fixtures: dict[str, Any]) -> dict[str, str]:
    hints = {}
    for backend in fixtures.get("backends", []):
        if not isinstance(backend, dict):
            continue
        name = backend.get("name")
        if isinstance(name, str):
            hints[name] = FIXTURE_ORIGINS.get(name, name)
    return hints


def fixture_widget_hints(origin_hints: dict[str, str]) -> dict[str, Any]:
    return {
        origin: WIDGET_HINTS[origin]
        for origin in origin_hints.values()
        if origin in WIDGET_HINTS
    }


def strip_code_fence(text: str) -> str:
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL)
    return fence.group(1).strip() if fence else text
