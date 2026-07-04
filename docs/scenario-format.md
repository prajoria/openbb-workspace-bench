# Scenario Format

Scenarios are JSON files bundled under `src/workspace_bench/core/scenario_packs`.

The bundled `workspace-bench-v1` pack uses this same format as private task
packs loaded through `--scenario-dir`.

## Minimal Shape

```json
{
  "id": "gen_t0_create_price_performance_aapl",
  "title": "Add a Price Performance Widget",
  "level": "L1",
  "capability": "widget-creation",
  "workflow": "equity-tearsheet",
  "domain": "finance",
  "subdomain": "equity-research",
  "difficulty": "easy",
  "tags": ["schema-discovery", "equities", "layout"],
  "source": "workspace-bench",
  "novelty": "Unique create/t0 exercise using schema discovery for AAPL price performance.",
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

Metadata splits general Workspace usability from business workflow context:

| Field | Required | Notes |
| --- | --- | --- |
| `id` | Yes | Stable scenario id. |
| `title` | Yes | Human-readable task name. |
| `level` | Yes | Capability tier such as `L0`, `L1`, or `L2`. |
| `capability` | Yes | General agent/workspace skill, e.g. `dashboard-construction`, `widget-creation`, or `skill-access`. |
| `workflow` | Yes | Real business task, e.g. `earnings-prep`, `portfolio-morning-review`, or `client-meeting-prep`. |
| `domain` | Yes | Broad domain such as `finance` or `workspace-usability`. |
| `subdomain` | Yes | Narrower area such as `equity-research`, `risk`, `execution`, or `client-ir`. |
| `difficulty` | Yes | One of `easy`, `medium`, `hard`. |
| `split` | Optional | One of `dev`, `validation`, `test`, or `train`. Defaults to the task pack default, then `dev`. |
| `tags` | Yes | Non-empty list for filtering and benchmark cards. |
| `source` | Recommended | Provenance for task authorship or dataset origin. |
| `novelty` | Optional | One-line uniqueness note used by catalogs and release checks. Defaults to empty. |

`workspace-bench validate` checks metadata, oracle traces, and no-op baseline strength.

## Public Task Envelope

`workspace-bench export-task` converts a scenario into the public payload shown to an evaluated external agent:

```bash
uv run workspace-bench export-task \
  --scenario gen_t0_create_price_performance_aapl \
  --output task.json
```

The task envelope includes prompt, metadata, fixtures, initial state, allowed tools, limits, and the JSONL tool-call protocol. It excludes `success` and `oracle_tool_calls`.

## Built-In Packs

Use `--pack` to select bundled scenarios:

- `core`: backward-compatible alias for the unified `workspace-bench-v1` pack.
- `all`: backward-compatible alias for the same unified pack.

## Fixtures

`fixtures.backends[].name` accepts either the fixture slug or display name:

- `equities` or `Bench Equities`
- `macro` or `Bench Macro`
- `portfolio` or `Bench Portfolio`
- `stark-enterprise` or `Bench Stark Enterprise`

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

### Required Tool Calls

Use this when the behavior itself matters, for example MCP skill access or
agent delegation:

```json
{
  "tool": "get_skill_content",
  "args_contains": { "slug": "finance-earnings-prep" },
  "min_count": 1
}
```

`args_contains` is a nested subset match against the trace call args.

### Required Tool Results

Use this when the agent must retrieve specific information through a tool:

```json
{
  "tool": "get_skill_content",
  "data_contains": ["Earnings prep workflow", "surprise drivers"]
}
```

The grader string-matches against the serialized tool result.

### Required Resource Reads

Use this when the agent must retrieve an MCP resource through the
`read_workspace_resource` tool:

```json
{
  "uri": "openbb://workspace/app-builder/index",
  "data_contains": ["Workspace app builder index", "template_id"]
}
```

Resource read checks match successful `read_workspace_resource` trace events by
exact URI, then string-match against the serialized tool result using the same
contains semantics as required tool results.

### Workspace Prompts And Resources

Scenarios may include these retrieval tools in `allowed_tools`:

- `read_workspace_resource` with `{"uri": "openbb://workspace/app-builder/index"}` or `{"uri": "openbb://workspace/skills/<slug>"}`.
- `get_workspace_prompt` with `{"name": "workspace_tool_usage"}` or `{"name": "workspace_session_context"}`.

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
