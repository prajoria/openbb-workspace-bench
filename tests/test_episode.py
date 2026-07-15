from __future__ import annotations

from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import ToolCall
from workspace_bench.core.runner import find_task


def test_episode_step_api_supports_incremental_tool_execution() -> None:
    task = find_task("decision_briefing_level0")
    episode = WorkspaceEpisode(task)

    for call in task.oracle_tool_calls:
        result = episode.step(call)
        assert result["command"] == call.name

    grade = episode.grade()
    assert grade.passed is True
    assert len(episode.trace) == len(task.oracle_tool_calls)


def test_episode_records_disallowed_tool_as_invalid_step() -> None:
    task = find_task("decision_briefing_level0")
    episode = WorkspaceEpisode(task)

    result = episode.step(ToolCall("manage_apps", {"operation": "list"}))

    assert result["ok"] is False
    assert episode.trace[0].ok is False
    assert episode.grade().passed is False


def test_episode_enforces_the_turn_budget_without_exposing_it() -> None:
    task = find_task("smoke_get_workspace_snapshot_level0")
    episode = WorkspaceEpisode(task)

    first = episode.step(ToolCall(name="get_workspace_snapshot", args={}))
    assert first["ok"] is True

    refused = episode.step(ToolCall(name="get_workspace_snapshot", args={}))
    assert refused["ok"] is False
    assert refused["error"] == "turn_budget_exhausted"
    # The refused call is not recorded or executed.
    assert len(episode.trace) == 1
    assert episode.grade().passed is True

    # An explicit override lifts the cap for interactive harness loops.
    episode = WorkspaceEpisode(task, max_turns_override=3)
    for _ in range(3):
        assert episode.step(ToolCall(name="get_workspace_snapshot", args={}))["ok"]
    assert episode.step(ToolCall(name="get_workspace_snapshot", args={}))["ok"] is False


def test_final_answer_is_harness_level_and_completes_the_episode() -> None:
    from dataclasses import replace

    task = find_task("cio_investment_committee_pack_p1_x", suite="enterprise-apps-default")
    task = replace(task, allowed_tools=(*task.allowed_tools, "final_answer"))
    episode = WorkspaceEpisode(task)

    empty = episode.step(ToolCall(name="final_answer", args={"text": "  "}))
    assert empty["ok"] is False

    result = episode.step(ToolCall(name="final_answer", args={"text": "Answer."}))
    assert result["ok"] is True
    assert episode.answered
    assert episode.final_answer == "Answer."

    refused = episode.step(ToolCall(name="get_workspace_snapshot", args={}))
    assert refused["ok"] is False
    assert refused["error"] == "episode_completed"
    # The workspace never saw the answer: no generated widget exists.
    composition = episode.snapshot()["dashboard_composition"]
    assert not [w for w in composition.get("widgets", []) if w.get("generated")]


def test_final_answer_requires_allowlisting() -> None:
    task = find_task("smoke_get_workspace_snapshot_level0")
    episode = WorkspaceEpisode(task)

    result = episode.step(ToolCall(name="final_answer", args={"text": "hi"}))
    assert result["ok"] is False
    assert "not allowed" in result["message"]
