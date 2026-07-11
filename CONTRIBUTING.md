# Contributing

WorkspaceBench contributions should keep the repo benchmark-first: tasks,
workspace state, tool traces, grading, exports, and RL adapters should all reuse
the same core contracts.

The detailed contribution guide lives in
[docs/contributing.md](docs/contributing.md).

## Quick Checks

Run these before opening a change:

```bash
uv run --extra dev ruff check src tests scripts examples
uv run --extra dev mypy src/workspace_bench
uv run --extra dev pytest
uv run workspace-bench validate --suite core --min-tasks 300
uv run workspace-bench validate --suite build-openbb-apps --min-tasks 212
```

For evaluator changes, also run:

```bash
uv run workspace-bench \
  --models-file examples/models.example.json \
  --difficulty easy \
  --dry-run
```

## Main Contribution Paths

- Add tasks under `src/workspace_bench/core/task_suites/` (bundled suites) or a
  private `--task-dir` directory.
- Add deterministic grader checks under `workspace_bench.core.graders`.
- Add external agents through the JSONL command protocol first.
- Add export formats under `workspace_bench.exports`.
- Add RL behavior as an adapter over `WorkspaceEpisode`, not as duplicate
  simulator or grader logic.
