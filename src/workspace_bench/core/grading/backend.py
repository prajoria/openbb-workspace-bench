"""Capability, connection, backend-definition, and published-app grading."""

from __future__ import annotations

from collections import defaultdict
from typing import Protocol

from workspace_bench.core.grading.matching import phrase_matches, subset_matches
from workspace_bench.core.grading.state import declared_backend_widgets, lookup_path
from workspace_bench.core.models import DeploymentReceipt, JsonDict, RequiredCapability, Task
from workspace_bench.workspace.geometry import rects_overlap
from workspace_bench.workspace.widget_params import flatten_params


class CheckBuilder(Protocol):
    """Structural type accepted by cohesive grading sections."""

    def check(self, condition: bool, code: str, message: str) -> None: ...


def app_layout_items(app: JsonDict) -> list[tuple[str, JsonDict]]:
    items: list[tuple[str, JsonDict]] = []
    for tab_key, tab in (app.get("tabs") or {}).items():
        if not isinstance(tab, dict):
            continue
        for item in tab.get("layout", []) or []:
            if isinstance(item, dict):
                items.append((str(tab_key), item))
    return items


def find_custom_backend(snapshot: JsonDict, backend_name: str) -> JsonDict | None:
    for meta in (snapshot.get("custom_backends") or {}).values():
        if isinstance(meta, dict) and meta.get("name") == backend_name:
            return meta
    return None


def widget_kinds(definition: JsonDict) -> set[str]:
    widget_type = str(definition.get("type", "table"))
    kinds: set[str] = set()
    if widget_type == "form" or any(
        str(param.get("type")) in {"form", "button"}
        for param in flatten_params(definition, recurse=True)
    ):
        kinds.add("form")
    if widget_type in {"ssrm_table", "live_grid"}:
        kinds.add("server-side-grid")
    elif widget_type == "table":
        kinds.add("table-like")
    elif widget_type in {
        "chart",
        "chart-highcharts",
        "chart-vegalite",
        "advanced_charting",
    }:
        kinds.add("chart-like")
    elif widget_type == "metric":
        kinds.add("metric")
    elif widget_type == "multi_file_viewer":
        kinds.add("multi-file")
    elif widget_type in {"html", "iframe", "markdown", "newsfeed", "pdf", "youtube"}:
        kinds.add(widget_type)
    return kinds or {"any"}


def param_kind(param: JsonDict) -> str:
    name = str(param.get("paramName", "")).casefold()
    param_type = str(param.get("type", "text")).casefold()
    roles = {str(role).casefold() for role in param.get("roles", []) or []}
    if param_type == "ticker" or name in {"symbol", "ticker", "tickers"} or "ticker" in roles:
        return "ticker"
    if param_type == "date" or "date" in name:
        return "date"
    if param_type == "endpoint":
        return "endpoint"
    if param_type in {"number", "boolean", "tabs", "form", "button"}:
        return param_type
    return "text"


def definition_param_kinds(definition: JsonDict) -> set[str]:
    return {param_kind(param) for param in flatten_params(definition, recurse=True)}


def _instantiated_widget_keys(final_snapshot: JsonDict) -> set[tuple[str, str]]:
    dashboards = final_snapshot.get("dashboard_compositions") or {}
    keys: set[tuple[str, str]] = set()
    if isinstance(dashboards, dict):
        compositions = list(dashboards.values())
    else:
        compositions = [final_snapshot.get("dashboard_composition") or {}]
    for composition in compositions:
        if not isinstance(composition, dict):
            continue
        for widget in composition.get("widgets", []) or []:
            if isinstance(widget, dict) and not widget.get("generated"):
                keys.add((str(widget.get("origin", "")), str(widget.get("widget_id", ""))))
    return keys


def _runtime_valid_widget_datasets(
    receipt: DeploymentReceipt | None,
) -> dict[tuple[str, str], str]:
    if receipt is None:
        return {}
    return {
        (outcome.backend_name, outcome.widget_id): str(outcome.dataset_name)
        for outcome in receipt.widget_probes
        if outcome.passed and outcome.dataset_name is not None
    }


