"""Load, replay, and normalize benchmark attempts into rollout records."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable

from workspace_bench.agents.agent_command import build_task_envelope, load_tool_calls
from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.exports.metadata import base_export_metadata
from workspace_bench.exports.schema import RolloutRecord
from workspace_bench.core.models import JsonDict, RunResult, Task, ToolCall
from workspace_bench.core.runner import TaskRunner


def rollouts_from_oracle(tasks: Iterable[Task]) -> list[RolloutRecord]:
    """Export reference oracle traces as rollout records."""

    runner = TaskRunner()
    records = []
    for task in tasks:
        result = runner.run(task, "oracle")
        records.append(
            run_result_to_rollout(
                result,
                task=build_task_envelope(task),
                metadata={
                    "source": "oracle",
                    "runner": "oracle",
                    "attempt_id": f"oracle:{task.id}:1",
                    "repeat": 1,
                },
            )
        )
    return records


def load_comparison_rollouts(
    comparison_dir: Path,
    tasks: Iterable[Task],
) -> list[RolloutRecord]:
    """Load model comparison artifacts and normalize them into rollout records."""

    if not comparison_dir.exists():
        raise FileNotFoundError(f"comparison directory does not exist: {comparison_dir}")
    task_by_id = {task.id: task for task in tasks}
    records = []
    for result_path in sorted(comparison_dir.glob("*.json")):
        if result_path.name == "comparison.json":
            continue
        payload = _read_json(result_path)
        if "results" not in payload or "model" not in payload:
            continue
        model = payload["model"]
        for item in payload["results"]:
            task = task_by_id.get(item["id"])
            if task is None:
                continue
            output_path = _resolve_artifact_path(
                item.get("output_path"), base_dir=comparison_dir
            )
            task_path = _resolve_artifact_path(
                item.get("task_path"), base_dir=comparison_dir
            )
            run_dir = _resolve_artifact_path(item.get("run_dir"), base_dir=comparison_dir)
            tool_calls = load_tool_calls(output_path)
            result = replay_tool_calls(task, tool_calls)
            task = _read_json(task_path) if task_path.exists() else build_task_envelope(task)
            messages_path = run_dir / "conversation.json"
            messages = _read_json(messages_path) if messages_path.exists() else []
            records.append(
                run_result_to_rollout(
                    result,
                    task=task,
                    messages=messages,
                    metadata={
                        "source": "comparison",
                        "model_slug": model.get("slug"),
                        "model_label": model.get("label"),
                        "runner": item.get("runner"),
                        "repeat": item.get("repeat", 1),
                        "attempt_id": (
                            f"{model.get('slug')}:{task.id}:"
                            f"{item.get('repeat', 1)}"
                        ),
                        "result_path": str(result_path),
                        "run_dir": str(run_dir),
                    },
                    process_metadata={
                        "agent_exit_code": item.get("agent_exit_code"),
                        "agent_timed_out": item.get("agent_timed_out"),
                        "process_failed": item.get("process_failed"),
                    },
                )
            )
    return records


def load_trace_dir_rollouts(
    trace_dir: Path,
    tasks: Iterable[Task],
) -> list[RolloutRecord]:
    """Load trace artifacts produced by ``workspace-bench run --trace-dir``."""

    if not trace_dir.exists():
        raise FileNotFoundError(f"trace directory does not exist: {trace_dir}")
    task_by_id = {task.id: task for task in tasks}
    records = []
    for trace_path in sorted(trace_dir.glob("*.json")):
        payload = _read_json(trace_path)
        task_payload = payload.get("task", {})
        task_id = task_payload.get("id")
        task = task_by_id.get(task_id)
        task = (
            build_task_envelope(task)
            if task is not None
            else {"schema_version": "workspace-bench-task-v1", "task": task_payload}
        )
        trace = payload.get("trace", [])
        tool_calls = [
            {"tool": event.get("tool"), "args": event.get("args", {})}
            for event in trace
        ]
        tool_results = [
            {
                "index": event.get("index"),
                "tool": event.get("tool"),
                "ok": event.get("ok"),
                "result": event.get("result"),
            }
            for event in trace
        ]
        grade = payload.get("grade", {})
        records.append(
            RolloutRecord(
                task=task,
                messages=synthesize_messages(task, tool_calls),
                tool_calls=tool_calls,
                tool_results=tool_results,
                final_snapshot=payload.get("final_snapshot", {}),
                grade=grade,
                metadata={
                    **base_export_metadata(),
                    "source": "trace_dir",
                    "task_id": task_id,
                    "level": task_payload.get("level"),
                    "difficulty": task_payload.get("difficulty"),
                    "capability": task_payload.get("capability"),
                    "workflow": task_payload.get("workflow"),
                    "domain": task_payload.get("domain"),
                    "subdomain": task_payload.get("subdomain"),
                    "passed": grade.get("passed"),
                    "score": grade.get("score"),
                    "trace_path": str(trace_path),
                },
            )
        )
    return records


def replay_tool_calls(task: Task, tool_calls: Iterable[ToolCall]) -> RunResult:
    """Replay tool calls in the simulator and return a freshly graded result."""

    episode = WorkspaceEpisode(task=task)
    for call in tool_calls:
        episode.step(call)
    return RunResult(
        task=task,
        grade=episode.grade(),
        trace=tuple(episode.trace),
        final_snapshot=episode.snapshot(),
    )


def run_result_to_rollout(
    result: RunResult,
    *,
    task: JsonDict,
    messages: list[JsonDict] | None = None,
    metadata: JsonDict | None = None,
    process_metadata: JsonDict | None = None,
) -> RolloutRecord:
    """Convert a graded run result into the canonical rollout schema."""

    tool_calls = [
        {"tool": event.call.name, "args": event.call.args}
        for event in result.trace
    ]
    grade = asdict(result.grade)
    combined_metadata = {
        **base_export_metadata(),
        "task_id": result.task.id,
        "level": result.task.level,
        "difficulty": result.task.difficulty,
        "split": result.task.split,
        "capability": result.task.capability,
        "workflow": result.task.workflow,
        "domain": result.task.domain,
        "subdomain": result.task.subdomain,
        "passed": result.grade.passed,
        "score": result.grade.score,
    }
    combined_metadata.update(metadata or {})
    combined_metadata.update(process_metadata or {})
    return RolloutRecord(
        task=task,
        messages=messages or synthesize_messages(task, tool_calls),
        tool_calls=tool_calls,
        tool_results=[
            {
                "index": event.index,
                "tool": event.call.name,
                "ok": event.ok,
                "result": event.result,
            }
            for event in result.trace
        ],
        final_snapshot=result.final_snapshot,
        grade=grade,
        metadata=combined_metadata,
    )


def synthesize_messages(task: JsonDict, tool_calls: list[JsonDict]) -> list[JsonDict]:
    """Create a minimal two-message training conversation from tool calls."""

    task = task.get("task", {})
    return [
        {
            "role": "user",
            "content": json.dumps(
                {
                    "prompt": task.get("prompt"),
                    "allowed_tools": task.get("allowed_tools", []),
                    "initial_state": task.get("initial_state", {}),
                },
                sort_keys=True,
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps({"tool_calls": tool_calls}, sort_keys=True),
        },
    ]


def _read_json(path: Path) -> JsonDict:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_artifact_path(value: Any, *, base_dir: Path) -> Path:
    if not isinstance(value, str) or not value:
        return base_dir
    path = Path(value)
    if path.is_absolute() or path.exists():
        return path
    candidate = base_dir / path
    if candidate.exists():
        return candidate
    return path
