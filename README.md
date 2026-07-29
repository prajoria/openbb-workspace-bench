# OpenBB Workspace Bench

[![CI](https://github.com/DidierRLopes/openbb-workspace-bench/actions/workflows/ci.yml/badge.svg)](https://github.com/DidierRLopes/openbb-workspace-bench/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

OpenBB Workspace Bench is a Terminal-Bench-style evaluation harness for agents that operate inside composable financial workspaces through OpenBB Workspace MCP tools.

The benchmark asks a simple question: can an agent inspect, build, update, and repair durable Workspace state? Scoring is based on final dashboard/app state, widget configuration, generated artifacts, layout, and tool-use discipline.

Motivation: a [NY Tech Week talk](https://youtu.be/7fDTDYh2NJ4?t=1210) showed agents driving real financial work in OpenBB Workspace over MCP, on the [Stark Industries demo](https://github.com/DidierRLopes/stark-industries-demo). A demo shows work can happen once; this benchmark measures how reliably agents actually drive it. The Stark demo is also where the enterprise tasks come from.

Three tasksets ship bundled in a capability ladder: `smoke` checks one round trip
per Workspace MCP surface (80 tasks), `enterprise-apps-default` answers the
default apps' product prompts in two data worlds (138), and
`workspace-tasks` operates Workspace state through agent-authored persona
storylines (120).

Benchmark vocabulary (task, taskset, family, oracle, closed-world) is mapped
to other benchmarks' terms in [Terminology](#terminology).

## Contents

- [What Is Included](#what-is-included)
- [Scope & Limitations](#scope--limitations)
- [Quick Start](#quick-start)
- [Evaluate Your Agent](#evaluate-your-agent)
- [Tasksets](#tasksets)
- [Private Tasksets](#private-tasksets)
- [Live Workspace MCP Smoke](#live-workspace-mcp-smoke)
- [Harbor Adapter](#harbor-adapter)
- [Reference](#reference) — [TASK-SCHEMA.md](TASK-SCHEMA.md) · [RESULT-SCHEMA.md](RESULT-SCHEMA.md)
- [Grading Model](#grading-model)
- [Task Organization](#task-organization)
- [Terminology](#terminology)
- [Repository Layout](#repository-layout)
- [Contamination Canary](#contamination-canary)
- [Status](#status)

## What Is Included

- 338 deterministic simulator tasks across three certified tasksets:
  - `smoke` — 80 tasks: a four-level execution ladder over every Workspace MCP surface
  - `enterprise-apps-default` — 138 tasks pairing 69 byte-verbatim product prompts across two data worlds
  - `workspace-tasks` — 120 agent-authored operating tasks: 6 personas
    (portfolio manager, fund operations, research analyst, trading desk,
    compliance, client advisor) x 4 stories x 5 levels (Execute, Find,
    Derive, Ground, Compose), run closed-world on the everything-mounted
    workspace and topped by authoring custom backends

  Each taskset directory under `src/workspace_bench/tasksets/` has a README
  explaining how it is generated and how its tasks are categorized.
- generated and agent-authored task families covering widgets, apps, prompts, resources, skills, delegation, inspection, repair, and layout
- transcription-grade Getting Started, Widget Examples, Stark enterprise, and Daloopa fixture backends
- simulator-backed Workspace MCP runtime for fast local evals
- live `workspace-mcp` sidecar smoke runner
- public task envelope export
- external agent command contract
- private task directory support
- oracle and no-op baselines
- state and trace graders
- provenance-aware report generation

The simulator is intentional. It makes evals fast, deterministic, and suitable for CI and high-volume regression runs. The live smoke runner exercises the real `workspace-mcp` HTTP and websocket bridge path against the same task contract.

## Scope & Limitations

WorkspaceBench is an agent evaluation harness, not a full training framework
or public leaderboard. Its default runner uses a deterministic simulator and
fixture data, not live market data or a real Workspace browser. The optional
sidecar smoke test verifies the MCP transport and tool surface, not
live-product parity - do not claim live Workspace execution from simulator
results.

Training, RL, and live Workspace execution are downstream paths that reuse the
same benchmark core. Other important boundaries:

- Public task files contain success criteria and oracle traces; use hidden
  private tasksets for held-out evaluation and never train on their answers.
- Runtime-enabled simulator tasks make real localhost HTTP probes against
  evaluator-owned deterministic data, but do not execute agent-authored backend
  code.
- `assign_tasks_to_agents` is an envelope echo in the simulator, not proof of
  downstream multi-agent work. Completion-note semantics and cosmetic polish
  are narrower than human review.
- Guided and cold evaluation tracks provide different assistance and must be
  reported separately.

## Quick Start

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/) (`uv run` creates
the environment on first use). Clone the repo, then inspect the benchmark:

```bash
uv run workspace-bench list
uv run workspace-bench manifest --json
uv run workspace-bench validate --taskset smoke --min-tasks 80
uv run workspace-bench validate --taskset enterprise-apps-default --min-tasks 138
uv run workspace-bench validate --taskset workspace-tasks --min-tasks 120
```

Run built-in baselines:

```bash
uv run workspace-bench run --taskset workspace-tasks --agent oracle
uv run workspace-bench run --taskset workspace-tasks --agent noop
uv run workspace-bench report --taskset workspace-tasks --output runs/reports/benchmark-report.md
```

The committed deterministic certification report is
`runs/reports/benchmark-report.md` (workspace-tasks).

Run tests:

```bash
uv run --extra dev pytest
```

## Evaluate Your Agent

Workspace Bench can evaluate any external process that writes tool calls as JSON Lines.

Run the included demo agent:

```bash
uv run workspace-bench run-agent-command \
  --task workspace-tasks/portfolio_manager/morning_briefing_level0 \
  --agent-command "python -m workspace_bench.agents.rule_agent" \
  --json
```

The harness writes a task envelope JSON file, sets environment variables for the agent command, reads the agent's emitted `tool_calls.jsonl`, executes those calls in the Workspace simulator, and grades the final state.

Run any external agent command (it receives the task envelope via
`WORKSPACE_BENCH_TASK_JSON` and writes tool calls to
`WORKSPACE_BENCH_OUTPUT_JSONL`):

```bash
uv run workspace-bench run-agent-command \
  --task workspace-tasks/portfolio_manager/morning_briefing_level0 \
  --agent-command "python -m workspace_bench.agents.rule_agent" \
  --run-dir runs/rule-agent \
  --json
```

The OpenAI adapter writes `openai_prompt.txt`, `openai_response.txt`, and `tool_calls.jsonl` inside the task run directory.

Run several models side by side — `--model` is repeatable:

```bash
uv run workspace-bench \
  --model openai:gpt-4.1-mini \
  --model ollama:qwen3:8b \
  --taskset workspace-tasks
```

Omit `--task` and the runner covers the whole taskset (e.g. `--taskset
workspace-tasks`); add `--family` (a persona, e.g.
`compliance_risk`), `--difficulty` (a level), or `--category` to run a slice.

Compare only one difficulty slice:

```bash
uv run workspace-bench \
  --taskset workspace-tasks \
  --difficulty level2 \
  --timeout 240
```

Run repeated attempts for a more stable comparison:

```bash
uv run workspace-bench \
  --taskset workspace-tasks \
  --release-run \
  --repeats 3 \
  --metric pass-at-k \
  --concurrency 4 \
  --episode-timeout 900 \
  --timeout 240
```

Run one specific task with one specific model — the fastest way to study
what a model actually does on a single task:

```bash
uv run workspace-bench --model openai:gpt-4.1-mini --task workspace-tasks/research_analyst/earnings_prep_level0
```

That's the whole command - no subcommand needed, evaluating is what the tool does: `--model provider:model` needs no adapter config
(API keys are read from the environment or `.env`; `ollama:<model>` works the
same for local models), the task id is found across the bundled
tasksets automatically, and the output directory defaults to a timestamped
folder under `runs/comparison/`. The run directory keeps the full
`conversation.json` (every turn: prompt, model actions, tool results),
raw `model_responses.jsonl`, and executed `tool_calls.jsonl` for inspection.
`--task` is repeatable, and `--repeats 3` shows whether behavior on a
task is stable.

The default `--track guided` includes the common procedure and fixture hints.
Use `--track cold` to remove both; the track is recorded in run metadata and
guided/cold scores must be reported separately.

The task's rubric lives next to its prompt in the task JSON
(`src/workspace_bench/tasksets/<taskset>/<family>/<id>.json`) — the
`success` block is exactly what the grader checks, and `oracle_tool_calls` is
a known-good solution to diff against.

Run models from a JSON adapter config:

```bash
uv run workspace-bench \
  --models-file my-models.json \
  --taskset workspace-tasks \
  --timeout 240
```

The comparison runner prints `[PASS]` or `[FAIL]` after each task and writes
raw JSON results plus `comparison.json`, `analysis.md`, `chart.svg`, and
`chart.png` into a timestamped directory under `runs/comparison/`.
`analysis.md` separates grader/task issues from provider or process failures.
PASS/FAIL status is colorized on normal terminals; use `--color always` or
`--color never` to force a behavior.

By default, the comparison runner is interactive: each model chooses one tool
call, receives the simulated Workspace result, then chooses the next call. Each
task run directory includes `conversation.json`, `model_responses.jsonl`,
and `tool_calls.jsonl`. Use `--runner batch` to compare against the older
single-shot JSONL adapter behavior. Transient model API failures such as HTTP
429/520 are retried with exponential backoff; tune this with `--model-retries`
and `--retry-backoff`. Use `--concurrency N` for bounded parallel episodes and
`--episode-timeout` for a wall-clock cap over all turns in one attempt. Every
completed task×repeat cell updates `<model>.checkpoint.json`; `--resume`
validates the deterministic model, temperature, harness-revision, taskset-hash,
and task manifest before replaying completed cells and running only missing
ones.

OpenRouter is a first-class OpenAI-compatible provider. It reads
`OPENROUTER_API_KEY` and defaults to `https://openrouter.ai/api/v1`:

```bash
uv run workspace-bench \
  --model openrouter:anthropic/claude-sonnet-4.5 \
  --task workspace-tasks/compliance_risk/alert_sweep_level0
```

[Concentrate](https://concentrate.ai) is also supported, speaking its
Responses-shaped API (`POST /v1/responses/`). It reads `CONCENTRATE_API_KEY`,
defaults to `https://api.concentrate.ai/v1` (override with
`CONCENTRATE_BASE_URL`), and accepts Concentrate model ids, provider-prefixed
names, or `auto`; `CONCENTRATE_REASONING_EFFORT` optionally sets the reasoning
effort. The `OPENAI_TEMPERATURE` / `OPENAI_MAX_TOKENS` /
`OPENAI_RESPONSE_FORMAT` knobs apply unchanged:

```bash
uv run workspace-bench \
  --model concentrate:openai/gpt-5.2 \
  --task workspace-tasks/compliance_risk/alert_sweep_level0
```

Per-episode rows record wall time, input/output/total tokens, API-call count,
and provider-reported cost. A `pricing` block in `--models-file` can supply
published per-million-token input, cached-input, and output prices when the
provider omits cost.

Use `--taskset workspace-tasks` for the stable interactive taskset, and `--task-dir`
for a private taskset. You can slice with `--family`, `--category`, and
`--difficulty`.

Export a task envelope without running an agent:

```bash
uv run workspace-bench export-task \
  --task workspace-tasks/research_analyst/earnings_prep_level0 \
  --output task.json
```

### External command contract

For each task, `run-agent-command` creates an isolated run directory, writes the
public `task.json` envelope, and sets these environment variables:

| variable | meaning |
| --- | --- |
| `WORKSPACE_BENCH_TASK_JSON` | Absolute path to the public task envelope. |
| `WORKSPACE_BENCH_OUTPUT_JSONL` | Output path for one `{"tool": ..., "args": ...}` object per line. |
| `WORKSPACE_BENCH_RUN_DIR` | Per-task scratch and artifact directory. |
| `WORKSPACE_BENCH_TASK_ID` | Qualified task identity being evaluated. |

The harness accepts JSONL (preferred) or a JSON array, executes the calls in
order, and grades the resulting state and trace. A non-zero exit, timeout,
unparseable output, or failed grade makes the run fail; malformed output is
retained as an invalid trace event. This command is trace-producing rather than
interactive. Use `workspace-bench --model ...` when the agent must observe each
tool result before selecting its next action.

## Tasksets

The benchmark is organized as **tasksets**: certified sets of tasks that can
be added independently and reported separately or in aggregate. Bundled today:

| taskset | tasks | what it measures |
| --- | --- | --- |
| `smoke` | 80 | four-level execution ladder across every Workspace MCP tool and knowledge surface |
| `enterprise-apps-default` | 138 | answering 69 byte-verbatim product prompts across two seeded data worlds |
| `workspace-tasks` | 120 | operating the workspace through agent-authored persona storylines: 6 personas x 4 stories x 5 levels (Execute, Find, Derive, Ground, Compose), closed-world |

```bash
# run or validate one taskset
uv run workspace-bench validate --taskset workspace-tasks --min-tasks 120
uv run workspace-bench --models-file my-models.json --taskset workspace-tasks
```

The current `workspace-tasks` board (strict pass@1, closed-world; the
reference model pools its three calibration repeats, every other row is a
single pass over the sealed 120; canonical record with per-level rates and
exclusion reasons in
[`runs/reports/workspace-tasks-board.json`](runs/reports/workspace-tasks-board.json)):

| model | overall | L0 execute | L1 find | L2 derive | L3 ground | L4 compose |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-5.5 | 93.3% | 100 | 96 | 88 | 88 | 96 |
| GLM-5.2 (Fireworks-pinned) | 81.7% | 100 | 92 | 79 | 71 | 67 |
| Gemini 2.5 Flash | 47.5% | 63 | 79 | 46 | 50 | 0 |
| gpt-4.1-mini (reference) | 39.4% | 85 | 60 | 36 | 17 | 0 |
| gpt-oss:20b | 19.2% | 38 | 21 | 29 | 8 | 0 |
| qwen3:8b | 16.7% | 38 | 21 | 17 | 8 | 0 |

Gemini 2.5 Flash runs free-form: under schema-grammar decoding it
degenerate-loops on invented tool names (0/4 probe tasks; 3/4 free-form,
same prompts). Its Find-above-Execute inversion is a reported model
property driven by skipped evidence notes, not a content defect.
Laguna S 2.1 (Poolside) ran the full 120 and is excluded with its reason
recorded: 110/120 episodes exhausted the malformed-action recoveries by
drifting into the model's native tool_call-tag syntax instead of the
harness's JSON action contract (7 of its 10 fully-compliant episodes
passed). GLM-5.2 runs pinned to a single upstream provider with fallbacks disabled:
an earlier unpinned run of the same weights scored 13.3% with 95/120
episodes dying on invalid-call storms, and stays in the board JSON as an
excluded cautionary row. Rows for claude-opus-5 and kimi-k3 are
credit-blocked (checkpoints resume when provider credits allow); each
exclusion is recorded with its reason in the board JSON.

Every taskset requires the reference solution to pass every task and a
do-nothing agent to fail every task. Additional generation and validation gates
are taskset-specific: they include prompt provenance, outcome-only rubric review,
coverage and difficulty quotas, mutation sensitivity, check caps, live-process
tests, and clean teardown where applicable. Each taskset README records its exact
generation method, axes, gates, and limitations.

This is the extension path: a firm can add a private taskset built from the
data and workflows that matter to it — its workspace skills, macro workflows,
client advisory, research, or trading flows — using the same task schema,
certification gates, and reporting. The taskset name in `--run name=dir` is
free-form, so a private taskset joins the aggregate just by naming itself.

## Private Tasksets

Evaluate private tasks from a directory:

```bash
uv run workspace-bench validate --task-dir ./my-workspace-tasks
uv run workspace-bench run-agent-command \
  --task-dir ./my-workspace-tasks \
  --agent-command "python my_agent.py" \
  --json
```

Private tasksets use the same task schema as the bundled benchmark. This is
the main BYO-data path: teams can point tasks at deterministic internal
Workspace backends and keep graders local. Discovery is recursive, so
`<family>/<task>.json` is the recommended layout. An optional
`taskset.json` can declare `taskset_id` and `visibility` (`private` or
`hidden`). Hidden tasksets redact prompts from trace artifacts while
retaining ids, scores, calls, results, and final snapshots. The public agent
envelope always excludes `success`, `oracle_tool_calls`, and hidden grader
logic. Good private tasks use deterministic versioned data, require tool use
and durable state, include an oracle, and fail the no-op baseline.

## Live Workspace MCP Smoke

Start a local `workspace-mcp` sidecar:

```bash
workspace-mcp --cors-allow https://pro.openbb.co
```

Then smoke-test the real MCP endpoint and browser bridge protocol:

```bash
uv run --extra live workspace-bench smoke-workspace-mcp \
  --url http://127.0.0.1:8787 \
  --task workspace-tasks/research_analyst/earnings_prep_level0 \
  --json
```

Check the broader live MCP surface against a workflow task:

```bash
uv run --extra live workspace-bench smoke-workspace-mcp \
  --url http://127.0.0.1:8787 \
  --taskset workspace-tasks \
  --task workspace-tasks/compliance_risk/alert_sweep_level4 \
  --check-surface \
  --json
```

The smoke command emulates the browser bridge with the benchmark simulator. It exercises the real streamable HTTP endpoint, tool schemas, server-side validation, websocket bridge, command translation layer, and session-context updates without requiring a Workspace browser tab. If a real browser is already connected, the command refuses to replace it unless `--replace-browser-session` is passed.

For release audits, `scripts/audits/audit_hosted_surface.py` compares full hosted input
schemas against the committed compatibility baseline, and
`scripts/audits/audit_live_golden_tasks.py` replays a small cross-surface golden set
through the real sidecar transport.

### Live Parity (hosted bridge)

When the hosted Workspace MCP bridge is paired with a logged-in Workspace
browser tab, one task can be run against the real product and the simulator
back-to-back, graded by the same `grade_task`, and diffed check-by-check:

```bash
export WORKSPACE_MCP_TOKEN=...   # or put it in .env
uv run --extra live workspace-bench live-parity --task smoke/get_widget_data/smoke_get_widget_data_level0
```

The live leg reproduces the task's initial state through public tool calls on
a dedicated marker-named dashboard, replays the oracle trace with origin
translation (`"Bench Stark Enterprise" → "Stark Fund"`, with identity mappings
for `Getting Started` and `Widget Examples`, by default;
`--origin-map` overrides), waits out the bridge's asynchronous write
application, grades the normalized final state, then deletes everything it
created and restores the previously active dashboard. Reports land in
`runs/live-parity/<task>/parity.json` with per-leg grades, an agreement
summary, and the live trace. Tasks the live surface cannot reproduce
faithfully are refused with a reason. Live runs execute in a real user
workspace: results are validation evidence for grader fidelity, never board
numbers.

The `workspace-tasks` live-parity eligibility set is pending derivation.
Compose-rung tasks use backend/app mutation tools that the conservative
replay does not execute, so they will be refused with a reason.

## Harbor Adapter

Workspace Bench can generate a self-contained [Harbor](https://harborframework.com/)
task while keeping the native task JSON, simulator, and grader authoritative.
The reference export uses Harbor `0.20.0` and the real committed
`workspace-mcp` sidecar:

```bash
uv run workspace-bench export-harbor \
  --workspace-mcp-repo ~/Documents/git/workspace-mcp
```

The generated task is written below `build/harbor/` (which is intentionally
ignored). To export another bundled task, pass its qualified
`taskset/family/task` reference with `--task`. The converter:

- archives the sidecar's committed `HEAD`, excluding dirty working-tree files;
- puts the sealed evaluator and reference trace only in trusted runtime,
  Oracle, and verifier contexts;
- exposes one task-aware MCP gateway to the agent;
- keeps the real sidecar's browser bootstrap on an isolated Docker network;
- records and finalizes a trusted episode artifact after the agent stops; and
- invokes the existing `grade_task` implementation in a separate verifier.

Run the deterministic reference gates with Harbor's local Docker provider:

```bash
HARBOR_TASK=build/harbor/workspace-bench-enterprise-apps-default/\
compliance_surveillance_hub/compliance_surveillance_hub_p3_x

uvx --python /usr/local/bin/python3.13 --from 'harbor==0.20.0' \
  harbor run -p "$HARBOR_TASK" -e docker -a oracle -y

uvx --python /usr/local/bin/python3.13 --from 'harbor==0.20.0' \
  harbor run -p "$HARBOR_TASK" -e docker -a nop -y
```

The primary Harbor reward is deterministic strict pass/fail. Enterprise
default tasks retain `judge_pending` and a separate `judged_strict` reward, so
an unevaluated answer judge is never presented as a completed judged result.
Harbor-native model runs are a separate harness track from the existing native
model loop. Multi-container certification currently targets the local Docker
provider. Harbor `0.20.0`'s local Docker provider does not accept a
`no-network` mode on a separate verifier, so the verifier image remains sealed
but uses the provider's public-network baseline; later provider certification
should restore an explicit no-network verifier policy where supported.

The reference task above is fully validated end to end (converter, trusted
runtime, verifier, Harbor oracle/NOP parity, and a real coding-agent trial);
suite-wide export and result ingestion are the remaining generalization work.

## Reference

Two focused reference documents sit at the repository root:

- **[TASK-SCHEMA.md](TASK-SCHEMA.md)** — the full `workspace-bench-task` JSON
  contract: task fields, `SuccessCriteria`, runtime datasets, capabilities, and
  the `specification_level` vs measured `difficulty` split.
- **[RESULT-SCHEMA.md](RESULT-SCHEMA.md)** — evaluator output: result rows and
  `GradeResult` dimensions, deployment receipts, and the complete issue-code
  catalog.

The generated per-task oracle-tool matrix and task catalog live under
`runs/reports/`. One maintainer-oriented subcommand rounds out the CLI:
`workspace-bench judge --run-dir ...` re-judges pending or errored answer
rows in a stored evaluator run.

## Grading Model

Strict success is conjunctive: **state ∧ trace ∧ configured runtime**. State is
the durable Workspace/app or code outcome, trace captures required tool use and
discipline, and runtime proves task-owned endpoint behavior over real localhost
HTTP. Polish is observable but non-gating. Partial scores are reported by
dimension; runtime-enabled outcome score is the mean of state and runtime
scores, while trace remains a strict-pass condition.

Capability grading makes less-specified tasks behavior-first. The oracle
is one witness, not a structural template: alternative solutions may choose
different widget ids, paths, counts, tabs, layouts, or split/merged views when
their runtime-valid widgets jointly expose the required business fields and
parameters, preserve app integrity, and satisfy required interaction edges.
Exact definitions and geometry remain appropriate when the explicit prompt or
core layout outcome requires them.

Grader soundness is certified against **twelve archetypes** of invalid
solutions: shifted endpoint data, never-instantiated apps, missing widgets,
incompatible values, broken forms, severed interactions, invalid gating
settings, collapsed connected views, field-less contributors, self-linked
connections, note-only proof, and apps with stripped starter prompts. Each clean oracle must pass immediately before mutation; every
mutant must fail with the issue code attributable to the injected defect.
Survivors, wrong-reason failures, or dirty oracles block release.

See [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) for release gates and
[CONTRIBUTING.md](CONTRIBUTING.md) for task, grader, agent, and export changes.

## Task Organization

Every active task has the canonical identity `taskset/family/task`, for example
`workspace-tasks/research_analyst/earnings_prep_level0`. The local task id contains only the
descriptive slug; generator mechanics are not part of the public identity.

**Category** — what kind of workflow the task is:

- `read`: inspect and answer from an existing dashboard
- `single-widget`: create, update, read, or lay out a single widget
- `dashboard`: build a multi-widget dashboard from analyst requirements
- `platform`: use app templates, tabs, parameter groups, prompts, skills, or delegation
- `repair`: fix incorrect Workspace state or bad metadata assumptions
- `story`: one persona storyline climbing the workspace-tasks ladder

**Difficulty** — `easy`, `medium`, or `hard` for classic tasks; the bundled
tasksets instead grade a `level0`–`level4` (workspace-tasks) or `level0`–`level3` (smoke)
operation ladder. It does not render prompts or select graders.
**Specification level** is the structural axis that does; see
[TASK-SCHEMA.md](TASK-SCHEMA.md).

## Terminology

For readers arriving from other benchmarks:

| here | elsewhere |
| --- | --- |
| task | Terminal-Bench / Inspect / GAIA / TMax "task" (HELM says "scenario") |
| taskset | lm-eval-harness "group"/"suite", Terminal-Bench registry "dataset" |
| difficulty | GAIA "Level 1–3", TMax "complexity buckets" |
| family | METR-style "task family" — the taskset's grouping axis (personas in workspace-tasks, tool families in smoke) |
| category | task type — τ-bench's "domain" plays a similar role |
| rubric / graders | Terminal-Bench "verification test suite", TMax "graded verifiers" |
| oracle | Terminal-Bench "oracle solution" (same word) |
| closed-world | the agent starts with no state in the prompt and discovers every dashboard through the snapshot tool |
| guided / cold tracks | two assistance levels for the same tasks — reported separately, never pooled |

## Repository Layout

```text
src/workspace_bench/
  cli.py                 Command line interface
  core/                  Task dataclasses, episodes, runner, graders
  tasksets/           Bundled tasksets, organized as taskset/family/task:
    smoke/                              MCP-surface round trips
    enterprise_apps_default/            Default-app product prompts
    workspace_tasks/                    Agent-authored persona storylines
      portfolio_manager/ ...              One directory per persona
  workspace/             Fixture backends, simulator, live workspace-mcp smoke bridge
  data/                  Packaged fixture metadata such as Stark and Daloopa widgets/apps
  agents/                Oracle/noop agents, JSONL command protocol, model adapter helpers
  reports/               Model comparison, reliability metrics, charts, analysis reports
  integrations/          Harbor task exporter, trusted runtime, and verifier
  __init__.py            Small public convenience surface
scripts/
  generators/             Deterministic taskset, catalog, matrix, and fixture generators
  audits/                 Local, release, hosted-surface, and prompt audits
runs/
  reports/                 Compiled reports and generated catalogs/matrices
    task-catalog.md         Generated catalog of the deterministic simulator tasks
    tool-coverage-matrix.md Per-task x Workspace MCP oracle-tool matrix
    tool-matrix-data.json   Machine-readable data behind the tool matrix
references/                 Local-only (gitignored) clones used during catalog
                            transcription; not distributed with the repo
task_templates/             Persona READMEs and story files — the source of truth
                            the workspace-tasks authoring pipeline works from
.claude/skills/             The authoring contracts (task-author, task-validator,
                            task-level-fairness, orchestrator) that govern it
tests/
```

## Contamination Canary

```bash
uv run workspace-bench canary
```

Benchmark data should not appear in model training corpora unless explicitly released for training.

## Status

The benchmark is ready for local evals, private tasksets, CI regression testing, and `workspace-mcp` sidecar smoke tests, and it ships with committed model boards and baselines. Before a broader public leaderboard: hidden tasksets and a certification pass against a real authenticated Workspace.
