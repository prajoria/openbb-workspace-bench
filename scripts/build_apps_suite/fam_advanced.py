"""Family ADVANCED - TradingView, live grid, and Omni surfaces."""

from __future__ import annotations

import json

from . import common as c


def _copy(definition: dict) -> dict:
    return json.loads(json.dumps(definition))


def _with_extra(definition: dict, **updates) -> dict:
    copied = _copy(definition)
    copied.update(updates)
    return copied


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


def _widget_checks(backend_name: str, widget_id: str, definition: dict) -> dict:
    """Full widget checks plus the advanced-surface data fields common renders."""

    check = c.widget_def_checks(backend_name, widget_id, definition)
    expect = check.setdefault("expect", {})
    data = definition.get("data") if isinstance(definition.get("data"), dict) else {}
    for key in ("defaultSymbol", "updateFrequency", "wsRowIdColumn"):
        if key in data:
            expect[f"data.{key}"] = data[key]
    if definition.get("type") == "omni":
        enriched = []
        for spec in check.get("params_include", []):
            item = dict(spec)
            if item.get("paramName") == "prompt":
                item["show"] = False
            enriched.append(item)
        if enriched:
            check["params_include"] = enriched
    return check


def _advanced_def(
    name: str,
    description: str,
    endpoint: str,
    symbol: str,
    update_frequency: int,
    grid: tuple[int, int] = (20, 20),
    params: list[dict] | None = None,
    category: str | None = None,
) -> dict:
    definition = c.simple_def(
        "advanced_charting", name, description, endpoint,
        params=params, grid=grid,
        data={"defaultSymbol": symbol, "updateFrequency": update_frequency},
    )
    if category:
        definition["category"] = category
    return definition


def _live_grid_def(
    name: str,
    description: str,
    endpoint: str,
    ws_endpoint: str,
    update_frequency: int | None = None,
    grid: tuple[int, int] = (24, 12),
    refetch_interval=None,
) -> dict:
    definition = _copy(c.desk_widget("execution", "live_orders_grid"))
    definition["name"] = name
    definition["description"] = description
    definition["endpoint"] = endpoint
    definition["wsEndpoint"] = ws_endpoint
    definition["gridData"] = {"w": grid[0], "h": grid[1]}
    definition.setdefault("data", {})["wsRowIdColumn"] = "order_id"
    if update_frequency is not None:
        definition["data"]["updateFrequency"] = update_frequency
    if refetch_interval is not None:
        definition["refetchInterval"] = refetch_interval
    return definition


def _omni_def(
    name: str,
    description: str,
    endpoint: str,
    grid: tuple[int, int] = (20, 9),
    category: str | None = None,
) -> dict:
    definition = _copy(c.desk_widget("compliance", "case_qa_omni"))
    definition["name"] = name
    definition["description"] = description
    definition["endpoint"] = endpoint
    definition["gridData"] = {"w": grid[0], "h": grid[1]}
    if category:
        definition["category"] = category
    return definition


