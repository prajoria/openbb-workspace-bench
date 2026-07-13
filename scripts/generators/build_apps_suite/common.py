"""Shared machinery for the WorkspaceBench Part 2 build-openbb-apps collection generator.

Design invariant: every task is built from one authored widget/app spec. The
oracle retains the exact valid payload; a separate functionalization pass turns
it into an open product brief, relaxes byte-level checks to declared behavior,
offers the complete tool surface, and requires the result to be placed or opened.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlparse

from _assembly import (
    ArtifactDiscriminator,
    CheckTypePolicy,
    NoveltyPolicy,
    PhrasingSelector,
    TaskAssembler,
    build_matrix as build_matrix,
    difficulty_for,
    diversify_generated_widget_proof,
    snap as snap,
)
from workspace_bench.workspace.runtime import declared_fields
from workspace_bench.workspace.tool_surface import WORKSPACE_TOOL_NAMES
from workspace_bench.workspace.widget_params import flatten_params

REPO = Path(__file__).resolve().parents[3]
BUNDLED_OUT_DIR = REPO / "src/workspace_bench/task_suites/build_openbb_apps"

RUNGS = ("r0", "r1", "r2", "r3", "r4")
# r4 slack is wider than part 1's because building oracles are SHORT (a 2-call
# oracle with slack 2 leaves zero margin for one validation round-trip).
# 5 -> 4 in proxy r4: with r4 now building r3-grade content plus operating it,
# one budgeted recovery round-trip is enough; two made orchestration too soft.
RUNG_SLACK = {"r0": 3, "r1": 3, "r2": 3, "r3": 3, "r4": 4}

# v3 families mirror the onboarding reference app (getting-started/
# reference-backend "Onboarding App for Devs") — each family is one tab theme,
# so widget-type coverage is by construction, not by quota (Didier review,
# 2026-07-08). `apps`/`extend` carry the app-side surfaces; `e2e` stays the
# r4-only capstone.
WIDGET_FAMILIES = (
    "types",
    "settings",
    "params",
    "forms",
    "aggrid",
    "charts",
    "advanced",
    "grouping",
)
APP_FAMILIES = ("apps", "extend")
LADDER_FAMILIES = WIDGET_FAMILIES + APP_FAMILIES
CAPSTONE_FAMILY = "e2e"
E2E_COUNT = 12
DEBUG_FAMILY = "debug"
DEBUG_COUNT = 24
DEBUG_RUNG = "debug"
ALL_RUNGS = RUNGS + (DEBUG_RUNG,)

CAPABILITY = {
    "types": "widget-building",
    "settings": "widget-building",
    "params": "widget-building",
    "forms": "widget-building",
    "aggrid": "widget-building",
    "charts": "widget-building",
    "advanced": "widget-building",
    "grouping": "widget-building",
    "apps": "app-building",
    "extend": "app-building",
    "e2e": "backend-integration",
    "debug": "backend-repair",
}

# Widget-type / param-type ownership per family (asserted at certification):
# every owned key must appear in that family's built artifacts. The maps live
# in the package so `workspace-bench validate` re-verifies the same gate on
# the shipped suite.
from workspace_bench.core.suite_checks import (  # noqa: E402, F401 - re-exported
    BUILD_MEASURED_DIFFICULTY_OVERRIDES as MEASURED_DIFFICULTY_OVERRIDES,
    BUILD_PARAM_OWNERSHIP as PARAM_OWNERSHIP,
    BUILD_TYPE_OWNERSHIP as TYPE_OWNERSHIP,
)

SCENARIOS: list[dict] = []
CELL_COUNTS: dict[tuple[str, str], int] = {}
PROMPT_POOL_SIZES: dict[str, int] = {}
VOLUME_TASKS = {
    ("aggrid", "estimates_ssrm"),
    ("advanced", "orders_stream"),
    ("e2e", "execution_monitor"),
}

# Building is a validation-loop workflow by design: the simulator's rejections are
# specific and actionable (mirroring the real product), so one rejected round-trip is
# budgeted rather than fatal. Calibration decision after gate run 2.
TRACE_ZERO = {"max_invalid_tool_calls": 1, "max_repeated_snapshots": 2}
# r4 carries orchestration risk on top of building; two budgeted round-trips keep
# its difficulty about breadth rather than sudden death (round-11 flakiness fix:
# 15% of r4 tasks flipped between identical runs, several on budget alone).
TRACE_T4 = {"max_invalid_tool_calls": 2, "max_repeated_snapshots": 2}


phrased = PhrasingSelector(PROMPT_POOL_SIZES)


def specification_level_for(level: str, cell_index: int) -> str:
    """Return the structural prompt/grading rung independently of difficulty."""

    return {
        "easy": "explicit",
        "medium": "partially-specified",
        "hard": "open-brief",
    }[difficulty_for(level, cell_index)]


def category_for(family: str) -> str:
    # v3: repair-under-preservation lives in the `extend` family (L4); the
    # rest of the pack is platform work (L3).
    return "repair" if family == "extend" else "platform"


def _set_build_category(task: dict, family: str) -> None:
    task.setdefault("category", category_for(family))


def _noop_identity(task: dict) -> None:
    del task


def _set_build_capability(
    task: dict, family: str, level: str, cell_index: int
) -> None:
    del level, cell_index
    task.setdefault("capability", CAPABILITY[family])


def _set_build_difficulty(
    task: dict, family: str, level: str, cell_index: int
) -> None:
    task_ref = f"build-openbb-apps/{family}/{task['id']}"
    structural_difficulty = difficulty_for(level, cell_index)
    task["specification_level"] = specification_level_for(level, cell_index)
    task["difficulty"] = MEASURED_DIFFICULTY_OVERRIDES.get(
        task_ref, structural_difficulty
    )
    # Invalid-call budget scales with single-payload size (proxy r4): r3 ships
    # the largest one-shot payload in the ladder (2-3 defs + multi-tab app +
    # convention), so it gets the same validation-loop allowance as r4's
    # multi-step flow. Enforced centrally so modules cannot underspend it.
    if level in ("r3", "r4"):
        trace = task.get("success", {}).setdefault("trace_checks", {})
        if trace.get("max_invalid_tool_calls", 0) < 2:
            trace["max_invalid_tool_calls"] = 2


def _build_tag_prefixes(family: str, level: str, cell_index: int) -> tuple[str, str]:
    del level
    return (f"family-{family}", f"cell{cell_index}")


def _finalize_build_task(
    task: dict, family: str, level: str, cell_index: int
) -> None:
    del cell_index
    _functionalize_task(task, family=family, level=level)
    _ensure_behavioral_field_contracts(task)
    _attach_runtime_checks(task)
    _apply_volume_tier(task, family=family)
    _migrate_behavioral_requirements(task, family=family)
    _render_prompt_contract(task, family=family, level=level)
    diversify_generated_widget_proof(task, share=20, selected_buckets=7)


add = TaskAssembler(
    scenarios=SCENARIOS,
    cell_counts=CELL_COUNTS,
    source="workspace-bench-build-apps-gen",
    rung_slack=RUNG_SLACK,
    set_category=_set_build_category,
    normalize_identity=_noop_identity,
    after_identity=_set_build_capability,
    set_difficulty=_set_build_difficulty,
    tag_prefixes=_build_tag_prefixes,
    finalize_task=_finalize_build_task,
).add


def _ensure_behavioral_field_contracts(task: dict) -> None:
    """Give every behavior-graded widget an explicit response-field contract."""

    if task.get("specification_level") == "explicit":
        return
    widgets, _ = _authored_payload(task)
    for widget_id, definition in widgets.items():
        if declared_fields(definition):
            continue
        field = f"{_slug(widget_id).replace('-', '_')}_value"
        definition.setdefault("data", {})["valueField"] = field


def _attach_runtime_checks(task: dict) -> None:
    """Author the deterministic response universe beside each custom build task."""

    widgets, _ = _authored_payload(task)
    if not widgets:
        return
    backend_name, _, _ = _backend_identity(task)
    datasets = [
        runtime_dataset(backend_name, widget_id, definition)
        for widget_id, definition in sorted(widgets.items())
    ]
    task.setdefault("success", {})["runtime_checks"] = {
        "datasets": datasets,
        # Product briefs intentionally allow agents to choose endpoint architecture.
        "pinned_paths": False,
    }


def _apply_volume_tier(task: dict, *, family: str) -> None:
    """Upgrade three existing tasks to compact 10k-row deterministic data."""

    if (family, str(task.get("id"))) not in VOLUME_TASKS:
        return
    datasets = task.get("success", {}).get("runtime_checks", {}).get("datasets", [])
    if not datasets:
        return
    dataset = datasets[0]
    fields = [str(field) for field in dataset.get("fields", [])]
    schema: dict[str, str] = {}
    for field in fields:
        lowered = field.casefold()
        if "date" in lowered or lowered.endswith("_at"):
            schema[field] = "date"
        elif any(token in lowered for token in ("count", "days", "rank", "id")):
            schema[field] = "integer"
        elif any(token in lowered for token in ("price", "value", "pct", "rate", "amount")):
            schema[field] = "number"
        else:
            schema[field] = "string"
    widgets, _ = _authored_payload(task)
    definition = widgets.get(str(dataset.get("widget_id")), {})
    data_key = (
        (definition.get("data") or {}).get("dataKey", "rows")
        if definition.get("type") == "table_ssrm"
        else "rows"
    )
    dataset.pop("payload", None)
    dataset["payload_spec"] = {
        "generator": "seeded_rows",
        "seed": int(hashlib.sha256(str(task["id"]).encode()).hexdigest()[:8], 16),
        "n_rows": 10_000,
        "schema": schema,
        "data_key": data_key,
    }


def runtime_dataset(backend_name: str, widget_id: str, definition: dict) -> dict:
    """Build stable, typed fixture data from one authored widget contract."""

    fields = sorted(declared_fields(definition))
    widget_type = str(definition.get("type", "table"))
    if not fields and widget_type in {
        "table",
        "table_ssrm",
        "live_grid",
        "chart",
        "chart-highcharts",
        "chart-vegalite",
        "advanced_charting",
    }:
        fields = ["category", "value"]
    rows = [
        {field: _field_value(field, definition, row_index) for field in fields}
        for row_index in range(1, 4)
    ]
    if widget_type == "table_ssrm":
        data_key = (definition.get("data") or {}).get("dataKey", "rows")
        payload: object = {data_key: rows, "lastRow": len(rows)}
    elif widget_type in {
        "table",
        "live_grid",
        "chart",
        "chart-highcharts",
        "chart-vegalite",
        "advanced_charting",
    }:
        payload = rows
    elif widget_type == "metric":
        fields = sorted(set(fields) | {"label", "value"})
        payload = {
            field: _field_value(field, definition, 1)
            for field in fields
        }
        payload.update({"label": str(definition.get("name", widget_id)), "value": 42.5})
    elif widget_type == "markdown":
        payload = f"{definition.get('name', widget_id)} fixture-backed runtime summary."
    elif widget_type == "html":
        payload = f"<section><h1>{definition.get('name', widget_id)}</h1><p>Runtime data ready.</p></section>"
    elif widget_type == "newsfeed":
        fields = sorted(set(fields) | {"title", "published_at", "summary"})
        payload = [
            {
                **{
                    field: _field_value(field, definition, 1)
                    for field in fields
                },
                "title": f"{definition.get('name', widget_id)} update",
                "published_at": "2026-01-15T14:30:00Z",
                "summary": "Fixture-backed desk update with verified data.",
            }
        ]
    elif widget_type in {"pdf", "youtube", "iframe", "multi_file_viewer"}:
        fields = sorted(set(fields) | {"title", "url"})
        payload = {
            **{
                field: _field_value(field, definition, 1)
                for field in fields
            },
            "title": str(definition.get("name", widget_id)),
            "url": f"https://fixtures.workspace-bench.invalid/{widget_id}",
        }
    elif widget_type == "omni":
        fields = sorted(set(fields) | {"answer", "sources"})
        payload = {
            **{
                field: _field_value(field, definition, 1)
                for field in fields
            },
            "answer": "Verified fixture-backed result.",
            "sources": ["task-dataset"],
        }
    else:
        fields = ["value"]
        payload = {"value": 42.5}
    endpoint = str(definition.get("endpoint", "/"))
    dataset = {
        "name": f"{_slug(backend_name)}__{widget_id}",
        "widget_id": widget_id,
        "fields": fields,
        "path": urlparse(endpoint).path or "/",
        "payload": payload,
    }
    form_endpoint = next(
        (
            str(param["endpoint"])
            for param in flatten_params(definition, recurse=True)
            if str(param.get("method", "GET")).upper() == "POST"
            and param.get("endpoint")
        ),
        None,
    )
    if form_endpoint is not None:
        dataset["form_endpoint"] = urlparse(form_endpoint).path or "/"
    return dataset


def _capability_param_kind(param: dict) -> str:
    name = str(param.get("paramName", "")).casefold()
    param_type = str(param.get("type", "text")).casefold()
    roles = {str(role).casefold() for role in param.get("roles", []) or []}
    if param_type == "ticker" or name in {"symbol", "ticker", "tickers"} or "ticker" in roles:
        return "ticker"
    if param_type == "date" or "date" in name:
        return "date"
    if param_type in {"endpoint", "number", "boolean", "tabs", "form", "button"}:
        return param_type
    return "text"


def _capability_widget_kind(definition: dict) -> str:
    widget_type = str(definition.get("type", "table"))
    if any(
        str(param.get("type")) in {"form", "button"}
        for param in flatten_params(definition, recurse=True)
    ):
        return "form"
    if widget_type in {"table_ssrm", "live_grid"}:
        return "server-side-grid"
    if widget_type == "table":
        return "table-like"
    if widget_type in {"chart", "chart-highcharts", "chart-vegalite", "advanced_charting"}:
        return "chart-like"
    if widget_type == "metric":
        return "metric"
    if widget_type == "multi_file_viewer":
        return "multi-file"
    if widget_type in {"html", "iframe", "markdown", "newsfeed", "pdf", "youtube"}:
        return widget_type
    return "any"


def _aggregate_runtime_dataset(task: dict, widgets: dict[str, dict]) -> str:
    """Add one union dataset so a legal alternative may merge authored widgets."""

    success = task.setdefault("success", {})
    runtime = success.get("runtime_checks") or {}
    datasets = runtime.get("datasets") or []
    fields = sorted(
        {field for definition in widgets.values() for field in declared_fields(definition)}
    )
    name = f"capability-union__{task['id']}"
    rows = [
        {field: _field_value(field, {}, row_index) for field in fields} for row_index in range(1, 4)
    ]
    datasets.append(
        {
            "name": name,
            "widget_id": f"capability_union_{task['id']}",
            "fields": fields,
            "path": "/capability-union",
            "payload": rows or [{"value": 42.5}],
        }
    )
    runtime["datasets"] = datasets
    success["runtime_checks"] = runtime
    return name


def _migrate_behavioral_requirements(task: dict, *, family: str) -> None:
    """Replace medium/hard oracle-shaped rubrics with behavioral capabilities."""

    if task.get("specification_level") == "explicit":
        return
    widgets, apps = _authored_payload(task)
    if not widgets:
        return
    success = task.setdefault("success", {})
    required_widget_ids = {
        str(required.get("widget_id"))
        for required in success.get("required_widgets", [])
        if int(required.get("min_count", 1)) > 0
    }
    behavioral_widgets = {
        widget_id: definition
        for widget_id, definition in widgets.items()
        if widget_id in required_widget_ids
    }
    if not behavioral_widgets:
        behavioral_widgets = widgets
    runtime_datasets = {
        str(dataset.get("widget_id")): str(dataset.get("name"))
        for dataset in success["runtime_checks"]["datasets"]
    }
    capabilities: list[dict] = []
    capability_by_widget: dict[str, str] = {}
    exact_by_widget = {
        str(required.get("widget_id")): required
        for required in success.get("required_widget_defs", [])
    }
    for index, (widget_id, definition) in enumerate(sorted(behavioral_widgets.items()), start=1):
        capability_name = f"capability_{index}_{_slug(widget_id)}"
        capability_by_widget[widget_id] = capability_name
        param_kinds = sorted(
            {
                _capability_param_kind(param)
                for param in flatten_params(definition, recurse=True)
            }
        )
        capabilities.append(
            {
                "name": capability_name,
                "datasets": [runtime_datasets[widget_id]],
                "widget_kind": _capability_widget_kind(definition),
                "must_cover_fields": sorted(declared_fields(definition)),
                "required_param_kinds": param_kinds,
                "required_config": {
                    path: expected
                    for path, expected in exact_by_widget.get(widget_id, {})
                    .get("expect", {})
                    .items()
                    if path not in {"type", "endpoint", "staleTime", "refetchInterval"}
                },
            }
        )

    connections: list[dict] = []
    connected_widgets: set[str] = set()
    for app in apps:
        for group in app.get("groups", []) or []:
            param_name = str(group.get("paramName", ""))
            grouped = [
                str(widget_id)
                for widget_id in group.get("widgetIds", []) or []
                if str(widget_id) in capability_by_widget
            ]
            param_kind = "text"
            for widget_id in grouped:
                matching = next(
                    (
                        param
                        for param in flatten_params(
                            behavioral_widgets[widget_id], recurse=True
                        )
                        if str(param.get("paramName", "")) == param_name
                    ),
                    None,
                )
                if matching is not None:
                    param_kind = _capability_param_kind(matching)
                    break
            for index, source_widget in enumerate(grouped):
                for target_widget in grouped[index + 1 :]:
                    connected_widgets.update((source_widget, target_widget))
                    connections.append(
                        {
                            "source": capability_by_widget[source_widget],
                            "target": capability_by_widget[target_widget],
                            "param_kind": param_kind,
                        }
                    )

    mergeable_widgets = {
        widget_id: definition
        for widget_id, definition in behavioral_widgets.items()
        if widget_id not in connected_widgets
        and str(definition.get("type", "table")) == "table"
    }
    if len(mergeable_widgets) >= 2:
        aggregate_dataset = _aggregate_runtime_dataset(task, mergeable_widgets)
        mergeable_capabilities = {
            capability_by_widget[widget_id] for widget_id in mergeable_widgets
        }
        for capability in capabilities:
            if capability["name"] in mergeable_capabilities:
                capability["datasets"].append(aggregate_dataset)

    polish: list[dict] = []
    for required in success.get("required_widget_defs", []):
        for path, expected in required.get("expect", {}).items():
            if path not in {"refetchInterval", "staleTime"}:
                continue
            polish.append(
                {
                    "code": "polish_refresh_policy",
                    "backend_name": required["backend_name"],
                    "widget_id": required["widget_id"],
                    "path": path,
                    "expected": expected,
                }
            )

    success["required_capabilities"] = capabilities
    if connections:
        success["capability_connections"] = connections
    if apps:
        success["app_structure"] = {
            "required": True,
            "layout_refs_valid": True,
            "no_overlaps": True,
        }
    if family == "e2e" and success.get("required_dashboard_name_contains"):
        success["business_names"] = [
            {
                "scope": "dashboard",
                "contains": success["required_dashboard_name_contains"],
            }
        ]
    if polish:
        success["polish"] = polish

    # Capabilities and generic app checks carry these outcomes without pinning
    # backend names, widget ids, tab ids, app ids, or authored layout geometry.
    success.pop("required_widget_defs", None)
    success.pop("required_app_defs", None)
    success.pop("required_widgets", None)
    success.pop("required_tabs", None)
    success.pop("required_layouts", None)
    success.pop("required_dashboard_name_contains", None)


def _field_value(field: str, definition: dict, row_index: int) -> object:
    lower = field.lower()
    data = definition.get("data")
    table = data.get("table") if isinstance(data, dict) else None
    column_types = {
        str(column.get("field")): str(column.get("cellDataType", ""))
        for column in (table or {}).get("columnsDefs", [])
        if isinstance(column, dict)
    }
    cell_type = column_types.get(field, "").lower()
    if "date" in lower or "date" in cell_type or "time" in lower:
        return f"2026-01-{12 + row_index:02d}"
    if cell_type == "boolean" or lower.startswith(("is_", "has_")) or lower.endswith("_beat"):
        return row_index % 2 == 1
    if cell_type == "number" or any(
        token in lower
        for token in (
            "value",
            "price",
            "px",
            "close",
            "yield",
            "rate",
            "pct",
            "percent",
            "count",
            "age",
            "days",
            "amount",
            "score",
            "latency",
            "weight",
            "eps",
            "revenue",
            "volume",
            "spread",
            "change",
            "rank",
            "priority",
        )
    ):
        return round(10.25 * row_index, 2)
    if lower in {"symbol", "ticker"}:
        return ("AAPL", "MSFT", "NVDA")[row_index - 1]
    if lower in {"category", "phase", "status", "severity", "desk", "venue"}:
        return ("Primary", "Review", "Approved")[row_index - 1]
    return f"{field}-{row_index}"


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _functionalize_task(task: dict, *, family: str, level: str) -> None:
    """Turn an authored-schema exercise into an outcome-based build task.

    The exact payload remains the oracle implementation, but the model sees a
    product brief and grading checks only declared behavior plus a live
    dashboard instantiation. All tools are available so tool selection is part
    of the evaluation rather than encoded by the allowlist.
    """

    task["allowed_tools"] = list(WORKSPACE_TOOL_NAMES)
    task["title"] = _clean_title(str(task["title"]))
    success = task.setdefault("success", {})
    _relax_schema_checks(success, family=family, level=level)
    _add_functional_oracle(task)
    _bind_generated_evidence(task)
    success.setdefault("workspace_checks", {}).update(
        {
            "preserve_other_dashboards": True,
            "max_dashboard_delta": 1 if success.get("required_app_defs") else 0,
            "max_custom_backend_delta": _expected_backend_delta(task),
        }
    )


def _bind_generated_evidence(task: dict) -> None:
    """Bind completion notes to semantic facts instead of authored prose."""

    calls = [
        call.get("args", {})
        for call in task.get("oracle_tool_calls", [])
        if call.get("tool") == "add_generative_widget"
    ]
    backend_name, _, _ = _backend_identity(task)
    configured_facts: list[tuple[str, str]] = []
    for widget in task.get("success", {}).get("required_widgets", []):
        for key, value in (widget.get("data_args") or {}).items():
            if isinstance(value, (str, int, float, bool)):
                configured_facts.append((str(key), str(value)))
    for required in task.get("success", {}).get("required_generated_widgets", []):
        match = next(
            (
                args
                for args in calls
                if args.get("widget_type") == required.get("widget_type")
                and (
                    not required.get("name_contains")
                    or required["name_contains"].lower() in str(args.get("name", "")).lower()
                )
            ),
            None,
        )
        if match is None:
            continue
        fragments = [str(item) for item in required.get("data_contains", [])]
        for fragment in (match.get("name"), backend_name):
            if fragment and not any(
                str(fragment).lower() == existing.lower() for existing in fragments
            ):
                fragments.append(str(fragment))
        for _, value in configured_facts:
            if value and not any(value.lower() == existing.lower() for existing in fragments):
                fragments.append(value)
        required["data_contains"] = fragments
        if configured_facts and isinstance(match.get("data"), str):
            rendered = ", ".join(f"{key}={value}" for key, value in configured_facts)
            match["data"] = f"{match['data']} Configured {rendered}."


def _clean_title(title: str) -> str:
    words = title.split()
    cleaned: list[str] = []
    for word in words:
        normalized = re.sub(r"[^a-z0-9]", "", word.lower())
        previous = re.sub(r"[^a-z0-9]", "", cleaned[-1].lower()) if cleaned else ""
        if normalized and normalized == previous:
            continue
        cleaned.append(word)
    return " ".join(cleaned)


def _relax_schema_checks(success: dict, *, family: str, level: str) -> None:
    policy_keys = {"staleTime", "refetchInterval", "runButton", "raw"}
    advanced_keys = {
        "wsEndpoint",
        "data.defaultSymbol",
        "data.updateFrequency",
        "data.wsRowIdColumn",
        "data.dataKey",
    }
    for required in success.get("required_widget_defs", []):
        expect = required.get("expect", {})
        keep = {"type", "endpoint"}
        if family in {"settings", "advanced", "aggrid", "charts", "extend"}:
            keep |= policy_keys
        if family in {"advanced", "aggrid"}:
            keep |= advanced_keys
        required["expect"] = {key: value for key, value in expect.items() if key in keep}
        required["params_include"] = [
            {
                key: value
                for key, value in param.items()
                if key
                in {
                    "paramName",
                    "type",
                    "optionsEndpoint",
                    "multiSelect",
                    "endpoint",
                    "method",
                }
            }
            for param in required.get("params_include", [])
        ]
        required["columns_include"] = [
            {
                key: value
                for key, value in column.items()
                if key in {"field", "cellDataType", "formatterFn", "renderFn"}
            }
            for column in required.get("columns_include", [])
        ]
        if level in {"r3", "r4"}:
            # Higher levels grade the meaningful interface, not presentation
            # defaults or a byte-for-byte reconstruction of the author spec.
            required["params_include"] = [
                {key: value for key, value in param.items() if key in {"paramName", "type"}}
                for param in required.get("params_include", [])
            ]
            required["columns_include"] = [
                {"field": column["field"]}
                for column in required.get("columns_include", [])
                if column.get("field")
            ]


def _backend_call(task: dict) -> dict | None:
    for call in task.get("oracle_tool_calls", []):
        args = call.get("args", {})
        if call.get("tool") == "manage_backends" and (
            args.get("widgets_json") or args.get("apps_json")
        ):
            return call
    return None


def _backend_identity(task: dict) -> tuple[str, str, str]:
    call = _backend_call(task)
    args = call.get("args", {}) if call else {}
    initial = (task.get("initial_state", {}).get("custom_backends") or [{}])[0]
    name = str(args.get("name") or initial.get("name") or "Custom Backend")
    url = str(args.get("url") or initial.get("url") or "")
    backend_id = str(args.get("backend_id") or initial.get("backend_id") or "backend_001")
    return name, url, backend_id


def _authored_payload(task: dict) -> tuple[dict, list[dict]]:
    call = _backend_call(task)
    if not call:
        return {}, []
    args = call.get("args", {})
    widgets = args.get("widgets_json") or {}
    if not widgets:
        backend_name, _, _ = _backend_identity(task)
        widgets = next(
            (
                backend.get("widgets_json") or {}
                for backend in task.get("initial_state", {}).get("custom_backends", []) or []
                if backend.get("name") == backend_name
            ),
            {},
        )
    return widgets, args.get("apps_json") or []


def _add_functional_oracle(task: dict) -> None:
    success = task.setdefault("success", {})
    widgets, apps = _authored_payload(task)
    backend_name, _, backend_id = _backend_identity(task)
    oracle = task.setdefault("oracle_tool_calls", [])
    has_live_widget = bool(success.get("required_widgets"))
    has_instantiation = any(
        call.get("tool") == "manage_apps" and call.get("args", {}).get("operation") == "instantiate"
        for call in oracle
    )

    if apps:
        app = apps[0]
        app_name = str(app.get("name", "Workspace App"))
        dashboard_name = f"{app_name} Live"
        if not has_instantiation:
            oracle.append(instantiate_call(backend_id, app_name, dashboard_name))
        success.setdefault("required_dashboard_name_contains", app_name)
        required_widgets = success.setdefault("required_widgets", [])
        existing = {(item.get("origin"), item.get("widget_id")) for item in required_widgets}
        for tab_id, tab in (app.get("tabs") or {}).items():
            for item in tab.get("layout", []):
                widget_id = str(item.get("i", ""))
                if not widget_id or widget_id == "navigation_bar":
                    continue
                key = (backend_name, widget_id)
                if key not in existing:
                    required_widgets.append(
                        {
                            "origin": backend_name,
                            "widget_id": widget_id,
                            "tab_id": str(tab_id),
                            "min_count": 1,
                        }
                    )
                    existing.add(key)
        return

    if widgets and not apps and not has_live_widget:
        widget_id = next(iter(widgets))
        oracle.extend(
            [
                {"tool": "list_available_widgets", "args": {"origin": backend_name}},
                {
                    "tool": "get_widget_schema",
                    "args": {"origin": backend_name, "widget_id": widget_id},
                },
                {
                    "tool": "create_widget",
                    "args": {"origin": backend_name, "widget_id": widget_id},
                },
            ]
        )
        success.setdefault("required_widgets", []).append(
            {"origin": backend_name, "widget_id": widget_id, "min_count": 1}
        )
        success.setdefault("trace_checks", {})["must_call_schema_before_create"] = True


def _expected_backend_delta(task: dict) -> int:
    for call in task.get("oracle_tool_calls", []):
        if call.get("tool") == "manage_backends":
            return 1 if call.get("args", {}).get("operation") == "add" else 0
    return 0


def _human_duration(milliseconds: Any) -> str:
    try:
        value = int(milliseconds)
    except (TypeError, ValueError):
        return str(milliseconds)
    if value % 60000 == 0:
        return f"{value // 60000} minute"
    if value % 1000 == 0:
        return f"{value // 1000} second"
    return f"{value} millisecond"


def _widget_outcome(widget_id: str, definition: dict, *, detailed: bool) -> str:
    name = str(definition.get("name") or widget_id.replace("_", " ").title())
    widget_type = str(definition.get("type", "table"))
    endpoint = str(definition.get("endpoint", ""))
    purpose = str(definition.get("description", "")).rstrip(".")
    # Catalog descriptions often open with the widget's own name; gluing that
    # after the name again reads machine-generated and trips the identity
    # audit, so the redundant prefix is dropped.
    if purpose.lower().startswith(name.lower()):
        purpose = purpose[len(name):].lstrip(" ,-")
        if purpose.lower().startswith("for "):
            purpose = purpose[4:]
    text = f"{name} (`{widget_id}`, {widget_type})"
    if endpoint:
        text += f" using `{endpoint}`"
    if purpose:
        text += f" for {purpose[0].lower() + purpose[1:]}"
    features: list[str] = []
    for param in definition.get("params") or []:
        if not isinstance(param, dict):
            continue
        label = str(param.get("label") or param.get("paramName"))
        param_type = str(param.get("type", "text"))
        param_name = str(param.get("paramName", ""))
        feature = f"{label} (`{param_name}`, {param_type})"
        if param.get("optionsEndpoint"):
            feature += f" from `{param['optionsEndpoint']}`"
        if param_type == "form":
            inputs = [
                str(item.get("label") or item.get("paramName"))
                for item in param.get("inputParams") or []
                if isinstance(item, dict)
            ]
            if inputs:
                feature += f" with {', '.join(inputs)}"
        features.append(feature)
    if features:
        text += "; user controls: " + ", ".join(features)
    if definition.get("staleTime") is not None:
        text += f"; cache for {_human_duration(definition['staleTime'])}s"
    if definition.get("refetchInterval") is not None:
        text += f"; refresh every {_human_duration(definition['refetchInterval'])}s"
    if definition.get("wsEndpoint"):
        text += f"; stream updates from `{definition['wsEndpoint']}`"
    if "runButton" in definition:
        text += "; run on demand" if definition["runButton"] else "; update without a run button"
    if definition.get("raw"):
        text += "; consume the raw backend payload"
    advanced_data = definition.get("data") or {}
    if not isinstance(advanced_data, dict):
        advanced_data = {}
    for key, label in (
        ("defaultSymbol", "default symbol"),
        ("updateFrequency", "update frequency"),
        ("wsRowIdColumn", "stream row id"),
        ("dataKey", "data key"),
    ):
        if key in advanced_data:
            text += f"; {label} `{advanced_data[key]}`"
    columns = _columns_for_definition(definition)
    if columns:
        column_summaries = []
        for column in columns:
            summary = str(column.get("field"))
            if detailed:
                extras = [
                    str(column[key])
                    for key in ("cellDataType", "formatterFn", "renderFn")
                    if column.get(key)
                ]
                if extras:
                    summary += f" ({', '.join(extras)})"
            column_summaries.append(summary)
        text += "; columns: " + ", ".join(column_summaries)
    return text


def _columns_for_definition(definition: dict) -> list[dict]:
    data = definition.get("data")
    table = data.get("table") if isinstance(data, dict) else None
    columns = table.get("columnsDefs") if isinstance(table, dict) else None
    return [column for column in (columns or []) if isinstance(column, dict)]


def _app_outcome(app: dict) -> str:
    name = str(app.get("name", "Workspace App"))
    parts = [f"app {name!r}"]
    tabs = app.get("tabs") or {}
    if tabs:
        tab_parts = []
        for tab_id, tab in tabs.items():
            widgets = [
                str(item.get("i"))
                for item in tab.get("layout", [])
                if item.get("i") != "navigation_bar"
            ]
            tab_parts.append(f"{tab.get('name', tab_id)} ({', '.join(widgets)})")
        parts.append("tabs " + "; ".join(tab_parts))
    groups = app.get("groups") or []
    if groups:
        parts.append(
            "shared interactions "
            + ", ".join(
                f"{group.get('name')} across {', '.join(group.get('widgetIds') or [])}"
                + (f" via `{group['paramName']}`" if group.get("paramName") else "")
                for group in groups
            )
        )
    prompts = app.get("prompts") or []
    if prompts:
        parts.append(f"{len(prompts)} starter prompt(s)")
    return " with ".join(parts)


_BUSINESS_CONTEXT = {
    "Vol Desk Data": ("a volatility analyst", "volatility and derivatives"),
    "Chain TVL Data": ("a digital-assets analyst", "chain activity and liquidity"),
    "Rates Watch Data": ("a rates strategist", "rates and Treasury markets"),
    "Vendor SLA Data": ("a vendor-operations manager", "vendor service levels"),
    "Earnings Prep Data": ("an equity-research analyst", "earnings and estimates"),
    "Execution Desk Data": ("an execution analyst", "orders and venue quality"),
    "Surveillance Data": ("a surveillance analyst", "cases and compliance alerts"),
    "Healthcare Research Data": (
        "a healthcare-research analyst",
        "clinical catalysts and pipelines",
    ),
}


def _business_description(description: object) -> str:
    """Remove implementation dialects from an authored data-subject description."""

    text = str(description).strip().rstrip(".")
    replacements = (
        (r"(?i)highcharts rendering of ", "comparisons of "),
        (r"(?i)vega-lite bar spec of ", "distribution of "),
        (r"(?i)plotly bar chart of ", "comparison of "),
        (r"(?i)plotly curve of ", "term structure for "),
        (r"(?i)plotly pipeline distribution by ", "pipeline distribution by "),
        (r"(?i)plotly slippage distribution by ", "slippage distribution by "),
        (r"(?i)plotly treasury yield curve snapshot", "the Treasury yield curve"),
        (r"(?i)plotly eps beat/miss history", "EPS beat and miss history"),
        (r"(?i)tradingview advanced charting for ", "market history for "),
        (r"(?i)tradingview chart for ", "market history for "),
        (r"(?i)streaming order blotter over websocket", "live order activity"),
        (r"(?i)omni search over ", "question answering over "),
        (r"(?i)monthly venue scorecard pdf", "monthly venue scorecard document"),
        (r"(?i)symbol cell syncs every tab", "ticker selection stays linked across analysis"),
        (r"(?i)symbol cell syncs revisions", "ticker selection links to revisions"),
        (r"(?i)\bchart(?:ing)?\b", "analysis"),
        (r"(?i)\bmarkdown\b", "written"),
        (r"(?i)\btable\b", "dataset"),
    )
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    if not text:
        return "the requested business data"
    first_word = text.split(maxsplit=1)[0]
    return text if len(first_word) > 1 and first_word[:2].isupper() else text[0].lower() + text[1:]


def _human_field(field: str) -> str:
    words = field.replace("_", " ")
    replacements = {
        "id": "ID",
        "eps": "EPS",
        "sla": "SLA",
        "tvl": "TVL",
        "usd": "USD",
        "pct": "percentage",
        "px": "price",
        "qty": "quantity",
        "b": "billions",
        "ms": "milliseconds",
        "1d": "one-day",
        "bn": "billions",
    }
    return " ".join(replacements.get(word.casefold(), word) for word in words.split())


def _unique_strings(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = value.casefold()
        if value and normalized not in seen:
            result.append(value)
            seen.add(normalized)
    return result


def _medium_anchors(task: dict, widgets: dict[str, dict]) -> list[str]:
    candidates = [
        str(param.get("paramName"))
        for definition in widgets.values()
        for param in flatten_params(definition, recurse=True)
        if param.get("paramName")
    ]
    candidates.extend(
        str(column.get("field"))
        for definition in widgets.values()
        for column in _columns_for_definition(definition)
        if column.get("field")
    )
    candidates = _unique_strings(candidates)
    if not candidates:
        backend_name, _, _ = _backend_identity(task)
        candidates = [backend_name]
    return candidates[:2]


def _hard_business_terms(task: dict, widgets: dict[str, dict]) -> list[str]:
    terms = [
        str(fragment)
        for required in task.get("success", {}).get("required_generated_widgets", [])
        for fragment in required.get("data_contains", [])
    ]
    terms.extend(
        str(required.get("contains"))
        for required in task.get("success", {}).get("business_names", [])
        if required.get("contains")
    )
    param_kinds = {
        _capability_param_kind(param)
        for definition in widgets.values()
        for param in flatten_params(definition, recurse=True)
    }
    if "ticker" in param_kinds:
        terms.append("ticker")
    if "date" in param_kinds:
        terms.append("date")
    return _unique_strings(terms)


def _brief_requirements(task: dict, widgets: dict[str, dict]) -> list[str]:
    purposes = _unique_strings(
        [_business_description(definition.get("description")) for definition in widgets.values()]
    )
    pieces = [f"The workspace must cover {purpose}." for purpose in purposes]
    fields = _unique_strings(
        [
            _human_field(str(column.get("field")))
            for definition in widgets.values()
            for column in _columns_for_definition(definition)
            if column.get("field")
        ]
    )
    if fields:
        pieces.append("Analysts need to inspect " + ", ".join(fields) + ".")
    capabilities = task.get("success", {}).get("required_capabilities", [])
    kinds = {str(capability.get("widget_kind")) for capability in capabilities}
    param_kinds = {
        str(kind)
        for capability in capabilities
        for kind in capability.get("required_param_kinds", [])
    }
    if "ticker" in param_kinds:
        pieces.append("An analyst can filter the analysis by ticker.")
    if "date" in param_kinds:
        pieces.append("An analyst can choose the relevant business date.")
    if "number" in param_kinds:
        pieces.append("An analyst can adjust the relevant numeric scope.")
    if "boolean" in param_kinds:
        pieces.append("An analyst can toggle the relevant screening constraint.")
    if "form" in param_kinds or "form" in kinds:
        pieces.append("The user can enter the required details and submit the workflow.")
    if "server-side-grid" in kinds:
        pieces.append(
            "Large result sets must stay responsive while analysts filter and page through them."
        )
    if task.get("success", {}).get("capability_connections"):
        pieces.append("A selection in one part of the analysis stays linked to related results.")
    if task.get("success", {}).get("app_structure", {}).get("required"):
        pieces.append("Leave the complete working workspace open for review.")
    return pieces


def _render_prompt_contract(task: dict, *, family: str, level: str) -> None:
    """Render the structural openness ladder and its identifier allowlist."""

    widgets, _ = _authored_payload(task)
    specification_level = str(task["specification_level"])
    if specification_level == "explicit":
        task["business_terms"] = []
        task["prompt"] = _explicit_prompt(task, family=family, level=level)
        return

    backend_name, _, _ = _backend_identity(task)
    role, subject = _BUSINESS_CONTEXT.get(
        backend_name, ("an investment analyst", "the requested financial dataset")
    )
    requirements = _brief_requirements(task, widgets)
    task_id = str(task["id"])
    if specification_level == "partially-specified":
        anchors = _medium_anchors(task, widgets)
        task["business_terms"] = anchors
        anchor_text = " and ".join(f"`{anchor}`" for anchor in anchors)
        body = " ".join(requirements)
        task["prompt"] = phrased(
            task_id,
            [
                f"Build a working Workspace experience for {role} covering {subject}. "
                f"{body} Keep these source-contract anchors: {anchor_text}. "
                "Choose the rest of the architecture and avoid unrelated changes.",
                f"Create a usable {subject} workflow for {role}. {body} "
                f"The source contract must retain {anchor_text}; decide the remaining "
                "implementation and preserve unrelated workspace state.",
                f"Deliver an analyst-ready Workspace solution for {subject}. {body} "
                f"Use {anchor_text} as the only fixed contract anchors, and make the "
                "other implementation choices yourself without collateral changes.",
            ],
        )
        return

    terms = _hard_business_terms(task, widgets)
    task["business_terms"] = terms
    body = " ".join(requirements)
    note = ""
    if task.get("success", {}).get("required_generated_widgets"):
        rendered_terms = ", ".join(repr(term) for term in terms)
        note = (
            " Add a short completion note that naturally includes the desk-required "
            f"terms {rendered_terms}."
        )
    repair = (
        " Preserve all working content while correcting the requested workflow."
        if family == "extend"
        else ""
    )
    task["prompt"] = phrased(
        task_id,
        [
            f"{role.capitalize()} needs a decision-ready Workspace for {subject}. {body}"
            f"{repair}{note} Choose an effective architecture and avoid unrelated changes.",
            f"Build {role} a dependable {subject} workspace. {body}{repair}{note} "
            "Decide how best to organize the experience and preserve unrelated work.",
            f"The desk needs a production-ready {subject} workflow for {role}. {body}"
            f"{repair}{note} Use your judgment on the architecture and leave other work intact.",
        ],
    )


def _explicit_prompt(task: dict, *, family: str, level: str) -> str:
    widgets, apps = _authored_payload(task)
    backend_name, url, _ = _backend_identity(task)
    detailed = level in {"r0", "r1", "r2"}
    widget_text = "; ".join(
        _widget_outcome(widget_id, definition, detailed=detailed)
        for widget_id, definition in widgets.items()
    )
    app_text = _app_outcome(apps[0]) if apps else ""
    if apps and level in {"r0", "r1"}:
        leads = [
            "Publish the requested app and open it in Workspace to verify it works.",
            "Build the specified app, publish it, and leave a working instance open.",
            "Implement the requested app and confirm it by opening it in Workspace.",
        ]
    elif level == "r0":
        leads = [
            "Connect the backend and make its first widget usable on the current dashboard.",
            "Register the backend and place the specified widget on the active dashboard.",
            "Make the requested backend widget available and working in the current view.",
        ]
    else:
        leads = [
            "Publish the backend app and open it in Workspace to verify it works.",
            "Build the specified backend app and leave a working instance open.",
            "Implement the requested app and confirm it in an open Workspace dashboard.",
        ]
    lead = phrased(str(task["id"]), leads)
    pieces = [lead, f"Use {backend_name!r} at {url}."]
    focus = {
        "types": "Choose the native widget type that fits the content.",
        "settings": "Implement the requested runtime and refresh behavior.",
        "params": "Make the user controls functional.",
        "forms": "Make the submission workflow functional.",
        "aggrid": "Make the data grid behavior and columns usable.",
        "charts": "Choose a working chart representation for the data.",
        "advanced": "Implement the live or advanced interaction correctly.",
        "grouping": "Make the cross-widget interaction work.",
        "apps": "Treat the app layout and navigation as the product outcome.",
        "extend": "Repair the existing backend without regressing working content.",
        "e2e": "Validate the complete workflow in the opened app.",
    }.get(family)
    if focus:
        pieces.append(focus)
    if widget_text:
        pieces.append("The experience needs " + widget_text + ".")
    if app_text:
        pieces.append("Organize it as " + app_text + ".")

    for required in task.get("success", {}).get("required_widgets", []):
        if required.get("data_args"):
            pieces.append(
                f"In the opened app, configure `{required['widget_id']}` with "
                f"{json.dumps(required['data_args'], sort_keys=True)}."
            )
    for call in task.get("oracle_tool_calls", []):
        if call.get("tool") == "add_generative_widget":
            args = call.get("args", {})
            generated_required: dict = next(
                (
                    item
                    for item in task.get("success", {}).get("required_generated_widgets", [])
                    if item.get("widget_type") == args.get("widget_type")
                    and (
                        not item.get("name_contains")
                        or str(item["name_contains"]).lower() in str(args.get("name", "")).lower()
                    )
                ),
                {},
            )
            facts = ", ".join(
                repr(str(fragment))
                for fragment in generated_required.get("data_contains", [])
            )
            pieces.append(
                phrased(
                    str(task.get("id", "completion-note")),
                    [
                        f"Add a short {args.get('widget_type', 'note')} named "
                        f"{args.get('name')!r} that covers these facts in your own "
                        f"words: {facts}.",
                        f"Document completion with a concise "
                        f"{args.get('widget_type', 'note')} called {args.get('name')!r}; "
                        f"make sure it mentions {facts}.",
                        f"Leave a brief {args.get('widget_type', 'note')} titled "
                        f"{args.get('name')!r}. Phrase it naturally while including "
                        f"the facts {facts}.",
                    ],
                )
            )
    pieces.append(
        "Choose the appropriate Workspace tools, validate the result, and avoid unrelated changes."
    )
    return " ".join(piece.strip() for piece in pieces if piece.strip()).replace("..", ".")


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
    definition: dict[str, Any] = {
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
    definition: dict[str, Any] = {
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
        "paramName": name,
        "type": "text",
        "label": label,
        "value": value,
        "options": [{"label": lab, "value": val} for lab, val in options],
    }


def endpoint_param(name: str, label: str, value, options_endpoint: str) -> dict:
    return {
        "paramName": name,
        "type": "endpoint",
        "label": label,
        "value": value,
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
    # grade) it when a task explicitly opts in — proxy round 1 (v3): every
    # words-brief r1 failed solely on "missing allowCustomization (expected
    # True)" that no prompt ever stated.
    app: dict[str, Any] = {
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
# Requirements rendering (r1+): every graded value is STATED, structured and
# unambiguous, but the finished JSON is NOT given — the model derives the
# definition. Exact-JSON briefs (widget_brief_text) are the r0 form.
# Calibration round 6: exact-JSON everywhere flattened r1–r3 into transcription.
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


def param_requirement(param: dict) -> str:
    name = param["paramName"]
    kind = param.get("type", "text")
    if kind == "form":
        inner = "; ".join(param_requirement(item) for item in param.get("inputParams", []))
        return (
            f"{name} — a form submitting {param.get('method', 'POST')} to "
            f"{param.get('endpoint')} with inputs [{inner}] (that bracket is "
            "the complete list of the form's inputParams)"
        )
    bits = [f"{name} — {_PARAM_KIND.get(kind, kind)} (type {kind})"]
    if "label" in param:
        bits.append(f'labeled "{param["label"]}"')
    if "optionsEndpoint" in param:
        bits.append(f"options fetched from {param['optionsEndpoint']}")
    if "optionsParams" in param:
        bits.append(f"passing optionsParams {_compact_json(param['optionsParams'])}")
    if "options" in param:
        pairs = ", ".join(
            f'"{opt["label"]}"={json.dumps(opt["value"])}' for opt in param["options"]
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
        bits.append(f'described "{param["description"]}"')
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
    text = f'{column["field"]} → header "{column["headerName"]}" ({", ".join(detail)})'
    if "renderFnParams" in column:
        text += f" with renderFnParams {_compact_json(column['renderFnParams'])}"
    return text


def widget_requirements_text(
    widget_id: str,
    definition: dict,
    omit_params: set[str] | None = None,
) -> str:
    """Structured-requirements brief: states every graded field, gives no JSON.

    ``omit_params`` lets a composed (r2/r4) brief factor a shared param out of the
    per-widget list — state it once with shared_param_note instead.
    """

    omit_params = omit_params or set()
    parts = [
        f'`{widget_id}`: name "{definition["name"]}"',
        f'description "{definition["description"]}"',
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
        param
        for param in (definition.get("params") or [])
        if isinstance(param, dict) and param.get("paramName") not in omit_params
    ]
    if params:
        has_form = any(p.get("type") == "form" for p in params)
        rendered_params = []
        for p in params:
            text = param_requirement(p)
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
    raw_data = definition.get("data")
    data = raw_data if isinstance(raw_data, dict) else {}
    if "dataKey" in data:
        parts.append(f"rows are read from the response key {json.dumps(data['dataKey'])}")
    for key in ("defaultSymbol", "updateFrequency", "wsRowIdColumn"):
        if key in data:
            parts.append(f"data.{key} {json.dumps(data[key])}")
    return ", ".join(parts)


def shared_param_note(param: dict, widget_ids: list[str]) -> str:
    """State a shared param once for a composed payload (r2/r4 factoring)."""

    return (
        f"All of {', '.join(f'`{wid}`' for wid in widget_ids)} take the same shared "
        f"param: {param_requirement(param)}."
    )


def stamp_consistency(widgets: dict, key: str = "staleTime", value=900000) -> str:
    """Apply one config value to EVERY def in the payload; return the
    convention clause to state ONCE in the prompt.

    The r3 composition dimension for cells with no shared param to group on
    (proxy r2 review): the convention is stated once and applies to all
    widgets, so the model must fan it out — graded on the focus def's full
    checks (and on any anchor extended via anchor_with_expect).
    """

    for definition in widgets.values():
        definition[key] = value
    return f"every widget this backend serves carries {key} {json.dumps(value)}"


def anchor_with_expect(backend_name: str, widget_id: str, definition: dict, *keys: str) -> dict:
    """A sibling anchor extended with named expect keys (e.g. the consistency
    convention key), so a stated convention grades on more than one widget."""

    check = widget_def_anchor_checks(backend_name, widget_id, definition)
    for key in keys:
        if key in definition:
            check["expect"][key] = definition[key]
    return check


# ---------------------------------------------------------------------------
# r1 data derivation: columns are DERIVED from served sample rows under stated
# conventions (the weak fairness invariant: graded values are deterministically
# derivable from stated data + stated rules, like a real analyst brief).
# ---------------------------------------------------------------------------

# r2 policy wording (proxy full-r6): config stated as a desk policy the model
# CONVERTS, not a value it copies. The rule is stated in the prompt alongside
# the policy, so the graded value stays deterministically derivable.
CONFIG_RULES = (
    'Time-based config converts to milliseconds: "cache results for N '
    'minutes" means staleTime N*60000; "auto-refresh every N seconds" '
    "means refetchInterval N*1000."
)


def cache_policy(minutes: int) -> tuple[dict, str]:
    """(config dict, policy clause) for a cache policy stated in minutes."""

    return (
        {"staleTime": minutes * 60000},
        f"it caches results for {minutes} minutes",
    )


DERIVATION_RULES = (
    "Derive the table columns from the served rows using the workspace "
    "conventions: every field in the rows becomes a column, in row order; "
    "headerName is the field name with underscores as spaces, Title Case; "
    "cellDataType is number for numeric values, dateString for ISO dates "
    "(YYYY-MM-DD), boolean for true/false, text otherwise; fields ending in "
    "_pct additionally carry formatterFn percent."
)

# r1 rules carry a worked example (round 8: r1 is one derived aspect with the
# example adjacent; r2 composes the same rules without the example).
DERIVATION_EXAMPLE = (
    'Example: a field {"filled_pct": 0.42} becomes {"field": "filled_pct", '
    '"headerName": "Filled Pct", "cellDataType": "number", '
    '"formatterFn": "percent"}.'
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

    Used for r1 data-derivation tasks: the prompt shows the rows + the rules;
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
    definition: dict[str, Any] = {
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
# r3 diagnosis: the defect is NOT named in the prompt. The seed carries the
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
    assert flags, "r3 diagnosis seed produced no validation flags"
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
        f"workspace validation failed: {count} {noun} in the backend's served payload need fixing"
    ]


def app_requirements_text(app: dict) -> str:
    """Structured app brief: placements and groups in words, no layout JSON."""

    parts = [f'app "{app["name"]}"']
    if app.get("description"):
        parts.append(f'description "{app["description"]}"')
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
        parts.append(f'tab `{tab_id}` named "{tab["name"]}" places: {placements}')
    for group in app.get("groups", []) or []:
        bits = [f'group "{group["name"]}" (type {group.get("type")})']
        if "paramName" in group:
            bits.append(f"syncing param {group['paramName']}")
        if group.get("widgetIds"):
            bits.append(f"across {_compact_json(group['widgetIds'])}")
        if "defaultValue" in group:
            bits.append(f"default {json.dumps(group['defaultValue'])}")
        parts.append(" ".join(bits))
    prompts = app.get("prompts")
    if prompts:
        parts.append("suggested prompts: " + "; ".join(f'"{p}"' for p in prompts))
    return ", ".join(parts)


def widget_brief_text(widget_id: str, definition: dict) -> str:
    """Render a widget-definition brief.

    Scalars read as prose; nested structures (params, columnsDefs, data extras)
    are given as EXACT JSON so the task measures building the definition, not
    decoding pseudo-JSON prose. Calibration round 4 change: mini copied nested
    JSON perfectly at r3 but omitted columnsDefs wholesale when they only
    appeared as prose fragments.
    """

    parts = [
        f'`{widget_id}`: name "{definition["name"]}"',
        f'description "{definition["description"]}"',
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
            f"columnsDefs (exact JSON, under data.table.columnsDefs): {_compact_json(columns)}"
        )
    raw_data = definition.get("data")
    data = raw_data if isinstance(raw_data, dict) else {}
    for key in ("dataKey", "defaultSymbol", "updateFrequency", "wsRowIdColumn"):
        if key in data:
            parts.append(f"data.{key} {json.dumps(data[key])}")
    return ", ".join(parts)


# ---------------------------------------------------------------------------
# Check derivation — grader blocks derived from the same definitions.
# ---------------------------------------------------------------------------


def widget_def_checks(backend_name: str, widget_id: str, definition: dict) -> dict:
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
    raw_data = definition.get("data")
    data = raw_data if isinstance(raw_data, dict) else {}
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


def add_backend_call(name: str, url: str, widgets: dict, apps: list | None = None) -> dict:
    args = {"operation": "add", "name": name, "url": url, "widgets_json": widgets}
    if apps is not None:
        args["apps_json"] = apps
    return {"tool": "manage_backends", "args": args}


def refresh_call(backend_id: str, widgets: dict | None = None, apps: list | None = None) -> dict:
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
            "operation": "instantiate",
            "backend_id": backend_id,
            "app_name": app_name,
            "dashboard_name": dashboard_name,
            "activate": True,
        },
    }


def seeded_custom(
    name: str,
    url: str,
    widgets: dict,
    apps: list | None = None,
    backend_id: str = "backend_001",
) -> dict:
    spec: dict = {
        "name": name,
        "url": url,
        "backend_id": backend_id,
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

STARK_ENTERPRISE = json.loads(
    (REPO / "src/workspace_bench/workspace/data/stark_enterprise.json").read_text(
        encoding="utf-8"
    )
)

DESKS: dict[str, dict] = {
    "stark": {
        "backend": "Bench Stark Enterprise",
        "url": "http://localhost:7809",
        "workflow": "enterprise-portfolio-review",
        "subdomain": "enterprise-asset-management",
        "widgets": STARK_ENTERPRISE["widgets"],
    },
    "vol": {
        "backend": "Vol Desk Data",
        "url": "http://localhost:7801",
        "workflow": "risk-review",
        "subdomain": "volatility",
        "widgets": {
            "vix_history": table_def(
                "VIX History",
                "Daily CBOE VIX closes with returns.",
                "/vix-history",
                columns=[
                    ("date", "Date", "dateString"),
                    ("close", "Close", "number"),
                    (
                        "return_pct",
                        "Return %",
                        "number",
                        {"formatterFn": "percent", "renderFn": "greenRed"},
                    ),
                ],
                params=[number_param("window", "Window", 30, minimum=5, maximum=365)],
            ),
            "vix_term_structure": simple_def(
                "chart",
                "VIX Term Structure",
                "Plotly curve of VIX futures by expiry.",
                "/vix-term-structure",
                grid=(20, 9),
                raw=True,
            ),
            "vix_advanced": simple_def(
                "advanced_charting",
                "VIX Advanced Chart",
                "TradingView advanced charting for VIX futures.",
                "/udf",
                grid=(20, 20),
                data={"defaultSymbol": "VIX", "updateFrequency": 60000},
            ),
            "vol_commentary": simple_def(
                "markdown",
                "Vol Commentary",
                "Morning volatility commentary.",
                "/vol-commentary",
                grid=(12, 8),
                params=[
                    dropdown_param(
                        "desk", "Desk", "index", [("Index", "index"), ("Single Stock", "single")]
                    )
                ],
            ),
            "vol_regime_metric": simple_def(
                "metric",
                "Vol Regime",
                "Current volatility regime score.",
                "/vol-regime",
                grid=(6, 4),
            ),
            "vol_screener": simple_def(
                "table",
                "Vol Screener",
                "Screen names by implied-vol criteria.",
                "/vol-screener",
                grid=(24, 10),
                params=[
                    {"paramName": "ticker", "type": "ticker", "label": "Ticker"},
                    date_param("as_of", "As of"),
                    boolean_param("only_liquid", "Liquid only", True),
                ],
            ),
        },
    },
    "tvl": {
        "backend": "Chain TVL Data",
        "url": "http://localhost:7802",
        "workflow": "portfolio-morning-review",
        "subdomain": "crypto",
        "widgets": {
            "chains_table": table_def(
                "Top Chains by TVL",
                "Current TVL of all chains from the desk aggregator.",
                "/chains-table",
                columns=[
                    ("name", "Chain", "text"),
                    ("tvl_usd", "TVL ($)", "number", {"formatterFn": "int"}),
                    (
                        "change_1d",
                        "1d Change",
                        "number",
                        {"formatterFn": "percent", "renderFn": "greenRed"},
                    ),
                ],
            ),
            "chains_chart": simple_def(
                "chart",
                "TVL by Chain",
                "Plotly bar chart of chain TVL.",
                "/chains-chart",
                grid=(20, 9),
                raw=True,
            ),
            "chains_highchart": simple_def(
                "chart-highcharts",
                "TVL by Chain (Highcharts)",
                "Highcharts rendering of chain TVL.",
                "/chains-highchart",
                grid=(20, 9),
            ),
            "chains_heatmap_html": simple_def(
                "html",
                "Chain Heatmap",
                "Raw HTML heatmap of chain flows.",
                "/chains-heatmap",
                grid=(20, 10),
            ),
            "protocol_details": simple_def(
                "markdown",
                "Protocol Details",
                "Markdown details for one protocol.",
                "/protocol-details",
                grid=(12, 8),
                params=[
                    text_param("protocol", "Protocol", "uniswap", "Protocol slug to describe.")
                ],
            ),
            "gas_metric": simple_def(
                "metric",
                "Gas Now",
                "Current gas price snapshot.",
                "/gas-now",
                grid=(5, 4),
            ),
        },
    },
    "rates": {
        "backend": "Rates Watch Data",
        "url": "http://localhost:7803",
        "workflow": "macro-rates-review",
        "subdomain": "macro",
        "widgets": {
            "yield_curve": simple_def(
                "chart",
                "Yield Curve",
                "Plotly treasury yield curve snapshot.",
                "/yield-curve",
                grid=(20, 9),
                raw=True,
            ),
            "auction_calendar": table_def(
                "Auction Calendar",
                "Upcoming treasury auctions.",
                "/auction-calendar",
                columns=[
                    ("date", "Date", "dateString"),
                    ("security", "Security", "text"),
                    ("size_bn", "Size ($B)", "number"),
                ],
            ),
            "rates_commentary": simple_def(
                "markdown",
                "Rates Commentary",
                "Desk commentary on the rates day.",
                "/rates-commentary",
                grid=(12, 8),
                params=[endpoint_param("series", "Series", "DGS10", "/series-options")],
            ),
            "curve_spread_metric": simple_def(
                "metric",
                "2s10s Spread",
                "Current 2s10s spread in bps.",
                "/curve-spread",
                grid=(6, 4),
            ),
            "curve_monitor_iframe": simple_def(
                "iframe",
                "Curve Monitor App",
                "Embedded standalone curve monitor application.",
                "http://localhost:5173",
                grid=(24, 16),
            ),
        },
    },
    "sla": {
        "backend": "Vendor SLA Data",
        "url": "http://localhost:7804",
        "workflow": "vendor-sla-monitoring",
        "subdomain": "operations",
        "widgets": {
            "vendor_sla_table": table_def(
                "Vendor SLA Status",
                "Vendor SLA state with breach flags.",
                "/vendor-sla",
                columns=[
                    ("vendor", "Vendor", "text"),
                    ("status", "Status", "text", {"renderFn": "titleCase"}),
                    ("latency_ms", "Latency (ms)", "number"),
                    ("breach", "Breach", "boolean"),
                ],
                params=[
                    dropdown_param(
                        "status",
                        "Status",
                        "Open",
                        [("Open", "Open"), ("Escalated", "Escalated"), ("Resolved", "Resolved")],
                    )
                ],
            ),
            "breach_metric": simple_def(
                "metric",
                "Open Breaches",
                "Count of open SLA breaches.",
                "/breach-count",
                grid=(6, 4),
            ),
            "sla_newsfeed": simple_def(
                "newsfeed",
                "Vendor Notices",
                "Vendor incident notices feed.",
                "/vendor-notices",
                grid=(12, 10),
            ),
            "sla_runbook": simple_def(
                "markdown",
                "SLA Runbook",
                "Runbook for SLA escalations.",
                "/sla-runbook",
                grid=(12, 8),
            ),
            "vendor_intake_form": simple_def(
                "table",
                "Vendor Intake Form",
                "Submit a new vendor record into the SLA register.",
                "/vendor-intake",
                grid=(20, 10),
                params=[
                    {
                        "paramName": "intake",
                        "type": "form",
                        "label": "New Vendor",
                        "endpoint": "/vendor-intake-submit",
                        "method": "POST",
                        "inputParams": [
                            {"paramName": "vendor", "type": "text", "label": "Vendor"},
                            {"paramName": "tier", "type": "number", "label": "Tier"},
                            {"paramName": "submit", "type": "button", "label": "Add Vendor"},
                        ],
                    }
                ],
            ),
        },
    },
    "earnings": {
        "backend": "Earnings Prep Data",
        "url": "http://localhost:7805",
        "workflow": "earnings-prep",
        "subdomain": "equity-research",
        "widgets": {
            "estimate_revisions": table_def(
                "Estimate Revisions",
                "Street estimate revisions by quarter.",
                "/estimate-revisions",
                columns=[
                    ("quarter", "Quarter", "text"),
                    ("eps_estimate", "EPS Est", "number"),
                    ("revenue_estimate_b", "Revenue Est ($B)", "number"),
                ],
                params=[endpoint_param("symbol", "Symbol", "AAPL", "/symbols")],
            ),
            "earnings_chart": simple_def(
                "chart",
                "EPS History",
                "Plotly EPS beat/miss history.",
                "/eps-history",
                grid=(20, 9),
                raw=True,
                params=[endpoint_param("symbol", "Symbol", "AAPL", "/symbols")],
            ),
            "earnings_note": simple_def(
                "markdown",
                "Earnings Preview",
                "Preview note for the earnings call.",
                "/earnings-preview",
                grid=(12, 8),
                params=[endpoint_param("symbol", "Symbol", "AAPL", "/symbols")],
            ),
            "surprise_metric": simple_def(
                "metric",
                "Avg Surprise",
                "Average EPS surprise last 4 quarters.",
                "/avg-surprise",
                grid=(6, 4),
            ),
            "estimates_ssrm": simple_def(
                "table_ssrm",
                "Estimates Explorer (SSRM)",
                "Server-side sorted and filtered estimates dataset.",
                "/estimates-ssrm",
                grid=(24, 16),
            ),
            "earnings_calls_video": simple_def(
                "youtube",
                "Earnings Call Replays",
                "Replay library of earnings calls.",
                "/call-videos",
                grid=(20, 12),
                params=[endpoint_param("video", "Video", "q1-call", "/call-video-options")],
            ),
            "kpi_tabs_table": simple_def(
                "table",
                "KPI Tabs",
                "KPI table with static and dynamic tab views.",
                "/kpi-tabs",
                grid=(24, 10),
                params=[
                    {
                        "paramName": "view",
                        "type": "tabs",
                        "label": "View",
                        "value": "growth",
                        "options": [
                            {"label": "Growth", "value": "growth"},
                            {"label": "Margins", "value": "margins"},
                        ],
                    }
                ],
            ),
        },
    },
    "execution": {
        "backend": "Execution Desk Data",
        "url": "http://localhost:7806",
        "workflow": "execution-exception-review",
        "subdomain": "execution",
        "widgets": {
            "open_orders": table_def(
                "Open Orders",
                "Live open orders blotter.",
                "/open-orders",
                columns=[
                    ("order_id", "Order", "text"),
                    ("symbol", "Symbol", "text"),
                    ("qty", "Qty", "number", {"formatterFn": "int"}),
                    ("status", "Status", "text", {"renderFn": "titleCase"}),
                ],
            ),
            "slippage_chart": simple_def(
                "chart",
                "Slippage by Venue",
                "Plotly slippage distribution by venue.",
                "/slippage-by-venue",
                grid=(20, 9),
                raw=True,
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
                    "table": {
                        "columnsDefs": [
                            {"field": "order_id", "headerName": "Order", "cellDataType": "text"},
                            {
                                "field": "px",
                                "headerName": "Price",
                                "cellDataType": "number",
                                "renderFn": "showCellChange",
                                "renderFnParams": {"colorValueKey": "px_change"},
                            },
                        ]
                    },
                },
            },
            "exception_metric": simple_def(
                "metric",
                "Exceptions",
                "Open execution exceptions.",
                "/exception-count",
                grid=(5, 4),
            ),
            "venue_pdf": simple_def(
                "pdf",
                "Venue Scorecard",
                "Monthly venue scorecard PDF.",
                "/venue-scorecard",
                grid=(16, 14),
            ),
        },
    },
    "compliance": {
        "backend": "Surveillance Data",
        "url": "http://localhost:7807",
        "workflow": "compliance-surveillance",
        "subdomain": "compliance",
        "widgets": {
            "alert_queue": table_def(
                "Alert Queue",
                "Open surveillance alerts.",
                "/alert-queue",
                columns=[
                    ("alert_id", "Alert", "text"),
                    ("desk", "Desk", "text"),
                    ("severity", "Severity", "text", {"renderFn": "titleCase"}),
                    ("age_days", "Age (d)", "number", {"formatterFn": "int"}),
                ],
                params=[
                    dropdown_param(
                        "severity",
                        "Severity",
                        "high",
                        [("High", "high"), ("Medium", "medium"), ("Low", "low")],
                    )
                ],
            ),
            "case_notes": simple_def(
                "markdown",
                "Case Notes",
                "Notes for one surveillance case.",
                "/case-notes",
                grid=(12, 8),
                params=[text_param("case_id", "Case", "C-1042", "Case identifier.")],
            ),
            "alert_metric": simple_def(
                "metric",
                "Open Alerts",
                "Open alert count.",
                "/alert-count",
                grid=(5, 4),
            ),
            "policy_pdf": simple_def(
                "pdf",
                "Policy Digest",
                "Latest surveillance policy digest.",
                "/policy-digest",
                grid=(16, 14),
            ),
            "case_qa_omni": simple_def(
                "omni",
                "Case Q&A",
                "Ask questions over the surveillance case corpus.",
                "/case-qa",
                grid=(20, 9),
                params=[
                    {
                        "paramName": "prompt",
                        "type": "text",
                        "label": "Prompt",
                        "description": "Question to run over the case corpus.",
                        "show": False,
                    }
                ],
            ),
            "evidence_files": simple_def(
                "multi_file_viewer",
                "Evidence Files",
                "Browse case evidence documents.",
                "/evidence-files",
                grid=(20, 14),
                params=[
                    {
                        "paramName": "file",
                        "type": "endpoint",
                        "label": "File",
                        "optionsEndpoint": "/evidence-file-options",
                        "roles": ["fileSelector"],
                        "multiSelect": True,
                        "value": [],
                    }
                ],
            ),
        },
    },
    "healthcare": {
        "backend": "Healthcare Research Data",
        "url": "http://localhost:7808",
        "workflow": "healthcare-catalyst-review",
        "subdomain": "healthcare",
        "widgets": {
            "trial_catalysts": table_def(
                "Trial Catalysts",
                "Upcoming clinical trial readouts.",
                "/trial-catalysts",
                columns=[
                    ("ticker", "Ticker", "text"),
                    ("phase", "Phase", "text"),
                    ("readout_date", "Readout", "dateString"),
                ],
                params=[endpoint_param("ticker", "Ticker", "PFE", "/tickers")],
            ),
            "pipeline_chart": simple_def(
                "chart",
                "Pipeline by Phase",
                "Plotly pipeline distribution by phase.",
                "/pipeline-by-phase",
                grid=(20, 9),
                raw=True,
            ),
            "pipeline_vegalite": simple_def(
                "chart-vegalite",
                "Pipeline Mix (Vega-Lite)",
                "Vega-Lite bar spec of pipeline phase mix.",
                "/pipeline-vegalite",
                grid=(20, 9),
            ),
            "fda_newsfeed": simple_def(
                "newsfeed",
                "FDA Notices",
                "FDA decision and notice feed.",
                "/fda-notices",
                grid=(12, 10),
            ),
            "catalyst_metric": simple_def(
                "metric",
                "Catalysts 30d",
                "Catalysts in the next 30 days.",
                "/catalyst-count",
                grid=(6, 4),
            ),
        },
    },
}

DESK_KEYS = tuple(DESKS)


def desk(key: str) -> dict:
    return DESKS[key]


def desk_widget(key: str, widget_id: str) -> dict:
    definition = json.loads(json.dumps(DESKS[key]["widgets"][widget_id]))
    if key != "stark":
        return definition
    # The fixture stores response samples under ``data`` and the production
    # widget contract under ``schema_data``. Build tasks author widgets.json,
    # so emit the latter and never mistake sample rows for widget metadata.
    schema_data = definition.pop("schema_data", None)
    widget_type = str(definition.get("type", "table"))
    if isinstance(schema_data, dict):
        definition["data"] = schema_data
    elif widget_type == "metric":
        definition["data"] = {"valueField": "value"}
    elif widget_type == "chart":
        definition["data"] = {
            "categoryField": "date",
            "series": [{"field": "value"}],
        }
    elif isinstance(definition.get("data"), list):
        rows = definition["data"]
        fields = list(rows[0]) if rows and isinstance(rows[0], dict) else ["value"]
        definition["data"] = {
            "table": {
                "columnsDefs": [
                    {"field": field, "headerName": _human_field(str(field))}
                    for field in fields
                ]
            }
        }
    return definition


# ---------------------------------------------------------------------------
# Novelty, lattice, quotas
# ---------------------------------------------------------------------------


task_check_types = CheckTypePolicy(
    success_checks={
        "required_tabs": "missing_tab",
        "required_generated_widgets": "missing_generated_widget",
        "required_layouts": "layout_mismatch",
        "required_tool_calls": "missing_tool_call",
        "required_tool_results": "missing_tool_result",
        "required_resource_reads": "missing_resource_read",
        "required_widget_defs": "widget_def",
        "required_app_defs": "app_def",
        "required_capabilities": "capability",
        "capability_connections": "capability_connection",
    },
    widget_mode="collection",
    within_grid_default=False,
    max_invalid_tool_calls_default=None,
)


def task_backends(task: dict) -> set[str]:
    backends = {
        ref.get("name")
        for ref in task.get("fixtures", {}).get("backends", [])
        if isinstance(ref, dict)
    }
    for spec in task.get("initial_state", {}).get("custom_backends", []) or []:
        backends.add(f"custom:{spec.get('name')}")
    for call in task.get("oracle_tool_calls", []):
        if call.get("tool") == "manage_backends" and call.get("args", {}).get("operation") == "add":
            if "widgets_json" in call.get("args", {}):
                backends.add(f"custom:{call['args'].get('name')}")
    backends.discard(None)
    return cast(set[str], backends)


def _build_artifact_parts(task: dict) -> list[str]:
    success = task.get("success", {})
    parts: list[str] = []
    widget_defs = [
        f"{req['backend_name']}/{req['widget_id']}"
        for req in success.get("required_widget_defs", [])
    ]
    if widget_defs:
        parts.append("widgetdefs:" + ",".join(sorted(widget_defs)))
    capabilities = [
        f"{req['name']}:{req.get('widget_kind', 'any')}:{','.join(req.get('must_cover_fields', []))}"
        for req in success.get("required_capabilities", [])
    ]
    if capabilities:
        parts.append("capabilities:" + ",".join(sorted(capabilities)))
    app_defs = [
        f"{req['backend_name']}/{req.get('template_id') or req.get('name_contains')}"
        for req in success.get("required_app_defs", [])
    ]
    if app_defs:
        parts.append("appdefs:" + ",".join(sorted(app_defs)))
    return parts


artifact_discriminator = ArtifactDiscriminator(leading_parts=_build_artifact_parts)
_NOVELTY = NoveltyPolicy(
    check_types=task_check_types,
    task_backends=task_backends,
    artifact_discriminator=artifact_discriminator,
    exercise_label="building exercise",
)
novelty_fingerprint = _NOVELTY.fingerprint
add_novelty = _NOVELTY.add_description


def assert_lattice(matrix: dict[str, dict[str, int]]) -> None:
    expected = set(LADDER_FAMILIES) | {CAPSTONE_FAMILY, DEBUG_FAMILY}
    assert set(matrix) == expected, f"expected families {sorted(expected)}, got {sorted(matrix)}"
    for family in LADDER_FAMILIES:
        for level in RUNGS:
            count = matrix[family].get(level, 0)
            assert count == 4, f"{family}/{level} expected 4, got {count}"
    capstone = matrix[CAPSTONE_FAMILY]
    assert capstone.get("r4", 0) == E2E_COUNT and set(capstone) == {"r4"}, (
        f"{CAPSTONE_FAMILY} must be exactly {E2E_COUNT} tasks at r4, got {capstone}"
    )
    debug = matrix[DEBUG_FAMILY]
    assert debug.get(DEBUG_RUNG, 0) == DEBUG_COUNT and set(debug) == {DEBUG_RUNG}, (
        f"{DEBUG_FAMILY} must be exactly {DEBUG_COUNT} long repair tasks, got {debug}"
    )
