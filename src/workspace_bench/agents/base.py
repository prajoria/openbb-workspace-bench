"""Simple benchmark agents."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from workspace_bench.core.models import FINAL_ANSWER_TOOL, Task, ToolCall


class BenchAgent(Protocol):
    """Agent interface used by the local runner."""

    @property
    def name(self) -> str:
        """Stable agent name used in reports."""
        ...

    def tool_calls(self, task: Task) -> tuple[ToolCall, ...]:
        """Return the tool calls to execute for a task."""


@dataclass(frozen=True)
class OracleAgent:
    """Replays the task's reference tool-call trace.

    The reference trace holds only the workspace interactions; for reply
    tasks the answer lives in ``eval.reference_answer``, so the oracle
    synthesizes the ``final_answer`` submission at the end of its replay.
    """

    name: str = "oracle"

    def tool_calls(self, task: Task) -> tuple[ToolCall, ...]:
        calls = task.oracle_tool_calls
        if task.reference_answer and not any(
            call.name == FINAL_ANSWER_TOOL for call in calls
        ):
            calls = (
                *calls,
                ToolCall(name=FINAL_ANSWER_TOOL, args={"text": task.reference_answer}),
            )
        return calls


@dataclass(frozen=True)
class NoopAgent:
    """Does nothing; useful as a failing baseline."""

    name: str = "noop"

    def tool_calls(self, task: Task) -> tuple[ToolCall, ...]:
        return ()


def build_agent(name: str) -> BenchAgent:
    """Create a built-in agent by name."""

    if name == "oracle":
        return OracleAgent()
    if name == "noop":
        return NoopAgent()
    raise ValueError(f"Unknown built-in agent {name!r}. Available: oracle, noop")

