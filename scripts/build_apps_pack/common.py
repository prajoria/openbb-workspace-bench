"""Shared machinery for the WorkspaceBench Part 2 build-openbb-apps collection generator.

Design invariant (the part-1 lesson, enforced by construction): every scenario is
built from ONE spec — the exact widgets.json / apps.json payload the oracle submits.
The prompt is RENDERED from that spec (`widget_brief_text`, `app_brief_text`) and the
grader checks are DERIVED from that spec (`widget_def_checks`, `app_def_checks`), so
the prompt can never demand less than the grader checks.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BUNDLED_OUT_DIR = (
    REPO / "src/workspace_bench/core/scenario_packs/workspace_bench_v2_build_openbb_apps"
)

TIERS = ("t0", "t1", "t2", "t3", "t4")
# t4 slack is wider than part 1's because building oracles are SHORT (a 2-call
# oracle with slack 2 leaves zero margin for one validation round-trip).
# 5 -> 4 in proxy r4: with t4 now building t3-grade content plus operating it,
# one budgeted recovery round-trip is enough; two made orchestration too soft.
TIER_SLACK = {"t0": 3, "t1": 3, "t2": 3, "t3": 3, "t4": 4}

# v3 families mirror the onboarding reference app (getting-started/
# reference-backend "Onboarding App for Devs") — each family is one tab theme,
# so widget-type coverage is by construction, not by quota (Didier review,
# 2026-07-08). `apps`/`extend` carry the app-side surfaces; `e2e` stays the
# t4-only capstone.
WIDGET_FAMILIES = (
    "types", "settings", "params", "forms",
    "aggrid", "charts", "advanced", "grouping",
)
APP_FAMILIES = ("apps", "extend")
LADDER_FAMILIES = WIDGET_FAMILIES + APP_FAMILIES
CAPSTONE_FAMILY = "e2e"
E2E_COUNT = 12

CAPABILITY = {
    "types": "widget-building", "settings": "widget-building",
    "params": "widget-building", "forms": "widget-building",
    "aggrid": "widget-building", "charts": "widget-building",
    "advanced": "widget-building", "grouping": "widget-building",
    "apps": "app-building", "extend": "app-building",
    "e2e": "backend-integration",
}

# Widget-type / param-type ownership per family (asserted at certification):
# every owned key must appear in that family's built artifacts.
TYPE_OWNERSHIP = {
    "types": {"markdown", "metric", "pdf", "html", "iframe", "youtube",
              "newsfeed", "multi_file_viewer"},
    "aggrid": {"table", "ssrm_table"},
    "charts": {"chart", "chart-highcharts", "chart-vegalite"},
    "advanced": {"advanced_charting", "live_grid", "omni"},
}
PARAM_OWNERSHIP = {
    "params": {"text", "date", "ticker", "number", "boolean", "endpoint", "tabs"},
    "forms": {"form", "button"},
}

SCENARIOS: list[dict] = []
CELL_COUNTS: dict[tuple[str, str], int] = defaultdict(int)
PROMPT_POOL_SIZES: dict[str, int] = {}

# Building is a validation-loop workflow by design: the simulator's rejections are
# specific and actionable (mirroring the real product), so one rejected round-trip is
# budgeted rather than fatal. Calibration decision after gate run 2.
TRACE_ZERO = {"max_invalid_tool_calls": 1, "max_repeated_snapshots": 2}
# t4 carries orchestration risk on top of building; two budgeted round-trips keep
# its difficulty about breadth rather than sudden death (round-11 flakiness fix:
# 15% of t4 scenarios flipped between identical runs, several on budget alone).
TRACE_T4 = {"max_invalid_tool_calls": 2, "max_repeated_snapshots": 2}


def phrased(scenario_id: str, variants: list[str]) -> str:
    """Select a prompt variant by stable scenario-id hash (part-1 convention)."""

    assert isinstance(variants, list), f"{scenario_id} prompt pool must be a list"
    assert len(variants) >= 3, f"{scenario_id} prompt pool has {len(variants)} variants"
    frame = sys._getframe(1)
    site = f"{Path(frame.f_code.co_filename).name}:{frame.f_lineno}"
    previous = PROMPT_POOL_SIZES.setdefault(site, len(variants))
    assert previous == len(variants), (
        f"prompt site {site} used pool sizes {previous} and {len(variants)}"
    )
    index = int(hashlib.md5(scenario_id.encode()).hexdigest(), 16) % len(variants)
    return variants[index]


def difficulty_for(tier: str, cell_index: int) -> str:
    if tier == "t0":
        return "easy"
    if tier == "t1":
        return "easy" if cell_index <= 2 else "medium"
    if tier == "t2":
        return "medium"
    if tier == "t3":
        return "medium" if cell_index <= 2 else "hard"
    return "hard"


def level_for(tier: str, family: str) -> str:
    # v3: repair-under-preservation lives in the `extend` family (L4); the
    # rest of the pack is platform work (L3).
    return "L4" if family == "extend" else "L3"


def add(family: str, tier: str, scenario: dict) -> None:
    CELL_COUNTS[(family, tier)] += 1
    cell_index = CELL_COUNTS[(family, tier)]
    scenario.setdefault("domain", "finance")
    scenario.setdefault("source", "workspace-bench-build-apps-gen")
    scenario.setdefault("level", level_for(tier, family))
    scenario.setdefault("capability", CAPABILITY[family])
    scenario["difficulty"] = difficulty_for(tier, cell_index)
    # Invalid-call budget scales with single-payload size (proxy r4): t3 ships
    # the largest one-shot payload in the ladder (2-3 defs + multi-tab app +
    # convention), so it gets the same validation-loop allowance as t4's
    # multi-step flow. Enforced centrally so modules cannot underspend it.
    if tier in ("t3", "t4"):
        trace = scenario.get("success", {}).setdefault("trace_checks", {})
        if trace.get("max_invalid_tool_calls", 0) < 2:
            trace["max_invalid_tool_calls"] = 2
    tags = scenario.setdefault("tags", [])
    tags.insert(0, f"cell{cell_index}")
    tags.insert(0, f"tier-{tier}")
    tags.insert(0, f"family-{family}")
    scenario.setdefault("limits", {})["max_turns"] = (
        len(scenario["oracle_tool_calls"]) + TIER_SLACK[tier]
    )
    scenario["_family"], scenario["_tier"] = family, tier
    SCENARIOS.append(scenario)


# ---------------------------------------------------------------------------
# Widget definition factories — always produce COMPLETE, VALID definitions.
# ---------------------------------------------------------------------------

def table_def(
    name: str,
    description: str,
    endpoint: str,
    columns: list[tuple] | None = None,
    params: list[dict] | None = None,
    grid: tuple[int, int] = (20, 9),
    **extra,
) -> dict:
    definition = {
        "name": name,
        "description": description,
        "endpoint": endpoint,
        "type": "table",
        "gridData": {"w": grid[0], "h": grid[1]},
    }
    if params:
        definition["params"] = params
    if columns:
        columns_defs = []
        for column in columns:
            field, header, cell_type = column[0], column[1], column[2]
            entry = {"field": field, "headerName": header, "cellDataType": cell_type}
            if len(column) > 3 and column[3]:
                entry.update(column[3])
            columns_defs.append(entry)
        definition["data"] = {"table": {"columnsDefs": columns_defs}}
    definition.update(extra)
    return definition


def simple_def(
    widget_type: str,
    name: str,
    description: str,
    endpoint: str,
    params: list[dict] | None = None,
    grid: tuple[int, int] = (12, 6),
    **extra,
) -> dict:
    definition = {
        "name": name,
        "description": description,
        "endpoint": endpoint,
        "type": widget_type,
        "gridData": {"w": grid[0], "h": grid[1]},
    }
    if params:
        definition["params"] = params
    definition.update(extra)
    return definition


def text_param(name: str, label: str, value: str = "", description: str = "") -> dict:
    param = {"paramName": name, "type": "text", "label": label, "value": value}
    if description:
        param["description"] = description
    return param


def number_param(name: str, label: str, value, minimum=None, maximum=None) -> dict:
    param = {"paramName": name, "type": "number", "label": label, "value": value}
    if minimum is not None:
        param["min"] = minimum
    if maximum is not None:
        param["max"] = maximum
    return param


def dropdown_param(name: str, label: str, value, options: list[tuple]) -> dict:
    return {
        "paramName": name, "type": "text", "label": label, "value": value,
        "options": [{"label": lab, "value": val} for lab, val in options],
    }


def endpoint_param(name: str, label: str, value, options_endpoint: str) -> dict:
    return {
        "paramName": name, "type": "endpoint", "label": label, "value": value,
        "optionsEndpoint": options_endpoint,
    }


def boolean_param(name: str, label: str, value: bool) -> dict:
    return {"paramName": name, "type": "boolean", "label": label, "value": value}


def date_param(name: str, label: str, value: str = "$currentDate-1d") -> dict:
    return {"paramName": name, "type": "date", "label": label, "value": value}


def app_def(
    name: str,
    description: str,
    tabs: list[tuple[str, str, list[dict]]],
    groups: list[dict] | None = None,
    prompts: list[str] | None = None,
    template_id: str | None = None,
    allow_customization: bool | None = None,
) -> dict:
    # allowCustomization is OPTIONAL in real apps.json. Only carry (and hence
    # grade) it when a scenario explicitly opts in — proxy round 1 (v3): every
    # words-brief t1 failed solely on "missing allowCustomization (expected
    # True)" that no prompt ever stated.
    app = {
        "name": name,
        "description": description,
        "tabs": {
            tab_id: {"id": tab_id, "name": tab_name, "layout": layout}
            for tab_id, tab_name, layout in tabs
        },
        "groups": groups or [],
    }
    if allow_customization is not None:
        app["allowCustomization"] = allow_customization
    if prompts:
        app["prompts"] = prompts
    if template_id:
        app["template_id"] = template_id
    return app


def layout_item(widget_id: str, x: int, y: int, w: int, h: int, params: dict | None = None) -> dict:
    item = {"i": widget_id, "x": x, "y": y, "w": w, "h": h}
    if params:
        item["state"] = {"params": params}
    return item


# ---------------------------------------------------------------------------
# Prompt rendering — the brief the analyst gives. Renders EVERY field of the
# definition so the prompt fully pins the graded payload.
# ---------------------------------------------------------------------------

def _compact_json(payload) -> str:
    return json.dumps(payload, sort_keys=True, separators=(", ", ": "))


# ---------------------------------------------------------------------------
# Requirements rendering (t1+): every graded value is STATED, structured and
# unambiguous, but the finished JSON is NOT given — the model derives the
# definition. Exact-JSON briefs (widget_brief_text) are the t0 form.
# Calibration round 6: exact-JSON everywhere flattened t1–t3 into transcription.
# ---------------------------------------------------------------------------

_PARAM_KIND = {
    "text": "a text input",
    "number": "a number input",
    "date": "a date picker",
    "boolean": "a boolean toggle",
    "endpoint": "a dropdown",
    "ticker": "a ticker picker",
    "tabs": "a tabs switcher",
    "button": "a button",
}


def _param_requirement(param: dict) -> str:
    name = param["paramName"]
    kind = param.get("type", "text")
    if kind == "form":
        inner = "; ".join(
            _param_requirement(item) for item in param.get("inputParams", [])
        )
        return (
            f"{name} — a form submitting {param.get('method', 'POST')} to "
            f"{param.get('endpoint')} with inputs [{inner}] (that bracket is "
            "the complete list of the form's inputParams)"
        )
    bits = [f"{name} — {_PARAM_KIND.get(kind, kind)} (type {kind})"]
    if "label" in param:
        bits.append(f"labeled \"{param['label']}\"")
    if "optionsEndpoint" in param:
        bits.append(f"options fetched from {param['optionsEndpoint']}")
    if "optionsParams" in param:
        bits.append(f"passing optionsParams {_compact_json(param['optionsParams'])}")
    if "options" in param:
        pairs = ", ".join(
            f"\"{opt['label']}\"={json.dumps(opt['value'])}" for opt in param["options"]
        )
        bits.append(f"static options [{pairs}]")
    if param.get("multiSelect"):
        bits.append("multi-select")
    if "value" in param:
        bits.append(f"default {json.dumps(param['value'])}")
    if "min" in param:
        bits.append(f"min {param['min']}")
    if "max" in param:
        bits.append(f"max {param['max']}")
    if param.get("show") is False:
        bits.append("hidden from the UI (show false)")
    if "roles" in param:
        bits.append(f"roles {json.dumps(param['roles'])}")
    if "language" in param:
        bits.append(f"{param['language']} code editor")
    if "description" in param:
        bits.append(f"described \"{param['description']}\"")
    return ", ".join(bits)


def _column_requirement(column: dict) -> str:
    detail = [column.get("cellDataType", "text")]
    if "formatterFn" in column:
        detail.append(f"{column['formatterFn']} formatter")
    if "renderFn" in column:
        rendered = column["renderFn"]
        rendered = rendered if isinstance(rendered, str) else ", ".join(rendered)
        detail.append(f"{rendered} render")
    if "pinned" in column:
        detail.append(f"pinned {column['pinned']}")
    if "chartDataType" in column:
        detail.append(f"chartDataType {column['chartDataType']}")
    text = f"{column['field']} → header \"{column['headerName']}\" ({', '.join(detail)})"
    if "renderFnParams" in column:
        text += f" with renderFnParams {_compact_json(column['renderFnParams'])}"
    return text


def widget_requirements_text(
    widget_id: str,
    definition: dict,
    omit_params: set[str] | None = None,
) -> str:
    """Structured-requirements brief: states every graded field, gives no JSON.

    ``omit_params`` lets a composed (t2/t4) brief factor a shared param out of the
    per-widget list — state it once with shared_param_note instead.
    """

    omit_params = omit_params or set()
    parts = [
        f"`{widget_id}`: name \"{definition['name']}\"",
        f"description \"{definition['description']}\"",
        f"endpoint {definition['endpoint']}",
        f"type {definition.get('type', 'table')}",
    ]
    grid = definition.get("gridData")
    if grid:
        parts.append(f"sized w={grid['w']} h={grid['h']} on the grid")
    for key in ("category", "source", "staleTime", "runButton", "raw", "wsEndpoint"):
        if key in definition:
            parts.append(f"{key} {json.dumps(definition[key])}")
    if "refetchInterval" in definition:
        parts.append(f"refetchInterval {json.dumps(definition['refetchInterval'])}")
    params = [
        param for param in (definition.get("params") or [])
        if isinstance(param, dict) and param.get("paramName") not in omit_params
    ]
    if params:
        has_form = any(p.get("type") == "form" for p in params)
        rendered_params = []
        for p in params:
            text = _param_requirement(p)
            if has_form and p.get("type") != "form":
                text += " (a separate widget-level param, NOT one of the form's inputs)"
            rendered_params.append(text)
        parts.append("params required: " + "; ".join(rendered_params))
    columns = (
        definition.get("data", {}).get("table", {}).get("columnsDefs")
        if isinstance(definition.get("data"), dict)
        else None
    )
    if columns:
        parts.append(
            "table columns required (field → header (type, extras)): "
            + "; ".join(_column_requirement(col) for col in columns)
        )
    data = definition.get("data") if isinstance(definition.get("data"), dict) else {}
    if "dataKey" in data:
        parts.append(f"rows are read from the response key {json.dumps(data['dataKey'])}")
    for key in ("defaultSymbol", "updateFrequency", "wsRowIdColumn"):
        if key in data:
            parts.append(f"data.{key} {json.dumps(data[key])}")
    return ", ".join(parts)


def shared_param_note(param: dict, widget_ids: list[str]) -> str:
    """State a shared param once for a composed payload (t2/t4 factoring)."""

    return (
        f"All of {', '.join(f'`{wid}`' for wid in widget_ids)} take the same shared "
        f"param: {_param_requirement(param)}."
    )


def stamp_consistency(
    widgets: dict, key: str = "staleTime", value=900000
) -> str:
    """Apply one config value to EVERY def in the payload; return the
    convention clause to state ONCE in the prompt.

    The t3 composition dimension for cells with no shared param to group on
    (proxy r2 review): the convention is stated once and applies to all
    widgets, so the model must fan it out — graded on the focus def's full
    checks (and on any anchor extended via anchor_with_expect).
    """

    for definition in widgets.values():
        definition[key] = value
    return f"every widget this backend serves carries {key} {json.dumps(value)}"


def anchor_with_expect(
    backend_name: str, widget_id: str, definition: dict, *keys: str
) -> dict:
    """A sibling anchor extended with named expect keys (e.g. the consistency
    convention key), so a stated convention grades on more than one widget."""

    check = widget_def_anchor_checks(backend_name, widget_id, definition)
    for key in keys:
        if key in definition:
            check["expect"][key] = definition[key]
    return check


# ---------------------------------------------------------------------------
# t1 data derivation: columns are DERIVED from served sample rows under stated
# conventions (the weak fairness invariant: graded values are deterministically
# derivable from stated data + stated rules, like a real analyst brief).
# ---------------------------------------------------------------------------

# t2 policy wording (proxy full-r6): config stated as a desk policy the model
# CONVERTS, not a value it copies. The rule is stated in the prompt alongside
# the policy, so the graded value stays deterministically derivable.
CONFIG_RULES = (
    "Time-based config converts to milliseconds: \"cache results for N "
    "minutes\" means staleTime N*60000; \"auto-refresh every N seconds\" "
    "means refetchInterval N*1000."
)


def cache_policy(minutes: int) -> tuple[dict, str]:
    """(config dict, policy clause) for a cache policy stated in minutes."""

    return (
        {"staleTime": minutes * 60000},
        f"it caches results for {minutes} minutes",
    )


def refresh_policy(seconds: int) -> tuple[dict, str]:
    """(config dict, policy clause) for an auto-refresh policy in seconds."""

    return (
        {"refetchInterval": seconds * 1000},
        f"it auto-refreshes every {seconds} seconds",
    )


DERIVATION_RULES = (
    "Derive the table columns from the served rows using the workspace "
    "conventions: every field in the rows becomes a column, in row order; "
    "headerName is the field name with underscores as spaces, Title Case; "
    "cellDataType is number for numeric values, dateString for ISO dates "
    "(YYYY-MM-DD), boolean for true/false, text otherwise; fields ending in "
    "_pct additionally carry formatterFn percent."
)

# t1 rules carry a worked example (round 8: t1 is one derived aspect with the
# example adjacent; t2 composes the same rules without the example).
DERIVATION_EXAMPLE = (
    "Example: a field {\"filled_pct\": 0.42} becomes {\"field\": \"filled_pct\", "
    "\"headerName\": \"Filled Pct\", \"cellDataType\": \"number\", "
    "\"formatterFn\": \"percent\"}."
)

import re as _re  # noqa: E402

_ISO_DATE = _re.compile(r"^\d{4}-\d{2}-\d{2}(T.*)?$")


def _derived_cell_type(value) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str) and _ISO_DATE.match(value):
        return "dateString"
    return "text"


def derive_table_def(
    name: str,
    description: str,
    endpoint: str,
    rows: list[dict],
    grid: tuple[int, int] = (20, 9),
    params: list[dict] | None = None,
    **extra,
) -> dict:
    """Build the table def DERIVATION_RULES produce from ``rows``.

    Used for t1 data-derivation scenarios: the prompt shows the rows + the rules;
    the oracle/graded definition is exactly this function's output, so the graded
    values are deterministically derivable from what the prompt states.
    """

    columns = []
    for field, value in rows[0].items():
        column = {
            "field": field,
            "headerName": field.replace("_", " ").title(),
            "cellDataType": _derived_cell_type(value),
        }
        if field.endswith("_pct"):
            column["formatterFn"] = "percent"
        columns.append(column)
    definition = {
        "name": name,
        "description": description,
        "endpoint": endpoint,
        "type": "table",
        "gridData": {"w": grid[0], "h": grid[1]},
        "data": {"table": {"columnsDefs": columns}},
    }
    if params:
        definition["params"] = params
    definition.update(extra)
    return definition


def rows_text(rows: list[dict]) -> str:
    return _compact_json(rows)


# ---------------------------------------------------------------------------
# t3 diagnosis: the defect is NOT named in the prompt. The seed carries the
# validator's real flags (readable in the snapshot's custom_backends warnings);
# the prompt restates the widget's requirements and says "fix what's flagged".
# ---------------------------------------------------------------------------

def validation_flags(
    widgets: dict | None = None,
    apps: list | None = None,
    widget_ids: set[str] | None = None,
) -> list[str]:
    """Run the real validator over a (broken) seed and harvest its messages."""

    from workspace_bench.workspace import backend_validation

    flags: list[str] = []
    if widgets is not None:
        errors, warns, _ = backend_validation.validate_widgets_json(widgets)
        flags.extend(errors)
        flags.extend(warns)
    if apps is not None:
        ids = widget_ids if widget_ids is not None else set(widgets or {})
        errors, warns, _ = backend_validation.validate_apps_json(apps, ids)
        flags.extend(errors)
        flags.extend(warns)
    assert flags, "t3 diagnosis seed produced no validation flags"
    return flags


_FLAG_SUBJECT = _re.compile(r"widget '([^']+)'|app '([^']+)'")


def terse_flags(flags: list[str]) -> list[str]:
    """Collapse validator messages to a count badge (round 9).

    The workspace surface shows only that validation failed and how many entries
    are affected — like a real validation badge. Diagnosis means scanning what the
    backend serves against the stated desk conventions; neither the entry nor the
    field is named.
    """

    subjects: set[str] = set()
    for flag in flags:
        match = _FLAG_SUBJECT.search(flag)
        subjects.add((match.group(1) or match.group(2)) if match else "payload")
    count = len(subjects)
    noun = "entry" if count == 1 else "entries"
    return [
        f"workspace validation failed: {count} {noun} in the backend's served "
        "payload need fixing"
    ]


def app_requirements_text(app: dict) -> str:
    """Structured app brief: placements and groups in words, no layout JSON."""

    parts = [f"app \"{app['name']}\""]
    if app.get("description"):
        parts.append(f"description \"{app['description']}\"")
    if "template_id" in app:
        parts.append(f"template_id {app['template_id']}")
    if "allowCustomization" in app:
        parts.append(f"allowCustomization {json.dumps(app['allowCustomization'])}")
    for tab_id, tab in app.get("tabs", {}).items():
        placements = "; ".join(
            f"`{item['i']}` at x={item['x']} y={item['y']} w={item['w']} h={item['h']}"
            + (
                f" preset with params {_compact_json(item['state']['params'])}"
                if item.get("state", {}).get("params")
                else ""
            )
            for item in tab.get("layout", [])
        )
        parts.append(f"tab `{tab_id}` named \"{tab['name']}\" places: {placements}")
    for group in app.get("groups", []) or []:
        bits = [f"group \"{group['name']}\" (type {group.get('type')})"]
        if "paramName" in group:
            bits.append(f"syncing param {group['paramName']}")
        if group.get("widgetIds"):
            bits.append(f"across {_compact_json(group['widgetIds'])}")
        if "defaultValue" in group:
            bits.append(f"default {json.dumps(group['defaultValue'])}")
        parts.append(" ".join(bits))
    prompts = app.get("prompts")
    if prompts:
        parts.append(
            "suggested prompts: " + "; ".join(f"\"{p}\"" for p in prompts)
        )
    return ", ".join(parts)


def widget_brief_text(widget_id: str, definition: dict) -> str:
    """Render a widget-definition brief.

    Scalars read as prose; nested structures (params, columnsDefs, data extras)
    are given as EXACT JSON so the task measures building the definition, not
    decoding pseudo-JSON prose. Calibration round 4 change: mini copied nested
    JSON perfectly at t3 but omitted columnsDefs wholesale when they only
    appeared as prose fragments.
    """

    parts = [
        f"`{widget_id}`: name \"{definition['name']}\"",
        f"description \"{definition['description']}\"",
        f"endpoint {definition['endpoint']}",
        f"type {definition.get('type', 'table')}",
    ]
    grid = definition.get("gridData")
    if grid:
        parts.append(f"gridData w={grid['w']} h={grid['h']}")
    for key in ("category", "source", "staleTime", "runButton", "raw", "wsEndpoint"):
        if key in definition:
            parts.append(f"{key} {json.dumps(definition[key])}")
    if "refetchInterval" in definition:
        parts.append(f"refetchInterval {json.dumps(definition['refetchInterval'])}")
    if "defaultViz" in definition:
        parts.append(f"defaultViz {definition['defaultViz']}")
    params = definition.get("params") or []
    if params:
        parts.append(f"params (exact JSON): {_compact_json(params)}")
    columns = (
        definition.get("data", {}).get("table", {}).get("columnsDefs")
        if isinstance(definition.get("data"), dict)
        else None
    )
    if columns:
        parts.append(
            "columnsDefs (exact JSON, under data.table.columnsDefs): "
            f"{_compact_json(columns)}"
        )
    data = definition.get("data") if isinstance(definition.get("data"), dict) else {}
    for key in ("dataKey", "defaultSymbol", "updateFrequency", "wsRowIdColumn"):
        if key in data:
            parts.append(f"data.{key} {json.dumps(data[key])}")
    return ", ".join(parts)


def app_brief_text(app: dict) -> str:
    parts = [f"app \"{app['name']}\""]
    if app.get("description"):
        parts.append(f"description \"{app['description']}\"")
    if "template_id" in app:
        parts.append(f"template_id {app['template_id']}")
    if "allowCustomization" in app:
        parts.append(f"allowCustomization {json.dumps(app['allowCustomization'])}")
    for tab_id, tab in app.get("tabs", {}).items():
        parts.append(
            f"tab `{tab_id}` named \"{tab['name']}\" with layout (exact JSON): "
            f"{_compact_json(tab.get('layout', []))}"
        )
    groups = app.get("groups") or []
    if groups:
        parts.append(f"groups (exact JSON): {_compact_json(groups)}")
    prompts = app.get("prompts")
    if prompts:
        parts.append(
            "suggested prompts: " + "; ".join(f"\"{prompt}\"" for prompt in prompts)
        )
    return ", ".join(parts)


# ---------------------------------------------------------------------------
# Check derivation — grader blocks derived from the same definitions.
# ---------------------------------------------------------------------------

def widget_def_checks(
    backend_name: str, widget_id: str, definition: dict
) -> dict:
    expect = {
        "type": definition.get("type", "table"),
        "endpoint": definition["endpoint"],
    }
    grid = definition.get("gridData")
    if grid:
        expect["gridData.w"] = grid["w"]
        expect["gridData.h"] = grid["h"]
    for key in ("category", "staleTime", "runButton", "raw", "wsEndpoint", "refetchInterval"):
        if key in definition:
            expect[key] = definition[key]
    data = definition.get("data") if isinstance(definition.get("data"), dict) else {}
    if "dataKey" in data:
        expect["data.dataKey"] = data["dataKey"]
    check: dict = {
        "backend_name": backend_name,
        "widget_id": widget_id,
        "expect": expect,
    }
    params_include = []
    for param in definition.get("params") or []:
        spec = {"paramName": param["paramName"], "type": param.get("type", "text")}
        if "optionsEndpoint" in param:
            spec["optionsEndpoint"] = param["optionsEndpoint"]
        if param.get("multiSelect"):
            spec["multiSelect"] = True
        params_include.append(spec)
    if params_include:
        check["params_include"] = params_include
    columns = (
        definition.get("data", {}).get("table", {}).get("columnsDefs")
        if isinstance(definition.get("data"), dict)
        else None
    )
    if columns:
        columns_include = []
        for column in columns:
            spec = {"field": column["field"], "headerName": column["headerName"]}
            for key in ("cellDataType", "formatterFn", "renderFn"):
                if key in column:
                    spec[key] = column[key]
            columns_include.append(spec)
        check["columns_include"] = columns_include
    return check


def widget_def_anchor_checks(backend_name: str, widget_id: str, definition: dict) -> dict:
    """Presence + anchor fields only (round 11).

    Used for PRESERVED and secondary definitions so grading breadth (check count)
    doesn't drive strict pass rates: strict pass ~= q^N, and re-grading every field
    of every copied def inflates N with near-free checks. Anchors capture the
    preservation skill (didn't drop it, didn't mutate its identity) in 3 checks.
    """

    return {
        "backend_name": backend_name,
        "widget_id": widget_id,
        "expect": {
            "type": definition.get("type", "table"),
            "endpoint": definition["endpoint"],
        },
    }


def app_def_anchor_checks(backend_name: str, app: dict) -> dict:
    """Presence + shape anchors for PRESERVED apps (round 11, see widget anchor)."""

    check: dict = {
        "backend_name": backend_name,
        "tab_count": len(app.get("tabs", {})),
        "layout_refs_valid": True,
    }
    if app.get("template_id"):
        check["template_id"] = app["template_id"]
    else:
        check["name_contains"] = app["name"]
    return check


def app_def_checks(backend_name: str, app: dict) -> dict:
    template_id = app.get("template_id")
    check: dict = {
        "backend_name": backend_name,
        "layout_refs_valid": True,
        "no_overlaps": True,
    }
    if template_id:
        check["template_id"] = template_id
    else:
        check["name_contains"] = app["name"]
    tabs = app.get("tabs", {})
    check["tabs_include"] = sorted(tabs)
    check["tab_count"] = len(tabs)
    widgets_on_tab = [
        {"tab_id": tab_id, "widget_id": item["i"]}
        for tab_id, tab in tabs.items()
        for item in tab.get("layout", [])
    ]
    if widgets_on_tab:
        check["widgets_on_tab"] = widgets_on_tab
    groups_include = []
    for group in app.get("groups", []) or []:
        spec: dict = {"name": group["name"], "type": group.get("type")}
        if "paramName" in group:
            spec["paramName"] = group["paramName"]
        if group.get("widgetIds"):
            spec["widgetIds_include"] = list(group["widgetIds"])
        groups_include.append(spec)
    if groups_include:
        check["groups_include"] = groups_include
    if app.get("prompts"):
        check["prompts_min_count"] = len(app["prompts"])
    expect = {}
    if "allowCustomization" in app:
        expect["allowCustomization"] = app["allowCustomization"]
    if expect:
        check["expect"] = expect
    return check


# ---------------------------------------------------------------------------
# Oracle call builders + seeding helpers
# ---------------------------------------------------------------------------

def snap() -> dict:
    return {"tool": "get_workspace_snapshot", "args": {}}


def add_backend_call(
    name: str, url: str, widgets: dict, apps: list | None = None
) -> dict:
    args = {"operation": "add", "name": name, "url": url, "widgets_json": widgets}
    if apps is not None:
        args["apps_json"] = apps
    return {"tool": "manage_backends", "args": args}


def refresh_call(
    backend_id: str, widgets: dict | None = None, apps: list | None = None
) -> dict:
    args: dict = {"operation": "refresh", "backend_id": backend_id}
    if widgets is not None:
        args["widgets_json"] = widgets
    if apps is not None:
        args["apps_json"] = apps
    return {"tool": "manage_backends", "args": args}


def instantiate_call(backend_id: str, app_name: str, dashboard_name: str) -> dict:
    return {
        "tool": "manage_apps",
        "args": {
            "operation": "instantiate", "backend_id": backend_id,
            "app_name": app_name, "dashboard_name": dashboard_name,
            "activate": True,
        },
    }


def seeded_custom(
    name: str, url: str, widgets: dict, apps: list | None = None,
    backend_id: str = "backend_001",
) -> dict:
    spec: dict = {
        "name": name, "url": url, "backend_id": backend_id,
        "widgets_json": widgets,
    }
    if apps is not None:
        spec["apps_json"] = apps
    return {"custom_backends": [spec]}


BUILD_TOOLS = ["get_workspace_snapshot", "manage_backends"]
APP_TOOLS = BUILD_TOOLS + ["manage_apps"]


# ---------------------------------------------------------------------------
# Desk material — deterministic briefs spanning domains and widget types.
# Inspired by backend-examples-for-openbb-workspace variety + Stark concepts.
# ---------------------------------------------------------------------------

DESKS: dict[str, dict] = {
    "vol": {
        "backend": "Vol Desk Data", "url": "http://localhost:7801",
        "workflow": "risk-review", "subdomain": "volatility",
        "widgets": {
            "vix_history": table_def(
                "VIX History", "Daily CBOE VIX closes with returns.", "/vix-history",
                columns=[
                    ("date", "Date", "dateString"),
                    ("close", "Close", "number"),
                    ("return_pct", "Return %", "number", {"formatterFn": "percent", "renderFn": "greenRed"}),
                ],
                params=[number_param("window", "Window", 30, minimum=5, maximum=365)],
            ),
            "vix_term_structure": simple_def(
                "chart", "VIX Term Structure", "Plotly curve of VIX futures by expiry.",
                "/vix-term-structure", grid=(20, 9), raw=True,
            ),
            "vix_advanced": simple_def(
                "advanced_charting", "VIX Advanced Chart",
                "TradingView advanced charting for VIX futures.", "/udf",
                grid=(20, 20),
                data={"defaultSymbol": "VIX", "updateFrequency": 60000},
            ),
            "vol_commentary": simple_def(
                "markdown", "Vol Commentary", "Morning volatility commentary.",
                "/vol-commentary", grid=(12, 8),
                params=[dropdown_param("desk", "Desk", "index", [("Index", "index"), ("Single Stock", "single")])],
            ),
            "vol_regime_metric": simple_def(
                "metric", "Vol Regime", "Current volatility regime score.",
                "/vol-regime", grid=(6, 4),
            ),
            "vol_screener": simple_def(
                "table", "Vol Screener", "Screen names by implied-vol criteria.",
                "/vol-screener", grid=(24, 10),
                params=[
                    {"paramName": "ticker", "type": "ticker", "label": "Ticker"},
                    date_param("as_of", "As of"),
                    boolean_param("only_liquid", "Liquid only", True),
                ],
            ),
        },
    },
    "tvl": {
        "backend": "Chain TVL Data", "url": "http://localhost:7802",
        "workflow": "portfolio-morning-review", "subdomain": "crypto",
        "widgets": {
            "chains_table": table_def(
                "Top Chains by TVL", "Current TVL of all chains from the desk aggregator.",
                "/chains-table",
                columns=[
                    ("name", "Chain", "text"),
                    ("tvl_usd", "TVL ($)", "number", {"formatterFn": "int"}),
                    ("change_1d", "1d Change", "number", {"formatterFn": "percent", "renderFn": "greenRed"}),
                ],
            ),
            "chains_chart": simple_def(
                "chart", "TVL by Chain", "Plotly bar chart of chain TVL.",
                "/chains-chart", grid=(20, 9), raw=True,
            ),
            "chains_highchart": simple_def(
                "chart-highcharts", "TVL by Chain (Highcharts)",
                "Highcharts rendering of chain TVL.", "/chains-highchart",
                grid=(20, 9),
            ),
            "chains_heatmap_html": simple_def(
                "html", "Chain Heatmap", "Raw HTML heatmap of chain flows.",
                "/chains-heatmap", grid=(20, 10),
            ),
            "protocol_details": simple_def(
                "markdown", "Protocol Details", "Markdown details for one protocol.",
                "/protocol-details", grid=(12, 8),
                params=[text_param("protocol", "Protocol", "uniswap", "Protocol slug to describe.")],
            ),
            "gas_metric": simple_def(
                "metric", "Gas Now", "Current gas price snapshot.", "/gas-now",
                grid=(5, 4),
            ),
        },
    },
    "rates": {
        "backend": "Rates Watch Data", "url": "http://localhost:7803",
        "workflow": "macro-rates-review", "subdomain": "macro",
        "widgets": {
            "yield_curve": simple_def(
                "chart", "Yield Curve", "Plotly treasury yield curve snapshot.",
                "/yield-curve", grid=(20, 9), raw=True,
            ),
            "auction_calendar": table_def(
                "Auction Calendar", "Upcoming treasury auctions.", "/auction-calendar",
                columns=[
                    ("date", "Date", "dateString"),
                    ("security", "Security", "text"),
                    ("size_bn", "Size ($B)", "number"),
                ],
            ),
            "rates_commentary": simple_def(
                "markdown", "Rates Commentary", "Desk commentary on the rates day.",
                "/rates-commentary", grid=(12, 8),
                params=[endpoint_param("series", "Series", "DGS10", "/series-options")],
            ),
            "curve_spread_metric": simple_def(
                "metric", "2s10s Spread", "Current 2s10s spread in bps.",
                "/curve-spread", grid=(6, 4),
            ),
            "curve_monitor_iframe": simple_def(
                "iframe", "Curve Monitor App",
                "Embedded standalone curve monitor application.",
                "http://localhost:5173", grid=(24, 16),
            ),
        },
    },
    "sla": {
        "backend": "Vendor SLA Data", "url": "http://localhost:7804",
        "workflow": "vendor-sla-monitoring", "subdomain": "operations",
        "widgets": {
            "vendor_sla_table": table_def(
                "Vendor SLA Status", "Vendor SLA state with breach flags.", "/vendor-sla",
                columns=[
                    ("vendor", "Vendor", "text"),
                    ("status", "Status", "text", {"renderFn": "titleCase"}),
                    ("latency_ms", "Latency (ms)", "number"),
                    ("breach", "Breach", "boolean"),
                ],
                params=[dropdown_param("status", "Status", "Open", [("Open", "Open"), ("Escalated", "Escalated"), ("Resolved", "Resolved")])],
            ),
            "breach_metric": simple_def(
                "metric", "Open Breaches", "Count of open SLA breaches.", "/breach-count",
                grid=(6, 4),
            ),
            "sla_newsfeed": simple_def(
                "newsfeed", "Vendor Notices", "Vendor incident notices feed.",
                "/vendor-notices", grid=(12, 10),
            ),
            "sla_runbook": simple_def(
                "markdown", "SLA Runbook", "Runbook for SLA escalations.", "/sla-runbook",
                grid=(12, 8),
            ),
            "vendor_intake_form": simple_def(
                "table", "Vendor Intake Form",
                "Submit a new vendor record into the SLA register.",
                "/vendor-intake", grid=(20, 10),
                params=[{
                    "paramName": "intake", "type": "form",
                    "label": "New Vendor", "endpoint": "/vendor-intake-submit",
                    "method": "POST",
                    "inputParams": [
                        {"paramName": "vendor", "type": "text", "label": "Vendor"},
                        {"paramName": "tier", "type": "number", "label": "Tier"},
                        {"paramName": "submit", "type": "button", "label": "Add Vendor"},
                    ],
                }],
            ),
        },
    },
    "earnings": {
        "backend": "Earnings Prep Data", "url": "http://localhost:7805",
        "workflow": "earnings-prep", "subdomain": "equity-research",
        "widgets": {
            "estimate_revisions": table_def(
                "Estimate Revisions", "Street estimate revisions by quarter.", "/estimate-revisions",
                columns=[
                    ("quarter", "Quarter", "text"),
                    ("eps_estimate", "EPS Est", "number"),
                    ("revenue_estimate_b", "Revenue Est ($B)", "number"),
                ],
                params=[endpoint_param("symbol", "Symbol", "AAPL", "/symbols")],
            ),
            "earnings_chart": simple_def(
                "chart", "EPS History", "Plotly EPS beat/miss history.",
                "/eps-history", grid=(20, 9), raw=True,
                params=[endpoint_param("symbol", "Symbol", "AAPL", "/symbols")],
            ),
            "earnings_note": simple_def(
                "markdown", "Earnings Preview", "Preview note for the earnings call.",
                "/earnings-preview", grid=(12, 8),
                params=[endpoint_param("symbol", "Symbol", "AAPL", "/symbols")],
            ),
            "surprise_metric": simple_def(
                "metric", "Avg Surprise", "Average EPS surprise last 4 quarters.",
                "/avg-surprise", grid=(6, 4),
            ),
            "estimates_ssrm": simple_def(
                "ssrm_table", "Estimates Explorer (SSRM)",
                "Server-side sorted and filtered estimates dataset.",
                "/estimates-ssrm", grid=(24, 16),
            ),
            "earnings_calls_video": simple_def(
                "youtube", "Earnings Call Replays", "Replay library of earnings calls.",
                "/call-videos", grid=(20, 12),
                params=[endpoint_param("video", "Video", "q1-call", "/call-video-options")],
            ),
            "kpi_tabs_table": simple_def(
                "table", "KPI Tabs", "KPI table with static and dynamic tab views.",
                "/kpi-tabs", grid=(24, 10),
                params=[{
                    "paramName": "view", "type": "tabs", "label": "View",
                    "value": "growth",
                    "options": [
                        {"label": "Growth", "value": "growth"},
                        {"label": "Margins", "value": "margins"},
                    ],
                }],
            ),
        },
    },
    "execution": {
        "backend": "Execution Desk Data", "url": "http://localhost:7806",
        "workflow": "execution-exception-review", "subdomain": "execution",
        "widgets": {
            "open_orders": table_def(
                "Open Orders", "Live open orders blotter.", "/open-orders",
                columns=[
                    ("order_id", "Order", "text"),
                    ("symbol", "Symbol", "text"),
                    ("qty", "Qty", "number", {"formatterFn": "int"}),
                    ("status", "Status", "text", {"renderFn": "titleCase"}),
                ],
            ),
            "slippage_chart": simple_def(
                "chart", "Slippage by Venue", "Plotly slippage distribution by venue.",
                "/slippage-by-venue", grid=(20, 9), raw=True,
            ),
            "live_orders_grid": {
                "name": "Live Orders Grid",
                "description": "Streaming order blotter over websocket.",
                "endpoint": "/live-orders",
                "type": "live_grid",
                "wsEndpoint": "live-orders-ws",
                "gridData": {"w": 24, "h": 12},
                "data": {
                    "wsRowIdColumn": "order_id",
                    "table": {"columnsDefs": [
                        {"field": "order_id", "headerName": "Order", "cellDataType": "text"},
                        {"field": "px", "headerName": "Price", "cellDataType": "number",
                         "renderFn": "showCellChange",
                         "renderFnParams": {"colorValueKey": "px_change"}},
                    ]},
                },
            },
            "exception_metric": simple_def(
                "metric", "Exceptions", "Open execution exceptions.", "/exception-count",
                grid=(5, 4),
            ),
            "venue_pdf": simple_def(
                "pdf", "Venue Scorecard", "Monthly venue scorecard PDF.", "/venue-scorecard",
                grid=(16, 14),
            ),
        },
    },
    "compliance": {
        "backend": "Surveillance Data", "url": "http://localhost:7807",
        "workflow": "compliance-surveillance", "subdomain": "compliance",
        "widgets": {
            "alert_queue": table_def(
                "Alert Queue", "Open surveillance alerts.", "/alert-queue",
                columns=[
                    ("alert_id", "Alert", "text"),
                    ("desk", "Desk", "text"),
                    ("severity", "Severity", "text", {"renderFn": "titleCase"}),
                    ("age_days", "Age (d)", "number", {"formatterFn": "int"}),
                ],
                params=[dropdown_param("severity", "Severity", "high", [("High", "high"), ("Medium", "medium"), ("Low", "low")])],
            ),
            "case_notes": simple_def(
                "markdown", "Case Notes", "Notes for one surveillance case.", "/case-notes",
                grid=(12, 8),
                params=[text_param("case_id", "Case", "C-1042", "Case identifier.")],
            ),
            "alert_metric": simple_def(
                "metric", "Open Alerts", "Open alert count.", "/alert-count", grid=(5, 4),
            ),
            "policy_pdf": simple_def(
                "pdf", "Policy Digest", "Latest surveillance policy digest.", "/policy-digest",
                grid=(16, 14),
            ),
            "case_qa_omni": simple_def(
                "omni", "Case Q&A", "Ask questions over the surveillance case corpus.",
                "/case-qa", grid=(20, 9),
                params=[{
                    "paramName": "prompt", "type": "text", "label": "Prompt",
                    "description": "Question to run over the case corpus.",
                    "show": False,
                }],
            ),
            "evidence_files": simple_def(
                "multi_file_viewer", "Evidence Files",
                "Browse case evidence documents.", "/evidence-files",
                grid=(20, 14),
                params=[{
                    "paramName": "file", "type": "endpoint", "label": "File",
                    "optionsEndpoint": "/evidence-file-options",
                    "roles": ["fileSelector"], "multiSelect": True,
                    "value": [],
                }],
            ),
        },
    },
    "healthcare": {
        "backend": "Healthcare Research Data", "url": "http://localhost:7808",
        "workflow": "healthcare-catalyst-review", "subdomain": "healthcare",
        "widgets": {
            "trial_catalysts": table_def(
                "Trial Catalysts", "Upcoming clinical trial readouts.", "/trial-catalysts",
                columns=[
                    ("ticker", "Ticker", "text"),
                    ("phase", "Phase", "text"),
                    ("readout_date", "Readout", "dateString"),
                ],
                params=[endpoint_param("ticker", "Ticker", "PFE", "/tickers")],
            ),
            "pipeline_chart": simple_def(
                "chart", "Pipeline by Phase", "Plotly pipeline distribution by phase.",
                "/pipeline-by-phase", grid=(20, 9), raw=True,
            ),
            "pipeline_vegalite": simple_def(
                "chart-vegalite", "Pipeline Mix (Vega-Lite)",
                "Vega-Lite bar spec of pipeline phase mix.", "/pipeline-vegalite",
                grid=(20, 9),
            ),
            "fda_newsfeed": simple_def(
                "newsfeed", "FDA Notices", "FDA decision and notice feed.", "/fda-notices",
                grid=(12, 10),
            ),
            "catalyst_metric": simple_def(
                "metric", "Catalysts 30d", "Catalysts in the next 30 days.",
                "/catalyst-count", grid=(6, 4),
            ),
        },
    },
}

DESK_KEYS = tuple(DESKS)


def desk(key: str) -> dict:
    return DESKS[key]


def desk_widget(key: str, widget_id: str) -> dict:
    return json.loads(json.dumps(DESKS[key]["widgets"][widget_id]))


# ---------------------------------------------------------------------------
# Novelty, splits, lattice, quotas
# ---------------------------------------------------------------------------

def scenario_check_types(scenario: dict) -> tuple:
    success = scenario.get("success", {})
    kinds = set()
    mapping = {
        "required_tabs": "missing_tab",
        "required_widgets": "missing_widget",
        "required_generated_widgets": "missing_generated_widget",
        "required_layouts": "layout_mismatch",
        "required_tool_calls": "missing_tool_call",
        "required_tool_results": "missing_tool_result",
        "required_resource_reads": "missing_resource_read",
        "required_widget_defs": "widget_def",
        "required_app_defs": "app_def",
    }
    for key, kind in mapping.items():
        if success.get(key):
            kinds.add(kind)
    if success.get("required_dashboard_name_contains"):
        kinds.add("dashboard_name")
    layout = success.get("layout", {})
    if layout.get("within_grid"):
        kinds.add("layout_out_of_grid")
    if layout.get("no_overlaps"):
        kinds.add("layout_overlap")
    trace = success.get("trace_checks", {})
    if trace.get("max_invalid_tool_calls") is not None:
        kinds.add("too_many_invalid_calls")
    if trace.get("must_call_schema_before_create"):
        kinds.add("schema_not_called_before_create")
    if trace.get("max_repeated_snapshots") is not None:
        kinds.add("repeated_snapshots")
    return tuple(sorted(kinds))


def scenario_backends(scenario: dict) -> set[str]:
    backends = {
        ref.get("name")
        for ref in scenario.get("fixtures", {}).get("backends", [])
        if isinstance(ref, dict)
    }
    for spec in scenario.get("initial_state", {}).get("custom_backends", []) or []:
        backends.add(f"custom:{spec.get('name')}")
    for call in scenario.get("oracle_tool_calls", []):
        if call.get("tool") == "manage_backends" and call.get("args", {}).get("operation") == "add":
            if "widgets_json" in call.get("args", {}):
                backends.add(f"custom:{call['args'].get('name')}")
    backends.discard(None)
    return backends


def artifact_discriminator(scenario: dict) -> str:
    success = scenario.get("success", {})
    parts: list[str] = []
    widget_defs = [
        f"{req['backend_name']}/{req['widget_id']}"
        for req in success.get("required_widget_defs", [])
    ]
    if widget_defs:
        parts.append("widgetdefs:" + ",".join(sorted(widget_defs)))
    app_defs = [
        f"{req['backend_name']}/{req.get('template_id') or req.get('name_contains')}"
        for req in success.get("required_app_defs", [])
    ]
    if app_defs:
        parts.append("appdefs:" + ",".join(sorted(app_defs)))
    widgets = [
        f"{req.get('origin')}/{req.get('widget_id')}@{req.get('tab_id', '*')}"
        for req in success.get("required_widgets", [])
        if int(req.get("min_count", 1)) > 0
    ]
    if widgets:
        parts.append("widgets:" + ",".join(sorted(widgets)))
    tabs = success.get("required_tabs", [])
    if tabs:
        parts.append("tabs:" + ",".join(sorted(tabs)))
    generated = [
        f"{req.get('widget_type')}@{req.get('tab_id', '*')}:{','.join(req.get('data_contains', [])[:2])}"
        for req in success.get("required_generated_widgets", [])
    ]
    if generated:
        parts.append("generated:" + ",".join(sorted(generated)))
    if not parts:
        parts.append("id:" + scenario["id"])
    return "|".join(parts)


def novelty_fingerprint(scenario: dict) -> tuple:
    oracle_tools = tuple(sorted({call["tool"] for call in scenario["oracle_tool_calls"]}))
    return (
        scenario["_family"], scenario["_tier"], oracle_tools,
        scenario_check_types(scenario), tuple(sorted(scenario_backends(scenario))),
        artifact_discriminator(scenario),
    )


def add_novelty(scenario: dict) -> None:
    tools = ", ".join(sorted({call["tool"] for call in scenario["oracle_tool_calls"]}))
    checks = ", ".join(scenario_check_types(scenario))
    backends = ", ".join(sorted(scenario_backends(scenario))) or "no preloaded backend"
    artifact = artifact_discriminator(scenario).replace("|", "; ")
    scenario["novelty"] = (
        f"Unique {scenario['_family']}/{scenario['_tier']} building exercise using "
        f"{tools} with checks {checks} on {backends}; artifact {artifact}."
    )


SPLIT_PATTERNS = {
    "t0": ("train", "train", "train", "validation"),
    "t1": ("train", "train", "validation", "test"),
    "t2": ("train", "train", "validation", "test"),
    "t3": ("train", "train", "validation", "test"),
    "t4": ("train", "train", "train", "test"),
}


def assign_splits(scenarios: list[dict]) -> None:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for scenario in scenarios:
        grouped[(scenario["_family"], scenario["_tier"])].append(scenario)
    for (family, tier), cell in grouped.items():
        cell.sort(key=lambda item: item["id"])
        if family == CAPSTONE_FAMILY:
            assert len(cell) == E2E_COUNT, (
                f"{family}/{tier} expected {E2E_COUNT}, got {len(cell)}"
            )
            pattern = ("train", "train", "validation", "test") * (E2E_COUNT // 4)
        else:
            assert len(cell) == 4, f"split assignment expects 4 scenarios in {family}/{tier}"
            pattern = SPLIT_PATTERNS[tier]
        for scenario, split in zip(cell, pattern):
            scenario["split"] = split


def build_matrix(scenarios: list[dict]) -> dict[str, dict[str, int]]:
    matrix: dict[str, dict[str, int]] = {}
    for scenario in scenarios:
        family, tier = scenario["_family"], scenario["_tier"]
        matrix.setdefault(family, {})[tier] = matrix.setdefault(family, {}).get(tier, 0) + 1
    return matrix


def assert_lattice(matrix: dict[str, dict[str, int]]) -> None:
    expected = set(LADDER_FAMILIES) | {CAPSTONE_FAMILY}
    assert set(matrix) == expected, (
        f"expected families {sorted(expected)}, got {sorted(matrix)}"
    )
    for family in LADDER_FAMILIES:
        for tier in TIERS:
            count = matrix[family].get(tier, 0)
            assert count == 4, f"{family}/{tier} expected 4, got {count}"
    capstone = matrix[CAPSTONE_FAMILY]
    assert capstone.get("t4", 0) == E2E_COUNT and set(capstone) == {"t4"}, (
        f"{CAPSTONE_FAMILY} must be exactly {E2E_COUNT} scenarios at t4, got {capstone}"
    )
