"""Tests for the policy-driven suite-authoring harness."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts/generators"))

from _assembly import (  # noqa: E402
    ArtifactDiscriminator,
    CheckTypePolicy,
    NoveltyPolicy,
    PhrasingSelector,
    SplitAssigner,
    TaskAssembler,
    build_matrix,
    difficulty_for,
    diversify_generated_widget_proof,
    snap,
    uniform_four_way_pattern,
)


def _select(
    selector: PhrasingSelector, task_id: str, variants: list[str]
) -> str:
    return selector(task_id, variants)


def test_literal_shared_helpers_preserve_generator_conventions() -> None:
    assert [difficulty_for("r1", index) for index in range(1, 5)] == [
        "easy",
        "easy",
        "medium",
        "medium",
    ]
    assert [difficulty_for("r3", index) for index in range(1, 5)] == [
        "medium",
        "medium",
        "hard",
        "hard",
    ]
    assert difficulty_for("r0", 99) == "easy"
    assert difficulty_for("r2", 1) == "medium"
    assert difficulty_for("r4", 1) == "hard"
    assert snap() == {"tool": "get_workspace_snapshot", "args": {}}


def test_phrasing_selector_supports_core_identity_normalization() -> None:
    pools: dict[str, int] = {}
    variants = ["alpha", "bravo", "charlie"]
    selector = PhrasingSelector(pools, normalize_id=lambda task_id: task_id.removeprefix("old_"))

    selected = _select(selector, "old_public_id", variants)
    expected_index = int(hashlib.md5(b"public_id").hexdigest(), 16) % len(variants)

    assert selected == variants[expected_index]
    assert list(pools.values()) == [3]
    assert _select(selector, "old_public_id", variants) == selected


def test_generated_widget_proof_diversification_is_deterministic() -> None:
    task = {
        "id": "proof_task",
        "prompt": "Add a completion note with the verified facts.",
        "success": {"required_generated_widgets": [{"widget_type": "note"}]},
        "oracle_tool_calls": [
            {
                "tool": "add_generative_widget",
                "args": {"widget_type": "note", "data": "verified facts"},
            }
        ],
    }
    diversify_generated_widget_proof(task, share=1)
    assert task["success"]["required_generated_widgets"][0]["widget_type"] == "html"
    assert task["oracle_tool_calls"][0]["args"]["widget_type"] == "html"
    assert task["oracle_tool_calls"][0]["args"]["data"].startswith("<section>")
    assert "HTML card" in task["prompt"]


def test_build_family_prompt_sites_all_use_phrased() -> None:
    from generate_build_apps_suite import prompt_sites_use_phrased

    assert prompt_sites_use_phrased()


def test_check_type_policies_make_historical_suite_differences_explicit() -> None:
    task = {
        "success": {
            "required_widgets": [{"min_count": 0, "max_count": 0}],
        }
    }
    common_checks = {"required_tabs": "missing_tab"}
    core_policy = CheckTypePolicy(
        success_checks=common_checks,
        widget_mode="cardinality",
        within_grid_default=True,
        max_invalid_tool_calls_default=0,
        include_forbid_invented_widget_ids=True,
    )
    build_policy = CheckTypePolicy(
        success_checks=common_checks,
        widget_mode="collection",
        within_grid_default=False,
        max_invalid_tool_calls_default=None,
    )

    assert core_policy(task) == (
        "layout_out_of_grid",
        "too_many_invalid_calls",
        "too_many_widgets",
    )
    assert build_policy(task) == ("missing_widget",)


def test_artifact_and_novelty_policies_share_mechanics_with_suite_prefixes() -> None:
    task = {
        "id": "task_one",
        "_family": "widgets",
        "_rung": "r2",
        "oracle_tool_calls": [{"tool": "create_widget", "args": {}}],
        "success": {
            "required_widgets": [
                {"origin": "Bench", "widget_id": "prices", "tab_id": "main"}
            ],
            "required_tabs": ["main"],
        },
    }
    discriminator = ArtifactDiscriminator(
        leading_parts=lambda item: [f"suite:{item['_family']}"]
    )
    novelty = NoveltyPolicy(
        check_types=lambda item: ("missing_widget",),
        task_backends=lambda item: {"equities"},
        artifact_discriminator=discriminator,
    )

    assert discriminator(task) == (
        "suite:widgets|widgets:Bench/prices@main|tabs:main"
    )
    assert novelty.fingerprint(task) == (
        "widgets",
        "r2",
        ("create_widget",),
        ("missing_widget",),
        ("equities",),
        "suite:widgets|widgets:Bench/prices@main|tabs:main",
    )
    novelty.add_description(task)
    assert task["novelty"].startswith("Unique widgets/task_one exercise using create_widget")


def test_task_assembly_split_assignment_and_matrix_are_policy_driven() -> None:
    scenarios: list[dict] = []
    counts: dict[tuple[str, str], int] = {}

    def set_category(task: dict, family: str) -> None:
        task["category"] = family

    def normalize_identity(task: dict) -> None:
        task["id"] = task["id"].lower()

    def after_identity(task: dict, family: str, level: str, cell_index: int) -> None:
        task["capability"] = f"{family}-{level}-{cell_index}"

    def set_difficulty(task: dict, family: str, level: str, cell_index: int) -> None:
        del family
        task["difficulty"] = difficulty_for(level, cell_index)
        task["specification_level"] = {
            "easy": "explicit",
            "medium": "partially-specified",
            "hard": "open-brief",
        }[task["difficulty"]]

    def tag_prefixes(family: str, level: str, cell_index: int) -> tuple[str, str]:
        del level
        return (f"family-{family}", f"cell{cell_index}")

    def finalize(task: dict, family: str, level: str, cell_index: int) -> None:
        del family, level, cell_index
        task["finalized"] = True

    assembler = TaskAssembler(
        scenarios=scenarios,
        cell_counts=counts,
        source="test-generator",
        rung_slack={"r1": 3},
        set_category=set_category,
        normalize_identity=normalize_identity,
        after_identity=after_identity,
        set_difficulty=set_difficulty,
        tag_prefixes=tag_prefixes,
        finalize_task=finalize,
    )
    for task_id in ("DELTA", "ALPHA", "CHARLIE", "BRAVO"):
        assembler.add(
            "sample",
            "r1",
            {"id": task_id, "oracle_tool_calls": [{"tool": "noop", "args": {}}]},
        )

    SplitAssigner(uniform_four_way_pattern)(scenarios)

    by_id = {task["id"]: task for task in scenarios}
    assert [by_id[task_id]["split"] for task_id in ("alpha", "bravo", "charlie", "delta")] == [
        "train",
        "train",
        "validation",
        "test",
    ]
    assert by_id["delta"]["source"] == "test-generator"
    assert by_id["delta"]["tags"] == ["family-sample", "cell1"]
    assert by_id["delta"]["limits"] == {"max_turns": 4}
    assert by_id["charlie"]["limits"] == {"max_turns": 13}
    assert by_id["bravo"]["limits"] == {"max_turns": 13}
    assert by_id["delta"]["finalized"] is True
    assert build_matrix(scenarios) == {"sample": {"r1": 4}}