def _capability_candidates(
    capability: RequiredCapability,
    definitions: dict[tuple[str, str], JsonDict],
    instantiated: set[tuple[str, str]],
    runtime_valid: set[tuple[str, str]],
    task: Task,
) -> dict[tuple[str, str], JsonDict]:
    from workspace_bench.workspace.runtime import bind_dataset

    accepted: dict[tuple[str, str], JsonDict] = {}
    allowed_datasets = tuple(
        dataset
        for dataset in (task.success.runtime.datasets if task.success.runtime else ())
        if dataset.name in capability.datasets
    )
    for key, definition in definitions.items():
        if key not in instantiated or key not in runtime_valid:
            continue
        actual_kinds = widget_kinds(definition)
        if capability.widget_kind != "any" and capability.widget_kind not in actual_kinds:
            continue
        if bind_dataset(definition, key[1], allowed_datasets) is None:
            continue
        accepted[key] = definition
    return accepted


def grade_capabilities(
    builder: CheckBuilder,
    task: Task,
    final_snapshot: JsonDict,
    receipt: DeploymentReceipt | None,
) -> dict[str, set[tuple[str, str]]]:
    from workspace_bench.workspace.runtime import declared_fields

    definitions = declared_backend_widgets(final_snapshot)
    instantiated = _instantiated_widget_keys(final_snapshot)
    runtime_valid = set(_runtime_valid_widget_datasets(receipt))
    contributors: dict[str, set[tuple[str, str]]] = {}
    for capability in task.success.required_capabilities:
        candidates = _capability_candidates(
            capability, definitions, instantiated, runtime_valid, task
        )
        builder.check(
            bool(candidates),
            "missing_capability",
            (
                f"Capability {capability.name!r} needs an instantiated, runtime-valid "
                f"{capability.widget_kind} widget bound to {list(capability.datasets)}."
            ),
        )
        required_fields = set(capability.must_cover_fields)
        contributing = {
            key
            for key, definition in candidates.items()
            if not required_fields or declared_fields(definition) & required_fields
        }
        covered = (
            set().union(*(declared_fields(candidates[key]) for key in contributing))
            if contributing
            else set()
        )
        builder.check(
            required_fields.issubset(covered),
            "capability_fields_uncovered",
            (
                f"Capability {capability.name!r} leaves fields "
                f"{sorted(required_fields - covered)} uncovered by runtime-valid widgets."
            ),
        )
        contributors[capability.name] = contributing
        param_kinds = (
            set().union(*(definition_param_kinds(candidates[key]) for key in contributing))
            if contributing
            else set()
        )
        for required_kind in capability.required_param_kinds:
            builder.check(
                required_kind in param_kinds,
                "capability_param_missing",
                (
                    f"Capability {capability.name!r} covering widgets do not expose a "
                    f"{required_kind!r} parameter."
                ),
            )
        for path, expected in capability.required_config.items():
            matches = []
            for key in contributors[capability.name]:
                found, actual = lookup_path(candidates[key], path)
                matches.append(found and actual == expected)
            builder.check(
                any(matches),
                "capability_config_missing",
                (
                    f"Capability {capability.name!r} covering widgets do not provide "
                    f"required configuration {path}={expected!r}."
                ),
            )
    return contributors


