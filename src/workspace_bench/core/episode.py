"""Step-based Workspace Bench episode API."""

from __future__ import annotations

from workspace_bench.core.graders import grade_task
from workspace_bench.core.models import GradeResult, JsonDict, Task, ToolCall, ToolTraceEvent
from workspace_bench.workspace.simulated_workspace import SimulatedWorkspace


class WorkspaceEpisode:
    """One resettable benchmark episode.

    This is the integration point for RL loops and external agent drivers. The
    model-visible action is a Workspace MCP tool call; the observation is the
    returned tool result. Final reward is produced by ``grade``.
    """

    def __init__(
        self,
        task: Task,
        workspace: SimulatedWorkspace | None = None,
    ):
        self.task = task
        self.workspace = workspace or SimulatedWorkspace()
        self.trace: list[ToolTraceEvent] = []
        self.workspace.reset(
            backends=task.fixtures,
            initial_state=task.initial_state,
            runtime_checks=task.success.runtime,
        )
        self.initial_snapshot = self.workspace.snapshot()

    def step(self, call: ToolCall) -> JsonDict:
        """Execute one tool call and append it to the episode trace."""

        result = self._execute_allowed(call)
        self.trace.append(
            ToolTraceEvent(
                index=len(self.trace) + 1,
                call=call,
                ok=bool(result.get("ok")),
                result=result,
            )
        )
        return result

    def snapshot(self) -> JsonDict:
        """Return the current Workspace snapshot."""

        return self.workspace.snapshot()

    def grade(self) -> GradeResult:
        """Grade the current episode state."""

        return grade_task(
            self.task,
            self.snapshot(),
            tuple(self.trace),
            initial_snapshot=self.initial_snapshot,
        )

    def _execute_allowed(self, call: ToolCall) -> JsonDict:
        if self.task.allowed_tools and call.name not in self.task.allowed_tools:
            return {
                "ok": False,
                "command": call.name,
                "request_id": None,
                "message": f"Tool {call.name!r} is not allowed for this task.",
                "data": None,
                "error": {
                    "code": "invalid_request",
                    "message": f"Tool {call.name!r} is not allowed.",
                    "retryable": False,
                },
            }
        return self.workspace.call_tool(call)
