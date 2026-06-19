# OpenBB Workspace Bench

OpenBB Workspace Bench is a Terminal-Bench-style evaluation harness for agents that operate inside composable financial workspaces through OpenBB Workspace MCP tools.

The benchmark asks a simple question: can an agent inspect, build, update, and repair durable Workspace state? Scoring is based on final dashboard/app state, widget configuration, generated artifacts, layout, and tool-use discipline.

Current release: `workspace-core-v0` alpha.

## What Is Included

- 25 deterministic scenarios across L0-L4
- equities, macro, and portfolio fixture domains
- simulator-backed Workspace MCP runtime for fast local evals
- live `workspace-mcp` sidecar smoke runner
- public task envelope export
- external agent command contract
- private scenario directory support
- oracle and no-op baselines
- state and trace graders
- release report generation

The simulator is intentional. It makes evals fast, deterministic, and suitable for CI or RL rollouts. The live smoke runner exercises the real `workspace-mcp` HTTP and websocket bridge path against the same scenario contract.

## Quick Start

Install dependencies and inspect the benchmark:

```bash
uv run --extra dev workspace-bench list
uv run --extra dev workspace-bench manifest --json
uv run --extra dev workspace-bench validate --min-scenarios 25
```

Run built-in baselines:

```bash
uv run --extra dev workspace-bench run --agent oracle
uv run --extra dev workspace-bench run --agent noop
uv run --extra dev workspace-bench report --output docs/benchmark-report.md
```

Run tests:

```bash
uv run --extra dev pytest
```

## Evaluate Your Agent

Workspace Bench can evaluate any external process that writes tool calls as JSON Lines.

Run the included demo agent:

```bash
uv run --extra dev workspace-bench run-agent-command \
  --scenario l1_add_price_widget \
  --agent-command "python -m workspace_bench.examples.jsonl_rule_agent" \
  --json
```

The harness writes a task envelope JSON file, sets environment variables for the agent command, reads the agent's emitted `tool_calls.jsonl`, executes those calls in the Workspace simulator, and grades the final state.

Run a local Ollama model:

```bash
OLLAMA_MODEL=gpt-oss:20b \
uv run --extra dev workspace-bench run-agent-command \
  --scenario l1_add_price_widget \
  --agent-command "python examples/ollama_agent.py" \
  --run-dir runs/ollama \
  --json
```

The Ollama adapter writes `ollama_prompt.txt`, `ollama_response.txt`, and `tool_calls.jsonl` inside the scenario run directory so you can debug what the model saw and emitted.

Run GPT-4.1 through the OpenAI API:

```bash
cp .env.example .env
# edit .env and set OPENAI_API_KEY

uv run --extra dev workspace-bench run-agent-command \
  --scenario l1_add_price_widget \
  --agent-command "python examples/openai_gpt4_1.py" \
  --run-dir runs/openai-gpt-4.1 \
  --json
```

The OpenAI adapter writes `openai_prompt.txt`, `openai_response.txt`, and `tool_calls.jsonl` inside the scenario run directory.

Compare two models over all bundled scenarios with the interactive runner:

```bash
uv run --extra dev python examples/compare_models.py \
  --difficulty all \
  --timeout 240
```

Compare only one difficulty slice:

```bash
uv run --extra dev python examples/compare_models.py \
  --difficulty easy \
  --timeout 240
```

Run repeated attempts for a more stable comparison:

```bash
uv run --extra dev python examples/compare_models.py \
  --difficulty all \
  --repeats 3 \
  --metric task-pass-rate \
  --timeout 240
```

The comparison runner prints `[PASS]` or `[FAIL]` after each scenario and writes
raw JSON results plus `comparison.json`, `analysis.md`, `chart.svg`, and
`chart.png` into a timestamped directory under `runs/comparison/`.
PASS/FAIL status is colorized on normal terminals; use `--color always` or
`--color never` to force a behavior.

By default, the comparison runner is interactive: each model chooses one tool
call, receives the simulated Workspace result, then chooses the next call. Each
scenario run directory includes `conversation.json`, `model_responses.jsonl`,
and `tool_calls.jsonl`. Use `--runner batch` to compare against the older
single-shot JSONL adapter behavior. Transient model API failures such as HTTP
520 are retried by default; tune this with `--model-retries` and
`--retry-backoff`.

Export a task envelope without running an agent:

```bash
uv run workspace-bench export-task \
  --scenario l1_add_price_widget \
  --output task.json
```

See [docs/agent-command.md](docs/agent-command.md) for the external-agent contract and [docs/result-schema.md](docs/result-schema.md) for result JSON.

## Private Task Packs

Evaluate private scenarios from a directory:

```bash
uv run --extra dev workspace-bench validate --scenario-dir ./my-workspace-tasks
uv run --extra dev workspace-bench run-agent-command \
  --scenario-dir ./my-workspace-tasks \
  --agent-command "python my_agent.py" \
  --json
```

