# Result Schema

Workspace Bench emits JSON results intended for local regression runs, private benchmark dashboards, and future leaderboards.

## Built-In Agent Runs

```bash
uv run --extra dev workspace-bench run --agent oracle --json
```

Top-level shape:

```json
{
  "summary": {
    "total": 300,
    "passed": 300,
    "failed": 0,
    "mean_score": 1.0,
    "by_level": {
      "t0": { "passed": 60, "total": 60 }
    }
  },
  "results": []
}
```

Each result includes:

- task id
- category, level, capability, workflow, domain, subdomain, difficulty, tags
- numeric score
- pass/fail
- checks passed and total
- issue list

## External Agent Runs

```bash
uv run --extra dev workspace-bench run-agent-command \
  --task gen_t0_create_price_performance_aapl \
  --agent-command "python -m workspace_bench.examples.jsonl_rule_agent" \
  --json
```

Top-level shape:

```json
{
  "benchmark": {
    "name": "openbb-workspace-bench",
    "version": "1.0.0",
    "release_id": "workspace-bench-v1"
  },
  "summary": {
    "total": 1,
    "passed": 1,
    "failed": 0,
    "mean_score": 1.0,
    "process_failures": 0
  },
  "results": []
}
```

External-agent result rows add:

- `grade_passed`
- `agent_command`
- `agent_exit_code`
- `agent_timed_out`
- `agent_stdout`
- `agent_stderr`
- `run_dir`
- `task_path`
- `output_path`

`passed` is true only when the process succeeds and the task grader passes.

## Evaluator Result Files

Each `workspace-bench --model ...` run writes one result JSON per model into
the run directory, alongside `comparison.json`, `analysis.md`, and charts.
The per-model payload adds, on top of the external-agent row fields:

- `benchmark`, `model`, `filters`, `runner`, `repeats`, `model_retries`
- `run_metadata`: `started_at`/`finished_at` timestamps, `harness`
  (`package_version`, `git_commit`), `settings` (the effective base URLs,
  temperatures, response-format modes, retry/turn budgets, `widget_hints`,
  and `malformed_retries` as they applied inside the adapter's environment),
  and `provider_observed` (the model identifiers and system fingerprints the
  provider actually reported serving)
- `summary` with strict and valid-attempt pass rates, `process_failures`,
  `by_level`, `by_category`, `by_difficulty`, and pass@k/pass^k reliability
  fields when `--repeats` is used

`comparison.json` carries the shared `benchmark`/`harness` blocks, the
selected filters, and one summary entry per model. Runs published before the
`run_metadata` capture do not contain that block.

## Trace Artifacts

Use `--trace-dir` to write per-task trace artifacts:

```bash
uv run --extra dev workspace-bench run-agent-command \
  --task gen_t0_create_price_performance_aapl \
  --agent-command "python -m workspace_bench.examples.jsonl_rule_agent" \
  --trace-dir traces
```

Each trace artifact includes:

- task metadata and prompt
- grade object
- ordered tool calls
- tool results
- final Workspace snapshot

Trace artifacts are the best debugging input when a benchmark run regresses.

## Rollout Export

Use `export-rollouts` to normalize oracle traces, comparison runs, or trace
artifacts into portable JSONL:

```bash
uv run --extra dev workspace-bench export-rollouts \
  --oracle \
  --task gen_t0_create_price_performance_aapl \
  --output rollouts.jsonl
```

Each JSONL row has this shape:

```json
{
  "schema_version": "workspace-bench-rollout-v1",
  "task": {},
  "messages": [],
  "tool_calls": [],
  "tool_results": [],
  "final_snapshot": {},
  "grade": {},
  "metadata": {}
}
```

Each row also includes versioning metadata such as `benchmark_release_id`,
`benchmark_version`, `export_schema_version`, and `exported_at`, plus the
task's `category`, `level`, `difficulty`, and `split`. Private or hidden
task-suite exports include task-suite metadata when a `task_suite.json`
manifest is available.

`export-sft` converts the same rollout records to `openai_messages`,
`sharegpt`, or `tool_call_jsonl`. Passing attempts are exported by default;
use `--include-failures` to include failed attempts with grade metadata.

`export-preferences` reads a repeated evaluator run and emits
`chosen`/`rejected` pairs for attempts on the same model and task.
