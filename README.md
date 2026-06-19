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

## What This Is Not

- It is not a full model-training framework.
- It is not a public leaderboard yet.
- It is not live-market-data financial reasoning by default.
- It is not a real browser-backed Workspace runner by default.

Training, RL, and live Workspace execution are downstream paths that reuse the
same benchmark core.

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
uv run --extra dev workspace-bench compare-models \
  --difficulty all \
  --timeout 240
```

Compare only one difficulty slice:

```bash
uv run --extra dev workspace-bench compare-models \
  --difficulty easy \
  --timeout 240
```

Run repeated attempts for a more stable comparison:

```bash
uv run --extra dev workspace-bench compare-models \
  --difficulty all \
  --repeats 3 \
  --metric pass-at-k \
  --timeout 240
```

Run models from a JSON adapter config:

```bash
uv run --extra dev workspace-bench compare-models \
  --models-file examples/models.example.json \
  --difficulty all \
  --timeout 240
```

The comparison runner prints `[PASS]` or `[FAIL]` after each scenario and writes
raw JSON results plus `comparison.json`, `analysis.md`, `chart.svg`, and
`chart.png` into a timestamped directory under `runs/comparison/`.
`analysis.md` separates grader/task issues from provider or process failures.
PASS/FAIL status is colorized on normal terminals; use `--color always` or
`--color never` to force a behavior.

By default, the comparison runner is interactive: each model chooses one tool
call, receives the simulated Workspace result, then chooses the next call. Each
scenario run directory includes `conversation.json`, `model_responses.jsonl`,
and `tool_calls.jsonl`. Use `--runner batch` to compare against the older
single-shot JSONL adapter behavior. Transient model API failures such as HTTP
520 are retried by default; tune this with `--model-retries` and
`--retry-backoff`.

Use `--scenario-dir` to compare models against a private task pack, and
`--split dev|validation|test|train` to select a release slice.

Export a task envelope without running an agent:

```bash
uv run workspace-bench export-task \
  --scenario l1_add_price_widget \
  --output task.json
```

Export rollouts or SFT data explicitly:

```bash
uv run --extra dev workspace-bench export-rollouts \
  --oracle \
  --scenario l1_add_price_widget \
  --output runs/exports/oracle-rollouts.jsonl

uv run --extra dev workspace-bench export-sft \
  --oracle \
  --scenario l1_add_price_widget \
  --format openai_messages \
  --output runs/exports/oracle-sft.jsonl
```

You can also export from a `compare-models` output directory with
`--comparison-dir runs/comparison/<run-id>`. SFT export includes only passing
attempts by default; add `--include-failures` to keep failed attempts with grade
metadata.

See [docs/agent-command.md](docs/agent-command.md) for the external-agent contract and [docs/result-schema.md](docs/result-schema.md) for result JSON.
See [docs/training-recipes.md](docs/training-recipes.md) for SFT, preference, and RL rollout export patterns.
For a visual walkthrough of how the repo fits together, open [docs/repo-explainer.html](docs/repo-explainer.html).

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
See [docs/contributing.md](docs/contributing.md) for scenario, grader, agent, export, and RL contribution paths.

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
  cli.py                 Command line interface
  core/                  Scenario dataclasses, bundled tasks, episodes, runner, graders
  workspace/             Fixture backends, simulator, live workspace-mcp smoke bridge
  agents/                Oracle/noop agents, JSONL command protocol, model adapter helpers
  reports/               Model comparison, reliability metrics, charts, analysis reports
  exports/               Rollout, SFT, preference, and metadata export helpers
  rl/                    Gym-style env, action/observation/reward helpers
  *.py                   Backward-compatible public import wrappers
docs/
  agent-command.md
  architecture.md
  benchmark-card.md
  benchmark-report.md
  contributing.md
  launch-readiness.md
  publishing.md
  private-task-packs.md
  result-schema.md
  rl-factory-adapter.md
  scenario-format.md
  training-recipes.md
  terminal-bench-lessons.md
examples/
  jsonl_rule_agent.py       Repo-checkout wrapper for the packaged demo agent
  ollama_agent.py           Local Ollama adapter template
  openai_gpt4_1.py          GPT-4.1 OpenAI API adapter template
  compare_models.py         Interactive multi-model runner and chart generator
  models.example.json       Model comparison adapter config example
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
`WorkspaceGymEnv` exposes these as optional additive shaping rewards, disabled by default.

Minimal Gym-style usage:

```python
from workspace_bench.envs import WorkspaceGymEnv

env = WorkspaceGymEnv()
observation, info = env.reset(seed=1)
observation, reward, terminated, truncated, info = env.step(
    {"tool": "get_workspace_snapshot", "args": {}}
)
```

## Release Notes

This is an alpha benchmark package. It is ready for local evals, private task packs, CI regression testing, and `workspace-mcp` sidecar smoke tests. Before a broader public leaderboard, add more real model baselines, hidden/generated scenario splits, and a browser-backed real Workspace runner.
