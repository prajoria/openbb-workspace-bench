"""Family CHARTS — Plotly, Highcharts, and Vega-Lite dialects."""

import json

from . import common as c


def _copy_with(definition: dict, **updates) -> dict:
    copied = json.loads(json.dumps(definition))
    copied.update(updates)
    return copied


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
    # ------------------------------------------------------------------ r0
    # Exact JSON briefs for all chart dialects, plus one extra Plotly chart.
    t0_specs = [
        ("rates", "yield_curve"),
        ("tvl", "chains_highchart"),
        ("healthcare", "pipeline_vegalite"),
        ("earnings", "earnings_chart"),
    ]
    for desk_key, widget_id in t0_specs:
        desk = c.desk(desk_key)
        definition = c.desk_widget(desk_key, widget_id)
        if widget_id == "yield_curve":
            definition["staleTime"] = 900000
        elif widget_id == "chains_highchart":
            definition.update({"staleTime": 900000, "category": "Chain Charts"})
        elif widget_id == "pipeline_vegalite":
            definition.update({"staleTime": 1800000, "category": "Pipeline Charts"})
        elif widget_id == "earnings_chart":
            definition["staleTime"] = 900000
        sid = f"{widget_id}"
        brief = c.widget_requirements_text(widget_id, definition)
        c.add("charts", "r0", {
            "id": sid,
            "title": f"Build the {definition['name']} chart definition",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "charts"],
            "prompt": c.phrased(sid, [
                (f"Connect a new custom backend named \"{desk['backend']}\" at "
                 f"{desk['url']}. Its widgets.json serves exactly one chart "
                 f"widget — {brief}. Register it with manage_backends."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) with one "
                 f"widgets.json chart entry: {brief}. Use one manage_backends add."),
                (f"You wrote a backend at {desk['url']}. Add it as "
                 f"\"{desk['backend']}\" serving this exact chart entry — {brief}."),
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

    # ------------------------------------------------------------------ r1
    # One chart plus a one-tab app wrapper. Widget anchored; app full.
    t1_specs = [
        ("rates", "yield_curve", {}, "Yield Curve App", "Treasury curve chart.",
         "curve", "Curve", (0, 0, 20, 9)),
        ("tvl", "chains_highchart", {}, "Chain Highchart", "Highcharts TVL view.",
         "chains", "Chains", (0, 0, 20, 9)),
        ("healthcare", "pipeline_vegalite",
         {"params": [c.endpoint_param("phase", "Phase", "all", "/phase-options")]},
         "Pipeline Vega App", "Vega-Lite pipeline view.",
         "pipeline", "Pipeline", (0, 0, 20, 9)),
        ("earnings", "earnings_chart", {}, "EPS Chart App", "EPS history chart.",
         "eps", "EPS", (0, 0, 20, 9)),
    ]
    for desk_key, widget_id, updates, app_name, app_desc, tab_id, tab_name, pos in t1_specs:
        desk = c.desk(desk_key)
        definition = _copy_with(c.desk_widget(desk_key, widget_id), **updates)
        x, y, w, h = pos
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(widget_id, x, y, w, h)]),
        ])
        sid = f"{widget_id}_app"
        brief = c.widget_requirements_text(widget_id, definition)
        wrap = (
            f"an app named \"{app_name}\" (description \"{app_desc}\") with a "
            f"single tab `{tab_id}` named \"{tab_name}\" placing `{widget_id}` at "
            f"x={x} y={y} w={w} h={h}"
        )
        c.add("charts", "r1", {
            "id": sid,
            "title": f"Ship {definition['name']} as the {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "charts"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']}. widgets.json serves one chart — {brief}. "
                 f"apps.json ships {wrap}. Publish both in one manage_backends add."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) serving "
                 f"{brief}, shipped as {wrap}. Both files go in the same add."),
                (f"Build widgets.json ({brief}) and apps.json ({wrap}) for "
                 f"\"{desk['backend']}\" at {desk['url']}, then add the backend."),
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

    # ------------------------------------------------------------------ r2
    # Words-only composed chart requirements: dialect + param + config.
    t2_specs = [
        ("earnings", "symbol_momentum_chart",
         c.simple_def(
             "chart", "Symbol Momentum Chart", "Plotly momentum chart by symbol.",
             "/symbol-momentum", grid=(20, 9), raw=True,
             params=[c.endpoint_param("symbol", "Symbol", "AAPL", "/symbols")],
             staleTime=900000,
             category="Earnings",
         )),
        ("tvl", "chain_flow_highchart",
         c.simple_def(
             "chart-highcharts", "Chain Flow Highchart",
             "Highcharts chain flow chart.", "/chain-flow-highchart", grid=(20, 9),
             params=[c.endpoint_param("chain", "Chain", "ethereum",
                                      "/chain-options")],
             staleTime=900000, category="Chain Flows", runButton=True,
         )),
        ("healthcare", "phase_mix_vegalite",
         c.simple_def(
             "chart-vegalite", "Phase Mix Vega-Lite",
             "Vega-Lite phase mix chart.", "/phase-mix-vegalite", grid=(20, 9),
             params=[c.endpoint_param("phase", "Phase", "all", "/phase-options")],
             staleTime=1800000,
             category="Clinical",
         )),
        ("execution", "venue_slippage_chart",
         c.simple_def(
             "chart", "Venue Slippage Chart", "Plotly slippage chart by venue.",
             "/venue-slippage-chart", grid=(20, 9), raw=True,
             params=[c.text_param("venue", "Venue", "ARCA",
                                  "Venue code to chart.")],
             refetchInterval=30000,
             category="Execution",
         )),
    ]
    for desk_key, widget_id, definition in t2_specs:
        desk = c.desk(desk_key)
        sid = f"{widget_id}"
        words = _policy_requirements(widget_id, definition)
        c.add("charts", "r2", {
            "id": sid,
            "title": f"Compose the {definition['name']} chart widget",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "charts", "composed"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']} serving one composed chart widget: {words}. "
                 "Publish it with manage_backends add."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) with exactly "
                 f"one chart entry. Requirements: {words}."),
                (f"Build the widgets.json for \"{desk['backend']}\" at "
                 f"{desk['url']}: {words}. Then add the backend."),
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

    # ------------------------------------------------------------------ r3
    # Chart-led multi-tab apps: chart focus full, table/metric siblings anchor.
    t3_specs = [
        ("rates", "yield_curve", ["curve_spread_metric"],
         ("Rates Chart Room", "Curve chart and spread metric.",
          [("curve", "Curve", [("yield_curve", 0, 0, 20, 9)]),
           ("spread", "Spread", [("curve_spread_metric", 0, 0, 6, 4)])]),
         ("Curve Sync",
          c.text_param("curve_scope", "Curve scope", "UST 2s10s",
                       "Curve segment shared across chart and spread."),
          ["yield_curve", "curve_spread_metric"])),
        ("tvl", "chains_highchart", ["chains_table"],
         ("Chain Chart Room", "Highcharts chain view and TVL table.",
          [("chart", "Chart", [("chains_highchart", 0, 0, 20, 9)]),
           ("table", "Table", [("chains_table", 0, 0, 20, 9)])]),
         ("Chain Sync",
          c.text_param("chain_scope", "Chain scope", "Ethereum",
                       "Chain reviewed across chart and table."),
          ["chains_highchart", "chains_table"])),
        ("healthcare", "pipeline_vegalite", ["trial_catalysts", "catalyst_metric"],
         ("Pipeline Chart Room", "Pipeline chart, trials, and catalyst count.",
          [("pipeline", "Pipeline", [("pipeline_vegalite", 0, 0, 20, 9),
                                        ("catalyst_metric", 20, 0, 6, 4)]),
           ("trials", "Trials", [("trial_catalysts", 0, 0, 20, 9)])]),
         ("Pipeline Sync",
          c.endpoint_param("pipeline_ticker", "Pipeline ticker", "PFE", "/tickers"),
          ["pipeline_vegalite", "trial_catalysts"])),
        ("earnings", "earnings_chart", ["estimate_revisions", "surprise_metric"],
         ("Earnings Chart Room", "EPS chart, revisions, and surprise metric.",
          [("chart", "Chart", [("earnings_chart", 0, 0, 20, 9),
                                  ("surprise_metric", 20, 0, 6, 4)]),
           ("revisions", "Revisions", [("estimate_revisions", 0, 0, 20, 9)])]),
         ("Period Sync",
          c.dropdown_param("period", "Period", "quarterly",
                           [("Quarterly", "quarterly"), ("Annual", "annual")]),
          ["earnings_chart", "estimate_revisions"])),
    ]
    for desk_key, focus_id, sibling_ids, app_spec, shared_spec in t3_specs:
        desk = c.desk(desk_key)
        focus = c.desk_widget(desk_key, focus_id)
        widgets = {focus_id: focus}
        for sibling_id in sibling_ids:
            widgets[sibling_id] = c.desk_widget(desk_key, sibling_id)
        group_name, shared_param, grouped_ids = shared_spec
        for grouped_id in grouped_ids:
            widgets[grouped_id].setdefault("params", []).append(
                json.loads(json.dumps(shared_param))
            )
        app_name, app_desc, tab_specs = app_spec
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name,
             [c.layout_item(wid, x, y, w, h) for wid, x, y, w, h in items])
            for tab_id, tab_name, items in tab_specs
        ], groups=[{"name": group_name, "type": "param",
                    "paramName": shared_param["paramName"],
                    "widgetIds": grouped_ids}])
        omit = {shared_param["paramName"]}
        widget_words = "; ".join(
            c.widget_requirements_text(wid, definition, omit_params=omit)
            for wid, definition in widgets.items()
        )
        widget_words += " " + c.shared_param_note(shared_param, grouped_ids)
        app_words = c.app_requirements_text(app)
        sid = f"{focus_id}_room"
        c.add("charts", "r3", {
            "id": sid,
            "title": f"Assemble the {app_name} chart app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "charts", "multi-tab"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then publish \"{desk['backend']}\" at "
                 f"{desk['url']} in one add. widgets.json serves: {widget_words}. "
                 f"apps.json ships {app_words}."),
                (f"Connect \"{desk['backend']}\" ({desk['url']}) with widgets "
                 f"{widget_words}. Ship the chart-led app too: {app_words}. One "
                 "manage_backends add."),
                (f"Build both files for \"{desk['backend']}\" at {desk['url']}. "
                 f"Widgets: {widget_words}. App: {app_words}. Publish together."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.widget_def_checks(desk["backend"], focus_id, focus)
                ] + [
                    c.widget_def_anchor_checks(desk["backend"], sid, widgets[sid])
                    for sid in sibling_ids
                ],
                "required_app_defs": [c.app_def_checks(desk["backend"], app)],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.snap(),
                c.add_backend_call(desk["backend"], desk["url"], widgets,
                                   apps=[app]),
            ],
        })

    # ------------------------------------------------------------------ r4
    # Chart pack + app + instantiate + configure + note.
    t4_specs = [
        ("rates", "yield_curve", ["curve_spread_metric", "rates_commentary"],
         ("Rates Chart Live", "Yield curve and spread.", "rates", "Rates"),
         "yield curve",
         (c.text_param("curve_view", "Curve View", "2s10s",
                       "Curve segment in focus."),
          "curve_view", "5s30s")),
        ("tvl", "chains_highchart", ["gas_metric", "chains_table"],
         ("Chain Chart Live", "Highcharts chain view and gas.", "chains", "Chains"),
         "chain TVL",
         (c.text_param("chain", "Chain", "Ethereum",
                       "Chain to chart."),
          "chain", "Solana")),
        ("healthcare", "pipeline_vegalite", ["catalyst_metric", "trial_catalysts"],
         ("Pipeline Chart Live", "Vega-Lite pipeline and catalysts.",
          "pipeline", "Pipeline"),
         "pipeline phases",
         (c.text_param("phase", "Phase", "all",
                       "Pipeline phase to chart."),
          "phase", "III")),
        ("earnings", "earnings_chart", ["surprise_metric", "estimate_revisions"],
         ("Earnings Chart Live", "EPS chart and surprise metric.", "earnings", "Earnings"),
         "earnings history",
         (None, "symbol", "MSFT")),
    ]
    for desk_key, focus_id, sibling_ids, app_spec, note_term, configure in t4_specs:
        desk = c.desk(desk_key)
        focus = c.desk_widget(desk_key, focus_id)
        widgets = {focus_id: focus}
        for sibling_id in sibling_ids:
            widgets[sibling_id] = c.desk_widget(desk_key, sibling_id)
        sibling_id = sibling_ids[0]
        new_param, param_name, set_value = configure
        if new_param is not None:
            focus.setdefault("params", []).append(json.loads(json.dumps(new_param)))
        app_name, app_desc, tab_id, tab_name = app_spec
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(focus_id, 0, 0, 20, 9)]),
            ("signals", "Signals", [c.layout_item(sibling_id, 0, 0, 8, 5)]),
        ])
        dashboard_name = f"{app_name} Board"
        note_text = f"{app_name} shipped from {desk['backend']}: {note_term} live."
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
        sid = f"{desk_key}_ship"
        c.add("charts", "r4", {
            "id": sid,
            "title": f"Ship, open, and configure the {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "charts",
                      "orchestration"],
            "prompt": c.phrased(sid, [
                (f"End to end. Publish \"{desk['backend']}\" at {desk['url']} — "
                 f"widgets.json: {widget_words}. apps.json: {app_words}. Then "
                 f"instantiate \"{app_name}\" from that backend into a dashboard "
                 f"named \"{dashboard_name}\", {configure_words}, and leave a note titled "
                 f"\"{app_name}\" that says exactly: \"{note_text}\""),
                (f"Build, publish, open, configure, document. \"{desk['backend']}\" "
                 f"({desk['url']}) serves {widget_words} and ships {app_words}. "
                 f"Open the app as \"{dashboard_name}\" via manage_apps, "
                 f"{configure_words}, then "
                 f"a note \"{app_name}\" saying: \"{note_text}\""),
                (f"Four steps. One: add \"{desk['backend']}\" at {desk['url']} "
                 f"serving {widget_words}, shipping {app_words}. Two: instantiate "
                 f"\"{app_name}\" into \"{dashboard_name}\". Three: "
                 f"{configure_words}. Four: a note titled "
                 f"\"{app_name}\" with the text: \"{note_text}\""),
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
                     "data_args": {param_name: set_value},
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
                c.add_backend_call(desk["backend"], desk["url"], widgets,
                                   apps=[app]),
                c.instantiate_call("backend_001", app_name, dashboard_name),
                {"tool": "update_widget",
                 "args": {"widget_id": focus_id,
                          "data_args": {param_name: set_value}}},
                {"tool": "add_generative_widget",
                 "args": {"widget_type": "note", "name": app_name,
                          "data": note_text}},
            ],
        })
