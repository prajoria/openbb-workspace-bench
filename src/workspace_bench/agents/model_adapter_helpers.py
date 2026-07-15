"""Shared prompt helpers for model comparison adapters."""

from __future__ import annotations

import re
from typing import Any


FIXTURE_ORIGINS = {
    "equities": "Bench Equities",
    "macro": "Bench Macro",
    "portfolio": "Bench Portfolio",
    "stark-enterprise": "Bench Stark Enterprise",
    "stark-enterprise-x": "Bench Stark Enterprise",
    "stark-enterprise-y": "Bench Stark Enterprise",
    "daloopa": "Bench Daloopa",
    "support-daloopa-skills": "Bench Daloopa",
    "getting-started": "Getting Started",
    "widget-examples": "Widget Examples",
}

TOOL_REFERENCE = {
    "get_workspace_snapshot": {
        "description": "Inspect the current dashboard composition, dashboard summaries, and skills. Discover backends via manage_backends or list_available_widgets.",
        "args": {},
    },
    "manage_dashboard": {
        "description": "Create, read, or rename dashboards.",
        "args": {
            "operation": "create|read|update",
            "name": "string, required for create/update",
            "dashboard_id": "string, required for update; optional otherwise",
            "activate": "boolean, optional for create",
        },
    },
    "manage_navigation_bar": {
        "description": "Create, add, remove, or rename dashboard tabs.",
        "args": {
            "operation": "create|add_tabs|remove_tabs|rename_tabs",
            "tabs": [{"name": "Tab Name"}],
            "rename_map": {"old-tab-id": "New Name"},
            "dashboard_id": "string, optional",
        },
    },
    "navigate_workspace": {
        "description": "Switch active dashboard or tab.",
        "args": {
            "operation": "dashboard|tab",
            "dashboard_id": "string, optional for tab, required for dashboard",
            "tab_id": "string, optional for dashboard, required for tab",
        },
    },
    "list_available_widgets": {
        "description": "List widgets for a backend origin such as Bench Equities.",
        "args": {"origin": "string, optional", "backend_id": "string, optional"},
    },
    "get_widget_schema": {
        "description": "Get schema for one listed widget.",
        "args": {"origin": "string", "widget_id": "string"},
    },
    "get_params_options": {
        "description": "Fetch options for a schema parameter that requires lookup.",
        "args": {
            "origin": "string",
            "widget_id": "string",
            "param_name": "string",
            "data_args": "object, optional",
        },
    },
    "get_widget_data": {
        "description": "Fetch fixture data for one widget.",
        "args": {
            "origin": "string",
            "widget_id": "string",
            "data_args": "object, optional",
        },
    },
    "create_widget": {
        "description": "Create a regular Workspace widget.",
        "args": {
            "origin": "string",
            "widget_id": "string",
            "data_args": "object, optional",
            "ui_args": "object, optional",
            "dashboard_id": "string, optional",
        },
    },
    "update_widget": {
        "description": "Update widget data_args or ui_args. Do not use for layout.",
        "args": {
            "widget_uuid": "string, preferred when known",
            "widget_id": "string, only when exactly one exists",
            "data_args": "object, optional",
            "ui_args": "object, optional",
            "dashboard_id": "string, optional",
        },
    },
    "update_widget_layout": {
        "description": "Move or resize one widget.",
        "args": {
            "widget_uuid": "string, preferred when known",
            "widget_id": "string, only when exactly one exists",
            "x": "number",
            "y": "number",
            "w": "number",
            "h": "number",
            "tab_id": "string, optional",
            "dashboard_id": "string, optional",
        },
    },
    "delete_widget": {
        "description": "Delete one widget.",
        "args": {
            "widget_uuid": "string, preferred when known",
            "widget_id": "string, only when exactly one exists",
            "dashboard_id": "string, optional",
        },
    },
    "add_generative_widget": {
        "description": "Add generated note, table, chart, or HTML widget.",
        "args": {
            "widget_type": "note|table|chart|html",
            "name": "string, optional",
            "data": "string for note/html; array for table/chart",
            "description": "string, optional",
            "chart_params": "object with chartType, xKey, yKey for chart",
            "inner_tab": "string tab id, optional",
            "dashboard_id": "string UUID from tool result only, optional; omit for active dashboard",
        },
    },
    "read_widget": {
        "description": "Read one existing widget.",
        "args": {
            "widget_uuid": "string, preferred when known",
            "widget_id": "string, only when exactly one exists",
            "dashboard_id": "string, optional",
        },
    },
    "manage_backends": {
        "description": (
            "List, add, or refresh backends. operation='add' with widgets_json "
            "registers a CUSTOM backend you author: widgets_json is the "
            "widgets.json object map your backend serves (each widget definition "
            "REQUIRES name, description, and endpoint; optional type from the "
            "workspace enum table|markdown|chart|chart-highcharts|chart-vegalite|"
            "metric|pdf|html|newsfeed|omni|live_grid|table_ssrm|multi_file_viewer|"
            "advanced_charting|iframe|youtube|note|file_viewer|ssrm_advanced "
            "(default table), gridData {w,h} on a 40-column grid, params "
            "[{paramName, type text|number|date|boolean|endpoint|ticker|button|"
            "tabs|form, label, value, options, optionsEndpoint, multiSelect, ...}], "
            "and data.table.columnsDefs [{field, headerName, cellDataType, "
            "formatterFn, renderFn greenRed|titleCase|hoverCard|cellOnClick|"
            "columnColor|showCellChange, renderFnParams {actionType "
            "groupBy|sendToAgent, groupBy {paramName}}, ...}] for tables). "
            "Widget config fields: staleTime "
            "(cache ms, >=1000), refetchInterval (auto-refresh ms), runButton "
            "(boolean, adds a manual run button), source, category. Type-specific "
            "data fields: data.defaultSymbol (advanced_charting), data.wsRowIdColumn "
            "+ top-level wsEndpoint (live_grid), data.updateFrequency, data.dataKey "
            "(response key holding rows). form params carry inputParams (an array "
            "of inner param definitions) plus their own submit 'endpoint' "
            "(relative path) and optional 'method' POST|PUT; 'multiple' is "
            "allowed on text params only. apps_json is the apps.json ARRAY "
            "(each app REQUIRES name and "
            "tabs {tab_id: {id, name, layout: [{i, x, y, w, h, optional state "
            "{params {..}} presets}]}}; every layout 'i' must be a widget_id the "
            "backend serves; no overlapping layout items; optional description, "
            "allowCustomization, groups [{name, type endpointParam|param|ticker, "
            "paramName, widgetIds}], prompts [string]). Invalid payloads are "
            "rejected with specific errors. operation='refresh' with widgets_json/"
            "apps_json replaces what an existing custom backend serves — use it to "
            "fix a broken custom backend."
        ),
        "args": {
            "operation": "list|add|refresh",
            "name": "string, required for add",
            "backend_id": "string, required for refresh",
            "url": "string, required when adding a custom backend",
            "widgets_json": "object map widget_id -> widget definition (build payload)",
            "apps_json": "array of app definitions (build payload)",
        },
    },
    "manage_apps": {
        "description": (
            "List, read, or instantiate app templates a backend serves. This tool "
            "does NOT publish or author apps — apps.json is served by the backend, "
            "so publish or update it via manage_backends (operation='add' or "
            "'refresh' with apps_json), then instantiate here."
        ),
        "args": {
            "operation": "list|read|instantiate",
            "backend_id": "string",
            "app_name": "string, optional",
            "template_id": "string, optional",
            "dashboard_name": "string, optional for instantiate",
            "activate": "boolean, optional",
        },
    },
    "get_skill_content": {
        "description": "Read deterministic Workspace skill content by exact skill slug.",
        "args": {
            "slug": "string, e.g. finance-earnings-prep",
            "reason": "string, optional",
        },
    },
    "read_workspace_resource": {
        "description": (
            "Read deterministic Workspace resources by exact URI, including the "
            "app-builder index and skill resources."
        ),
        "args": {
            "uri": (
                "string, e.g. openbb://workspace/app-builder/index or "
                "openbb://workspace/skills/finance-comps"
            ),
        },
    },
    "get_workspace_prompt": {
        "description": "Fetch deterministic Workspace prompt text by exact prompt name.",
        "args": {
            "name": "workspace_tool_usage|workspace_session_context",
        },
    },
    "assign_tasks_to_agents": {
        "description": "Delegate work to external Workspace agents.",
        "args": {
            "task_requests": [
                {
                    "id": "string task id",
                    "description": "string task description",
                    "assigned_holder_url": "string URL or workspace holder",
                    "assigned_agent_id": "string agent id",
                }
            ]
        },
    },
}


def fixture_origin_hints(fixtures: dict[str, Any]) -> dict[str, str]:
    hints = {}
    for backend in fixtures.get("backends", []):
        if not isinstance(backend, dict):
            continue
        name = backend.get("name")
        if isinstance(name, str):
            hints[name] = FIXTURE_ORIGINS.get(name, name)
    return hints


def envelope_origin_hints(task: dict[str, Any]) -> dict[str, str]:
    """Slug -> display-name hints from fixtures and the workspace axes."""

    hints = fixture_origin_hints(task.get("fixtures") or {})
    for slug in task.get("workspace_backends") or []:
        if isinstance(slug, str):
            hints[slug] = FIXTURE_ORIGINS.get(slug, slug)
    return hints


def strip_code_fence(text: str) -> str:
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL)
    return fence.group(1).strip() if fence else text
