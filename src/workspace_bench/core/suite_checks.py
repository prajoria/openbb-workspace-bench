"""Release-gate checks for the bundled task suites.

The generators certify a suite at generation time; the functions here re-verify
the release-report subset from the shipped task JSON so that
``workspace-bench validate`` and ``workspace-bench report`` hold the same gates
without rerunning generation. The build-suite constants are imported by
``scripts/generate_build_apps_suite.py`` and ``scripts/build_apps_suite`` so
there is one source of truth for caps and ownership.

Profiles apply only to the bundled suites. Private ``--task-dir`` suites are
validated for loadability, metadata, oracle pass, and no-op failure, but are
never held to the bundled suites' coverage quotas.
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from workspace_bench.core.models import JsonDict, RunResult, Task

CORE_SUITE = "core"
BUILD_SUITE = "build-openbb-apps"

# build-openbb-apps ladder constants.
#
# Per-task graded-check caps per level: strict pass ~= q^N, so uncontrolled
# check mass (N) would drive the level curve instead of per-check difficulty
# (q). t1 > t2 is intentional: t1 CONTAINS t0 (full widget) plus the app
# wrapper, while t2 is one composed artifact.
BUILD_CHECK_CAPS = {"t0": 12, "t1": 20, "t2": 16, "t3": 26, "t4": 30}
BUILD_DIFFICULTY_BANDS = {"easy": 60, "medium": 80, "hard": 72}
# Widget-type / param-type ownership per family: every owned key must appear
# in that family's authored payloads.
BUILD_TYPE_OWNERSHIP = {
    "types": {"markdown", "metric", "pdf", "html", "iframe", "youtube",
              "newsfeed", "multi_file_viewer"},
    "aggrid": {"table", "ssrm_table"},
    "charts": {"chart", "chart-highcharts", "chart-vegalite"},
    "advanced": {"advanced_charting", "live_grid", "omni"},
}
BUILD_PARAM_OWNERSHIP = {
    "params": {"text", "date", "ticker", "number", "boolean", "endpoint", "tabs"},
    "forms": {"form", "button"},
}


def release_checks_for_suite(
    suite: str | None,
    tasks: list[Task],
    oracle_results: list[RunResult],
) -> dict[str, bool]:
    """Return the release checks for a bundled suite; {} for private suites."""

    if suite == CORE_SUITE:
        return core_release_checks(tasks)
    if suite == BUILD_SUITE:
        return build_release_checks(tasks, oracle_results)
    return {}


def core_release_checks(tasks: list[Task]) -> dict[str, bool]:
    total = len(tasks)
    categories = Counter(task.category for task in tasks)
    difficulties = Counter(task.difficulty for task in tasks)
    backends = Counter(
        backend for task in tasks for backend in _task_backend_slugs(task)
    )
    widget_pairs = {
        (required.origin, required.widget_id)
        for task in tasks
        for required in task.success.required_widgets
        if required.min_count > 0
    }
    checks = _core_check_type_counts(tasks)
    novelty = [task.novelty for task in tasks]
    return {
        "task_count_at_least_300": total >= 300,
        "fingerprint_unique": len(set(novelty)) == total and all(novelty),
        "quota_dashboard_construction": categories["dashboard"] >= total * 0.15,
        "quota_backend_equities": backends["equities"] >= total * 0.15,
        "quota_backend_macro": backends["macro"] >= total * 0.15,
        "quota_backend_portfolio": backends["portfolio"] >= total * 0.15,
        "quota_backend_stark_enterprise": backends["stark-enterprise"] >= total * 0.15,
        "quota_difficulty_bands": (
            abs(difficulties["easy"] - total * 0.30) <= total * 0.05
            and abs(difficulties["medium"] - total * 0.40) <= total * 0.05
            and abs(difficulties["hard"] - total * 0.30) <= total * 0.05
        ),
        "quota_required_widget_pairs": len(widget_pairs) >= 120,
        "quota_grader_check_types": bool(checks)
        and all(count >= 10 for count in checks.values()),
    }


def build_release_checks(
    tasks: list[Task],
    oracle_results: list[RunResult],
) -> dict[str, bool]:
    total = len(tasks)
    difficulties = Counter(task.difficulty for task in tasks)
    novelty = [task.novelty for task in tasks]
    widget_types: Counter = Counter()
    param_types: Counter = Counter()
    type_coverage: dict[str, set[str]] = {}
    param_coverage: dict[str, set[str]] = {}
    ops: Counter = Counter()
    widget_def_tasks = sum(1 for task in tasks if task.success.required_widget_defs)
    app_def_tasks = sum(1 for task in tasks if task.success.required_app_defs)

    for task in tasks:
        family = _task_family(task)
        for call in task.oracle_tool_calls:
            if call.name != "manage_backends":
                continue
            operation = call.args.get("operation")
            if operation == "add" and "widgets_json" in call.args:
                ops["add_custom"] += 1
            if operation == "refresh" and (
                "widgets_json" in call.args or "apps_json" in call.args
            ):
                ops["refresh_payload"] += 1
            if "apps_json" in call.args:
                ops["apps_payload"] += 1
        for definition in _authored_definitions(task):
            widget_type = str(definition.get("type", "table"))
            widget_types[widget_type] += 1
            if family:
                type_coverage.setdefault(family, set()).add(widget_type)
            for param in _flat_params(definition):
                for param_type in _param_type_names(param):
                    param_types[param_type] += 1
                    if family:
                        param_coverage.setdefault(family, set()).add(param_type)

    caps_ok = all(
        result.grade.checks_total <= BUILD_CHECK_CAPS.get(task.level, 0)
        for task, result in zip(tasks, oracle_results)
    )
    checks = {
        "task_count_is_212": total == 212,
        "fingerprint_unique": len(set(novelty)) == total and all(novelty),
        "quota_difficulty_bands": all(
            difficulties[band] == count
            for band, count in BUILD_DIFFICULTY_BANDS.items()
        ),
        "quota_widget_types_at_least_16": len(widget_types) >= 16,
        "quota_param_types_at_least_9": len(param_types) >= 9,
        "quota_custom_adds_at_least_120": ops["add_custom"] >= 120,
        "quota_payload_refreshes_at_least_16": ops["refresh_payload"] >= 16,
        "quota_apps_payloads_at_least_100": ops["apps_payload"] >= 100,
        "quota_widget_def_tasks_at_least_160": widget_def_tasks >= 160,
        "quota_app_def_tasks_at_least_100": app_def_tasks >= 100,
        "per_level_graded_check_caps": caps_ok,
    }
    for family, owned in sorted(BUILD_TYPE_OWNERSHIP.items()):
        observed = type_coverage.get(family, set())
        checks[f"ownership_{family}_widget_types"] = not (owned - observed)
    for family, owned in sorted(BUILD_PARAM_OWNERSHIP.items()):
        observed = param_coverage.get(family, set())
        checks[f"ownership_{family}_param_types"] = not (owned - observed)
    return checks


def _task_family(task: Task) -> str | None:
    for tag in task.tags:
        if tag.startswith("family-"):
            return tag[len("family-"):]
    return None


def _authored_definitions(task: Task) -> Iterable[JsonDict]:
    for call in task.oracle_tool_calls:
        if call.name != "manage_backends":
            continue
        for definition in (call.args.get("widgets_json") or {}).values():
            if isinstance(definition, dict):
                yield definition


def _flat_params(definition: JsonDict) -> list[JsonDict]:
    params = definition.get("params")
    flat: list[JsonDict] = []
    if not isinstance(params, list):
        return flat
    for entry in params:
        if isinstance(entry, list):
            flat.extend(item for item in entry if isinstance(item, dict))
        elif isinstance(entry, dict):
            flat.append(entry)
    return flat


def _param_type_names(param: JsonDict) -> list[str]:
    names = [str(param.get("type", "text"))]
    for inner in param.get("inputParams") or []:
        if isinstance(inner, dict):
            names.append(str(inner.get("type", "text")))
    return names


def _task_backend_slugs(task: Task) -> set[str]:
    backends = {_backend_slug(backend.name) for backend in task.fixtures}
    for call in task.oracle_tool_calls:
        if call.name == "manage_backends" and call.args.get("operation") == "add":
            name = call.args.get("name")
            if isinstance(name, str):
                backends.add(_backend_slug(name))
    return backends


def _backend_slug(name: str) -> str:
    return {
        "equities": "equities",
        "Bench Equities": "equities",
        "macro": "macro",
        "Bench Macro": "macro",
        "portfolio": "portfolio",
        "Bench Portfolio": "portfolio",
        "stark-enterprise": "stark-enterprise",
        "Bench Stark Enterprise": "stark-enterprise",
    }.get(name, name)


def _core_check_type_counts(tasks: list[Task]) -> Counter:
    counts: Counter = Counter()
    for task in tasks:
        success = task.success
        if success.required_dashboard_name_contains:
            counts["dashboard_name"] += 1
        if success.required_tabs:
            counts["missing_tab"] += 1
        for required in success.required_widgets:
            if required.min_count > 0:
                counts["missing_widget"] += 1
            if required.max_count is not None:
                counts["too_many_widgets"] += 1
        if success.required_generated_widgets:
            counts["missing_generated_widget"] += 1
        if success.required_layouts:
            counts["layout_mismatch"] += 1
        if success.required_tool_calls:
            counts["missing_tool_call"] += 1
        if success.required_tool_results:
            counts["missing_tool_result"] += 1
        if success.required_resource_reads:
            counts["missing_resource_read"] += 1
        if success.layout.within_grid:
            counts["layout_out_of_grid"] += 1
        if success.layout.no_overlaps:
            counts["layout_overlap"] += 1
        counts["too_many_invalid_calls"] += 1
        if success.trace.must_call_schema_before_create:
            counts["schema_not_called_before_create"] += 1
        if success.trace.forbid_invented_widget_ids:
            counts["unlisted_widget_id"] += 1
        if success.trace.max_repeated_snapshots is not None:
            counts["repeated_snapshots"] += 1
    return counts
