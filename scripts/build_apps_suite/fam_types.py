"""Family TYPES — content and embed widget types.

Owns widget types: markdown, metric, pdf, html, iframe, youtube, newsfeed,
multi_file_viewer.
"""

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
    # ------------------------------------------------------------------ t0
    # Exact widget-definition briefs for four owned content/embed types.
    t0_specs = [
        ("vol", "vol_commentary"),
        ("tvl", "gas_metric"),
        ("execution", "venue_pdf"),
        ("tvl", "chains_heatmap_html"),
    ]
    for desk_key, widget_id in t0_specs:
        desk = c.desk(desk_key)
        definition = c.desk_widget(desk_key, widget_id)
        if widget_id == "vol_commentary":
            definition["staleTime"] = 900000
        elif widget_id == "gas_metric":
            definition.update({"staleTime": 900000, "runButton": True})
        elif widget_id == "venue_pdf":
            definition.update({"staleTime": 1800000, "category": "Execution Reports"})
        elif widget_id == "chains_heatmap_html":
            definition.update({"staleTime": 900000, "category": "Network Ops"})
        sid = f"auth_t0_types_{widget_id}"
        brief = c.widget_requirements_text(widget_id, definition)
        c.add("types", "t0", {
            "id": sid,
            "title": f"Build the {definition['name']} {definition.get('type', 'table')} widget",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "types"],
            "prompt": c.phrased(sid, [
                (f"Connect a new custom backend named \"{desk['backend']}\" at "
                 f"{desk['url']}. Its widgets.json serves exactly one content "
                 f"widget — {brief}. Register it with manage_backends."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) with one "
                 f"widgets.json entry: {brief}. Use a single manage_backends add."),
                (f"You wrote a backend at {desk['url']}. Add it as "
                 f"\"{desk['backend']}\" serving this exact widgets.json entry — "
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

    # ------------------------------------------------------------------ t1
    # Four more owned types shipped as one-tab apps. The widget is anchored;
    # the app wrapper is fully graded.
    t1_specs = [
        ("rates", "curve_monitor_iframe", "Curve Monitor", "Embedded curve monitor.",
         "monitor", "Monitor", (0, 0, 24, 16)),
        ("sla", "sla_newsfeed", "Vendor Notices", "Vendor incident notices.",
         "notices", "Notices", (0, 0, 12, 10)),
        ("earnings", "earnings_calls_video", "Replay Room", "Earnings call replays.",
         "replays", "Replays", (0, 0, 20, 12)),
        ("compliance", "evidence_files", "Evidence Browser", "Case evidence files.",
         "evidence", "Evidence", (0, 0, 20, 14)),
    ]
    for desk_key, widget_id, app_name, app_desc, tab_id, tab_name, pos in t1_specs:
        desk = c.desk(desk_key)
        definition = c.desk_widget(desk_key, widget_id)
        x, y, w, h = pos
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(widget_id, x, y, w, h)]),
        ])
        sid = f"auth_t1_types_{widget_id}_app"
        brief = c.widget_requirements_text(widget_id, definition)
        wrap = (
            f"an app named \"{app_name}\" (description \"{app_desc}\") with a "
            f"single tab `{tab_id}` named \"{tab_name}\" that places "
            f"`{widget_id}` at x={x} y={y} w={w} h={h}"
        )
        c.add("types", "t1", {
            "id": sid,
            "title": f"Ship {definition['name']} as the {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "types"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']}. Its widgets.json serves one widget — {brief}. "
                 f"Its apps.json ships {wrap}. Publish both in the same "
                 "manage_backends add."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) serving "
                 f"{brief}, and ship it as {wrap}. One add should include both "
                 "widgets.json and apps.json."),
                (f"Build both files for \"{desk['backend']}\" at {desk['url']}: "
                 f"widgets.json with {brief}, apps.json with {wrap}. Then add "
                 "the backend."),
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
    # Words-only composed widget requirements. Each cell keeps one artifact but
    # composes type + params/settings/source dimensions.
    t2_specs = [
        ("vol", "vol_playbook_note",
         c.simple_def(
             "markdown", "Vol Playbook Note", "Markdown playbook for the vol desk.",
             "/vol-playbook", grid=(12, 8),
             params=[c.text_param("section", "Section", "morning",
                                  "Playbook section to open.")],
             staleTime=900000,
             category="Volatility",
         )),
        ("tvl", "gas_priority_metric",
         c.simple_def(
             "metric", "Gas Priority", "Priority gas fee monitor.",
             "/gas-priority", grid=(6, 4),
             category="Network Ops", refetchInterval=30000, runButton=True,
         )),
        ("compliance", "policy_digest_pdf",
         c.simple_def(
             "pdf", "Policy Digest PDF", "Current surveillance policy digest.",
             "/policy-digest-pdf", grid=(16, 14),
             source="/policy/digest.pdf", staleTime=1800000,
             category="Surveillance",
         )),
        ("earnings", "call_replay_video",
         c.simple_def(
             "youtube", "Call Replay Video", "Selected earnings replay video.",
             "/call-replay-video", grid=(20, 12),
             params=[c.endpoint_param("video", "Video", "q1-call",
                                      "/call-video-options")],
             staleTime=900000, category="Earnings Media",
         )),
    ]
    for desk_key, widget_id, definition in t2_specs:
        desk = c.desk(desk_key)
        sid = f"auth_t2_types_{widget_id}"
        words = _policy_requirements(widget_id, definition)
        c.add("types", "t2", {
            "id": sid,
            "title": f"Compose the {definition['name']} content widget",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "types", "composed"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']} with one widgets.json entry described in words: "
                 f"{words}. Publish it with manage_backends add."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) serving a "
                 f"single composed content widget: {words}. Submit the widget "
                 "definition in widgets_json."),
                (f"Build the widgets.json for \"{desk['backend']}\" at "
                 f"{desk['url']}. It has exactly one entry, {words}. Then add "
                 "the backend."),
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
    # Multi-widget, multi-tab content apps in words. Focus is full; siblings
    # anchor; app is full. Each room adds a factored shared param group as the
    # t3 composition dimension.
    t3_specs = [
        ("compliance", "case_notes", ["policy_pdf"],
         ("Case Research Room", "Case notes and policy digest.",
          [("notes", "Notes", [("case_notes", 0, 0, 12, 8)]),
           ("policy", "Policy", [("policy_pdf", 0, 0, 16, 14)])]),
         ("Case Sync",
          c.text_param("case_scope", "Case scope", "C-1042",
                       "Case bundle reviewed across the room."),
          ["case_notes", "policy_pdf"])),
        ("healthcare", "fda_newsfeed", ["catalyst_metric"],
         ("Catalyst Wire", "FDA notices and catalyst count.",
          [("wire", "Wire", [("fda_newsfeed", 0, 0, 12, 10)]),
           ("metrics", "Metrics", [("catalyst_metric", 0, 0, 6, 4)])]),
         ("Therapy Sync",
          c.text_param("therapy_area", "Therapy area", "Oncology",
                       "Therapy area for the catalyst wire."),
          ["fda_newsfeed", "catalyst_metric"])),
        ("earnings", "earnings_calls_video", ["earnings_note", "surprise_metric"],
         ("Media Research Room", "Replays, previews, and surprise posture.",
          [("replays", "Replays", [("earnings_calls_video", 0, 0, 20, 12),
                                      ("surprise_metric", 20, 0, 6, 4)]),
           ("preview", "Preview", [("earnings_note", 0, 0, 12, 8)])]),
         ("Symbol Sync",
          c.endpoint_param("symbol_scope", "Symbol scope", "AAPL", "/symbols"),
          ["earnings_calls_video", "earnings_note"])),
        ("compliance", "evidence_files", ["case_notes", "alert_metric"],
         ("Evidence Hub", "Evidence, notes, and alert posture.",
          [("evidence", "Evidence", [("evidence_files", 0, 0, 20, 14),
                                        ("alert_metric", 20, 0, 6, 4)]),
           ("notes", "Notes", [("case_notes", 0, 0, 12, 8)])]),
         ("Evidence Sync",
          c.text_param("case_scope", "Case scope", "C-1042",
                       "Case bundle used by the evidence room."),
          ["evidence_files", "case_notes"])),
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
        sid = f"auth_t3_types_{focus_id}_room"
        c.add("types", "t3", {
            "id": sid,
            "title": f"Assemble the {app_name} content app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "types", "multi-tab"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then publish \"{desk['backend']}\" at "
                 f"{desk['url']} in one add. widgets.json serves: {widget_words}. "
                 f"apps.json ships {app_words}."),
                (f"Connect \"{desk['backend']}\" ({desk['url']}) with widgets "
                 f"{widget_words}. Ship the multi-tab app too: {app_words}. One "
                 "manage_backends add."),
                (f"Build both files for \"{desk['backend']}\" at {desk['url']}. "
                 f"Widgets: {widget_words}. App: {app_words}. Publish both "
                 "together."),
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

    # ------------------------------------------------------------------ t4
    # Build a content pack, instantiate the app, configure it, and add the exact note.
    t4_specs = [
        ("compliance", "evidence_files", ["alert_metric", "case_notes"],
         ("Evidence Live", "Evidence files, alerts, and notes.", "evidence", "Evidence"),
         "evidence",
         (None, "file", ["case-pack.pdf"])),
        ("sla", "sla_newsfeed", ["breach_metric", "vendor_sla_table"],
         ("Vendor Notice Room", "Vendor notices and breach count.", "notices", "Notices"),
         "notices",
         (c.text_param("vendor", "Vendor", "AlphaFeed",
                       "Vendor filter for notices."),
          "vendor", "QuoteStream")),
        ("compliance", "policy_digest_pdf", ["alert_queue", "case_notes"],
         ("Policy Digest Live", "Policy PDF, alert queue, and case notes.",
          "policy", "Policy"),
         "policy digest",
         (None, "case_scope", "C-2099")),
        ("execution", "venue_packet_pdf", ["exception_metric", "open_orders"],
         ("Venue Packet Live", "Venue PDF, exceptions, and open orders.",
          "venue", "Venue"),
         "venue packet",
         (None, "venue", "EDGX")),
    ]
    custom_t4 = {
        "policy_digest_pdf": c.simple_def(
            "pdf", "Policy Digest PDF", "Current surveillance policy digest.",
            "/policy-digest-pdf", grid=(16, 14),
            params=[c.text_param("case_scope", "Case scope", "C-1042",
                                 "Case bundle for the policy review.")],
            source="/policy/digest.pdf", staleTime=1800000,
            category="Surveillance",
        ),
        "venue_packet_pdf": c.simple_def(
            "pdf", "Venue Packet PDF", "Monthly venue scorecard packet.",
            "/venue-packet-pdf", grid=(16, 14),
            params=[c.endpoint_param("venue", "Venue", "ARCA",
                                     "/venue-options")],
            source="/reports/venue-scorecard.pdf", staleTime=1800000,
            category="Execution Reports",
        ),
    }
    for desk_key, focus_id, sibling_ids, app_spec, note_term, configure in t4_specs:
        desk = c.desk(desk_key)
        focus = custom_t4.get(focus_id) or c.desk_widget(desk_key, focus_id)
        widgets = {focus_id: focus}
        for sibling_id in sibling_ids:
            widgets[sibling_id] = c.desk_widget(desk_key, sibling_id)
        sibling_id = sibling_ids[0]
        new_param, param_name, set_value = configure
        if new_param is not None:
            focus.setdefault("params", []).append(json.loads(json.dumps(new_param)))
        app_name, app_desc, tab_id, tab_name = app_spec
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(focus_id, 0, 0, 20, 12)]),
            ("signals", "Signals", [c.layout_item(sibling_id, 0, 0, 8, 5)]),
        ])
        dashboard_name = f"{app_name} Live"
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
        sid = f"auth_t4_types_{focus_id}_ship"
        c.add("types", "t4", {
            "id": sid,
            "title": f"Ship, open, and configure the {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "types",
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
                 f"record a note \"{app_name}\" saying: \"{note_text}\""),
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