def _shared_param_graph(
    final_snapshot: JsonDict,
    definitions: dict[tuple[str, str], JsonDict],
    required_param_kind: str,
) -> dict[tuple[str, str], set[tuple[str, str]]]:
    graph: dict[tuple[str, str], set[tuple[str, str]]] = defaultdict(set)
    for backend in (final_snapshot.get("custom_backends") or {}).values():
        if not isinstance(backend, dict):
            continue
        backend_name = str(backend.get("name", ""))
        for app in backend.get("apps_json", []) or []:
            if not isinstance(app, dict):
                continue
            for group in app.get("groups", []) or []:
                if not isinstance(group, dict) or group.get("type", "param") != "param":
                    continue
                param_name = str(group.get("paramName", ""))
                keys = [
                    (backend_name, str(widget_id))
                    for widget_id in group.get("widgetIds", []) or []
                ]
                eligible = [
                    key
                    for key in keys
                    if key in definitions
                    and any(
                        str(param.get("paramName", "")) == param_name
                        and param_kind(param) == required_param_kind
                        for param in flatten_params(definitions[key], recurse=True)
                    )
                ]
                for key in eligible:
                    graph.setdefault(key, set())
                for index, left in enumerate(eligible):
                    for right in eligible[index + 1 :]:
                        graph[left].add(right)
                        graph[right].add(left)
    return graph


def _sets_connected(
    graph: dict[tuple[str, str], set[tuple[str, str]]],
    sources: set[tuple[str, str]],
    targets: set[tuple[str, str]],
) -> bool:
    return any(
        target != source and target in graph.get(source, set())
        for source in sources
        for target in targets
    )


def grade_capability_connections(
    builder: CheckBuilder,
    task: Task,
    final_snapshot: JsonDict,
    contributors: dict[str, set[tuple[str, str]]],
) -> None:
    definitions = declared_backend_widgets(final_snapshot)
    for connection in task.success.capability_connections:
        graph = _shared_param_graph(final_snapshot, definitions, connection.param_kind)
        connected = _sets_connected(
            graph,
            contributors.get(connection.source, set()),
            contributors.get(connection.target, set()),
        )
        builder.check(
            connected,
            "capability_unconnected",
            (
                f"Capabilities {connection.source!r} and {connection.target!r} are not "
                f"connected through a shared {connection.param_kind!r} parameter graph."
            ),
        )


def grade_business_names(builder: CheckBuilder, task: Task, final_snapshot: JsonDict) -> None:
    composition = final_snapshot.get("dashboard_composition") or {}
    app_names: list[str] = []
    tab_names: list[str] = [
        str(tab.get("name", "")) for tab in composition.get("tabs", []) if isinstance(tab, dict)
    ]
    for backend in (final_snapshot.get("custom_backends") or {}).values():
        if not isinstance(backend, dict):
            continue
        for app in backend.get("apps_json", []) or []:
            if not isinstance(app, dict):
                continue
            app_names.append(str(app.get("name", "")))
            tab_names.extend(
                str(tab.get("name", ""))
                for tab in (app.get("tabs") or {}).values()
                if isinstance(tab, dict)
            )
    values = {
        "dashboard": [str(composition.get("name", ""))],
        "app": app_names,
        "tab": tab_names,
    }
    for requirement in task.success.business_names:
        builder.check(
            any(phrase_matches(value, requirement.contains) for value in values[requirement.scope]),
            "business_name_missing",
            (
                f"No {requirement.scope} name satisfies business requirement "
                f"{requirement.contains!r}."
            ),
        )


def grade_app_structure(builder: CheckBuilder, task: Task, final_snapshot: JsonDict) -> None:
    checks = task.success.app_structure
    apps: list[tuple[str, JsonDict, set[str]]] = []
    for backend in (final_snapshot.get("custom_backends") or {}).values():
        if not isinstance(backend, dict):
            continue
        widget_ids = set(backend.get("widgets_json") or {})
        for app in backend.get("apps_json", []) or []:
            if isinstance(app, dict):
                apps.append((str(app.get("name", "app")), app, widget_ids))
    if checks.required:
        builder.check(bool(apps), "missing_capability", "A published app is required.")
    for label, app, widget_ids in apps:
        items = app_layout_items(app)
        if checks.layout_refs_valid:
            dangling = sorted(
                str(item.get("i"))
                for _, item in items
                if str(item.get("i")) not in widget_ids
                and str(item.get("i")) != "navigation_bar"
            )
            builder.check(
                not dangling,
                "app_layout_ref_invalid",
                f"App {label!r} has dangling widget references: {dangling}.",
            )
        if checks.no_overlaps:
            overlaps: list[tuple[str, str, str]] = []
            by_tab: dict[str, list[JsonDict]] = defaultdict(list)
            for tab_id, item in items:
                by_tab[tab_id].append(item)
            for tab_id, tab_items in by_tab.items():
                for index, first in enumerate(tab_items):
                    for second in tab_items[index + 1 :]:
                        if rects_overlap(first, second):
                            overlaps.append((tab_id, str(first.get("i")), str(second.get("i"))))
            builder.check(
                not overlaps,
                "app_layout_overlap",
                f"App {label!r} has overlapping layout items: {overlaps}.",
            )


