# Scenario Format

Scenarios are JSON files bundled under `src/workspace_bench/core/scenarios`.

The bundled `workspace-core-v0` release uses this same format as private task packs loaded through `--scenario-dir`.

## Minimal Shape

```json
{
  "id": "l1_add_price_widget",
  "title": "Add a Price Performance Widget",
  "level": "L1",
  "category": "widget-creation",
  "difficulty": "easy",
  "tags": ["schema-discovery", "equities", "layout"],
  "source": "workspace-bench",
  "prompt": "Add a price performance widget for AAPL to the active dashboard.",
  "fixtures": {
    "backends": [{ "name": "equities" }]
  },
  "initial_state": {},
  "allowed_tools": ["list_available_widgets", "get_widget_schema", "create_widget"],
  "success": {
    "required_widgets": [
      {
        "origin": "Bench Equities",
        "widget_id": "price_performance",
        "data_args": { "symbol": "AAPL" }
      }
    ],
    "trace_checks": {
      "max_invalid_tool_calls": 0,
      "must_call_schema_before_create": true
    }
  },
  "oracle_tool_calls": [
    {
      "tool": "list_available_widgets",
      "args": { "origin": "Bench Equities" }
    }
  ],
  "limits": { "max_turns": 8 }
}
```

## Metadata

Metadata follows the same practical shape that makes Terminal-Bench tasks easy to browse and slice:

| Field | Required | Notes |
| --- | --- | --- |
| `id` | Yes | Stable scenario id. |
| `title` | Yes | Human-readable task name. |
| `level` | Yes | Capability tier such as `L0`, `L1`, or `L2`. |
| `category` | Yes | Broad task family, e.g. `dashboard-construction`. |
| `difficulty` | Yes | One of `easy`, `medium`, `hard`. |
| `split` | Optional | One of `dev`, `validation`, `test`, or `train`. Defaults to the task pack default, then `dev`. |
| `tags` | Yes | Non-empty list for filtering and benchmark cards. |
| `source` | Recommended | Provenance for task authorship or dataset origin. |

`workspace-bench validate` checks metadata, oracle traces, and no-op baseline strength.

## Public Task Envelope

`workspace-bench export-task` converts a scenario into the public payload shown to an evaluated external agent:

```bash
uv run workspace-bench export-task \
  --scenario l1_add_price_widget \
  --output task.json
```

The task envelope includes prompt, metadata, fixtures, initial state, allowed tools, limits, and the JSONL tool-call protocol. It excludes `success` and `oracle_tool_calls`.

## Fixtures

`fixtures.backends[].name` accepts either the fixture slug or display name:

- `equities` or `Bench Equities`
- `macro` or `Bench Macro`
- `portfolio` or `Bench Portfolio`

The simulator assigns backend ids in registration order: `backend_001`, `backend_002`, and so on.

## Initial State

Use `initial_state.dashboard` to seed a dashboard:

```json
{
  "dashboard": {
    "name": "Existing AAPL Review",
    "activate": true,
    "tabs": [{ "id": "overview", "name": "Overview" }],
    "widgets": [
      {
        "origin": "Bench Equities",
        "widget_id": "price_performance",
        "data_args": { "symbol": "AAPL" },
        "tab_id": "overview",
        "layout": { "x": 0, "y": 2, "w": 20, "h": 12 }
      }
    ],
    "generated_widgets": [
      {
        "widget_type": "note",
        "name": "Seed Note",
        "data": "Existing note body.",
        "tab_id": "overview"
      }
    ]
  }
}
```

## Success Criteria

### Required Tabs

```json
"required_tabs": ["overview", "estimates"]
```

Tabs are checked by `tab_id`, not display name.

### Required Widgets

```json
{
  "origin": "Bench Equities",
  "widget_id": "latest_news",
  "data_args": { "symbol": "AAPL", "limit": 5 },
  "tab_id": "overview",
  "min_count": 1,
  "max_count": 1
}
```

`data_args` is a subset match. A widget may have additional args, but the expected keys must match exactly.

### Required Generated Widgets

```json
{
  "widget_type": "note",
  "name_contains": "Takeaways",
  "data_contains": ["AAPL", "EPS", "revenue"],
  "tab_id": "overview"
}
```

`data_contains` is case-insensitive over the generated data serialized as JSON.

### Required Layouts

```json
{
  "widget_id": "price_performance",
  "tab_id": "charts",
  "x": 0,
  "y": 2,
  "w": 20,
  "h": 12
}
```

Use `widget_uuid` when a scenario has multiple instances with the same `widget_id`.

### Layout Checks

```json
"layout": {
  "within_grid": true,
  "no_overlaps": true,
  "grid_width": 40
}
```

The grid width defaults to 40 columns, matching Workspace guidance.

### Trace Checks

```json
"trace_checks": {
  "max_invalid_tool_calls": 0,
  "must_call_schema_before_create": true,
  "forbid_invented_widget_ids": true,
  "max_repeated_snapshots": 1
}
```

Trace checks are useful process rewards for RL:

- `must_call_schema_before_create` rewards schema discovery before mutation.
- `forbid_invented_widget_ids` requires listed widget ids before schema/create calls.
- `max_repeated_snapshots` discourages redundant state inspection.

## Oracle Tool Calls

Oracle traces are reference trajectories, not the only valid solution. They serve three purposes:

- smoke-test scenario correctness
- produce bootstrap trajectories for SFT/RL
- document the intended tool path for benchmark authors

The grader remains the source of truth.

## Private Task Packs

Run a directory of scenario files:

```bash
uv run --extra dev workspace-bench validate --scenario-dir ./my-workspace-tasks
uv run --extra dev workspace-bench run --scenario-dir ./my-workspace-tasks --agent oracle
```

Use `--scenario-file` when iterating on one local scenario.

A scenario directory can include a `task_pack.json` manifest:

```json
{
  "pack_id": "my-workspace-tasks",
  "release_id": "my-workspace-tasks-v1",
  "version": "1.0.0",
  "visibility": "private",
  "default_split": "validation",
  "description": "Internal Workspace tasks for model selection."
}
```

`default_split` is applied to scenario files that do not set `split` directly.
Use `workspace-bench list --scenario-dir ./my-workspace-tasks --split validation`
or `workspace-bench compare-models --scenario-dir ./my-workspace-tasks --split validation`
to run a specific slice.
