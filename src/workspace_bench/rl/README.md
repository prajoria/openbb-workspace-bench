# RL

`workspace_bench.rl` exposes the benchmark through a Gym-style interface.

The RL adapter does not replace the benchmark core. It wraps the same task
loader, `WorkspaceEpisode`, simulator, and deterministic grader used by normal
eval runs.

The public environment is `WorkspaceGymEnv`.

Module responsibilities:

- `env.py`: public `WorkspaceGymEnv`.
- `actions.py`: JSON action normalization and done-action detection.
- `observations.py`: observation construction.
- `rewards.py`: optional process reward helpers.
- `rollouts.py`: simple fixed-action rollout collection.

Actions are structured Workspace tool calls:

```python
{"tool": "create_widget", "args": {"origin": "Bench Equities", "widget_id": "price_performance"}}
```

Observations include the task, allowed tools, last tool result, current
workspace snapshot, turn index, and remaining turns.

Reward modes:

- sparse final grade reward
- optional process rewards for useful tool discipline
- optional penalties for invalid or repetitive actions

Keep policy training code outside this package. This package should provide the
environment and rollout primitives that trainers can consume.
