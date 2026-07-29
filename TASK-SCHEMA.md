# Task & Success Schema

Reference for authoring task JSON. See [README](README.md) for the
project overview and [CONTRIBUTING](CONTRIBUTING.md) for the authoring workflow.

Tasks are strict JSON objects under
`src/workspace_bench/tasksets/<taskset>/<family>/`; private
`--task-dir` trees use the same schema. Unknown fields are rejected.

## Taskset manifest workspace axes

`taskset.json` selects three independent axes that episode setup layers
beneath every task's own `fixtures` and `initial_state`. Their contents live
under `src/workspace_bench/data/` in one folder per axis
(`backends/`, `initial_states/`, `skills/`):

| field | contract |
| --- | --- |
| `workspace_baseline` | Versioned initial state (which dashboards exist at episode start): `all-stark-enterprise-apps` (Home plus all 23 Stark apps), `stark-workspace-a` (the everything-mounted lived-in workspace: Home, all Stark apps, three personal desk dashboards, all four catalog backends), `stark-onboard-a` (PM/research desk: Home, three opened apps, three personal cross-app dashboards), `stark-onboard-b` (trading/ops desk with a different composition of the same shape), or `""` for explicitly none (bare workspace). A task-level `""` clears a taskset baseline; omitting the field inherits it. |
| `workspace_backends` | Fixture backends connected to the Workspace. Omitted, it falls back to the baseline version's default set; overriding must still include the backends the baseline requires. The Stark data worlds `stark-enterprise` / `stark-enterprise-x` (canonical data) / `stark-enterprise-y` (same catalog; deterministically different row counts, entities, and values, always within each widget's declared schema and options) are interchangeable here — at most one may be connected per episode. |

| `workspace_skills` | Platform skills exposed to the agent, by slug (files under `data/skills/`). Explicit axis: when neither the task nor the taskset manifest declares it, no skills are loaded. |

Tasks may override any axis with the optional task fields of the same names
(state-variant tasks: same prompt, different world); a task value wins over
the taskset manifest on that axis.

Bundled tasksets additionally hold per-taskset authoring profiles through
`workspace-bench validate` release checks (field allowlists and
no-redundant-defaults; the smoke profile is documented in that taskset's
README). The task schema itself is one shared contract.

## Task fields

| field | contract |
| --- | --- |
| `id` | Stable local slug. The public identity is `taskset/family/task`. |
| `category`, `family` | Workflow kind (`read`, `single-widget`, `dashboard`, `platform`, `repair`, or `story` — one persona storyline in the workspace-tasks ladder) and the taskset's grouping family (tool families in smoke, personas in workspace-tasks). `family` may be omitted — the loader derives it from the task's directory. `category` (and `difficulty`) may be omitted when derivable: from the canonical tool-family map, or from the taskset manifest's `task_defaults` (e.g. `{"category": "read", "difficulty": "medium"}` for a uniform taskset). A manifest may also carry `task_defaults.eval` — taskset policy criteria (layout hygiene, trace discipline, preservation) merged into every task's eval block wherever the task file omits the key. |
| `specification_level` | Structural prompt level: `explicit`, `partially-specified`, or `open-brief`. Written only when it deviates from the difficulty default (easy→explicit, medium→partially-specified, hard→open-brief). |
| `difficulty` | Measured `easy`, `medium`, or `hard` reporting label — or a ladder level: `level0`–`level3` in smoke, `level0`–`level4` in workspace-tasks (Execute/Find/Derive/Ground/Compose). Ladder levels 0–2 default to explicit prompts, levels 3–4 to partially specified. (The retired `level5` label remains accepted for backward compatibility and maps to open-brief; no bundled task carries it.) |
| `business_terms` | Optional declared allowlist of genuine verbatim business identifiers in less-specified prompts; omitted when empty. |
| `prompt` | Analyst-facing instruction. |
| `setup` | The world the agent acts in, grouped in one block: `workspace_baseline`, `workspace_backends`, `workspace_skills` (per-task selections/overrides of the taskset manifest's workspace axes, for state-variant tasks), `default_selected_dashboard` (the dashboard already open when the episode starts, by name), `fixtures` (deterministic backend references), `initial_state` (optional seeded dashboards, tabs, widgets, apps, generated widgets, or repair state), and `allowed_tools` (the agent-visible Workspace MCP tool surface, plus optionally the harness-level `final_answer` answer action — a tool-shaped reply that is recorded in the trace, never dispatched to the workspace, and completes the episode). The same fields remain accepted flat at the top level as the legacy spelling. |
| `eval` | The sealed evaluator-only block: deterministic grading criteria (below), `reference_trace` (the known-good reference trajectory — evidence that the task is solvable, not the only valid solution), `reference_answer` (judge-graded tasksets: the model-authored exemplar answer; the reference trace holds only workspace interactions, and the oracle replay synthesizes the `final_answer` submission from this field), and `max_turns` (the harness-enforced turn budget, never shown to agents). `reference`, an eval `limits` block, and `success` + top-level `oracle_tool_calls`/`limits` remain accepted as legacy spellings. |
| `code_task` | Experimental code-track contract: confined starter/oracle paths, argv install/start/test commands, health path, timeouts, manifest requirements, and typed HTTP probes. |

`workspace-bench export-task` publishes prompt, business terms, metadata,
fixtures, initial state, tools, protocol, taskset hash, and Git provenance.
The interactive harness additionally runs **closed-world** by default: the
rendered prompt withholds `initial_state`, so the agent discovers the seeded
workspace through `get_workspace_snapshot`
(`WORKSPACE_BENCH_SHOW_INITIAL_STATE=1` restores the legacy open-world
prompt). It
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
| `calls_match_reference` | Grades the reference trajectory directly: every `reference_trace` call becomes a required call (`args_contains` = its args), except calls annotated `"optional": true` (legitimate to skip, e.g. discovery) or narrowed with `"graded_args": [...]` (only the named args are graded). Mutually exclusive with an explicit `required_tool_calls`. Writing the trajectory under `required_tools` instead of `reference_trace` implies this flag — one field that is both the oracle replay and the graded contract. |
| `required_values_in_answer` | Deterministic answer grading: the episode must end with a `final_answer` submission (the `missing_final_answer` gate applies) and the answer text must contain every listed value (case-insensitive). Pair with an `eval.reference_answer` exemplar so the oracle replay can submit a passing answer. |
| `judge_evaluation` (alias `required_answer_judgment`) | Opt-in binary LLM answer judge over the agent's reply. It always adds a deterministic gate — the episode must end with a `final_answer` submission (`missing_final_answer`) — so no-op baselines fail without a judge. A taskset may define its own judge template in a `JUDGE.md` beside its task families (apps-default's compares the agent's trace and answer against `eval.reference`); tasks without one use the fixed default template. |
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
