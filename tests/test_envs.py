from __future__ import annotations

from workspace_bench.rl.env import WorkspaceGymEnv
from workspace_bench.rl import action_to_tool_call, collect_rollout, is_done_action
from workspace_bench.core.runner import find_task


def test_workspace_gym_env_reset_returns_task_observation() -> None:
    task = find_task("price_performance_aapl")
    env = WorkspaceGymEnv(task=task)

    observation, info = env.reset(seed=1)

    assert info["task_id"] == "price_performance_aapl"
    assert observation["task"]["id"] == "price_performance_aapl"
    assert observation["turn_index"] == 0
    assert observation["remaining_turns"] == task.limits["max_turns"]
    assert "create_widget" in observation["allowed_tools"]


def test_workspace_gym_env_oracle_actions_terminate_with_final_reward() -> None:
    task = find_task("price_performance_aapl")
    env = WorkspaceGymEnv(task=task)
    env.reset(seed=1)

    terminated = False
    truncated = False
    reward = 0.0
    info = {}
    for call in task.oracle_tool_calls:
        _, reward, terminated, truncated, info = env.step(
            {"tool": call.name, "args": call.args}
        )
        if terminated or truncated:
            break

    assert terminated is True
    assert truncated is False
    assert reward == 1.0
    assert info["grade"]["passed"] is True


def test_workspace_gym_env_done_action_terminates_with_current_score() -> None:
    task = find_task("price_performance_aapl")
    env = WorkspaceGymEnv(task=task)
    env.reset(seed=1)

    _, reward, terminated, truncated, info = env.step({"done": True})

    assert terminated is True
    assert truncated is False
    assert reward == info["grade"]["score"]
    assert info["done_reason"] == "agent_done"


def test_workspace_gym_env_invalid_actions_can_receive_process_penalty() -> None:
    task = find_task("price_performance_aapl")
    env = WorkspaceGymEnv(
        task=task,
        process_rewards=True,
        invalid_tool_penalty=-0.25,
    )
    env.reset(seed=1)

    _, reward, terminated, truncated, info = env.step({"tool": "manage_apps"})

    assert reward == -0.25
    assert terminated is False
    assert truncated is False
    assert info["tool_result"]["ok"] is False


def test_workspace_gym_env_rewards_schema_before_create() -> None:
    task = find_task("price_performance_msft")
    env = WorkspaceGymEnv(
        task=task,
        process_rewards=True,
        schema_before_create_reward=0.4,
    )
    env.reset(seed=1)

    calls = {call.name: call for call in task.oracle_tool_calls}
    env.step(
        {
            "tool": "list_available_widgets",
            "args": calls["list_available_widgets"].args,
        }
    )
    env.step(
        {
            "tool": "get_widget_schema",
            "args": calls["get_widget_schema"].args,
        }
    )
    _, reward, _, _, info = env.step(
        {
            "tool": "create_widget",
            "args": calls["create_widget"].args,
        }
    )

    assert info["process_reward"] == 0.4
    assert reward >= 0.4


def test_workspace_gym_env_penalizes_repeated_snapshots() -> None:
    task = find_task("price_performance_aapl")
    env = WorkspaceGymEnv(
        task=task,
        process_rewards=True,
        repeated_snapshot_penalty=-0.3,
    )
    env.reset(seed=1)

    env.step({"tool": "get_workspace_snapshot", "args": {}})
    _, reward, terminated, truncated, info = env.step(
        {"tool": "get_workspace_snapshot", "args": {}}
    )

    assert reward == -0.3
    assert info["process_reward"] == -0.3
    assert terminated is False
    assert truncated is False


def test_rl_action_helpers_normalize_done_and_tool_calls() -> None:
    assert is_done_action({"tool": "finish"}) is True

    call = action_to_tool_call({"tool": "get_workspace_snapshot", "args": {}})

    assert call.name == "get_workspace_snapshot"
    assert call.args == {}


def test_collect_rollout_records_fixed_action_sequence() -> None:
    task = find_task("price_performance_aapl")
    env = WorkspaceGymEnv(task=task)

    transitions = collect_rollout(
        env,
        [{"tool": "get_workspace_snapshot", "args": {}}],
        seed=1,
    )

    assert len(transitions) == 1
    assert transitions[0]["action"]["tool"] == "get_workspace_snapshot"
    assert transitions[0]["reward"] == 0.0
    assert transitions[0]["terminated"] is False
