# `enterprise-apps-usage` task suite

Tasks: 300

## Purpose

A pass means the agent can operate a Workspace through the MCP surface: inspect and read data, create and update widgets, arrange dashboards, navigate, use apps and resources, delegate work, and repair seeded state while satisfying the task's durable outcome contract.

## Workspace baseline

The manifest declares no default-workspace version, so the baseline is minimal. Each task seeds only the deterministic fixtures and initial state its graded workflow needs, which isolates operating behavior from the larger product setup.

## Generation method

`template-scaled-from-basis`. Fifteen tool-anchored families are expanded into five rungs with four tasks per cell by `scripts/generators/generate_usage_suite.py`; generation-time quotas and adversarial certification are release gates. The deterministic phrasing and task assembly mechanics live in `scripts/generators/_assembly/`.

## Axes

Family identifies the anchor capability. Each family contains five structural rungs (`r0` through `r4`), with four tasks per rung; higher rungs add composition, discovery, pathology, and tighter budgets while the anchor capability stays central. Category names the workflow outcome, and difficulty is balanced independently across the rung lattice rather than being another name for a rung.

| Axis | File-derived counts |
| --- | --- |
| `family` | 15 families, 20 tasks each: `apps`, `backends`, `create`, `delegate`, `delete`, `inspect`, `layout`, `navigate`, `note`, `params`, `prompts`, `read`, `resources`, `skills`, `update` |
| rung | 5 per family, 4 tasks per family/rung cell; 60 tasks at each of `r0`, `r1`, `r2`, `r3`, `r4` |
| `category` | `single-widget` 124; `dashboard` 76; `platform` 40; `repair` 32; `read` 28 |
| `difficulty` | `easy` 90; `medium` 120; `hard` 90 |

## Gates

The generator and `workspace-bench validate --suite enterprise-apps-usage` require every reference trace to pass, every no-op trace to fail, rubric mutations to change grades, unique novelty fingerprints and prompts, a matching manifest content hash, and quotas for families, categories, backends, difficulty, widget pairs, and grader-check types. The adversarial audit must also reject certified incorrect behaviors without dirty reference traces or wrong-reason failures.

## Limitations

The simulator uses deterministic fixture data, not live market data, so a pass demonstrates contract-level Workspace operation rather than full live-product parity. The rungs are structural pressure settings, while difficulty remains a balanced label pending broader empirical measurement. Public task files include reference traces and success criteria and therefore are not hidden evaluation data.
