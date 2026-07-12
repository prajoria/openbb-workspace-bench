# Contributing to WorkspaceBench

WorkspaceBench should stay benchmark-first. Contributions must preserve the
same task, simulator, trace, and grader contracts used by the CLI, exports, and
RL adapter. Generated task suites and reports are changed through their
generators, never by editing generated artifacts.

## Add a task

1. Edit the relevant family generator for a bundled suite, or copy an existing
   task into a private task directory.
2. Give it a stable `id`, title, family, capability, workflow, domain,
   subdomain, specification level where applicable, difficulty, split, tags,
   provenance, and novelty note.
3. Keep fixture data deterministic and versioned.
4. Add clear `success` criteria that grade durable Workspace state.
5. Add a known-good `oracle_tool_calls` trace.
6. Regenerate the suite twice, confirm deterministic output, and run its
   validation gate.

Private task discovery is recursive through `--task-dir`. The complete task and
success-criteria contract is in [README.md](README.md#task--success-schema).

## Author a build prompt

Generate build-suite prompts from the family modules and shared renderer; do
not edit bundled task JSON. Follow the structural specification contract:

- Keep `explicit` tasks explicit.
- Give `partially-specified` tasks a business outcome plus one or two contract
  anchors, and declare each verbatim anchor in `business_terms`.
- Write `open-brief` tasks as business briefs: identify the user, data subject,
  what they need to see or do, and only genuine named business constraints. Do
  not state widget ids/types, paths, field identifiers, tabs, coordinates, or
  refresh intervals.

Do not add an oracle identifier to `business_terms` merely to silence lint. A
term must be meaningful to the desk, appear in the prompt, and have a matching
behavioral or semantic requirement. Partially specified and open-brief grading
must use `required_capabilities`, runtime datasets, generic app structure, and
optional business names—not exact oracle widget/app definitions or layouts.

```bash
uv run python scripts/generators/generate_build_apps_suite.py
uv run python scripts/audits/audit_task_identity.py
uv run python scripts/audits/report_prompt_stats.py
```

The core and build-suite generators share their deterministic assembly mechanics
in `scripts/generators/_assembly/`. Keep suite policy in small callbacks/configuration
(identity cleanup, artifact prefixes, exceptional cell sizes) rather than adding
a second implementation of phrasing, difficulty, split, novelty, or matrix logic.
After changing either generator, run it twice and verify that the bundled JSON is
unchanged on the second run.

The `debug` family is a fixed 24-task long-repair allocation rather than a
four-task ladder cell. Each task must seed a genuinely broken custom backend,
use task-owned runtime datasets for an agent-visible failed probe and repaired
retest, keep its oracle within 8–20 calls, and set `max_turns` near 2.5 times
the oracle length. Grade the repaired capability and preservation outcome, not
the oracle's inspection sequence. New failure archetypes need a no-op proof and
an independent still-broken repair mutant.

## Author a real-code backend task

Edit `scripts/generators/generate_backend_code_suite.py`; never hand-edit its generated
task JSON, starter repositories, or oracle overlays. A code task must include:

- a unique business brief and provisional difficulty;
- a minimal pinned FastAPI `pyproject.toml`, README, start command, and pytest
  scaffold under its starter fixture;
- an oracle solved-file overlay that does not replace starter tests merely to
  make them pass;
- typed GET/POST probes for every widget and form endpoint, including multiple
  requests where parameter behavior is the capability;
- business fields/types and request-reflecting `expected_values`;
- `require_apps: true` when the task promises an installable app.

Starter tests must fail before implementation; oracle tests must be green and
non-empty. The evaluator also temporarily replaces `app.py` with a garbage
FastAPI catch-all, and repository tests must reject it. Repair and extension
starters should retain at least one already-passing endpoint/test so they
measure regression discipline.

```bash
uv run python scripts/generators/generate_backend_code_suite.py
uv run workspace-bench validate --suite build-openbb-backends --min-tasks 12
uv run pytest -q tests/test_code_tasks.py
```

Run the generator twice and compare hashes. Code tasks are excluded from the
Workspace MCP tool-coverage matrix because their agent surface is filesystem
and process execution, not the simulated tool surface.

## Add a grader check

1. Add the check to `workspace_bench.core.graders` or the relevant runtime/code
   grader.
2. Return a stable, narrow issue code for reports.
3. Keep strict pass/fail separate from partial score and non-gating polish.
4. Add focused unit tests.
5. Confirm the oracle passes, no-op fails, and an independent mutant fails for
   the intended code.

Trace codes include `missing_tool_call`, `missing_tool_result`,
`missing_resource_read`, `too_many_invalid_calls`,
`schema_not_called_before_create`, `unlisted_widget_id`, and
`repeated_snapshots`. Runtime codes include `endpoint_unreachable`,
`endpoint_bad_status`, `endpoint_response_malformed`,
`endpoint_response_incompatible`, `endpoint_response_placeholder`,
`endpoint_params_invalid`, and `form_submission_incompatible`.

Author capabilities against existing `runtime_checks.datasets`; do not create
a parallel field-binding rule. Use the narrowest meaningful widget-kind class,
list only business-critical fields and parameter kinds, and express
interactions through `capability_connections`. The grader derives edges from
actual `apps.json` shared-parameter groups, so group names, ids, tab ids, and
group JSON must not appear in the requirement. Use `business_names` only when
the name itself is part of the brief.

Keep exact `required_layouts` for core move/resize tasks. For build tasks,
prefer `app_structure` plus `layout.within_grid`/`no_overlaps`. Put refresh
cadence and other non-critical presentation conventions in `polish`; polish
checks must never affect `passed`.

Every new gating check also needs an adversarial archetype or an extension to
an existing one in `workspace_bench.core.adversarial`. Define applicability
from task semantics, mutate at the tool-call level when practical, and declare
the narrow issue code caused by that defect. The untouched oracle must grade
cleanly immediately before the mutation, then the invalid candidate must fail
with its expected code. Add a representative test and run:

```bash
uv run workspace-bench adversarial --suite core --family backends
uv run workspace-bench adversarial --suite build-openbb-apps
```

In-memory archetypes run on every applicable task. HTTP/data-side archetypes
use a deterministic sample of three applicable tasks per family by default; a
survivor or wrong-reason failure is a release blocker.

## Add an agent adapter

Prefer the external JSONL command protocol first:

```bash
uv run workspace-bench run-agent-command \
  --task core/create/price_performance_aapl \
  --agent-command "python my_agent.py" \
  --json
```

The adapter reads `WORKSPACE_BENCH_TASK_JSON`,
`WORKSPACE_BENCH_OUTPUT_JSONL`, `WORKSPACE_BENCH_RUN_DIR`, and
`WORKSPACE_BENCH_TASK_ID`, then writes one tool-call object per output line.

For comparison adapters, add an entry to a `--models-file` config rather than
changing built-in defaults. Add published per-million-token pricing and its
reviewable source when the provider omits cost. Large runs should use bounded
`--concurrency`, an `--episode-timeout`, a stable `--output-dir`, and
`--resume`; never combine checkpoints whose manifests differ.

Measured difficulty changes are source-reviewed. Run the proposal script on at
least two complete model result sets, review its raw and conservatively
approved evidence, then use `--apply-overrides` to generate
`src/workspace_bench/core/measured_difficulty.json`. Never edit generated task
labels directly. Relabeling difficulty must not alter specification level,
prompt text, or success criteria.

## Add an export format

1. Keep canonical rollout records unchanged.
2. Add conversion logic under `workspace_bench.exports`.
3. Preserve Git/content provenance, export schema, task, and suite metadata.
4. Add tests in `tests/test_exports.py`.
5. Document the format in the README's
   [Result & Output Schema](README.md#result--output-schema).

## Add RL behavior

Keep RL code as an adapter over the benchmark core:

- actions in `workspace_bench.rl.actions`;
- observations in `workspace_bench.rl.observations`;
- rewards in `workspace_bench.rl.rewards`;
- rollout helpers in `workspace_bench.rl.rollouts`;
- environment wiring in `workspace_bench.rl.env`.

Do not duplicate simulator or grader logic inside the RL package.

## Required checks

Run before submitting:

```bash
uv run pytest -q
uv run ruff check .
uv run mypy src
uv run python scripts/audits/audit_task_identity.py
uv run python scripts/audits/report_prompt_stats.py
uv run python scripts/audits/audit_release_consistency.py
uv run --extra dev workspace-bench validate --suite core --min-tasks 300
uv run --extra dev workspace-bench validate --suite build-openbb-apps --min-tasks 236
uv run --extra dev workspace-bench validate --suite build-openbb-backends --min-tasks 12
uv run workspace-bench runtime-probe --suite core --family backends
uv run workspace-bench runtime-probe --suite build-openbb-apps
```

For evaluator changes, also run the relevant adversarial gates and:

```bash
uv run workspace-bench \
  --models-file examples/models.example.json \
  --difficulty easy \
  --dry-run
```
