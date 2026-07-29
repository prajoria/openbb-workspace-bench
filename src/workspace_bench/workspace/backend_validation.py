"""Validation for authored custom-backend widgets.json / apps.json payloads.

Mirrors the real OpenBB Workspace frontend validation (terminalpro):
- ``src/utils/zodForms.ts`` (widgetSchema / specificationSchema / KNOWN_WIDGET_KEYS)
- ``src/lib/types/app.ts`` (ParamDefSchema, TableColumnDefsSchema,
  backendTemplateSchema, WidgetVizTypes)
- ``src/lib/utils/validateBackend.ts`` (orchestration, error strings, warn-vs-reject)

Enforcement classes follow the real product:
- REJECT (hard error, whole payload refused — the real validator drops all widgets or
  all templates when one entry fails schema validation).
- WARN (payload accepted; warning recorded — e.g. unknown top-level keys, app layout
  referencing a widget id the backend does not serve, overlapping layout items).
"""

from __future__ import annotations

import re
from typing import Any

from workspace_bench.core.models import JsonDict
from workspace_bench.workspace.widget_params import rects_overlap
from workspace_bench.workspace.widget_params import slugify
from workspace_bench.workspace.widget_params import flatten_params

# Canonical live catalog from openbb://workspace/specs/widget-types (2026-07-12).
# ``ssrm_table`` is accepted as a manifest alias because some
# production backend examples still publish it; generators and oracles must
# always emit the canonical ``table_ssrm`` spelling.
CANONICAL_WIDGET_VIZ_TYPES = frozenset({
    "advanced_charting", "chart", "chart-highcharts", "chart-vegalite",
    "file_viewer", "html", "iframe", "live_grid", "markdown", "metric",
    "multi_file_viewer", "newsfeed", "note", "omni", "pdf", "table",
    "table_ssrm", "ssrm_advanced", "youtube",
})
WIDGET_VIZ_TYPE_ALIASES = {"ssrm_table": "table_ssrm"}
WIDGET_VIZ_TYPES = CANONICAL_WIDGET_VIZ_TYPES | frozenset(WIDGET_VIZ_TYPE_ALIASES)

# ParamDefSchemaBase type enum + the form variant — app.ts:399-541
PARAM_TYPES = frozenset({
    "text", "date", "ticker", "number", "boolean", "endpoint", "button",
    "tabs", "form",
})

EDITOR_LANGUAGES = frozenset({
    "sql", "javascript", "python", "json", "html", "css", "markdown", "xml", "text",
})

# TableColumnDefsSchema — app.ts:193-368
CELL_DATA_TYPES = frozenset({"text", "number", "boolean", "date", "dateString", "object"})
CHART_DATA_TYPES = frozenset({"category", "series", "time", "excluded"})
FORMATTER_FNS = frozenset({
    "int", "none", "percent", "normalized", "normalizedPercent", "dateToYear",
})
RENDER_FNS = frozenset({
    "greenRed", "titleCase", "hoverCard", "cellOnClick", "columnColor",
    "showCellChange",
})
COLOR_RULE_CONDITIONS = frozenset({
    "eq", "ne", "gt", "lt", "gte", "lte", "contains", "notContains", "between",
})
COLOR_NAMES = frozenset({"green", "red", "blue"})
HEX_COLOR = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

GROUP_TYPES = frozenset({"ticker", "endpointParam", "param"})

GRID_COLUMNS = 40

# KNOWN_WIDGET_KEYS — derived from widgetShapeDefinition (zodForms.ts:149-209);
# IGNORE_KEYS mcp_tool/searchCategory are never flagged (zodForms.ts:264).
KNOWN_WIDGET_KEYS = frozenset({
    "name", "showTitle", "description", "category", "subCategory", "sub_category",
    "schemaName", "source", "widgetId", "widgetType", "endpoint", "fileEndpoint",
    "wsEndpoint", "params", "groupById", "data", "type", "defaultViz", "gridData",
    "staleTime", "refetchInterval", "dataUpdateDisplay", "runButton",
    "disableRetrievalForCopilot", "copilotParseAs", "inputType", "raw", "exportable",
    "storage", "mcp_tool", "searchCategory",
})

KNOWN_TEMPLATE_KEYS = frozenset({
    "templateId", "template_id", "id", "name", "description", "selected_agent",
    "img", "img_dark", "img_light", "authentication", "tabs", "groups", "prompts",
    "mcpServers", "mcp_servers", "allowCustomization",
})

