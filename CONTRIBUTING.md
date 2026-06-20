# Contributing

WorkspaceBench contributions should keep the repo benchmark-first: scenarios,
workspace state, tool traces, grading, exports, and RL adapters should all reuse
the same core contracts.

The detailed contribution guide lives in
[docs/contributing.md](docs/contributing.md).

## Quick Checks

Run these before opening a change:

```bash
uv run --extra dev python -m pytest
uv run --extra dev workspace-bench validate --min-scenarios 25
```

For comparison-runner changes, also run:

```bash
uv run --extra dev workspace-bench compare-models \
  --models-file examples/models.example.json \
  --difficulty easy \
  --dry-run
```

## Main Contribution Paths

- Add scenarios under `src/workspace_bench/core/scenarios`.
- Add deterministic grader checks under `workspace_bench.core.graders`.
- Add external agents through the JSONL command protocol first.
- Add export formats under `workspace_bench.exports`.
- Add RL behavior as an adapter over `WorkspaceEpisode`, not as duplicate
  simulator or grader logic.

