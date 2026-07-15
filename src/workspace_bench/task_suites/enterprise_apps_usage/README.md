# `enterprise-apps-usage` task suite

Tasks: 90

## Purpose

Operating a lived-in, everything-mounted workspace: every episode starts on
the `stark-workspace-a` baseline (Home, all Stark Enterprise apps, three
personal desk dashboards) with all four catalog backends connected
(`stark-enterprise-x`, `support-daloopa-skills`, `getting-started`,
`widget-examples`), all ten skills declared, and the full 20-tool surface
allowed. Prompts are business asks — they never name tools, and above the
floor rung they never name raw identifiers: the model connects the dots with
the tools and data available.

## Eight job families x a level ladder

| family | the job | levels |
| --- | --- | --- |
| `retrieve` | find the right data and answer with exact figures (`final_answer`) | 0-5 |
| `curate` | place and configure views, cross-catalog at the top | 0-5 |
| `parameterize` | param surgery and policy translation on existing widgets | 0-5 |
| `organize` | dashboards, tabs, and navigation | 0-5 |
| `repair` | fix seeded defects, preserve everything else | 1-5 |
| `platform` | skills, workspace prompts, and MCP resources govern correctness | 1-5 |
| `extend` | the data-backend lifecycle, up to writing new manifests | 0-5 |
| `handoff` | durable notes with grounded facts, then delegation | 0-4 |

Each family holds two spines (one target threaded up the ladder; catalog
balance across spines makes Getting Started, Widget Examples, and Daloopa
first-class targets). Levels add one difficulty driver each: level0 execute
(everything stated, including param keys), level1 discover, level2 translate
policy into declared parameter values, level3 ambient state under
preservation, level4 knowledge-governed or multi-intent work, level5 build —
author `widgets_json`, wrap it in `apps_json`, instantiate, and use it.

## Grading

Deterministic and outcome-first. Mutations grade final state
(`required_widgets`, `required_tabs`, `required_dashboard_name_contains`);
information tasks grade the trajectory (`required_tools`, where discovery
steps are `optional` and free-form arguments narrow via `graded_args`) plus
exact answer values (`required_values_in_answer`, grounded in served rows);
level5 grades authored definitions (`required_widget_defs`,
`required_app_defs`). Suite policy (layout hygiene, `<=2` invalid calls,
`forbid_invented_widget_ids`, preservation) applies through the manifest's
`task_defaults.eval`. Budgets are `len(required_tools) + 3` turns, hidden
from agents.

## Generation method

`scripts/generators/generate_usage_suite.py` writes every task
(ai-authored-direct) and certifies at generation time: the reference replay
passes and a no-op fails every task; per-level graded-check caps; the
fairness invariant is mechanical (every graded value must be stated in the
prompt, derivable from a stated policy, or the declared catalog default;
graded widget ids require their display name in the prompt or the stated
snake_case convention); cross-catalog target uniqueness (no other widget in
any mounted catalog matches a prompt's discriminating tokens); answer values
must appear literally in the target's served rows; prompt register checks
(<=110 words, no tool names, no shared opening 5-grams).

Difficulty calibration (July 2026, gpt-4.1-mini, two repeats per task):
strict-pass staircase 92% / 59% / 50% / 34% / 6% / 7% across level0-level5 —
strictly decreasing, an achievable floor, and a hard but non-zero top.
gpt-oss:20b failed every task of the pilot calibration rounds and serves as
the below-floor reference point.

## Limitations

The `extend` family grades authored manifests and lifecycle calls without
runtime HTTP probes (unlike `build-openbb-apps`). Live-parity eligibility for
the rebuilt suite is pending re-derivation. Judge-free by design: every check
is a deterministic boolean.