Private task packs use the same scenario schema as the bundled benchmark. This is the main BYO-data path: teams can point scenarios at deterministic internal Workspace backends and keep graders local.

See [docs/private-task-packs.md](docs/private-task-packs.md).

## Live Workspace MCP Smoke

Start a local `workspace-mcp` sidecar:

```bash
workspace-mcp --cors-allow https://pro.openbb.dev
```

Then smoke-test the real MCP endpoint and browser bridge protocol:

```bash
uv run --extra live workspace-bench smoke-workspace-mcp \
  --url http://127.0.0.1:8787 \
  --scenario l1_add_price_widget \
  --json
```

The smoke command emulates the browser bridge with the benchmark simulator. It exercises the real streamable HTTP endpoint, tool schemas, server-side validation, websocket bridge, command translation layer, and session-context updates without requiring a Workspace browser tab. If a real browser is already connected, the command refuses to replace it unless `--replace-browser-session` is passed.

## Serve Fixture Backends

Serve a deterministic fixture as a Workspace backend:

```bash
uv run workspace-bench serve-fixture --backend equities --port 9101
```

The server exposes:

- `GET /widgets.json`
- `GET /apps.json`
- widget data endpoints such as `/price-performance?symbol=AAPL&raw=true`

## Scenario Shape

Each scenario defines:

- analyst prompt
- fixture backends
- optional initial Workspace state
- allowed tools and limits
- deterministic success criteria
- oracle trace
- metadata for slicing and reporting

The agent acts through Workspace MCP-like tools such as:

- `get_workspace_snapshot`
- `manage_dashboard`
- `manage_navigation_bar`
- `navigate_workspace`
- `list_available_widgets`
- `get_widget_schema`
- `get_params_options`
- `get_widget_data`
- `create_widget`
- `update_widget`
- `update_widget_layout`
- `delete_widget`
- `add_generative_widget`
- `read_widget`
- `manage_backends`
- `manage_apps`

The grader evaluates final Workspace state first. Text-only answers are secondary; the durable artifact is the dashboard/app state the agent produced.

See [docs/scenario-format.md](docs/scenario-format.md).

See [docs/benchmark-card.md](docs/benchmark-card.md) for the `workspace-core-v0` benchmark card, scope, and limitations.
See [docs/publishing.md](docs/publishing.md) for release and publishing gates.

## Task Levels

- `L0`: inspect and answer from an existing dashboard
- `L1`: create, update, read, or lay out a single widget
- `L2`: build a multi-widget dashboard from analyst requirements
- `L3`: use app templates, tabs, parameter groups, and prompts
- `L4`: repair incorrect Workspace state or bad metadata assumptions
- `L5`: multi-agent delegation and skill workflows, reserved for later

## Repository Layout

```text
src/workspace_bench/
  agent_command.py       External agent command adapter
  agents.py              Oracle and no-op agents
  cli.py                 Command line interface
  fixtures.py            Deterministic fixture backends and HTTP server
  graders.py             State and trace graders
  live_mcp.py            Live workspace-mcp smoke bridge
  models.py              Scenario and result dataclasses
  runner.py              Scenario loading and execution
  simulated_workspace.py Workspace MCP simulator
  scenarios/*.json       Bundled workspace-core-v0 scenarios
docs/
  agent-command.md
  architecture.md
  benchmark-card.md
  benchmark-report.md
  launch-readiness.md
  publishing.md
  private-task-packs.md
  result-schema.md
  rl-factory-adapter.md
  scenario-format.md
  terminal-bench-lessons.md
examples/
  jsonl_rule_agent.py       Repo-checkout wrapper for the packaged demo agent
  ollama_agent.py           Local Ollama adapter template
  openai_gpt4_1.py          GPT-4.1 OpenAI API adapter template
  compare_models.py         Interactive multi-model runner and chart generator
tests/
```

## Contamination Canary

```bash
uv run workspace-bench canary
```

Benchmark data should not appear in model training corpora unless explicitly released for training.

## RL Path

RL is a downstream consumer of the benchmark, not the primary identity. The same scenario, step, trace, and grader contracts can be wrapped by RL-Factory or a Gym-style environment:

1. load a scenario
2. reset a simulated or real Workspace environment
3. expose Workspace MCP tools to the rollout model
4. execute tool calls through the environment
5. compute reward with the same grader used by evaluation

The first reward should be sparse final-state correctness. Process rewards can then reuse trace checks: schema-before-create, valid identifiers, no repeated snapshots, and limited invalid calls.

## Release Notes

This is an alpha benchmark package. It is ready for local evals, private task packs, CI regression testing, and `workspace-mcp` sidecar smoke tests. Before a broader public leaderboard, add more real model baselines, hidden/generated scenario splits, and a browser-backed real Workspace runner.
