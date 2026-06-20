from __future__ import annotations

from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import ToolCall
from workspace_bench.core.runner import find_scenario


def test_episode_step_api_supports_incremental_tool_execution() -> None:
    scenario = find_scenario("l1_add_price_widget")
    episode = WorkspaceEpisode(scenario)

    for call in scenario.oracle_tool_calls:
        result = episode.step(call)
        assert result["command"] == call.name

    grade = episode.grade()
    assert grade.passed is True
    assert len(episode.trace) == len(scenario.oracle_tool_calls)


def test_episode_records_disallowed_tool_as_invalid_step() -> None:
    scenario = find_scenario("l1_add_price_widget")
    episode = WorkspaceEpisode(scenario)

    result = episode.step(ToolCall("manage_apps", {"operation": "list"}))

    assert result["ok"] is False
    assert episode.trace[0].ok is False
    assert episode.grade().passed is False

