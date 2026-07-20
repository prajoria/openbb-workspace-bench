"""Release-gate checks for the bundled task suites.

The generators certify a suite at generation time; the functions here re-verify
the release-report subset from the shipped task JSON so that
``workspace-bench validate`` and ``workspace-bench report`` hold the same gates
without rerunning generation.

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
from workspace_bench.core.models import WORKSPACE_TOOL_NAMES

USAGE_SUITE = "enterprise-apps-usage"
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

# Job-shaped usage families: a full grid so every level carries the same
# number of attempts (8 families x 6 levels x 2 spines).
USAGE_FAMILIES = {
    "retrieve": (24, (0, 1, 2, 3, 4, 5)),
    "curate": (24, (0, 1, 2, 3, 4, 5)),
    "parameterize": (24, (0, 1, 2, 3, 4, 5)),
    "organize": (24, (0, 1, 2, 3, 4, 5)),
    "repair": (24, (0, 1, 2, 3, 4, 5)),
    "platform": (24, (0, 1, 2, 3, 4, 5)),
    "extend": (24, (0, 1, 2, 3, 4, 5)),
    "handoff": (24, (0, 1, 2, 3, 4, 5)),
}


def release_checks_for_suite(
    suite: str | None,
    tasks: list[Task],
    oracle_results: list[RunResult],
) -> dict[str, bool]:
    """Return the release checks for a bundled suite; {} for private suites."""

    if suite == USAGE_SUITE:
        return usage_release_checks(tasks, oracle_results)
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
        == 4
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
        "task_count_192": total == 192,
        "level_counts_equal": len(
            {
                sum(1 for task in tasks if task.difficulty == f"level{level}")
                for level in range(6)
            }
        )
        == 1,
        "ladder_cells_four_spines": ladder_ok,
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
