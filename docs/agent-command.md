# External Agent Command

Workspace Bench can evaluate any agent process that can write Workspace tool calls as JSON Lines. This is the first BYO-agent contract. It is simple enough for CI and private baselines, while still using the same task reset, simulator, traces, and graders as the built-in oracle/no-op agents.

## Run The Demo Agent

```bash
uv run workspace-bench run-agent-command \
  --task gen_t0_create_price_performance_aapl \
  --agent-command "python -m workspace_bench.examples.jsonl_rule_agent" \
  --json
```

The command should pass `gen_t0_create_price_performance_aapl`. The demo is not a model agent; it is a tiny script that demonstrates the protocol.

## Run A Local Ollama Agent

Start Ollama separately if it is not already running:

```bash
ollama serve
```

Then run the provided adapter with your local model:

```bash
OLLAMA_MODEL=gpt-oss:20b \
uv run workspace-bench run-agent-command \
  --task gen_t0_create_price_performance_aapl \
  --agent-command "python examples/ollama_agent.py" \
  --run-dir runs/ollama \
  --json
```

The adapter uses `http://127.0.0.1:11434` by default. Override it with:

```bash
OLLAMA_BASE_URL=http://127.0.0.1:11434
```

For each task, the adapter saves:

- `task.json`
- `ollama_prompt.txt`
- `ollama_response.txt`
- `tool_calls.jsonl`

This makes failures easy to inspect without touching the benchmark internals.

## Run GPT-4.1 Through The OpenAI API

Create a local `.env` file:

```bash
cp .env.example .env
```

Then edit `.env`:

```bash
OPENAI_API_KEY=sk-your-key-here
```

Run one task:

```bash
uv run workspace-bench run-agent-command \
  --task gen_t0_create_price_performance_aapl \
  --agent-command "python examples/openai_gpt4_1.py" \
  --run-dir runs/openai-gpt-4.1 \
  --json
```

The adapter is hardcoded to `gpt-4.1`. It reads `OPENAI_API_KEY` from the
environment first, then `.env`. It writes `openai_prompt.txt`,
`openai_response.txt`, and `tool_calls.jsonl` inside the task run directory.

## Compare Model Runs With A Bar Chart

Run both built-in model adapters across all tasks with the interactive
comparison runner:

```bash
uv run workspace-bench \
  --difficulty all \
  --timeout 240
```

Run one difficulty slice:

```bash
uv run workspace-bench \
  --difficulty medium \
  --timeout 240
```

Change the chart metric from pass rate to mean score:

```bash
uv run workspace-bench \
  --difficulty all \
  --metric mean-score \
  --timeout 240
```

Run repeated attempts and chart task pass rate:

```bash
uv run workspace-bench \
  --difficulty all \
  --repeats 3 \
  --metric task-pass-rate \
  --timeout 240
```

Run a configured set of adapters:

```bash
uv run workspace-bench \
  --models-file examples/models.example.json \
  --difficulty all \
  --timeout 240
```

The config file shape is:

```json
{
  "models": [
    {
      "slug": "local-openai-compatible",
      "label": "Local OpenAI Compatible",
      "provider": "openai",
      "model": "local-model",
      "command": "python my_agent.py",
      "env": {
        "OPENAI_BASE_URL": "http://127.0.0.1:8000/v1"
      }
    }
  ]
}
```

The comparison runner writes:

- per-model raw JSON result files
- `comparison.json`
- `analysis.md`
- `chart.svg`
- `chart.png`

It prints `[PASS]` or `[FAIL]` after each task finishes. By default, outputs
go into a timestamped directory under `runs/comparison/`; pass `--output-dir` if
you want a fixed location. Full comparisons will make OpenAI API calls for each
selected task. Use `--dry-run` first to see which tasks will run.
The summary reports strict pass rate, task pass rate, task failures, and
process failures separately. Strict pass rate counts provider/process failures
as failed attempts. Task pass rate excludes provider/process failures and asks
whether valid attempts satisfied the grader.

The comparison runner defaults to `--runner interactive`. In that mode the
model chooses one Workspace tool call, receives the real simulated tool result,
then chooses the next call. Each task directory includes `conversation.json`,
`model_responses.jsonl`, and `tool_calls.jsonl`. Use `--runner batch` when you
want the older one-shot JSONL adapter behavior. Transient model API failures
such as HTTP 520 are retried by default; tune retries with `--model-retries`
and `--retry-backoff`.

## Contract

For every task, the harness:

1. creates an isolated run directory
2. writes `task.json`
3. sets environment variables for the agent command
4. runs the command
5. reads `tool_calls.jsonl`
6. executes those calls in the Workspace simulator
7. grades the final state and trace

Environment variables:

| Variable | Meaning |
| --- | --- |
| `WORKSPACE_BENCH_TASK_JSON` | Absolute path to the task envelope JSON. |
| `WORKSPACE_BENCH_OUTPUT_JSONL` | Absolute path where the agent must write tool calls. |
| `WORKSPACE_BENCH_RUN_DIR` | Absolute path to the task run directory. |
| `WORKSPACE_BENCH_TASK_ID` | Task id being evaluated. |

The command runs from the caller's current working directory. Use `WORKSPACE_BENCH_RUN_DIR` for per-run scratch files and `WORKSPACE_BENCH_OUTPUT_JSONL` for the evaluated tool-call output.

Output format:

```jsonl
{"tool":"get_workspace_snapshot","args":{}}
{"tool":"list_available_widgets","args":{"origin":"Bench Equities"}}
{"tool":"create_widget","args":{"origin":"Bench Equities","widget_id":"price_performance","data_args":{"symbol":"AAPL"}}}
```

The harness also accepts a JSON array of tool call objects, but JSONL is preferred for streaming agents.

## Task Envelope

Export one task without running an agent:

```bash
uv run workspace-bench export-task \
  --task gen_t0_create_price_performance_aapl \
  --output task.json
```

The envelope includes:

- benchmark name, version, release id, and canary
- task id, prompt, level, capability, workflow, domain, subdomain, difficulty, tags
- fixture backend references
- initial Workspace state
- allowed tools
- limits
- the JSONL output protocol

`allowed_tools` uses Workspace MCP-style tool names. Retrieval-only tools may
include `read_workspace_resource` with `{"uri": "openbb://workspace/app-builder/index"}`
or `{"uri": "openbb://workspace/skills/<slug>"}`, and `get_workspace_prompt`
with `{"name": "workspace_tool_usage"}` or `{"name": "workspace_session_context"}`.

It intentionally does not include success criteria or oracle tool calls. Those remain grader-side data.

## Private Agents

Use `--task-dir` to evaluate an agent over a private task suite:

```bash
uv run workspace-bench run-agent-command \
  --task-dir ./my-workspace-tasks \
  --agent-command "python my_agent.py" \
  --json
```

Use `--run-dir` if you want deterministic output paths:

```bash
uv run workspace-bench run-agent-command \
  --task gen_t0_create_price_performance_aapl \
  --agent-command "python my_agent.py" \
  --run-dir runs/my-agent
```

Each task gets a subdirectory under `runs/my-agent`.

## Failure Semantics

A run fails if:

- the agent exits non-zero
- the command times out
- the output cannot be parsed as JSONL or a JSON array
- the emitted tool calls fail the task grader

Malformed output is converted into an invalid trace event so it is visible in the result JSON.

## Current Limitation

`run-agent-command` evaluates trace-producing agents. The agent does not receive
interactive observations after each tool call from that command alone. For
interactive local model evaluation, use `workspace-bench`, which
is backed by `WorkspaceEpisode.step` and shares the same tasks and graders.
