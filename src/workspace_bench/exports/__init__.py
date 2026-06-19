"""Rollout and training-data export helpers."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Literal

from workspace_bench.agent_command import build_task_envelope, load_tool_calls
from workspace_bench.episode import WorkspaceEpisode
from workspace_bench.models import JsonDict, RunResult, Scenario, ToolCall
from workspace_bench.runner import ScenarioRunner


SFTFormat = Literal["sharegpt", "openai_messages", "tool_call_jsonl"]


@dataclass(frozen=True)
class RolloutRecord:
    """Canonical portable record for one Workspace Bench attempt."""

    task: JsonDict
    messages: list[JsonDict]
    tool_calls: list[JsonDict]
    tool_results: list[JsonDict]
    final_snapshot: JsonDict
    grade: JsonDict
    metadata: JsonDict

    def to_dict(self) -> JsonDict:
        return {
            "schema_version": "workspace-bench-rollout-v1",
            "task": self.task,
            "messages": self.messages,
            "tool_calls": self.tool_calls,
            "tool_results": self.tool_results,
            "final_snapshot": self.final_snapshot,
            "grade": self.grade,
            "metadata": self.metadata,
        }


def rollouts_from_oracle(scenarios: Iterable[Scenario]) -> list[RolloutRecord]:
    """Export reference oracle traces as rollout records."""

    runner = ScenarioRunner()
    records = []
    for scenario in scenarios:
        result = runner.run(scenario, "oracle")
        records.append(
            run_result_to_rollout(
                result,
                task=build_task_envelope(scenario),
                metadata={
                    "source": "oracle",
                    "runner": "oracle",
                    "attempt_id": f"oracle:{scenario.id}:1",
                    "repeat": 1,
                },
            )
        )
    return records


def load_comparison_rollouts(
    comparison_dir: Path,
    scenarios: Iterable[Scenario],
) -> list[RolloutRecord]:
    """Load model comparison artifacts and normalize them into rollout records."""

    if not comparison_dir.exists():
        raise FileNotFoundError(f"comparison directory does not exist: {comparison_dir}")
    scenario_by_id = {scenario.id: scenario for scenario in scenarios}
    records = []
    for result_path in sorted(comparison_dir.glob("*.json")):
        if result_path.name == "comparison.json":
            continue
        payload = _read_json(result_path)
        if "results" not in payload or "model" not in payload:
            continue
        model = payload["model"]
        for item in payload["results"]:
            scenario = scenario_by_id.get(item["id"])
            if scenario is None:
                continue
            output_path = _resolve_artifact_path(
                item.get("output_path"), base_dir=comparison_dir
            )
            task_path = _resolve_artifact_path(
                item.get("task_path"), base_dir=comparison_dir
            )
            run_dir = _resolve_artifact_path(item.get("run_dir"), base_dir=comparison_dir)
            tool_calls = load_tool_calls(output_path)
            result = replay_tool_calls(scenario, tool_calls)
            task = _read_json(task_path) if task_path.exists() else build_task_envelope(scenario)
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
                            f"{model.get('slug')}:{scenario.id}:"
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
    scenarios: Iterable[Scenario],
) -> list[RolloutRecord]:
    """Load trace artifacts produced by ``workspace-bench run --trace-dir``."""

    if not trace_dir.exists():
        raise FileNotFoundError(f"trace directory does not exist: {trace_dir}")
    scenario_by_id = {scenario.id: scenario for scenario in scenarios}
    records = []
    for trace_path in sorted(trace_dir.glob("*.json")):
        payload = _read_json(trace_path)
        scenario_payload = payload.get("scenario", {})
        scenario_id = scenario_payload.get("id")
        scenario = scenario_by_id.get(scenario_id)
        task = (
            build_task_envelope(scenario)
            if scenario is not None
            else {"schema_version": "workspace-bench-task-v1", "scenario": scenario_payload}
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
                    "source": "trace_dir",
                    "scenario_id": scenario_id,
                    "level": scenario_payload.get("level"),
                    "difficulty": scenario_payload.get("difficulty"),
                    "category": scenario_payload.get("category"),
                    "passed": grade.get("passed"),
                    "score": grade.get("score"),
                    "trace_path": str(trace_path),
                },
            )
        )
    return records


def replay_tool_calls(scenario: Scenario, tool_calls: Iterable[ToolCall]) -> RunResult:
    """Replay tool calls in the simulator and return a freshly graded result."""

    episode = WorkspaceEpisode(scenario=scenario)
    for call in tool_calls:
        episode.step(call)
    return RunResult(
        scenario=scenario,
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
        "scenario_id": result.scenario.id,
        "level": result.scenario.level,
        "difficulty": result.scenario.difficulty,
        "split": result.scenario.split,
        "category": result.scenario.category,
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


def write_rollouts_jsonl(records: Iterable[RolloutRecord], output_path: Path) -> int:
    """Write canonical rollout JSONL and return record count."""

    return _write_jsonl((record.to_dict() for record in records), output_path)


def write_sft_jsonl(
    records: Iterable[RolloutRecord],
    output_path: Path,
    *,
    fmt: SFTFormat,
    include_failures: bool = False,
) -> int:
    """Write SFT-ready JSONL in one of the supported message formats."""

    rows = []
    for record in records:
        if not include_failures and not record.metadata.get("passed"):
            continue
        rows.append(format_sft_record(record, fmt=fmt))
    return _write_jsonl(rows, output_path)


def format_sft_record(record: RolloutRecord, *, fmt: SFTFormat) -> JsonDict:
    if fmt == "openai_messages":
        return {"messages": record.messages, "metadata": record.metadata}
    if fmt == "sharegpt":
        role_map = {"system": "system", "user": "human", "assistant": "gpt"}
        return {
            "conversations": [
                {
                    "from": role_map.get(str(message.get("role")), message.get("role")),
                    "value": message.get("content", ""),
                }
                for message in record.messages
            ],
            "metadata": record.metadata,
        }
    if fmt == "tool_call_jsonl":
        return {
            "task": record.task,
            "tool_calls": record.tool_calls,
            "metadata": record.metadata,
        }
    raise ValueError(f"Unknown SFT format {fmt!r}")


def build_preference_pairs(records: Iterable[RolloutRecord]) -> list[JsonDict]:
    """Create best-vs-worst pairs from repeated attempts on the same scenario."""

    grouped: dict[tuple[str | None, str | None], list[RolloutRecord]] = {}
    for record in records:
        key = (
            record.metadata.get("model_slug") or record.metadata.get("runner"),
            record.metadata.get("scenario_id"),
        )
        grouped.setdefault(key, []).append(record)

    pairs = []
    for (model_slug, scenario_id), attempts in grouped.items():
        if len(attempts) < 2:
            continue
        ranked = sorted(attempts, key=_preference_rank)
        rejected = ranked[0]
        chosen = ranked[-1]
        if _preference_rank(chosen) == _preference_rank(rejected):
            continue
        pairs.append(
            {
                "schema_version": "workspace-bench-preference-v1",
                "scenario_id": scenario_id,
                "model_slug": model_slug,
                "chosen": chosen.to_dict(),
                "rejected": rejected.to_dict(),
                "metadata": {
                    "chosen_score": chosen.metadata.get("score"),
                    "rejected_score": rejected.metadata.get("score"),
                    "chosen_passed": chosen.metadata.get("passed"),
                    "rejected_passed": rejected.metadata.get("passed"),
                },
            }
        )
    return pairs


def write_preferences_jsonl(
    records: Iterable[RolloutRecord],
    output_path: Path,
) -> int:
    return _write_jsonl(build_preference_pairs(records), output_path)


def synthesize_messages(task: JsonDict, tool_calls: list[JsonDict]) -> list[JsonDict]:
    """Create a minimal two-message training conversation from tool calls."""

    scenario = task.get("scenario", {})
    return [
        {
            "role": "user",
            "content": json.dumps(
                {
                    "prompt": scenario.get("prompt"),
                    "allowed_tools": scenario.get("allowed_tools", []),
                    "initial_state": scenario.get("initial_state", {}),
                },
                sort_keys=True,
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps({"tool_calls": tool_calls}, sort_keys=True),
        },
    ]


def _preference_rank(record: RolloutRecord) -> tuple[int, float]:
    return (
        1 if record.metadata.get("passed") else 0,
        float(record.metadata.get("score") or 0.0),
    )


def _write_jsonl(rows: Iterable[JsonDict], output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
            count += 1
    return count


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
