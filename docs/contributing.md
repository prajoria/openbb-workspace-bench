# Contributing To WorkspaceBench

WorkspaceBench should stay benchmark-first. Contributions should preserve the
same scenario, simulator, trace, and grader contracts used by the CLI, exports,
and RL adapter.

## Add A Scenario

1. Copy an existing scenario from `src/workspace_bench/core/scenario_packs/workspace_bench_v1` or create one in a private scenario directory.
2. Give it a stable `id`, title, level, capability, workflow, domain, subdomain, difficulty, split, and tags.
3. Keep fixture data deterministic.
4. Add clear `success` criteria that grade durable Workspace state.
5. Add an `oracle_tool_calls` trace.
6. Run:

```bash
uv run --extra dev workspace-bench validate --pack all --min-scenarios 300
```

For private scenarios, put JSON files in a separate directory and use
`--scenario-dir`.

## Add A Grader Check

1. Add the check to `workspace_bench.core.graders`.
2. Return a stable issue code that can be used in reports.
3. Keep strict pass/fail separate from partial score.
4. Add a focused unit test in `tests/test_graders.py`.
5. Confirm oracle still passes and noop still fails.

Current trace-oriented issue codes include `missing_tool_call`,
`missing_tool_result`, `missing_resource_read`, `too_many_invalid_calls`,
`schema_not_called_before_create`, `unlisted_widget_id`, and
`repeated_snapshots`.

## Add An Agent Adapter

Prefer the external JSONL command protocol first:

```bash
uv run --extra dev workspace-bench run-agent-command \
  --scenario gen_t0_create_price_performance_aapl \
  --agent-command "python my_agent.py" \
  --json
```

Your adapter should read:

- `WORKSPACE_BENCH_TASK_JSON`
- `WORKSPACE_BENCH_OUTPUT_JSONL`
- `WORKSPACE_BENCH_RUN_DIR`
- `WORKSPACE_BENCH_SCENARIO_ID`

It should write one JSON object per line to `WORKSPACE_BENCH_OUTPUT_JSONL`.

For model-comparison adapters, add a JSON entry to a `--models-file` config
rather than changing the built-in defaults.

## Add An Export Format

1. Keep canonical rollout records unchanged.
2. Add conversion logic under `workspace_bench.exports`.
3. Preserve benchmark release, export schema, scenario, and task-pack metadata.
4. Add tests in `tests/test_exports.py`.
5. Document the new format in `docs/result-schema.md` or
   `docs/training-recipes.md`.

## Add RL Behavior

Keep RL code as an adapter over the benchmark core:

- actions in `workspace_bench.rl.actions`
- observations in `workspace_bench.rl.observations`
- rewards in `workspace_bench.rl.rewards`
- rollout helpers in `workspace_bench.rl.rollouts`
- environment wiring in `workspace_bench.rl.env`

Do not duplicate simulator or grader logic inside the RL package.

## Required Checks

Run before submitting:

```bash
uv run --extra dev python -m pytest
uv run --extra dev workspace-bench validate --pack all --min-scenarios 300
```

For comparison-runner changes, also run:

```bash
uv run --extra dev workspace-bench compare-models \
  --models-file examples/models.example.json \
  --difficulty easy \
  --dry-run
```
