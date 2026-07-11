# Private Task Suites

Workspace Bench is designed to be useful both as a public benchmark and as a private evaluation harness. A private task suite is a directory of task JSON files using the same schema as the bundled `workspace-bench-v1` pack.

## Directory Shape

```text
my-workspace-tasks/
  task_suite.json
  portfolio_rebalance_note.json
  earnings_dashboard_repair.json
  macro_rates_briefing.json
```

Run the pack:

```bash
uv run workspace-bench validate --task-dir ./my-workspace-tasks
uv run workspace-bench run --task-dir ./my-workspace-tasks --agent oracle
uv run workspace-bench run-agent-command \
  --task-dir ./my-workspace-tasks \
  --agent-command "python my_agent.py" \
  --json
```

## Custom Data

Bundled tasks use deterministic in-package fixture backends. Private packs can use the same fixture names or point fixtures at URLs that represent internal Workspace backends:

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

For public benchmark submissions, keep data deterministic and versioned. For private regression testing, the same task format can wrap proprietary backend data as long as the grader expectations are stable.

## From Pack to Suite

A private pack becomes a **suite** the moment you report it as one. Three steps:

```bash
# 1. certify it the same way the bundled suites are certified:
#    the reference solution must pass, a do-nothing agent must fail
uv run workspace-bench validate --task-dir ./my-workspace-tasks

# 2. run your models over it (one run directory per model)
uv run workspace-bench \
  --models-file models.json --task-dir ./my-workspace-tasks \
  --output-dir runs/comparison/mydesk-gpt-4.1-mini

# 3. pool it with the bundled suites — the name before '=' is yours
uv run python scripts/compile_suites_report.py \
  --run core=runs/comparison/core-gpt-4.1-mini \
  --run build-openbb-apps=runs/comparison/build-gpt-4.1-mini \
  --run my-desk-flows=runs/comparison/mydesk-gpt-4.1-mini \
  --output runs/reports/suites.json
```

The report keeps every suite separable (a model's score on *your* flows is
its own number) and pools task counts into the aggregate. Models that have
not run a suite are marked pending there and excluded from its pool, so
adding a suite never distorts existing ones.

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

Add `task_suite.json` when a pack needs release metadata or redaction behavior:

```json
{
  "suite_id": "internal-workspace-tasks",
  "release_id": "internal-workspace-tasks-v1",
  "version": "1.0.0",
  "visibility": "hidden",
  "default_split": "validation"
}
```

For `visibility: "hidden"`, manifests and reports mark the pack as redacted.
Trace artifacts written with `--trace-dir` keep task ids, scores, tool
calls, tool results, and final snapshots, but omit the task prompt.