CRON_FIELDS = 5


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _looks_like_single_widget(payload: JsonDict) -> bool:
    """Real ``isValidWidget``: a bare widget object instead of an id -> def map."""

    return (
        isinstance(payload.get("name"), str)
        and isinstance(payload.get("endpoint"), str)
    )


def _valid_cron(value: str) -> bool:
    return len(value.split()) == CRON_FIELDS


def _render_fn_list(value: Any) -> list[str] | None:
    """renderFn accepts an array or a comma-separated string (app.ts)."""

    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return [item.strip() for item in value]
    return None


def _validate_render_fn_params(where: str, column: JsonDict, errors: list[str]) -> None:
    params = column.get("renderFnParams")
    if params is None:
        return
    if not isinstance(params, dict):
        errors.append(f"{where}: renderFnParams must be an object.")
        return
    action = params.get("actionType")
    if action == "groupBy":
        group_by = params.get("groupBy")
        flat_param_name = params.get("groupByParamName")
        has_param = bool(isinstance(flat_param_name, str) and flat_param_name)
        if isinstance(group_by, dict) and isinstance(group_by.get("paramName"), str):
            has_param = has_param or bool(group_by["paramName"])
        if not has_param:
            errors.append(
                f"{where}: `groupBy.paramName` is required when actionType is `groupBy`."
            )
    elif action == "sendToAgent":
        send = params.get("sendToAgent")
        if not (isinstance(send, dict) and isinstance(send.get("markdown"), str) and send["markdown"]):
            errors.append(
                f"{where}: `sendToAgent.markdown` is required when actionType is `sendToAgent`."
            )
    elif action is not None and action not in {"groupBy", "sendToAgent"}:
        errors.append(
            f"{where}: renderFnParams.actionType must be 'groupBy' or 'sendToAgent'."
        )
    rules = params.get("colorRules")
    if rules is not None:
        if not isinstance(rules, list):
            errors.append(f"{where}: colorRules must be an array.")
            return
        for index, rule in enumerate(rules):
            rule_where = f"{where} colorRules[{index}]"
            if not isinstance(rule, dict):
                errors.append(f"{rule_where}: must be an object.")
                continue
            condition = rule.get("condition")
            if condition not in COLOR_RULE_CONDITIONS:
                errors.append(
                    f"{rule_where}: condition must be one of "
                    f"{sorted(COLOR_RULE_CONDITIONS)}."
                )
                continue
            if condition == "between":
                rng = rule.get("range")
                if not (
                    isinstance(rng, dict)
                    and _is_number(rng.get("min"))
                    and _is_number(rng.get("max"))
                ):
                    errors.append(
                        f"{rule_where}: 'between' requires range with numeric min and max."
                    )
            elif "value" not in rule:
                errors.append(f"{rule_where}: condition '{condition}' requires a value.")
            color = rule.get("color")
            if not (isinstance(color, str) and (color in COLOR_NAMES or HEX_COLOR.match(color))):
                errors.append(
                    f"{rule_where}: color must be green, red, blue, or a hex value."
                )


def _validate_columns_defs(where: str, columns: Any, errors: list[str]) -> None:
    if not isinstance(columns, list):
        errors.append(f"{where}: columnsDefs must be an array.")
        return
    for index, column in enumerate(columns):
        col_where = f"{where} columnsDefs[{index}]"
        if not isinstance(column, dict):
            errors.append(f"{col_where}: must be an object.")
            continue
        if not (isinstance(column.get("field"), str) and column["field"]):
            errors.append(f"{col_where}: field is required.")
        if not (isinstance(column.get("headerName"), str) and column["headerName"]):
            errors.append(f"{col_where}: headerName is required.")
        cell_type = column.get("cellDataType")
        if cell_type is not None and cell_type not in CELL_DATA_TYPES:
            errors.append(
                f"{col_where}: cellDataType must be one of {sorted(CELL_DATA_TYPES)}."
            )
        chart_type = column.get("chartDataType")
        if chart_type is not None and chart_type not in CHART_DATA_TYPES:
            errors.append(
                f"{col_where}: chartDataType must be one of {sorted(CHART_DATA_TYPES)}."
            )
        formatter = column.get("formatterFn")
        if formatter is not None and formatter not in FORMATTER_FNS:
            errors.append(
                f"{col_where}: formatterFn must be one of {sorted(FORMATTER_FNS)}."
            )
        decimals = column.get("decimalPlaces")
        if decimals is not None and not (
            isinstance(decimals, int) and not isinstance(decimals, bool) and 0 <= decimals <= 6
        ):
            errors.append(f"{col_where}: decimalPlaces must be an integer between 0 and 6.")
        render_fn = column.get("renderFn")
        if render_fn is not None:
            fns = _render_fn_list(render_fn)
            if fns is None:
                errors.append(f"{col_where}: renderFn must be a string or array of strings.")
            else:
                unknown = [fn for fn in fns if fn not in RENDER_FNS]
                if unknown:
                    errors.append(
                        f"{col_where}: unknown renderFn {unknown} — supported: "
                        f"{sorted(RENDER_FNS)}."
                    )
        pinned = column.get("pinned")
        if pinned is not None and pinned not in {"left", "right", True, False}:
            errors.append(f"{col_where}: pinned must be 'left', 'right', or a boolean.")
        _validate_render_fn_params(col_where, column, errors)


