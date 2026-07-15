# `enterprise-apps-usage` task suite

Tasks: 192

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
| `repair` | fix seeded defects, preserve everything else | 0-5 |
| `platform` | skills, workspace prompts, and MCP resources govern correctness | 0-5 |
| `extend` | the data-backend lifecycle, up to writing new manifests | 0-5 |
| `handoff` | durable notes with grounded facts, then delegation | 0-5 |

Each family holds four spines (one target threaded up the ladder; catalog
balance across spines makes Getting Started, Widget Examples, and Daloopa
first-class targets, and all ten workspace skills govern tasks somewhere in
the suite), and the grid is complete — 8 x 6 x 4 — so every level carries
exactly 32 tasks and per-level pass rates rest on equal attempts. Levels add
one difficulty driver each: level0 execute (everything stated, including
param keys), level1 discover, level2 translate policy into declared parameter
values, level3 ambient state under preservation, level4 knowledge-governed
(in half the spines, strictly: a skill, MCP resource, or workspace prompt
named in the prompt determines the graded outcome) or multi-intent work,
level5 build — author `widgets_json`, wrap it in `apps_json`, instantiate,
and use it.

Distinct graded targets per catalog: Bench Stark Enterprise 9/349, Bench
Daloopa 7/10, Getting Started 19/70, Widget Examples 12/30 — spanning tables,
charts, forms with submit inputs, live grids, and media/content widgets.

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

Difficulty calibration (July 2026, on this exact content). gpt-4.1-mini
(two repeats, 64 attempts per level): strict-pass staircase
94% / 72% / 66% / 45% / 14% / 20% across level0-level5 (51.8% overall) — an
achievable floor and a hard top that sits at the gating model's noise
level. The top rungs were verified against GPT-5.5 (single attempt per
task, pooled over all 32 tasks per rung): 78% at level4 and 59% at level5,
so the deep ladder orders correctly and separates frontier models where
the gating model cannot.

## Limitations

The `extend` family grades authored manifests and lifecycle calls without
runtime HTTP probes (unlike `build-openbb-apps`). Live-parity eligibility for
the rebuilt suite is pending re-derivation. Judge-free by design: every check
is a deterministic boolean.
