"""Family PARAMS - input parameter building (onboarding tab: Input Params)."""

from __future__ import annotations

import json

from . import common as c


def _ticker_param(name: str = "symbol", label: str = "Symbol", value: str = "AAPL") -> dict:
    return {"paramName": name, "type": "ticker", "label": label, "value": value}


def _tabs_param(name: str = "view", value: str = "growth") -> dict:
    return {
        "paramName": name, "type": "tabs", "label": "View", "value": value,
        "options": [
            {"label": "Growth", "value": "growth"},
            {"label": "Margins", "value": "margins"},
        ],
    }


def _with_params(definition: dict, params: list[dict]) -> dict:
    definition["params"] = params
    return definition


def _without_time_config(definition: dict) -> dict:
    copied = json.loads(json.dumps(definition))
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
    # Exact widgets.json briefs, one single-param widget per task.
    t0_specs = [
        ("vol", "vix_history", ["window"]),
        ("healthcare", "trial_catalysts", ["ticker"]),
        ("compliance", "case_notes", ["case_id"]),
        ("earnings", "kpi_tabs_table", ["view"]),
    ]
    for desk_key, widget_id, keep_params in t0_specs:
        desk = c.desk(desk_key)
        definition = c.desk_widget(desk_key, widget_id)
        keep = set(keep_params)
        definition["params"] = [
            param for param in definition.get("params", [])
            if param.get("paramName") in keep
        ]
        sid = f"auth_t0_params_{widget_id}"
        brief = c.widget_requirements_text(widget_id, definition)
        c.add("params", "t0", {
            "id": sid,
            "title": f"Build the {definition['name']} parameter widget",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "params"],
            "prompt": c.phrased(sid, [
                (f"Connect a new custom backend named \"{desk['backend']}\" at "
                 f"{desk['url']}. Its widgets.json serves exactly one widget - "
                 f"{brief}. Register it with manage_backends."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) with one "
                 f"param-bearing widgets.json entry: {brief}."),
                (f"Add the custom backend \"{desk['backend']}\" at {desk['url']} "
                 f"serving this single widget definition: {brief}."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.widget_def_checks(desk["backend"], widget_id, definition)
                ],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.add_backend_call(desk["backend"], desk["url"], {widget_id: definition}),
            ],
        })

    # ------------------------------------------------------------------ t1
    # Param-carrying widget plus a one-tab app wrapper, from scratch.
    t1_specs = [
        ("healthcare", "trial_catalysts", "Catalyst Filter",
         "Ticker-filtered trial catalysts.", "catalysts", "Catalysts",
         (0, 0, 20, 9)),
        ("rates", "rates_commentary", "Series Commentary",
         "Rates commentary by selected series.", "commentary", "Commentary",
         (0, 0, 12, 8)),
        ("sla", "vendor_sla_table", "Vendor Filter Board",
         "Status-filtered vendor SLA table.", "vendors", "Vendors",
         (0, 0, 20, 9)),
        ("compliance", "case_notes", "Case Note Filter",
         "Case notes by entered case id.", "notes", "Notes",
         (0, 0, 12, 8)),
    ]
    for desk_key, widget_id, app_name, app_desc, tab_id, tab_name, pos in t1_specs:
        desk = c.desk(desk_key)
        definition = c.desk_widget(desk_key, widget_id)
        x, y, w, h = pos
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(widget_id, x, y, w, h)]),
        ])
        sid = f"auth_t1_params_{widget_id}_app"
        brief = c.widget_requirements_text(widget_id, definition)
        wrap = (
            f"an app named \"{app_name}\" (description \"{app_desc}\") with one "
            f"tab `{tab_id}` named \"{tab_name}\" placing `{widget_id}` at "
            f"x={x} y={y} w={w} h={h}"
        )
        c.add("params", "t1", {
            "id": sid,
            "title": f"Ship {definition['name']} as the {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "params"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']}. widgets.json serves one widget - {brief}. "
                 f"apps.json ships {wrap}. Publish both in one manage_backends add."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) with {brief}, "
                 f"and include apps.json shipping it as {wrap}."),
                (f"Build widgets.json ({brief}) and apps.json ({wrap}) for "
                 f"\"{desk['backend']}\" at {desk['url']}; add them together."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.widget_def_checks(desk["backend"], widget_id, definition)
                ],
                "required_app_defs": [c.app_def_checks(desk["backend"], app)],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.snap(),
                c.add_backend_call(desk["backend"], desk["url"],
                                   {widget_id: definition}, apps=[app]),
            ],
        })

    # ------------------------------------------------------------------ t2
    # Words-only composed widget requirements: params plus one config dimension.
    t2_specs = [
        ("vol", "vol_screener",
         c.simple_def(
             "table", "Vol Screener",
             "Screen names by implied-vol criteria.",
             "/vol-screener", grid=(24, 10),
             params=[
                 _ticker_param("ticker", "Ticker", "AAPL"),
                 c.date_param("as_of", "As of"),
                 c.boolean_param("only_liquid", "Liquid only", True),
             ],
             staleTime=600000,
             category="Volatility",
         )),
        ("rates", "series_markdown",
         c.simple_def(
             "markdown", "Series Markdown",
             "Rates note for the selected time series.",
             "/series-markdown", grid=(12, 8),
             params=[c.endpoint_param("series", "Series", "DGS10", "/series-options")],
             runButton=True, staleTime=900000,
         )),
        ("earnings", "kpi_param_tabs",
         c.simple_def(
             "table", "KPI Param Tabs",
             "KPI table switched between growth and margin views.",
             "/kpi-param-tabs", grid=(24, 10),
             params=[_tabs_param()],
             refetchInterval=60000, category="Earnings",
         )),
        ("vol", "windowed_vix_slice",
         c.simple_def(
             "chart", "Windowed VIX Slice",
             "VIX chart for a selected window and as-of date.",
             "/windowed-vix", grid=(20, 9), raw=True,
             params=[
                 c.number_param("window", "Window", 30, minimum=5, maximum=365),
                 c.date_param("as_of", "As of", "$currentDate-1d"),
             ],
             staleTime=600000,
         )),
    ]
    for desk_key, widget_id, definition in t2_specs:
        desk = c.desk(desk_key)
        words = _policy_requirements(widget_id, definition)
        sid = f"auth_t2_params_{widget_id}"
        c.add("params", "t2", {
            "id": sid,
            "title": f"Compose the {definition['name']} parameter widget",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "params", "composed"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']} with one widgets.json entry. Requirements: {words}. "
                 "Build the definition from those words and add the backend."),
                (f"Build one parameterized widget for \"{desk['backend']}\" "
                 f"({desk['url']}): {words}. Submit it with manage_backends add."),
                (f"Publish \"{desk['backend']}\" at {desk['url']} serving a single "
                 f"widgets.json entry with these requirements: {words}."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.widget_def_checks(desk["backend"], widget_id, definition)
                ],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.snap(),
                c.add_backend_call(desk["backend"], desk["url"], {widget_id: definition}),
            ],
        })

    # ------------------------------------------------------------------ t3
    # Multi-widget apps with param-carrying siblings. Shared params are stated once.
    t3_specs = [
        ("earnings",
         ["estimate_revisions", "earnings_chart"],
         ("Earnings Param Review", "Symbol-linked revisions and EPS history.",
          [("revisions", "Revisions", [("estimate_revisions", 0, 0, 20, 9)]),
           ("history", "History", [("earnings_chart", 0, 0, 20, 9)])]),
         "symbol"),
        ("healthcare",
         ["trial_catalysts", "pipeline_chart"],
         ("Trial Param Review", "Ticker-filtered catalysts and pipeline mix.",
          [("catalysts", "Catalysts", [("trial_catalysts", 0, 0, 20, 9)]),
           ("pipeline", "Pipeline", [("pipeline_chart", 0, 0, 20, 9)])]),
         "ticker"),
        ("vol",
         ["vol_screener", "vix_history", "vol_commentary"],
         ("Vol Param Cockpit", "Screen, history, and commentary filters.",
          [("screen", "Screen", [("vol_screener", 0, 0, 24, 10),
                                  ("vol_commentary", 24, 0, 12, 8)]),
           ("history", "History", [("vix_history", 0, 0, 20, 9)])]),
         None),
        ("earnings",
         ["earnings_note", "estimate_revisions", "earnings_chart"],
         ("Symbol Param Desk", "Shared-symbol earnings review.",
          [("review", "Review", [("earnings_note", 0, 0, 12, 8),
                                  ("estimate_revisions", 12, 0, 20, 9)]),
           ("price", "Price", [("earnings_chart", 0, 0, 20, 9)])]),
         "symbol"),
    ]
    for desk_key, widget_ids, app_spec, shared_param_name in t3_specs:
        desk = c.desk(desk_key)
        widgets = {wid: c.desk_widget(desk_key, wid) for wid in widget_ids}
        if desk_key == "healthcare":
            shared = c.endpoint_param("ticker", "Ticker", "PFE", "/tickers")
            widgets["pipeline_chart"] = _with_params(widgets["pipeline_chart"], [shared])
        app_name, app_desc, tab_specs = app_spec
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name,
             [c.layout_item(wid, x, y, w, h) for wid, x, y, w, h in items])
            for tab_id, tab_name, items in tab_specs
        ])
        focus_id = widget_ids[0]
        omit = {shared_param_name} if shared_param_name else set()
        widget_words = []
        for wid in widget_ids:
            widget_words.append(c.widget_requirements_text(wid, widgets[wid], omit_params=omit))
        if shared_param_name:
            shared_param = next(
                param for param in widgets[focus_id].get("params", [])
                if param["paramName"] == shared_param_name
            )
            widget_words.append(c.shared_param_note(shared_param, widget_ids))
        widget_surface = "; ".join(widget_words)
        if not shared_param_name:
            convention = c.stamp_consistency(widgets)
            widget_surface += f". Desk convention: {convention}"
        app_words = c.app_requirements_text(app)
        sid = f"auth_t3_params_{app_name.lower().replace(' ', '_')}"
        c.add("params", "t3", {
            "id": sid,
            "title": f"Assemble the {app_name} app with shared parameters",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "params", "multi-tab"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then publish \"{desk['backend']}\" at "
                 f"{desk['url']} in one add. widgets.json serves: "
                 f"{widget_surface}. apps.json ships {app_words}."),
                (f"Connect \"{desk['backend']}\" ({desk['url']}) with widgets "
                 f"{widget_surface}. Ship the app too: {app_words}."),
                (f"Build both files for \"{desk['backend']}\" at {desk['url']}. "
                 f"Widgets: {widget_surface}. App: {app_words}. One add."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.widget_def_checks(desk["backend"], focus_id, widgets[focus_id])
                ] + [
                    c.widget_def_anchor_checks(desk["backend"], wid, widgets[wid])
                    for wid in widget_ids[1:]
                ],
                "required_app_defs": [c.app_def_checks(desk["backend"], app)],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.snap(),
                c.add_backend_call(desk["backend"], desk["url"], widgets, apps=[app]),
            ],
        })

    # ------------------------------------------------------------------ t4
    # Build, publish, instantiate, configure, and document a param-aware app.
    t4_specs = [
        ("earnings", "estimate_revisions", ["earnings_chart", "surprise_metric"],
         ("Earnings Symbol Live", "Preset symbol revisions and EPS history.",
          "earnings", "Earnings", {"symbol": "NVDA"}), "symbol sync",
         ("symbol", "MSFT")),
        ("healthcare", "trial_symbol_pack", ["catalyst_metric", "trial_catalysts"],
         ("Trial Symbol Live", "Preset symbol catalyst review.",
          "trials", "Trials", {"symbol": "MRNA"}), "trial symbol",
         ("symbol", "PFE")),
        ("vol", "vol_symbol_pack", ["vol_regime_metric", "vix_history"],
         ("Vol Symbol Live", "Preset symbol volatility review.",
          "vol", "Vol", {"symbol": "MSFT"}), "vol symbol",
         ("symbol", "AAPL")),
        ("rates", "rates_series_pack", ["curve_spread_metric", "rates_commentary"],
         ("Rates Series Live", "Preset rates series commentary.",
          "series", "Series", {"series": "DGS2"}), "series preset",
         ("series", "DGS10")),
    ]
    custom_t4 = {
        "trial_symbol_pack": c.simple_def(
            "table", "Trial Symbol Pack",
            "Trial review filtered by symbol.", "/trial-symbol-pack",
            grid=(20, 9), params=[_ticker_param("symbol", "Symbol", "MRNA")],
        ),
        "vol_symbol_pack": c.simple_def(
            "table", "Vol Symbol Pack",
            "Volatility review filtered by symbol.", "/vol-symbol-pack",
            grid=(20, 9), params=[
                _ticker_param("symbol", "Symbol", "MSFT"),
                c.boolean_param("only_liquid", "Liquid only", True),
            ],
        ),
        "rates_series_pack": c.simple_def(
            "markdown", "Rates Series Pack",
            "Rates commentary filtered by selected series.", "/rates-series-pack",
            grid=(12, 8),
            params=[c.endpoint_param("series", "Series", "DGS2", "/series-options")],
        ),
    }
    for desk_key, focus_id, sibling_ids, app_spec, note_term, configure in t4_specs:
        desk = c.desk(desk_key)
        focus = custom_t4.get(focus_id) or c.desk_widget(desk_key, focus_id)
        widgets = {focus_id: focus}
        for sibling_id in sibling_ids:
            widgets[sibling_id] = c.desk_widget(desk_key, sibling_id)
        sibling_id = sibling_ids[0]
        param_name, set_value = configure
        app_name, app_desc, tab_id, tab_name, preset = app_spec
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [
                c.layout_item(focus_id, 0, 0, 20, 9, params=preset),
            ]),
            ("posture", "Posture", [c.layout_item(sibling_id, 0, 0, 12, 6)]),
        ])
        dashboard_name = f"{app_name} Board"
        note_text = f"{app_name} is live from {desk['backend']}: {note_term} ready."
        convention = c.stamp_consistency(widgets)
        widget_words = "; ".join(
            c.widget_requirements_text(wid, definition)
            for wid, definition in widgets.items()
        )
        widget_words += f". Desk convention: {convention}"
        configure_words = (
            f"set {param_name} to {json.dumps(set_value)} on the opened "
            f"`{focus_id}` widget"
        )
        app_words = c.app_requirements_text(app)
        sid = f"auth_t4_params_{desk_key}_ship"
        c.add("params", "t4", {
            "id": sid,
            "title": f"Ship, open, and configure the {app_name} parameter app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "params", "orchestration"],
            "prompt": c.phrased(sid, [
                (f"End to end. Publish \"{desk['backend']}\" at {desk['url']} - "
                 f"widgets.json: {widget_words}. apps.json: {app_words}. Then "
                 f"instantiate \"{app_name}\" from that backend into a dashboard "
                 f"named \"{dashboard_name}\", {configure_words}, and leave a note titled "
                 f"\"{app_name}\" that says exactly: \"{note_text}\""),
                (f"Build, publish, open, configure, document. \"{desk['backend']}\" "
                 f"({desk['url']}) serves {widget_words} and ships {app_words}. "
                 f"Open it as \"{dashboard_name}\" via manage_apps, "
                 f"{configure_words}, then add a "
                 f"note \"{app_name}\" saying: \"{note_text}\""),
                (f"Four steps: add \"{desk['backend']}\" at {desk['url']} with "
                 f"{widget_words} and {app_words}; instantiate \"{app_name}\" as "
                 f"\"{dashboard_name}\"; {configure_words}; add a note titled \"{app_name}\" with "
                 f"the text \"{note_text}\"."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.APP_TOOLS + ["add_generative_widget",
                                              "update_widget"],
            "success": {
                "required_widget_defs": [
                    c.widget_def_checks(desk["backend"], focus_id, focus),
                ] + [
                    c.widget_def_anchor_checks(desk["backend"], sid, widgets[sid])
                    for sid in sibling_ids
                ],
                "required_app_defs": [c.app_def_anchor_checks(desk["backend"], app)],
                "required_widgets": [
                    {"origin": desk["backend"], "widget_id": focus_id,
                     "data_args": {param_name: set_value}, "min_count": 1},
                ],
                "required_generated_widgets": [{
                    "widget_type": "note",
                    "data_contains": [app_name, note_term],
                    "min_count": 1,
                }],
                "layout": {"within_grid": True, "no_overlaps": True, "grid_width": 40},
                "trace_checks": dict(c.TRACE_T4),
            },
            "oracle_tool_calls": [
                c.add_backend_call(desk["backend"], desk["url"], widgets, apps=[app]),
                c.instantiate_call("backend_001", app_name, dashboard_name),
                {"tool": "update_widget",
                 "args": {"widget_id": focus_id,
                          "data_args": {param_name: set_value}}},
                {"tool": "add_generative_widget",
                 "args": {"widget_type": "note", "name": app_name, "data": note_text}},
            ],
        })
