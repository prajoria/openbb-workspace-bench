"""Family E2E - r4-only building capstones."""

from __future__ import annotations

import json

from . import common as c


def _add_capstone(
    slug: str,
    desk_key: str,
    table_id: str,
    table_name: str,
    table_desc: str,
    endpoint: str,
    rows: list[dict],
    sibling_id: str,
    app_name: str,
    app_desc: str,
    tabs: tuple[tuple[str, str], tuple[str, str]],
    dashboard_name: str,
    note_term: str,
) -> None:
    desk = c.desk(desk_key)
    focus_field = next(iter(rows[0]))
    config_param = c.text_param(
        focus_field,
        focus_field.replace("_", " ").title(),
        str(rows[0][focus_field]),
        f"{table_name} focus field.",
    )
    set_value = rows[1][focus_field]
    table = c.derive_table_def(
        table_name, table_desc, endpoint, rows, params=[config_param]
    )
    sibling = c.desk_widget(desk_key, sibling_id)
    widgets = {table_id: table, sibling_id: sibling}
    (table_tab_id, table_tab_name), (sibling_tab_id, sibling_tab_name) = tabs
    app = c.app_def(app_name, app_desc, tabs=[
        (table_tab_id, table_tab_name, [c.layout_item(table_id, 0, 0, 20, 9)]),
        (sibling_tab_id, sibling_tab_name, [c.layout_item(sibling_id, 0, 0, 20, 9)]),
    ])
    note_text = f"{app_name} is live from {desk['backend']}: {note_term} ready."
    param_words = c.param_requirement(config_param)
    table_words = (
        f"`{table_id}` data API: name \"{table_name}\", description "
        f"\"{table_desc}\", endpoint {endpoint}, type table, gridData w=20 h=9. "
        f"It takes {param_words}. "
        f"The endpoint serves sample rows like {c.rows_text(rows)}. "
        f"{c.DERIVATION_RULES} {c.DERIVATION_EXAMPLE}"
    )
    sibling_words = c.widget_requirements_text(sibling_id, sibling)
    app_words = c.app_requirements_text(app)
    configure_words = (
        f"set {focus_field} to {json.dumps(set_value)} on the opened "
        f"`{table_id}` widget"
    )
    sid = f"{slug}"
    c.add("e2e", "r4", {
        "id": sid,
        "title": f"Ship, open, and configure {app_name}",
        "workflow": desk["workflow"], "subdomain": desk["subdomain"],
        "tags": ["build-openbb-apps", "widgets-json", "apps-json", "e2e",
                  "orchestration"],
        "prompt": c.phrased(sid, [
            (f"End to end. Publish \"{desk['backend']}\" at {desk['url']} in one "
             f"manage_backends add. widgets.json has the derived table "
             f"{table_words}; plus sibling widget {sibling_words}. apps.json "
             f"ships {app_words}. Then instantiate \"{app_name}\" into dashboard "
             f"\"{dashboard_name}\", {configure_words}, and leave a note titled \"{app_name}\" that "
             f"says exactly: \"{note_text}\""),
            (f"Build, publish, open, configure, document. Backend \"{desk['backend']}\" "
             f"({desk['url']}) serves a data-API table: {table_words}. It also "
             f"serves {sibling_words}. Ship app {app_words}, instantiate it as "
             f"\"{dashboard_name}\", {configure_words}, then add note \"{app_name}\" saying "
             f"\"{note_text}\"."),
            (f"Build the full custom backend for \"{desk['backend']}\" at "
             f"{desk['url']}: table from rows and rules ({table_words}); sibling "
             f"{sibling_words}; app {app_words}. Add it once, instantiate "
             f"\"{app_name}\" into \"{dashboard_name}\", {configure_words}, and create note "
             f"\"{app_name}\" with text \"{note_text}\"."),
        ]),
        "fixtures": {},
        "initial_state": {},
        "allowed_tools": c.APP_TOOLS + ["add_generative_widget", "update_widget"],
        "success": {
            "required_widget_defs": [
                c.widget_def_checks(desk["backend"], table_id, table),
                c.widget_def_anchor_checks(desk["backend"], sibling_id, sibling),
            ],
            "required_app_defs": [c.app_def_checks(desk["backend"], app)],
            "required_widgets": [
                {"origin": desk["backend"], "widget_id": table_id,
                 "data_args": {focus_field: set_value},
                 "min_count": 1},
            ],
            "required_generated_widgets": [{
                "widget_type": "note",
                "data_contains": [app_name, note_term],
                "min_count": 1,
            }],
            "layout": {"within_grid": True, "no_overlaps": True,
                        "grid_width": 40},
            "trace_checks": dict(c.TRACE_T4),
        },
        "oracle_tool_calls": [
            c.add_backend_call(desk["backend"], desk["url"], widgets, apps=[app]),
            c.instantiate_call("backend_001", app_name, dashboard_name),
            {"tool": "update_widget",
             "args": {"widget_id": table_id,
                      "data_args": {focus_field: set_value}}},
            {"tool": "add_generative_widget",
             "args": {"widget_type": "note", "name": app_name,
                      "data": note_text}},
        ],
    })


