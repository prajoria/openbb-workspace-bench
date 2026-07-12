# Result & Output Schema

Reference for evaluator output — result rows, grade dimensions, receipts,
exports, and issue codes. See [README](README.md) for the project overview and
[TASK-SCHEMA](TASK-SCHEMA.md) for the input side.

All result issues are `{code, message}` objects. A built-in `run --json` emits
`{summary, results}`; external commands and model comparisons also include a
`benchmark` provenance block with benchmark/suite identity, content SHA-256,
Git commit, and dirty-worktree flag.

## Result rows and GradeResult

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

## Rollouts and trace artifacts

`export-rollouts` writes one `workspace-bench-rollout-v1` JSONL object per
episode with `task`, `messages`, `tool_calls`, `tool_results`,
`final_snapshot`, `grade`, and `metadata`. Metadata includes export schema and
time, Git state, suite hash, taxonomy, difficulty, and split; private/hidden
suite metadata is retained when available. `export-sft` converts the same
record to `openai_messages`, `sharegpt`, or `tool_call_jsonl`, while
`export-preferences` selects chosen/rejected attempts for the same model/task.
Per-task trace artifacts retain task metadata and prompt, grade, ordered calls
and results, and final snapshot.

## Issue-code catalog

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