def _validate_param(
    where: str,
    param: Any,
    seen_names: set[str],
    file_selector_count: list[int],
    errors: list[str],
) -> None:
    if not isinstance(param, dict):
        errors.append(f"{where}: each param must be an object.")
        return
    name = param.get("paramName")
    if not (isinstance(name, str) and name):
        errors.append(f"{where}: paramName is required.")
        return
    if name in seen_names:
        errors.append(f"{where}: duplicate paramName '{name}'.")
    seen_names.add(name)
    param_type = param.get("type", "text")
    if param_type not in PARAM_TYPES:
        errors.append(
            f"{where}: param '{name}' has unsupported type '{param_type}' — "
            f"supported: {sorted(PARAM_TYPES)}."
        )
    if param.get("multiple") and param_type != "text":
        errors.append(
            f"{where}: param '{name}': `multiple` can only be true when `type` is 'text'."
        )
    options = param.get("options")
    if options is not None:
        if not isinstance(options, list):
            errors.append(f"{where}: param '{name}': options must be an array.")
        else:
            for option in options:
                if not (isinstance(option, dict) and "label" in option and "value" in option):
                    errors.append(
                        f"{where}: param '{name}': each option needs label and value."
                    )
                    break
    options_endpoint = param.get("optionsEndpoint")
    if options_endpoint is not None and not isinstance(options_endpoint, str):
        errors.append(f"{where}: param '{name}': optionsEndpoint must be a string.")
    options_params = param.get("optionsParams")
    if options_params is not None and not isinstance(options_params, dict):
        errors.append(f"{where}: param '{name}': optionsParams must be an object.")
    style = param.get("style")
    if style is not None:
        popup = style.get("popupWidth") if isinstance(style, dict) else None
        if popup is not None and not (_is_number(popup) and 100 <= popup <= 1000):
            errors.append(
                f"{where}: param '{name}': style.popupWidth must be between 100 and 1000."
            )
    roles = param.get("roles")
    if roles is not None:
        if not (isinstance(roles, list) and all(isinstance(role, str) for role in roles)):
            errors.append(f"{where}: param '{name}': roles must be an array of strings.")
        elif "fileSelector" in roles:
            file_selector_count[0] += 1
            if file_selector_count[0] > 1:
                errors.append(
                    f"{where}: Only one parameter can have the role 'fileSelector'."
                )
    language = param.get("language")
    if language is not None and language not in EDITOR_LANGUAGES:
        errors.append(
            f"{where}: param '{name}': language must be one of {sorted(EDITOR_LANGUAGES)}."
        )
    if param_type == "form":
        if not isinstance(param.get("inputParams"), list):
            errors.append(
                f"{where}: param '{name}': type 'form' requires an inputParams array."
            )
        if not (isinstance(param.get("endpoint"), str) and param["endpoint"]):
            errors.append(
                f"{where}: param '{name}': type 'form' requires a submit endpoint — "
                "set the param's 'endpoint' key to the relative submit path "
                "(e.g. '/form-submit')."
            )
        method = param.get("method")
        if method is not None and method not in {"POST", "PUT"}:
            errors.append(
                f"{where}: param '{name}': form method must be 'POST' or 'PUT'."
            )
    if param_type == "number":
        for bound in ("min", "max"):
            if bound in param and not _is_number(param[bound]):
                errors.append(
                    f"{where}: param '{name}': {bound} must be a number."
                )


