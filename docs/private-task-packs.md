# Private Task Packs

Workspace Bench is designed to be useful both as a public benchmark and as a private evaluation harness. A private task pack is a directory of scenario JSON files using the same schema as the bundled `workspace-core-v0` and `stark-enterprise-v0` packs.

## Directory Shape

```text
my-workspace-tasks/
  task_pack.json
  portfolio_rebalance_note.json
  earnings_dashboard_repair.json
  macro_rates_briefing.json
```

Run the pack:

```bash
uv run --extra dev workspace-bench validate --scenario-dir ./my-workspace-tasks
uv run --extra dev workspace-bench run --scenario-dir ./my-workspace-tasks --agent oracle
uv run --extra dev workspace-bench run-agent-command \
  --scenario-dir ./my-workspace-tasks \
  --agent-command "python my_agent.py" \
  --json
```

## Custom Data

Bundled scenarios use deterministic in-package fixture backends. Private packs can use the same fixture names or point fixtures at URLs that represent internal Workspace backends:

```json
{
  "fixtures": {
    "backends": [
      {
        "name": "Bench Equities",
        "backend_id": "backend_001",
        "url": "http://127.0.0.1:9101"
      }
    ]
  }
}
```

For public benchmark submissions, keep data deterministic and versioned. For private regression testing, the same scenario format can wrap proprietary backend data as long as the grader expectations are stable.

## Authoring Rules

Good private tasks should:

- model a real analyst workflow
- require tool use, not only final prose
- include deterministic fixture data
- grade durable Workspace state
- fail the no-op baseline
- include an oracle trace for regression testing
- use `max_count` checks for repair/delete tasks
- avoid live market data unless the task is explicitly non-reproducible

## Public vs Private Fields

When an agent is evaluated with `run-agent-command`, it receives a public task envelope. The envelope excludes:

- `success`
- `oracle_tool_calls`
- hidden grader logic

This keeps the agent-facing prompt and metadata separate from the evaluator-facing answer key.

## Hidden Packs

Add `task_pack.json` when a pack needs release metadata or redaction behavior:

```json
{
  "pack_id": "internal-workspace-tasks",
  "release_id": "internal-workspace-tasks-v1",
  "version": "1.0.0",
  "visibility": "hidden",
  "default_split": "validation"
}
```

For `visibility: "hidden"`, manifests and reports mark the pack as redacted.
Trace artifacts written with `--trace-dir` keep scenario ids, scores, tool
calls, tool results, and final snapshots, but omit the scenario prompt.
