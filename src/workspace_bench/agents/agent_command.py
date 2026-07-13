"""External command adapter for bring-your-own Workspace agents."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from workspace_bench.core._proc import decode_output, truncate_output
from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import (
    BENCHMARK_NAME,
    CANARY_GUID,
    JsonDict,
    RunResult,
    Task,
    ToolCall,
)
from workspace_bench.core.provenance import git_provenance


@dataclass(frozen=True)
class AgentCommandRun:
    """One external-agent execution and its graded Workspace result."""

    run_result: RunResult
    command: str
    exit_code: int | None
    timed_out: bool
    stdout: str
    stderr: str
    run_dir: Path
    task_path: Path
    output_path: Path


def build_task_envelope(task: Task) -> JsonDict:
    """Build the public task payload handed to external agents."""

    suite = task.suite
    return {
        "schema_version": "workspace-bench-envelope",
        "benchmark": {
            "name": BENCHMARK_NAME,
            "suite_id": suite.suite_id if suite else "local",
            "content_sha256": suite.content_sha256 if suite else None,
            **git_provenance(source_paths=[task.source_path] if task.source_path else None),
            "canary_guid": CANARY_GUID,
        },
        "task": {
            "id": task.id,
            "qualified_id": task.qualified_id,
            "category": task.category,
            "family": task.family,
            "specification_level": task.specification_level,
            "difficulty": task.difficulty,
            "prompt": task.prompt,
            "business_terms": list(task.business_terms),
            "fixtures": {
                "backends": [
                    {
                        "name": backend.name,
                        "backend_id": backend.backend_id,
                        "url": backend.url,
                    }
                    for backend in task.fixtures
                ]
            },
            "initial_state": task.initial_state,
            "allowed_tools": list(task.allowed_tools),
            "limits": task.limits,
        },
        "tool_call_protocol": {
            "format": "jsonl",
            "output_env": "WORKSPACE_BENCH_OUTPUT_JSONL",
            "record_shape": {"tool": "tool_name", "args": {}},
            "notes": [
                "Write one JSON object per line.",
                "Use only tools listed in task.allowed_tools.",
                "The harness executes calls after the command exits and grades final state.",
            ],
        },
    }


def write_task_envelope(path: Path, task: Task) -> None:
    """Write one task envelope JSON file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(build_task_envelope(task), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_tool_calls(path: Path) -> tuple[ToolCall, ...]:
    """Load JSONL or JSON-array tool calls emitted by an external agent."""

    if not path.exists():
        return ()
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return ()
    if text.startswith("["):
        payload = json.loads(text)
        if not isinstance(payload, list):
            raise ValueError("tool call JSON must be an array or JSONL records")
        return tuple(ToolCall.from_dict(item) for item in payload)
    calls = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"tool call line {line_number} must be an object")
        calls.append(ToolCall.from_dict(payload))
    return tuple(calls)


def run_agent_command(
    *,
    task: Task,
    command: str,
    timeout_seconds: float = 120,
    run_dir: Path | None = None,
) -> AgentCommandRun:
    """Run an external command that writes JSONL tool calls, then grade it."""

    resolved_run_dir = run_dir or Path(tempfile.mkdtemp(prefix="workspace-bench-"))
    resolved_run_dir.mkdir(parents=True, exist_ok=True)
    task_path = resolved_run_dir / "task.json"
    output_path = resolved_run_dir / "tool_calls.jsonl"
    write_task_envelope(task_path, task)
    if output_path.exists():
        output_path.unlink()

    env = os.environ.copy()
    env.update(
        {
            "WORKSPACE_BENCH_TASK_JSON": str(task_path),
            "WORKSPACE_BENCH_OUTPUT_JSONL": str(output_path),
            "WORKSPACE_BENCH_RUN_DIR": str(resolved_run_dir),
            "WORKSPACE_BENCH_TASK_ID": task.id,
        }
    )

    timed_out = False
    exit_code: int | None
    stdout = ""
    stderr = ""
    try:
        completed = subprocess.run(
            command,
            shell=True,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        exit_code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        exit_code = None
        stdout = decode_output(error.stdout)
        stderr = decode_output(error.stderr)

    try:
        tool_calls = load_tool_calls(output_path)
    except Exception as error:  # noqa: BLE001 - convert malformed output to failed run.
        tool_calls = (
            ToolCall(
                name="agent_output_parse_error",
                args={"message": str(error)},
            ),
        )

    episode = WorkspaceEpisode(task=task)
    for call in tool_calls:
        episode.step(call)
    final_snapshot = episode.snapshot()
    grade = episode.grade()

    return AgentCommandRun(
        run_result=RunResult(
            task=task,
            grade=grade,
            trace=tuple(episode.trace),
            final_snapshot=final_snapshot,
        ),
        command=command,
        exit_code=exit_code,
        timed_out=timed_out,
        stdout=truncate_output(stdout),
        stderr=truncate_output(stderr),
        run_dir=resolved_run_dir,
        task_path=task_path,
        output_path=output_path,
    )