def build() -> None:
    # ------------------------------------------------------------------ t0
    # One exact-JSON widget per owned surface, plus one advanced-chart repeat
    # with a different default symbol.
    t0_specs = [
        ("vol", "vix_advanced", c.desk_widget("vol", "vix_advanced")),
        ("execution", "live_orders_grid", c.desk_widget("execution", "live_orders_grid")),
        ("compliance", "case_qa_omni", c.desk_widget("compliance", "case_qa_omni")),
        ("rates", "rates_advanced_chart",
         _advanced_def(
             "Rates Advanced Chart",
             "TradingView advanced charting for the 10Y yield future.",
             "/rates-udf", "US10Y", 30000, grid=(20, 18),
         )),
    ]
    for desk_key, widget_id, definition in t0_specs:
        desk = c.desk(desk_key)
        definition = _copy(definition)
        sid = f"auth_t0_advanced_{widget_id}"
        brief = c.widget_requirements_text(widget_id, definition)
        c.add("advanced", "t0", {
            "id": sid,
            "title": f"Build the {definition['name']} advanced widget",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "advanced"],
            "prompt": c.phrased(sid, [
                (f"Connect a new custom backend named \"{desk['backend']}\" at "
                 f"{desk['url']}. Its widgets.json serves exactly one widget - "
                 f"{brief}. Register it with manage_backends."),
                (f"Register custom backend \"{desk['backend']}\" ({desk['url']}) "
                 f"with one widgets.json entry: {brief}."),
                (f"Add \"{desk['backend']}\" at {desk['url']} as a custom backend "
                 f"serving this single widget definition - {brief}."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    _widget_checks(desk["backend"], widget_id, definition)
                ],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.add_backend_call(desk["backend"], desk["url"], {widget_id: definition}),
            ],
        })

    # ------------------------------------------------------------------ t1
    # Exact widget brief plus a one-tab app wrapper in words. The last two apps
        # stays at the same widget class plus a one-tab app wrapper.
    t1_specs = [
        ("vol", "vix_advanced", c.desk_widget("vol", "vix_advanced"),
         "Vol Advanced", "TradingView VIX view.", "chart", "Chart",
         (0, 0, 20, 20), None),
        ("execution", "live_orders_grid", c.desk_widget("execution", "live_orders_grid"),
         "Live Order Tape", "Streaming orders for the execution desk.",
         "orders", "Orders", (0, 0, 24, 12), None),
        ("compliance", "case_qa_omni", c.desk_widget("compliance", "case_qa_omni"),
         "Case QA", "Ask over the surveillance corpus.", "qa", "Q&A",
         (0, 0, 20, 9), None),
        ("rates", "rates_advanced_chart",
         _advanced_def(
             "Rates Advanced Chart",
             "TradingView advanced charting for the 10Y yield future.",
             "/rates-udf", "US10Y", 30000, grid=(20, 18),
         ),
         "Rates Advanced", "TradingView rates charting.",
         "rates", "Rates", (0, 0, 20, 18),
         None),
    ]
    for (
        desk_key, widget_id, definition, app_name, app_desc, tab_id, tab_name,
        pos, prompts,
    ) in t1_specs:
        desk = c.desk(desk_key)
        x, y, w, h = pos
        app = c.app_def(
            app_name, app_desc,
            tabs=[(tab_id, tab_name, [c.layout_item(widget_id, x, y, w, h)])],
            prompts=prompts,
        )
        sid = f"auth_t1_advanced_{widget_id}_app"
        brief = c.widget_requirements_text(widget_id, definition)
        wrap = (
            f"an app named \"{app_name}\" (description \"{app_desc}\") with a "
            f"single tab `{tab_id}` named \"{tab_name}\" placing `{widget_id}` at "
            f"x={x} y={y} w={w} h={h}"
        )
        if prompts:
            wrap += "; suggested prompt " + "; ".join(f"\"{p}\"" for p in prompts)
        c.add("advanced", "t1", {
            "id": sid,
            "title": f"Ship {definition['name']} as {app_name}",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "advanced"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']}. Its widgets.json serves one widget - {brief}. "
                 f"Its apps.json ships {wrap}. Publish both in one add."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) serving {brief}, "
                 f"and wrap it as {wrap}. Use one manage_backends add for both "
                 "files."),
                (f"Build widgets.json and apps.json for \"{desk['backend']}\" at "
                 f"{desk['url']}: widget {brief}; app {wrap}. One add call."),
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
    # Words-only composed requirements, focused on type-specific advanced fields.
    t2_specs = [
        ("execution", "orders_stream",
         _with_extra(_live_grid_def(
             "Orders Stream", "Streaming orders with a stable row id.",
             "/orders-stream", "wss://execution.example/orders",
             update_frequency=1000, grid=(24, 10), refetch_interval=False,
         ), params=[c.text_param("venue", "Venue", "ARCA",
                                 "Execution venue filter.")],
             category="Execution", staleTime=900000),
         "stream from the websocket endpoint and do not poll HTTP again — "
         "polling is disabled by setting refetchInterval to false"),
        ("rates", "rates_symbol_chart",
         _with_extra(_advanced_def(
             "Rates Symbol Chart", "TradingView chart with a selectable symbol.",
             "/rates-symbol-udf", "US10Y", 30000, grid=(20, 18),
             params=[c.endpoint_param("symbol", "Symbol", "US10Y", "/rates-symbols")],
             category="Macro",
         ), staleTime=900000),
         "carry the default TradingView symbol and expose the symbol dropdown"),
        ("compliance", "case_prompt_omni",
         _with_extra(_omni_def(
             "Case Prompt Omni", "Hidden-prompt Omni search over case evidence.",
             "/case-prompt-qa", category="Compliance",
         ), staleTime=900000),
         "keep the prompt param hidden and place the widget in the Compliance category"),
        ("vol", "vol_symbol_chart",
         _with_extra(_advanced_def(
             "Vol Symbol Chart", "TradingView chart for volatility futures.",
             "/vol-symbol-udf", "VX1", 15000, grid=(20, 18),
             params=[c.text_param("venue", "Venue", "CFE")],
             category="Volatility",
         ), staleTime=600000),
         "use a faster update frequency and a text venue param"),
    ]
    for desk_key, widget_id, definition, composed_note in t2_specs:
        desk = c.desk(desk_key)
        sid = f"auth_t2_advanced_{widget_id}"
        words = _policy_requirements(widget_id, definition)
        c.add("advanced", "t2", {
            "id": sid,
            "title": f"Compose the {definition['name']} widget",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "advanced", "composed"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']} serving one widgets.json entry. Requirements: "
                 f"{words}. Also, {composed_note}."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) with a single "
                 f"advanced-surface widget. Build it from these requirements, not "
                 f"from copied JSON: {words}. The composed detail is to "
                 f"{composed_note}."),
                (f"Build the widgets.json for \"{desk['backend']}\" at "
                 f"{desk['url']}. One widget only: {words}. Make sure to "
                 f"{composed_note}, then add the backend."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    _widget_checks(desk["backend"], widget_id, definition)
                ],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.snap(),
                c.add_backend_call(desk["backend"], desk["url"], {widget_id: definition}),
            ],
        })

    # ------------------------------------------------------------------ t3
    # Multi-widget advanced rooms: focus full, siblings anchored, app full.
    t3_specs = [
        ("execution", "orders_ops_stream",
         _live_grid_def(
             "Orders Ops Stream", "Streaming order tape for the ops room.",
             "/orders-ops-stream", "wss://execution.example/ops-orders",
             update_frequency=1000, grid=(24, 10), refetch_interval=False,
         ),
         ["exception_metric"],
         ("Execution Stream Room", "Live orders and exception posture.",
          [("stream", "Stream", [("orders_ops_stream", 0, 0, 24, 10)]),
           ("exceptions", "Exceptions", [("exception_metric", 0, 0, 8, 5)])]),
         ("Venue Sync",
          c.text_param("venue_scope", "Venue scope", "ARCA",
                       "Venue reviewed across the stream room."),
          ["orders_ops_stream", "exception_metric"])),
        ("vol", "vix_room_chart", c.desk_widget("vol", "vix_advanced"),
         ["vix_history"],
         ("Vol Chart Room", "TradingView chart and historical context.",
          [("chart", "Chart", [("vix_room_chart", 0, 0, 20, 20)]),
           ("history", "History", [("vix_history", 0, 0, 20, 9)])]),
         ("Window Sync",
          c.number_param("window_days", "Window days", 30, 5, 365),
          ["vix_room_chart", "vix_history"])),
        ("compliance", "case_room_omni",
         _omni_def(
             "Case Room Omni", "Omni search over surveillance cases.",
             "/case-room-qa", category="Compliance",
         ),
         ["alert_queue", "alert_metric"],
         ("Case QA Room", "Case questions, alert queue, and posture.",
          [("qa", "Q&A", [("case_room_omni", 0, 0, 20, 9),
                          ("alert_metric", 20, 0, 8, 5)]),
           ("queue", "Queue", [("alert_queue", 0, 0, 24, 10)])]),
         ("Severity Sync",
          c.dropdown_param("severity_scope", "Severity scope", "high",
                           [("High", "high"), ("Medium", "medium"),
                            ("Low", "low")]),
          ["case_room_omni", "alert_queue"])),
        ("rates", "macro_advanced_chart",
         _advanced_def(
             "Macro Advanced Chart", "TradingView chart for treasury futures.",
             "/macro-udf", "ZN", 30000, grid=(20, 18), category="Macro",
         ),
         ["yield_curve", "curve_spread_metric"],
         ("Macro Chart Room", "TradingView rates chart, curve, and spread.",
          [("chart", "Chart", [("macro_advanced_chart", 0, 0, 20, 18),
                                ("curve_spread_metric", 20, 0, 8, 5)]),
           ("curve", "Curve", [("yield_curve", 0, 0, 20, 9)])]),
         None),
    ]
    for desk_key, focus_id, focus, sibling_ids, app_spec, shared_spec in t3_specs:
        desk = c.desk(desk_key)
        widgets = {focus_id: focus}
        for sibling_id in sibling_ids:
            widgets[sibling_id] = c.desk_widget(desk_key, sibling_id)
        shared_param = grouped_ids = None
        groups = None
        if shared_spec:
            group_name, shared_param, grouped_ids = shared_spec
            for grouped_id in grouped_ids:
                widgets[grouped_id].setdefault("params", []).append(
                    json.loads(json.dumps(shared_param))
                )
            groups = [{"name": group_name, "type": "param",
                       "paramName": shared_param["paramName"],
                       "widgetIds": grouped_ids}]
        app_name, app_desc, tab_specs = app_spec
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name,
             [c.layout_item(wid, x, y, w, h) for wid, x, y, w, h in items])
            for tab_id, tab_name, items in tab_specs
        ], groups=groups)
        omit = {shared_param["paramName"]} if shared_param else set()
        widget_words = "; ".join(
            c.widget_requirements_text(wid, definition, omit_params=omit)
            for wid, definition in widgets.items()
        )
        if shared_param:
            widget_words += " " + c.shared_param_note(shared_param, grouped_ids)
        else:
            convention = c.stamp_consistency(widgets)
            widget_words += f". Desk convention: {convention}"
        app_words = c.app_requirements_text(app)
        sid = f"auth_t3_advanced_{focus_id}_room"
        c.add("advanced", "t3", {
            "id": sid,
            "title": f"Assemble the {app_name}",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "advanced",
                      "multi-tab"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then publish \"{desk['backend']}\" at "
                 f"{desk['url']} in one add. widgets.json serves: {widget_words}. "
                 f"apps.json ships {app_words}."),
                (f"Connect \"{desk['backend']}\" ({desk['url']}) with these "
                 f"advanced room widgets: {widget_words}. Ship the app too - "
                 f"{app_words}. One manage_backends add."),
                (f"Build both files for \"{desk['backend']}\" at {desk['url']}. "
                 f"Widgets: {widget_words}. App: {app_words}. Publish both in "
                 "one add."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    _widget_checks(desk["backend"], focus_id, focus)
                ] + [
                    c.widget_def_anchor_checks(desk["backend"], sibling_id,
                                               widgets[sibling_id])
                    for sibling_id in sibling_ids
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

    # ------------------------------------------------------------------ t4
    # Build, publish, instantiate, configure, and document each advanced surface.
    t4_specs = [
        ("vol", "vix_advanced", c.desk_widget("vol", "vix_advanced"),
         ["vol_regime_metric", "vix_history"],
         ("Vol Advanced Live", "VIX TradingView chart and regime.",
          [("vol", "Vol", [("vix_advanced", 0, 0, 20, 20),
                            ("vol_regime_metric", 20, 0, 8, 5)])]),
         "advanced chart",
         (c.text_param("symbol", "Symbol", "VX1",
                       "Advanced chart symbol."),
          "symbol", "VX2")),
        ("execution", "live_orders_grid",
         _live_grid_def(
             "Live Orders Grid", "Streaming order blotter over websocket.",
             "/live-orders", "live-orders-ws",
         ),
         ["exception_metric", "open_orders"],
         ("Execution Live Grid", "Streaming order grid and exceptions.",
          [("orders", "Orders", [("live_orders_grid", 0, 0, 24, 12),
                                  ("exception_metric", 24, 0, 8, 5)])]),
         "live stream",
         (c.text_param("venue", "Venue", "ARCA",
                       "Execution venue filter."),
          "venue", "EDGX")),
        ("compliance", "case_qa_omni", c.desk_widget("compliance", "case_qa_omni"),
         ["alert_queue", "alert_metric"],
         ("Surveillance QA", "Omni case questions and alerts.",
          [("qa", "Q&A", [("case_qa_omni", 0, 0, 20, 9)]),
           ("alerts", "Alerts", [("alert_queue", 0, 0, 24, 10)])]),
         "case QA",
         (None, "prompt", "Show high severity cases")),
        ("rates", "rates_live_chart",
         _advanced_def(
             "Rates Live Chart", "TradingView chart for treasury futures.",
             "/rates-live-udf", "ZN", 30000, grid=(20, 18), category="Macro",
         ),
         ["yield_curve", "curve_spread_metric"],
         ("Rates Advanced Live", "TradingView rates chart and curve.",
          [("chart", "Chart", [("rates_live_chart", 0, 0, 20, 18)]),
           ("curve", "Curve", [("yield_curve", 0, 0, 20, 9)])]),
         "rates chart",
         (c.text_param("contract", "Contract", "ZN",
                       "Treasury futures contract."),
          "contract", "ZB")),
    ]
    for desk_key, focus_id, focus, sibling_ids, app_spec, note_term, configure in t4_specs:
        desk = c.desk(desk_key)
        focus = _copy(focus)
        config_param, param_name, set_value = configure
        if config_param is not None:
            focus.setdefault("params", []).append(_copy(config_param))
        widgets = {focus_id: focus}
        for sibling_id in sibling_ids:
            widgets[sibling_id] = c.desk_widget(desk_key, sibling_id)
        app_name, app_desc, tab_specs = app_spec
        if len(tab_specs) == 1 and len(tab_specs[0][2]) > 1:
            primary_tab_id, primary_tab_name, items = tab_specs[0]
            tab_specs = [
                (primary_tab_id, primary_tab_name, items[:1]),
                ("signals", "Signals", items[1:]),
            ]
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name,
             [c.layout_item(wid, x, y, w, h) for wid, x, y, w, h in items])
            for tab_id, tab_name, items in tab_specs
        ])
        dashboard_name = f"{app_name} Dashboard"
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
        sid = f"auth_t4_advanced_{focus_id}_ship"
        c.add("advanced", "t4", {
            "id": sid,
            "title": f"Ship, open, and configure {app_name}",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "advanced",
                      "orchestration"],
            "prompt": c.phrased(sid, [
                (f"End to end. Publish \"{desk['backend']}\" at {desk['url']} - "
                 f"widgets.json: {widget_words}. apps.json: {app_words}. Then "
                 f"instantiate \"{app_name}\" into a dashboard named "
                 f"\"{dashboard_name}\", {configure_words}, and leave a note titled \"{app_name}\" "
                 f"that says exactly: \"{note_text}\""),
                (f"Build, publish, open, configure, document. Backend \"{desk['backend']}\" "
                 f"({desk['url']}) serves {widget_words} and ships {app_words}. "
                 f"Open it as \"{dashboard_name}\" via manage_apps, "
                 f"{configure_words}, then add a "
                 f"note \"{app_name}\" saying: \"{note_text}\""),
                (f"Four steps. One: add \"{desk['backend']}\" at {desk['url']} "
                 f"serving {widget_words}, shipping {app_words}. Two: instantiate "
                 f"\"{app_name}\" into \"{dashboard_name}\". Three: "
                 f"{configure_words}. Four: note titled "
                 f"\"{app_name}\" with text \"{note_text}\""),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.APP_TOOLS + ["add_generative_widget",
                                              "update_widget"],
            "success": {
                "required_widget_defs": [
                    _widget_checks(desk["backend"], focus_id, focus)
                ] + [
                    c.widget_def_anchor_checks(desk["backend"], sibling_id,
                                               widgets[sibling_id])
                    for sibling_id in sibling_ids
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
