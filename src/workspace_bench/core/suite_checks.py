"""Release-gate checks for the bundled task suites.

The generators certify a suite at generation time; the functions here re-verify
the release-report subset from the shipped task JSON so that
``workspace-bench validate`` and ``workspace-bench report`` hold the same gates
without rerunning generation. The build-suite constants are imported by
``scripts/generators/generate_build_apps_suite.py`` and
``scripts/generators/build_apps_suite`` so
there is one source of truth for caps and ownership.

Profiles apply only to the bundled suites. Private ``--task-dir`` suites are
validated for loadability, metadata, oracle pass, and no-op failure, but are
never held to the bundled suites' coverage quotas.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Iterable

from workspace_bench.core.models import JsonDict, RunResult, Task
from workspace_bench.core.mutation_checks import grader_mutation_failures
from workspace_bench.core.prompt_openness import task_prompt_openness_issues
from workspace_bench.workspace.tool_surface import WORKSPACE_TOOL_NAMES
from workspace_bench.workspace.widget_params import flatten_params

USAGE_SUITE = "enterprise-apps-usage"
BUILD_SUITE = "build-openbb-apps"

# build-openbb-apps ladder constants.
#
# Per-task graded-check caps per structural specification level: strict pass ~= q^N,
# so uncontrolled
# check mass (N) would drive the level curve instead of per-check difficulty
# (q). t1 > t2 is intentional: t1 CONTAINS t0 (full widget) plus the app
# wrapper, while t2 is one composed artifact.
# Caps bound each level without rewarding a smaller schema-only rubric.
BUILD_SPECIFICATION_CHECK_CAPS = {
    "explicit": 24,
    "partially-specified": 36,
    "open-brief": 36,
}
BUILD_SPECIFICATION_LEVEL_BANDS = {
    "explicit": 60,
    "partially-specified": 92,
    "open-brief": 84,
}


def _load_measured_difficulty() -> tuple[dict[str, int], dict[str, str]]:
    path = Path(__file__).with_name("measured_difficulty.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    bands = payload.get("bands")
    overrides = payload.get("overrides")
    if (
        payload.get("schema_version") != "workspace-bench-measured-difficulty/v1"
        or not isinstance(bands, dict)
        or set(bands) != {"easy", "medium", "hard"}
        or not all(isinstance(value, int) and value >= 0 for value in bands.values())
        or not isinstance(overrides, dict)
        or not all(
            isinstance(task_ref, str) and difficulty in {"easy", "medium", "hard"}
            for task_ref, difficulty in overrides.items()
        )
    ):
        raise ValueError(f"invalid measured difficulty table: {path}")
    return dict(bands), dict(overrides)


BUILD_DIFFICULTY_BANDS, BUILD_MEASURED_DIFFICULTY_OVERRIDES = _load_measured_difficulty()
BUILD_DEBUG_CHECK_CAP = 42
# Widget-type / param-type ownership per family: every owned key must appear
# in that family's authored payloads.
BUILD_TYPE_OWNERSHIP = {
    "types": {
        "markdown",
        "metric",
        "pdf",
        "html",
        "iframe",
        "youtube",
        "newsfeed",
        "multi_file_viewer",
    },
    "aggrid": {"table", "table_ssrm"},
    "charts": {"chart", "chart-highcharts", "chart-vegalite"},
    "advanced": {"advanced_charting", "live_grid", "omni"},
}
BUILD_PARAM_OWNERSHIP = {
    "params": {"text", "date", "ticker", "number", "boolean", "endpoint", "tabs"},
    "forms": {"form", "button"},
}
CORE_FAMILIES = {
    "apps",
    "backends",
    "create",
    "delegate",
    "delete",
    "inspect",
    "layout",
    "navigate",
    "note",
    "params",
    "prompts",
    "read",
    "resources",
    "skills",
    "update",
}
BUILD_LADDER_FAMILIES = {
    "advanced",
    "aggrid",
    "apps",
    "charts",
    "extend",
    "forms",
    "grouping",
    "params",
    "settings",
    "types",
}


def release_checks_for_suite(
    suite: str | None,
    tasks: list[Task],
    oracle_results: list[RunResult],
) -> dict[str, bool]:
    """Return the release checks for a bundled suite; {} for private suites."""

    if suite == USAGE_SUITE:
        return core_release_checks(tasks, oracle_results)
    if suite == BUILD_SUITE:
        return build_release_checks(tasks, oracle_results)
    return {}


def core_release_checks(tasks: list[Task], oracle_results: list[RunResult]) -> dict[str, bool]:
    total = len(tasks)
    categories = Counter(task.category for task in tasks)
    difficulties = Counter(task.difficulty for task in tasks)
    backends = Counter(backend for task in tasks for backend in _task_backend_slugs(task))
    widget_pairs = {
        (required.origin, required.widget_id)
        for task in tasks
        for required in task.success.required_widgets
        if required.min_count > 0
    }
    checks = _core_check_type_counts(tasks)
    fingerprints = [_task_fingerprint(task) for task in tasks]
    return {
        **_universal_release_checks(tasks, max_duplicate_prompts=2, max_prompt_words=350),
        **_family_count_checks(
            tasks,
            expected={family: 20 for family in CORE_FAMILIES},
        ),
        "grader_mutation_sensitive": _mutation_suite_passes(tasks, oracle_results),
        "runtime_all_backend_tasks": all(
            task.success.runtime is not None for task in tasks if task.family == "backends"
        ),
        "task_count_at_least_300": total >= 300,
        "fingerprint_unique": len(set(fingerprints)) == total,
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
        "quota_grader_check_types": bool(checks) and all(count >= 10 for count in checks.values()),
    }


def build_release_checks(
    tasks: list[Task],
    oracle_results: list[RunResult],
) -> dict[str, bool]:
    total = len(tasks)
    difficulties = Counter(task.difficulty for task in tasks)
    specification_levels = Counter(task.specification_level for task in tasks)
    fingerprints = [_task_fingerprint(task) for task in tasks]
    widget_types: Counter = Counter()
    param_types: Counter = Counter()
    type_coverage: dict[str, set[str]] = {}
    param_coverage: dict[str, set[str]] = {}
    ops: Counter = Counter()
    widget_def_tasks = sum(1 for task in tasks if task.success.required_widget_defs)
    app_def_tasks = sum(1 for task in tasks if task.success.required_app_defs)
    capability_tasks = sum(1 for task in tasks if task.success.required_capabilities)
    app_structure_tasks = sum(1 for task in tasks if task.success.app_structure.required)

    for task in tasks:
        family = _task_family(task)
        for call in task.oracle_tool_calls:
            if call.name != "manage_backends":
                continue
            operation = call.args.get("operation")
            if operation == "add" and "widgets_json" in call.args:
                ops["add_custom"] += 1
            if operation == "refresh" and ("widgets_json" in call.args or "apps_json" in call.args):
                ops["refresh_payload"] += 1
            if "apps_json" in call.args:
                ops["apps_payload"] += 1
        for definition in _authored_definitions(task):
            widget_type = str(definition.get("type", "table"))
            widget_types[widget_type] += 1
            if family:
                type_coverage.setdefault(family, set()).add(widget_type)
            for param in flatten_params(definition, recurse=True):
                for param_type in _param_type_names(param):
                    param_types[param_type] += 1
                    if family:
                        param_coverage.setdefault(family, set()).add(param_type)

    caps_ok = all(
        result.grade.checks_total - result.grade.runtime_checks_total
        <= (
            BUILD_DEBUG_CHECK_CAP
            if task.family == "debug"
            else BUILD_SPECIFICATION_CHECK_CAPS.get(task.specification_level, 0)
        )
        for task, result in zip(tasks, oracle_results)
    )
    expected_family_counts = {family: 20 for family in BUILD_LADDER_FAMILIES}
    expected_family_counts["e2e"] = 12
    expected_family_counts["debug"] = 24
    checks = {
        **_universal_release_checks(tasks, max_duplicate_prompts=0, max_prompt_words=180),
        **_family_count_checks(tasks, expected=expected_family_counts),
        "grader_mutation_sensitive": _mutation_suite_passes(tasks, oracle_results),
        "prompt_specification_lint_236": total == 236
        and all(not task_prompt_openness_issues(task) for task in tasks),
        "open_prompts_use_capability_grading": all(
            task.specification_level == "explicit"
            or (
                task.success.required_capabilities
                and not task.success.required_widget_defs
                and not task.success.required_app_defs
                and not task.success.required_tabs
                and not task.success.required_layouts
            )
            for task in tasks
        ),
        "task_count_is_236": total == 236,
        "full_tool_surface_available": all(
            task.allowed_tools == WORKSPACE_TOOL_NAMES for task in tasks
        ),
        "functional_workspace_outcome": all(
            (task.success.required_widgets or task.success.required_capabilities)
            and (
                not (task.success.required_app_defs or task.success.app_structure.required)
                or task.success.required_dashboard_name_contains
                or task.success.business_names
                or task.success.required_capabilities
            )
            for task in tasks
        ),
        "fingerprint_unique": len(set(fingerprints)) == total,
        "quota_difficulty_bands": all(
            difficulties[band] == count for band, count in BUILD_DIFFICULTY_BANDS.items()
        ),
        "quota_specification_level_bands": all(
            specification_levels[level] == count
            for level, count in BUILD_SPECIFICATION_LEVEL_BANDS.items()
        ),
        "quota_widget_types_at_least_16": len(widget_types) >= 16,
        "quota_param_types_at_least_9": len(param_types) >= 9,
        "quota_custom_adds_at_least_120": ops["add_custom"] >= 120,
        "quota_payload_refreshes_at_least_16": ops["refresh_payload"] >= 16,
        "quota_apps_payloads_at_least_100": ops["apps_payload"] >= 100,
        "quota_exact_widget_def_tasks_at_least_40": widget_def_tasks >= 40,
        "quota_exact_app_def_tasks_at_least_20": app_def_tasks >= 20,
        "quota_capability_tasks_at_least_140": capability_tasks >= 140,
        "quota_app_structure_tasks_at_least_70": app_structure_tasks >= 70,
        "runtime_all_behavioral_widget_tasks": all(
            task.success.runtime is not None
            for task in tasks
            if task.success.required_widget_defs or task.success.required_capabilities
        ),
        "capability_contracts_non_empty": all(
            capability.must_cover_fields
            or capability.required_param_kinds
            or capability.required_config
            for task in tasks
            for capability in task.success.required_capabilities
        ),
        "form_capabilities_have_submission_contract": all(
            capability.widget_kind != "form"
            or (
                "form" in capability.required_param_kinds
                and task.success.runtime is not None
                and any(
                    dataset.name in capability.datasets
                    and dataset.form_endpoint is not None
                    for dataset in task.success.runtime.datasets
                )
            )
            for task in tasks
            for capability in task.success.required_capabilities
        ),
        "runtime_all_e2e_tasks": all(
            task.success.runtime is not None for task in tasks if task.family == "e2e"
        ),
        "completion_notes_have_live_evidence": all(
            task.success.runtime is not None
            and task.success.required_capabilities
            and task.success.app_structure.required
            for task in tasks
            if task.success.required_generated_widgets
        ),
        "completion_notes_have_semantic_deployment_facts": all(
            _completion_notes_have_deployment_facts(task)
            for task in tasks
            if task.success.required_generated_widgets
        ),
        "per_specification_level_graded_check_caps": caps_ok,
    }
    for family, owned in sorted(BUILD_TYPE_OWNERSHIP.items()):
        observed = type_coverage.get(family, set())
        checks[f"ownership_{family}_widget_types"] = not (owned - observed)
    for family, owned in sorted(BUILD_PARAM_OWNERSHIP.items()):
        observed = param_coverage.get(family, set())
        checks[f"ownership_{family}_param_types"] = not (owned - observed)
    return checks


def _task_fingerprint(task: Task) -> str:
    payload = {
        "prompt": task.prompt,
        "initial_state": task.initial_state,
        "allowed_tools": list(task.allowed_tools),
        "oracle": [{"tool": call.name, "args": call.args} for call in task.oracle_tool_calls],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _mutation_suite_passes(tasks: list[Task], oracle_results: list[RunResult]) -> bool:
    return len(tasks) == len(oracle_results) and all(
        not grader_mutation_failures(task, result) for task, result in zip(tasks, oracle_results)
    )


def _completion_notes_have_deployment_facts(task: Task) -> bool:
    expected = {required.backend_name.casefold() for required in task.success.required_app_defs}
    if task.success.required_dashboard_name_contains:
        expected.add(task.success.required_dashboard_name_contains.casefold())
    if not expected:
        return all(required.data_contains for required in task.success.required_generated_widgets)
    return all(
        expected.issubset({fragment.casefold() for fragment in required.data_contains})
        for required in task.success.required_generated_widgets
    )


def task_payload_digest(payloads: Iterable[JsonDict]) -> str:
    """Stable digest of a suite's authored task payloads."""

    canonical = [
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        for payload in sorted(
            payloads,
            key=lambda item: (str(item.get("family", "")), str(item.get("id", ""))),
        )
    ]
    return hashlib.sha256("\n".join(canonical).encode("utf-8")).hexdigest()