def build() -> None:
    specs = [
        {
            "slug": "research_room",
            "desk_key": "earnings",
            "table_id": "research_room_table",
            "table_name": "Research Room Table",
            "table_desc": "Analyst research actions by ticker.",
            "endpoint": "/research-room-table",
            "rows": [
                {"ticker": "AAPL", "analyst": "North Coast",
                 "rating": "Buy", "upside_pct": 0.12},
                {"ticker": "MSFT", "analyst": "Lake Street",
                 "rating": "Hold", "upside_pct": 0.04},
            ],
            "sibling_id": "earnings_note",
            "app_name": "Research Room",
            "app_desc": "Analyst actions and earnings notes.",
            "tabs": (("research", "Research"), ("notes", "Notes")),
            "dashboard_name": "Research Room Live",
            "note_term": "research room",
        },
        {
            "slug": "execution_monitor",
            "desk_key": "execution",
            "table_id": "execution_monitor_table",
            "table_name": "Execution Monitor Table",
            "table_desc": "Venue execution quality and rejects.",
            "endpoint": "/execution-monitor-table",
            "rows": [
                {"venue": "ARCA", "orders": 1240,
                 "reject_rate_pct": 0.003, "as_of": "2026-07-01"},
                {"venue": "EDGX", "orders": 980,
                 "reject_rate_pct": 0.005, "as_of": "2026-07-01"},
            ],
            "sibling_id": "exception_metric",
            "app_name": "Execution Monitor",
            "app_desc": "Execution venue quality and exceptions.",
            "tabs": (("venues", "Venues"), ("exceptions", "Exceptions")),
            "dashboard_name": "Execution Monitor Live",
            "note_term": "execution monitor",
        },
        {
            "slug": "compliance_surveillance",
            "desk_key": "compliance",
            "table_id": "surveillance_cases_table",
            "table_name": "Surveillance Cases Table",
            "table_desc": "Open surveillance cases by severity.",
            "endpoint": "/surveillance-cases-table",
            "rows": [
                {"case_id": "C-1042", "desk": "Rates",
                 "severity": "high", "age_days": 12},
                {"case_id": "C-1044", "desk": "Equities",
                 "severity": "medium", "age_days": 4},
            ],
            "sibling_id": "alert_metric",
            "app_name": "Compliance Surveillance",
            "app_desc": "Surveillance cases and alert posture.",
            "tabs": (("cases", "Cases"), ("posture", "Posture")),
            "dashboard_name": "Compliance Surveillance Live",
            "note_term": "surveillance",
        },
        {
            "slug": "vendor_ops",
            "desk_key": "sla",
            "table_id": "vendor_ops_table",
            "table_name": "Vendor Ops Table",
            "table_desc": "Vendor uptime and latency posture.",
            "endpoint": "/vendor-ops-table",
            "rows": [
                {"vendor": "AlphaFeed", "uptime_pct": 0.999,
                 "latency_ms": 240, "status": "open"},
                {"vendor": "QuoteStream", "uptime_pct": 0.982,
                 "latency_ms": 610, "status": "breach"},
            ],
            "sibling_id": "breach_metric",
            "app_name": "Vendor Ops",
            "app_desc": "Vendor uptime, latency, and breaches.",
            "tabs": (("vendors", "Vendors"), ("breaches", "Breaches")),
            "dashboard_name": "Vendor Ops Live",
            "note_term": "vendor ops",
        },
        {
            "slug": "macro_morning",
            "desk_key": "rates",
            "table_id": "macro_morning_table",
            "table_name": "Macro Morning Table",
            "table_desc": "Rates morning levels and changes.",
            "endpoint": "/macro-morning-table",
            "rows": [
                {"series": "DGS10", "level": 4.21,
                 "change_bp": -3, "as_of": "2026-07-01"},
                {"series": "DGS2", "level": 3.86,
                 "change_bp": -1, "as_of": "2026-07-01"},
            ],
            "sibling_id": "yield_curve",
            "app_name": "Macro Morning",
            "app_desc": "Rates levels and curve context.",
            "tabs": (("levels", "Levels"), ("curve", "Curve")),
            "dashboard_name": "Macro Morning Live",
            "note_term": "macro morning",
        },
        {
            "slug": "healthcare_pipeline",
            "desk_key": "healthcare",
            "table_id": "pipeline_status_table",
            "table_name": "Pipeline Status Table",
            "table_desc": "Healthcare pipeline programs by phase.",
            "endpoint": "/pipeline-status-table",
            "rows": [
                {"ticker": "PFE", "phase": "III",
                 "programs": 4, "readout_date": "2026-08-19"},
                {"ticker": "MRNA", "phase": "II",
                 "programs": 3, "readout_date": "2026-09-02"},
            ],
            "sibling_id": "pipeline_chart",
            "app_name": "Healthcare Pipeline",
            "app_desc": "Pipeline table and phase chart.",
            "tabs": (("pipeline", "Pipeline"), ("phase", "Phase")),
            "dashboard_name": "Healthcare Pipeline Live",
            "note_term": "pipeline",
        },
        {
            "slug": "earnings_season",
            "desk_key": "earnings",
            "table_id": "earnings_season_table",
            "table_name": "Earnings Season Table",
            "table_desc": "Earnings surprises and report dates.",
            "endpoint": "/earnings-season-table",
            "rows": [
                {"ticker": "AAPL", "eps_surprise_pct": 0.042,
                 "revenue_beat": True, "report_date": "2026-07-24"},
                {"ticker": "MSFT", "eps_surprise_pct": 0.021,
                 "revenue_beat": True, "report_date": "2026-07-29"},
            ],
            "sibling_id": "surprise_metric",
            "app_name": "Earnings Season",
            "app_desc": "Season surprises and headline metric.",
            "tabs": (("season", "Season"), ("surprise", "Surprise")),
            "dashboard_name": "Earnings Season Live",
            "note_term": "earnings season",
        },
        {
            "slug": "vol_cockpit",
            "desk_key": "vol",
            "table_id": "vol_cockpit_table",
            "table_name": "Vol Cockpit Table",
            "table_desc": "Implied and realized volatility by tenor.",
            "endpoint": "/vol-cockpit-table",
            "rows": [
                {"tenor": "1M", "iv_pct": 0.182,
                 "realized_pct": 0.164, "as_of": "2026-07-01"},
                {"tenor": "3M", "iv_pct": 0.204,
                 "realized_pct": 0.181, "as_of": "2026-07-01"},
            ],
            "sibling_id": "vix_advanced",
            "app_name": "Vol Cockpit",
            "app_desc": "Volatility table and advanced chart.",
            "tabs": (("surface", "Surface"), ("chart", "Chart")),
            "dashboard_name": "Vol Cockpit Live",
            "note_term": "vol cockpit",
        },
        {
            "slug": "chain_flows",
            "desk_key": "tvl",
            "table_id": "chain_flows_table",
            "table_name": "Chain Flows Table",
            "table_desc": "Net chain flows and fee share.",
            "endpoint": "/chain-flows-table",
            "rows": [
                {"chain": "Ethereum", "net_flow_usd": 120000000,
                 "fee_pct": 0.031, "as_of": "2026-07-01"},
                {"chain": "Solana", "net_flow_usd": -15000000,
                 "fee_pct": 0.018, "as_of": "2026-07-01"},
            ],
            "sibling_id": "gas_metric",
            "app_name": "Chain Flows",
            "app_desc": "Chain flows and gas context.",
            "tabs": (("flows", "Flows"), ("gas", "Gas")),
            "dashboard_name": "Chain Flows Live",
            "note_term": "chain flows",
        },
        {
            "slug": "rates_auctions",
            "desk_key": "rates",
            "table_id": "rates_auctions_table",
            "table_name": "Rates Auctions Table",
            "table_desc": "Upcoming auctions and demand metrics.",
            "endpoint": "/rates-auctions-table",
            "rows": [
                {"auction_date": "2026-07-14", "security": "10Y Note",
                 "size_bn": 42, "bid_to_cover": 2.43},
                {"auction_date": "2026-07-15", "security": "30Y Bond",
                 "size_bn": 25, "bid_to_cover": 2.31},
            ],
            "sibling_id": "curve_spread_metric",
            "app_name": "Rates Auctions",
            "app_desc": "Auction calendar and curve spread.",
            "tabs": (("auctions", "Auctions"), ("spread", "Spread")),
            "dashboard_name": "Rates Auctions Live",
            "note_term": "rates auctions",
        },
        {
            "slug": "case_triage",
            "desk_key": "compliance",
            "table_id": "case_triage_table",
            "table_name": "Case Triage Table",
            "table_desc": "Case owners, priorities, and SLA days.",
            "endpoint": "/case-triage-table",
            "rows": [
                {"case_id": "C-1045", "owner": "Mira",
                 "priority": "high", "sla_days": 2},
                {"case_id": "C-1048", "owner": "Jon",
                 "priority": "medium", "sla_days": 5},
            ],
            "sibling_id": "case_notes",
            "app_name": "Case Triage",
            "app_desc": "Case triage queue and notes.",
            "tabs": (("triage", "Triage"), ("notes", "Notes")),
            "dashboard_name": "Case Triage Live",
            "note_term": "case triage",
        },
        {
            "slug": "catalyst_calendar",
            "desk_key": "healthcare",
            "table_id": "catalyst_calendar_table",
            "table_name": "Catalyst Calendar Table",
            "table_desc": "Healthcare catalysts and impact scores.",
            "endpoint": "/catalyst-calendar-table",
            "rows": [
                {"ticker": "MRNA", "event": "Phase II readout",
                 "event_date": "2026-09-02", "impact_score": 8},
                {"ticker": "PFE", "event": "FDA decision",
                 "event_date": "2026-10-11", "impact_score": 7},
            ],
            "sibling_id": "catalyst_metric",
            "app_name": "Catalyst Calendar",
            "app_desc": "Catalyst calendar and 30-day count.",
            "tabs": (("calendar", "Calendar"), ("count", "Count")),
            "dashboard_name": "Catalyst Calendar Live",
            "note_term": "catalyst calendar",
        },
    ]
    for spec in specs:
        _add_capstone(**spec)
