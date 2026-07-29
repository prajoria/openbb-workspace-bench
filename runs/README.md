# Runs

Committed evidence and local artifact output for the benchmark.

## Tracked

- `reports/` — compiled views and generated references:
  - `workspace-tasks-board.json` — the sealed workspace-tasks model board
    (pooled reference row plus single-pass rows, with exclusions and their
    reasons recorded in place), compiled by
    `scripts/audits/compile_workspace_tasks_board.py`.
  - `workspace-tasks-calibration.json` / `workspace-tasks-calibration.md` —
    the per-persona reference-model calibration ledger and its pooled
    staircase, written by `scripts/audits/calibrate_workspace_tasks.py`.
  - `benchmark-report.md` — the deterministic oracle/no-op certification
    report for the workspace-tasks taskset.
  - `task-catalog.md`, `tool-coverage-matrix.md`, `tool-matrix-data.json` —
    generated references covering all three tasksets.
- `hosted-surface/` — pinned snapshots of the hosted Workspace MCP surface
  (tool schemas, resource catalog, widget types) used by
  `scripts/audits/audit_hosted_surface.py` and the backend-building tests.

## Local (untracked)

- `comparison/` — model-comparison runs land here (one directory per run with
  per-model results, `comparison.json`, `analysis.md`, and charts). Raw run
  directories are never committed; the compiled boards in `reports/` are the
  retained evidence.
- `live-parity/` — per-task `parity.json` from `workspace-bench live-parity`
  against the hosted Workspace MCP bridge.
- `browser-cert/` — screenshots, traces, and verdicts from
  `workspace-bench browser-cert`.

## Provenance of the compiled boards

- The workspace-tasks board pools the reference model's three calibration
  repeats and records every other model as a single sealed pass (closed-world,
  temperature 0, task-defined turn budgets). No result was patched or
  spliced; excluded rows stay in the record with their exclusion reasons.
- Recomputing any board requires re-running the models against the current
  tasksets, not just re-compiling.
