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

from workspace_bench.core.models import FINAL_ANSWER_TOOL, JsonDict, RunResult, Task
from workspace_bench.core.mutation_checks import grader_mutation_failures
from workspace_bench.core.prompt_openness import task_prompt_openness_issues
from workspace_bench.core.models import WORKSPACE_TOOL_NAMES
from workspace_bench.workspace.widget_params import flatten_params

USAGE_SUITE = "enterprise-apps-usage"
BUILD_SUITE = "build-openbb-apps"
SMOKE_SUITE = "smoke"
APPS_DEFAULT_SUITE = "enterprise-apps-default"

# Field profile for apps-default: identity, instruction, world, sealed eval.
APPS_DEFAULT_TASK_FIELDS = frozenset({"id", "prompt", "setup", "eval"})

# Field profile for the smoke ladder: identity, per-task workspace axes, and
# grading. Category is derived from the family by the loader and never
# written; fixtures/business_terms/specification_level may not appear; no
# field may carry an empty default the loader would infer anyway.
SMOKE_TASK_FIELDS = frozenset(
    {
        "id",
        "family",
        "difficulty",
        "prompt",
        "setup",
        "eval",
    }
)
SMOKE_LEVELS = ("level0", "level1", "level2", "level3")
SMOKE_BASELINE = "stark-onboard-a"
SMOKE_LEVEL_TURNS = {"level0": 1, "level1": 2, "level2": 2, "level3": 4}

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
# Job-shaped usage families: {family: (task count, levels present)}.
USAGE_FAMILIES = {
    "retrieve": (12, (0, 1, 2, 3, 4, 5)),
    "curate": (12, (0, 1, 2, 3, 4, 5)),
    "parameterize": (12, (0, 1, 2, 3, 4, 5)),
    "organize": (12, (0, 1, 2, 3, 4, 5)),
    "repair": (10, (1, 2, 3, 4, 5)),
    "platform": (10, (1, 2, 3, 4, 5)),
    "extend": (12, (0, 1, 2, 3, 4, 5)),
    "handoff": (10, (0, 1, 2, 3, 4)),
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
        return usage_release_checks(tasks, oracle_results)
    if suite == BUILD_SUITE:
        return build_release_checks(tasks, oracle_results)
    if suite == SMOKE_SUITE:
        return smoke_release_checks(tasks)
    if suite == APPS_DEFAULT_SUITE:
        return apps_default_release_checks(tasks)
    return {}


def apps_default_release_checks(tasks: list[Task]) -> dict[str, bool]:
    """Hold the paired-data-world design against the shipped task JSON."""

    payloads = [_authored_task_payload(task) for task in tasks]
    by_id = {task.id: task for task in tasks}
    x_tasks = [task for task in tasks if task.id.endswith("_x")]
    y_tasks = [task for task in tasks if task.id.endswith("_y")]

    def _world(task: Task) -> str:
        backends = task.workspace_backends or ()
        return backends[0] if backends else ""

    return {
        "task_count_138": len(tasks) == 138,
        "paired_data_worlds": (
            len(x_tasks) == 69
            and len(y_tasks) == 69
            and all(
                (twin := by_id.get(task.id[: -len("_x")] + "_y")) is not None
                and twin.prompt == task.prompt
                for task in x_tasks
            )
        ),
        "worlds_bound_to_ids": all(
            _world(task)
            == ("stark-enterprise-y" if task.id.endswith("_y") else "stark-enterprise-x")
            for task in tasks
        ),
        "judge_evaluation_all": all(
            task.success.required_answer_judgment for task in tasks
        ),
        # The reference trace holds only workspace interactions; the reply
        # lives in reference_answer and the oracle replay synthesizes its
        # submission (one extra turn beyond the trace, plus two of slack).
        "reference_answer_authored": all(
            task.reference_answer
            and all(
                call.name != FINAL_ANSWER_TOOL for call in task.oracle_tool_calls
            )
            for task in tasks
        ),
        "turn_budget_reference_plus_three": all(
            int(task.limits.get("max_turns", 0)) == len(task.oracle_tool_calls) + 3
            for task in tasks
        ),
        "task_fields_within_profile": bool(payloads)
        and all(
            payload is not None and set(payload) <= APPS_DEFAULT_TASK_FIELDS
            for payload in payloads
        ),
        "suite_content_hash_matches": _suite_content_hash_matches(tasks),
    }


def smoke_release_checks(tasks: list[Task]) -> dict[str, bool]:
    """Hold the smoke ladder field profile against the shipped task JSON."""

    payloads = [_authored_task_payload(task) for task in tasks]

    def _level_contract(task: Task) -> bool:
        if task.difficulty == "level0":
            surface_ok = len(task.allowed_tools) == 1
        else:
            surface_ok = set(task.allowed_tools) == set(WORKSPACE_TOOL_NAMES)
        if task.difficulty in ("level0", "level1"):
            baseline_ok = task.workspace_baseline == ""
        else:
            baseline_ok = task.workspace_baseline == SMOKE_BASELINE
        turns_ok = task.limits.get("max_turns") == SMOKE_LEVEL_TURNS.get(task.difficulty)
        return surface_ok and baseline_ok and turns_ok

    return {
        "difficulty_is_level_ladder": all(
            task.difficulty in SMOKE_LEVELS for task in tasks
        ),
        "level_contract_holds": all(_level_contract(task) for task in tasks),
        "one_task_per_family_per_level": (
            all(
                count == len(SMOKE_LEVELS)
                for count in Counter(task.family for task in tasks).values()
            )
            and len({(task.family, task.difficulty) for task in tasks}) == len(tasks)
        ),
        "explicit_workspace_axes": all(
            task.workspace_baseline is not None
            and task.workspace_backends is not None
            and task.workspace_skills is not None
            for task in tasks
        ),
        "task_fields_within_smoke_profile": bool(payloads)
        and all(
            payload is not None and set(payload) <= SMOKE_TASK_FIELDS
            for payload in payloads
        ),
        "no_redundant_default_fields": bool(payloads)
        and all(
            payload is not None
            and all(value not in ({}, []) for value in payload.values())
            for payload in payloads
        ),
        "suite_content_hash_matches": _suite_content_hash_matches(tasks),
    }


def _authored_task_payload(task: Task) -> JsonDict | None:
    """Return the task JSON exactly as authored on disk, or None."""

    if task.source_path is None:
        return None
    try:
        payload = json.loads(Path(task.source_path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def usage_release_checks(tasks: list[Task], oracle_results: list[RunResult]) -> dict[str, bool]:
    total = len(tasks)
    fingerprints = [_task_fingerprint(task) for task in tasks]
    origins: set[str] = set()
    for task in tasks:
        for call in task.oracle_tool_calls:
            origin = call.args.get("origin")
            if isinstance(origin, str):
                origins.add(origin)
        for required in task.success.required_widgets:
            origins.add(required.origin)
    ladder_ok = all(
        sum(
            1
            for task in tasks
            if task.family == family and task.difficulty == f"level{level}"
        )
        == 2
        for family, (_, levels) in USAGE_FAMILIES.items()
        for level in levels
    )
    budget_ok = all(
        task.limits.get("max_turns") == len(task.oracle_tool_calls) + 3
        for task in tasks
    )
    universal = _universal_release_checks(
        tasks, max_duplicate_prompts=1, max_prompt_words=200
    )
    # The reply channel replaced note-mailbox deliverables: with only a
    # handful of artifact tasks, the generated-widget-type share quotas
    # would force artificial variety.
    universal.pop("generated_widget_type_diversity", None)
    universal.pop("generated_widget_type_max_share_80pct", None)
    return {
        **universal,
        **_family_count_checks(
            tasks,
            expected={family: count for family, (count, _) in USAGE_FAMILIES.items()},
        ),
        "grader_mutation_sensitive": _mutation_suite_passes(tasks, oracle_results),
        "task_count_90": total == 90,
        "ladder_cells_two_spines": ladder_ok,
        "turn_budget_reference_plus_three": budget_ok,
        "fingerprint_unique": len(set(fingerprints)) == total,
        "all_level_difficulties": all(
            task.difficulty.startswith("level") for task in tasks
        ),
        "catalog_coverage": {
            "Bench Stark Enterprise",
            "Getting Started",
            "Widget Examples",
            "Bench Daloopa",
        } <= origins,
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
        "suite_content_hash_matches": _suite_content_hash_matches(tasks),
    }


def _suite_content_hash_matches(tasks: list[Task]) -> bool:
    """Recompute the shipped payload digest and compare to the manifest's."""

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
    return (
        len(expected_hashes) == 1
        and observed_hash is not None
        and observed_hash in expected_hashes
    )


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
