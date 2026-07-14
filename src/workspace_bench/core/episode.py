"""Step-based Workspace Bench episode API."""

from __future__ import annotations

from workspace_bench.core.graders import grade_task
from workspace_bench.core.models import (
    FINAL_ANSWER_TOOL,
    GradeResult,
    JsonDict,
    Task,
    ToolCall,
    ToolTraceEvent,
    final_answer_from_trace,
)
from workspace_bench.workspace.default_setup import apply_workspace_baseline
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
        max_turns_override: int | None = None,
    ):
        self.task = task
        self.workspace = workspace or SimulatedWorkspace()
        self.trace: list[ToolTraceEvent] = []
        # The turn budget is enforced here, never shown to the agent: the
        # agent envelope excludes limits so agents always aim for the fastest
        # outcome instead of pacing themselves against a known budget.
        self.max_turns = (
            max_turns_override
            if max_turns_override is not None
            else int(task.limits.get("max_turns", 0) or 0)
        )
        fixtures, initial_state = apply_workspace_baseline(
            task.suite,
            task.fixtures,
            task.initial_state,
            baseline_override=task.workspace_baseline,
            backends_override=task.workspace_backends,
        )
        # Skills are an explicit axis: a task (or its suite manifest) must
        # declare workspace_skills to have any loaded — no hidden default.
        skills = (
            task.workspace_skills
            if task.workspace_skills is not None
            else (task.suite.workspace_skills if task.suite else None)
        )
        if skills is None:
            skills = ()
        self.workspace.reset(
            backends=fixtures,
            initial_state=initial_state,
            runtime_checks=task.success.runtime,
            skills=skills,
        )
        self.initial_snapshot = self.workspace.snapshot()

    def step(self, call: ToolCall) -> JsonDict:
        """Execute one tool call and append it to the episode trace."""

        if self.max_turns and len(self.trace) >= self.max_turns:
            return {
                "ok": False,
                "command": call.name,
                "error": "turn_budget_exhausted",
                "message": "The episode's turn budget is exhausted; the call was not executed.",
            }
        if self.answered:
            return {
                "ok": False,
                "command": call.name,
                "error": "episode_completed",
                "message": "A final answer was already submitted; the episode is complete.",
            }
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

    @property
    def answered(self) -> bool:
        """Whether a final answer has been submitted."""

        return final_answer_from_trace(tuple(self.trace)) is not None

    @property
    def final_answer(self) -> str | None:
        """The submitted final answer, if any."""

        return final_answer_from_trace(tuple(self.trace))

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
        if call.name == FINAL_ANSWER_TOOL:
            # Harness-level answer action: recorded, never dispatched to the
            # workspace, and it completes the episode.
            text = call.args.get("text")
            if not isinstance(text, str) or not text.strip():
                return {
                    "ok": False,
                    "command": call.name,
                    "request_id": None,
                    "message": "final_answer requires non-empty text.",
                    "data": None,
                    "error": {
                        "code": "invalid_request",
                        "message": "final_answer requires non-empty text.",
                        "retryable": True,
                    },
                }
            return {
                "ok": True,
                "command": call.name,
                "request_id": None,
                "message": "Final answer recorded; the episode is complete.",
                "data": None,
            }
        return self.workspace.call_tool(call)
