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
    "total": 25,
    "passed": 25,
    "failed": 0,
    "mean_score": 1.0,
    "by_level": {
      "L1": { "passed": 8, "total": 8 }
    }
  },
  "results": []
}
```

Each result includes:

- scenario id
- level, category, difficulty, tags
- numeric score
- pass/fail
- checks passed and total
- issue list

## External Agent Runs

```bash
uv run --extra dev workspace-bench run-agent-command \
  --scenario l1_add_price_widget \
  --agent-command "python -m workspace_bench.examples.jsonl_rule_agent" \
  --json
```

Top-level shape:

```json
{
  "benchmark": {
    "name": "openbb-workspace-bench",
    "version": "0.1.0",
    "release_id": "workspace-core-v0"
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

`passed` is true only when the process succeeds and the scenario grader passes.

## Trace Artifacts

Use `--trace-dir` to write per-scenario trace artifacts:

```bash
uv run --extra dev workspace-bench run-agent-command \
  --scenario l1_add_price_widget \
  --agent-command "python -m workspace_bench.examples.jsonl_rule_agent" \
  --trace-dir traces
```

Each trace artifact includes:

- scenario metadata and prompt
- grade object
- ordered tool calls
- tool results
- final Workspace snapshot

Trace artifacts are the best debugging input when a benchmark run regresses.
