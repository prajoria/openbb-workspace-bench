"""Family EXTEND - refresh served custom backends without dropping artifacts."""

from __future__ import annotations

import json

from . import common as c


def _copy(definition: dict) -> dict:
    return json.loads(json.dumps(definition))


def _anchor_with_patch(
    backend_name: str,
    widget_id: str,
    definition: dict,
    patch: dict,
) -> dict:
    check = c.widget_def_anchor_checks(backend_name, widget_id, definition)
    check["expect"].update(patch.get("expect", {}))
    if "params_include" in patch:
        check["params_include"] = patch["params_include"]
    if "columns_include" in patch:
        check["columns_include"] = patch["columns_include"]
    return check


def _seed_with_warnings(
    name: str,
    url: str,
    widgets: dict,
    apps: list[dict] | None = None,
) -> dict:
    flags = c.validation_flags(
        widgets=widgets,
        apps=apps,
        widget_ids=set(widgets),
    )
    state = c.seeded_custom(name, url, widgets, apps=apps)
    state["custom_backends"][0]["warnings"] = c.terse_flags(flags)
    return state


def _mutate_type(definition: dict, bad_type: str) -> dict:
    broken = _copy(definition)
    broken["type"] = bad_type
    return broken


def _mutate_grid_w(definition: dict, bad_w: int) -> dict:
    broken = _copy(definition)
    broken.setdefault("gridData", {})["w"] = bad_w
    return broken


def _mutate_stale(definition: dict, bad_stale: int) -> dict:
    broken = _copy(definition)
    broken["staleTime"] = bad_stale
    return broken


def _mutate_param_type(definition: dict, param_name: str, bad_type: str) -> dict:
    broken = _copy(definition)
    for param in broken.get("params", []) or []:
        if isinstance(param, dict) and param.get("paramName") == param_name:
            param["type"] = bad_type
    return broken


def _drop_header(definition: dict, field: str) -> dict:
    broken = _copy(definition)
    columns = broken.get("data", {}).get("table", {}).get("columnsDefs", [])
    for column in columns:
        if isinstance(column, dict) and column.get("field") == field:
            column.pop("headerName", None)
    return broken


def _with_config(definition: dict, **config) -> dict:
    updated = _copy(definition)
    updated.update(config)
    return updated


def _without_time_config(definition: dict) -> dict:
    copied = _copy(definition)
    copied.pop("staleTime", None)
    copied.pop("refetchInterval", None)
    return copied


def _policy_requirements(widget_id: str, definition: dict) -> str:
    policies = []
    stale = definition.get("staleTime")
    if isinstance(stale, int) and not isinstance(stale, bool):
        policies.append(f"it caches results for {stale // 60000} minutes")
    interval = definition.get("refetchInterval")
    if isinstance(interval, int) and not isinstance(interval, bool):
        policies.append(f"it auto-refreshes every {interval // 1000} seconds")
    return (
        f"{c.widget_requirements_text(widget_id, _without_time_config(definition))}; "
        f"{' and '.join(policies)}. {c.CONFIG_RULES}"
    )


