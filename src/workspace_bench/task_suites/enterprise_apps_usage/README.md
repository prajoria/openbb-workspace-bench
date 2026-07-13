# `enterprise-apps-usage` task suite

Tasks: 300

## Purpose

A pass means the agent can operate a Workspace through the MCP surface: inspect and read data, create and update widgets, arrange dashboards, navigate, use apps and resources, delegate work, and repair seeded state while satisfying the task's durable outcome contract.

## Workspace baseline

The manifest default is `minimal`, but the same 300 task files are certified with both `minimal` and `default-v1`. This is an ablation axis for measuring how much a crowded, realistic workspace costs a model. The baseline override changes only the in-memory suite manifest; it does not copy or alter task files.

```bash
uv run workspace-bench validate --suite enterprise-apps-usage --workspace-baseline minimal --min-tasks 300
uv run workspace-bench validate --suite enterprise-apps-usage --workspace-baseline default-v1 --min-tasks 300
```

| Workspace baseline | Oracle | No-op | Status |
| --- | ---: | ---: | --- |
| `minimal` | 300/300 pass | 300/300 fail | certified |
| `default-v1` | 300/300 pass | 300/300 fail | certified |

Model runs use the same `--workspace-baseline` flag. The effective value is recorded in run manifests, result rows, trace metadata, exports, and compiled reports.

## Generation method

`template-scaled-from-basis`. Fifteen tool-anchored families are expanded into five levels with four tasks per cell by `scripts/generators/generate_usage_suite.py`; generation-time quotas and adversarial certification are release gates. The deterministic phrasing and task assembly mechanics live in `scripts/generators/_assembly/`.

Every widget catalog used by this suite is transcription-grade. `Bench Stark Enterprise` is transcribed from the [Stark Industries demo](https://github.com/DidierRLopes/stark-industries-demo). `Getting Started` is transcribed from `reference-backend/apps.json` and `reference-backend/widgets_*.py` in the real [OpenBB backend examples repository](https://github.com/OpenBB-finance/backend-examples-for-openbb-workspace). `Widget Examples` is transcribed from that repository's `widget-types/`, `parameters-types/`, and `ssrm_mode/` sources. Literal response samples and parameter options are extracted without importing or executing the source backends; unstable dates and binary bodies use explicit stable placeholders. The former Equities, Macro, and Portfolio fixture slugs remain lookup aliases only and expose no invented catalog.

## Axes

Family identifies the anchor capability. Each family contains five structural levels (`r0` through `r4`), with four tasks per level; higher levels add composition, discovery, pathology, and tighter budgets while the anchor capability stays central. Category names the workflow outcome, and difficulty is balanced independently across the level matrix rather than being another name for a level.

| Axis | File-derived counts |
| --- | --- |
| `family` | 15 families, 20 tasks each: `apps`, `backends`, `create`, `delegate`, `delete`, `inspect`, `layout`, `navigate`, `note`, `params`, `prompts`, `read`, `resources`, `skills`, `update` |
| `level` | 5 per family, 4 tasks per family/level cell; 60 tasks at each of `r0`, `r1`, `r2`, `r3`, `r4` |
| `category` | `single-widget` 124; `dashboard` 76; `platform` 40; `repair` 32; `read` 28 |
| `difficulty` | `easy` 90; `medium` 120; `hard` 90 |

## Live parity eligibility

The default live-origin map now includes `Getting Started` and `Widget Examples` as identity mappings alongside `Bench Stark Enterprise` to `Stark Fund`. As a result, 232/300 tasks are eligible for local-to-live structural parity replay: all 20 tasks in each of `create`, `delete`, `inspect`, `layout`, `navigate`, `note`, `params`, `prompts`, `read`, `skills`, and `update`, plus 12 resource tasks. The remaining 68 tasks use backend/app mutation or delegation tools that the conservative replay intentionally refuses. No live test is part of certification.

| Eligibility | Tasks |
| --- | ---: |
| Eligible | 232 |
| Ineligible: backend/app mutation | 48 |
| Ineligible: delegation | 20 |

## Gates

The generator and both baseline validation commands require every reference trace to pass, every no-op trace to fail, rubric mutations to change grades, unique novelty fingerprints and prompts, a matching manifest content hash, and quotas for families, categories, backends, difficulty, widget pairs, and grader-check types. The adversarial audit must also reject certified incorrect behaviors without dirty reference traces or wrong-reason failures.

## Limitations

The simulator uses deterministic fixture data, not live market data, so a pass demonstrates contract-level Workspace operation rather than full live-product parity. The levels are structural pressure settings, while difficulty remains a balanced label pending broader empirical measurement. Public task files include reference traces and success criteria and therefore are not hidden evaluation data.
