# `build-openbb-apps` task suite

Tasks: 236

## Purpose

A pass means the agent can turn a product brief into a valid custom Workspace backend and prove the result through durable widget or app state, including diagnosis, repair, retesting, and operation where the task requires them.

## Workspace baseline

The manifest declares no default-workspace version, so the baseline is minimal. Tasks seed their own deterministic backends, broken states, and dashboards as needed, keeping the custom-app outcome independent of the default enterprise workspace.

## Generation method

`agent-authored-certified`. Family modules in `scripts/generators/build_apps_suite/` were written by agents as distinct task definitions rather than scaled from a common basis. `scripts/generators/generate_build_apps_suite.py` assembles them deterministically, certifies them in process, enforces per-specification-level check caps, and applies the measured-difficulty calibration history.

## Axes

Family names the product capability. Ten ladder families each have five functional rungs with four tasks per rung; `e2e` adds full product deliveries and `debug` adds long repair incidents. Specification level describes how much implementation structure the prompt supplies, while difficulty is an independent empirical label from calibration results.

| Axis | File-derived counts |
| --- | --- |
| `family` | `advanced`, `aggrid`, `apps`, `charts`, `extend`, `forms`, `grouping`, `params`, `settings`, `types`: 20 each; `debug`: 24; `e2e`: 12 |
| rung | ladder families: 5 functional rungs, 4 tasks per family/rung cell; plus 24 `debug` and 12 `e2e` tasks |
| `category` | `platform` 192; `repair` 44 |
| effective `specification_level` | `explicit` 60; `partially-specified` 92; `open-brief` 84 |
| `difficulty` | `easy` 17; `medium` 43; `hard` 176 |

The effective specification-level counts reconstruct the difficulty-based default when the JSON omits the field. Rungs progress from a guided widget through app publication, composed workflows, multi-widget briefs, and operation of the built result; they are not difficulty labels.

## Gates

In-process certification and `workspace-bench validate --suite build-openbb-apps` require reference pass, no-op failure, mutation-sensitive grading, distinct prompts, specification-aware prompt lint, unique novelty fingerprints, a matching content hash, widget and parameter ownership quotas, runtime dataset and app-structure coverage, calibrated difficulty and specification-level bands, and graded-check caps. Open briefs are graded through capabilities and outcomes rather than exact reference definitions or layouts.

## Limitations

Runtime-enabled tasks probe evaluator-owned deterministic fixture data rather than live services, and the simulator does not execute agent-written backend code. Difficulty reflects the current calibration history and can change after complete repeated evidence. Passing the suite establishes the graded Workspace outcome, not production security, accessibility, visual polish, or live-browser parity.