def build() -> None:
    # ------------------------------------------------------------------ t0
    # Seed one widget, then refresh widgets_json with the served widget plus
    # one exact-JSON addition.
    t0_specs = [
        ("vol", "vix_term_structure", "vol_regime_metric"),
        ("rates", "yield_curve", "curve_spread_metric"),
        ("execution", "open_orders", "exception_metric"),
        ("healthcare", "pipeline_chart", "catalyst_metric"),
    ]
    for desk_key, seeded_id, added_id in t0_specs:
        desk = c.desk(desk_key)
        seeded = c.desk_widget(desk_key, seeded_id)
        added = _with_config(
            c.desk_widget(desk_key, added_id),
            staleTime=900000,
            category="Desk Extensions",
        )
        initial_widgets = {seeded_id: seeded}
        final_widgets = {seeded_id: seeded, added_id: added}
        sid = f"auth_t0_extend_add_{added_id}"
        brief = c.widget_requirements_text(added_id, added)
        c.add("extend", "t0", {
            "id": sid,
            "title": f"Refresh {desk['backend']} with {added['name']}",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "refresh", "extend"],
            "prompt": c.phrased(sid, [
                (f"The custom backend \"{desk['backend']}\" is already connected "
                 f"at {desk['url']} and serves `{seeded_id}`. Refresh its "
                 f"widgets_json so it still carries `{seeded_id}` and also adds "
                 f"one exact widget: {brief}."),
                (f"Update the connected backend \"{desk['backend']}\" with a "
                 "manage_backends refresh. The widgets_json payload replaces the "
                 f"served file, so include existing `{seeded_id}` and add {brief}."),
                (f"Refresh \"{desk['backend']}\" ({desk['url']}) with widgets_json "
                 f"containing both the served `{seeded_id}` and this new entry - "
                 f"{brief}."),
            ]),
            "fixtures": {},
            "initial_state": c.seeded_custom(desk["backend"], desk["url"],
                                             initial_widgets),
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.widget_def_checks(desk["backend"], added_id, added),
                    c.widget_def_anchor_checks(desk["backend"], seeded_id, seeded),
                ],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.snap(),
                c.refresh_call("backend_001", widgets=final_widgets),
            ],
        })

    # ------------------------------------------------------------------ t1
    # Seed widgets and a one-tab app. Add a briefed widget and update the app
    # placement in the same refresh.
    t1_specs = [
        ("vol", ["vix_history"], "Vol Review", "Vol history and regime.",
         "overview", "Overview", [("vix_history", 0, 0, 20, 9)],
         "vol_regime_metric", (20, 0, 8, 5)),
        ("rates", ["auction_calendar"], "Auction Review",
         "Auctions and curve posture.", "auctions", "Auctions",
         [("auction_calendar", 0, 0, 20, 9)],
         "curve_spread_metric", (20, 0, 8, 5)),
        ("sla", ["vendor_sla_table"], "Vendor Review",
         "Vendor status and breach count.", "vendors", "Vendors",
         [("vendor_sla_table", 0, 0, 20, 9)],
         "breach_metric", (20, 0, 8, 5)),
        ("compliance", ["alert_queue"], "Alert Review",
         "Alert queue and open-alert posture.", "alerts", "Alerts",
         [("alert_queue", 0, 0, 24, 10)],
         "alert_metric", (24, 0, 8, 5)),
    ]
    for (
        desk_key, seeded_ids, app_name, app_desc, tab_id, tab_name,
        initial_items, added_id, added_pos,
    ) in t1_specs:
        desk = c.desk(desk_key)
        seeded_widgets = {wid: c.desk_widget(desk_key, wid) for wid in seeded_ids}
        added = c.desk_widget(desk_key, added_id)
        initial_app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [
                c.layout_item(wid, x, y, w, h)
                for wid, x, y, w, h in initial_items
            ]),
        ])
        ax, ay, aw, ah = added_pos
        updated_items = initial_items + [(added_id, ax, ay, aw, ah)]
        updated_app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [
                c.layout_item(wid, x, y, w, h)
                for wid, x, y, w, h in updated_items
            ]),
        ])
        final_widgets = dict(seeded_widgets)
        final_widgets[added_id] = added
        sid = f"auth_t1_extend_place_{added_id}"
        brief = c.widget_requirements_text(added_id, added)
        edit_words = (
            f"keep app \"{app_name}\" on tab `{tab_id}` named \"{tab_name}\" and "
            f"add `{added_id}` at x={ax} y={ay} w={aw} h={ah}; preserve the "
            "existing placement"
        )
        c.add("extend", "t1", {
            "id": sid,
            "title": f"Add {added['name']} to {app_name}",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "refresh",
                      "extend"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace. \"{desk['backend']}\" already serves "
                 f"{', '.join(f'`{w}`' for w in seeded_ids)} and app "
                 f"\"{app_name}\". Refresh both files: widgets_json must keep the "
                 f"served widgets and add {brief}. apps_json must {edit_words}."),
                (f"Use manage_backends refresh on \"{desk['backend']}\". Because "
                 f"widgets_json replaces the file, include "
                 f"{', '.join(f'`{w}`' for w in seeded_ids)} plus {brief}. Also "
                 f"refresh apps_json so it will {edit_words}."),
                (f"Extend the connected backend \"{desk['backend']}\" at "
                 f"{desk['url']}: add widget {brief}, keep the existing widgets, "
                 f"and edit apps.json to {edit_words}."),
            ]),
            "fixtures": {},
            "initial_state": c.seeded_custom(desk["backend"], desk["url"],
                                             seeded_widgets, apps=[initial_app]),
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.widget_def_anchor_checks(desk["backend"], added_id, added)
                ],
                "required_app_defs": [c.app_def_checks(desk["backend"], updated_app)],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.snap(),
                c.refresh_call("backend_001", widgets=final_widgets,
                               apps=[updated_app]),
            ],
        })

    # ------------------------------------------------------------------ t2
    # Words-only modifications over served state; each cell applies a policy
    # config change and fixes a bad parameter type while preserving a sibling.
    t2_specs = [
        ("vol", "vol_screener",
         {"staleTime": 600000, "category": "Volatility"},
         "vol_regime_metric",
         "the Vol Screener caches results for 10 minutes and is categorized as "
         "Volatility",
         "ticker", "dropdownz",
         "its ticker parameter must be restored to type ticker"),
        ("rates", "rates_commentary",
         {"refetchInterval": 30000, "runButton": True}, "curve_spread_metric",
         "Rates Commentary auto-refreshes every 30 seconds and exposes a run button",
         "series", "dropdownz",
         "its series parameter must be an endpoint dropdown backed by "
         "/series-options"),
        ("compliance", "case_notes",
         {"staleTime": 600000, "category": "Surveillance"}, "alert_metric",
         "Case Notes cache results for 10 minutes and are categorized as Surveillance",
         "case_id", "dropdownz",
         "its case_id parameter must be restored to a text input"),
        ("healthcare", "trial_catalysts",
         {"staleTime": 600000},
         "catalyst_metric",
         "Trial Catalysts cache results for 10 minutes",
         "ticker", "dropdownz",
         "its ticker parameter must be an endpoint dropdown backed by /tickers"),
    ]
    for (
        desk_key, modified_id, config, sibling_id, change_words,
        param_name, bad_type, param_fix_words,
    ) in t2_specs:
        desk = c.desk(desk_key)
        original = c.desk_widget(desk_key, modified_id)
        broken = _mutate_param_type(original, param_name, bad_type)
        modified = _with_config(original, **config)
        sibling = c.desk_widget(desk_key, sibling_id)
        initial_widgets = {modified_id: broken, sibling_id: sibling}
        final_widgets = {modified_id: modified, sibling_id: sibling}
        sid = f"auth_t2_extend_modify_{modified_id}"
        req = _policy_requirements(modified_id, modified)
        c.add("extend", "t2", {
            "id": sid,
            "title": f"Modify {modified['name']} without dropping siblings",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "refresh", "extend",
                      "composed"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace. The connected backend \"{desk['backend']}\" "
                 f"already serves `{modified_id}` and `{sibling_id}`. Refresh "
                 f"widgets_json to preserve everything except these two stated "
                 f"changes: {change_words}; and {param_fix_words}. The resulting "
                 f"`{modified_id}` should read: {req}."),
                (f"Use a manage_backends refresh for \"{desk['backend']}\". "
                 f"widgets_json replaces all served widgets, so carry `{sibling_id}` "
                 f"unchanged and update `{modified_id}` so {change_words}; also "
                 f"{param_fix_words}. Requirements for the changed widget: {req}."),
                (f"Modify one served widget on \"{desk['backend']}\" at "
                 f"{desk['url']}: `{modified_id}` must now satisfy {req}; this "
                 f"means {param_fix_words}. Keep `{sibling_id}` exactly as served "
                 "and refresh widgets_json."),
            ]),
            "fixtures": {},
            "initial_state": c.seeded_custom(desk["backend"], desk["url"],
                                             initial_widgets),
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.widget_def_checks(desk["backend"], modified_id, modified),
                    c.widget_def_anchor_checks(desk["backend"], sibling_id, sibling),
                ],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.snap(),
                c.refresh_call("backend_001", widgets=final_widgets),
            ],
        })

    # ------------------------------------------------------------------ t3
    # Diagnosis scans: broken seed carries only a count badge; prompts state the
    # conventions, then the refresh fixes flagged entries and adds one widget.
    t3_specs = []

    hc_trial = c.desk_widget("healthcare", "trial_catalysts")
    hc_vega = c.desk_widget("healthcare", "pipeline_vegalite")
    hc_news = _with_config(c.desk_widget("healthcare", "fda_newsfeed"),
                           staleTime=900000)
    hc_add = c.desk_widget("healthcare", "catalyst_metric")
    t3_specs.append((
        "healthcare",
        {
            "trial_catalysts": _drop_header(hc_trial, "readout_date"),
            "pipeline_vegalite": _mutate_type(hc_vega, "chart-vega"),
            "fda_newsfeed": _mutate_stale(hc_news, 500),
        },
        {
            "trial_catalysts": hc_trial,
            "pipeline_vegalite": hc_vega,
            "fda_newsfeed": hc_news,
            "catalyst_metric": hc_add,
        },
        [
            _anchor_with_patch(
                c.desk("healthcare")["backend"], "trial_catalysts", hc_trial,
                {"columns_include": [{"field": "readout_date",
                                      "headerName": "Readout"}]},
            ),
            _anchor_with_patch(
                c.desk("healthcare")["backend"], "pipeline_vegalite", hc_vega,
                {"expect": {"type": "chart-vegalite"}},
            ),
            _anchor_with_patch(
                c.desk("healthcare")["backend"], "fda_newsfeed", hc_news,
                {"expect": {"staleTime": 900000}},
            ),
            c.widget_def_checks(c.desk("healthcare")["backend"],
                                "catalyst_metric", hc_add),
        ],
        "Healthcare conventions: Vega-Lite pipeline widgets use the "
        "chart-vegalite type; clinical readout date columns display as Readout; "
        "cached healthcare feeds cache for 15 minutes. " + c.CONFIG_RULES,
        "catalyst_metric",
    ))

    er_est = c.desk_widget("earnings", "estimate_revisions")
    er_chart = c.desk_widget("earnings", "earnings_chart")
    er_metric = c.desk_widget("earnings", "surprise_metric")
    er_add = c.desk_widget("earnings", "earnings_note")
    t3_specs.append((
        "earnings",
        {
            "estimate_revisions": _mutate_param_type(er_est, "symbol", "dropdownz"),
            "earnings_chart": _mutate_grid_w(er_chart, 99),
            "surprise_metric": _mutate_grid_w(er_metric, 99),
        },
        {
            "estimate_revisions": er_est,
            "earnings_chart": er_chart,
            "surprise_metric": er_metric,
            "earnings_note": er_add,
        },
        [
            _anchor_with_patch(
                c.desk("earnings")["backend"], "estimate_revisions", er_est,
                {"params_include": [{"paramName": "symbol", "type": "endpoint",
                                     "optionsEndpoint": "/symbols"}]},
            ),
            _anchor_with_patch(
                c.desk("earnings")["backend"], "earnings_chart", er_chart,
                {"expect": {"gridData.w": 20}},
            ),
            _anchor_with_patch(
                c.desk("earnings")["backend"], "surprise_metric", er_metric,
                {"expect": {"gridData.w": 6}},
            ),
            c.widget_def_checks(c.desk("earnings")["backend"],
                                "earnings_note", er_add),
        ],
        "Earnings conventions: symbol controls are endpoint params using "
        "/symbols; history charts use the standard 20-column chart width; "
        "single-value metric tiles use compact width 6.",
        "earnings_note",
    ))

    rates_auc = c.desk_widget("rates", "auction_calendar")
    rates_comment = c.desk_widget("rates", "rates_commentary")
    rates_metric = c.desk_widget("rates", "curve_spread_metric")
    rates_add = c.desk_widget("rates", "yield_curve")
    t3_specs.append((
        "rates",
        {
            "auction_calendar": _drop_header(rates_auc, "date"),
            "rates_commentary": _mutate_param_type(
                rates_comment, "series", "dropdownz"
            ),
            "curve_spread_metric": _mutate_grid_w(rates_metric, 99),
        },
        {
            "auction_calendar": rates_auc,
            "rates_commentary": rates_comment,
            "curve_spread_metric": rates_metric,
            "yield_curve": rates_add,
        },
        [
            _anchor_with_patch(
                c.desk("rates")["backend"], "auction_calendar", rates_auc,
                {"columns_include": [{"field": "date", "headerName": "Date"}]},
            ),
            _anchor_with_patch(
                c.desk("rates")["backend"], "rates_commentary", rates_comment,
                {"params_include": [{"paramName": "series", "type": "endpoint",
                                     "optionsEndpoint": "/series-options"}]},
            ),
            _anchor_with_patch(
                c.desk("rates")["backend"], "curve_spread_metric", rates_metric,
                {"expect": {"gridData.w": 6}},
            ),
            c.widget_def_checks(c.desk("rates")["backend"],
                                "yield_curve", rates_add),
        ],
        "Rates conventions: Auction Calendar keeps Date as the date header; "
        "Rates Commentary series is an endpoint param from /series-options; "
        "single-value spread metric tiles use compact width 6.",
        "yield_curve",
    ))

    sla_table = _with_config(c.desk_widget("sla", "vendor_sla_table"),
                             staleTime=600000)
    sla_metric = c.desk_widget("sla", "breach_metric")
    sla_feed = c.desk_widget("sla", "sla_newsfeed")
    sla_add = c.desk_widget("sla", "sla_runbook")
    t3_specs.append((
        "sla",
        {
            "vendor_sla_table": _mutate_stale(sla_table, 500),
            "breach_metric": _mutate_grid_w(sla_metric, 99),
            "sla_newsfeed": _mutate_type(sla_feed, "feedz"),
        },
        {
            "vendor_sla_table": sla_table,
            "breach_metric": sla_metric,
            "sla_newsfeed": sla_feed,
            "sla_runbook": sla_add,
        },
        [
            _anchor_with_patch(
                c.desk("sla")["backend"], "vendor_sla_table", sla_table,
                {"expect": {"staleTime": 600000}},
            ),
            _anchor_with_patch(
                c.desk("sla")["backend"], "breach_metric", sla_metric,
                {"expect": {"gridData.w": 6}},
            ),
            _anchor_with_patch(
                c.desk("sla")["backend"], "sla_newsfeed", sla_feed,
                {"expect": {"type": "newsfeed"}},
            ),
            c.widget_def_checks(c.desk("sla")["backend"],
                                "sla_runbook", sla_add),
        ],
        "Vendor conventions: SLA status tables cache for 10 minutes; "
        "single-value breach metrics use compact width 6; incident notice "
        "streams are newsfeed widgets. " + c.CONFIG_RULES,
        "sla_runbook",
    ))

    for desk_key, broken_widgets, final_widgets, checks, conventions, added_id in t3_specs:
        desk = c.desk(desk_key)
        added = final_widgets[added_id]
        sid = f"auth_t3_extend_diagnose_{desk_key}"
        add_brief = c.widget_requirements_text(added_id, added)
        c.add("extend", "t3", {
            "id": sid,
            "title": f"Diagnose and extend {desk['backend']}",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "refresh", "extend",
                      "diagnosis"],
            "prompt": c.phrased(sid, [
                (f"The connected backend \"{desk['backend']}\" shows only a "
                 "validation badge in the snapshot, with a count of affected "
                 f"entries. Scan the served widgets against these desk "
                 f"conventions: {conventions} Fix every flagged entry, preserve "
                 f"healthy entries, and ship the queued addition in the same "
                 f"widgets_json refresh: {add_brief}."),
                (f"Use manage_backends refresh for \"{desk['backend']}\". The "
                 "snapshot's warning badge names no fields, so compare the served "
                 f"payload to the conventions: {conventions} Then fix the bad "
                 f"entries, keep compliant widgets, and add {add_brief}."),
                (f"Diagnose \"{desk['backend']}\" from its served payload and "
                 f"count-only warning badge. Conventions: {conventions} Refresh "
                 f"widgets_json with all widgets preserved or repaired, plus the "
                 f"queued widget {add_brief}."),
            ]),
            "fixtures": {},
            "initial_state": _seed_with_warnings(desk["backend"], desk["url"],
                                                 broken_widgets),
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": checks,
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.snap(),
                c.refresh_call("backend_001", widgets=final_widgets),
            ],
        })

    # ------------------------------------------------------------------ t4
    # Diagnose, repair, extend the served app, instantiate, configure, and document.
    t4_specs = []

    vol_focus = c.desk_widget("vol", "vix_advanced")
    vol_add = _with_config(
        c.desk_widget("vol", "vol_regime_metric"),
        params=[c.text_param("symbol", "Symbol", "VIX", "Volatility symbol.")],
    )
    t4_specs.append((
        "vol", "vix_advanced", _mutate_grid_w(vol_focus, 99), vol_focus,
        "vol_regime_metric", vol_add,
        {"expect": {"gridData.w": 20}},
        "VIX Advanced Chart uses grid width 20.",
        ("Vol Repair Live", "VIX chart and regime.", "vol", "Vol"),
        "vol regime",
        (c.text_param("symbol", "Symbol", "VX1",
                      "Advanced chart symbol."),
         "symbol", "VX2"),
    ))

    rates_focus = c.desk_widget("rates", "rates_commentary")
    rates_add2 = _with_config(
        c.desk_widget("rates", "curve_spread_metric"),
        params=[c.endpoint_param("series", "Series", "DGS10", "/series-options")],
    )
    t4_specs.append((
        "rates", "rates_commentary",
        _mutate_param_type(rates_focus, "series", "dropdownz"), rates_focus,
        "curve_spread_metric", rates_add2,
        {"params_include": [{"paramName": "series", "type": "endpoint",
                             "optionsEndpoint": "/series-options"}]},
        "Rates Commentary series is an endpoint param backed by /series-options.",
        ("Rates Repair Live", "Rates commentary and curve spread.",
         "rates", "Rates"),
        "rates repair",
        (None, "series", "DGS2"),
    ))

    comp_focus = c.desk_widget("compliance", "case_qa_omni")
    comp_add = _with_config(
        c.desk_widget("compliance", "alert_metric"),
        params=[c.dropdown_param(
            "severity", "Severity", "high",
            [("High", "high"), ("Medium", "medium"), ("Low", "low")],
        )],
    )
    t4_specs.append((
        "compliance", "case_qa_omni",
        _mutate_param_type(comp_focus, "prompt", "dropdownz"), comp_focus,
        "alert_metric", comp_add,
        {"params_include": [{"paramName": "prompt", "type": "text",
                             "show": False}]},
        "Case Q&A keeps a hidden text prompt param.",
        ("Case Repair Live", "Case Q&A and alert posture.", "qa", "Q&A"),
        "case repair",
        (None, "prompt", "Show high severity cases"),
    ))

    exec_focus = c.desk_widget("execution", "live_orders_grid")
    exec_add = _with_config(
        c.desk_widget("execution", "exception_metric"),
        params=[c.text_param("venue", "Venue", "ARCA", "Execution venue.")],
    )
    t4_specs.append((
        "execution", "live_orders_grid",
        _drop_header(exec_focus, "order_id"), exec_focus,
        "exception_metric", exec_add,
        {"columns_include": [{"field": "order_id", "headerName": "Order"}]},
        "Live Orders Grid keeps Order as the order_id header.",
        ("Execution Repair Live", "Live orders and exceptions.",
         "orders", "Orders"),
        "execution repair",
        (c.text_param("venue", "Venue", "ARCA",
                      "Execution venue filter."),
         "venue", "EDGX"),
    ))

    for (
        desk_key, focus_id, broken_focus, fixed_focus, added_id, added,
        patch, convention, app_spec, note_term, configure,
    ) in t4_specs:
        desk = c.desk(desk_key)
        fixed_focus = _copy(fixed_focus)
        config_param, param_name, set_value = configure
        if config_param is not None:
            fixed_focus.setdefault("params", []).append(_copy(config_param))
            patch = _copy(patch)
            patch["params_include"] = [
                {"paramName": param_name, "type": config_param.get("type", "text")}
            ]
            convention = (
                f"{convention} The repaired `{focus_id}` also takes "
                f"{c.param_requirement(config_param)}."
            )
        app_name, app_desc, tab_id, tab_name = app_spec
        initial_app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(focus_id, 0, 0, 20, 9)]),
        ])
        updated_app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(focus_id, 0, 0, 20, 9)]),
            ("posture", "Posture", [c.layout_item(added_id, 0, 0, 8, 5)]),
        ])
        broken_widgets = {focus_id: broken_focus}
        final_widgets = {focus_id: fixed_focus, added_id: added}
        dashboard_name = f"{app_name} Dashboard"
        note_text = f"{app_name} is live from {desk['backend']}: {note_term} done."
        sid = f"auth_t4_extend_repair_{desk_key}"
        add_words = c.widget_requirements_text(added_id, added)
        configure_words = (
            f"set {param_name} to {json.dumps(set_value)} on the opened "
            f"`{focus_id}` widget"
        )
        c.add("extend", "t4", {
            "id": sid,
            "title": f"Repair, extend, open, and configure {app_name}",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "refresh",
                      "extend", "orchestration"],
            "prompt": c.phrased(sid, [
                (f"End to end on the connected backend \"{desk['backend']}\". "
                 "The snapshot shows a count-only validation badge. Desk "
                 f"convention: {convention} Refresh widgets_json to repair "
                 f"`{focus_id}`, preserve it, and add {add_words}. Refresh "
                 f"apps_json so app \"{app_name}\" keeps `{focus_id}` on tab "
                 f"`{tab_id}` and places `{added_id}` on a second tab `posture` "
                 "named \"Posture\". Then instantiate "
                 f"\"{app_name}\" into dashboard \"{dashboard_name}\", "
                 f"{configure_words}, and leave "
                 f"a note titled \"{app_name}\" that says exactly: "
                 f"\"{note_text}\""),
                (f"Diagnose and ship \"{desk['backend']}\". The warning badge "
                 f"does not name fields; apply this convention: {convention} "
                 f"Refresh widgets_json with fixed `{focus_id}` plus {add_words}, "
                 f"refresh the served app \"{app_name}\" to include `{added_id}` "
                 "on a second `posture` tab, open it as "
                 f"\"{dashboard_name}\", {configure_words}, and add note \"{app_name}\" saying "
                 f"\"{note_text}\"."),
                (f"Repair, extend, open, configure, document. For \"{desk['backend']}\" at "
                 f"{desk['url']}, use the count-only badge and convention "
                 f"{convention} to fix `{focus_id}`. Add {add_words}, update "
                 f"\"{app_name}\" so `{focus_id}` stays on `{tab_id}` and "
                 f"`{added_id}` moves to a new `posture` tab, instantiate into "
                 f"\"{dashboard_name}\", {configure_words}, and create note \"{app_name}\" with text "
                 f"\"{note_text}\"."),
            ]),
            "fixtures": {},
            "initial_state": _seed_with_warnings(
                desk["backend"], desk["url"], broken_widgets, apps=[initial_app],
            ),
            "allowed_tools": c.APP_TOOLS + ["add_generative_widget",
                                              "update_widget"],
            "success": {
                "required_widget_defs": [
                    _anchor_with_patch(desk["backend"], focus_id, fixed_focus, patch),
                    c.widget_def_checks(desk["backend"], added_id, added),
                ],
                "required_app_defs": [c.app_def_checks(desk["backend"], updated_app)],
                "required_widgets": [
                    {"origin": desk["backend"], "widget_id": focus_id,
                     "data_args": {param_name: set_value}, "min_count": 1},
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
                c.snap(),
                c.refresh_call("backend_001", widgets=final_widgets,
                               apps=[updated_app]),
                c.instantiate_call("backend_001", app_name, dashboard_name),
                {"tool": "update_widget",
                 "args": {"widget_id": focus_id,
                          "data_args": {param_name: set_value}}},
                {"tool": "add_generative_widget",
                 "args": {"widget_type": "note", "name": app_name,
                          "data": note_text}},
            ],
        })
