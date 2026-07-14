# Runs

Committed evidence and local artifact output for the benchmark.

## Tracked

- `reports/` — compiled views and generated references: `calibration.json`
  (core per-level/per-family detail), `suites.json` (per-suite and pooled
  boards), `significance.json` (Wilson intervals, held-out slices, pairwise
  McNemar tests), `benchmark-report.md` / `build-apps-benchmark-report.md`
  (oracle/no-op release reports), plus the generated `task-catalog.md`,
  `tool-coverage-matrix.md`, and `tool-matrix-data.json`.
- `hosted-surface/` — pinned snapshots of the hosted Workspace MCP surface
  (tool schemas, resource catalog, widget types) used by
  `scripts/audits/audit_hosted_surface.py` and the backend-building tests.

## Local (untracked)

- `comparison/` — model-comparison runs land here (one directory per run with
  per-model results, `comparison.json`, `analysis.md`, and charts). The raw
  July 2026 published runs are not committed; the compiled boards in
  `reports/` are the retained evidence.
- `live-parity/` — per-task `parity.json` from `workspace-bench live-parity`
  against the hosted Workspace MCP bridge.
- `browser-cert/` — screenshots, traces, and verdicts from
  `workspace-bench browser-cert`.

## Provenance of the compiled boards

- The published model runs were executed in early July 2026 (`repeats=1`
  core, `repeats=2` build calibration), interactive runner, temperature 0,
  task-defined turn budgets. No result was patched or spliced;
  provider/process failures are committed as failures.
- The regraded build board uses GPT-5.1, GPT-5.4 mini, and GPT-5.5, replayed
  against the fixed grader (`resumed_cells=472`, `new_cells=0` per model).
- Split assignments were rebalanced on 2026-07-11 to 150/75/75 (`core`) and
  118/59/59 (`build-openbb-apps`) so every family/level cell contributes one
  validation and one test task; task ids, prompts, rubrics, and oracle traces
  were untouched, so the published outcomes remain valid. Join per-task
  outcomes on task id for split-sliced analysis.
- Boards compiled before the 2026-07-12 task-schema and grading reset are not
  comparable with runs made against the current suites; recomputing any board
  requires re-running the models, not just re-compiling.
