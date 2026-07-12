"""Family SETTINGS — widget configuration hygiene."""

import json

from . import common as c


def _copy_with(definition: dict, **updates) -> dict:
    copied = json.loads(json.dumps(definition))
    copied.update(updates)
    return copied


def _strip(definition: dict, *keys: str) -> dict:
    copied = json.loads(json.dumps(definition))
    for key in keys:
        copied.pop(key, None)
    return copied


def _policy_clause(definition: dict) -> str:
    policies = []
    stale = definition.get("staleTime")
    if isinstance(stale, int) and not isinstance(stale, bool):
        policies.append(f"it caches results for {stale // 60000} minutes")
    interval = definition.get("refetchInterval")
    if isinstance(interval, int) and not isinstance(interval, bool):
        policies.append(f"it auto-refreshes every {interval // 1000} seconds")
    return " and ".join(policies)


def _policy_requirements(widget_id: str, definition: dict) -> str:
    return (
        f"{c.widget_requirements_text(widget_id, _strip(definition, 'staleTime', 'refetchInterval'))}; "
        f"{_policy_clause(definition)}. {c.CONFIG_RULES}"
    )


def build() -> None:
    # ------------------------------------------------------------------ r0
    # Exact JSON briefs, each carrying at least two configuration keys.
    t0_specs = [
        ("vol", "vol_regime_metric",
         {"staleTime": 900000, "runButton": True},
         "cached run-button metric"),
        ("tvl", "gas_metric",
         {"refetchInterval": 30000, "category": "Network Ops"},
         "auto-refresh categorized metric"),
        ("rates", "rates_commentary",
         {"staleTime": 1800000, "category": "Macro Notes"},
         "cached categorized markdown"),
        ("execution", "exception_metric",
         {"refetchInterval": 45000, "runButton": True},
         "refreshing run-button metric"),
    ]
    for desk_key, widget_id, updates, label in t0_specs:
        desk = c.desk(desk_key)
        definition = _copy_with(c.desk_widget(desk_key, widget_id), **updates)
        sid = f"{widget_id}"
        brief = c.widget_requirements_text(widget_id, definition)
        c.add("settings", "r0", {
            "id": sid,
            "title": f"Build the {definition['name']} {label}",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "settings"],
            "prompt": c.phrased(sid, [
                (f"Connect a new custom backend named \"{desk['backend']}\" at "
                 f"{desk['url']}. Its widgets.json serves exactly one configured "
                 f"widget — {brief}. Register it with manage_backends."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) with one "
                 f"widgets.json entry carrying its configuration: {brief}."),
                (f"You wrote a backend at {desk['url']}. Add it as "
                 f"\"{desk['backend']}\" serving this configured widget exactly — "
                 f"{brief}."),
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
    # Configured widget plus one-tab app wrapper.
    t1_specs = [
        ("compliance", "alert_metric",
         {"staleTime": 900000, "category": "Surveillance"},
         "Alert Settings", "Cached alert posture.", "alerts", "Alerts", (0, 0, 6, 4)),
        ("healthcare", "catalyst_metric",
         {"refetchInterval": 30000, "runButton": True},
         "Catalyst Settings", "Refreshing catalyst count.", "catalysts", "Catalysts",
         (0, 0, 6, 4)),
        ("earnings", "surprise_metric",
         {"staleTime": 1800000, "category": "Earnings", "source": "surprise-service"},
         "Surprise Settings", "Cached earnings surprise.", "surprises", "Surprises",
         (0, 0, 8, 5)),
        ("sla", "sla_runbook",
         {"staleTime": 900000, "runButton": True, "category": "Runbooks"},
         "Runbook Settings", "Configured SLA runbook.", "runbook", "Runbook",
         (0, 0, 12, 8)),
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
            f"an app named \"{app_name}\" (description \"{app_desc}\") with one "
            f"tab `{tab_id}` named \"{tab_name}\" placing `{widget_id}` at "
            f"x={x} y={y} w={w} h={h}"
        )
        c.add("settings", "r1", {
            "id": sid,
            "title": f"Ship the configured {definition['name']} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "settings"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']}. widgets.json serves one configured widget — "
                 f"{brief}. apps.json ships {wrap}. Publish both in one "
                 "manage_backends add."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) serving "
                 f"{brief}, shipped as {wrap}. Include widgets.json and apps.json "
                 "in the same add."),
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
    # Words-only composed settings: base widget plus two or more config
    # dimensions. Tables derive columns from stated rows.
    t2_specs = [
        ("rates", "auction_cache_grid", "Auction Cache Grid", "/auction-cache",
         "Cached auction watchlist.",
         [{"auction_date": "2026-07-14", "security": "10Y Note", "size_bn": 42},
          {"auction_date": "2026-07-15", "security": "30Y Bond", "size_bn": 25}],
         {"staleTime": 900000, "runButton": True, "category": "Rates"},
         "it caches results for 15 minutes, exposes a run button, and is categorized as Rates"),
        ("sla", "runbook_markdown", None, None, None, None,
         c.simple_def(
             "markdown", "Runbook Markdown", "Configured SLA runbook note.",
             "/runbook-markdown", grid=(12, 8),
             staleTime=900000, category="Runbooks", source="sla-runbook",
             runButton=True,
         ),
         "it caches results for 15 minutes and is categorized as Runbooks"),
        ("tvl", "gas_refresh_metric", None, None, None, None,
         c.simple_def(
             "metric", "Gas Refresh Metric", "Auto-refreshing gas snapshot.",
             "/gas-refresh", grid=(6, 4),
             refetchInterval=30000, category="Network Ops", runButton=True,
         ),
         "it auto-refreshes every 30 seconds and is categorized as Network Ops"),
        ("execution", "exception_refresh_grid", "Exception Refresh Grid",
         "/exception-refresh", "Execution exceptions with manual refresh.",
         [{"order_id": "O-1042", "symbol": "AAPL", "age_min": 12},
          {"order_id": "O-1043", "symbol": "MSFT", "age_min": 7}],
         {"refetchInterval": 45000, "runButton": True, "category": "Execution",
          "staleTime": 900000},
         "it auto-refreshes every 45 seconds, exposes a run button, is categorized as Execution, and caches results for 15 minutes"),
    ]
    for desk_key, widget_id, name, endpoint, description, rows, spec_or_dims, extra_text in t2_specs:
        desk = c.desk(desk_key)
        if rows is None:
            definition = spec_or_dims
            words = _policy_requirements(widget_id, definition)
        else:
            definition = c.derive_table_def(name, description, endpoint, rows,
                                            **spec_or_dims)
            words = (
                f"`{widget_id}`: name \"{name}\", description \"{description}\", "
                f"endpoint {endpoint}, type table, gridData w=20 h=9; "
                f"{extra_text}. {c.CONFIG_RULES} The endpoint returns rows like {c.rows_text(rows)} — "
                f"{c.DERIVATION_RULES} {c.DERIVATION_EXAMPLE}"
            )
        sid = f"{widget_id}"
        c.add("settings", "r2", {
            "id": sid,
            "title": f"Compose the configured {definition['name']} widget",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "settings", "composed"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']} serving one configured widgets.json entry: "
                 f"{words}. Publish it with manage_backends add."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) with exactly "
                 f"one configured widget. Requirements: {words}."),
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
    # Multi-widget apps where the shared config convention is stated once.
    t3_specs = [
        ("vol",
         [("vol_commentary", {"staleTime": 900000}),
          ("vol_regime_metric", {"staleTime": 900000})],
         "Both widgets cache with staleTime 900000.",
         "vol_commentary",
         ("Vol Settings Room", "Cached commentary and regime.",
          [("commentary", "Commentary", [("vol_commentary", 0, 0, 12, 8)]),
           ("regime", "Regime", [("vol_regime_metric", 0, 0, 6, 4)])])),
        ("tvl",
         [("gas_metric", {"category": "Network Ops", "refetchInterval": 30000}),
          ("protocol_details", {"category": "Network Ops", "refetchInterval": 30000})],
         "Both widgets are categorized as Network Ops and refresh every 30000 ms.",
         "gas_metric",
         ("Network Settings Room", "Gas and protocol settings.",
          [("gas", "Gas", [("gas_metric", 0, 0, 6, 4)]),
           ("protocol", "Protocol", [("protocol_details", 0, 0, 12, 8)])])),
        ("compliance",
         [("alert_metric", {"category": "Surveillance", "staleTime": 1800000}),
          ("case_notes", {"category": "Surveillance", "staleTime": 1800000}),
          ("policy_pdf", {"category": "Surveillance", "staleTime": 1800000})],
         "All three widgets are categorized as Surveillance and cache with staleTime 1800000.",
         "alert_metric",
         ("Surveillance Settings Room", "Alerts, notes, and policy settings.",
          [("alerts", "Alerts", [("alert_metric", 0, 0, 6, 4),
                                    ("case_notes", 6, 0, 12, 8)]),
           ("policy", "Policy", [("policy_pdf", 0, 0, 16, 14)])])),
        ("earnings",
         [("surprise_metric", {"runButton": True, "refetchInterval": 45000}),
          ("earnings_note", {"runButton": True, "refetchInterval": 45000}),
          ("earnings_chart", {"runButton": True, "refetchInterval": 45000})],
         "All three widgets expose runButton true and refresh every 45000 ms.",
         "surprise_metric",
         ("Earnings Settings Room", "Surprise, preview, and chart settings.",
          [("summary", "Summary", [("surprise_metric", 0, 0, 6, 4),
                                      ("earnings_chart", 6, 0, 20, 9)]),
           ("preview", "Preview", [("earnings_note", 0, 0, 12, 8)])])),
    ]
    for desk_key, widget_specs, shared_text, focus_id, app_spec in t3_specs:
        desk = c.desk(desk_key)
        widgets = {
            wid: _copy_with(c.desk_widget(desk_key, wid), **updates)
            for wid, updates in widget_specs
        }
        app_name, app_desc, tab_specs = app_spec
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name,
             [c.layout_item(wid, x, y, w, h) for wid, x, y, w, h in items])
            for tab_id, tab_name, items in tab_specs
        ])
        configured_keys = {"staleTime", "refetchInterval", "runButton", "category"}
        widget_words = "; ".join(
            c.widget_requirements_text(wid, _strip(definition, *configured_keys))
            for wid, definition in widgets.items()
        )
        app_words = c.app_requirements_text(app)
        sid = f"{focus_id}_room"
        c.add("settings", "r3", {
            "id": sid,
            "title": f"Assemble the {app_name} configured app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "settings", "multi-tab"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then publish \"{desk['backend']}\" at "
                 f"{desk['url']} in one add. Shared configuration: {shared_text} "
                 f"widgets.json serves: {widget_words}. apps.json ships {app_words}."),
                (f"Connect \"{desk['backend']}\" ({desk['url']}). Apply this "
                 f"shared configuration once: {shared_text} Widgets: "
                 f"{widget_words}. App: {app_words}. One manage_backends add."),
                (f"Build both files for \"{desk['backend']}\" at {desk['url']}. "
                 f"{shared_text} Widget requirements: {widget_words}. App "
                 f"requirements: {app_words}. Publish together."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.widget_def_checks(desk["backend"], focus_id, widgets[focus_id])
                ] + [
                    c.widget_def_anchor_checks(desk["backend"], wid, widgets[wid])
                    for wid in widgets if wid != focus_id
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
    # Configured pack + app + instantiate + configure + note.
    t4_specs = [
        ("vol",
         [("vol_regime_metric", {"staleTime": 900000, "runButton": True}),
          ("vol_commentary", {"staleTime": 900000, "runButton": True}),
          ("vix_history", {"staleTime": 900000, "runButton": True})],
         "vol_regime_metric",
         ("Vol Config Live", "Configured vol metric and commentary.", "vol", "Vol"),
         "15-minute cache",
         (c.text_param("regime_view", "Regime View", "summary",
                       "Vol regime view to show."),
          "regime_view", "stress")),
        ("rates",
         [("curve_spread_metric", {"category": "Macro", "refetchInterval": 30000}),
          ("rates_commentary", {"category": "Macro", "refetchInterval": 30000}),
          ("yield_curve", {"category": "Macro", "refetchInterval": 30000})],
         "curve_spread_metric",
         ("Rates Config Live", "Configured curve spread and commentary.", "rates", "Rates"),
         "Macro category",
         (c.text_param("curve_view", "Curve View", "2s10s",
                       "Curve segment in focus."),
          "curve_view", "5s30s")),
        ("execution",
         [("exception_metric", {"runButton": True, "refetchInterval": 45000}),
          ("open_orders", {"runButton": True, "refetchInterval": 45000}),
          ("venue_pdf", {"runButton": True, "refetchInterval": 45000})],
         "exception_metric",
         ("Execution Config Live", "Configured exceptions and orders.", "execution", "Execution"),
         "on-demand updates",
         (c.text_param("queue", "Queue", "all",
                       "Exception queue to inspect."),
          "queue", "urgent")),
        ("healthcare",
         [("catalyst_metric", {"category": "Catalysts", "staleTime": 1800000}),
          ("trial_catalysts", {"category": "Catalysts", "staleTime": 1800000}),
          ("pipeline_chart", {"category": "Catalysts", "staleTime": 1800000})],
         "catalyst_metric",
         ("Catalyst Config Live", "Configured catalysts and trial table.",
          "catalysts", "Catalysts"),
         "Catalysts category",
         (c.text_param("window", "Window", "30d",
                       "Catalyst window in focus."),
          "window", "60d")),
    ]
    for desk_key, widget_specs, focus_id, app_spec, note_term, configure in t4_specs:
        desk = c.desk(desk_key)
        widgets = {
            wid: _copy_with(c.desk_widget(desk_key, wid), **updates)
            for wid, updates in widget_specs
        }
        new_param, param_name, set_value = configure
        widgets[focus_id].setdefault("params", []).append(
            json.loads(json.dumps(new_param))
        )
        sibling_ids = [wid for wid in widgets if wid != focus_id]
        sibling_id = sibling_ids[0]
        app_name, app_desc, tab_id, tab_name = app_spec
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(focus_id, 0, 0, 8, 5)]),
            ("posture", "Posture", [c.layout_item(sibling_id, 0, 0, 20, 9)]),
        ])
        dashboard_name = f"{app_name} Board"
        note_text = f"{app_name} shipped from {desk['backend']}: {note_term}."
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
        c.add("settings", "r4", {
            "id": sid,
            "title": f"Ship, open, and configure the {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "settings",
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
                    c.widget_def_checks(desk["backend"], focus_id, widgets[focus_id]),
                ] + [
                    c.widget_def_anchor_checks(desk["backend"], wid, widgets[wid])
                    for wid in sibling_ids
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
