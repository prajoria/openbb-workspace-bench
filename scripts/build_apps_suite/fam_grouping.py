"""Family GROUPING - app param groups and cell-click groupBy wiring."""

from __future__ import annotations

import json

from . import common as c


def _group(name: str, param_name: str, widget_ids: list[str]) -> dict:
    return {
        "name": name, "type": "param",
        "paramName": param_name, "widgetIds": widget_ids,
    }


def _symbol_click_table(
    name: str,
    description: str,
    endpoint: str,
    grid: tuple[int, int] | None = (20, 9),
) -> dict:
    definition = {
        "name": name,
        "description": description,
        "endpoint": endpoint,
        "type": "table",
        "params": [c.endpoint_param("symbol", "Symbol", "AAPL", "/symbols")],
        "data": {"table": {"columnsDefs": [
            {
                "field": "symbol", "headerName": "Symbol", "cellDataType": "text",
                "renderFn": "cellOnClick",
                "renderFnParams": {
                    "actionType": "groupBy",
                    "groupByParamName": "symbol",
                },
                "cellOnClick": {
                    "actionType": "groupBy",
                    "groupByParamName": "symbol",
                },
            },
            {
                "field": "revision_pct", "headerName": "Revision %",
                "cellDataType": "number", "formatterFn": "percent",
            },
        ]}},
    }
    if grid:
        definition["gridData"] = {"w": grid[0], "h": grid[1]}
    return definition


