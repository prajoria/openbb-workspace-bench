"""Family APPS — apps.json building (app-side exemplar for the v3 ladder).

The apps.json file IS the artifact under test at every level; widgets stay
deliberately simple so grading breadth tracks the app skill:
- r0 one app with the right schema — the backend is SEEDED with widgets; the
  model writes apps.json from a words-form requirements brief, shipped via refresh.
- r1 ship it as an app — build widgets.json (one widget, words) AND the
  one-tab apps.json wrapper (words) from scratch in one add.
- r2 one app, >=2 composed requirements — seeded widgets; the app is stated in
  words and composes placements + a param group / preset params / prompts.
- r3 the app takes shape — 2-3 widgets (words) + a multi-tab app in one add;
  focus widget full, siblings anchored, app full.
- r4 operate what you built — build, publish, instantiate, document.
"""

import json
from typing import Any, TypedDict

from . import common as c


class ComposedAppSpec(TypedDict):
    name: str
    desc: str
    tab_id: str
    tab_name: str
    items: list[tuple[str, int, int, int, int, dict[str, Any] | None]]
    groups: list[dict[str, Any]]
    prompts: list[str] | None


class MultiTabAppSpec(TypedDict):
    name: str
    desc: str
    tabs: list[tuple[str, str, list[tuple[str, int, int, int, int]]]]
    groups: list[dict[str, Any]]


