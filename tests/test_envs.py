from __future__ import annotations

from workspace_bench.envs import WorkspaceGymEnv
from workspace_bench.runner import find_scenario


def test_workspace_gym_env_reset_returns_task_observation() -> None:
    scenario = find_scenario("l1_add_price_widget")
    env = WorkspaceGymEnv(scenario=scenario)

    observation, info = env.reset(seed=1)

    assert info["scenario_id"] == "l1_add_price_widget"
    assert observation["task"]["id"] == "l1_add_price_widget"
    assert observation["turn_index"] == 0
    assert observation["remaining_turns"] == scenario.limits["max_turns"]
    assert "create_widget" in observation["allowed_tools"]


def test_workspace_gym_env_oracle_actions_terminate_with_final_reward() -> None:
    scenario = find_scenario("l1_add_price_widget")
    env = WorkspaceGymEnv(scenario=scenario)
    env.reset(seed=1)

    terminated = False
    truncated = False
    reward = 0.0
    info = {}
    for call in scenario.oracle_tool_calls:
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
    scenario = find_scenario("l1_add_price_widget")
    env = WorkspaceGymEnv(scenario=scenario)
    env.reset(seed=1)

    _, reward, terminated, truncated, info = env.step({"done": True})

    assert terminated is True
    assert truncated is False
    assert reward == info["grade"]["score"]
    assert info["done_reason"] == "agent_done"


def test_workspace_gym_env_invalid_actions_can_receive_process_penalty() -> None:
    scenario = find_scenario("l1_add_price_widget")
    env = WorkspaceGymEnv(
        scenario=scenario,
        process_rewards=True,
        invalid_tool_penalty=-0.25,
    )
    env.reset(seed=1)

    _, reward, terminated, truncated, info = env.step({"tool": "manage_apps"})

    assert reward == -0.25
    assert terminated is False
    assert truncated is False
    assert info["tool_result"]["ok"] is False
