# RL-Factory Adapter Notes

RL-Factory can use Workspace Bench as a task environment once the rollout loop speaks the same tool-call protocol as the runner.

## Environment Mapping

Workspace Bench conceptually maps to an RL-Factory environment like this:

| RL concept | Workspace Bench object |
| --- | --- |
| prompt | `Task.prompt` plus tool instructions |
| observation | latest tool result or Workspace snapshot |
| action | model-emitted Workspace MCP tool call or final answer |
| transition | `workspace.call_tool(...)` |
| done | final answer, max turns, or terminal tool policy |
| reward | `grade_task(...)` final score plus optional trace rewards |

## Sparse Final Reward

Start with a sparse final reward:

```python
from workspace_bench.rl.env import WorkspaceGymEnv

env = WorkspaceGymEnv(task=task)
observation, info = env.reset()

for action in rollout_actions:
    observation, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        break
```

This is robust because it uses deterministic state checks instead of judging prose.

For fixed policy traces or smoke tests, the helper in `workspace_bench.rl` can
collect transition records:

```python
from workspace_bench.rl import collect_rollout

transitions = collect_rollout(
    env,
    [{"tool": "get_workspace_snapshot", "args": {}}],
    seed=1,
)
```

## Process Rewards

Once sparse reward works, trace checks can become process rewards:

- valid tool schema
- no invented widget ids
- `get_widget_schema` before `create_widget`
- limited invalid calls
- no redundant snapshots
- correct use of `widget_uuid` for layout-sensitive tasks

These process rewards are directly available from the trace and do not require an LLM judge.

`WorkspaceGymEnv` exposes the first set of configurable process rewards:

```python
env = WorkspaceGymEnv(
    task=task,
    process_rewards=True,
    valid_tool_reward=0.01,
    invalid_tool_penalty=-0.25,
    schema_before_create_reward=0.1,
    repeated_snapshot_penalty=-0.05,
)
```

The final reward still comes from the deterministic grader. Process rewards are
additive shaping signals for rollout suite and can be disabled entirely.

The RL package is split by responsibility: `actions.py` normalizes JSON actions,
`observations.py` builds observations, `rewards.py` holds process-reward logic,
and `env.py` wires those pieces into `WorkspaceGymEnv`.

## Tool Configuration

For the simulator, a lightweight adapter can expose the same tools in-process. For a real Workspace sidecar, RL-Factory should connect to streamable HTTP MCP:

```json
[
  {
    "mcpServers": {
      "workspace": {
        "type": "streamable-http",
        "url": "http://127.0.0.1:8787/mcp"
      }
    }
  }
]
```

The real sidecar path needs a bench control plane to reset browser state and register fixture backends. Those reset controls should not be part of the model-visible toolset.

## Recommended Build Order

1. Run the bundled oracle traces against the simulator.
2. Add an RL-Factory environment wrapper that executes tool calls against `SimulatedWorkspace`.
3. Train/evaluate on a small task subset.
4. Add a real `workspace-mcp` adapter.
5. Compare simulator and real-sidecar grades on the same oracle traces.
6. Scale only after reset isolation and fixture backend lifecycle are reliable.

## Open Questions

- How should final answers be represented for agents that stop without creating an artifact?
- Should real Workspace browser sessions be pooled or created per task?
- Which trace checks should be process rewards versus hard failures?
- How much layout quality should be rewarded beyond no overlap and grid bounds?
