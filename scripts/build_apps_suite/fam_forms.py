"""Family FORMS - form and button parameter building."""

from __future__ import annotations

import json

from . import common as c


def _button_param(name: str, label: str) -> dict:
    return {"paramName": name, "type": "button", "label": label}


def _form_param(
    name: str,
    label: str,
    endpoint: str,
    input_params: list[dict],
    method: str = "POST",
) -> dict:
    return {
        "paramName": name, "type": "form", "label": label,
        "endpoint": endpoint, "method": method,
        "inputParams": input_params,
    }


def _form_widget(
    name: str,
    description: str,
    endpoint: str,
    form: dict,
    widget_type: str = "table",
    grid: tuple[int, int] = (20, 10),
    **extra,
) -> dict:
    return c.simple_def(
        widget_type, name, description, endpoint, grid=grid, params=[form], **extra
    )


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


def _custom_forms() -> dict[str, dict]:
    return {
        "incident_triage_form": _form_widget(
            "Incident Triage Form",
            "Submit an incident triage record for review.",
            "/incident-triage",
            _form_param("triage", "Triage", "/incident-triage-submit", [
                c.text_param("incident_id", "Incident", "INC-1042"),
                c.date_param("review_date", "Review date", "$currentDate"),
                _button_param("submit", "Submit"),
            ]),
        ),
        "access_review_form": _form_widget(
            "Access Review Form",
            "Capture an access review decision.",
            "/access-review",
            _form_param("review", "Access Review", "/access-review-submit", [
                c.text_param("user_name", "User", "analyst1"),
                c.boolean_param("approved", "Approved", False),
                _button_param("save", "Save"),
            ]),
            widget_type="markdown", grid=(12, 8),
        ),
        "threshold_update_form": _form_widget(
            "Threshold Update Form",
            "Submit a threshold change for operations.",
            "/threshold-update",
            _form_param("threshold", "Threshold", "/threshold-update-submit", [
                c.number_param("limit", "Limit", 250, minimum=0, maximum=1000),
                c.text_param("owner", "Owner", "ops"),
                _button_param("apply", "Apply"),
            ]),
        ),
        "case_escalation_form": _form_widget(
            "Case Escalation Form",
            "Escalate a surveillance case to a reviewer.",
            "/case-escalation",
            _form_param("escalation", "Escalation", "/case-escalation-submit", [
                c.text_param("case_id", "Case", "C-1042"),
                c.date_param("due_date", "Due date", "$currentDate+2d"),
                _button_param("escalate", "Escalate"),
            ]),
        ),
        "venue_exception_form": _form_widget(
            "Venue Exception Form",
            "Record an execution venue exception.",
            "/venue-exception",
            _form_param("exception", "Exception", "/venue-exception-submit", [
                c.text_param("venue", "Venue", "ARCA"),
                c.number_param("slippage_bps", "Slippage bps", 12, minimum=0),
                _button_param("record", "Record"),
            ]),
        ),
        "curve_comment_form": _form_widget(
            "Curve Comment Form",
            "Submit a curve desk comment.",
            "/curve-comment",
            _form_param("comment", "Comment", "/curve-comment-submit", [
                c.text_param("series", "Series", "DGS10"),
                c.text_param("commentary", "Commentary", "Steeper bias."),
                _button_param("post", "Post"),
            ]),
            widget_type="markdown", grid=(12, 8),
        ),
        "vendor_review_form": _form_widget(
            "Vendor Review Form",
            "Create a vendor review item.",
            "/vendor-review",
            _form_param("review", "Review", "/vendor-review-submit", [
                c.text_param("vendor_name", "Vendor", "AlphaFeed"),
                c.date_param("review_date", "Review date", "$currentDate"),
                _button_param("submit", "Submit"),
            ]),
            staleTime=900000,
        ),
        "policy_exception_form": _form_widget(
            "Policy Exception Form",
            "Submit a policy exception request.",
            "/policy-exception",
            _form_param("exception", "Exception", "/policy-exception-submit", [
                c.text_param("policy_id", "Policy", "POL-7"),
                c.text_param("owner", "Owner", "compliance"),
                _button_param("request", "Request"),
            ]),
            runButton=True,
        ),
        "trade_break_form": _form_widget(
            "Trade Break Form",
            "Record a trade break for operations review.",
            "/trade-break",
            _form_param("break_item", "Break Item", "/trade-break-submit", [
                c.text_param("trade_id", "Trade", "TR-8821"),
                c.number_param("break_amount", "Break amount", 1000, minimum=0),
                _button_param("record", "Record"),
            ]),
            refetchInterval=30000,
        ),
        "trial_readout_form": _form_widget(
            "Trial Readout Form",
            "Capture a clinical trial readout note.",
            "/trial-readout-form",
            _form_param("readout", "Readout", "/trial-readout-submit", [
                c.text_param("ticker", "Ticker", "PFE"),
                c.date_param("readout_date", "Readout date", "2026-08-19"),
                _button_param("save", "Save"),
            ]),
            category="Research",
        ),
    }