def _effective_type(definition: JsonDict) -> str:
    widget_type = definition.get("type") or definition.get("defaultViz")
    return widget_type if isinstance(widget_type, str) else "table"


def validate_widgets_json(
    payload: Any,
) -> tuple[list[str], list[str], dict[str, JsonDict]]:
    """Validate an authored widgets.json payload.

    Returns (errors, warnings, normalized). ``normalized`` is only meaningful when
    there are no errors: definitions with `type` filled in (defaultViz fallback,
    table default) and gridData stripped to {w, h} — matching the real zod transform.
    """

    errors: list[str] = []
    warnings: list[str] = []
    normalized: dict[str, JsonDict] = {}

    if isinstance(payload, list):
        errors.append(
            "[widgets.json]: Invalid format. Expected an object map of "
            'widget_id -> definition, e.g. {"table_data": {"name": "Table data", ...}}; '
            "received an array."
        )
        return errors, warnings, normalized
    if not isinstance(payload, dict):
        errors.append("[widgets.json]: Invalid format. Expected an object map.")
        return errors, warnings, normalized
    if _looks_like_single_widget(payload):
        errors.append(
            "[widgets.json]: Invalid format. Received a bare widget definition; "
            "expected an object map of widget_id -> definition."
        )
        return errors, warnings, normalized

    for widget_id, definition in payload.items():
        where = f"[widgets.json] widget '{widget_id}'"
        if not isinstance(widget_id, str) or not widget_id:
            errors.append("[widgets.json]: widget ids must be non-empty strings.")
            continue
        if not isinstance(definition, dict):
            errors.append(f"{where}: definition must be an object.")
            continue

        for required in ("name", "description", "endpoint"):
            value = definition.get(required)
            if not (isinstance(value, str) and value):
                errors.append(f"{where}: '{required}' is required and must be a string.")

        declared_type = definition.get("type")
        if declared_type is not None and declared_type not in WIDGET_VIZ_TYPES:
            errors.append(
                f"{where}: unsupported type '{declared_type}' — supported types: "
                f"{sorted(WIDGET_VIZ_TYPES)}."
            )
        default_viz = definition.get("defaultViz")
        if default_viz is not None and default_viz not in WIDGET_VIZ_TYPES:
            errors.append(f"{where}: unsupported defaultViz '{default_viz}'.")

        grid = definition.get("gridData")
        if grid is not None:
            if not isinstance(grid, dict):
                errors.append(f"{where}: gridData must be an object with numeric w and h.")
            else:
                for key in ("w", "h"):
                    if not _is_number(grid.get(key)):
                        errors.append(f"{where}: gridData.{key} must be a number.")
                if _is_number(grid.get("w")) and not 1 <= grid["w"] <= GRID_COLUMNS:
                    errors.append(
                        f"{where}: gridData.w must be between 1 and {GRID_COLUMNS}."
                    )
                if _is_number(grid.get("h")) and grid["h"] < 1:
                    errors.append(f"{where}: gridData.h must be at least 1.")

        stale = definition.get("staleTime")
        if stale is not None and not (_is_number(stale) and stale >= 1000):
            errors.append(f"{where}: staleTime must be a number >= 1000 (milliseconds).")

        refetch = definition.get("refetchInterval")
        if refetch is not None and refetch is not False:
            if isinstance(refetch, str):
                if not _valid_cron(refetch):
                    errors.append(
                        f"{where}: refetchInterval string must be a 5-field cron expression."
                    )
            elif not _is_number(refetch):
                errors.append(
                    f"{where}: refetchInterval must be milliseconds, a cron string, or false."
                )

        update_display = definition.get("dataUpdateDisplay")
        if update_display is not None and not (
            isinstance(update_display, str) and _valid_cron(update_display)
        ):
            errors.append(f"{where}: dataUpdateDisplay must be a 5-field cron expression.")

        params = definition.get("params")
        seen_names: set[str] = set()
        file_selector_count = [0]
        if params is not None:
            if not isinstance(params, list):
                errors.append(f"{where}: params must be an array.")
            else:
                for entry in params:
                    entries = entry if isinstance(entry, list) else [entry]
                    errors.extend(
                        f"{where}: each param must be an object."
                        for param in entries
                        if not isinstance(param, dict)
                    )
                params_flat = flatten_params(definition, recurse=False)
                for param in params_flat:
                    _validate_param(
                        where, param, seen_names, file_selector_count, errors
                    )
                for param in params_flat:
                    options_params = param.get("optionsParams")
                    if isinstance(options_params, dict):
                        for ref in options_params.values():
                            if isinstance(ref, str) and ref.startswith("$"):
                                if ref[1:] not in seen_names:
                                    warnings.append(
                                        f"{where}: optionsParams references '{ref}' but no "
                                        f"param named '{ref[1:]}' exists."
                                    )

        effective = _effective_type(definition)
        if effective == "multi_file_viewer":
            has_file_selector = any(
                isinstance(param, dict)
                and param.get("type") == "endpoint"
                and isinstance(param.get("roles"), list)
                and "fileSelector" in param["roles"]
                for param in flatten_params(definition, recurse=False)
            )
            if not has_file_selector:
                errors.append(
                    f"{where}: Endpoint param with `{{ roles: [\"fileSelector\"] }}` "
                    "required for `multi_file_viewer`."
                )
        if effective == "live_grid" and not definition.get("wsEndpoint"):
            warnings.append(f"{where}: type 'live_grid' usually requires wsEndpoint.")

        data = definition.get("data")
        if data is not None:
            if not isinstance(data, dict):
                errors.append(f"{where}: data must be an object.")
            else:
                data_key = data.get("dataKey")
                if data_key is not None and not isinstance(data_key, str):
                    errors.append(f"{where}: data.dataKey must be a string.")
                table = data.get("table")
                if table is not None:
                    if not isinstance(table, dict):
                        errors.append(f"{where}: data.table must be an object.")
                    elif table.get("columnsDefs") is not None:
                        _validate_columns_defs(where, table["columnsDefs"], errors)

        unknown = [
            key for key in definition
            if key not in KNOWN_WIDGET_KEYS and isinstance(key, str)
        ]
        if unknown:
            warnings.append(
                f"{where}: unrecognized keys {sorted(unknown)} (accepted but ignored "
                "by the workspace)."
            )

        if not errors:
            stored = dict(definition)
            stored["type"] = effective
            if isinstance(stored.get("gridData"), dict):
                stored["gridData"] = {
                    key: stored["gridData"][key]
                    for key in ("w", "h")
                    if key in stored["gridData"]
                }
            normalized[widget_id] = stored

    if errors:
        return errors, warnings, {}
    return errors, warnings, normalized