def grade_polish(builder: CheckBuilder, task: Task, final_snapshot: JsonDict) -> None:
    for check in task.success.polish:
        backend = find_custom_backend(final_snapshot, check.backend_name)
        definition = (
            (backend.get("widgets_json") or {}).get(check.widget_id)
            if backend is not None
            else None
        )
        found, actual = (
            lookup_path(definition, check.path)
            if isinstance(definition, dict)
            else (False, None)
        )
        builder.check(
            found and actual == check.expected,
            check.code,
            (
                f"Polish check {check.backend_name}/{check.widget_id} {check.path} expected "
                f"{check.expected!r}, found {actual!r}."
            ),
        )


def grade_backend_building(
    builder: CheckBuilder, task: Task, final_snapshot: JsonDict
) -> None:
    backend_names = {required.backend_name for required in task.success.required_widget_defs} | {
        required.backend_name for required in task.success.required_app_defs
    }
    for backend_name in sorted(backend_names):
        backend = find_custom_backend(final_snapshot, backend_name)
        if backend is not None:
            warnings = backend.get("warnings") or []
            builder.check(
                not warnings,
                "backend_validation_warnings",
                f"Custom backend {backend_name!r} has validation warnings: {warnings}.",
            )
    for required in task.success.required_widget_defs:
        backend = find_custom_backend(final_snapshot, required.backend_name)
        if backend is None:
            builder.check(
                False,
                "missing_custom_backend",
                (
                    f"Expected custom backend {required.backend_name!r} to be "
                    "registered (manage_backends operation='add' with widgets_json)."
                ),
            )
            continue
        definition = (backend.get("widgets_json") or {}).get(required.widget_id)
        builder.check(
            definition is not None,
            "missing_widget_def",
            (
                f"Expected widget definition {required.widget_id!r} on custom "
                f"backend {required.backend_name!r}."
            ),
        )
        if definition is None:
            continue
        for path, expected in required.expect.items():
            found, actual = lookup_path(definition, path)
            if found:
                message = (
                    f"Widget def {required.widget_id!r}: expected {path} == "
                    f"{expected!r}, found {actual!r}."
                )
            else:
                message = (
                    f"Widget def {required.widget_id!r}: missing {path} (expected {expected!r})."
                )
            builder.check(found and actual == expected, "widget_def_mismatch", message)
        params = flatten_params(definition, recurse=True)
        for spec in required.params_include:
            builder.check(
                any(subset_matches(spec, param) for param in params),
                "widget_def_mismatch",
                f"Widget def {required.widget_id!r}: no param matching {spec}.",
            )
        found_cols, columns = lookup_path(definition, "data.table.columnsDefs")
        column_entries = columns if found_cols and isinstance(columns, list) else []
        for spec in required.columns_include:
            builder.check(
                any(
                    isinstance(column, dict) and subset_matches(spec, column)
                    for column in column_entries
                ),
                "widget_def_mismatch",
                f"Widget def {required.widget_id!r}: no columnsDefs entry matching {spec}.",
            )

    for required_app in task.success.required_app_defs:
        backend = find_custom_backend(final_snapshot, required_app.backend_name)
        if backend is None:
            builder.check(
                False,
                "missing_custom_backend",
                (
                    f"Expected custom backend {required_app.backend_name!r} to be "
                    "registered (manage_backends operation='add' with widgets_json)."
                ),
            )
            continue
        label = required_app.template_id or required_app.name_contains
        app = None
        for candidate in backend.get("apps_json") or []:
            if not isinstance(candidate, dict):
                continue
            if (
                required_app.template_id
                and candidate.get("template_id") == required_app.template_id
            ):
                app = candidate
                break
            if (
                required_app.name_contains
                and required_app.name_contains.lower() in str(candidate.get("name", "")).lower()
            ):
                app = candidate
                break
        builder.check(
            app is not None,
            "missing_app_def",
            (
                f"Expected app {label!r} in the apps.json of custom backend "
                f"{required_app.backend_name!r}."
            ),
        )
        if app is None:
            continue
        for path, expected in required_app.expect.items():
            found, actual = lookup_path(app, path)
            if found:
                message = f"App {label!r}: expected {path} == {expected!r}, found {actual!r}."
            else:
                message = f"App {label!r}: missing {path} (expected {expected!r})."
            builder.check(found and actual == expected, "app_def_mismatch", message)
        tabs = app.get("tabs") or {}
        for tab_id in required_app.tabs_include:
            builder.check(
                tab_id in tabs,
                "app_def_mismatch",
                f"App {label!r}: expected tab {tab_id!r}, found {sorted(tabs)}.",
            )
        if required_app.tab_count is not None:
            builder.check(
                len(tabs) == required_app.tab_count,
                "app_def_mismatch",
                f"App {label!r}: expected {required_app.tab_count} tab(s), found {len(tabs)}.",
            )
        if required_app.prompts_min_count is not None:
            prompts = app.get("prompts") or []
            count = len(prompts) if isinstance(prompts, list) else 0
            builder.check(
                count >= required_app.prompts_min_count,
                "app_def_mismatch",
                (
                    f"App {label!r}: expected at least {required_app.prompts_min_count} "
                    f"prompt(s), found {count}."
                ),
            )
        items = app_layout_items(app)
        if required_app.layout_refs_valid:
            widget_ids = set(backend.get("widgets_json") or {})
            dangling = sorted(
                {
                    str(item.get("i"))
                    for _, item in items
                    if str(item.get("i")) not in widget_ids
                    and str(item.get("i")) != "navigation_bar"
                }
            )
            builder.check(
                not dangling,
                "app_layout_ref_invalid",
                (
                    f"App {label!r}: layout references widgets the backend does "
                    f"not serve: {dangling}."
                ),
            )
        if required_app.no_overlaps:
            by_tab: dict[str, list[JsonDict]] = {}
            for tab_key, item in items:
                by_tab.setdefault(tab_key, []).append(item)
            overlaps = []
            for tab_key, tab_items in by_tab.items():
                for index, first in enumerate(tab_items):
                    for second in tab_items[index + 1 :]:
                        if rects_overlap(first, second):
                            overlaps.append((tab_key, str(first.get("i")), str(second.get("i"))))
            builder.check(
                not overlaps,
                "app_layout_overlap",
                f"App {label!r}: overlapping layout items: {overlaps}.",
            )
        for placement in required_app.widgets_on_tab:
            tab_id = str(placement.get("tab_id"))
            widget_id = str(placement.get("widget_id"))
            present = any(
                tab_key == tab_id and str(item.get("i")) == widget_id for tab_key, item in items
            )
            builder.check(
                present,
                "app_def_mismatch",
                f"App {label!r}: expected widget {widget_id!r} on tab {tab_id!r}.",
            )
        groups = app.get("groups") or []
        for spec in required_app.groups_include:
            widget_ids_include = spec.get("widgetIds_include", [])
            base_spec = {key: value for key, value in spec.items() if key != "widgetIds_include"}
            matched = False
            for group in groups:
                if not isinstance(group, dict):
                    continue
                if not subset_matches(base_spec, group):
                    continue
                group_widgets = group.get("widgetIds") or []
                if all(wid in group_widgets for wid in widget_ids_include):
                    matched = True
                    break
            builder.check(
                matched,
                "app_def_mismatch",
                f"App {label!r}: no group matching {spec}.",
            )