def build() -> None:
    custom = _custom_forms()

    # ------------------------------------------------------------------ t0
    # Exact widgets.json briefs for form and button param shapes.
    t0_specs = [
        ("sla", "vendor_intake_form", c.desk_widget("sla", "vendor_intake_form")),
        ("sla", "incident_triage_form", custom["incident_triage_form"]),
        ("compliance", "access_review_form", custom["access_review_form"]),
        ("execution", "threshold_update_form", custom["threshold_update_form"]),
    ]
    for desk_key, widget_id, definition in t0_specs:
        desk = c.desk(desk_key)
        definition = json.loads(json.dumps(definition))
        definition["category"] = "Workflow Forms"
        sid = f"auth_t0_forms_{widget_id}"
        brief = c.widget_requirements_text(widget_id, definition)
        c.add("forms", "t0", {
            "id": sid,
            "title": f"Build the {definition['name']} form widget",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "forms"],
            "prompt": c.phrased(sid, [
                (f"Connect a new custom backend named \"{desk['backend']}\" at "
                 f"{desk['url']}. Its widgets.json serves exactly one form widget - "
                 f"{brief}. Register it with manage_backends."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) with one "
                 f"widgets.json entry for the form: {brief}."),
                (f"Add \"{desk['backend']}\" at {desk['url']} serving this single "
                 f"form-capable widget definition: {brief}."),
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
    # Exact form widget plus a one-tab app wrapper in words.
    t1_specs = [
        ("sla", "vendor_intake_form", c.desk_widget("sla", "vendor_intake_form"),
         "Vendor Intake", "New vendor intake.", "intake", "Intake", (0, 0, 20, 10)),
        ("compliance", "case_escalation_form", custom["case_escalation_form"],
         "Case Escalation", "Escalate surveillance cases.", "cases", "Cases",
         (0, 0, 20, 10)),
        ("execution", "venue_exception_form", custom["venue_exception_form"],
         "Venue Exceptions", "Capture venue exception records.", "exceptions",
         "Exceptions", (0, 0, 20, 10)),
        ("rates", "curve_comment_form", custom["curve_comment_form"],
         "Curve Comments", "Submit curve desk comments.", "comments", "Comments",
         (0, 0, 12, 8)),
    ]
    for desk_key, widget_id, definition, app_name, app_desc, tab_id, tab_name, pos in t1_specs:
        desk = c.desk(desk_key)
        x, y, w, h = pos
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(widget_id, x, y, w, h)]),
        ])
        sid = f"auth_t1_forms_{widget_id}_app"
        brief = c.widget_requirements_text(widget_id, definition)
        wrap = (
            f"an app named \"{app_name}\" (description \"{app_desc}\") with one "
            f"tab `{tab_id}` named \"{tab_name}\" placing `{widget_id}` at "
            f"x={x} y={y} w={w} h={h}"
        )
        c.add("forms", "t1", {
            "id": sid,
            "title": f"Ship {definition['name']} as the {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "forms"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']}. widgets.json serves one form widget - {brief}. "
                 f"apps.json ships {wrap}. Publish both in one add."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) with {brief}, "
                 f"and ship that form as {wrap}."),
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
    # Words-only form requirements, field by field, plus one config dimension.
    t2_specs = [
        ("sla", "vendor_review_form", custom["vendor_review_form"],
         {"category": "Vendor Ops"}),
        ("compliance", "policy_exception_form", custom["policy_exception_form"],
         {"category": "Surveillance", "staleTime": 900000}),
        ("execution", "trade_break_form", custom["trade_break_form"],
         {"category": "Execution"}),
        ("healthcare", "trial_readout_form", custom["trial_readout_form"],
         {"staleTime": 900000}),
    ]
    for desk_key, widget_id, definition, extra in t2_specs:
        desk = c.desk(desk_key)
        definition = json.loads(json.dumps(definition))
        definition.update(extra)
        words = _policy_requirements(widget_id, definition)
        sid = f"auth_t2_forms_{widget_id}"
        c.add("forms", "t2", {
            "id": sid,
            "title": f"Compose the {definition['name']} form widget",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "forms", "composed"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']} with one widgets.json entry. Requirements: {words}."),
                (f"Build a form widget for \"{desk['backend']}\" ({desk['url']}): "
                 f"{words}. Submit it with manage_backends add."),
                (f"Publish \"{desk['backend']}\" at {desk['url']} serving a single "
                 f"form widget from these requirements: {words}."),
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
    # Form focus plus status siblings in a two-tab app.
    t3_specs = [
        ("sla", "vendor_intake_form", c.desk_widget("sla", "vendor_intake_form"),
         ["vendor_sla_table"],
         ("Vendor Intake Room", "Vendor intake and status.",
          [("intake", "Intake", [("vendor_intake_form", 0, 0, 20, 10)]),
           ("status", "Status", [("vendor_sla_table", 0, 0, 20, 9)])]),
         ("Vendor Sync",
          c.text_param("vendor_scope", "Vendor scope", "Acme Cloud",
                       "Vendor reviewed across intake and status."),
          ["vendor_intake_form", "vendor_sla_table"])),
        ("compliance", "case_escalation_form", custom["case_escalation_form"],
         ["alert_queue"],
         ("Case Intake Room", "Case escalation and alert status.",
          [("intake", "Intake", [("case_escalation_form", 0, 0, 20, 10)]),
           ("status", "Status", [("alert_queue", 0, 0, 24, 10)])]),
         ("Case Sync",
          c.text_param("case_scope", "Case scope", "C-1042",
                       "Case bundle reviewed by intake and status."),
          ["case_escalation_form", "alert_queue"])),
        ("execution", "venue_exception_form", custom["venue_exception_form"],
         ["open_orders", "exception_metric"],
         ("Exception Intake Room", "Venue exceptions and order status.",
          [("intake", "Intake", [("venue_exception_form", 0, 0, 20, 10),
                                  ("exception_metric", 20, 0, 8, 6)]),
           ("status", "Status", [("open_orders", 0, 0, 20, 9)])]),
         ("Venue Sync",
          c.text_param("venue_scope", "Venue scope", "ARCA",
                       "Venue reviewed across intake and status."),
          ["venue_exception_form", "open_orders"])),
        ("healthcare", "trial_readout_form", custom["trial_readout_form"],
         ["trial_catalysts", "catalyst_metric"],
         ("Trial Intake Room", "Trial readouts and catalyst status.",
          [("intake", "Intake", [("trial_readout_form", 0, 0, 20, 10),
                                  ("catalyst_metric", 20, 0, 8, 6)]),
           ("status", "Status", [("trial_catalysts", 0, 0, 20, 9)])]),
         ("Trial Sync",
          c.endpoint_param("trial_ticker", "Trial ticker", "PFE", "/tickers"),
          ["trial_readout_form", "trial_catalysts"])),
    ]
    for desk_key, focus_id, focus, sibling_ids, app_spec, shared_spec in t3_specs:
        desk = c.desk(desk_key)
        widgets = {focus_id: json.loads(json.dumps(focus))}
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
        sid = f"auth_t3_forms_{app_name.lower().replace(' ', '_')}"
        c.add("forms", "t3", {
            "id": sid,
            "title": f"Assemble the {app_name} form app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "forms", "multi-tab"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then publish \"{desk['backend']}\" at "
                 f"{desk['url']} in one add. widgets.json serves: {widget_words}. "
                 f"apps.json ships {app_words}."),
                (f"Connect \"{desk['backend']}\" ({desk['url']}) with widgets "
                 f"{widget_words}. Ship the two-tab form app: {app_words}."),
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
                    c.widget_def_anchor_checks(desk["backend"], sid_id, widgets[sid_id])
                    for sid_id in sibling_ids
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
    # Build, publish, instantiate, configure, and document a form pack.
    t4_specs = [
        ("sla", "vendor_intake_form", c.desk_widget("sla", "vendor_intake_form"),
         ["breach_metric", "vendor_sla_table"],
         ("Vendor Intake Live", "Vendor intake and breach count.", "intake", "Intake"),
         "vendor intake",
         (c.text_param("vendor_scope", "Vendor Scope", "AlphaFeed",
                       "Vendor intake filter."),
          "vendor_scope", "QuoteStream")),
        ("compliance", "case_escalation_form", custom["case_escalation_form"],
         ["alert_metric", "alert_queue"],
         ("Case Intake Live", "Case escalation and alert count.", "cases", "Cases"),
         "case intake",
         (c.text_param("case_scope", "Case Scope", "C-1042",
                       "Case intake filter."),
          "case_scope", "C-1044")),
        ("execution", "venue_exception_form", custom["venue_exception_form"],
         ["exception_metric", "open_orders"],
         ("Exception Intake Live", "Venue exceptions and exception count.",
          "exceptions", "Exceptions"),
         "exception intake",
         (c.text_param("venue_scope", "Venue Scope", "ARCA",
                       "Venue exception filter."),
          "venue_scope", "EDGX")),
        ("healthcare", "trial_readout_form", custom["trial_readout_form"],
         ["catalyst_metric", "trial_catalysts"],
         ("Trial Intake Live", "Trial readouts and catalyst count.", "trials", "Trials"),
         "trial intake",
         (c.text_param("ticker_scope", "Ticker Scope", "PFE",
                       "Trial readout ticker filter."),
          "ticker_scope", "MRNA")),
    ]
    for desk_key, focus_id, focus, sibling_ids, app_spec, note_term, configure in t4_specs:
        desk = c.desk(desk_key)
        focus = json.loads(json.dumps(focus))
        widgets = {focus_id: focus}
        for sibling_id in sibling_ids:
            widgets[sibling_id] = c.desk_widget(desk_key, sibling_id)
        sibling_id = sibling_ids[0]
        sibling = widgets[sibling_id]
        config_param, param_name, set_value = configure
        focus.setdefault("params", []).append(json.loads(json.dumps(config_param)))
        app_name, app_desc, tab_id, tab_name = app_spec
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(focus_id, 0, 0, 20, 10)]),
            ("status", "Status", [c.layout_item(sibling_id, 0, 0, 8, 6)]),
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
        sid = f"auth_t4_forms_{desk_key}_ship"
        c.add("forms", "t4", {
            "id": sid,
            "title": f"Ship, open, and configure the {app_name} form app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "forms", "orchestration"],
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
