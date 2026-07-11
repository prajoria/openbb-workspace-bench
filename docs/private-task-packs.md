# Private Task Packs

Workspace Bench is designed to be useful both as a public benchmark and as a private evaluation harness. A private task pack is a directory of scenario JSON files using the same schema as the bundled `workspace-bench-v1` pack.

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
uv run workspace-bench validate --scenario-dir ./my-workspace-tasks
uv run workspace-bench run --scenario-dir ./my-workspace-tasks --agent oracle
uv run workspace-bench run-agent-command \
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

## From Pack to Collection

A private pack becomes a **collection** the moment you report it as one. Three steps:

```bash
# 1. certify it the same way the bundled collections are certified:
#    the reference solution must pass, a do-nothing agent must fail
uv run workspace-bench validate --scenario-dir ./my-workspace-tasks

# 2. run your models over it (one run directory per model)
uv run workspace-bench compare-models \
  --models-file models.json --scenario-dir ./my-workspace-tasks \
  --output-dir runs/comparison/mydesk-gpt-4.1-mini

# 3. pool it with the bundled collections — the name before '=' is yours
uv run python scripts/compile_collections_report.py \
  --run core=runs/comparison/core-gpt-4.1-mini \
  --run build-openbb-apps=runs/comparison/build-gpt-4.1-mini \
  --run my-desk-flows=runs/comparison/mydesk-gpt-4.1-mini \
  --output runs/reports/collections.json
```

The report keeps every collection separable (a model's score on *your* flows is
its own number) and pools scenario counts into the aggregate. Models that have
not run a collection are marked pending there and excluded from its pool, so
adding a collection never distorts existing ones.

## Building Rules

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
