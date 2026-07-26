# OpenBB Workspace Bench

[![CI](https://github.com/DidierRLopes/openbb-workspace-bench/actions/workflows/ci.yml/badge.svg)](https://github.com/DidierRLopes/openbb-workspace-bench/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

OpenBB Workspace Bench is a Terminal-Bench-style evaluation harness for agents that operate inside composable financial workspaces through OpenBB Workspace MCP tools.

The benchmark asks a simple question: can an agent inspect, build, update, and repair durable Workspace state? Scoring is based on final dashboard/app state, widget configuration, generated artifacts, layout, and tool-use discipline.

Motivation: a [NY Tech Week talk](https://youtu.be/7fDTDYh2NJ4?t=1210) showed agents driving real financial work in OpenBB Workspace over MCP, on the [Stark Industries demo](https://github.com/DidierRLopes/stark-industries-demo). A demo shows work can happen once; this benchmark measures how reliably agents actually drive it. The Stark demo is also where the enterprise tasks come from.

Three suites ship bundled in a capability ladder: `smoke` checks one round trip
per Workspace MCP surface (80 tasks), `enterprise-apps-default` answers the
default apps' product prompts in two data worlds (138), and
`workspace-tasks` operates Workspace state through agent-authored persona
storylines (120).

## Contents

- [What Is Included](#what-is-included)
- [Scope & Limitations](#scope--limitations)
- [Quick Start](#quick-start)
- [Archived Baselines](#archived-baselines)
- [Evaluate Your Agent](#evaluate-your-agent)
- [Suites](#suites)
- [Private Task Suites](#private-task-suites)
- [Live Workspace MCP Smoke](#live-workspace-mcp-smoke)
- [Browser Certification](#browser-certification)
- [Serve Fixture Backends](#serve-fixture-backends)
- [Reference](#reference) — [TASK-SCHEMA.md](TASK-SCHEMA.md) · [RESULT-SCHEMA.md](RESULT-SCHEMA.md)
- [Grading Model](#grading-model)
- [Task Organization](#task-organization)
- [Terminology](#terminology)
- [Repository Layout](#repository-layout)
- [Contamination Canary](#contamination-canary)
- [Release Notes](#release-notes)

## What Is Included

- 338 deterministic simulator tasks across three certified suites:
  - `smoke` — 80 tasks: a four-level execution ladder over every Workspace MCP surface
  - `enterprise-apps-default` — 138 tasks pairing 69 byte-verbatim product prompts across two data worlds
  - `workspace-tasks` — 120 agent-authored operating tasks: 6 personas
    (portfolio manager, fund operations, research analyst, trading desk,
    compliance, client advisor) x 4 stories x 5 levels (Execute, Find,
    Derive, Ground, Compose), run closed-world on the everything-mounted
    workspace and topped by authoring custom backends

  Each suite directory under `src/workspace_bench/task_suites/` has a README
  explaining how it is generated and how its tasks are categorized.
- generated and agent-authored task families covering widgets, apps, prompts, resources, skills, delegation, inspection, repair, and layout
- transcription-grade Getting Started, Widget Examples, Stark enterprise, and Daloopa fixture backends
- simulator-backed Workspace MCP runtime for fast local evals
- live `workspace-mcp` sidecar smoke runner
- optional Playwright browser-certification harness for runtime-enabled suites
- public task envelope export
- external agent command contract
- private task directory support
- oracle and no-op baselines
- state and trace graders
- provenance-aware report generation

The simulator is intentional. It makes evals fast, deterministic, and suitable for CI and high-volume regression runs. The live smoke runner exercises the real `workspace-mcp` HTTP and websocket bridge path against the same task contract.
The browser subset is a separate, slower realism gate; its bundled self-test
uses real Chromium against a mock Workspace page, while a real-product run
requires one saved human login.

## Scope & Limitations

WorkspaceBench is an agent evaluation harness, not a full training framework
or public leaderboard. Its default runner uses a deterministic simulator and
fixture data, not live market data or a real Workspace browser. The optional
sidecar smoke test verifies the MCP transport and tool surface; browser dry-run
and self-test verify the local harness, not live-product parity. A real
authenticated `browser-cert --all` run is required before claiming live
Workspace execution.

Training, RL, and live Workspace execution are downstream paths that reuse the
same benchmark core. Other important boundaries:

- Public task files contain success criteria and oracle traces; use hidden
  private suites for held-out evaluation and never train on their answers.
- Runtime-enabled simulator tasks make real localhost HTTP probes against
  evaluator-owned deterministic data, but do not execute agent-authored backend
  code.
- `assign_tasks_to_agents` is an envelope echo in the simulator, not proof of
  downstream multi-agent work. Completion-note semantics and cosmetic polish
  are narrower than human review.
- Guided and cold evaluation tracks provide different assistance and must be
  reported separately. Archived boards predate the current contracts and must
  not be pooled with current runs.

## Quick Start

Install dependencies and inspect the benchmark:

```bash
uv run workspace-bench list
uv run workspace-bench manifest --json
uv run workspace-bench validate --suite smoke --min-tasks 80
uv run workspace-bench validate --suite enterprise-apps-default --min-tasks 138
uv run workspace-bench validate --suite workspace-tasks --min-tasks 120
```

Run built-in baselines:

```bash
uv run workspace-bench run --agent oracle
uv run workspace-bench run --agent noop
uv run workspace-bench report --output runs/reports/benchmark-report.md
```

The committed deterministic certification report is
`runs/reports/benchmark-report.md` (core).

Run tests:

```bash
uv run --extra dev pytest
```

## Archived Baselines

The current operating-suite board lives in the [Suites](#suites) section;
everything below predates the current task contract and is preserved as
history. The `enterprise-apps-usage` suite itself was retired in July 2026
when the agent-authored `workspace-tasks` suite replaced it as the operating
suite.

The committed model runs below predate the current task contract. Their task
ids include the retired generation labels and their prompts/graders differ from
the active corpus. Historical numbers remain for reproducibility and must not
be compared directly with fresh runs. New reports record the Git commit, dirty
state, and suite content hash instead of a hand-maintained release number.

Six models have been run against both suites (pass@1, single fresh
end-to-end attempt per suite, temperature 0, same grader and turn budget
for every model — no patched or spliced results).

Retired usage suite (operating the workspace, 192 tasks):

| Model | Strict pass | t0 → t4 pass rate (%) |
|---|---|---|
| GPT-5.5 | 282/300 (94.0%) | 98 · 100 · 90 · 87 · 95 |
| Claude Sonnet 5 | 267/300 (89.0%) | 100 · 98 · 85 · 82 · 80 |
| GLM-5.2 | 229/300 (76.3%) | 85 · 100 · 73 · 60 · 63 |
| gpt-4.1-mini ‡ | 211/300 (70.3%) | 98 · 92 · 77 · 52 · 33 |
| gpt-oss:20b | 178/300 (59.3%) | 93 · 68 · 57 · 45 · 33 |
| Qwen3 8B | 149/300 (49.7%) | 80 · 78 · 47 · 27 · 17 |

Historical task-IID 95% Wilson intervals at n=300 span roughly ±3–6 points (GPT-5.5 90.7–96.2%,
Qwen3 8B 44.0–55.3%). Paired McNemar tests separate every adjacent rank
except GLM-5.2 vs gpt-4.1-mini (p=0.06). Strict pass counts provider/process
failures as failures — core process failures: Sonnet 5 15, gpt-oss:20b 22,
Qwen3 8B 20, GLM-5.2 4, GPT-5.5 1, gpt-4.1-mini 0; excluding them, the
valid-attempt pass rates are 94.3 / 93.7 / 77.4 / 70.3 / 64.0 / 53.2%.

The raw per-task traces from those runs predate the 2026-07 schema resets and
were removed from the repository as non-comparable; the compiled evidence
remains at `runs/reports/calibration.json` (built by
`workspace-bench compile calibration`), and confidence intervals, difficulty
slices, and all pairwise tests at `runs/reports/significance.json`. Task-IID
Wilson and McNemar statistics are retained only as descriptive historical
measures.

‡ gpt-4.1-mini is the calibration model; the other five models never
influenced task selection.

The retired 512-task pooled snapshot was GPT-5.5 96.5%, Sonnet 5 93.0%,
GLM-5.2 85.7%, gpt-4.1-mini 71.1%, gpt-oss:20b 62.9%, and Qwen3 8B 35.0%.
It is preserved here as history but deliberately absent from the current
aggregate in `runs/reports/suites.json`; cross-era pooling is invalid.

Repeatability: the calibration model repeated 3x over the 300 core tasks lands
at 71.7 / 70.0 / 70.7% strict per attempt (pass@3 73.7%, pass^3 67.3%), with
only 19/300 tasks showing within-model variance.

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
  --suite workspace-tasks
```

Omit `--task` and the runner covers the whole suite (e.g. `--suite
workspace-tasks`); add `--family` (a persona, e.g.
`compliance_risk`), `--difficulty` (a level), or `--tag` to run a slice.

Compare only one difficulty slice:

```bash
uv run workspace-bench \
  --suite workspace-tasks \
  --difficulty level2 \
  --timeout 240
```

Run repeated attempts for a more stable comparison:

```bash
uv run workspace-bench \
  --suite workspace-tasks \
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
suites automatically, and the output directory defaults to a timestamped
folder under `runs/comparison/`. The run directory keeps the full
`conversation.json` (every turn: prompt, model actions, tool results),
raw `model_responses.jsonl`, and executed `tool_calls.jsonl` for inspection.
`--task` is repeatable, and `--repeats 3` shows whether behavior on a
task is stable.

The default `--track guided` includes the common procedure and fixture hints.
Use `--track cold` to remove both; the track is recorded in run metadata and
guided/cold scores must be reported separately.

The task's rubric lives next to its prompt in the task JSON
(`src/workspace_bench/task_suites/<suite>/<family>/<id>.json`) — the
`success` block is exactly what the grader checks, and `oracle_tool_calls` is
a known-good solution to diff against.

Run models from a JSON adapter config:

```bash
uv run workspace-bench \
  --models-file my-models.json \
  --suite workspace-tasks \
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
validates the deterministic model, temperature, harness-revision, suite-hash,
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

Compile a smoke or full result directory into family×difficulty and per-task
calibration matrices:

```bash
uv run workspace-bench compile calibration runs/comparison/<run-id> \
  --output runs/comparison/<run-id>/calibration.json
```

After at least two model result sets exist,
`workspace-bench compile difficulty` produces a raw band proposal and a
conservatively approved override payload; `--apply-overrides PATH` writes the
approved table to a measured-difficulty JSON file for downstream review.

Use `--suite workspace-tasks` for the stable interactive suite, and `--task-dir`
for a private task suite. You can slice with `--family`, `--category`, and
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

Training exports are explicit downstream artifacts. Preserve their Git commit,
dirty-worktree flag, suite content hash, schema version, task identity, and
model/runner metadata. Prefer passing attempts for SFT, keep failed attempts
only with grade metadata, and do not mix in hidden answer data.

## Suites

The benchmark is organized as **suites**: certified sets of tasks that can
be added independently and reported separately or in aggregate. Bundled today:

| suite | tasks | what it measures |
| --- | --- | --- |
| `smoke` | 80 | four-level execution ladder across every Workspace MCP tool and knowledge surface |
| `enterprise-apps-default` | 138 | answering 69 byte-verbatim product prompts across two seeded data worlds |
| `workspace-tasks` | 120 | operating the workspace through agent-authored persona storylines: 6 personas x 4 stories x 5 levels (Execute, Find, Derive, Ground, Compose), closed-world |

```bash
# run or validate one suite
uv run workspace-bench validate --suite workspace-tasks --min-tasks 120
uv run workspace-bench --models-file my-models.json --suite workspace-tasks
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
| gpt-4.1-mini (reference) | 39.4% | 85 | 60 | 36 | 17 | 0 |
| gpt-oss:20b | 19.2% | 38 | 21 | 29 | 8 | 0 |
| qwen3:8b | 16.7% | 38 | 21 | 17 | 8 | 0 |

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

Every suite requires the reference solution to pass every task and a
do-nothing agent to fail every task. Additional generation and validation gates
are suite-specific: they include prompt provenance, outcome-only rubric review,
coverage and difficulty quotas, mutation sensitivity, check caps, live-process
tests, and clean teardown where applicable. Each suite README records its exact
generation method, axes, gates, and limitations.

Per-suite results roll up into one pooled aggregate — task counts are
added across suites, never averaged percentages. Point the report at one
run directory per model per suite:

```bash
# each evaluator invocation writes one run directory per model
uv run workspace-bench compile suites \
  --run workspace-tasks=runs/comparison/<run-id>/<model>.json \
  --historical-run core=runs/comparison/<historical-run-id> \
  --output /tmp/workspace-bench-suites-example.json
```

This is the extension path: a firm can add a private suite built from the
data and workflows that matter to it — its workspace skills, macro workflows,
client advisory, research, or trading flows — using the same task schema,
certification gates, and reporting. The suite name in `--run name=dir` is
free-form, so a private suite joins the aggregate just by naming itself.

## Private Task Suites

Evaluate private tasks from a directory:

```bash
uv run workspace-bench validate --task-dir ./my-workspace-tasks
uv run workspace-bench run-agent-command \
  --task-dir ./my-workspace-tasks \
  --agent-command "python my_agent.py" \
  --json
```

Private task suites use the same task schema as the bundled benchmark. This is
the main BYO-data path: teams can point tasks at deterministic internal
Workspace backends and keep graders local. Discovery is recursive, so
`<family>/<task>.json` is the recommended layout. An optional
`task_suite.json` can declare `suite_id` and `visibility` (`private` or
`hidden`). Hidden suites redact prompts from trace artifacts while
retaining ids, scores, calls, results, and final snapshots. The public agent
envelope always excludes `success`, `oracle_tool_calls`, and hidden grader
logic. Good private tasks use deterministic versioned data, require tool use
and durable state, include an oracle, and fail the no-op baseline.

## Live Workspace MCP Smoke

Start a local `workspace-mcp` sidecar:

```bash
workspace-mcp --cors-allow https://pro.openbb.dev
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
  --suite workspace-tasks \
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

The operating suite was replaced by the agent-authored `workspace-tasks`
suite in July 2026; its live-parity eligibility set is pending derivation.
Compose-rung tasks use backend/app mutation tools that the conservative
replay does not execute, so they will be refused with a reason.

## Browser Certification

Install the optional browser dependency and Chromium once:

```bash
uv sync --extra dev --extra browser
uv run playwright install chromium
```

The local gates need no Workspace account. Dry-run validates every manifest
entry, its oracle backend, runtime-derived evidence, parameters,
columns, tabs, CORS, and live HTTP routes. Self-test drives real Chromium
through the same connection, app/widget placement, interaction, assertion,
screenshot, and trace code used for the product run:

```bash
uv run --extra browser workspace-bench browser-cert --dry-run
uv run --extra browser workspace-bench browser-cert --self-test
```

The bundled certification manifest currently ships no entries (the previous
subset certified the retired app-building suite), so certification fails
closed until a new subset of runtime-enabled tasks is authored.

Artifacts are written under `runs/browser-cert/selftest-*/` as
`screenshot.png`, `trace.zip`, and `verdict.json`.

A real OpenBB Workspace run has one human step: save an authenticated browser
storage state outside the repository. No credentials are accepted or stored by
the harness.

```bash
mkdir -p ~/.config/workspace-bench
uv run --extra browser workspace-bench browser-cert \
  --setup-auth \
  --workspace-url https://pro.openbb.co \
  --auth-state ~/.config/workspace-bench/openbb.workspace-auth.json

uv run --extra browser workspace-bench browser-cert \
  --all \
  --workspace-url https://pro.openbb.co \
  --auth-state ~/.config/workspace-bench/openbb.workspace-auth.json
```

Workspace UI selectors are externalized in
`src/workspace_bench/workspace/browser/selectors.json`. If the live product differs,
copy that file outside the repository, edit only the selectors, and pass it
with `--selectors PATH`. The local self-test proves the browser, backend, and
artifact layers; it does **not** prove live-product selector or rendering
parity. Keep the no-live-execution claim in place until the real `--all` run
passes and its verdicts are reviewed.

## Serve Fixture Backends

Serve a deterministic fixture as a Workspace backend:

```bash
uv run workspace-bench serve-fixture --backend getting-started --port 9106
```

The server exposes:

- `GET /widgets.json`
- `GET /apps.json`
- widget data endpoints such as `/company_performance?company=TM&year=2024`

`Getting Started` and `Widget Examples` are transcribed from the real
[OpenBB backend examples repository](https://github.com/OpenBB-finance/backend-examples-for-openbb-workspace),
including widget ids, names, parameters, data shapes, literal samples, and the
Getting Started app. The historical `equities`, `macro`, and `portfolio` slugs
remain CLI lookup aliases for compatibility; they no longer expose separate
invented data.

The bundled `Bench Stark Enterprise` fixture packages widget and app metadata
from the [Stark Industries demo](https://github.com/DidierRLopes/stark-industries-demo) into a stable local backend, with seeded
deterministic data per widget. It is used for enterprise workflow coverage
without depending on a live demo app. Serving it exposes the exact catalog and
baked payloads the simulated workspace grades against (349 widgets, 23 apps):

```bash
uv run workspace-bench serve-fixture --backend stark-enterprise --port 9104
```

The bundled `Bench Daloopa` fixture mirrors the data surface consumed by the
[Daloopa Claude plugin skills](https://github.com/daloopa/daloopa-plugin-claude):
company discovery, series discovery, fundamentals with per-datapoint citation
ids, operating KPIs, segment breakdowns, management guidance, consensus
estimates, SEC document search, and daily stock prices across six covered
companies. Unlike the Stark catalog (imported from a demo repo, then baked),
the Daloopa catalog is fully authored and baked by
`scripts/generators/generate_daloopa_data.py`. It is deliberately a
standalone vendor feed — 10 widgets and no app templates — because the
matching `daloopa-*` workspace skills (tearsheet, earnings review, guidance
tracker, inflection, capital allocation, industry comparison; served through
`get_skill_content`) are what drive dashboard composition against it. Pair it
with `stark-enterprise` in a task's fixture backends to test Daloopa skill
workflows inside the enterprise workspace:

```bash
uv run workspace-bench serve-fixture --backend daloopa --port 9105
```

A runtime-enabled task's oracle-declared backend and task-owned runtime
datasets can be served with `workspace-bench serve-task-backend` (pass the
qualified task ref and a port), which exposes that task's `widgets.json`,
`apps.json`, widget data, parameter options, and form-submit endpoints with
CORS enabled.

## Reference

Two focused reference documents sit at the repository root:

- **[TASK-SCHEMA.md](TASK-SCHEMA.md)** — the full `workspace-bench-task` JSON
  contract: task fields, `SuccessCriteria`, runtime datasets, capabilities, and
  the `specification_level` vs measured `difficulty` split.
- **[RESULT-SCHEMA.md](RESULT-SCHEMA.md)** — evaluator output: result rows and
  `GradeResult` dimensions, deployment receipts, rollout/SFT/preference exports,
  and the complete issue-code catalog.

The generated per-task oracle-tool matrix and task catalog live under
`runs/reports/`.

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

Every active task has the canonical identity `suite/family/task`, for example
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
suites instead grade a `level0`–`level4` (workspace-tasks) or `level0`–`level3` (smoke)
operation ladder. It does not render prompts or select graders.
**Specification level** is the structural axis that does; see
[TASK-SCHEMA.md](TASK-SCHEMA.md).

## Terminology

For readers arriving from other benchmarks:

| here | elsewhere |
| --- | --- |
| task | Terminal-Bench / Inspect / GAIA / TMax "task" (HELM says "scenario") |
| suite | lm-eval-harness "group"/"suite", Terminal-Bench registry "dataset" |
| difficulty | GAIA "Level 1–3", TMax "complexity buckets" |
| family | METR-style "task family" — the suite's grouping axis (personas in workspace-tasks, tool families in smoke) |
| category | task type — τ-bench's "domain" plays a similar role |
| rubric / graders | Terminal-Bench "verification test suite", TMax "graded verifiers" |
| oracle | Terminal-Bench "oracle solution" (same word) |

## Repository Layout

```text
src/workspace_bench/
  cli.py                 Command line interface
  core/                  Task dataclasses, episodes, runner, graders
  task_suites/           Bundled suites, organized as suite/family/task:
    smoke/                              MCP-surface round trips
    enterprise_apps_default/            Default-app product prompts
    workspace_tasks/                    Agent-authored persona storylines
      portfolio_manager/ ...              One directory per persona
  workspace/             Fixture backends, simulator, live workspace-mcp smoke bridge
    data/                Packaged fixture metadata such as Stark and Daloopa widgets/apps
  agents/                Oracle/noop agents, JSONL command protocol, model adapter helpers
  reports/               Model comparison, reliability metrics, charts, analysis reports
  exports/               Rollout, SFT, preference, and metadata export helpers
  rl/                    Gym-style env, action/observation/reward helpers
  __init__.py            Small public convenience surface
scripts/
  generators/             Deterministic suite, catalog, matrix, and fixture generators
  audits/                 Local, release, hosted-surface, and prompt audits
runs/
  reports/                 Compiled reports and generated catalogs/matrices
    task-catalog.md         Generated catalog of the deterministic simulator tasks
    tool-coverage-matrix.md Per-task x Workspace MCP oracle-tool matrix
    tool-matrix-data.json   Machine-readable data behind the tool matrix
references/
  openbb-backend-examples/  Vendored OpenBB backend reference implementations (MIT,
                            pinned upstream commit) — ground truth for building
                            widget-creation and backend-building tasks
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

## Release Notes

This is an alpha benchmark package. It is ready for local evals, private task suites, CI regression testing, `workspace-mcp` sidecar smoke tests, and local browser-harness self-testing, and it ships with committed model boards and baselines. Before a broader public leaderboard: hidden task suites and a completed browser-certification run against a real authenticated Workspace.
