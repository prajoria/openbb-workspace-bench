# Release Checklist

Use this checklist before announcing a public Workspace Bench release.

## Required

- [ ] `uv run --extra dev ruff check src tests scripts examples` passes.
- [ ] `uv run --extra dev mypy src scripts examples` passes.
- [ ] `uv run --extra dev pytest` passes.
- [ ] `uv run python scripts/audits/audit_task_identity.py` reports 0 findings across 548 tasks, including the 236/236 build-prompt specification lint and 12 experimental code-task identities.
- [ ] `uv run python scripts/audits/report_prompt_stats.py` reports unique prompts within the documented 180-word cap plus current specification-level and measured-difficulty statistics.
- [ ] `uv run python scripts/audits/audit_release_consistency.py` reports zero stale active counts or cross-phase claims across release-facing docs, metadata, CLI text, CI, and tests.
- [ ] `uv run workspace-bench validate --suite core --min-tasks 300` passes with release checks green.
- [ ] `uv run workspace-bench validate --suite build-openbb-apps --min-tasks 236` passes with release checks green.
- [ ] `uv run workspace-bench validate --suite build-openbb-backends --min-tasks 12` starts real servers and reports 12/12 oracle pass, 12/12 starter no-op fail, clean teardown, and both code mutations rejected.
- [ ] `uv run workspace-bench runtime-probe --suite core --family backends` passes 20/20 tasks.
- [ ] `uv run workspace-bench runtime-probe --suite build-openbb-apps` passes every runtime-enabled task, including all 12 e2e capstones.
- [ ] `uv run workspace-bench adversarial --suite core --family backends` reports zero survivors, wrong-reason failures, and dirty oracles (budget: 30 seconds).
- [ ] `uv run workspace-bench adversarial --suite build-openbb-apps` reports zero survivors, wrong-reason failures, and dirty oracles across all 13 archetypes (currently 1,026 applicable candidates; 749 exercised with three runtime samples per applicable family/archetype; budget: 60 seconds).
- [ ] `uv run --extra browser workspace-bench browser-cert --dry-run` passes all 30 certification entries with the exact 4/4/4/4/4/4/3/3 category counts.
- [ ] `uv run --extra browser workspace-bench browser-cert --self-test` passes all three marked tasks in real Chromium and writes PNG, trace ZIP, and verdict JSON artifacts.
- [ ] Optional code flagship browser self-test passes by adding `--code-task-backend http://127.0.0.1:<port>` for an oracle/agent-built `risk_command_center_product` backend; terminate only that tracked backend PID afterward.
- [ ] `uv run workspace-bench run --agent oracle` passes all core tasks; the two other stable/code suites use their suite-specific commands above.
- [ ] `uv run workspace-bench run --agent noop` fails every core task; the suite validations prove their own no-op baselines.
- [ ] `uv run --extra dev workspace-bench export-task --task core/create/price_performance_aapl --output /tmp/workspace-task.json` succeeds.
- [ ] `uv run --extra dev workspace-bench run-agent-command --task core/create/price_performance_aapl --agent-command "python -m workspace_bench.agents.rule_agent"` passes.
- [ ] `uv run workspace-bench report --suite core --output runs/reports/benchmark-report.md` succeeds.
- [ ] `uv run --extra live python scripts/audits/audit_hosted_surface.py` reports no missing tools, prompts, or resources against the hosted Workspace MCP (needs `WORKSPACE_MCP_TOKEN` in `.env`).
- [ ] Stable task counts: exactly 300 in `core`, exactly 236 in `build-openbb-apps` (536 total); experimental `build-openbb-backends` is exactly 12 and reported separately.
- [ ] Split counts are 150/75/75 (`core`) and 118/59/59 (`build-openbb-apps`) train/validation/test, with every family/level or debug-family allocation contributing validation and test tasks.
- [ ] Novelty fingerprints and task ids are unique in both suites.
- [ ] Coverage quotas pass in both suites via `validate` (core: backend, difficulty, widget-pair, dashboard-category, grader-check quotas; build-openbb-apps: widget/param ownership, 55/11/170 measured difficulty, 60/92/84 specification levels, and per-specification-level check caps).
- [ ] `runs/reports/calibration.json` is compiled from the three complete 2026-07 guided runs; OpenRouter credit failures appear only as excluded limitations.
- [ ] Difficulty relabel review requires both repeats, retains one-episode knife edges, and forces zero-pass debug tasks hard; prompt+success hashes are unchanged for every relabel.
- [ ] `runs/reports/suites.json` uses the three current build runs and marks core historical/pre-rename with a pending re-run, excluding cross-era pooling.
- [ ] `runs/reports/significance.json` is recomputed (`workspace-bench compile significance`) and the README board notes match it; paired build episodes retain both repeats.
- [ ] README quick start, suites table, and aggregate command are accurate.
- [ ] `runs/reports/task-catalog.md` is regenerated and covers both stable simulator suites (536 entries); `tool-coverage-matrix.md` and `tool-matrix-data.json` are regenerated beside it.
- [ ] `uv run python scripts/generators/generate_backend_code_suite.py` is deterministic across two runs; starter/oracle fixtures are generator-owned and excluded from the Workspace MCP tool matrix.
- [ ] `uv run pytest -q tests/test_code_tasks.py` proves real HTTP execution, non-empty/test-sensitive pytest enforcement, agent workdir envelopes, and no orphan process.
- [ ] Root `CONTRIBUTING.md` explains how to add tasks and suites.
- [ ] Repository URL in `pyproject.toml` is correct.
- [ ] License decision is made before open-source publication.
- [ ] `uv lock --check` passes and `uv build` produces both sdist and wheel.
- [ ] CI is green.

## Strongly Recommended Before Wider Launch

- [ ] Add at least one real Workspace MCP sidecar parity run.
- [ ] Run the full browser subset against a real authenticated Workspace (one-time human login, then certification):

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

  If selectors have drifted, copy `src/workspace_bench/browser/selectors.json`
  outside the repository and add `--selectors PATH` to the second command.
- [ ] Add a hidden or held-out task split.
- [ ] Add an optional Docker or compose workflow for fixture backend serving.
- [ ] Publish a short benchmark report with coverage, baselines, and limitations.

## Claims to Avoid Until Verified

- Do not claim live OpenBB Workspace execution from dry-run or mock self-test results. Lift the claim only after the real `browser-cert --all` run passes and its screenshots, traces, network checks, and verdicts are reviewed.
- Do not claim financial reasoning coverage beyond the included deterministic fixture domains.
