# OpenBB Workspace Bench

[![CI](https://github.com/DidierRLopes/openbb-workspace-bench/actions/workflows/ci.yml/badge.svg)](https://github.com/DidierRLopes/openbb-workspace-bench/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

OpenBB Workspace Bench is a Terminal-Bench-style evaluation harness for agents that operate inside composable financial workspaces through OpenBB Workspace MCP tools.

The benchmark asks a simple question: can an agent inspect, build, update, and repair durable Workspace state? Scoring is based on final dashboard/app state, widget configuration, generated artifacts, layout, and tool-use discipline.

Motivation: a [NY Tech Week talk](https://youtu.be/7fDTDYh2NJ4?t=1210) showed agents driving real financial work in OpenBB Workspace over MCP, on the [Stark Industries demo](https://github.com/DidierRLopes/stark-industries-demo). A demo shows work can happen once; this benchmark measures how reliably agents actually drive it. The Stark demo is also where the enterprise scenarios come from.

Two collections ship bundled: `core` (operating the workspace, 300 scenarios) and `build-openbb-apps` (building custom backend apps, 212 scenarios). `all` is a backward-compatible CLI alias for `core`.

## What Is Included

- two scenario collections, 512 deterministic scenarios total:
  - `core` — the operating collection: 300 scenarios, 15 tool-anchored families x 5 structural tiers (t0-t4) x 4, stratified 180/60/60 train/validation/test splits
  - `build-openbb-apps` — the app-building collection: 212 scenarios where the agent writes valid `widgets.json` / `apps.json` payloads for custom backends (10 families x t0-t4 x 4 + a 12-scenario e2e capstone)
- generated families covering widgets, apps, prompts, resources, skills, delegation, inspection, repair, layout, and backend/app building
- six committed model baselines with full traces and rollout exports
- equities, macro, portfolio, and Stark enterprise fixture backends
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
uv run workspace-bench list
uv run workspace-bench manifest --json
uv run workspace-bench validate --collection core --min-scenarios 300
uv run workspace-bench validate --collection build-openbb-apps --min-scenarios 212
```

Run built-in baselines:

```bash
uv run workspace-bench run --agent oracle
uv run workspace-bench run --agent noop
uv run workspace-bench report --output runs/reports/benchmark-report.md
```

Run tests:

```bash
uv run --extra dev pytest
```

## Baselines

Six models have been run against both collections (pass@1, single fresh
end-to-end attempt per collection, temperature 0, same grader and turn budget
for every model — no patched or spliced results).

Core collection (operating the workspace, 300 scenarios):

| Model | Strict pass | t0 → t4 pass rate (%) |
|---|---|---|
| GPT-5.5 | 282/300 (94.0%) | 98 · 100 · 90 · 87 · 95 |
| Claude Sonnet 5 | 267/300 (89.0%) | 100 · 98 · 85 · 82 · 80 |
| GLM-5.2 | 229/300 (76.3%) | 85 · 100 · 73 · 60 · 63 |
| gpt-4.1-mini | 211/300 (70.3%) | 98 · 92 · 77 · 52 · 33 |
| gpt-oss:20b | 178/300 (59.3%) | 93 · 68 · 57 · 45 · 33 |
| Qwen3 8B | 149/300 (49.7%) | 80 · 78 · 47 · 27 · 17 |

Full per-scenario results and traces are committed under `runs/comparison/`,
portable rollout JSONL for all 1,800 episodes under `runs/exports/`, and the
compiled report at `runs/reports/calibration.json` (built by
`scripts/compile_calibration.py`).

build-openbb-apps collection (building custom backend apps, 212 scenarios):

| Model | Strict pass | t0 → t4 pass rate (%) |
|---|---|---|
| GPT-5.5 | 212/212 (100.0%) | 100 · 100 · 100 · 100 · 100 |
| GLM-5.2 | 210/212 (99.1%) | 100 · 100 · 100 · 100 · 96 |
| Claude Sonnet 5 | 209/212 (98.6%) | 100 · 98 · 100 · 95 · 100 |
| gpt-4.1-mini | 153/212 (72.2%) | 95 · 90 · 73 · 63 · 48 |
| gpt-oss:20b | 144/212 (67.9%) | 88 · 68 · 83 · 65 · 44 |
| Qwen3 8B | 30/212 (14.2%) | 28 · 20 · 10 · 10 · 6 |

Pooled over all 512 scenarios: GPT-5.5 96.5%, Sonnet 5 93.0%, GLM-5.2 85.7%,
gpt-4.1-mini 71.1%, gpt-oss:20b 62.9%, Qwen3 8B 35.0% — per-collection and
pooled results in `runs/reports/collections.json`.

Repeatability: the gating model repeated 3x over the 300 core scenarios lands
at 71.7 / 70.0 / 70.7% strict per attempt (pass@3 73.7%, pass^3 67.3%), with
only 19/300 scenarios showing within-model variance.

## Evaluate Your Agent

Workspace Bench can evaluate any external process that writes tool calls as JSON Lines.

Run the included demo agent:

```bash
uv run workspace-bench run-agent-command \
  --scenario gen_t0_create_price_performance_aapl \
  --agent-command "python -m workspace_bench.examples.jsonl_rule_agent" \
  --json
```

The harness writes a task envelope JSON file, sets environment variables for the agent command, reads the agent's emitted `tool_calls.jsonl`, executes those calls in the Workspace simulator, and grades the final state.

Run a local Ollama model:

```bash
OLLAMA_MODEL=gpt-oss:20b \
uv run workspace-bench run-agent-command \
  --scenario gen_t0_create_price_performance_aapl \
  --agent-command "python examples/ollama_agent.py" \
  --run-dir runs/ollama \
  --json
```

The Ollama adapter writes `ollama_prompt.txt`, `ollama_response.txt`, and `tool_calls.jsonl` inside the scenario run directory so you can debug what the model saw and emitted.

Run GPT-4.1 through the OpenAI API:

```bash
cp .env.example .env
# edit .env and set OPENAI_API_KEY

uv run workspace-bench run-agent-command \
  --scenario gen_t0_create_price_performance_aapl \
  --agent-command "python examples/openai_gpt4_1.py" \
  --run-dir runs/openai-gpt-4.1 \
  --json
```

The OpenAI adapter writes `openai_prompt.txt`, `openai_response.txt`, and `tool_calls.jsonl` inside the scenario run directory.

Compare two models over all bundled scenarios with the interactive runner:

```bash
uv run workspace-bench compare-models \
  --pack all \
  --difficulty all \
  --timeout 240
```

Compare only one difficulty slice:

```bash
uv run workspace-bench compare-models \
  --pack all \
  --difficulty easy \
  --timeout 240
```

Run repeated attempts for a more stable comparison:

```bash
uv run workspace-bench compare-models \
  --pack all \
  --difficulty all \
  --repeats 3 \
  --metric pass-at-k \
  --timeout 240
```

Run one specific scenario with one specific model — the fastest way to study
what a model actually does on a single task:

```bash
uv run workspace-bench eval \
  --model openai:gpt-4.1-mini \
  --scenario auth_t2_aggrid_revision_grid
```

That's the whole command: `--model provider:model` needs no adapter config
(API keys are read from the environment or `.env`; `ollama:<model>` works the
same for local models), the scenario id is found across the bundled
collections automatically, and the output directory defaults to a timestamped
folder under `runs/comparison/`. The run directory keeps the full
`conversation.json` (every turn: prompt, model actions, tool results),
raw `model_responses.jsonl`, and executed `tool_calls.jsonl` for inspection.
`--scenario` is repeatable, and `--repeats 3` shows whether behavior on a
task is stable.

The scenario's rubric lives next to its prompt in the scenario JSON
(`src/workspace_bench/core/scenario_packs/<collection>/<id>.json`) — the
`success` block is exactly what the grader checks, and `oracle_tool_calls` is
a known-good solution to diff against.

Run models from a JSON adapter config:

```bash
uv run workspace-bench compare-models \
  --models-file examples/models.example.json \
  --pack all \
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

Use `--collection core|build-openbb-apps` for the bundled collections (`--pack`
is a synonym, `all` an alias for `core`), `--scenario-dir`
for a private task pack, and `--split train|validation|test` to select a
release slice. Private packs may also use `dev`. You can also slice with `--capability`, `--workflow`,
`--domain`, and `--subdomain`.

Export a task envelope without running an agent:

```bash
uv run workspace-bench export-task \
  --scenario gen_t0_create_price_performance_aapl \
  --output task.json
```

Export rollouts or SFT data explicitly:

```bash
uv run workspace-bench export-rollouts \
  --oracle \
  --scenario gen_t0_create_price_performance_aapl \
  --output runs/exports/oracle-rollouts.jsonl

uv run workspace-bench export-sft \
  --oracle \
  --scenario gen_t0_create_price_performance_aapl \
  --format openai_messages \
  --output runs/exports/oracle-sft.jsonl
```

You can also export from a `compare-models` output directory with
`--comparison-dir runs/comparison/<run-id>`. SFT export includes only passing
attempts by default; add `--include-failures` to keep failed attempts with grade
metadata.

See [docs/agent-command.md](docs/agent-command.md) for the external-agent contract and [docs/result-schema.md](docs/result-schema.md) for result JSON.
See [docs/training-recipes.md](docs/training-recipes.md) for SFT, preference, and RL rollout export patterns.
See [docs/research-tmax-general-agent.md](docs/research-tmax-general-agent.md) for notes on applying TMax and General Agent-style environment generation to WorkspaceBench.
For a visual walkthrough of how the repo fits together, open [docs/repo-explainer.html](docs/repo-explainer.html).

## Collections

The benchmark is organized as **collections**: certified sets of scenarios that can
be added independently and reported separately or in aggregate. Bundled today:

| collection | scenarios | what it measures |
| --- | --- | --- |
| `core` | 300 | operating the workspace (widgets, dashboards, apps, skills, repair) |
| `build-openbb-apps` | 212 | building for the workspace (writing the `widgets.json` / `apps.json` a backend serves) |

```bash
# run or validate one collection (--pack is an alias of --collection)
uv run workspace-bench validate --collection build-openbb-apps --min-scenarios 212
uv run workspace-bench compare-models --models-file examples/models.example.json --collection build-openbb-apps
```

Every collection has to clear the same gates before it counts: the reference
solution passes every scenario (oracle 100%), a do-nothing agent fails every
scenario (no-op 0%), novelty fingerprints are unique, generation-time quotas hold
(coverage, difficulty bands), graded-check counts stay within per-tier caps (so
strict pass rates track per-check difficulty rather than grading breadth), and a
calibration model's pass rate falls across the tier ladder.

Per-collection results roll up into one pooled aggregate — scenario counts are
added across collections, never averaged percentages. Point the report at one
run directory per model per collection:

```bash
# each compare-models invocation writes one run directory per model
uv run python scripts/compile_collections_report.py \
  --run core=runs/comparison/core-gpt-4.1-mini \
  --run build-openbb-apps=runs/comparison/build-gpt-4.1-mini \
  --output runs/reports/collections.json
```

This is the extension path: a firm can add a private collection built from the
data and workflows that matter to it — its workspace skills, macro workflows,
client advisory, research, or trading flows — using the same scenario schema,
certification gates, and reporting. The collection name in `--run name=dir` is
free-form, so a private collection joins the aggregate just by naming itself.
See [docs/private-task-packs.md](docs/private-task-packs.md) for the private path.

## Private Task Packs

Evaluate private scenarios from a directory:

```bash
uv run workspace-bench validate --scenario-dir ./my-workspace-tasks
uv run workspace-bench run-agent-command \
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
  --scenario gen_t0_create_price_performance_aapl \
  --json
```

Check the broader live MCP surface against a workflow scenario:

```bash
uv run --extra live workspace-bench smoke-workspace-mcp \
  --url http://127.0.0.1:8787 \
  --pack all \
  --scenario gen_t0_skill_finance_earnings_prep \
  --check-surface \
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

The bundled `Bench Stark Enterprise` fixture packages widget and app metadata
from the [Stark Industries demo](https://github.com/DidierRLopes/stark-industries-demo) into a stable local backend, with seeded
deterministic data per widget. It is used for enterprise workflow coverage
without depending on a live demo app.

## Scenario Shape

Each scenario defines:

- analyst prompt
- fixture backends
- optional initial Workspace state
- allowed tools and limits
- deterministic success criteria
- oracle trace
- metadata for slicing and reporting:
  - `capability`: the benchmark action under test, such as widget creation, app instantiation, repair, data reading, skill access, or MCP tool use
  - `workflow`: the real analyst workflow, such as earnings prep, risk review, client meeting prep, or vendor SLA monitoring
  - `domain`: broad area, usually `finance` or `workspace-ops`
  - `subdomain`: narrower finance or ops area, such as equities, portfolio, macro, compliance, execution, or research

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
- `get_skill_content`
- `read_workspace_resource`
- `get_workspace_prompt`
- `assign_tasks_to_agents`

The grader evaluates final Workspace state first. Text-only answers are secondary; the durable artifact is the dashboard/app state the agent produced.

See [docs/scenario-format.md](docs/scenario-format.md).

See [docs/benchmark-card.md](docs/benchmark-card.md) for the benchmark card, scope, and limitations.
See [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) for release gates.
See [CONTRIBUTING.md](CONTRIBUTING.md) for scenario, grader, agent, export, and RL contribution paths.

## Task Levels and Tiers

Levels classify what kind of workflow a task is:

- `L0`: inspect and answer from an existing dashboard
- `L1`: create, update, read, or lay out a single widget
- `L2`: build a multi-widget dashboard from analyst requirements
- `L3`: use app templates, tabs, parameter groups, prompts, skills, or delegation
- `L4`: repair incorrect Workspace state or bad metadata assumptions
- `L5`: long-horizon multi-agent workflows, reserved for later

Structural tiers grade how demanding the episode is, orthogonally to level —
every tool family carries a complete ladder:

- `t0`: one action, generous budget
- `t1`: one mutation under full discovery discipline
- `t2`: composed artifacts — several checks must hold at once
- `t3`: repair seeded pathologies without collateral damage
- `t4`: multi-intent composition under a tight turn budget

Difficulty labels derive from tiers (t0 easy, t2 medium, t4 hard; t1 and t3
straddle bands), yielding 90 easy / 120 medium / 90 hard in `core`. Calibration
against six models confirmed the ladder: the gating model's pass rate falls
monotonically 98 → 92 → 77 → 52 → 33 across t0 → t4.

The `build-openbb-apps` collection carries its own ladder — t0 one widget with
the right schema, t1 ship it as an app (graded in full: each tier contains the
one below by construction), t2 composed requirements with policy derivation,
t3 multi-widget multi-tab apps, t4 build-publish-instantiate-configure-document
— with 60 easy / 80 medium / 72 hard. Its official gating curve falls
95 → 90 → 73 → 63 → 48.

## Repository Layout

```text
src/workspace_bench/
  cli.py                 Command line interface
  core/                  Scenario dataclasses, bundled tasks, episodes, runner, graders
    scenario_packs/      Bundled collections: workspace-bench-v1 (core),
                         workspace-bench-v2-build-openbb-apps
  workspace/             Fixture backends, simulator, live workspace-mcp smoke bridge
    data/                Packaged fixture metadata such as Stark widgets/apps
  agents/                Oracle/noop agents, JSONL command protocol, model adapter helpers
  reports/               Model comparison, reliability metrics, charts, analysis reports
  exports/               Rollout, SFT, preference, and metadata export helpers
  rl/                    Gym-style env, action/observation/reward helpers
  __init__.py            Small public convenience surface
docs/
  agent-command.md
  architecture.md
  benchmark-card.md
  contributing.md
  private-task-packs.md
  result-schema.md
  research-tmax-general-agent.md
  rl-factory-adapter.md
  roadmap.md
  scenario-format.md
  scenario-catalog.md      All 512 scenarios (both collections), documented
  tool-coverage-matrix.md  Per-test x per-tool requirement matrix
  training-recipes.md
scripts/
  generate_gen_pack.py     Core collection generator (families x tiers)
  generate_build_apps_pack.py  build-openbb-apps collection generator + certifier
  generate_stark_data.py   Seeded Stark fixture data baker
  compile_calibration.py   Aggregates core runs into runs/reports/calibration.json
  compile_collections_report.py  Pools collections into runs/reports/collections.json
runs/
  comparison/              Committed runs: six models x both collections
                           (core-<model>, build-<model>)
  exports/                 Rollout JSONL for the 1,800 core episodes
  reports/                 Compiled calibration + collections reports
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
from workspace_bench.rl.env import WorkspaceGymEnv

env = WorkspaceGymEnv()
observation, info = env.reset(seed=1)
observation, reward, terminated, truncated, info = env.step(
    {"tool": "get_workspace_snapshot", "args": {}}
)
```

## Release Notes

This is an alpha benchmark package. It is ready for local evals, private task packs, CI regression testing, and `workspace-mcp` sidecar smoke tests, and it ships with six real model baselines. Before a broader public leaderboard: held-out/hidden scenario splits and a browser-backed real Workspace runner.
