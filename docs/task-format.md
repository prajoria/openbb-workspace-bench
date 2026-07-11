# Task Format

Tasks are JSON files bundled under `src/workspace_bench/core/task_suites`.

The bundled suites use this same format as private task suites loaded
through `--task-dir`.

## Minimal Shape

```json
{
  "id": "gen_t0_create_price_performance_aapl",
  "title": "Add a Price Performance Widget",
  "category": "single-widget",
  "level": "t1",
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
| `id` | Yes | Stable task id. |
| `title` | Yes | Human-readable task name. |
| `category` | Yes | Workflow kind: `read`, `single-widget`, `dashboard`, `platform`, or `repair`. |
| `level` | Yes | Difficulty level `t0`–`t4` (the `t` label is kept stable in ids and tags). |
| `capability` | Yes | General agent/workspace skill, e.g. `dashboard-construction`, `widget-creation`, or `skill-access`. |
| `workflow` | Yes | Real business task, e.g. `earnings-prep`, `portfolio-morning-review`, or `client-meeting-prep`. |
| `domain` | Yes | Broad domain such as `finance` or `workspace-usability`. |
| `subdomain` | Yes | Narrower area such as `equity-research`, `risk`, `execution`, or `client-ir`. |
| `difficulty` | Yes | One of `easy`, `medium`, `hard`. |
| `split` | Optional | One of `dev`, `validation`, `test`, or `train`. Defaults to the task suite default, then `dev`. |
| `tags` | Yes | Non-empty list for filtering and benchmark cards. |
| `source` | Recommended | Provenance for task authorship or dataset origin. |
| `novelty` | Optional | One-line uniqueness note used by catalogs and release checks. Defaults to empty. |

`workspace-bench validate` checks metadata, oracle traces, and no-op baseline strength.

## Public Task Envelope

`workspace-bench export-task` converts a task into the public payload shown to an evaluated external agent:

```bash
uv run workspace-bench export-task \
  --task gen_t0_create_price_performance_aapl \
  --output task.json
```

The task envelope includes prompt, metadata, fixtures, initial state, allowed tools, limits, and the JSONL tool-call protocol. It excludes `success` and `oracle_tool_calls`.

## Built-In Suites

Use `--suite` to select bundled tasks:

- `core`: the `workspace-bench-v1` operating suite (300 tasks).
- `build-openbb-apps`: the `workspace-bench-v2-build-openbb-apps` app-building
  suite (212 tasks).

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

Tasks may include these retrieval tools in `allowed_tools`:

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

Use `widget_uuid` when a task has multiple instances with the same `widget_id`.

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

- smoke-test task correctness
- produce bootstrap trajectories for SFT/RL
- document the intended tool path for benchmark authors

The grader remains the source of truth.

## Private Task Suites

Run a directory of task files:

```bash
uv run --extra dev workspace-bench validate --task-dir ./my-workspace-tasks
uv run --extra dev workspace-bench run --task-dir ./my-workspace-tasks --agent oracle
```

Use `--task-file` when iterating on one local task.

A task directory can include a `task_suite.json` manifest:

```json
{
  "suite_id": "my-workspace-tasks",
  "release_id": "my-workspace-tasks-v1",
  "version": "1.0.0",
  "visibility": "private",
  "default_split": "validation",
  "description": "Internal Workspace tasks for model selection."
}
```

`default_split` is applied to task files that do not set `split` directly.
Use `workspace-bench list --task-dir ./my-workspace-tasks --split validation`
or `workspace-bench --task-dir ./my-workspace-tasks --split validation`
to run a specific slice.
