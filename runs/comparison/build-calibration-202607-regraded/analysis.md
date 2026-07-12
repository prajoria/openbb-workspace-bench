# Workspace Bench Model Comparison

- Benchmark: `openbb-workspace-bench`
- Git commit: `22f477c86823c26b67241e5a525169dc77041c6f`
- Git dirty: `True`
- Tasks: `236`
- Attempts: `472`
- Filters: `{"category": null, "difficulty": "all", "family": null, "split": null, "suite": "build-openbb-apps", "task_dir": null, "track": "guided"}`
- Runner: `interactive`
- Repeats: `2`

## How To Read This

`pass_rate` is strict task success: a task counts as passed only when every grader check passes and the agent process exits cleanly.
`task_pass_rate` excludes provider/process failures and asks whether valid attempts satisfied the grader.
`mean_score` is partial credit: it averages each task's fraction of passed checks.
`pass@k` counts a task when at least one repeat passes. `pass^k` counts it only when every repeat passes.
Two models can therefore have the same pass rate but different mean scores when they pass the same number of tasks but fail with different severity.

## Summary

| Model | Strict Passed | Attempts | Strict Pass Rate | Task Pass Rate | Mean Score | Task Failures | Process Failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenAI GPT-5.1 | 36 | 472 | 7.6% | 7.6% | 62.1% | 436 | 0 |
| OpenAI GPT-5.4 mini | 12 | 472 | 2.5% | 2.9% | 26.1% | 395 | 65 |
| OpenAI GPT-5.5 | 105 | 472 | 22.2% | 22.2% | 65.3% | 367 | 0 |

## Reliability

| Model | pass@k | pass^k | Tasks | k Range |
| --- | ---: | ---: | ---: | ---: |
| OpenAI GPT-5.1 | 9.3% | 5.9% | 236 | 2 |
| OpenAI GPT-5.4 mini | 4.7% | 0.4% | 236 | 2 |
| OpenAI GPT-5.5 | 24.6% | 19.9% | 236 | 2 |

## By Difficulty

| Model | Easy | Medium | Hard |
| --- | ---: | ---: | ---: |
| OpenAI GPT-5.1 | 24/34 (71%) | 12/86 (14%) | 0/352 (0%) |
| OpenAI GPT-5.4 mini | 2/34 (6%) | 10/86 (12%) | 0/352 (0%) |
| OpenAI GPT-5.5 | 29/34 (85%) | 76/86 (88%) | 0/352 (0%) |

## By Category

| Model | read | single-widget | dashboard | platform | repair |
| --- | ---: | ---: | ---: | ---: | ---: |
| OpenAI GPT-5.1 | - | - | - | 16/384 (4%) | 20/88 (23%) |
| OpenAI GPT-5.4 mini | - | - | - | 10/384 (3%) | 2/88 (2%) |
| OpenAI GPT-5.5 | - | - | - | 72/384 (19%) | 33/88 (38%) |

## Task Issue Counts

### OpenAI GPT-5.1

| Issue Code | Count |
| --- | ---: |
| `capability_fields_uncovered` | 528 |
| `capability_param_missing` | 481 |
| `missing_capability` | 429 |
| `endpoint_response_incompatible` | 195 |
| `widget_list_not_called_before_use` | 98 |
| `widget_def_mismatch` | 88 |
| `capability_config_missing` | 87 |
| `schema_not_called_before_create` | 86 |
| `unexpected_dashboard_created` | 81 |
| `capability_unconnected` | 81 |
| `endpoint_unreachable` | 63 |
| `form_submission_incompatible` | 56 |
| `missing_generated_widget` | 49 |
| `too_many_invalid_calls` | 25 |
| `missing_widget` | 16 |
| `app_def_mismatch` | 11 |
| `dashboard_name` | 8 |
| `app_layout_overlap` | 7 |
| `missing_tool_call` | 6 |
| `duplicate_custom_backend_name` | 6 |
| `missing_app_def` | 5 |
| `backend_validation_warnings` | 4 |
| `missing_custom_backend` | 4 |
| `collateral_app_change` | 4 |
| `layout_overlap` | 3 |
| `app_prompts_missing` | 3 |
| `missing_widget_def` | 2 |

### OpenAI GPT-5.4 mini

| Issue Code | Count |
| --- | ---: |
| `missing_capability` | 842 |
| `capability_fields_uncovered` | 627 |
| `capability_param_missing` | 575 |
| `endpoint_unreachable` | 286 |
| `widget_list_not_called_before_use` | 98 |
| `capability_config_missing` | 90 |
| `missing_widget` | 84 |
| `capability_unconnected` | 84 |
| `missing_generated_widget` | 70 |
| `missing_custom_backend` | 50 |
| `app_def_mismatch` | 23 |
| `widget_def_mismatch` | 22 |
| `missing_app_def` | 15 |
| `too_many_invalid_calls` | 14 |
| `dashboard_name` | 13 |
| `unlisted_widget_id` | 12 |
| `schema_not_called_before_create` | 12 |
| `business_name_missing` | 11 |
| `endpoint_response_incompatible` | 10 |
| `form_submission_incompatible` | 8 |
| `unexpected_dashboard_created` | 8 |
| `backend_validation_warnings` | 8 |
| `missing_tool_call` | 6 |
| `duplicate_custom_backend_name` | 6 |
| `endpoint_params_invalid` | 4 |
| `app_layout_ref_invalid` | 3 |
| `app_prompts_missing` | 2 |

### OpenAI GPT-5.5

| Issue Code | Count |
| --- | ---: |
| `capability_fields_uncovered` | 479 |
| `capability_param_missing` | 445 |
| `endpoint_response_incompatible` | 438 |
| `missing_capability` | 283 |
| `capability_config_missing` | 83 |
| `capability_unconnected` | 78 |
| `widget_list_not_called_before_use` | 65 |
| `missing_generated_widget` | 46 |
| `unexpected_dashboard_created` | 35 |
| `form_submission_incompatible` | 22 |
| `app_def_mismatch` | 14 |
| `missing_widget` | 9 |
| `widget_def_mismatch` | 9 |
| `missing_tool_call` | 6 |
| `duplicate_custom_backend_name` | 6 |
| `dashboard_name` | 4 |
| `missing_custom_backend` | 4 |
| `app_prompts_missing` | 4 |
| `endpoint_unreachable` | 3 |
| `missing_app_def` | 2 |
| `too_many_invalid_calls` | 1 |

## Process Failures

| Model | Task | Repeat | Exit Code | Timed Out | Stderr Preview |
| --- | --- | ---: | ---: | --- | --- |
| OpenAI GPT-5.4 mini | case_intake_room | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | case_notes | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | case_room_omni_room | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | catalyst_calendar | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | chains_table_app | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | click_summary_desk | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | diagnose_earnings | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | diagnose_rates | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | evidence_files_ship | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | execution_ship | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | full_earnings_sync | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | orders_ops_stream_room | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | phase_mix_vegalite | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | sla_runbook_app | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | trial_catalysts_app | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | trial_catalysts_app | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | tvl_ship | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vendor_intake_form_app | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vendor_intake_room | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vendor_review_form | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vendor_sla_table_app | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | venue_pdf | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vix_room_chart_room | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vol_commentary | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vol_overview | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vol_ship | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vol_symbol_chart | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | windowed_vix_slice | 1 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | alert_metric_room | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | alert_metric_wrap | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | case_intake_room | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | case_qa_omni_app | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | case_room_omni_room | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | chains_heatmap_html | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | chains_highchart | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | chains_highchart_room | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | earnings_ship | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | evidence_files_app | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | full_earnings_sync | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | gas_metric | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | gas_metric_room | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | healthcare_ship | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | kpi_tabs_table | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | macro_advanced_chart_room | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | modify_case_notes | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | modify_rates_commentary | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | open_orders | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | phase_mix_vegalite | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | rates_morning | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | research_room | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | sla_newsfeed_app | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | sla_ship | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | sla_ship | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | trial_intake_room | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | tvl_ship | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vendor_dangling_app | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vendor_intake_room | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vendor_sla_table_app | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vendor_sla_table_app | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | venue_exception_form_app | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vix_history | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vix_room_chart_room | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vol_commentary | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | vol_commentary_room | 2 | 1 | False | turn 1 did not include a tool name |
| OpenAI GPT-5.4 mini | windowed_vix_slice | 2 | 1 | False | turn 1 did not include a tool name |