def build() -> None:
    # ------------------------------------------------------------------ r0
    # Seeded earnings widgets; build only apps.json with an exact group brief.
    t0_specs = [
        (["estimate_revisions", "earnings_chart"],
         "Earnings Symbol Board", "Revisions and EPS history synced by symbol.",
         "review", "Review", "Symbol Sync"),
        (["estimate_revisions", "earnings_note"],
         "Revision Note Board", "Revisions and preview note synced by symbol.",
         "notes", "Notes", "Revision Symbol Sync"),
        (["earnings_chart", "earnings_note"],
         "Chart Note Board", "Chart and preview note synced by symbol.",
         "preview", "Preview", "Preview Symbol Sync"),
        (["estimate_revisions", "earnings_chart"],
         "NVDA Review Board", "A second symbol-synced earnings review.",
         "nvda", "NVDA", "NVDA Symbol Sync"),
    ]
    for widget_ids, app_name, app_desc, tab_id, tab_name, group_name in t0_specs:
        desk = c.desk("earnings")
        widgets = {wid: c.desk_widget("earnings", wid) for wid in widget_ids}
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [
                c.layout_item(widget_ids[0], 0, 0, 20, 9),
                c.layout_item(widget_ids[1], 20, 0, 12, 9),
            ]),
        ], groups=[_group(group_name, "symbol", widget_ids)])
        sid = f"{app_name.lower().replace(' ', '_')}"
        brief = c.app_requirements_text(app)
        c.add("grouping", "r0", {
            "id": sid,
            "title": f"Build the grouped {app_name} app definition",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "apps-json", "grouping"],
            "prompt": c.phrased(sid, [
                (f"Your backend \"{desk['backend']}\" is already connected and "
                 f"serves {', '.join(f'`{w}`' for w in widget_ids)}. Ship its "
                 f"apps.json - exactly one grouped app: {brief}. Submit it with "
                 "manage_backends refresh (apps_json)."),
                (f"Add apps.json to the connected backend \"{desk['backend']}\" "
                 f"(already serving {', '.join(f'`{w}`' for w in widget_ids)}): "
                 f"{brief}. Use operation refresh with apps_json."),
                (f"The widgets are served; build the missing grouped app file "
                 f"for \"{desk['backend']}\". apps.json contains one app: {brief}."),
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
    # Build one widget and wrap it in a one-tab app with a group.
    t1_widgets = [
        ("estimate_revisions", c.desk_widget("earnings", "estimate_revisions"),
         "Revision Group App", "Grouped revisions by symbol.",
         "revisions", "Revisions", "Revision Symbol Group"),
        ("earnings_chart", c.desk_widget("earnings", "earnings_chart"),
         "Chart Group App", "Grouped EPS chart by symbol.",
         "chart", "Chart", "Chart Symbol Group"),
        ("earnings_note", c.desk_widget("earnings", "earnings_note"),
         "Preview Group App", "Grouped earnings preview by symbol.",
         "preview", "Preview", "Preview Symbol Group"),
        ("symbol_click_summary",
         _symbol_click_table(
             "Symbol Click Summary",
             "Symbol rows that can drive a grouped app.",
             "/symbol-click-summary",
         ),
         "Click Group App", "Clickable symbol rows in a grouped app.",
         "clicks", "Clicks", "Click Symbol Group"),
    ]
    for widget_id, definition, app_name, app_desc, tab_id, tab_name, group_name in t1_widgets:
        desk = c.desk("earnings")
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [c.layout_item(widget_id, 0, 0, 20, 9)]),
        ], groups=[_group(group_name, "symbol", [widget_id])])
        sid = f"{widget_id}_app"
        brief = c.widget_requirements_text(widget_id, definition)
        app_words = c.app_requirements_text(app)
        c.add("grouping", "r1", {
            "id": sid,
            "title": f"Ship {definition['name']} with a grouping app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "grouping"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then connect \"{desk['backend']}\" at "
                 f"{desk['url']}. widgets.json serves one widget - {brief}. "
                 f"apps.json ships {app_words}. Publish both in one add."),
                (f"Register \"{desk['backend']}\" ({desk['url']}) with {brief}, "
                 f"and wrap it in a grouped app: {app_words}."),
                (f"Build widgets.json ({brief}) and apps.json ({app_words}) for "
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

    # ------------------------------------------------------------------ r2
    # Seeded widgets; words-only app requirements always include a group and preset.
    t2_specs = [
        (["estimate_revisions", "earnings_chart"], "Earnings Review Sync",
         "Preset chart with synced revisions.", "review", "Review",
         {"earnings_chart": {"symbol": "NVDA"}}, "Review Symbol Sync",
         "Summarize the synced NVDA revision signal."),
        (["estimate_revisions", "earnings_note"], "Revision Preview Sync",
         "Preset preview note with synced revisions.", "preview", "Preview",
         {"earnings_note": {"symbol": "MSFT"}}, "Preview Symbol Sync",
         "Draft a preview note for the synced symbol."),
        (["earnings_chart", "earnings_note"], "Chart Preview Sync",
         "Preset chart and preview note.", "chart", "Chart",
         {"earnings_chart": {"symbol": "AAPL"}}, "Chart Symbol Sync",
         "Compare the chart and preview for the synced symbol."),
        (["estimate_revisions", "earnings_chart", "earnings_note"],
         "Full Earnings Sync", "Three earnings widgets synced by symbol.",
         "full", "Full",
         {"estimate_revisions": {"symbol": "NVDA"}}, "Full Symbol Sync",
         "List the main synced earnings takeaway."),
    ]
    for (
        widget_ids, app_name, app_desc, tab_id, tab_name, presets, group_name,
        prompt,
    ) in t2_specs:
        desk = c.desk("earnings")
        initial_widgets = {wid: c.desk_widget("earnings", wid) for wid in widget_ids}
        widgets = {
            wid: json.loads(json.dumps(definition))
            for wid, definition in initial_widgets.items()
        }
        policy_target = widget_ids[0]
        policy_config, policy_clause = c.cache_policy(15)
        widgets[policy_target].update(policy_config)
        policy_key = next(iter(policy_config))
        positions = [(0, 0, 20, 9), (20, 0, 12, 9), (32, 0, 8, 6)]
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [
                c.layout_item(wid, *positions[index], params=presets.get(wid))
                for index, wid in enumerate(widget_ids)
            ]),
        ], groups=[_group(group_name, "symbol", widget_ids)], prompts=[prompt])
        sid = f"{app_name.lower().replace(' ', '_')}"
        app_words = c.app_requirements_text(app)
        c.add("grouping", "r2", {
            "id": sid,
            "title": f"Compose the grouped {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "grouping", "composed"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace. \"{desk['backend']}\" already serves "
                 f"{', '.join(f'`{w}`' for w in widget_ids)}. Refresh widgets_json "
                 f"so `{policy_target}` {policy_clause}. {c.CONFIG_RULES} Build "
                 f"apps.json with one grouped app: {app_words}. Refresh the backend."),
                (f"Build the grouped apps.json for \"{desk['backend']}\" "
                 f"({desk['url']}) over served widgets "
                 f"{', '.join(f'`{w}`' for w in widget_ids)}: {app_words}. Also "
                 f"refresh widgets_json so `{policy_target}` {policy_clause}. "
                 f"{c.CONFIG_RULES}"),
                (f"One grouped app to ship on \"{desk['backend']}\": {app_words}. "
                 f"The widgets are already served - submit apps_json and refresh "
                 f"widgets_json so `{policy_target}` {policy_clause}. {c.CONFIG_RULES}"),
            ]),
            "fixtures": {},
            "initial_state": c.seeded_custom(desk["backend"], desk["url"], initial_widgets),
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.anchor_with_expect(
                        desk["backend"], policy_target, widgets[policy_target],
                        policy_key,
                    )
                ],
                "required_app_defs": [c.app_def_checks(desk["backend"], app)],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.snap(),
                c.refresh_call("backend_001", widgets=widgets, apps=[app]),
            ],
        })

    # ------------------------------------------------------------------ r3
    # Multi-widget, two-tab apps with a group spanning tabs and a cell-click table.
    t3_specs = [
        ("click_revision_table",
         _symbol_click_table("Click Revision Table",
                             "Revision rows whose symbol cell syncs the app.",
                             "/click-revision-table"),
         ["earnings_chart"],
         ("Click Revision Desk", "Clickable revisions and EPS history.",
          [("table", "Table", [("click_revision_table", 0, 0, 20, 9)]),
           ("chart", "Chart", [("earnings_chart", 0, 0, 20, 9)])],
          "Click Revision Sync")),
        ("click_preview_table",
         _symbol_click_table("Click Preview Table",
                             "Preview rows whose symbol cell syncs the app.",
                             "/click-preview-table"),
         ["earnings_note"],
         ("Click Preview Desk", "Clickable preview rows and notes.",
          [("table", "Table", [("click_preview_table", 0, 0, 20, 9)]),
           ("note", "Note", [("earnings_note", 0, 0, 12, 8)])],
          "Click Preview Sync")),
        ("click_summary_table",
         _symbol_click_table("Click Summary Table",
                             "Summary rows whose symbol cell syncs every tab.",
                             "/click-summary-table", grid=None),
         ["earnings_chart", "earnings_note"],
         ("Click Summary Desk", "Clickable summary, chart, and note.",
          [("summary", "Summary", [("click_summary_table", 0, 0, 20, 9),
                                    ("earnings_note", 20, 0, 12, 8)]),
           ("chart", "Chart", [("earnings_chart", 0, 0, 20, 9)])],
          "Click Summary Sync")),
        ("click_season_table",
         _symbol_click_table("Click Season Table",
                             "Season rows whose symbol cell syncs revisions.",
                             "/click-season-table", grid=None),
         ["estimate_revisions", "earnings_chart"],
         ("Click Season Desk", "Clickable season rows, revisions, and chart.",
          [("season", "Season", [("click_season_table", 0, 0, 20, 9),
                                  ("estimate_revisions", 20, 0, 20, 9)]),
           ("chart", "Chart", [("earnings_chart", 0, 0, 20, 9)])],
          "Click Season Sync")),
    ]
    for focus_id, focus, sibling_ids, app_spec in t3_specs:
        desk = c.desk("earnings")
        widgets = {focus_id: focus}
        for sibling_id in sibling_ids:
            widgets[sibling_id] = c.desk_widget("earnings", sibling_id)
        app_name, app_desc, tab_specs, group_name = app_spec
        all_ids = [focus_id] + sibling_ids
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name,
             [c.layout_item(wid, x, y, w, h) for wid, x, y, w, h in items])
            for tab_id, tab_name, items in tab_specs
        ], groups=[_group(group_name, "symbol", all_ids)])
        click_note = (
            "The `symbol` column's cell-click action must group by the shared "
            "`symbol` param."
        )
        widget_words = [c.widget_requirements_text(focus_id, focus), click_note]
        widget_words.extend(
            c.widget_requirements_text(sibling_id, widgets[sibling_id])
            for sibling_id in sibling_ids
        )
        app_words = c.app_requirements_text(app)
        sid = f"{app_name.lower().replace(' ', '_')}"
        c.add("grouping", "r3", {
            "id": sid,
            "title": f"Assemble the grouped {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "grouping", "cell-click"],
            "prompt": c.phrased(sid, [
                (f"Check the workspace, then publish \"{desk['backend']}\" at "
                 f"{desk['url']} in one add. widgets.json serves: "
                 f"{'; '.join(widget_words)}. apps.json ships {app_words}."),
                (f"Connect \"{desk['backend']}\" ({desk['url']}) with widgets "
                 f"{'; '.join(widget_words)}. Ship the grouped app: {app_words}."),
                (f"Build both files for \"{desk['backend']}\" at {desk['url']}. "
                 f"Widgets: {'; '.join(widget_words)}. App: {app_words}. One add."),
            ]),
            "fixtures": {},
            "initial_state": {},
            "allowed_tools": c.BUILD_TOOLS,
            "success": {
                "required_widget_defs": [
                    c.widget_def_checks(desk["backend"], focus_id, focus)
                ] + [
                    c.widget_def_anchor_checks(desk["backend"], sibling_id, widgets[sibling_id])
                    for sibling_id in sibling_ids
                ],
                "required_app_defs": [c.app_def_checks(desk["backend"], app)],
                "trace_checks": dict(c.TRACE_ZERO),
            },
            "oracle_tool_calls": [
                c.snap(),
                c.add_backend_call(desk["backend"], desk["url"], widgets, apps=[app]),
            ],
        })

    # ------------------------------------------------------------------ r4
    # Publish a grouped app, instantiate it, configure it, and leave a note.
    t4_specs = [
        ("estimate_revisions", c.desk_widget("earnings", "estimate_revisions"),
         ["earnings_chart", "earnings_note"],
         ("Earnings Sync Live", "Live grouped revisions and EPS history.",
          "review", "Review", "Live Symbol Sync"),
         "symbol sync",
         ("symbol", "MSFT")),
        ("earnings_note", c.desk_widget("earnings", "earnings_note"),
         ["estimate_revisions", "earnings_chart"],
         ("Preview Sync Live", "Live grouped preview and revisions.",
          "preview", "Preview", "Preview Symbol Sync"),
         "preview sync",
         ("symbol", "AAPL")),
        ("earnings_chart", c.desk_widget("earnings", "earnings_chart"),
         ["earnings_note", "estimate_revisions"],
         ("Chart Sync Live", "Live grouped chart and preview.",
          "chart", "Chart", "Chart Symbol Sync"),
         "linked earnings selection",
         ("symbol", "MSFT")),
        ("click_live_table",
         _symbol_click_table("Click Live Table",
                             "Clickable live symbol rows for grouped review.",
                             "/click-live-table"),
         ["earnings_chart", "earnings_note"],
         ("Click Sync Live", "Live grouped click table and chart.",
          "clicks", "Clicks", "Click Live Sync"),
         "click sync",
         ("symbol", "AAPL")),
    ]
    for focus_id, focus, sibling_ids, app_spec, note_term, configure in t4_specs:
        desk = c.desk("earnings")
        widgets = {focus_id: focus}
        for sibling_id in sibling_ids:
            widgets[sibling_id] = c.desk_widget("earnings", sibling_id)
        sibling_id = sibling_ids[0]
        param_name, set_value = configure
        app_name, app_desc, tab_id, tab_name, group_name = app_spec
        app = c.app_def(app_name, app_desc, tabs=[
            (tab_id, tab_name, [
                c.layout_item(focus_id, 0, 0, 20, 9, params={"symbol": "NVDA"}),
            ]),
            ("linked", "Linked", [c.layout_item(sibling_id, 0, 0, 12, 9)]),
        ], groups=[_group(group_name, "symbol", [focus_id, sibling_id])])
        dashboard_name = f"{app_name} Board"
        note_text = f"{app_name} is live from {desk['backend']}: {note_term} ready."
        widget_words = "; ".join(
            c.widget_requirements_text(wid, definition)
            for wid, definition in widgets.items()
        )
        configure_words = (
            f"set {param_name} to {json.dumps(set_value)} on the opened "
            f"`{focus_id}` widget"
        )
        app_words = c.app_requirements_text(app)
        sid = f"{app_name.lower().replace(' ', '_')}"
        c.add("grouping", "r4", {
            "id": sid,
            "title": f"Ship, open, and configure the grouped {app_name} app",
            "workflow": desk["workflow"], "subdomain": desk["subdomain"],
            "tags": ["build-openbb-apps", "widgets-json", "apps-json", "grouping", "orchestration"],
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
