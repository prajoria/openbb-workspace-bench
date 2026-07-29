from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import pytest

from workspace_bench.agents import OracleAgent
from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.graders import grade_task
from workspace_bench.core.models import GradeResult, Task
from workspace_bench.core.runner import find_task
from workspace_bench.integrations.harbor.artifacts import (
    EPISODE_SCHEMA_VERSION,
    trace_event_payload,
)
from workspace_bench.integrations.harbor.bundle import (
    BUNDLE_SCHEMA_VERSION,
    load_sealed_task,
)
from workspace_bench.integrations.harbor.exporter import _instruction
from workspace_bench.integrations.harbor.verifier import load_episode, verify_episode
from workspace_bench.reports.serialization import grade_summary


TASK_REF = (
    "enterprise-apps-default/compliance_surveillance_hub/"
    "compliance_surveillance_hub_p3_x"
)


def _sealed_bundle(tmp_path: Path) -> tuple[Path, Task, dict]:
    task = find_task(TASK_REF)
    assert task.source_path is not None
    assert task.suite is not None
    bundle = {
        "schema_version": BUNDLE_SCHEMA_VERSION,
        "qualified_id": task.qualified_id,
        "family": task.family,
        "task": json.loads(task.source_path.read_text(encoding="utf-8")),
        "suite": asdict(task.suite),
        "provenance": {
            "workspace_bench_git_commit": "test-bench",
            "workspace_mcp_git_commit": "test-sidecar",
            "harbor_version": "0.20.0",
        },
    }
    path = tmp_path / "sealed-task.json"
    path.write_text(json.dumps(bundle), encoding="utf-8")
    loaded, metadata = load_sealed_task(path)
    return path, loaded, metadata


def _episode_payload(
    task: Task, metadata: dict, *, oracle: bool
) -> tuple[dict, GradeResult]:
    episode = WorkspaceEpisode(task)
    if oracle:
        for call in OracleAgent().tool_calls(task):
            episode.step(call)
    final_snapshot = episode.snapshot()
    trace = tuple(episode.trace)
    payload = {
        "schema_version": EPISODE_SCHEMA_VERSION,
        "task": metadata,
        "status": "finalized",
        "initial_snapshot": episode.initial_snapshot,
        "final_snapshot": final_snapshot,
        "trace": [trace_event_payload(event) for event in trace],
        "bridge_events": [
            {"translated_tool": event.call.name}
            for event in trace
            if event.call.name != "final_answer"
        ],
        "rejections": [],
        "answered": episode.answered,
        "final_answer": episode.final_answer,
        "turns_used": len(trace),
        "max_turns": episode.max_turns,
        "turns_exhausted": False,
        "finalized": True,
    }
    native_grade = grade_task(
        task,
        final_snapshot,
        trace,
        initial_snapshot=episode.initial_snapshot,
    )
    return payload, native_grade


@pytest.mark.parametrize(
    ("oracle", "expected_reward"),
    [(True, 1.0), (False, 0.0)],
)
def test_harbor_verifier_matches_native_grade(
    tmp_path: Path,
    oracle: bool,
    expected_reward: float,
) -> None:
    task_path, task, metadata = _sealed_bundle(tmp_path)
    payload, native_grade = _episode_payload(task, metadata, oracle=oracle)
    episode_path = tmp_path / "episode.json"
    episode_path.write_text(json.dumps(payload), encoding="utf-8")

    grade, rewards = verify_episode(task_path=task_path, episode_path=episode_path)

    for field, value in asdict(native_grade).items():
        assert grade[field] == value
    assert rewards["reward"] == expected_reward
    assert rewards["deterministic_strict"] == expected_reward
    assert rewards["judge_pending"] == 1.0
    if oracle:
        assert rewards["judged_strict"] == 0.0


def test_harbor_episode_must_be_finalized(tmp_path: Path) -> None:
    path = tmp_path / "episode.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": EPISODE_SCHEMA_VERSION,
                "finalized": False,
                "initial_snapshot": {},
                "final_snapshot": {},
                "trace": [],
                "bridge_events": [],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="not finalized"):
        load_episode(path)


def test_grade_summary_preserves_judge_dimensions() -> None:
    task = find_task(TASK_REF)
    episode = WorkspaceEpisode(task)
    for call in OracleAgent().tool_calls(task):
        episode.step(call)
    payload = grade_summary(episode.grade())
    assert payload["judge_passed"] is True
    assert payload["judge_pending"] is True
    assert payload["judge_checks_passed"] == 0
    assert payload["judge_checks_total"] == 1


def test_harbor_instruction_discloses_tool_budget() -> None:
    task = find_task(TASK_REF)
    instruction = _instruction(task)
    max_turns = int(task.limits["max_turns"])

    assert f"at most {max_turns} MCP tool calls" in instruction
    assert "`final_answer` submission counts as one" in instruction