def validate_apps_json(
    payload: Any,
    widget_ids: set[str],
) -> tuple[list[str], list[str], list[JsonDict]]:
    """Validate an authored apps.json payload against the backend's widget ids.

    Returns (errors, warnings, normalized). Mirrors backendTemplateSchema: schema
    violations REJECT; dangling widget references, geometry problems, and group
    wiring problems WARN (the real product adds the app and toasts a warning; the
    grader is what fails the task).
    """

    errors: list[str] = []
    warnings: list[str] = []
    normalized: list[JsonDict] = []

    if payload is None:
        return errors, warnings, normalized
    if isinstance(payload, dict):
        payload = [payload]
    if not isinstance(payload, list):
        errors.append("[apps.json]: Invalid format. Expected an array of app objects.")
        return errors, warnings, normalized

    seen_template_ids: set[str] = set()
    for index, app in enumerate(payload):
        app_label = f"[apps.json] app[{index}]"
        if not isinstance(app, dict):
            errors.append(f"{app_label}: each app must be an object.")
            continue
        name = app.get("name")
        if not (isinstance(name, str) and name):
            errors.append(f"{app_label}: 'name' is required and must be a string.")
            name = "Unknown App"
        where = f"[apps.json] app '{name}'"

        tabs = app.get("tabs")
        if not isinstance(tabs, dict) or not tabs:
            errors.append(f"{where}: 'tabs' is required and must be a non-empty object.")
            tabs = {}

        for tab_key, tab in tabs.items():
            tab_where = f"{where} (tab: {tab_key})"
            if not isinstance(tab, dict):
                errors.append(f"{tab_where}: each tab must be an object.")
                continue
            if not isinstance(tab.get("id"), str):
                errors.append(f"{tab_where}: tab 'id' is required.")
            if not isinstance(tab.get("name"), str):
                errors.append(f"{tab_where}: tab 'name' is required.")
            layout = tab.get("layout")
            if not isinstance(layout, list):
                errors.append(f"{tab_where}: tab 'layout' must be an array.")
                continue
            rects: list[JsonDict] = []
            missing_ids: list[str] = []
            for item_index, item in enumerate(layout):
                item_where = f"{tab_where} layout[{item_index}]"
                if not isinstance(item, dict):
                    errors.append(f"{item_where}: must be an object.")
                    continue
                widget_ref = item.get("i")
                if not (isinstance(widget_ref, str) and widget_ref):
                    errors.append(f"{item_where}: 'i' (widget id) is required.")
                    continue
                bad_geometry = False
                for key in ("x", "y", "w", "h"):
                    if not _is_number(item.get(key)):
                        errors.append(f"{item_where}: '{key}' is required and numeric.")
                        bad_geometry = True
                if bad_geometry:
                    continue
                if widget_ref not in widget_ids and widget_ref != "navigation_bar":
                    missing_ids.append(widget_ref)
                if item["x"] < 0 or item["y"] < 0 or item["w"] <= 0 or item["h"] <= 0:
                    warnings.append(
                        f"{item_where}: geometry must be positive and within the grid."
                    )
                elif item["x"] + item["w"] > GRID_COLUMNS:
                    warnings.append(
                        f"{item_where}: extends past the {GRID_COLUMNS}-column grid "
                        f"(x={item['x']}, w={item['w']})."
                    )
                rect = {
                    "i": widget_ref,
                    "x": item["x"], "y": item["y"], "w": item["w"], "h": item["h"],
                }
                for other in rects:
                    if rects_overlap(rect, other):
                        warnings.append(
                            f"{tab_where}: layout items '{other['i']}' and "
                            f"'{widget_ref}' overlap."
                        )
                rects.append(rect)
            if missing_ids:
                warnings.append(
                    f"{tab_where}: [widgets.json]: Missing widgets used in tab "
                    f"`{', '.join(missing_ids)}`."
                )

        groups = app.get("groups")
        if groups is not None:
            if not isinstance(groups, list):
                errors.append(f"{where}: 'groups' must be an array.")
            else:
                for group_index, group in enumerate(groups):
                    group_where = f"{where} groups[{group_index}]"
                    if not isinstance(group, dict):
                        errors.append(f"{group_where}: must be an object.")
                        continue
                    if not (isinstance(group.get("name"), str) and group["name"]):
                        errors.append(f"{group_where}: group 'name' is required.")
                    group_type = group.get("type")
                    if not isinstance(group_type, str):
                        errors.append(f"{group_where}: group 'type' is required.")
                    elif group_type not in GROUP_TYPES:
                        warnings.append(
                            f"{group_where}: group type '{group_type}' is not one of "
                            f"{sorted(GROUP_TYPES)}."
                        )
                    group_widgets = group.get("widgetIds")
                    if group_widgets is not None:
                        if not isinstance(group_widgets, list):
                            errors.append(f"{group_where}: widgetIds must be an array.")
                        else:
                            unknown_ids = [
                                wid for wid in group_widgets if wid not in widget_ids
                            ]
                            if unknown_ids:
                                warnings.append(
                                    f"{group_where}: widgetIds reference unknown "
                                    f"widgets {unknown_ids}."
                                )

        prompts = app.get("prompts")
        if prompts is not None and not (
            isinstance(prompts, list) and all(isinstance(p, str) for p in prompts)
        ):
            errors.append(f"{where}: 'prompts' must be an array of strings.")

        unknown_keys = [
            key for key in app if isinstance(key, str) and key not in KNOWN_TEMPLATE_KEYS
        ]
        if unknown_keys:
            warnings.append(
                f"{where}: unrecognized keys {sorted(unknown_keys)} (accepted but "
                "ignored by the workspace)."
            )

        if not errors:
            stored = dict(app)
            template_id = (
                stored.get("template_id")
                or stored.get("templateId")
                or slugify(str(name))
            )
            if template_id in seen_template_ids:
                template_id = f"{template_id}-{index}"
            seen_template_ids.add(template_id)
            stored["template_id"] = template_id
            normalized.append(stored)

    if errors:
        return errors, warnings, []
    return errors, warnings, normalized