def build() -> None:
    # ------------------------------------------------------------------ r0
    # The backend already serves two widgets (seeded); build apps.json only.
    t0_specs = [
        # (desk, widget ids serving, app name, desc, tab_id, tab name, layout)
        ("vol", ["vix_history", "vol_regime_metric"],
         "Vol Overview", "Vol level and regime.",
         "overview", "Overview",
         [("vix_history", 0, 0, 20, 9), ("vol_regime_metric", 20, 0, 12, 6)]),
        ("rates", ["yield_curve", "curve_spread_metric"],
         "Rates Morning", "Curve and spread at the open.",
         "morning", "Morning",
         [("yield_curve", 0, 0, 20, 9), ("curve_spread_metric", 20, 0, 12, 6)]),
        ("execution", ["open_orders", "exception_metric"],
         "Order Watch", "Open orders and exceptions.",
         "orders", "Orders",
         [("open_orders", 0, 0, 20, 9), ("exception_metric", 20, 0, 12, 6)]),
        ("sla", ["vendor_sla_table", "breach_metric"],
         "Vendor Board", "Vendor SLAs and breaches.",
         "vendors", "Vendors",
         [("vendor_sla_table", 0, 0, 20, 9), ("breach_metric", 20, 0, 12, 6)]),
    ]
    for desk_key, widget_ids, app_name, app_desc, tab_id, tab_name, items in t0_specs:
        desk = c.desk(desk_key)
        widgets = {wid: c.desk_widget(desk_key, wid) for wid in widget_ids}
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name,
             [c.layout_item(wid, x, y, w, h) for wid, x, y, w, h in items]),
        ])
        sid = f"{app_name.lower().replace(' ', '_')}"
        brief = c.app_requirements_text(app)
        c.add("apps", "r0", {
            "id": sid,
            "title": f"Build the {app_name} app definition",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "apps-json"],
            "prompt": c.phrased(sid, [
                (f"Your backend \"{desk['backend']}\" is already connected and "
                 f"serves {', '.join(f'`{w}`' for w in widget_ids)}. Ship its "
                 f"apps.json — exactly one app: {brief}. Submit it with a "
                 "manage_backends refresh (apps_json)."),
                (f"Add an apps.json to the connected backend "
                 f"\"{desk['backend']}\" (it already serves "
                 f"{', '.join(f'`{w}`' for w in widget_ids)}): {brief}. Use "
                 "operation refresh with the apps_json payload."),
                (f"The widgets are served; the app file is missing. For "
                 f"\"{desk['backend']}\", build apps.json with one entry — "
                 f"{brief} — and refresh the backend with it."),
            ]),
            "fixtures": {},
            "initial_state": c.seeded_custom(desk["backend"], desk["url"], widgets),
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_app_defs": [c.app_def_checks(desk["backend"], app)],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.snap(),
                c.refresh_call("backend_001", apps=[app]),
            ],
        })

    # ------------------------------------------------------------------ r1
    # From scratch: one exact-JSON widget + the one-tab app wrapper in words.
    t1_specs = [
        ("tvl", "gas_metric", "Gas Board", "Gas posture at a glance.",
         "gas", "Gas", (0, 0, 12, 6)),
        ("compliance", "alert_metric", "Alert Board", "Alert posture.",
         "alerts", "Alerts", (0, 0, 12, 6)),
        ("healthcare", "catalyst_metric", "Catalyst Board", "Catalyst count.",
         "catalysts", "Catalysts", (0, 0, 12, 6)),
        ("earnings", "surprise_metric", "Surprise Board", "Surprise posture.",
         "surprises", "Surprises", (0, 0, 12, 6)),
    ]
    for desk_key, widget_id, app_name, app_desc, tab_id, tab_name, pos in t1_specs:
        desk = c.desk(desk_key)
        definition = c.desk_widget(desk_key, widget_id)
        x, y, w, h = pos
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(widget_id, x, y, w, h)]),
        ])
        sid = f"{widget_id}_wrap"
        brief = c.widget_requirements_text(widget_id, definition)
        wrap = (
            f"an app named \"{app_name}\" (description \"{app_desc}\") with one "
            f"tab `{tab_id}` named \"{tab_name}\" placing `{widget_id}` at "
            f"x={x} y={y} w={w} h={h}"
        )
        c.add("apps", "r1", {
            "id": sid,
            "title": f"Ship {definition['name']} inside the {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']}. widgets.json serves one widget — {brief}. "
                 f"apps.json ships {wrap}. Publish both in one manage_backends "
                 "add."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) serving {brief}, "
                 f"shipped as {wrap} — both files in the same add."),
                (f"Build widgets.json ({brief}) and apps.json ({wrap}) for "
                 f"\"{desk['backend']}\" at {desk['url']}, then add the backend."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.widget_def_anchor_checks(desk["backend"], widget_id, definition)
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
    # Composed app requirements in words over seeded widgets: placements plus a
    # second dimension (param group / preset params / suggested prompts).
    t2_specs: list[tuple[str, list[str], ComposedAppSpec]] = [
        # (desk, served ids, app spec dict)
        ("earnings", ["estimate_revisions", "earnings_chart", "surprise_metric"],
         {"name": "Earnings Command", "desc": "Symbol-synced earnings review.",
          "tab_id": "review", "tab_name": "Review",
          "items": [("estimate_revisions", 0, 0, 20, 9, None),
                     ("earnings_chart", 20, 0, 12, 9, {"symbol": "NVDA"}),
                     ("surprise_metric", 32, 0, 8, 6, None)],
          "groups": [{"name": "Symbol Sync", "type": "param",
                       "paramName": "symbol",
                       "widgetIds": ["estimate_revisions", "earnings_chart"]}],
          "prompts": None}),
        ("vol", ["vix_history", "vix_term_structure", "vol_regime_metric"],
         {"name": "Vol Morning", "desc": "Vol level, structure, regime.",
          "tab_id": "morning", "tab_name": "Morning",
          "items": [("vix_history", 0, 0, 20, 9, {"window": 30}),
                     ("vix_term_structure", 20, 0, 12, 9, None),
                     ("vol_regime_metric", 32, 0, 8, 6, None)],
          "groups": [],
          "prompts": ["What changed in the term structure overnight?",
                        "Summarize the vol regime in one line."]}),
        ("compliance", ["alert_queue", "case_notes", "alert_metric"],
         {"name": "Surveillance Morning", "desc": "Alerts and case notes.",
          "tab_id": "alerts", "tab_name": "Alerts",
          "items": [("alert_queue", 0, 0, 24, 10, {"severity": "high"}),
                     ("case_notes", 24, 0, 12, 10, None),
                     ("alert_metric", 0, 10, 12, 6, None)],
          "groups": [],
          "prompts": ["Which high-severity alerts are unassigned?"]}),
        ("sla", ["vendor_sla_table", "breach_metric", "sla_newsfeed"],
         {"name": "Vendor Command", "desc": "Vendors, breaches, headlines.",
          "tab_id": "vendors", "tab_name": "Vendors",
          "items": [("vendor_sla_table", 0, 0, 20, 9, {"status": "breach"}),
                     ("breach_metric", 20, 0, 12, 6, None),
                     ("sla_newsfeed", 20, 6, 12, 8, None)],
          "groups": [],
          "prompts": ["Which vendors breached SLA this week?"]}),
    ]
    for desk_key, served_ids, spec in t2_specs:
        desk = c.desk(desk_key)
        widgets = {wid: c.desk_widget(desk_key, wid) for wid in served_ids}
        app = c.app_def(
            spec["name"], spec["desc"],
            tabs=[(spec["tab_id"], spec["tab_name"], [
                c.layout_item(wid, x, y, w, h, params=params)
                for wid, x, y, w, h, params in spec["items"]
            ])],
            groups=spec["groups"] or None,
            prompts=spec["prompts"],
        )
        sid = f"{spec['name'].lower().replace(' ', '_')}"
        words = c.app_requirements_text(app)
        c.add("apps", "r2", {
            "id": sid,
            "title": f"Compose the {spec['name']} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "apps-json", "composed"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace. Your backend \"{desk['backend']}\" "
                 f"already serves {', '.join(f'`{w}`' for w in served_ids)}; its "
                 f"apps.json is missing. Build it — one app: {words}. Ship it "
                 "via manage_backends refresh."),
                (f"Build the apps.json for the connected backend "
                 f"\"{desk['backend']}\" (serving "
                 f"{', '.join(f'`{w}`' for w in served_ids)}): {words}. Then "
                 "refresh the backend with the payload."),
                (f"One app to ship on \"{desk['backend']}\": {words}. The "
                 "widgets are already served — submit apps_json with a refresh."),
            ]),
            "fixtures": {},
            "initial_state": c.seeded_custom(desk["backend"], desk["url"], widgets),
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_app_defs": [c.app_def_checks(desk["backend"], app)],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.snap(),
                c.refresh_call("backend_001", apps=[app]),
            ],
        })

    # ------------------------------------------------------------------ r3
    # From scratch: 2-3 widgets in words + a multi-tab app in one add. Every
    # cell carries a composition dimension: a param group where the widgets
    # share a param (added to the defs when needed), or a desk convention
    # stated once and fanned out (proxy r2 hardening).
    t3_specs: list[
        tuple[str, str, list[str], MultiTabAppSpec, dict[str, Any] | None]
    ] = [
        # (desk, focus widget id, sibling ids, app spec, shared_param)
        ("tvl", "chains_table", ["chains_chart"],
         {"name": "Chain Deck", "desc": "TVL table and trend.",
          "tabs": [("table", "Table", [("chains_table", 0, 0, 20, 9)]),
                    ("trend", "Trend", [("chains_chart", 0, 0, 20, 9)])],
          "groups": [{"name": "Chain Sync", "type": "param",
                       "paramName": "chain",
                       "widgetIds": ["chains_table", "chains_chart"]}]},
         c.text_param("chain", "Chain", "Ethereum",
                       "Chain the deck is focused on.")),
        ("rates", "auction_calendar", ["yield_curve"],
         {"name": "Rates Desk", "desc": "Auctions and the curve.",
          "tabs": [("auctions", "Auctions", [("auction_calendar", 0, 0, 20, 9)]),
                    ("curve", "Curve", [("yield_curve", 0, 0, 20, 9)])],
          "groups": []},
         None),
        ("earnings", "earnings_chart", ["estimate_revisions", "surprise_metric"],
         {"name": "Earnings Desk", "desc": "Revisions, price, surprises.",
          "tabs": [("revisions", "Revisions",
                     [("estimate_revisions", 0, 0, 20, 9),
                      ("surprise_metric", 20, 0, 12, 6)]),
                    ("price", "Price", [("earnings_chart", 0, 0, 20, 9)])],
          "groups": [{"name": "Symbol Sync", "type": "param",
                       "paramName": "symbol",
                       "widgetIds": ["estimate_revisions", "earnings_chart"]}]},
         None),
        ("compliance", "case_notes", ["alert_queue", "alert_metric"],
         {"name": "Case Command", "desc": "Alerts, notes, posture.",
          "tabs": [("queue", "Queue", [("alert_queue", 0, 0, 24, 10),
                                         ("alert_metric", 24, 0, 12, 6)]),
                    ("notes", "Notes", [("case_notes", 0, 0, 20, 10)])],
          "groups": []},
         None),
    ]
    for desk_key, focus_id, sibling_ids, multi_tab_spec, shared_param in t3_specs:
        desk = c.desk(desk_key)
        focus = c.desk_widget(desk_key, focus_id)
        widgets = {focus_id: focus}
        for sib in sibling_ids:
            widgets[sib] = c.desk_widget(desk_key, sib)
        shared_note = ""
        if shared_param is not None:
            grouped_ids = multi_tab_spec["groups"][0]["widgetIds"]
            for wid in grouped_ids:
                widgets[wid].setdefault("params", []).append(
                    json.loads(json.dumps(shared_param))
                )
            shared_note = " " + c.shared_param_note(shared_param, grouped_ids)
        app = c.app_def(multi_tab_spec["name"], multi_tab_spec["desc"], tabs=[
            (tab_id, tab_name,
             [c.layout_item(wid, x, y, w, h) for wid, x, y, w, h in items])
            for tab_id, tab_name, items in multi_tab_spec["tabs"]
        ], groups=multi_tab_spec["groups"] or None)
        omit = {shared_param["paramName"]} if shared_param else set()
        widget_words = "; ".join(
            c.widget_requirements_text(wid, definition, omit_params=omit)
            for wid, definition in widgets.items()
        )
        widget_words += shared_note
        convention = ""
        if shared_param is None and not multi_tab_spec["groups"]:
            convention = c.stamp_consistency(widgets)
            widget_words += f". Desk convention: {convention}"
        app_words = c.app_requirements_text(app)
        sid = f"{multi_tab_spec['name'].lower().replace(' ', '_')}"
        c.add("apps", "r3", {
            "id": sid,
            "title": f"Assemble the {multi_tab_spec['name']} app from scratch",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "multi-tab"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then publish \"{desk['backend']}\" at "
                 f"{desk['url']} in one add. widgets.json serves: {widget_words}. "
                 f"apps.json ships {app_words}."),
                (f"Connect \"{desk['backend']}\" ({desk['url']}) with widgets "
                 f"{widget_words} — and ship the app: {app_words}. Both files in "
                 "one manage_backends add."),
                (f"Build both files for \"{desk['backend']}\" at {desk['url']}. "
                 f"Widgets: {widget_words}. App: {app_words}. One add."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.widget_def_checks(desk["backend"], focus_id, focus)
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

    # ------------------------------------------------------------------ r4
    # Build + publish + instantiate + CONFIGURE + document (proxy r5:
    # without the configure step r4's operate legs were nearly free).
    t4_specs = [
        # (..., note_term, configure=(param|None to use an existing one,
        #  param_name, set_value))
        ("vol", "vix_history", ["vol_regime_metric", "vol_commentary"],
         ("Vol Command", "Vol level and regime.", "vol", "Vol"), "vol",
         (None, "window", 60)),
        ("sla", "breach_metric", ["vendor_sla_table", "sla_newsfeed"],
         ("Vendor Live", "Vendors and breaches.", "vendors", "Vendors"),
         "vendors",
         (c.text_param("desk_view", "Desk View", "summary",
                        "Which posture view the metric shows."),
          "desk_view", "detail")),
        ("tvl", "chains_table", ["gas_metric", "chains_chart"],
         ("Chain Live", "TVL and gas.", "chains", "Chains"), "chains",
         (c.text_param("chain", "Chain", "Ethereum", "Chain in focus."),
          "chain", "Solana")),
        ("healthcare", "trial_catalysts", ["catalyst_metric", "pipeline_chart"],
         ("Trial Desk", "Catalysts on tap.", "trials", "Trials"), "catalysts",
         (None, "ticker", "MRNA")),
    ]
    for desk_key, focus_id, sibling_ids, app_spec, note_term, configure in t4_specs:
        desk = c.desk(desk_key)
        focus = c.desk_widget(desk_key, focus_id)
        widgets = {focus_id: focus}
        for sib in sibling_ids:
            widgets[sib] = c.desk_widget(desk_key, sib)
        sibling_id = sibling_ids[0]
        new_param, param_name, set_value = configure
        if new_param is not None:
            focus.setdefault("params", []).append(
                json.loads(json.dumps(new_param))
            )
        app_name, app_desc, tab_id, tab_name = app_spec
        # r4 writes r3-grade content (two tabs + fanned-out convention) and
        # then operates it (proxy r3 inversion fix).
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(focus_id, 0, 0, 20, 9)]),
            ("posture", "Posture", [c.layout_item(sibling_id, 0, 0, 12, 6)]),
        ])
        dashboard_name = f"{app_name} Board"
        note_text = (
            f"{app_name} shipped from {desk['backend']}: {note_term} live."
        )
        widget_words = "; ".join(
            c.widget_requirements_text(wid, definition)
            for wid, definition in widgets.items()
        )
        convention = c.stamp_consistency(widgets)
        widget_words += f". Desk convention: {convention}"
        configure_words = (
            f"set {param_name} to {json.dumps(set_value)} on the opened "
            f"`{focus_id}` widget"
        )
        app_words = c.app_requirements_text(app)
        sid = f"{desk_key}_ship"
        c.add("apps", "r4", {
            "id": sid,
            "title": f"Ship, open, and configure the {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "orchestration"],
            "prompt": c.phrased(sid, [
                (f"End to end. Publish \"{desk['backend']}\" at {desk['url']} — "
                 f"widgets.json: {widget_words}. apps.json: {app_words}. Then "
                 f"instantiate \"{app_name}\" from that backend into a dashboard "
                 f"named \"{dashboard_name}\", {configure_words}, and leave a "
                 f"note titled \"{app_name}\" that says exactly: \"{note_text}\""),
                (f"Build, publish, open, configure, document. "
                 f"\"{desk['backend']}\" "
                 f"({desk['url']}) serves {widget_words} and ships {app_words}. "
                 f"Open the app as \"{dashboard_name}\" via manage_apps, "
                 f"{configure_words}, then a "
                 f"note \"{app_name}\" saying: \"{note_text}\""),
                (f"Four steps. One: add \"{desk['backend']}\" at {desk['url']} "
                 f"serving {widget_words}, shipping {app_words}. Two: "
                 f"instantiate \"{app_name}\" into \"{dashboard_name}\". Three: "
                 f"{configure_words}. Four: "
                 f"a note titled \"{app_name}\" with the text: \"{note_text}\""),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.APP_TOOLS + ["add_generative_widget",
                                              "update_widget"],
            "success": {
                # the apps family's focus artifact IS the app, so it stays
                # fully graded at r4 while all widgets anchor (widget-side
                # families do the inverse — see fam_aggrid r4).
                "required_widget_defs": [
                    c.widget_def_anchor_checks(desk["backend"], wid, widgets[wid])
                    for wid in widgets
                ],
                "required_app_defs": [c.app_def_checks(desk["backend"], app)],
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