## Task Matrix

| Task | Category | Difficulty | OpenAI GPT-5.1 | OpenAI GPT-5.4 mini | OpenAI GPT-5.5 |
| --- | --- | --- | ---: | ---: | ---: |
| build-openbb-apps/forms/access_review_form | platform | medium | 0/2 avg=0.750 (schema_not_called_before_create,widget_list_not_called_before_use,form_submission_incompatible) | 0/2 avg=0.250 (form_submission_incompatible,missing_widget,missing_custom_backend) | 2/2 avg=1.000 |
| build-openbb-apps/extend/add_catalyst_metric | repair | medium | 0/2 avg=1.000 (schema_not_called_before_create,widget_list_not_called_before_use) | 1/2 avg=0.733 (missing_widget) | 1/2 avg=0.733 (widget_list_not_called_before_use,missing_widget) |
| build-openbb-apps/extend/add_curve_spread_metric | repair | easy | 0/2 avg=1.000 (widget_list_not_called_before_use,schema_not_called_before_create) | 0/2 avg=0.400 (missing_widget) | 1/2 avg=0.733 (widget_list_not_called_before_use,missing_widget) |
| build-openbb-apps/extend/add_exception_metric | repair | easy | 0/2 avg=0.167 (missing_widget,endpoint_response_incompatible) | 0/2 avg=0.333 (missing_widget) | 1/2 avg=1.000 (widget_list_not_called_before_use) |
| build-openbb-apps/extend/add_vol_regime_metric | repair | hard | 0/2 avg=1.000 (schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=0.333 (missing_widget) | 0/2 avg=1.000 (widget_list_not_called_before_use) |
| build-openbb-apps/settings/alert_metric_app | platform | easy | 2/2 avg=1.000 | 2/2 avg=1.000 | 2/2 avg=1.000 |
| build-openbb-apps/settings/alert_metric_room | platform | hard | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.062, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.719 (capability_fields_uncovered,missing_capability,capability_param_missing) |
| build-openbb-apps/apps/alert_metric_wrap | platform | easy | 2/2 avg=1.000 | 0/2 avg=0.083, proc=1 (missing_custom_backend,missing_widget,endpoint_unreachable) | 2/2 avg=1.000 |
| build-openbb-apps/aggrid/alert_queue_app | platform | hard | 0/2 avg=0.792 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.625 (missing_capability,widget_list_not_called_before_use,capability_fields_uncovered) | 0/2 avg=0.604 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/settings/auction_cache_grid | platform | hard | 0/2 avg=0.750 (schema_not_called_before_create,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.125 (widget_list_not_called_before_use,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/aggrid/auction_calendar | platform | medium | 0/2 avg=0.940 (widget_def_mismatch,schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=1.000 (unexpected_dashboard_created,schema_not_called_before_create,widget_list_not_called_before_use) | 2/2 avg=1.000 |
| build-openbb-apps/aggrid/auction_watch | platform | hard | 0/2 avg=0.688 (capability_fields_uncovered,capability_config_missing,schema_not_called_before_create) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.125 (widget_list_not_called_before_use,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/types/call_replay_video | platform | hard | 0/2 avg=0.438 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.625 (capability_fields_uncovered,capability_param_missing,widget_list_not_called_before_use) |
| build-openbb-apps/aggrid/case_aging | platform | hard | 0/2 avg=0.458 (capability_fields_uncovered,missing_capability,endpoint_response_incompatible) | 0/2 avg=0.062 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.438 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/apps/case_command | platform | hard | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.882 (capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/forms/case_escalation_form_app | platform | hard | 0/2 avg=0.475 (widget_def_mismatch,form_submission_incompatible,too_many_invalid_calls) | 0/2 avg=0.325 (missing_custom_backend,missing_widget,endpoint_unreachable) | 0/2 avg=0.500 (form_submission_incompatible) |
| build-openbb-apps/forms/case_intake_room | platform | hard | 0/2 avg=0.338 (capability_param_missing,form_submission_incompatible,missing_capability) | 0/2 avg=0.000, proc=2 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.238 (capability_param_missing,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/params/case_notes | platform | medium | 0/2 avg=1.000 (schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=0.438, proc=1 (missing_widget,missing_custom_backend,endpoint_unreachable) | 2/2 avg=1.000 |
| build-openbb-apps/params/case_notes_app | platform | hard | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.062 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.292 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/types/case_notes_room | platform | hard | 0/2 avg=0.408 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.100 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.449 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/advanced/case_prompt_omni | platform | hard | 0/2 avg=0.792 (capability_fields_uncovered,capability_param_missing,schema_not_called_before_create) | 0/2 avg=0.438 (capability_fields_uncovered,capability_param_missing,schema_not_called_before_create) | 0/2 avg=0.500 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/advanced/case_qa_omni | platform | medium | 0/2 avg=1.000 (schema_not_called_before_create,widget_list_not_called_before_use) | 1/2 avg=1.000 (widget_list_not_called_before_use) | 2/2 avg=1.000 |
| build-openbb-apps/advanced/case_qa_omni_app | platform | hard | 0/2 avg=0.479 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.062, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.833 (capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/advanced/case_qa_omni_ship | platform | hard | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.688 (capability_fields_uncovered,capability_param_missing,missing_generated_widget) |
| build-openbb-apps/advanced/case_room_omni_room | platform | hard | 0/2 avg=0.560 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) | 0/2 avg=0.000, proc=2 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.518 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/e2e/case_triage | platform | hard | 0/2 avg=0.611 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.286 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.741 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/e2e/catalyst_calendar | platform | hard | 0/2 avg=0.352 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) | 0/2 avg=0.143, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.704 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/settings/catalyst_metric_app | platform | medium | 1/2 avg=0.958 (app_def_mismatch,missing_widget) | 0/2 avg=0.556 (missing_widget,missing_custom_backend,endpoint_unreachable) | 2/2 avg=1.000 |
| build-openbb-apps/apps/catalyst_metric_wrap | platform | hard | 0/2 avg=0.537 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,endpoint_unreachable) | 0/2 avg=0.425 (endpoint_response_incompatible,capability_fields_uncovered,missing_capability) |
| build-openbb-apps/apps/chain_deck | platform | hard | 0/2 avg=0.740 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.333 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/charts/chain_flow_highchart | platform | hard | 0/2 avg=0.743 (capability_fields_uncovered,capability_param_missing,capability_config_missing) | 0/2 avg=0.100 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.700 (capability_fields_uncovered,capability_param_missing,capability_config_missing) |
| build-openbb-apps/aggrid/chain_flows | platform | hard | 0/2 avg=0.333 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,endpoint_unreachable) | 0/2 avg=0.333 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/e2e/chain_flows | platform | hard | 0/2 avg=0.387 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) | 0/2 avg=0.214 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.352 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/types/chains_heatmap_html | platform | medium | 0/2 avg=1.000 (schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=0.500, proc=1 (widget_list_not_called_before_use,missing_widget,missing_custom_backend) | 2/2 avg=1.000 |
| build-openbb-apps/charts/chains_highchart | platform | medium | 0/2 avg=1.000 (schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=0.438, proc=1 (missing_widget,missing_custom_backend,endpoint_unreachable) | 2/2 avg=1.000 |
| build-openbb-apps/charts/chains_highchart_app | platform | medium | 2/2 avg=1.000 | 0/2 avg=0.208 (missing_custom_backend,missing_widget,endpoint_unreachable) | 1/2 avg=0.958 (app_def_mismatch,missing_widget) |
| build-openbb-apps/charts/chains_highchart_room | platform | hard | 0/2 avg=0.643 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.050, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.601 (capability_fields_uncovered,capability_param_missing,capability_unconnected) |
| build-openbb-apps/aggrid/chains_table_app | platform | medium | 0/2 avg=0.970 (widget_def_mismatch) | 0/2 avg=0.417, proc=1 (missing_widget,missing_custom_backend,dashboard_name) | 2/2 avg=1.000 |
| build-openbb-apps/grouping/chart_note_board | platform | medium | 2/2 avg=1.000 | 1/2 avg=0.867 (app_def_mismatch,missing_widget) | 0/2 avg=0.967 (app_def_mismatch) |
| build-openbb-apps/grouping/chart_preview_sync | platform | hard | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.571 (capability_fields_uncovered,capability_param_missing,capability_unconnected) |
| build-openbb-apps/grouping/chart_sync_live | platform | hard | 0/2 avg=0.514 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.214 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.296 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/grouping/click_preview_desk | platform | hard | 0/2 avg=0.429 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) | 0/2 avg=0.100 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.470 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/grouping/click_revision_desk | platform | hard | 0/2 avg=0.762 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.050 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.321 (missing_capability,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/grouping/click_season_desk | platform | hard | 0/2 avg=0.500 (capability_fields_uncovered,capability_param_missing,capability_unconnected) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.232 (missing_capability,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/grouping/click_summary_desk | platform | hard | 0/2 avg=0.583 (capability_fields_uncovered,capability_param_missing,capability_unconnected) | 0/2 avg=0.000, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.304 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/grouping/click_sync_live | platform | hard | 0/2 avg=0.143 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.071 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.484 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/forms/compliance_ship | platform | hard | 0/2 avg=0.333 (capability_param_missing,form_submission_incompatible,missing_capability) | 0/2 avg=0.250 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.500 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/e2e/compliance_surveillance | platform | hard | 0/2 avg=0.713 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) | 0/2 avg=0.286 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.778 (capability_fields_uncovered,endpoint_response_incompatible,capability_param_missing) |
| build-openbb-apps/forms/curve_comment_form_app | platform | hard | 0/2 avg=0.292 (capability_param_missing,form_submission_incompatible,missing_capability) | 0/2 avg=0.125 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.292 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/types/curve_monitor_iframe_app | platform | medium | 0/2 avg=0.975 (widget_def_mismatch) | 0/2 avg=0.500 (missing_widget,missing_custom_backend,missing_app_def) | 2/2 avg=1.000 |
| build-openbb-apps/extend/diagnose_earnings | repair | hard | 0/2 avg=1.000 (unexpected_dashboard_created) | 0/2 avg=0.000, proc=1 (widget_list_not_called_before_use,missing_capability,capability_fields_uncovered) | 0/2 avg=0.750 (unexpected_dashboard_created,endpoint_response_incompatible) |
| build-openbb-apps/extend/diagnose_healthcare | repair | hard | 0/2 avg=1.000 (unexpected_dashboard_created) | 0/2 avg=0.000 (widget_list_not_called_before_use,missing_capability,capability_fields_uncovered) | 0/2 avg=1.000 (unexpected_dashboard_created) |
| build-openbb-apps/extend/diagnose_rates | repair | hard | 0/2 avg=0.525 (app_layout_overlap,unexpected_dashboard_created,missing_capability) | 0/2 avg=0.000, proc=1 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) | 0/2 avg=0.750 (unexpected_dashboard_created,endpoint_response_incompatible) |
| build-openbb-apps/extend/diagnose_sla | repair | hard | 0/2 avg=0.700 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.125 (widget_list_not_called_before_use,missing_capability,capability_fields_uncovered) | 0/2 avg=1.000 (unexpected_dashboard_created) |
| build-openbb-apps/types/earnings_calls_video_app | platform | hard | 0/2 avg=0.417 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) | 0/2 avg=0.062 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.458 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/types/earnings_calls_video_room | platform | hard | 0/2 avg=0.334 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.050 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.518 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/charts/earnings_chart | platform | hard | 0/2 avg=0.960 (widget_def_mismatch,schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=0.915 (widget_def_mismatch,widget_list_not_called_before_use,missing_widget) | 0/2 avg=0.980 (widget_def_mismatch,widget_list_not_called_before_use) |
| build-openbb-apps/grouping/earnings_chart_app | platform | hard | 0/2 avg=0.971 (widget_def_mismatch,app_def_mismatch) | 0/2 avg=0.700 (app_def_mismatch,endpoint_response_incompatible,missing_widget) | 0/2 avg=0.988 (app_def_mismatch) |
| build-openbb-apps/charts/earnings_chart_app | platform | hard | 0/2 avg=0.518 (capability_fields_uncovered,capability_param_missing,capability_config_missing) | 0/2 avg=0.050 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.393 (capability_fields_uncovered,capability_param_missing,capability_config_missing) |
| build-openbb-apps/charts/earnings_chart_room | platform | hard | 0/2 avg=0.594 (capability_param_missing,capability_fields_uncovered,missing_capability) | 0/2 avg=0.042 (missing_capability,capability_param_missing,capability_fields_uncovered) | 0/2 avg=0.609 (capability_param_missing,capability_fields_uncovered,capability_config_missing) |
| build-openbb-apps/apps/earnings_command | platform | hard | 0/2 avg=0.104 (capability_fields_uncovered,capability_param_missing,capability_unconnected) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.167 (capability_fields_uncovered,capability_param_missing,capability_unconnected) |
| build-openbb-apps/apps/earnings_desk | platform | hard | 0/2 avg=0.421 (capability_fields_uncovered,endpoint_response_incompatible,capability_param_missing) | 0/2 avg=0.050 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.375 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/grouping/earnings_note_app | platform | hard | 0/2 avg=0.479 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) | 0/2 avg=0.062 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.542 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/params/earnings_param_review | platform | hard | 0/2 avg=0.806 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.367 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.278 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/grouping/earnings_review_sync | platform | hard | 0/2 avg=0.714 (capability_fields_uncovered,capability_param_missing,capability_unconnected) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.714 (capability_fields_uncovered,capability_param_missing,capability_unconnected) |
| build-openbb-apps/e2e/earnings_season | platform | hard | 0/2 avg=0.431 (capability_fields_uncovered,missing_capability,endpoint_response_incompatible) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,missing_generated_widget) | 0/2 avg=0.699 (missing_generated_widget,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/charts/earnings_ship | platform | hard | 0/2 avg=0.406 (capability_fields_uncovered,missing_capability,capability_param_missing) | 0/2 avg=0.214 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.671 (capability_fields_uncovered,endpoint_response_incompatible,capability_param_missing) |
| build-openbb-apps/aggrid/earnings_ship | platform | hard | 0/2 avg=0.375 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.125, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.500 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/params/earnings_ship | platform | hard | 0/2 avg=0.818 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.417 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/grouping/earnings_symbol_board | platform | hard | 0/2 avg=0.983 (app_def_mismatch,too_many_invalid_calls) | 0/2 avg=0.333 (missing_widget,missing_app_def,too_many_invalid_calls) | 0/2 avg=0.967 (app_def_mismatch) |
| build-openbb-apps/grouping/earnings_sync_live | platform | hard | 0/2 avg=0.515 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.107 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.296 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/grouping/estimate_revisions_app | platform | hard | 0/2 avg=0.971 (widget_def_mismatch,app_def_mismatch) | 0/2 avg=0.167 (missing_custom_backend,missing_widget,endpoint_unreachable) | 0/2 avg=0.988 (app_def_mismatch) |
| build-openbb-apps/aggrid/estimates_ssrm | platform | hard | 0/2 avg=0.975 (schema_not_called_before_create,widget_def_mismatch,widget_list_not_called_before_use) | 0/2 avg=0.975 (widget_def_mismatch,widget_list_not_called_before_use) | 0/2 avg=0.475 (widget_def_mismatch,endpoint_response_incompatible) |
| build-openbb-apps/types/evidence_files_app | platform | hard | 0/2 avg=0.542 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.062, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.521 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/types/evidence_files_room | platform | hard | 0/2 avg=0.100 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.050 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.643 (capability_fields_uncovered,capability_param_missing,missing_capability) |
| build-openbb-apps/types/evidence_files_ship | platform | hard | 0/2 avg=0.250 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.125, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.875 (capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/forms/exception_intake_room | platform | hard | 0/2 avg=0.166 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.100 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.232 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/settings/exception_metric | platform | medium | 0/2 avg=1.000 (widget_list_not_called_before_use,schema_not_called_before_create) | 1/2 avg=1.000 (widget_list_not_called_before_use) | 2/2 avg=1.000 |
| build-openbb-apps/settings/exception_refresh_grid | platform | hard | 0/2 avg=0.625 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_config_missing) |
| build-openbb-apps/debug/execution_broken_group | repair | medium | 1/2 avg=0.563 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.556 (capability_unconnected,missing_capability,capability_fields_uncovered) | 2/2 avg=1.000 |
| build-openbb-apps/debug/execution_dangling_app | repair | easy | 2/2 avg=1.000 | 0/2 avg=0.635 (missing_capability,capability_fields_uncovered,capability_param_missing) | 2/2 avg=1.000 |
| build-openbb-apps/debug/execution_data_mismatch | repair | hard | 0/2 avg=0.838 (missing_generated_widget) | 0/2 avg=0.246 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.838 (missing_generated_widget) |
| build-openbb-apps/debug/execution_duplicate_backend | repair | hard | 0/2 avg=1.000 (missing_tool_call,duplicate_custom_backend_name) | 0/2 avg=0.364 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=1.000 (missing_tool_call,duplicate_custom_backend_name) |
| build-openbb-apps/debug/execution_invalid_widget | repair | hard | 0/2 avg=0.810 (capability_config_missing,backend_validation_warnings) | 0/2 avg=0.302 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.810 (capability_config_missing,widget_list_not_called_before_use) |
| build-openbb-apps/e2e/execution_monitor | platform | hard | 0/2 avg=0.840 (capability_fields_uncovered,missing_capability,capability_param_missing) | 0/2 avg=0.286 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.593 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/settings/execution_ship | platform | hard | 0/2 avg=0.254 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) | 0/2 avg=0.071, proc=1 (missing_capability,capability_fields_uncovered,missing_generated_widget) | 0/2 avg=0.324 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/forms/execution_ship | platform | hard | 0/2 avg=0.208 (capability_param_missing,form_submission_incompatible,missing_capability) | 0/2 avg=0.000 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.271 (capability_param_missing,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/aggrid/execution_ship | platform | hard | 0/2 avg=0.469 (missing_capability,capability_fields_uncovered,missing_generated_widget) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,missing_generated_widget) | 0/2 avg=0.271 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/debug/execution_silent_second_tab | repair | easy | 2/2 avg=1.000 | 0/2 avg=0.569 (missing_capability,capability_fields_uncovered,capability_param_missing) | 2/2 avg=1.000 |
| build-openbb-apps/debug/execution_wrong_form_endpoint | repair | easy | 2/2 avg=1.000 | 0/2 avg=0.488 (missing_capability,capability_fields_uncovered,capability_param_missing) | 2/2 avg=1.000 |
| build-openbb-apps/debug/execution_wrong_live_row_id | repair | hard | 0/2 avg=0.378 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.317 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.867 (missing_generated_widget) |
| build-openbb-apps/types/fda_newsfeed_room | platform | hard | 0/2 avg=0.169 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) | 0/2 avg=0.050 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.429 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/aggrid/fill_quality | platform | hard | 0/2 avg=0.900 (capability_fields_uncovered,unexpected_dashboard_created) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,endpoint_unreachable) | 0/2 avg=0.233 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/grouping/full_earnings_sync | platform | hard | 0/2 avg=0.667 (capability_unconnected,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.000, proc=2 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.667 (capability_unconnected,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/settings/gas_metric | platform | medium | 0/2 avg=1.000 (schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=0.500, proc=1 (widget_list_not_called_before_use,missing_widget,missing_custom_backend) | 2/2 avg=1.000 |
| build-openbb-apps/types/gas_metric | platform | medium | 0/2 avg=1.000 (schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=1.000 (widget_list_not_called_before_use) | 2/2 avg=1.000 |
| build-openbb-apps/settings/gas_metric_room | platform | hard | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.062, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.472 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/apps/gas_metric_wrap | platform | hard | 0/2 avg=0.750 (missing_custom_backend,dashboard_name,missing_widget) | 0/2 avg=0.000 (missing_custom_backend,dashboard_name,missing_widget) | 0/2 avg=0.750 (missing_custom_backend,dashboard_name,missing_widget) |
| build-openbb-apps/types/gas_priority_metric | platform | hard | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,unexpected_dashboard_created) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,endpoint_unreachable) | 0/2 avg=0.617 (widget_list_not_called_before_use,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/settings/gas_refresh_metric | platform | hard | 0/2 avg=0.438 (capability_fields_uncovered,capability_config_missing,schema_not_called_before_create) | 0/2 avg=0.062 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.500 (capability_fields_uncovered,capability_config_missing,endpoint_response_incompatible) |
| build-openbb-apps/e2e/healthcare_pipeline | platform | hard | 0/2 avg=0.661 (capability_fields_uncovered,missing_generated_widget,missing_capability) | 0/2 avg=0.179 (missing_capability,capability_fields_uncovered,missing_generated_widget) | 0/2 avg=0.556 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/settings/healthcare_ship | platform | hard | 0/2 avg=0.594 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.125, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.396 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/forms/healthcare_ship | platform | hard | 0/2 avg=0.333 (capability_param_missing,endpoint_response_incompatible,missing_capability) | 0/2 avg=0.250 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.333 (capability_param_missing,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/charts/healthcare_ship | platform | hard | 0/2 avg=0.854 (capability_fields_uncovered,missing_capability,capability_param_missing) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.427 (endpoint_response_incompatible,capability_fields_uncovered,missing_capability) |
| build-openbb-apps/aggrid/healthcare_ship | platform | hard | 0/2 avg=0.333 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) | 0/2 avg=0.250 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.417 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/params/healthcare_ship | platform | hard | 0/2 avg=0.854 (capability_fields_uncovered,missing_capability,capability_param_missing) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.333 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/apps/healthcare_ship | platform | hard | 0/2 avg=0.823 (capability_fields_uncovered,missing_capability,capability_param_missing) | 0/2 avg=0.250 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.542 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/forms/incident_triage_form | platform | hard | 0/2 avg=0.500 (schema_not_called_before_create,widget_list_not_called_before_use,form_submission_incompatible) | 0/2 avg=0.438 (form_submission_incompatible,missing_widget,unexpected_dashboard_created) | 0/2 avg=0.500 (widget_list_not_called_before_use,form_submission_incompatible,endpoint_response_incompatible) |
| build-openbb-apps/params/kpi_param_tabs | platform | hard | 0/2 avg=0.625 (capability_fields_uncovered,capability_param_missing,schema_not_called_before_create) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/params/kpi_tabs_table | platform | medium | 0/2 avg=1.000 (widget_list_not_called_before_use,schema_not_called_before_create) | 1/2 avg=0.500, proc=1 (missing_widget,missing_custom_backend,endpoint_unreachable) | 2/2 avg=1.000 |
| build-openbb-apps/aggrid/latency_history | platform | hard | 0/2 avg=0.250 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,endpoint_unreachable) | 0/2 avg=0.808 (capability_fields_uncovered,missing_capability,endpoint_response_incompatible) |
| build-openbb-apps/advanced/live_orders_grid | platform | easy | 0/2 avg=0.950 (widget_def_mismatch,schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=0.883 (widget_list_not_called_before_use,backend_validation_warnings,widget_def_mismatch) | 1/2 avg=0.992 (widget_def_mismatch) |
| build-openbb-apps/advanced/live_orders_grid_app | platform | medium | 0/2 avg=0.980 (widget_def_mismatch) | 0/2 avg=0.846 (widget_def_mismatch,missing_widget,backend_validation_warnings) | 2/2 avg=1.000 |
| build-openbb-apps/advanced/live_orders_grid_ship | platform | hard | 0/2 avg=0.255 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.214 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.296 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/advanced/macro_advanced_chart_room | platform | hard | 0/2 avg=0.406 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.000, proc=1 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.396 (capability_fields_uncovered,missing_capability,capability_config_missing) |
| build-openbb-apps/e2e/macro_morning | platform | hard | 0/2 avg=0.286 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.250 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.870 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/extend/modify_case_notes | repair | hard | 0/2 avg=0.667 (capability_fields_uncovered,capability_param_missing,unexpected_dashboard_created) | 0/2 avg=0.000, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.667 (capability_fields_uncovered,capability_param_missing,unexpected_dashboard_created) |
| build-openbb-apps/extend/modify_rates_commentary | repair | hard | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.200, proc=1 (widget_list_not_called_before_use,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.571 (capability_fields_uncovered,capability_param_missing,capability_config_missing) |
| build-openbb-apps/extend/modify_trial_catalysts | repair | hard | 0/2 avg=0.500 (unexpected_dashboard_created,missing_capability,capability_fields_uncovered) | 0/2 avg=0.500 (widget_list_not_called_before_use,missing_capability,capability_fields_uncovered) | 0/2 avg=1.000 (unexpected_dashboard_created) |
| build-openbb-apps/extend/modify_vol_screener | repair | hard | 0/2 avg=0.722 (capability_param_missing,capability_fields_uncovered,schema_not_called_before_create) | 0/2 avg=0.167 (capability_param_missing,widget_list_not_called_before_use,missing_capability) | 0/2 avg=0.556 (capability_param_missing,capability_fields_uncovered,unexpected_dashboard_created) |
| build-openbb-apps/grouping/nvda_review_board | platform | hard | 0/2 avg=0.983 (too_many_invalid_calls,app_def_mismatch) | 0/2 avg=0.333 (missing_widget,missing_app_def) | 0/2 avg=0.967 (app_def_mismatch) |
| build-openbb-apps/aggrid/open_orders | platform | medium | 0/2 avg=0.933 (widget_def_mismatch,schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=0.492, proc=1 (widget_def_mismatch,schema_not_called_before_create,widget_list_not_called_before_use) | 2/2 avg=1.000 |
| build-openbb-apps/apps/order_watch | platform | hard | 0/2 avg=0.426 (too_many_invalid_calls,missing_widget,app_prompts_missing) | 0/2 avg=0.722 (app_def_mismatch,missing_widget,app_prompts_missing) | 0/2 avg=0.852 (app_prompts_missing) |
| build-openbb-apps/advanced/orders_ops_stream_room | platform | hard | 0/2 avg=0.208 (endpoint_response_incompatible,capability_config_missing,missing_capability) | 0/2 avg=0.042, proc=1 (missing_capability,capability_config_missing,capability_fields_uncovered) | 0/2 avg=0.208 (endpoint_response_incompatible,capability_config_missing,missing_capability) |
| build-openbb-apps/advanced/orders_stream | platform | hard | 0/2 avg=0.700 (capability_config_missing,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.100 (capability_config_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.100 (capability_config_missing,widget_list_not_called_before_use,endpoint_response_incompatible) |
| build-openbb-apps/charts/phase_mix_vegalite | platform | hard | 0/2 avg=0.833 (capability_fields_uncovered,capability_param_missing,unexpected_dashboard_created) | 0/2 avg=0.000, proc=2 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.750 (capability_fields_uncovered,capability_param_missing,widget_list_not_called_before_use) |
| build-openbb-apps/charts/pipeline_vegalite | platform | medium | 0/2 avg=1.000 (schema_not_called_before_create,widget_list_not_called_before_use) | 1/2 avg=1.000 (widget_list_not_called_before_use) | 2/2 avg=1.000 |
| build-openbb-apps/charts/pipeline_vegalite_app | platform | hard | 0/2 avg=0.833 (capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.062 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.708 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/charts/pipeline_vegalite_room | platform | hard | 0/2 avg=0.768 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.050 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.542 (capability_fields_uncovered,capability_param_missing,missing_capability) |
| build-openbb-apps/extend/place_alert_metric | repair | hard | 0/2 avg=0.844 (capability_fields_uncovered,unexpected_dashboard_created,too_many_invalid_calls) | 0/2 avg=0.370 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.844 (capability_fields_uncovered) |
| build-openbb-apps/extend/place_breach_metric | repair | hard | 0/2 avg=0.740 (missing_capability,capability_fields_uncovered) | 0/2 avg=0.083 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.792 (capability_fields_uncovered,missing_capability) |
| build-openbb-apps/extend/place_curve_spread_metric | repair | medium | 1/2 avg=0.500 (missing_widget,dashboard_name,missing_widget_def) | 1/2 avg=0.969 (app_def_mismatch,widget_list_not_called_before_use) | 2/2 avg=1.000 |
| build-openbb-apps/extend/place_vol_regime_metric | repair | medium | 0/2 avg=0.969 (app_def_mismatch,widget_list_not_called_before_use,too_many_invalid_calls) | 0/2 avg=0.453 (missing_widget,dashboard_name) | 2/2 avg=1.000 |
| build-openbb-apps/types/policy_digest_pdf | platform | hard | 0/2 avg=0.533 (capability_fields_uncovered,missing_capability,endpoint_unreachable) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,endpoint_unreachable) | 0/2 avg=0.833 (capability_fields_uncovered) |
| build-openbb-apps/types/policy_digest_pdf_ship | platform | hard | 0/2 avg=0.250 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.250 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.906 (capability_param_missing,capability_fields_uncovered) |
| build-openbb-apps/forms/policy_exception_form | platform | hard | 0/2 avg=0.188 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.062 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.188 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/grouping/preview_sync_live | platform | hard | 0/2 avg=0.451 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.241 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/advanced/rates_advanced_chart | platform | medium | 0/2 avg=0.988 (widget_list_not_called_before_use,schema_not_called_before_create,widget_def_mismatch) | 1/2 avg=1.000 (widget_list_not_called_before_use) | 2/2 avg=1.000 |
| build-openbb-apps/advanced/rates_advanced_chart_app | platform | hard | 0/2 avg=0.750 (capability_fields_uncovered,missing_capability,too_many_invalid_calls) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,endpoint_unreachable) | 0/2 avg=0.775 (capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/e2e/rates_auctions | platform | hard | 0/2 avg=0.806 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) | 0/2 avg=0.286 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.444 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/settings/rates_commentary | platform | medium | 0/2 avg=1.000 (schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=1.000 (widget_list_not_called_before_use,unexpected_dashboard_created,too_many_invalid_calls) | 2/2 avg=1.000 |
| build-openbb-apps/params/rates_commentary_app | platform | medium | 0/2 avg=0.542 (dashboard_name,missing_widget,missing_widget_def) | 0/2 avg=0.542 (missing_widget,app_def_mismatch,missing_custom_backend) | 2/2 avg=1.000 |
| build-openbb-apps/apps/rates_desk | platform | hard | 0/2 avg=0.786 (capability_param_missing,capability_fields_uncovered,capability_unconnected) | 0/2 avg=0.050 (missing_capability,capability_param_missing,capability_fields_uncovered) | 0/2 avg=0.333 (capability_param_missing,endpoint_response_incompatible,capability_fields_uncovered) |
| build-openbb-apps/advanced/rates_live_chart_ship | platform | hard | 0/2 avg=0.214 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.107 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.688 (capability_fields_uncovered,capability_config_missing,capability_param_missing) |
| build-openbb-apps/apps/rates_morning | platform | hard | 0/2 avg=0.852 (app_prompts_missing) | 0/2 avg=0.167, proc=1 (missing_widget,missing_app_def,dashboard_name) | 0/2 avg=0.852 (app_prompts_missing) |
| build-openbb-apps/settings/rates_ship | platform | hard | 0/2 avg=0.250 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.250 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.688 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/charts/rates_ship | platform | hard | 0/2 avg=0.311 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.107 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.514 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/aggrid/rates_ship | platform | hard | 0/2 avg=0.479 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) | 0/2 avg=0.250 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.396 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/params/rates_ship | platform | hard | 0/2 avg=0.583 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.729 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/advanced/rates_symbol_chart | platform | hard | 0/2 avg=0.786 (capability_config_missing,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.100 (capability_config_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.700 (capability_config_missing,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/aggrid/realized_screen | platform | medium | 0/2 avg=0.867 (capability_fields_uncovered,schema_not_called_before_create,unexpected_dashboard_created) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,endpoint_unreachable) | 1/2 avg=1.000 (unexpected_dashboard_created) |
| build-openbb-apps/aggrid/realized_vol_grid | platform | hard | 0/2 avg=0.812 (capability_fields_uncovered,missing_capability) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,endpoint_unreachable) | 0/2 avg=0.421 (capability_fields_uncovered,missing_capability,endpoint_response_incompatible) |
| build-openbb-apps/extend/repair_compliance | repair | hard | 0/2 avg=0.638 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.638 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/extend/repair_execution | repair | hard | 0/2 avg=0.000 (capability_param_missing,widget_list_not_called_before_use,endpoint_response_incompatible) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.000 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/extend/repair_rates | repair | hard | 0/2 avg=0.000 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) | 0/2 avg=0.318 (capability_fields_uncovered,capability_param_missing,missing_generated_widget) | 0/2 avg=0.193 (capability_fields_uncovered,capability_param_missing,missing_generated_widget) |
| build-openbb-apps/extend/repair_vol | repair | hard | 0/2 avg=0.523 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.023 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/e2e/research_room | platform | hard | 0/2 avg=0.440 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.107, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.426 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/aggrid/revision_grid | platform | medium | 0/2 avg=0.750 (capability_fields_uncovered,capability_config_missing,schema_not_called_before_create) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_config_missing) | 1/2 avg=0.562 (widget_list_not_called_before_use,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/grouping/revision_note_board | platform | hard | 0/2 avg=0.983 (app_def_mismatch,too_many_invalid_calls) | 0/2 avg=0.333 (missing_widget,missing_app_def) | 0/2 avg=0.967 (app_def_mismatch) |
| build-openbb-apps/grouping/revision_preview_sync | platform | hard | 0/2 avg=0.714 (capability_fields_uncovered,capability_param_missing,capability_unconnected) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.714 (capability_fields_uncovered,capability_param_missing,capability_unconnected) |
| build-openbb-apps/settings/runbook_markdown | platform | hard | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.750 (capability_fields_uncovered,capability_config_missing) |
| build-openbb-apps/params/series_markdown | platform | hard | 0/2 avg=0.833 (capability_fields_uncovered,capability_param_missing,unexpected_dashboard_created) | 0/2 avg=0.062 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.792 (capability_fields_uncovered,capability_param_missing,unexpected_dashboard_created) |
| build-openbb-apps/types/sla_newsfeed_app | platform | easy | 2/2 avg=1.000 | 0/2 avg=0.458, proc=1 (missing_widget,app_def_mismatch,missing_custom_backend) | 2/2 avg=1.000 |
| build-openbb-apps/types/sla_newsfeed_ship | platform | hard | 0/2 avg=0.312 (missing_capability,capability_fields_uncovered,missing_generated_widget) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,missing_generated_widget) | 0/2 avg=0.750 (capability_fields_uncovered,missing_generated_widget,capability_param_missing) |
| build-openbb-apps/settings/sla_runbook_app | platform | hard | 0/2 avg=0.312 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.062, proc=1 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.500 (endpoint_response_incompatible,capability_fields_uncovered,capability_config_missing) |
| build-openbb-apps/forms/sla_ship | platform | hard | 0/2 avg=0.479 (capability_param_missing,form_submission_incompatible,missing_capability) | 0/2 avg=0.125, proc=1 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.583 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/apps/sla_ship | platform | hard | 0/2 avg=0.375 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.125, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.688 (capability_fields_uncovered,capability_param_missing,missing_capability) |
| build-openbb-apps/settings/surprise_metric_app | platform | hard | 0/2 avg=0.458 (missing_capability,capability_fields_uncovered,too_many_invalid_calls) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,endpoint_unreachable) | 0/2 avg=0.350 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/settings/surprise_metric_room | platform | hard | 0/2 avg=0.342 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.050 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.304 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/apps/surprise_metric_wrap | platform | hard | 0/2 avg=0.533 (capability_fields_uncovered,missing_capability,endpoint_unreachable) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,endpoint_unreachable) | 0/2 avg=0.900 (capability_fields_uncovered) |
| build-openbb-apps/debug/surveillance_broken_group | repair | easy | 2/2 avg=1.000 | 0/2 avg=0.556 (missing_capability,capability_fields_uncovered,capability_param_missing) | 2/2 avg=1.000 |
| build-openbb-apps/debug/surveillance_dangling_app | repair | easy | 2/2 avg=1.000 | 0/2 avg=0.417 (missing_capability,capability_fields_uncovered,capability_param_missing) | 2/2 avg=1.000 |
| build-openbb-apps/debug/surveillance_data_mismatch | repair | medium | 1/2 avg=0.785 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.123 (missing_capability,capability_fields_uncovered,capability_param_missing) | 2/2 avg=1.000 |
| build-openbb-apps/debug/surveillance_duplicate_backend | repair | hard | 0/2 avg=1.000 (missing_tool_call,duplicate_custom_backend_name,collateral_app_change) | 0/2 avg=0.364 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=1.000 (missing_tool_call,duplicate_custom_backend_name) |
| build-openbb-apps/debug/surveillance_invalid_widget | repair | hard | 0/2 avg=0.619 (missing_generated_widget,capability_config_missing,backend_validation_warnings) | 0/2 avg=0.365 (missing_generated_widget,capability_config_missing,missing_capability) | 0/2 avg=0.619 (missing_generated_widget,capability_config_missing) |
| build-openbb-apps/apps/surveillance_morning | platform | hard | 0/2 avg=0.663 (capability_fields_uncovered,missing_capability,widget_list_not_called_before_use) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.806 (capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/debug/surveillance_silent_second_tab | repair | hard | 0/2 avg=0.838 (missing_generated_widget) | 0/2 avg=0.408 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.838 (missing_generated_widget) |
| build-openbb-apps/debug/surveillance_wrong_form_endpoint | repair | medium | 0/2 avg=0.462 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.569 (missing_capability,capability_fields_uncovered,capability_param_missing) | 2/2 avg=1.000 |
| build-openbb-apps/debug/surveillance_wrong_live_row_id | repair | easy | 2/2 avg=1.000 | 0/2 avg=0.511 (missing_capability,capability_fields_uncovered,capability_param_missing) | 2/2 avg=1.000 |
| build-openbb-apps/grouping/symbol_click_summary_app | platform | medium | 1/2 avg=0.875 (endpoint_response_incompatible) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.917 (unexpected_dashboard_created,endpoint_response_incompatible) |
| build-openbb-apps/charts/symbol_momentum_chart | platform | hard | 0/2 avg=0.300 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.100 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.400 (capability_fields_uncovered,capability_param_missing,capability_config_missing) |
| build-openbb-apps/params/symbol_param_desk | platform | hard | 0/2 avg=0.646 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.271 (missing_capability,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/forms/threshold_update_form | platform | hard | 0/2 avg=0.500 (schema_not_called_before_create,widget_list_not_called_before_use,form_submission_incompatible) | 0/2 avg=0.500 (form_submission_incompatible) | 0/2 avg=0.500 (endpoint_response_incompatible) |
| build-openbb-apps/forms/trade_break_form | platform | hard | 0/2 avg=0.125 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.062 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.125 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/params/trial_catalysts | platform | medium | 0/2 avg=0.958 (widget_def_mismatch,schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=0.983 (widget_def_mismatch,widget_list_not_called_before_use,unexpected_dashboard_created) | 2/2 avg=1.000 |
| build-openbb-apps/aggrid/trial_catalysts_app | platform | hard | 0/2 avg=0.812 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.000, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.292 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/params/trial_catalysts_app | platform | medium | 0/2 avg=0.967 (widget_def_mismatch) | 0/2 avg=0.458, proc=1 (missing_custom_backend,dashboard_name,missing_widget) | 2/2 avg=1.000 |
| build-openbb-apps/forms/trial_intake_room | platform | hard | 0/2 avg=0.166 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.000, proc=1 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.232 (capability_param_missing,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/params/trial_param_review | platform | hard | 0/2 avg=0.556 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.062 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.278 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/forms/trial_readout_form | platform | hard | 0/2 avg=0.125 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.125 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.125 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/charts/tvl_ship | platform | hard | 0/2 avg=0.552 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.000, proc=2 (missing_capability,capability_fields_uncovered,missing_generated_widget) | 0/2 avg=0.688 (capability_fields_uncovered,capability_param_missing,missing_capability) |
| build-openbb-apps/apps/tvl_ship | platform | hard | 0/2 avg=0.750 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) | 0/2 avg=0.250 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.583 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/apps/vendor_board | platform | medium | 1/2 avg=0.500 (missing_widget,dashboard_name,missing_app_def) | 1/2 avg=0.667 (missing_widget,missing_app_def) | 2/2 avg=1.000 |
| build-openbb-apps/debug/vendor_broken_group | repair | hard | 0/2 avg=0.310 (missing_generated_widget,capability_unconnected,missing_capability) | 0/2 avg=0.365 (missing_generated_widget,missing_capability,capability_fields_uncovered) | 0/2 avg=0.810 (missing_generated_widget) |
| build-openbb-apps/apps/vendor_command | platform | medium | 0/2 avg=0.621 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,widget_list_not_called_before_use) | 1/2 avg=0.944 (capability_fields_uncovered) |
| build-openbb-apps/debug/vendor_dangling_app | repair | easy | 2/2 avg=1.000 | 0/2 avg=0.208, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 2/2 avg=1.000 |
| build-openbb-apps/debug/vendor_data_mismatch | repair | medium | 0/2 avg=0.515 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.408 (missing_capability,capability_fields_uncovered,capability_param_missing) | 2/2 avg=1.000 |
| build-openbb-apps/debug/vendor_duplicate_backend | repair | hard | 0/2 avg=0.761 (missing_generated_widget,missing_tool_call,duplicate_custom_backend_name) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.761 (missing_generated_widget,missing_tool_call,duplicate_custom_backend_name) |
| build-openbb-apps/forms/vendor_intake_form | platform | hard | 0/2 avg=0.750 (schema_not_called_before_create,widget_list_not_called_before_use,endpoint_response_incompatible) | 0/2 avg=0.250 (widget_list_not_called_before_use,form_submission_incompatible,missing_widget) | 0/2 avg=0.500 (endpoint_response_incompatible,too_many_invalid_calls) |
| build-openbb-apps/forms/vendor_intake_form_app | platform | hard | 0/2 avg=0.483 (form_submission_incompatible,widget_def_mismatch,too_many_invalid_calls) | 0/2 avg=0.208, proc=1 (missing_widget,missing_custom_backend,app_def_mismatch) | 0/2 avg=0.500 (form_submission_incompatible,endpoint_response_incompatible) |
| build-openbb-apps/forms/vendor_intake_room | platform | hard | 0/2 avg=0.323 (capability_param_missing,form_submission_incompatible,missing_capability) | 0/2 avg=0.000, proc=2 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.562 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/debug/vendor_invalid_widget | repair | hard | 0/2 avg=0.619 (missing_generated_widget,capability_config_missing,backend_validation_warnings) | 0/2 avg=0.365 (missing_generated_widget,capability_config_missing,widget_list_not_called_before_use) | 0/2 avg=0.619 (missing_generated_widget,capability_config_missing) |
| build-openbb-apps/e2e/vendor_ops | platform | hard | 0/2 avg=0.486 (endpoint_response_incompatible,capability_fields_uncovered,missing_capability) | 0/2 avg=0.250 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.516 (endpoint_response_incompatible,capability_fields_uncovered,missing_capability) |
| build-openbb-apps/forms/vendor_review_form | platform | hard | 0/2 avg=0.250 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.062, proc=1 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.188 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/debug/vendor_silent_second_tab | repair | easy | 2/2 avg=1.000 | 0/2 avg=0.569 (missing_capability,capability_fields_uncovered,capability_param_missing) | 2/2 avg=1.000 |
| build-openbb-apps/aggrid/vendor_sla_table_app | platform | medium | 0/2 avg=0.971 (widget_def_mismatch) | 0/2 avg=0.411, proc=1 (missing_widget,missing_custom_backend,widget_def_mismatch) | 2/2 avg=1.000 |
| build-openbb-apps/params/vendor_sla_table_app | platform | medium | 1/2 avg=0.917 (capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.000, proc=2 (missing_capability,capability_fields_uncovered,capability_param_missing) | 2/2 avg=1.000 |
| build-openbb-apps/debug/vendor_wrong_form_endpoint | repair | medium | 1/2 avg=0.731 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.569 (missing_capability,capability_fields_uncovered,capability_param_missing) | 2/2 avg=1.000 |
| build-openbb-apps/debug/vendor_wrong_live_row_id | repair | hard | 0/2 avg=0.622 (missing_generated_widget,missing_capability,capability_fields_uncovered) | 0/2 avg=0.378 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.867 (missing_generated_widget) |
| build-openbb-apps/forms/venue_exception_form_app | platform | hard | 0/2 avg=0.292 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.062, proc=1 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.292 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/types/venue_packet_pdf_ship | platform | hard | 0/2 avg=0.292 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,missing_generated_widget) | 0/2 avg=0.437 (endpoint_response_incompatible,capability_fields_uncovered,missing_generated_widget) |
| build-openbb-apps/types/venue_pdf | platform | medium | 0/2 avg=1.000 (schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=0.500, proc=1 (widget_list_not_called_before_use,missing_widget,missing_custom_backend) | 2/2 avg=1.000 |
| build-openbb-apps/charts/venue_slippage_chart | platform | hard | 0/2 avg=0.743 (capability_fields_uncovered,capability_param_missing,capability_config_missing) | 0/2 avg=0.100 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.457 (capability_fields_uncovered,capability_param_missing,capability_config_missing) |
| build-openbb-apps/advanced/vix_advanced | platform | medium | 0/2 avg=1.000 (schema_not_called_before_create,widget_list_not_called_before_use) | 1/2 avg=1.000 (widget_list_not_called_before_use) | 2/2 avg=1.000 |
| build-openbb-apps/advanced/vix_advanced_app | platform | easy | 2/2 avg=1.000 | 0/2 avg=0.917 (app_def_mismatch,missing_widget,too_many_invalid_calls) | 2/2 avg=1.000 |
| build-openbb-apps/advanced/vix_advanced_ship | platform | hard | 0/2 avg=0.431 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.214 (missing_capability,capability_fields_uncovered,capability_config_missing) | 0/2 avg=0.461 (endpoint_response_incompatible,capability_fields_uncovered,capability_config_missing) |
| build-openbb-apps/aggrid/vix_history | platform | medium | 0/2 avg=0.950 (widget_def_mismatch,schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=0.983 (widget_def_mismatch,schema_not_called_before_create,widget_list_not_called_before_use) | 2/2 avg=1.000 |
| build-openbb-apps/params/vix_history | platform | medium | 0/2 avg=0.950 (widget_def_mismatch,schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=0.500, proc=1 (widget_list_not_called_before_use,missing_widget,missing_custom_backend) | 2/2 avg=1.000 |
| build-openbb-apps/advanced/vix_room_chart_room | platform | hard | 0/2 avg=0.573 (capability_config_missing,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.000, proc=2 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.667 (capability_config_missing,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/e2e/vol_cockpit | platform | hard | 0/2 avg=0.590 (capability_fields_uncovered,endpoint_response_incompatible,missing_generated_widget) | 0/2 avg=0.143 (missing_capability,capability_fields_uncovered,missing_generated_widget) | 0/2 avg=0.389 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/types/vol_commentary | platform | easy | 0/2 avg=1.000 (schema_not_called_before_create,widget_list_not_called_before_use) | 0/2 avg=0.000, proc=2 (missing_widget,missing_custom_backend,endpoint_unreachable) | 1/2 avg=1.000 (widget_list_not_called_before_use) |
| build-openbb-apps/settings/vol_commentary_room | platform | hard | 0/2 avg=0.340 (capability_fields_uncovered,missing_capability,capability_param_missing) | 0/2 avg=0.062, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.569 (capability_fields_uncovered,endpoint_response_incompatible,capability_param_missing) |
| build-openbb-apps/apps/vol_morning | platform | medium | 0/2 avg=0.889 (capability_fields_uncovered,too_many_invalid_calls,unexpected_dashboard_created) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,widget_list_not_called_before_use) | 1/2 avg=0.944 (capability_fields_uncovered) |
| build-openbb-apps/apps/vol_overview | platform | hard | 0/2 avg=0.000 (missing_widget,dashboard_name,missing_app_def) | 0/2 avg=0.000, proc=1 (missing_widget,dashboard_name,missing_app_def) | 0/2 avg=0.000 (missing_widget,dashboard_name,missing_app_def) |
| build-openbb-apps/params/vol_param_cockpit | platform | hard | 0/2 avg=0.425 (capability_param_missing,capability_fields_uncovered,endpoint_response_incompatible) | 0/2 avg=0.062 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.711 (capability_param_missing,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/types/vol_playbook_note | platform | hard | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.125 (missing_capability,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/settings/vol_regime_metric | platform | easy | 0/2 avg=1.000 (widget_list_not_called_before_use,schema_not_called_before_create) | 0/2 avg=1.000 (widget_list_not_called_before_use) | 1/2 avg=1.000 (widget_list_not_called_before_use) |
| build-openbb-apps/params/vol_screener | platform | hard | 0/2 avg=0.125 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.125 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.125 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/settings/vol_ship | platform | hard | 0/2 avg=0.524 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.214 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.688 (capability_fields_uncovered,capability_param_missing,capability_config_missing) |
| build-openbb-apps/params/vol_ship | platform | hard | 0/2 avg=0.747 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.000 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.427 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/apps/vol_ship | platform | hard | 0/2 avg=0.167 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.083, proc=1 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.458 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/advanced/vol_symbol_chart | platform | hard | 0/2 avg=0.443 (capability_config_missing,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.050, proc=1 (capability_config_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.400 (capability_config_missing,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/params/windowed_vix_slice | platform | hard | 0/2 avg=0.750 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.000, proc=2 (capability_param_missing,missing_capability,capability_fields_uncovered) | 0/2 avg=0.125 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/charts/yield_curve | platform | hard | 0/2 avg=0.975 (widget_list_not_called_before_use,widget_def_mismatch,schema_not_called_before_create) | 0/2 avg=0.975 (widget_def_mismatch) | 0/2 avg=0.975 (widget_def_mismatch) |
| build-openbb-apps/charts/yield_curve_app | platform | hard | 0/2 avg=0.983 (widget_def_mismatch) | 0/2 avg=0.250 (missing_custom_backend,missing_widget,endpoint_unreachable) | 0/2 avg=0.983 (widget_def_mismatch) |
| build-openbb-apps/charts/yield_curve_room | platform | hard | 0/2 avg=0.417 (capability_fields_uncovered,capability_param_missing,missing_capability) | 0/2 avg=0.083 (missing_capability,capability_fields_uncovered,capability_param_missing) | 0/2 avg=0.542 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |

## Common Interpretation

- Missing generated-widget failures often mean the model added no note/chart, added it to the wrong tab, or wrote placeholder text that did not include required task facts.
- Missing-widget and missing-tab failures are common on multi-widget dashboard tasks when the model chooses the wrong widget, tab, or data arguments.
- Invalid-call failures usually mean the model emitted a malformed tool name, used unresolved placeholders, or ignored an ID returned by an earlier observation.
- In batch mode, app-template tasks are especially sensitive to backend IDs because the model cannot read `manage_backends` output before calling `manage_apps`.

Raw outputs are under `runs/comparison/build-calibration-202607-regraded`.
