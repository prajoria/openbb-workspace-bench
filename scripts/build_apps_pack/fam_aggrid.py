"""Family AGGRID — tables & columnsDefs (onboarding tabs: AgGrid, Sparkline).

EXEMPLAR MODULE for the v3 ladder: every widget-side family follows this shape.
Owns widget types: table, ssrm_table (asserted by TYPE_OWNERSHIP at certify).

The v3 ladder (Didier alignment, 2026-07-08):
- t0 one widget with the right schema — words-form requirements brief (the model builds the JSON), single add.
- t1 ship it as an app — the widget (words) plus a one-tab apps.json wrapper
  described in words; the widget grades as a 3-check anchor (skill proven at
  t0), the app block grades fully.
- t2 one widget, >=2 composed requirements — requirements in words, never JSON;
  columns DERIVED from served rows; a second dimension (settings/type/extras)
  composed on top.
- t3 the app takes shape — 2-3 widgets + a multi-tab app with placements in
  words; focus widget full, siblings anchored, app full.
- t4 operate what you built — build, publish, instantiate the built app,
  document; TRACE_T4 budget.
"""

import json

from . import common as c


def _strip(definition: dict, *keys: str) -> dict:
    return {key: value for key, value in definition.items() if key not in keys}


def build() -> None:
    # ------------------------------------------------------------------ t0
    # One table definition with the right schema; exact-JSON brief; one add.
    t0_specs = [
        # (desk, widget_id) — every t0 def keeps its full schema surface
        # (params + columns where the type carries them): "the right schema"
        # must include the structured elements, or the tier is a giveaway
        # (proxy r3: bare defs kept the floor model at 100%).
        ("vol", "vix_history"),
        ("execution", "open_orders"),
        ("rates", "auction_calendar"),
        ("earnings", "estimates_ssrm"),  # owns ssrm_table at the base tier
    ]
    for desk_key, widget_id in t0_specs:
        desk = c.desk(desk_key)
        definition = c.desk_widget(desk_key, widget_id)
        if widget_id == "estimates_ssrm":
            # the served ssrm def is bare — t0 requires a real schema surface
            definition["params"] = [
                c.endpoint_param("symbol", "Symbol", "AAPL", "/symbols")
            ]
            definition.setdefault("data", {})["dataKey"] = "rows"
        sid = f"auth_t0_aggrid_{widget_id}"
        brief = c.widget_requirements_text(widget_id, definition)
        c.add("aggrid", "t0", {
            "id": sid,
            "title": f"Build the {definition['name']} table definition",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "aggrid"],
            "prompt": c.phrased(sid, [
                (f"Connect a new custom backend named \"{desk['backend']}\" at "
                 f"{desk['url']}. Its widgets.json serves exactly one widget — "
                 f"{brief}. Register it with manage_backends."),
                (f"Register a custom backend \"{desk['backend']}\" (url "
                 f"{desk['url']}) whose widgets.json contains one entry: {brief}."),
                (f"You wrote a backend at {desk['url']}. Add it to the workspace "
                 f"as \"{desk['backend']}\" serving this single widgets.json "
                 f"entry — {brief}."),
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
    # Ship it as an app: the widget (exact JSON, graded in full) plus a
    # one-tab apps.json wrapper stated in words.
    t1_specs = [
        # (desk, widget_id, app_name, app_desc, tab_id, tab_name, (x, y, w, h))
        ("tvl", "chains_table", "Chains Board", "Chain TVL at a glance.",
         "overview", "Overview", (0, 0, 20, 9)),
        ("sla", "vendor_sla_table", "Vendor Ops", "Vendor SLA operations.",
         "vendors", "Vendors", (0, 0, 20, 9)),
        ("compliance", "alert_queue", "Surveillance Desk", "Open surveillance alerts.",
         "alerts", "Alerts", (0, 0, 24, 10)),
        ("healthcare", "trial_catalysts", "Catalyst Watch", "Upcoming trial catalysts.",
         "catalysts", "Catalysts", (0, 0, 24, 10)),
    ]
    for desk_key, widget_id, app_name, app_desc, tab_id, tab_name, pos in t1_specs:
        desk = c.desk(desk_key)
        definition = c.desk_widget(desk_key, widget_id)
        x, y, w, h = pos
        app = c.app_def(app_name, app_desc,
                        tabs=[(tab_id, tab_name, [c.layout_item(widget_id, x, y, w, h)])])
        sid = f"auth_t1_aggrid_{widget_id}_app"
        brief = c.widget_requirements_text(widget_id, definition)
        wrap = (
            f"an app named \"{app_name}\" (description \"{app_desc}\") with a "
            f"single tab `{tab_id}` named \"{tab_name}\" that places "
            f"`{widget_id}` at x={x} y={y} w={w} h={h}"
        )
        c.add("aggrid", "t1", {
            "id": sid,
            "title": f"Ship {definition['name']} as the {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "aggrid"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']}. Its widgets.json serves one widget — {brief}. "
                 f"Its apps.json ships {wrap}. Publish both in the same "
                 "manage_backends add."),
                (f"Register the backend \"{desk['backend']}\" ({desk['url']}) "
                 f"serving {brief} — and ship it as {wrap}, widgets.json and "
                 "apps.json in one add."),
                (f"Build both files for \"{desk['backend']}\" at {desk['url']}: "
                 f"widgets.json with {brief}, apps.json with {wrap}. One "
                 "manage_backends call."),
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
    # Composed requirements in words: columns derived from served rows PLUS a
    # second stated dimension (settings / type / render extras). No JSON given.
    t2_specs = [
        # (desk, widget_id, name, endpoint, description, rows, extra_dims,
        #  extra_text) — extra_dims patches the derived def; extra_text states
        #  the composed requirement in words.
        ("rates", "auction_watch", "Auction Watch", "/auction-watch",
         "Upcoming treasury auctions.",
         [{"auction_date": "2026-07-14", "security": "10Y Note", "size_bn": 42,
           "bid_to_cover": 2.43},
          {"auction_date": "2026-07-15", "security": "30Y Bond", "size_bn": 25,
           "bid_to_cover": 2.31}],
         {"staleTime": 900000, "runButton": True},
         "it caches results for 15 minutes and exposes a run button "
         "(runButton true). " + c.CONFIG_RULES),
        ("execution", "fill_quality", "Fill Quality", "/fill-quality",
         "Fill quality by venue.",
         [{"venue": "ARCA", "fills": 1240, "slippage_pct": 0.0021,
           "as_of": "2026-07-01"},
          {"venue": "EDGX", "fills": 980, "slippage_pct": 0.0034,
           "as_of": "2026-07-01"}],
         {"refetchInterval": 30000, "category": "Execution"},
         "it auto-refreshes every 30 seconds and files under category "
         "\"Execution\". " + c.CONFIG_RULES),
        ("vol", "realized_screen", "Realized Vol Screen", "/realized-vol",
         "Realized volatility by tenor.",
         [{"tenor": "1M", "realized_pct": 0.182, "as_of": "2026-07-01"},
          {"tenor": "3M", "realized_pct": 0.204, "as_of": "2026-07-01"}],
         {"_patch_render": ("realized_pct", "greenRed"), "staleTime": 1200000},
         "the realized_pct column additionally renders greenRed (renderFn), "
         "and it caches results for 20 minutes. " + c.CONFIG_RULES),
        ("earnings", "revision_grid", "Revision Grid", "/revision-momentum",
         "Street revision momentum by ticker.",
         [{"ticker": "AAPL", "revised_up": 14, "revised_down": 3,
           "momentum_pct": 0.084},
          {"ticker": "MSFT", "revised_up": 11, "revised_down": 5,
           "momentum_pct": 0.041}],
         {"type": "ssrm_table", "_data_key": "rows"},
         "it is served as a server-side row-model grid — type ssrm_table — "
         "whose rows are read from the response key \"rows\""),
    ]
    for desk_key, widget_id, name, endpoint, description, rows, dims, extra_text in t2_specs:
        desk = c.desk(desk_key)
        patch_render = dims.pop("_patch_render", None)
        data_key = dims.pop("_data_key", None)
        definition = c.derive_table_def(name, description, endpoint, rows, **dims)
        if patch_render:
            field, render_fn = patch_render
            for column in definition["data"]["table"]["columnsDefs"]:
                if column["field"] == field:
                    column["renderFn"] = render_fn
        if data_key:
            definition["data"]["dataKey"] = data_key
        sid = f"auth_t2_aggrid_{widget_id}"
        surface = (
            f"`{widget_id}`: name \"{name}\", description \"{description}\", "
            f"endpoint {endpoint}, "
            f"type {definition.get('type', 'table')}, gridData w=20 h=9"
        )
        c.add("aggrid", "t2", {
            "id": sid,
            "title": f"Compose the {name} table from its rows and requirements",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "aggrid", "derivation", "composed"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']} serving one widgets.json entry — {surface}. Two "
                 f"composed requirements. First, {extra_text}. Second, the "
                 f"endpoint returns rows like {c.rows_text(rows)} — "
                 f"{c.DERIVATION_RULES} {c.DERIVATION_EXAMPLE}"),
                (f"Register \"{desk['backend']}\" ({desk['url']}) with a single "
                 f"table — {surface}. Requirements: {extra_text}; and the columns "
                 f"come from the served rows {c.rows_text(rows)}. "
                 f"{c.DERIVATION_RULES} {c.DERIVATION_EXAMPLE}"),
                (f"Build the widgets.json for \"{desk['backend']}\" at "
                 f"{desk['url']}: {surface}. Note that {extra_text}. Columns are "
                 f"derived from rows like {c.rows_text(rows)} — "
                 f"{c.DERIVATION_RULES} {c.DERIVATION_EXAMPLE} Then add the "
                 "backend via manage_backends."),
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
    # The app takes shape: 2-3 widgets + a multi-tab app, all in words. The
    # derived table is the graded focus; siblings anchor; the app grades fully.
    t3_specs = [
        # (desk, focus=(widget_id, name, endpoint, description, rows, dims),
        #  siblings=[widget_id, ...], app=(name, desc,
        #  [(tab_id, tab_name, [(wid, x, y, w, h), ...]), ...]), hard)
        ("sla",
         ("latency_history", "Latency History", "/latency-history",
          "Vendor latency history.",
          [{"vendor": "AlphaFeed", "day": "2026-07-01", "latency_ms": 240,
            "breach": False},
           {"vendor": "QuoteStream", "day": "2026-07-01", "latency_ms": 610,
            "breach": True}],
          {"staleTime": 900000}),
         ["breach_metric"],
         ("Vendor Health", "Latency and breach posture.",
          [("latency", "Latency", [("latency_history", 0, 0, 20, 9)]),
           ("signals", "Signals", [("breach_metric", 0, 0, 12, 6)])]),
         False),
        ("tvl",
         ("chain_flows", "Chain Flows", "/chain-flows",
          "Net flows by chain.",
          [{"chain": "Ethereum", "inflow_usd": 120000000, "outflow_usd": 90000000,
            "net_pct": 0.033},
           {"chain": "Solana", "inflow_usd": 80000000, "outflow_usd": 95000000,
            "net_pct": -0.019}],
          {"staleTime": 900000}),
         ["gas_metric"],
         ("Flow Monitor", "Chain flows and gas.",
          [("flows", "Flows", [("chain_flows", 0, 0, 20, 9)]),
           ("gas", "Gas", [("gas_metric", 0, 0, 12, 6)])]),
         False),
        ("compliance",
         ("case_aging", "Case Aging", "/case-aging",
          "Open surveillance cases by age bucket.",
          [{"case_id": "C-1042", "desk": "Rates", "age_days": 12},
           {"case_id": "C-1044", "desk": "Equities", "age_days": 4}],
          {}),
         ["alert_queue", "alert_metric"],
         ("Case Room", "Cases, alerts, posture.",
          [("cases", "Cases", [("case_aging", 0, 0, 20, 9),
                                ("alert_metric", 20, 0, 12, 6)]),
           ("queue", "Queue", [("alert_queue", 0, 0, 24, 10)])]),
         True),
        ("vol",
         ("realized_vol_grid", "Realized Vol Grid", "/realized-vol-grid",
          "Realized volatility by tenor.",
          [{"tenor": "1M", "realized_pct": 0.182, "as_of": "2026-07-01"},
           {"tenor": "3M", "realized_pct": 0.204, "as_of": "2026-07-01"}],
          {}),
         ["vix_term_structure", "vol_regime_metric"],
         ("Vol Cockpit", "Realized, term structure, regime.",
          [("realized", "Realized", [("realized_vol_grid", 0, 0, 20, 9),
                                      ("vol_regime_metric", 20, 0, 12, 6)]),
           ("structure", "Structure", [("vix_term_structure", 0, 0, 20, 9)])]),
         True),
    ]
    for desk_key, focus_spec, sibling_ids, app_spec, _hard in t3_specs:
        desk = c.desk(desk_key)
        widget_id, name, endpoint, description, rows, dims = focus_spec
        focus = c.derive_table_def(name, description, endpoint, rows, **dims)
        widgets = {widget_id: focus}
        sibling_briefs = []
        for sib in sibling_ids:
            widgets[sib] = c.desk_widget(desk_key, sib)
            sibling_briefs.append(
                c.widget_requirements_text(sib, widgets[sib])
            )
        # hard cells (no per-focus dims): the composition dimension is a desk
        # convention stated ONCE and fanned out to every served def by the
        # model (graded on the focus's full checks).
        convention = "" if dims else c.stamp_consistency(widgets)
        app_name, app_desc, tab_specs = app_spec
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name,
             [c.layout_item(wid, x, y, w, h) for wid, x, y, w, h in items])
            for tab_id, tab_name, items in tab_specs
        ])
        dim_words = "".join(
            f", {key} {json.dumps(value)}" for key, value in dims.items()
        )
        focus_surface = (
            f"`{widget_id}`: name \"{name}\", description \"{description}\", "
            f"endpoint {endpoint}, type table, gridData w=20 h=9{dim_words}, "
            f"columns derived from served rows like {c.rows_text(rows)} — "
            f"{c.DERIVATION_RULES}"
        )
        if convention:
            focus_surface += f". Desk convention: {convention}"
        app_words = c.app_requirements_text(app)
        sid = f"auth_t3_aggrid_{widget_id}"
        c.add("aggrid", "t3", {
            "id": sid,
            "title": f"Assemble the {app_name} app around {name}",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "aggrid", "multi-tab"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then publish \"{desk['backend']}\" at "
                 f"{desk['url']} in one add. widgets.json serves "
                 f"{len(widgets)} entries: {focus_surface}. Plus: "
                 f"{'; '.join(sibling_briefs)}. apps.json ships {app_words}."),
                (f"Connect \"{desk['backend']}\" ({desk['url']}) serving "
                 f"{focus_surface}; alongside {'; '.join(sibling_briefs)}. Ship "
                 f"the app too — {app_words} — widgets.json and apps.json in the "
                 "same manage_backends add."),
                (f"Build both files for \"{desk['backend']}\" at {desk['url']}. "
                 f"Widgets: {focus_surface}; {'; '.join(sibling_briefs)}. App: "
                 f"{app_words}. Publish everything in one add."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.widget_def_checks(desk["backend"], widget_id, focus)
                ] + [
                    c.widget_def_anchor_checks(desk["backend"], sib, widgets[sib])
                    for sib in sibling_ids
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
    # Operate what you built: build + publish + instantiate + CONFIGURE +
    # document (proxy r5: without the configure step, t4's operate legs were
    # nearly free and t4 tied t3).
    t4_specs = [
        # (desk, focus=(widget_id, name, endpoint, description, rows), sibling,
        #  app=(name, desc, tab_id, tab_name), note_term,
        #  configure=(param, set_value))
        ("rates",
         ("auction_ladder", "Auction Ladder", "/auction-ladder",
          "Upcoming treasury auctions.",
          [{"auction_date": "2026-07-14", "security": "10Y Note", "size_bn": 42},
           {"auction_date": "2026-07-15", "security": "30Y Bond", "size_bn": 25}]),
         ["curve_spread_metric", "rates_commentary"],
         ("Auction Desk", "Auctions and curve posture.", "auctions", "Auctions"),
         "auctions",
         (c.text_param("security", "Security", "10Y Note",
                        "Security filter for the ladder."), "30Y Bond")),
        ("execution",
         ("venue_scorecard", "Venue Scorecard", "/venue-scorecard",
          "Execution quality by venue.",
          [{"venue": "ARCA", "fills": 1240, "slippage_pct": 0.0021},
           {"venue": "EDGX", "fills": 980, "slippage_pct": 0.0034}]),
         ["exception_metric", "slippage_chart"],
         ("Execution Room", "Venue quality and exceptions.", "venues", "Venues"),
         "venues",
         (c.text_param("venue", "Venue", "ARCA", "Venue in focus."), "EDGX")),
        ("healthcare",
         ("readout_calendar", "Readout Calendar", "/readout-calendar",
          "Upcoming trial readouts.",
          [{"ticker": "PFE", "phase": "III", "readout": "2026-08-19"},
           {"ticker": "MRNA", "phase": "II", "readout": "2026-09-02"}]),
         ["catalyst_metric", "fda_newsfeed"],
         ("Readout Desk", "Trial readouts and catalysts.", "readouts", "Readouts"),
         "readouts",
         (c.text_param("phase", "Phase", "III", "Trial phase filter."), "II")),
        ("earnings",
         ("beat_miss_grid", "Beat Miss Grid", "/beat-miss",
          "Beat/miss by ticker this season.",
          [{"ticker": "AAPL", "eps_surprise_pct": 0.042, "revenue_beat": True},
           {"ticker": "MSFT", "eps_surprise_pct": 0.021, "revenue_beat": True}]),
         ["surprise_metric", "earnings_note"],
         ("Season Tracker", "Beats, misses, surprises.", "season", "Season"),
         "season",
         (c.text_param("ticker", "Ticker", "AAPL", "Ticker in focus."), "MSFT")),
    ]
    for desk_key, focus_spec, sibling_ids, app_spec, note_term, configure in t4_specs:
        desk = c.desk(desk_key)
        widget_id, name, endpoint, description, rows = focus_spec
        config_param, set_value = configure
        focus = c.derive_table_def(name, description, endpoint, rows,
                                   params=[config_param])
        widgets = {widget_id: focus}
        for sib in sibling_ids:
            widgets[sib] = c.desk_widget(desk_key, sib)
        sibling_id = sibling_ids[0]
        sibling = widgets[sibling_id]
        app_name, app_desc, tab_id, tab_name = app_spec
        # t4 writes what t3 writes (two tabs + a fanned-out convention) and
        # then OPERATES it — proxy r3 found a t3/t4 inversion when t4's
        # built content was lighter than t3's.
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(widget_id, 0, 0, 20, 9)]),
            ("signals", "Signals", [c.layout_item(sibling_id, 0, 0, 12, 6)]),
        ])
        dashboard_name = f"{app_name} Live"
        note_text = f"{app_name} is live from {desk['backend']}: {note_term} on tap."
        sibling_brief = "; ".join(
            c.widget_requirements_text(sib, widgets[sib]) for sib in sibling_ids
        )
        convention = c.stamp_consistency(widgets)
        param_name = config_param["paramName"]
        param_words = c._param_requirement(config_param)
        focus_surface = (
            f"`{widget_id}`: name \"{name}\", description \"{description}\", "
            f"endpoint {endpoint}, type table, gridData w=20 h=9, taking "
            f"{param_words}, columns derived from served rows like "
            f"{c.rows_text(rows)} — {c.DERIVATION_RULES}"
            f". Desk convention: {convention}"
        )
        configure_words = (
            f"set {param_name} to \"{set_value}\" on the opened `{widget_id}` "
            "widget"
        )
        app_words = c.app_requirements_text(app)
        sid = f"auth_t4_aggrid_{desk_key}_ship"
        c.add("aggrid", "t4", {
            "id": sid,
            "title": f"Ship, open, and configure the {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "aggrid",
                      "orchestration"],
            "prompt": c.phrased(sid, [
                (f"End to end. Publish \"{desk['backend']}\" at {desk['url']} — "
                 f"widgets.json: {focus_surface}; plus {sibling_brief}. apps.json: "
                 f"{app_words}. Then instantiate the \"{app_name}\" app from that "
                 f"backend into a dashboard named \"{dashboard_name}\", "
                 f"{configure_words}, and leave a "
                 f"note titled \"{app_name}\" that says exactly: \"{note_text}\""),
                (f"Build, publish, open, configure, document. Backend "
                 f"\"{desk['backend']}\" "
                 f"({desk['url']}) serves {focus_surface}; {sibling_brief}; and "
                 f"ships {app_words}. Open the app as \"{dashboard_name}\" via "
                 f"manage_apps, {configure_words}, then record a note "
                 f"\"{app_name}\" saying: \"{note_text}\""),
                (f"Four steps. One: add \"{desk['backend']}\" at {desk['url']} "
                 f"serving {focus_surface}, {sibling_brief}, and {app_words}. Two: "
                 f"instantiate \"{app_name}\" into \"{dashboard_name}\". Three: "
                 f"{configure_words}. Four: a "
                 f"note titled \"{app_name}\" with the text: \"{note_text}\""),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.APP_TOOLS + ["add_generative_widget",
                                              "update_widget"],
            "success": {
                "required_widget_defs": [
                    c.widget_def_checks(desk["backend"], widget_id, focus),
                ] + [
                    c.widget_def_anchor_checks(desk["backend"], sib, widgets[sib])
                    for sib in sibling_ids
                ],
                # the app-building skill is graded fully at t1-t3; t4 grades
                # its marginal skill (the operate chain), so the app anchors
                # (proxy full-r6: full app grading left t4's building lighter
                # than t3's and the tiers tied).
                "required_app_defs": [
                    c.app_def_anchor_checks(desk["backend"], app)
                ],
                "required_widgets": [
                    {"origin": desk["backend"], "widget_id": widget_id,
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
                c.add_backend_call(desk["backend"], desk["url"], widgets,
                                   apps=[app]),
                c.instantiate_call("backend_001", app_name, dashboard_name),
                {"tool": "update_widget",
                 "args": {"widget_id": widget_id,
                          "data_args": {param_name: set_value}}},
                {"tool": "add_generative_widget",
                 "args": {"widget_type": "note", "name": app_name,
                          "data": note_text}},
            ],
        })
