"""Separate Harbor verifier backed by the canonical Workspace Bench grader."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from workspace_bench.core.graders import grade_task
from workspace_bench.integrations.harbor.artifacts import (
    EPISODE_SCHEMA_VERSION,
    atomic_write_json,
    full_grade_payload,
    trace_event_from_payload,
)
from workspace_bench.integrations.harbor.bundle import load_sealed_task


SYNTHETIC_MCP_ACTIONS = {"read_workspace_resource", "get_workspace_prompt"}


def load_episode(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("episode artifact must contain a JSON object")
    if payload.get("schema_version") != EPISODE_SCHEMA_VERSION:
        raise ValueError(f"unsupported episode schema: {payload.get('schema_version')!r}")
    if payload.get("finalized") is not True:
        raise ValueError("episode artifact was not finalized by the trusted runtime")
    if not isinstance(payload.get("initial_snapshot"), dict):
        raise ValueError("episode artifact is missing initial_snapshot")
    if not isinstance(payload.get("final_snapshot"), dict):
        raise ValueError("episode artifact is missing final_snapshot")
    if not isinstance(payload.get("trace"), list):
        raise ValueError("episode artifact is missing trace")
    if not isinstance(payload.get("bridge_events"), list):
        raise ValueError("episode artifact is missing bridge_events")
    return payload


def _validate_trace_and_bridge(trace: tuple[Any, ...], bridge_events: list[Any]) -> None:
    for expected_index, event in enumerate(trace, start=1):
        if event.index != expected_index:
            raise ValueError("trace indexes must be contiguous and one-based")

    bridge_names = []
    for item in bridge_events:
        if not isinstance(item, dict) or not isinstance(item.get("translated_tool"), str):
            raise ValueError("bridge event has an invalid shape")
        bridge_names.append(item["translated_tool"])

    # Every browser command must correspond, in order, to an agent-facing
    # canonical call. Validation errors and the harness-only actions legitimately
    # have no browser command, so trace may contain additional entries.
    trace_names = [
        event.call.name
        for event in trace
        if event.call.name not in {"final_answer", *SYNTHETIC_MCP_ACTIONS}
    ]
    cursor = 0
    for bridge_name in bridge_names:
        while cursor < len(trace_names) and trace_names[cursor] != bridge_name:
            cursor += 1
        if cursor >= len(trace_names):
            raise ValueError(
                f"bridge command {bridge_name!r} has no matching canonical trace call"
            )
        cursor += 1


def verify_episode(*, task_path: Path, episode_path: Path) -> tuple[dict[str, Any], dict[str, float]]:
    task, metadata = load_sealed_task(task_path)
    episode = load_episode(episode_path)
    observed_task = episode.get("task")
    if not isinstance(observed_task, dict):
        raise ValueError("episode artifact is missing task identity")
    for field in ("qualified_id", "suite_content_sha256", "bundle_sha256"):
        if observed_task.get(field) != metadata.get(field):
            raise ValueError(
                f"episode task identity mismatch for {field}: "
                f"{observed_task.get(field)!r} != {metadata.get(field)!r}"
            )

    trace = tuple(trace_event_from_payload(item) for item in episode["trace"])
    _validate_trace_and_bridge(trace, episode["bridge_events"])
    grade = grade_task(
        task,
        episode["final_snapshot"],
        trace,
        initial_snapshot=episode["initial_snapshot"],
    )
    grade_payload = full_grade_payload(grade)
    grade_payload.update(
        {
            "schema_version": "workspace-bench-harbor-grade/v1",
            "qualified_id": task.qualified_id,
            "suite_content_sha256": task.suite.content_sha256 if task.suite else None,
            "bundle_sha256": metadata["bundle_sha256"],
            "track": "harbor-native",
        }
    )
    rewards = {
        "reward": float(grade.passed),
        "deterministic_strict": float(grade.passed),
        "judged_strict": float(grade.passed and not grade.judge_pending),
        "outcome": float(grade.score),
        "state": float(grade.state_score),
        "trace": float(grade.trace_score),
        "preservation": float(grade.preservation_score),
        "runtime": float(grade.runtime_score),
        "judge_pending": float(grade.judge_pending),
    }
    return grade_payload, rewards


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="workspace-bench-harbor-verify")
    parser.add_argument("--task", type=Path, required=True)
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("/logs/verifier"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.output.mkdir(parents=True, exist_ok=True)
    reward_path = args.output / "reward.json"
    try:
        grade, rewards = verify_episode(task_path=args.task, episode_path=args.episode)
    except Exception as error:  # noqa: BLE001 - verifier must fail closed with a reward.
        rewards = {
            "reward": 0.0,
            "deterministic_strict": 0.0,
            "judged_strict": 0.0,
            "outcome": 0.0,
            "state": 0.0,
            "trace": 0.0,
            "preservation": 0.0,
            "runtime": 0.0,
            "judge_pending": 0.0,
        }
        atomic_write_json(
            args.output / "verifier_error.json",
            {
                "schema_version": "workspace-bench-harbor-verifier-error/v1",
                "error_type": type(error).__name__,
                "message": str(error),
            },
        )
        atomic_write_json(reward_path, rewards)
        return 0

    atomic_write_json(args.output / "grade.json", grade)
    atomic_write_json(reward_path, rewards)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

