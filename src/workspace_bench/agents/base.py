"""Simple benchmark agents."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from workspace_bench.core.models import Scenario, ToolCall


class BenchAgent(Protocol):
    """Agent interface used by the local runner."""

    name: str

    def tool_calls(self, scenario: Scenario) -> tuple[ToolCall, ...]:
        """Return the tool calls to execute for a scenario."""


@dataclass(frozen=True)
class OracleAgent:
    """Replays the scenario's reference tool-call trace."""

    name: str = "oracle"

    def tool_calls(self, scenario: Scenario) -> tuple[ToolCall, ...]:
        return scenario.oracle_tool_calls


@dataclass(frozen=True)
class NoopAgent:
    """Does nothing; useful as a failing baseline."""

    name: str = "noop"

    def tool_calls(self, scenario: Scenario) -> tuple[ToolCall, ...]:
        return ()


def build_agent(name: str) -> BenchAgent:
    """Create a built-in agent by name."""

    if name == "oracle":
        return OracleAgent()
    if name == "noop":
        return NoopAgent()
    raise ValueError(f"Unknown built-in agent {name!r}. Available: oracle, noop")

