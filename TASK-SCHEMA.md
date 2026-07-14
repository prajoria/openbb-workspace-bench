# Task & Success Schema

Reference for authoring task JSON. See [README](README.md) for the
project overview and [CONTRIBUTING](CONTRIBUTING.md) for the authoring workflow.

Tasks are strict JSON objects under
`src/workspace_bench/task_suites/<suite>/<family>/`; private
`--task-dir` trees use the same schema. Unknown fields are rejected.

## Suite manifest workspace axes

`task_suite.json` selects three independent axes that episode setup layers
beneath every task's own `fixtures` and `initial_state`. Their contents live
under `src/workspace_bench/data/` in one folder per axis
(`backends/`, `initial_states/`, `skills/`):

| field | contract |
| --- | --- |
| `workspace_baseline` | Versioned initial state (which dashboards exist at episode start): `all-stark-enterprise-apps` (Home plus all 23 Stark apps), `stark-onboard-a` (PM/research desk: Home, three opened apps, three personal cross-app dashboards), `stark-onboard-b` (trading/ops desk with a different composition of the same shape), or `""` for explicitly none (bare workspace). A task-level `""` clears a suite baseline; omitting the field inherits it. |
| `workspace_backends` | Fixture backends connected to the Workspace. Omitted, it falls back to the baseline version's default set; overriding must still include the backends the baseline requires. The Stark data worlds `stark-enterprise` / `stark-enterprise-x` (canonical data) / `stark-enterprise-y` (same catalog; deterministically different row counts, entities, and values, always within each widget's declared schema and options) are interchangeable here — at most one may be connected per episode. |

| `workspace_skills` | Platform skills exposed to the agent, by slug (files under `data/skills/`). Omitted, all skills are available. |

Tasks may override any axis with the optional task fields of the same names
(state-variant tasks: same prompt, different world); a task value wins over
the suite manifest on that axis.

Bundled suites additionally hold per-suite authoring profiles through
`workspace-bench validate` release checks (field allowlists and
no-redundant-defaults; the smoke profile is documented in that suite's
README). The task schema itself is one shared contract.

## Task fields

| field | contract |
| --- | --- |
| `id` | Stable local slug. The public identity is `suite/family/task`. |
| `category`, `family` | Workflow kind (`read`, `single-widget`, `dashboard`, `platform`, or `repair`) and generator/verifier family. `family` may be omitted — the loader derives it from the task's directory. `category` (and `difficulty`) may be omitted when derivable: from the canonical tool-family map, or from the suite manifest's `task_defaults` (e.g. `{"category": "read", "difficulty": "medium"}` for a uniform suite). |
| `specification_level` | Structural prompt level: `explicit`, `partially-specified`, or `open-brief`. Written only when it deviates from the difficulty default (easy→explicit, medium→partially-specified, hard→open-brief). |
| `difficulty` | Measured `easy`, `medium`, or `hard` reporting label — or, in the smoke ladder, the execution-context level `level0`–`level3` (levels 0–2 default to explicit prompts, level3 to partially specified). |
| `business_terms` | Optional declared allowlist of genuine verbatim business identifiers in less-specified prompts; omitted when empty. |
| `prompt` | Analyst-facing instruction. |
| `setup` | The world the agent acts in, grouped in one block: `workspace_baseline`, `workspace_backends`, `workspace_skills` (per-task selections/overrides of the suite manifest's workspace axes, for state-variant tasks), `default_selected_dashboard` (the dashboard already open when the episode starts, by name), `fixtures` (deterministic backend references), `initial_state` (optional seeded dashboards, tabs, widgets, apps, generated widgets, or repair state), and `allowed_tools` (the agent-visible Workspace MCP tool surface, plus optionally the harness-level `final_answer` answer action — a tool-shaped reply that is recorded in the trace, never dispatched to the workspace, and completes the episode). The same fields remain accepted flat at the top level as the legacy spelling. |
| `eval` | The sealed evaluator-only block: deterministic grading criteria (below), `reference_trace` (the known-good reference trajectory — evidence that the task is solvable, not the only valid solution), `reference_answer` (judge-graded suites: the model-authored exemplar answer; the reference trace holds only workspace interactions, and the oracle replay synthesizes the `final_answer` submission from this field), and `limits` (harness-enforced budgets such as `max_turns`). `reference`, and `success` + top-level `oracle_tool_calls`/`limits`, remain accepted as legacy spellings. |
| `code_task` | Experimental code-track contract: confined starter/oracle paths, argv install/start/test commands, health path, timeouts, manifest requirements, and typed HTTP probes. |

`workspace-bench export-task` publishes prompt, business terms, metadata,
fixtures, initial state, tools, protocol, suite hash, and Git provenance. It
deliberately excludes the entire `eval` block: agents never see grading
criteria, the reference trajectory, or their turn budget — the harness
enforces the budget and refuses calls past `max_turns` — so agents always
pursue the fastest outcome instead of pacing themselves against a known
budget.

`specification_level` and `difficulty` are independent. Specification level
controls prompt structure, openness linting, exact-versus-capability grading,
and graded-check caps. Difficulty is measured from calibration evidence and
never changes prompt rendering or grader selection. Explicit tasks can name a
complete implementation contract; partially specified tasks provide a business
outcome and one or two declared anchors; open briefs describe the user,
subject, actions, and genuine constraints while leaving ids, widget types,
paths, fields, tabs, and geometry to the agent.

## The eval block

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
| `judge_evaluation` (alias `required_answer_judgment`) | Opt-in binary LLM answer judge over the agent's reply. It always adds a deterministic gate — the episode must end with a `final_answer` submission (`missing_final_answer`) — so no-op baselines fail without a judge. A suite may define its own judge template in a `judge.md` beside its task families (apps-default's compares the agent's trace and answer against `eval.reference`); tasks without one use the fixed default template. |
| `trace_checks` | Invalid-call budget, schema-before-create, listed-widget-id discipline, and repeated-snapshot limit. |
| `workspace_checks` | Preservation of unrelated dashboards/apps/backend ids, warning/name invariants, mutable ids, and dashboard/backend delta bounds. |
| `runtime_checks` | Task-owned datasets and evaluator HTTP probes, with optional pinned paths and request timeout. |
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

For generated widgets, `data_contains` is the semantic contract. It searches
serialized data plus name, description, and tab id case-insensitively, with
supported aliases and numeric equivalence.

The `reference` trace smoke-tests task correctness, but the grader is the
source of truth. For experimental `code_task` entries the
oracle is a solved-file overlay instead; paths cannot escape the task fixture,
commands are argv arrays, every manifest endpoint needs a typed probe, starter
tests must fail before implementation, and the oracle plus test-sensitivity
mutation must pass validation.

The simulator surface includes snapshot, dashboard/navigation, widget
discovery/data/create/update/layout/delete/read, generated-widget, backend/app,
skill/resource/prompt, and delegation tools. The complete per-task oracle-tool
matrix and generated task catalog live under `runs/reports/`.
