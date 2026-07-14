"""Generate the stark-onboard-a and stark-onboard-b initial-state files.

Each onboard state is a lived-in analyst workspace: Home, a few Stark apps
opened as-is, and personal dashboards assembled from widgets across other
apps, with names that never match an app name. This script instantiates the
compositions from the canonical Stark catalog, certifies them (widget and tab
references resolve, layouts are grid-bound and non-overlapping, personal
dashboards mix at least two source apps), and writes the self-contained files
under ``data/initial_states/`` that ``default_setup`` loads. Re-run
it only to regenerate the files.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from workspace_bench.core.models import JsonDict
from workspace_bench.workspace.default_setup import _home_dashboard, _instantiate_app
from workspace_bench.workspace.fixtures import FixtureBackend, build_stark_enterprise_backend
from workspace_bench.workspace.geometry import rects_overlap
from workspace_bench.workspace.widget_params import sanitize_data_args

OUTPUT_DIR = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "workspace_bench"
    / "data"
    / "initial_states"
)

GRID_WIDTH = 40

# A is a PM/research desk; B is a trading/operations desk. Personal dashboard
# names deliberately do not match any Stark app name, so discovery requires
# inspecting contents rather than matching titles.
COMPOSITIONS: dict[str, JsonDict] = {
    "stark_onboard_a.json": {
        "open_apps": (
            "Portfolio Command Center",
            "Equity Research Workbench",
            "Compliance Surveillance Hub",
        ),
        "personal_dashboards": (
            {
                "name": "Morning Markets",
                "tabs": [{"id": "overview", "name": "Overview"}],
                "widgets": [
                    {
                        "widget_id": "executive_investment_dashboard_firm_overview_firm_snapshot",
                        "tab_id": "overview",
                        "layout": {"x": 0, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "1D"},
                    },
                    {
                        "widget_id": "risk_exposure_monitor_dashboard_risk_snapshot",
                        "tab_id": "overview",
                        "layout": {"x": 20, "y": 0, "w": 20, "h": 14},
                        "data_args": {"portfolio": "Macro Multi-Asset", "period": "1D"},
                    },
                    {
                        "widget_id": "earnings_estimates_monitor_calendar_upcoming_earnings",
                        "tab_id": "overview",
                        "layout": {"x": 0, "y": 14, "w": 20, "h": 14},
                        "data_args": {"period": "1D"},
                    },
                    {
                        "widget_id": "crypto_research_dashboard_market_price_and_volume",
                        "tab_id": "overview",
                        "layout": {"x": 20, "y": 14, "w": 20, "h": 14},
                        "data_args": {"period": "1D"},
                    },
                ],
            },
            {
                "name": "IC Prep - Q3 Review",
                "tabs": [
                    {"id": "agenda", "name": "Agenda"},
                    {"id": "evidence", "name": "Evidence"},
                ],
                "widgets": [
                    {
                        "widget_id": "cio_investment_committee_pack_agenda_ic_agenda",
                        "tab_id": "agenda",
                        "layout": {"x": 0, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "QTD"},
                    },
                    {
                        "widget_id": "cio_investment_committee_pack_agenda_decisions_required",
                        "tab_id": "agenda",
                        "layout": {"x": 20, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "QTD"},
                    },
                    {
                        "widget_id": "cio_investment_committee_pack_allocations_capital_allocation",
                        "tab_id": "agenda",
                        "layout": {"x": 0, "y": 14, "w": 40, "h": 14},
                        "data_args": {"period": "QTD"},
                    },
                    {
                        "widget_id": "strategy_health_monitor_overview_workflow_overview",
                        "tab_id": "evidence",
                        "layout": {"x": 0, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "QTD"},
                    },
                    {
                        "widget_id": "client_360_flows_subscriptions_and_redemptions",
                        "tab_id": "evidence",
                        "layout": {"x": 20, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "QTD"},
                    },
                    {
                        "widget_id": "reporting_factsheet_studio_commentary_approved_commentary_library",
                        "tab_id": "evidence",
                        "layout": {"x": 0, "y": 14, "w": 40, "h": 14},
                        "data_args": {"period": "QTD"},
                    },
                ],
            },
            {
                "name": "Ops Daily Checks",
                "tabs": [{"id": "checks", "name": "Checks"}],
                "widgets": [
                    {
                        "widget_id": "fund_operations_control_tower_overview_workflow_overview",
                        "tab_id": "checks",
                        "layout": {"x": 0, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "1D"},
                    },
                    {
                        "widget_id": "nav_fees_close_dashboard_close_close_exceptions",
                        "tab_id": "checks",
                        "layout": {"x": 20, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "MTD"},
                    },
                    {
                        "widget_id": "vendor_dataset_monitor_incidents_incident_log",
                        "tab_id": "checks",
                        "layout": {"x": 0, "y": 14, "w": 20, "h": 14},
                        "data_args": {"period": "MTD"},
                    },
                    {
                        "widget_id": "workspace_data_control_center_data_health_feed_status",
                        "tab_id": "checks",
                        "layout": {"x": 20, "y": 14, "w": 20, "h": 14},
                        "data_args": {"period": "1D"},
                    },
                ],
            },
        ),
    },
    "stark_onboard_b.json": {
        "open_apps": (
            "Execution Desk",
            "Risk & Exposure Monitor",
            "Fund Operations Control Tower",
        ),
        "personal_dashboards": (
            {
                "name": "Trade Desk Morning",
                "tabs": [{"id": "desk", "name": "Desk"}],
                "widgets": [
                    {
                        "widget_id": "liquidity_tca_workbench_brokers_broker_scorecard",
                        "tab_id": "desk",
                        "layout": {"x": 0, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "1D"},
                    },
                    {
                        "widget_id": "stress_liquidity_lab_liquidity_crowded_names",
                        "tab_id": "desk",
                        "layout": {"x": 20, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "1D"},
                    },
                    {
                        "widget_id": "earnings_estimates_monitor_calendar_catalyst_calendar",
                        "tab_id": "desk",
                        "layout": {"x": 0, "y": 14, "w": 20, "h": 14},
                        "data_args": {"period": "1D"},
                    },
                    {
                        "widget_id": "crypto_research_dashboard_derivatives_funding_and_basis",
                        "tab_id": "desk",
                        "layout": {"x": 20, "y": 14, "w": 20, "h": 14},
                        "data_args": {"period": "1D"},
                    },
                ],
            },
            {
                "name": "Client Review Pack",
                "tabs": [
                    {"id": "book", "name": "Book"},
                    {"id": "reporting", "name": "Reporting"},
                ],
                "widgets": [
                    {
                        "widget_id": "client_360_client_book_client_accounts",
                        "tab_id": "book",
                        "layout": {"x": 0, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "QTD"},
                    },
                    {
                        "widget_id": "client_360_flows_pipeline_by_stage",
                        "tab_id": "book",
                        "layout": {"x": 20, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "QTD"},
                    },
                    {
                        "widget_id": "nav_fees_close_dashboard_cash_cash_movements",
                        "tab_id": "book",
                        "layout": {"x": 0, "y": 14, "w": 40, "h": 14},
                        "data_args": {"period": "QTD"},
                    },
                    {
                        "widget_id": "reporting_factsheet_studio_ddqs_ddq_and_rfp_tracker",
                        "tab_id": "reporting",
                        "layout": {"x": 0, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "QTD"},
                    },
                    {
                        "widget_id": "executive_investment_dashboard_firm_overview_net_flows",
                        "tab_id": "reporting",
                        "layout": {"x": 20, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "QTD"},
                    },
                    {
                        "widget_id": "corporate_access_meeting_notes_compliance_compliance_follow_ups",
                        "tab_id": "reporting",
                        "layout": {"x": 0, "y": 14, "w": 40, "h": 14},
                        "data_args": {},
                    },
                ],
            },
            {
                "name": "Quant Ideas Scratchpad",
                "tabs": [{"id": "ideas", "name": "Ideas"}],
                "widgets": [
                    {
                        "widget_id": "quant_research_backtest_lab_backtest_backtest_performance",
                        "tab_id": "ideas",
                        "layout": {"x": 0, "y": 0, "w": 20, "h": 14},
                        "data_args": {"period": "YTD"},
                    },
                    {
                        "widget_id": "quant_research_backtest_lab_optimization_efficient_frontier",
                        "tab_id": "ideas",
                        "layout": {"x": 20, "y": 0, "w": 20, "h": 14},
                        "data_args": {},
                    },
                    {
                        "widget_id": "strategy_health_monitor_capacity_capacity_utilization",
                        "tab_id": "ideas",
                        "layout": {"x": 0, "y": 14, "w": 20, "h": 14},
                        "data_args": {"period": "YTD"},
                    },
                    {
                        "widget_id": "healthcare_research_dashboard_clinical_trial_catalyst_calendar",
                        "tab_id": "ideas",
                        "layout": {"x": 20, "y": 14, "w": 20, "h": 14},
                        "data_args": {},
                    },
                ],
            },
        ),
    },
}


def build_state(stark: FixtureBackend, composition: JsonDict) -> JsonDict:
    apps_by_name = {str(app["name"]): app for app in stark.apps}
    dashboards: list[JsonDict] = [_home_dashboard()]
    for app_name in composition["open_apps"]:
        if app_name not in apps_by_name:
            raise ValueError(f"unknown Stark app in onboard composition: {app_name!r}")
        dashboards.append(_instantiate_app(stark, apps_by_name[app_name]))
    for spec in composition["personal_dashboards"]:
        dashboards.append(_personal_dashboard(stark, spec))
    return {"dashboards": dashboards}


def _personal_dashboard(stark: FixtureBackend, spec: JsonDict) -> JsonDict:
    widgets: list[JsonDict] = []
    for entry in spec["widgets"]:
        widget_id = str(entry["widget_id"])
        if widget_id not in stark.widgets:
            raise ValueError(f"unknown Stark widget in onboard composition: {widget_id!r}")
        data_args = sanitize_data_args(
            stark.widgets[widget_id],
            copy.deepcopy(entry.get("data_args", {})),
            mode="create",
        )
        widgets.append(
            {
                "origin": stark.name,
                "widget_id": widget_id,
                "tab_id": str(entry["tab_id"]),
                "layout": copy.deepcopy(entry["layout"]),
                "data_args": data_args,
            }
        )
    return {
        "name": str(spec["name"]),
        "tabs": copy.deepcopy(spec["tabs"]),
        "widgets": widgets,
        "activate": False,
    }


def certify(stark: FixtureBackend, state: JsonDict, composition: JsonDict) -> None:
    app_names = {str(app["name"]) for app in stark.apps}
    dashboards = state["dashboards"]
    failures: list[str] = []
    if dashboards[0] != _home_dashboard():
        failures.append("first dashboard must be the active Home")
    personal_count = len(composition["personal_dashboards"])
    for dashboard in dashboards[-personal_count:]:
        if dashboard["name"] in app_names:
            failures.append(f"personal dashboard {dashboard['name']!r} matches an app name")
        prefixes = {widget["widget_id"].split("_")[0] for widget in dashboard["widgets"]}
        if len(prefixes) < 2:
            failures.append(f"{dashboard['name']!r} does not mix source apps")
    for dashboard in dashboards[1:]:
        tab_ids = {tab["id"] for tab in dashboard["tabs"]}
        rects_by_tab: dict[str, list[JsonDict]] = {}
        for widget in dashboard["widgets"]:
            if widget["widget_id"] not in stark.widgets:
                failures.append(f"{dashboard['name']!r}: unknown widget {widget['widget_id']!r}")
            if widget["tab_id"] not in tab_ids:
                failures.append(f"{dashboard['name']!r}: unknown tab {widget['tab_id']!r}")
            layout = widget["layout"]
            if not (
                layout["x"] >= 0
                and layout["y"] >= 0
                and layout["w"] > 0
                and layout["h"] > 0
                and layout["x"] + layout["w"] <= GRID_WIDTH
            ):
                failures.append(f"{dashboard['name']!r}: layout out of grid")
            rects_by_tab.setdefault(widget["tab_id"], []).append(layout)
        for rects in rects_by_tab.values():
            for index, rect in enumerate(rects):
                for other in rects[index + 1 :]:
                    if rects_overlap(rect, other):
                        failures.append(f"{dashboard['name']!r}: overlapping layouts")
    if failures:
        raise RuntimeError("Onboard state certification failed:\n" + "\n".join(failures))


def main() -> int:
    stark = build_stark_enterprise_backend()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, composition in COMPOSITIONS.items():
        state = build_state(stark, composition)
        certify(stark, state, composition)
        payload = {
            "source": {
                "derived_from": "backends/stark_enterprise_x.json",
                "generator": "scripts/generators/generate_onboard_states.py",
                "open_apps": list(composition["open_apps"]),
            },
            "initial_state": state,
        }
        path = OUTPUT_DIR / filename
        path.write_text(
            json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        widgets = sum(len(d["widgets"]) for d in state["dashboards"])
        print(f"Wrote {filename}: {len(state['dashboards'])} dashboards, {widgets} widgets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
