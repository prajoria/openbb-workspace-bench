# Contributing

Workspace Bench tasks should be deterministic, state-graded, and useful for evaluating agents that compose OpenBB Workspace artifacts through MCP-like tools.

## Add a Scenario

1. Copy an existing JSON file in `src/workspace_bench/scenarios`.
2. Give it a stable `id`, `title`, `level`, `category`, `difficulty`, `tags`, and `source`.
3. Keep fixture data deterministic. Do not add live API dependencies to bundled scenarios.
4. Define success criteria against final Workspace state, not prose alone.
5. Add an `oracle_tool_calls` trace that passes the grader.
6. Run:

```bash
uv run --extra dev workspace-bench validate --min-scenarios 25
uv run --extra dev pytest
```

## Scenario Review Checklist

- The no-op baseline fails.
- The oracle trace passes.
- The task cannot pass by only preserving initial state.
- Required widgets use exact `origin` and `widget_id`.
- Layout checks are enabled when the task creates or moves widgets.
- Repair/delete tasks use `max_count` where duplicates or stale widgets matter.
- The prompt is realistic for a financial analyst workflow.
- Tags are specific enough for filtering.

## Add Fixture Data

Fixture data lives in `src/workspace_bench/fixtures.py`. Prefer small, readable tables with stable dates and values. If a widget has parameters, expose realistic parameter options so schema/option discovery remains meaningful.

## Add a Grader

Add deterministic graders before adding LLM judges. Good graders inspect:

- dashboard composition
- widget identity and configuration
- generated artifact content
- layout bounds and overlaps
- trace behavior

## Release Checks

Before opening a release PR:

```bash
uv run --extra dev pytest
uv run --extra dev workspace-bench validate --min-scenarios 25
uv run --extra dev workspace-bench run --agent oracle --json
uv run --extra dev workspace-bench report --output docs/benchmark-report.md
```
