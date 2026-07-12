# Published Runs

This directory is the benchmark's evidence: every number in the README boards
is recomputable from the artifacts here, and every episode is replayable
because the simulator is deterministic.

## Layout

- `comparison/` — twelve published runs: `core-<model>` and `build-<model>`
  for six models. Each run directory holds the per-model result JSON,
  `comparison.json`, `analysis.md`, charts, and one folder per task with the
  full `conversation.json`, raw `model_responses.jsonl`, executed
  `tool_calls.jsonl`, the task envelope handed to the harness, and
  `run_meta.json`.
- `exports/` — the 1,800 core episodes as portable rollout JSONL
  (`workspace-bench-rollout-v1`), rebuilt by replaying each run's recorded
  tool calls through the simulator and re-grading.
- `reports/` — compiled views: `calibration.json` (core per-level/per-family
  detail), `suites.json` (per-suite and pooled boards),
  `significance.json` (Wilson intervals, held-out slices, pairwise McNemar
  tests), `benchmark-report.md` (oracle/no-op release report), plus the
  generated task catalog and Workspace MCP tool-coverage matrix.

## Provenance

- Runs were executed in early July 2026 and published on 2026-07-10.
- One clean end-to-end attempt per model per suite (`repeats=1`), interactive
  runner, temperature 0, transient-failure retries 2, task-defined turn
  budgets (no `--max-turns` override). No result was patched or spliced;
  provider/process failures are committed as failures.
- Provider endpoints: the OpenAI API (GPT-5.5, gpt-4.1-mini), OpenRouter's
  OpenAI-compatible endpoint (Claude Sonnet 5, GLM-5.2), and a local Ollama
  server (gpt-oss:20b, Qwen3 8B). Per-adapter environment (base URLs and
  structured-output opt-outs) was supplied through a local models file that
  is not committed; these runs predate the harness's `run_metadata` capture,
  so their result files do not record provider-reported model fingerprints.
  Runs made with the current harness record effective settings, timestamps,
  the harness git commit, and the provider-reported model identity.
- The current regraded build board uses GPT-5.1, GPT-5.4 mini, and GPT-5.5;
  all three are replayed against the fixed current grader.

## Split provenance

Split assignments were rebalanced on 2026-07-11 to 150/75/75 (`core`) and
118/59/59 (`build-openbb-apps`) so that every family/level cell contributes
one validation and one test task. Task ids, prompts, rubrics, and oracle
traces were untouched, so all published outcomes remain valid. Artifacts
inside `comparison/` record the split assignment that existed at run time;
the shipped suite is canonical for split-sliced analysis — join per-task
outcomes on task id, as `scripts/reports/compute_significance.py` does for the
held-out slices in `reports/significance.json`.

## Re-verifying

```bash
# replay + re-grade every core episode into fresh rollout JSONL
uv run workspace-bench export-rollouts \
  --comparison-dir runs/comparison/core-gpt-4.1-mini \
  --output /tmp/mini-rollouts.jsonl

# recompute the compiled reports from the committed run directories
uv run python scripts/reports/compile_calibration.py
uv run python scripts/reports/compute_significance.py
```

The exports in `exports/` were rebuilt this way on 2026-07-11; the replayed
strict pass counts match the published boards exactly for all six models.
