# OpenBB Workspace Bench

[![CI](https://github.com/DidierRLopes/openbb-workspace-bench/actions/workflows/ci.yml/badge.svg)](https://github.com/DidierRLopes/openbb-workspace-bench/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

OpenBB Workspace Bench is a Terminal-Bench-style evaluation harness for agents that operate inside composable financial workspaces through OpenBB Workspace MCP tools.

The benchmark asks a simple question: can an agent inspect, build, update, and repair durable Workspace state? Scoring is based on final dashboard/app state, widget configuration, generated artifacts, layout, and tool-use discipline.

Motivation: a [NY Tech Week talk](https://youtu.be/7fDTDYh2NJ4?t=1210) showed agents driving real financial work in OpenBB Workspace over MCP, on the [Stark Industries demo](https://github.com/DidierRLopes/stark-industries-demo). A demo shows work can happen once; this benchmark measures how reliably agents actually drive it. The Stark demo is also where the enterprise tasks come from.

Three suites ship bundled: `core` (operating the workspace, 300 tasks),
`build-openbb-apps` (building and debugging custom backend apps, 236 tasks), and
the separate experimental-v0 `build-openbb-backends` real-code track (12 tasks).

## Contents

- [What Is Included](#what-is-included)
- [Scope & Limitations](#scope--limitations)
- [Quick Start](#quick-start)
- [Current Build Calibration](#current-build-calibration)
- [Archived Baselines](#archived-baselines)
- [Evaluate Your Agent](#evaluate-your-agent)
- [Suites](#suites)
- [Private Task Suites](#private-task-suites)
- [Live Workspace MCP Smoke](#live-workspace-mcp-smoke)
- [Browser Certification](#browser-certification)
- [Serve Fixture Backends](#serve-fixture-backends)
- [Real-Code Backend Track](#real-code-backend-track)
- [Task & Success Schema](#task--success-schema)
- [Result & Output Schema](#result--output-schema)
- [Grading Model](#grading-model)
- [Task Organization](#task-organization)
- [Terminology](#terminology)
- [Repository Layout](#repository-layout)
- [Contamination Canary](#contamination-canary)
- [Release Notes](#release-notes)

## What Is Included

- 548 task identities: two stable simulator suites with 536 deterministic tasks,
  plus 12 experimental code tasks:
  - `core` — 300 operating tasks across 15 tool-anchored families, with deterministic 150/75/75 train/validation/test splits
  - `build-openbb-apps` — 236 specification-tiered app-building tasks across 12 families,
    including 24 long diagnosis/repair/retest incidents
  - `build-openbb-backends` — 12 pinned FastAPI starter repositories graded by launching the agent's own server
- generated families covering widgets, apps, prompts, resources, skills, delegation, inspection, repair, layout, and backend/app building
- six archived pre-hardening model baselines with full traces and rollout exports
- equities, macro, portfolio, and Stark enterprise fixture backends
- simulator-backed Workspace MCP runtime for fast local evals
- live `workspace-mcp` sidecar smoke runner
- optional Playwright browser-certification harness with a 30-task realism subset
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
  code. The experimental code track does execute agent code and is not a
  security sandbox.
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
uv run workspace-bench validate --suite core --min-tasks 300
uv run workspace-bench validate --suite build-openbb-apps --min-tasks 236
uv run workspace-bench validate --suite build-openbb-backends --min-tasks 12
```

Run built-in baselines:

```bash
uv run workspace-bench run --agent oracle
uv run workspace-bench run --agent noop
uv run workspace-bench report --output runs/reports/benchmark-report.md
```

Committed deterministic certification reports are
`runs/reports/benchmark-report.md` (core) and
`runs/reports/build-apps-benchmark-report.md` (build apps).

Run tests:

```bash
uv run --extra dev pytest
```

## Current build calibration

The current `build-openbb-apps` board is the July 2026 guided interactive
calibration: 236 tasks × 2 repeats (472 strict attempts per model). The repeats
remain separate observations; Wilson intervals and paired McNemar results are
in `runs/reports/significance.json`.

| Model | Strict pass (95% Wilson CI) | State pass | Runtime pass |
| --- | ---: | ---: | ---: |
| OpenAI GPT-5.5 | 128/472 (27.1%; 23.3–31.3%) | 147/472 (31.1%) | 231/472 (48.9%) |
| OpenAI GPT-5.1 | 47/472 (10.0%; 7.6–13.0%) | 98/472 (20.8%) | 275/472 (58.3%) |
| OpenAI GPT-5.4 mini | 15/472 (3.2%; 1.9–5.2%) | 36/472 (7.6%) | 165/472 (35.0%) |

Every row above comes from the replay-only fixed-grader directory
`runs/comparison/build-calibration-202607-regraded/`; each model records
`resumed_cells=472` and `new_cells=0`. The before → after replay comparison is:

| Model | Strict | State | Runtime |
| --- | ---: | ---: | ---: |
| OpenAI GPT-5.5 | 150 → 128 | 181 → 147 | 227 → 231 |
| OpenAI GPT-5.1 | 50 → 47 | 104 → 98 | 271 → 275 |
| OpenAI GPT-5.4 mini | 15 → 15 | 37 → 36 | 165 → 165 |

The conservative relabel review moved seven tasks from medium to hard:
`advanced/case_qa_omni_app`, `aggrid/latency_history`,
`apps/surprise_metric_wrap`, `apps/surveillance_morning`,
`extend/place_alert_metric`, `extend/place_breach_metric`, and
`types/policy_digest_pdf`. No task moved into easy or medium; the measured
distribution is now 55/11/170.

OpenRouter Claude Sonnet 5 and GLM-5.2 are excluded: credit exhaustion caused
362/472 and 357/472 process failures, respectively, with 356 and 349 HTTP 402
responses. Their alphabet-biased valid-attempt slices are limitation evidence
only and never feed measured difficulty.

## Archived Baselines

The committed model runs below predate the current task contract. Their task
ids include the retired generation labels and their prompts/graders differ from
the active corpus. Historical numbers remain for reproducibility and must not
be compared directly with fresh runs. New reports record the Git commit, dirty
state, and suite content hash instead of a hand-maintained release number.

Six models have been run against both suites (pass@1, single fresh
end-to-end attempt per suite, temperature 0, same grader and turn budget
for every model — no patched or spliced results).

Core suite (operating the workspace, 300 tasks):

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

Full per-task results and traces are committed under `runs/comparison/`,
portable rollout JSONL for all 1,800 episodes under `runs/exports/`, the
compiled report at `runs/reports/calibration.json` (built by
`scripts/compile_calibration.py`), and confidence intervals, held-out-split
slices, and all pairwise tests at `runs/reports/significance.json` (built by
`scripts/compute_significance.py`). The current analysis script additionally
reports family-cluster bootstrap intervals; task-IID Wilson and McNemar
statistics are retained only as descriptive historical measures.

Archived pre-debug build-openbb-apps baseline (the former 212-task suite):

| Model | Strict pass | t0 → t4 pass rate (%) |
|---|---|---|
| GPT-5.5 | 212/212 (100.0%) | 100 · 100 · 100 · 100 · 100 |
| GLM-5.2 | 210/212 (99.1%) | 100 · 100 · 100 · 100 · 96 |
| Claude Sonnet 5 | 209/212 (98.6%) | 100 · 98 · 100 · 95 · 100 |
| gpt-4.1-mini ‡ | 153/212 (72.2%) | 95 · 90 · 73 · 63 · 48 |
| gpt-oss:20b | 144/212 (67.9%) | 88 · 68 · 83 · 65 · 44 |
| Qwen3 8B | 30/212 (14.2%) | 28 · 20 · 10 · 10 · 6 |

The top three build scores are not statistically separable at n=212
(GPT-5.5 vs GLM-5.2 p=0.50; GLM-5.2 vs Sonnet 5 p=1.0), and neither are
gpt-4.1-mini vs gpt-oss:20b (p=0.35) — read those as ties. The suite is
saturated at the frontier: its headroom is for small and mid-tier models,
and it doubles as the certification gate for the build-task generator.
Build process failures: gpt-oss:20b 11, GLM-5.2 2, Qwen3 8B 2.

‡ gpt-4.1-mini is the calibration model. The build ladder was accepted only
when its pass rate fell strictly from t0 to t4, so its build curve is a
design target rather than an independent measurement; the other five models
never influenced task selection.

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
  --task core/create/price_performance_aapl \
  --agent-command "python -m workspace_bench.examples.jsonl_rule_agent" \
  --json
```

The harness writes a task envelope JSON file, sets environment variables for the agent command, reads the agent's emitted `tool_calls.jsonl`, executes those calls in the Workspace simulator, and grades the final state.

Run a local Ollama model:

```bash
OLLAMA_MODEL=gpt-oss:20b \
uv run workspace-bench run-agent-command \
  --task core/create/price_performance_aapl \
  --agent-command "python examples/ollama_agent.py" \
  --run-dir runs/ollama \
  --json
```

The Ollama adapter writes `ollama_prompt.txt`, `ollama_response.txt`, and `tool_calls.jsonl` inside the task run directory so you can debug what the model saw and emitted.

Run GPT-4.1 through the OpenAI API:

```bash
cp .env.example .env
# edit .env and set OPENAI_API_KEY

uv run workspace-bench run-agent-command \
  --task core/create/price_performance_aapl \
  --agent-command "python examples/openai_gpt4_1.py" \
  --run-dir runs/openai-gpt-4.1 \
  --json
```

The OpenAI adapter writes `openai_prompt.txt`, `openai_response.txt`, and `tool_calls.jsonl` inside the task run directory.

Run several models side by side — `--model` is repeatable:

```bash
uv run workspace-bench \
  --model openai:gpt-4.1-mini \
  --model ollama:qwen3:8b \
  --suite build-openbb-apps
```

Omit `--task` and the runner covers the whole suite (`--suite
core` or `--suite build-openbb-apps`); add `--family`, `--difficulty`, or
`--tag` to run a slice.

Compare only one difficulty slice:

```bash
uv run workspace-bench \
  --suite core \
  --difficulty easy \
  --timeout 240
```

Run repeated attempts for a more stable comparison:

```bash
uv run workspace-bench \
  --suite core \
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
uv run workspace-bench --model openai:gpt-4.1-mini --task build-openbb-apps/aggrid/revision_grid
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
(`src/workspace_bench/core/task_suites/<suite>/<family>/<id>.json`) — the
`success` block is exactly what the grader checks, and `oracle_tool_calls` is
a known-good solution to diff against.

Run models from a JSON adapter config:

```bash
uv run workspace-bench \
  --models-file examples/models.example.json \
  --suite core \
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
  --task build-openbb-apps/aggrid/auction_calendar
```

Per-episode rows record wall time, input/output/total tokens, API-call count,
and provider-reported cost. A `pricing` block in `--models-file` can supply
published per-million-token input, cached-input, and output prices when the
provider omits cost.

Compile a smoke or full result directory into family×difficulty and per-task
calibration matrices:

```bash
uv run python scripts/compile_calibration.py runs/comparison/<run-id> \
  --output runs/comparison/<run-id>/calibration.json
```

After at least two model result sets exist,
`scripts/propose_measured_difficulty.py` produces a raw band proposal and a
conservatively approved override payload. `--apply-overrides` writes the
approved table to `src/workspace_bench/core/measured_difficulty.json`; the
generator consumes it and verifies the empirical counts.

Use `--suite core|build-openbb-apps` for the stable interactive suites,
`run-code-task` for `build-openbb-backends`, and `--task-dir`
for a private task suite, and `--split train|validation|test` to select a
split. Private suites may also use `dev`. You can also slice with `--capability`, `--workflow`,
`--domain`, and `--subdomain`.

Export a task envelope without running an agent:

```bash
uv run workspace-bench export-task \
  --task core/create/price_performance_aapl \
  --output task.json
```

Export rollouts or SFT data explicitly:

```bash
uv run workspace-bench export-rollouts \
  --oracle \
  --task core/create/price_performance_aapl \
  --output runs/exports/oracle-rollouts.jsonl

uv run workspace-bench export-sft \
  --oracle \
  --task core/create/price_performance_aapl \
  --format openai_messages \
  --output runs/exports/oracle-sft.jsonl
```

You can also export from an evaluator output directory with
`--comparison-dir runs/comparison/<run-id>`. SFT export includes only passing
attempts by default; add `--include-failures` to keep failed attempts with grade
metadata.

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
dirty-worktree flag, suite content hash, schema version, task identity, split,
and model/runner metadata. Prefer passing attempts for SFT, keep failed attempts
only with grade metadata, and do not mix train, validation, test, or hidden
answer data.

## Suites

The benchmark is organized as **suites**: certified sets of tasks that can
be added independently and reported separately or in aggregate. Bundled today:

| suite | tasks | what it measures |
| --- | --- | --- |
| `core` | 300 | operating the workspace (widgets, dashboards, apps, skills, repair) |
| `build-openbb-apps` | 236 | building, diagnosing, repairing, retesting, and opening custom-backend widgets and apps |
| `build-openbb-backends` | 12 | editing, testing, launching, and probing real custom-backend code (experimental v0) |

```bash
# run or validate one suite
uv run workspace-bench validate --suite build-openbb-apps --min-tasks 236
uv run workspace-bench validate --suite build-openbb-backends --min-tasks 12
uv run workspace-bench --models-file examples/models.example.json --suite build-openbb-apps
```

Every suite has to clear the same gates before it counts: the reference
solution passes every task (oracle 100%), a do-nothing agent fails every
task (no-op 0%), independent rubric mutations fail, suite content hashes and the
family/split coverage matches, prompts pass specification-aware linting,
generation-time quotas hold (coverage, empirical difficulty, and structural
specification bands), and graded-check counts stay within per-specification-level
caps so rubric breadth remains anchored to prompt structure.

Per-suite results roll up into one pooled aggregate — task counts are
added across suites, never averaged percentages. Point the report at one
run directory per model per suite:

```bash
# each evaluator invocation writes one run directory per model
uv run python scripts/compile_suites_report.py \
  --run build-openbb-apps=runs/comparison/build-calibration-202607-regraded/openai-gpt-5.5.json \
  --historical-run core=runs/comparison/core-gpt-5.5 \
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
`task_suite.json` can declare `suite_id`, `visibility` (`private` or `hidden`),
and `default_split`. Hidden suites redact prompts from trace artifacts while
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
  --task core/create/price_performance_aapl \
  --json
```

Check the broader live MCP surface against a workflow task:

```bash
uv run --extra live workspace-bench smoke-workspace-mcp \
  --url http://127.0.0.1:8787 \
  --suite core \
  --task core/skills/read_the_finance_earnings_prep_skill \
  --check-surface \
  --json
```

The smoke command emulates the browser bridge with the benchmark simulator. It exercises the real streamable HTTP endpoint, tool schemas, server-side validation, websocket bridge, command translation layer, and session-context updates without requiring a Workspace browser tab. If a real browser is already connected, the command refuses to replace it unless `--replace-browser-session` is passed.

For release audits, `scripts/audit_hosted_surface.py` compares full hosted input
schemas against the committed compatibility baseline, and
`scripts/audit_live_golden_tasks.py` replays a small cross-surface golden set
through the real sidecar transport.

## Browser Certification

Install the optional browser dependency and Chromium once:

```bash
uv sync --extra dev --extra browser
uv run playwright install chromium
```

The required local gates need no Workspace account. Dry-run validates all 30
manifest entries, their oracle backends, runtime-derived evidence, parameters,
columns, tabs, CORS, and live HTTP routes. Self-test drives real Chromium
through the same connection, app/widget placement, interaction, assertion,
screenshot, and trace code used for the product run:

```bash
uv run --extra browser workspace-bench browser-cert --dry-run
uv run --extra browser workspace-bench browser-cert --self-test
```

The flagship code task is an optional additional self-test entry. Start an
agent-built `risk_command_center_product` backend, then add
`--code-task-backend http://127.0.0.1:<port>` to the self-test command. This
does not change the fixed 30-task product subset.

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
`src/workspace_bench/browser/selectors.json`. If the live product differs,
copy that file outside the repository, edit only the selectors, and pass it
with `--selectors PATH`. The local self-test proves the browser, backend, and
artifact layers; it does **not** prove live-product selector or rendering
parity. Keep the no-live-execution claim in place until the real `--all` run
passes and its verdicts are reviewed.

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

Serve one build task's oracle-declared backend and task-owned runtime datasets:

```bash
uv run workspace-bench serve-task-backend \
  --task build-openbb-apps/apps/earnings_desk \
  --port 9102
```

This exposes that task's `widgets.json`, `apps.json`, widget data, parameter
options, and form-submit endpoints with CORS enabled.

## Real-Code Backend Track

Install the optional authoring environment if you want the same packages in
the repository environment (each starter also pins and installs its own):

```bash
uv sync --extra dev --extra codetrack
```

Run any external CLI coding agent in an instantiated starter repository:

```bash
uv run workspace-bench run-code-task \
  --task build-openbb-backends/backend-code/market_movers_table \
  --agent-command "your-agent-command" \
  --timeout 300
```

The command sets `WORKSPACE_BENCH_WORKDIR`, `WORKSPACE_BENCH_TASK_BRIEF`,
`WORKSPACE_BENCH_TASK_JSON`, and `WORKSPACE_BENCH_TASK_ID`. After the agent
exits, the evaluator installs the pinned task environment, starts its FastAPI
process on an ephemeral localhost port, strictly validates manifests and CORS,
probes all declared endpoint/parameter cases, runs non-empty pytest tests, and
checks those tests reject a garbage endpoint implementation. The exact spawned
process is terminated and a `deployment-receipt.json` is left under
`.workspace-bench/` in the task workdir.

## Task & Success Schema

Tasks are strict `workspace-bench-task` JSON objects under
`src/workspace_bench/core/task_suites/<suite>/<family>/`; private
`--task-dir` trees use the same schema. Unknown fields are rejected.

### Task fields

| field | contract |
| --- | --- |
| `schema_version` | Required; `workspace-bench-task`. |
| `id`, `title` | Stable local slug and human-readable title. The public identity is `suite/family/task`. |
| `category`, `family` | Required workflow kind (`read`, `single-widget`, `dashboard`, `platform`, or `repair`) and generator/verifier family. Neither is inferred from paths or tags. |
| `capability`, `workflow`, `domain`, `subdomain` | Required slicing axes: the general action, analyst workflow, broad area, and narrower desk/function. |
| `specification_level` | Required for build tasks; structural prompt level: `explicit`, `partially-specified`, or `open-brief`. |
| `difficulty` | Measured `easy`, `medium`, or `hard` reporting label. |
| `split` | `train`, `validation`, `test`, or private-suite `dev`; otherwise the suite default, then `dev`. |
| `tags`, `source`, `novelty`, `business_terms` | Filtering, provenance, uniqueness, and the declared allowlist of genuine verbatim business identifiers in less-specified prompts. |
| `prompt` | Analyst-facing instruction. |
| `fixtures`, `initial_state` | Deterministic backend references and optional seeded dashboards, tabs, widgets, apps, generated widgets, or repair state. |
| `allowed_tools`, `limits` | Agent-visible Workspace MCP tool surface and budgets such as `max_turns`. |
| `success` | Evaluator-only deterministic `SuccessCriteria`. |
| `oracle_tool_calls` | Known-good reference trajectory; it is evidence, not the only valid solution. |
| `code_task` | Experimental code-track contract: confined starter/oracle paths, argv install/start/test commands, health path, timeouts, manifest requirements, and typed HTTP probes. |

`workspace-bench export-task` publishes prompt, business terms, metadata,
fixtures, initial state, tools, limits, protocol, suite hash, and Git
provenance. It deliberately excludes `success` and `oracle_tool_calls`.
Pre-versioned tasks must be migrated explicitly with `workspace-bench
migrate-task`.

`specification_level` and `difficulty` are independent. Specification level
controls prompt structure, openness linting, exact-versus-capability grading,
and graded-check caps. Difficulty is measured from calibration evidence and
never changes prompt rendering or grader selection. Explicit tasks can name a
complete implementation contract; partially specified tasks provide a business
outcome and one or two declared anchors; open briefs describe the user,
subject, actions, and genuine constraints while leaving ids, widget types,
paths, fields, tabs, and geometry to the agent.

### SuccessCriteria

| field | what it checks |
| --- | --- |
| `required_dashboard_name_contains`, `required_tabs` | Required active-dashboard phrase and tab ids. |
| `required_widgets` | Origin/widget id, subset-matched `data_args`, optional tab, and min/max instance counts. |
| `required_generated_widgets` | Type, optional name/tab, minimum count, and case-insensitive semantic `data_contains` facts. |
| `required_widget_defs`, `required_app_defs` | Exact custom-backend manifest contracts for structurally explicit tasks. |
| `required_capabilities` | Architecture-neutral business capability, bound to runtime datasets by widget kind, covered fields, parameter kinds, and business-significant config. |
| `capability_connections` | Required source/target capability edge through the final app's real shared-parameter graph. |
| `business_names`, `app_structure` | Opt-in business-critical dashboard/app/tab names and generic app/reference/layout integrity. |
| `required_layouts`, `layout` | Exact move/resize outcomes plus grid-bound and no-overlap invariants. |
| `required_tool_calls`, `required_tool_results`, `required_resource_reads` | Nested-subset call arguments and required fragments from successful tool results or exact resource URIs. |
| `trace_checks` | Invalid-call budget, schema-before-create, listed-widget-id discipline, and repeated-snapshot limit. |
| `runtime_checks` | Task-owned datasets and evaluator HTTP probes, with optional pinned paths and request timeout. |
| `workspace_checks` | Preservation of unrelated dashboards/apps/backend ids, warning/name invariants, mutable ids, and dashboard/backend delta bounds. |
| `polish` | Desirable authored details reported separately; never gates strict pass. |

A required capability names one or more `runtime_checks.datasets`, selects a
widget kind (`any`, table/grid/chart-like, metric, form, or a native content
kind), and may require fields, parameter kinds, and meaningful configuration.
Several runtime-valid widgets may jointly cover its fields; one combined widget
may cover compatible capabilities. Connections are derived from actual
`apps.json` shared-parameter groups, so group names and oracle ids are not
compared. Use `business_names` only when the literal name is part of the brief.

Each runtime dataset has a unique `name`, authored `widget_id`, field
vocabulary, JSON `payload`, and optional `path` or `form_endpoint`; negative
fixtures may provide `status` or `raw_body`. Paths are flexible unless
`pinned_paths` is true. The evaluator remaps the authored backend to its own
localhost server, synthesizes representative parameters, issues GET or POST,
and rejects unreachable/non-2xx endpoints, malformed or incompatible JSON,
empty placeholder data, invalid parameter schemas, and broken form submission
contracts.

For generated widgets, `data_contains` is the current semantic contract. It
searches serialized data plus name, description, and tab id case-insensitively,
with supported aliases and numeric equivalence. Legacy `data_equals` remains
accepted for private and older schemas but performs strict payload equality;
bundled suites do not use it.

Oracle traces smoke-test task correctness and can bootstrap SFT/RL exports, but
the grader is the source of truth. For experimental `code_task` entries the
oracle is a solved-file overlay instead; paths cannot escape the task fixture,
commands are argv arrays, every manifest endpoint needs a typed probe, starter
tests must fail before implementation, and the oracle plus test-sensitivity
mutation must pass validation.

The simulator surface includes snapshot, dashboard/navigation, widget
discovery/data/create/update/layout/delete/read, generated-widget, backend/app,
skill/resource/prompt, and delegation tools. The complete per-task oracle-tool
matrix and generated task catalog live under `runs/reports/`.

## Result & Output Schema

All result issues are `{code, message}` objects. A built-in `run --json` emits
`{summary, results}`; external commands and model comparisons also include a
`benchmark` provenance block with benchmark/suite identity, content SHA-256,
Git commit, and dirty-worktree flag.

### Result rows and GradeResult

Every result row identifies the qualified task, family, category, capability,
workflow, domain, subdomain, specification level, difficulty, and tags. Its
grade exposes these dimensions:

| dimension | fields | meaning |
| --- | --- | --- |
| outcome/state | `score`, `state_score`, `state_passed`, state check counts | Correct durable workspace or code outcome. For runtime tasks, primary partial credit averages state and runtime dimension scores rather than raw checks. |
| trace | `trace_score`, `trace_passed`, trace check counts | Required retrieval/tool behavior and workflow-policy discipline. |
| runtime | `runtime_score`, `runtime_passed`, runtime check counts | Real evaluator-owned HTTP usability; neutral defaults when unconfigured. |
| polish | `polish_score`, polish check counts, `polish_issues` | Non-gating authored quality diagnostics. |
| combined | `passed`, total check counts, `issues` | Strict pass requires state, trace, and every configured runtime check; polish is excluded. |

Runtime-enabled rows carry an evaluator-generated `deployment_receipt` (and
other rows use `null`). It records observed backend names, app ids,
instantiated dashboard ids, per-widget endpoint/method/dataset probe outcomes,
issue codes, and aggregate counts. It is derived from final state and real
probes, never authored by the agent or used as a requested success artifact.

External-agent rows additionally record `grade_passed`, command, exit code,
timeout, stdout/stderr, run directory, task path, and output path. Their
`passed` requires both process and grade success. Interactive evaluator files
add model/filter/runner/repeat settings, run timestamps and harness/provider
identity, strict/state/runtime/browser summaries, invalid-call and recovery
metrics, turns, tokens, cost, per-task repeats/pass@k/pass^k, durable manifests,
and checkpoints. Resume is accepted only when model, provider, temperature,
harness revision, suite hash, track, repeats, and ordered task manifest match.

The real-code command emits `workspace-bench-code-result/v0`, containing task,
agent process, strict code grade, artifact paths, and an evaluator-owned
`workspace-bench-code-receipt/v0`. The receipt covers install, server pid/log
tails, manifests, HTTP probes, non-empty pytest results, garbage-mutation test
sensitivity, cleanup, and final grade.

### Rollouts and trace artifacts

`export-rollouts` writes one `workspace-bench-rollout-v1` JSONL object per
episode with `task`, `messages`, `tool_calls`, `tool_results`,
`final_snapshot`, `grade`, and `metadata`. Metadata includes export schema and
time, Git state, suite hash, taxonomy, difficulty, and split; private/hidden
suite metadata is retained when available. `export-sft` converts the same
record to `openai_messages`, `sharegpt`, or `tool_call_jsonl`, while
`export-preferences` selects chosen/rejected attempts for the same model/task.
Per-task trace artifacts retain task metadata and prompt, grade, ordered calls
and results, and final snapshot.

### Issue-code catalog

- State and definition: `dashboard_name`, `missing_tab`, `missing_widget`,
  `too_many_widgets`, `missing_generated_widget`, `layout_mismatch`,
  `layout_out_of_grid`, `layout_overlap`, `missing_custom_backend`,
  `missing_widget_def`, and `missing_app_def`.
- Trace: `missing_tool_call`, `missing_tool_result`, `missing_resource_read`,
  `too_many_invalid_calls`, `schema_not_called_before_create`,
  `unlisted_widget_id`, and `repeated_snapshots`.
- Runtime: `endpoint_unreachable`, `endpoint_bad_status`,
  `endpoint_response_malformed`, `endpoint_response_incompatible`,
  `endpoint_response_placeholder`, `endpoint_params_invalid`, and
  `form_submission_incompatible`.
- Capability: `missing_capability`, `capability_fields_uncovered`,
  `capability_param_missing`, `capability_config_missing`,
  `capability_unconnected`, and `business_name_missing`.
- Repair/preservation: `backend_validation_warnings`,
  `custom_backend_replaced`, `duplicate_custom_backend_name`,
  `collateral_app_change`, and `collateral_dashboard_change`.
- Code track: `code_install_failed`, `code_server_startup_failed`,
  `code_widgets_invalid`, `code_apps_invalid`, `code_cors_missing`,
  `code_probe_coverage_missing`, `code_endpoint_unreachable`,
  `code_endpoint_incompatible`, `code_endpoint_placeholder`,
  `code_tests_failed`, `code_tests_insensitive`, and `code_server_orphaned`.

Polish codes are task-authored (bundled tasks currently use
`polish_refresh_policy`) and appear only in `polish_issues`.

## Grading Model

Strict success is conjunctive: **state ∧ trace ∧ configured runtime**. State is
the durable Workspace/app or code outcome, trace captures required tool use and
discipline, and runtime proves task-owned endpoint behavior over real localhost
HTTP. Polish is observable but non-gating. Partial scores are reported by
dimension; runtime-enabled outcome score is the mean of state and runtime
scores, while trace remains a strict-pass condition.

Capability grading makes less-specified build tasks behavior-first. The oracle
is one witness, not a structural template: alternative solutions may choose
different widget ids, paths, counts, tabs, layouts, or split/merged views when
their runtime-valid widgets jointly expose the required business fields and
parameters, preserve app integrity, and satisfy required interaction edges.
Exact definitions and geometry remain appropriate when the explicit prompt or
core layout outcome requires them.

Grader soundness is certified against **thirteen archetypes** of invalid
solutions: shifted endpoint data, never-instantiated apps, missing widgets,
incompatible values, broken forms, severed interactions, collateral damage,
invalid gating settings, collapsed connected views, field-less contributors,
self-linked connections, note-only proof, and duplicate-backend teardown and
replacement. Each clean oracle must pass immediately before mutation; every
mutant must fail with the issue code attributable to the injected defect.
Survivors, wrong-reason failures, or dirty oracles block release.

See [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) for release gates and
[CONTRIBUTING.md](CONTRIBUTING.md) for task, grader, agent, and export changes.

## Task Organization

Every active task has the canonical identity `suite/family/task`, for example
`core/create/price_performance_aapl`. The local task id contains only the
descriptive slug; generator mechanics are not part of the public identity.

**Category** — what kind of workflow the task is:

- `read`: inspect and answer from an existing dashboard
- `single-widget`: create, update, read, or lay out a single widget
- `dashboard`: build a multi-widget dashboard from analyst requirements
- `platform`: use app templates, tabs, parameter groups, prompts, skills, or delegation
- `repair`: fix incorrect Workspace state or bad metadata assumptions

**Difficulty** — `easy`, `medium`, or `hard`. For `build-openbb-apps` this is
empirical metadata measured in July 2026: 55/11/170. It does not render prompts
or select graders. **Specification level** is the structural axis that does:
60 `explicit`, 92 `partially-specified`, and 84 `open-brief`. Core remains
90/120/90 and the experimental code track is 3/6/3. Every manifest-track build
task exposes the full tool surface, so selecting the right path is evaluated.

## Terminology

For readers arriving from other benchmarks:

| here | elsewhere |
| --- | --- |
| task | Terminal-Bench / Inspect / GAIA / TMax "task" (HELM says "scenario") |
| suite | lm-eval-harness "group"/"suite", Terminal-Bench registry "dataset" |
| difficulty | GAIA "Level 1–3", TMax "complexity buckets" |
| family | METR-style "task family" (generated variations of one capability) |
| category | task type — τ-bench's "domain" plays a similar role |
| rubric / graders | Terminal-Bench "verification test suite", TMax "graded verifiers" |
| oracle | Terminal-Bench "oracle solution" (same word) |

## Repository Layout

```text
src/workspace_bench/
  cli.py                 Command line interface
  core/                  Task dataclasses, bundled tasks, episodes, runner, graders
    task_suites/         Bundled suites, organized as suite/family/task:
      core/                               Core operating suite
        create/ update/ ...                Family directories
      build_openbb_apps/                  Build suite families
  workspace/             Fixture backends, simulator, live workspace-mcp smoke bridge
    data/                Packaged fixture metadata such as Stark widgets/apps
  agents/                Oracle/noop agents, JSONL command protocol, model adapter helpers
  reports/               Model comparison, reliability metrics, charts, analysis reports
  exports/               Rollout, SFT, preference, and metadata export helpers
  rl/                    Gym-style env, action/observation/reward helpers
  __init__.py            Small public convenience surface
scripts/
  generate_gen_pack.py     Core suite generator (families x levels)
  generate_build_apps_suite.py  build-openbb-apps suite generator + certifier
  generate_backend_code_suite.py  12 real-code starters, oracles, and task specs
  generate_stark_data.py   Seeded Stark fixture data baker
  compile_calibration.py   Aggregates calibration runs into runs/reports/calibration.json
  compile_suites_report.py  Pools suites into runs/reports/suites.json
runs/
  comparison/              Historical boards plus the 2026-07 build calibration
  exports/                 Rollout JSONL for the 1,800 core episodes
  reports/                 Compiled reports and generated catalogs/matrices
    task-catalog.md         All 536 stable simulator tasks; code track noted separately
    tool-coverage-matrix.md Per-task x Workspace MCP oracle-tool matrix
    tool-matrix-data.json   Machine-readable data behind the tool matrix
examples/
  jsonl_rule_agent.py       Repo-checkout wrapper for the packaged demo agent
  ollama_agent.py           Local Ollama adapter template
  openai_gpt4_1.py          GPT-4.1 OpenAI API adapter template
  models.example.json       Model comparison adapter config example
tests/
```

## Contamination Canary

```bash
uv run workspace-bench canary
```

Benchmark data should not appear in model training corpora unless explicitly released for training.

## Release Notes

This is an alpha benchmark package. It is ready for local evals, private task suites, CI regression testing, `workspace-mcp` sidecar smoke tests, and local browser-harness self-testing, and it ships with six real model baselines. Before a broader public leaderboard: held-out/hidden task splits and a completed browser-certification run against a real authenticated Workspace.
