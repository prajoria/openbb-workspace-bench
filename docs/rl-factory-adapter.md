# RL-Factory Adapter Notes

RL-Factory can use Workspace Bench as a task environment once the rollout loop speaks the same tool-call protocol as the runner.

## Environment Mapping

Workspace Bench conceptually maps to an RL-Factory environment like this:

| RL concept | Workspace Bench object |
| --- | --- |
| prompt | `Scenario.prompt` plus tool instructions |
| observation | latest tool result or Workspace snapshot |
| action | model-emitted Workspace MCP tool call or final answer |
| transition | `workspace.call_tool(...)` |
| done | final answer, max turns, or terminal tool policy |
| reward | `grade_scenario(...)` final score plus optional trace rewards |

## Sparse Final Reward

Start with a sparse final reward:

```python
from workspace_bench.episode import WorkspaceEpisode
from workspace_bench.models import ToolCall

episode = WorkspaceEpisode(scenario)

for action in rollout_actions:
    observation = episode.step(ToolCall(action.name, action.args))

reward = episode.grade().score
```

This is robust because it uses deterministic state checks instead of judging prose.

## Process Rewards

Once sparse reward works, trace checks can become process rewards:

- valid tool schema
- no invented widget ids
- `get_widget_schema` before `create_widget`
- limited invalid calls
- no redundant snapshots
- correct use of `widget_uuid` for layout-sensitive tasks

These process rewards are directly available from the trace and do not require an LLM judge.

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
3. Train/evaluate on a small scenario subset.
4. Add a real `workspace-mcp` adapter.
5. Compare simulator and real-sidecar grades on the same oracle traces.
6. Scale only after reset isolation and fixture backend lifecycle are reliable.

## Open Questions

- How should final answers be represented for agents that stop without creating an artifact?
- Should real Workspace browser sessions be pooled or created per scenario?
- Which trace checks should be process rewards versus hard failures?
- How much layout quality should be rewarded beyond no overlap and grid bounds?