def _universal_release_checks(
    tasks: list[Task], *, max_duplicate_prompts: int, max_prompt_words: int
) -> dict[str, bool]:
    ids = [(task.family, task.id) for task in tasks]
    prompts = [task.prompt for task in tasks]
    generated_types = Counter(
        required.widget_type
        for task in tasks
        for required in task.success.required_generated_widgets
    )
    generated_total = sum(generated_types.values())
    expected_hashes = {
        task.suite.content_sha256 for task in tasks if task.suite and task.suite.content_sha256
    }
    observed_hash: str | None = None
    if tasks and all(task.source_path and task.source_path.exists() for task in tasks):
        payloads = [
            json.loads(task.source_path.read_text(encoding="utf-8"))
            for task in tasks
            if task.source_path
        ]
        observed_hash = task_payload_digest(payloads)
    return {
        "task_ids_unique": len(set(ids)) == len(ids),
        "prompt_duplicate_cap": len(prompts) - len(set(prompts)) <= max_duplicate_prompts,
        "prompt_template_hygiene": all(
            ".." not in task.prompt and len(task.prompt.split()) <= max_prompt_words
            for task in tasks
        ),
        "generated_widget_type_diversity": len(generated_types) >= 2,
        "generated_widget_type_max_share_80pct": bool(generated_total)
        and max(generated_types.values()) / generated_total <= 0.80,
        "path_family_consistent": all(
            task.source_path is None or task.source_path.parent.name == task.family
            for task in tasks
        ),
        "suite_content_hash_matches": (
            len(expected_hashes) == 1
            and observed_hash is not None
            and observed_hash in expected_hashes
        ),
    }


def _family_count_checks(
    tasks: list[Task],
    *,
    expected: dict[str, int],
) -> dict[str, bool]:
    observed = Counter(task.family for task in tasks)
    return {
        "exact_family_coverage": set(observed) == set(expected),
        "exact_per_family_counts": dict(observed) == expected,
    }


def _task_family(task: Task) -> str | None:
    return task.family


def _authored_definitions(task: Task) -> Iterable[JsonDict]:
    for call in task.oracle_tool_calls:
        if call.name != "manage_backends":
            continue
        for definition in (call.args.get("widgets_json") or {}).values():
            if isinstance(definition, dict):
                yield definition


def _param_type_names(param: JsonDict) -> list[str]:
    return [str(param.get("type", "text"))]


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
        "daloopa": "daloopa",
        "Bench Daloopa": "daloopa",
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
        if success.required_capabilities:
            counts["missing_capability"] += 1
            counts["capability_fields_uncovered"] += 1
        if success.capability_connections:
            counts["capability_unconnected"] += 1
        if success.business_names:
            counts["business_name_missing"] += 1
    return counts
