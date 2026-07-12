# Workspace Bench Model Comparison

- Benchmark: `openbb-workspace-bench`
- Git commit: `fab4b7ef4bdba318eca7de6ec604813e96a60272`
- Git dirty: `True`
- Tasks: `236`
- Attempts: `472`
- Filters: `{"capability": null, "difficulty": "all", "domain": null, "family": null, "split": null, "subdomain": null, "suite": "build-openbb-apps", "tags": [], "task_dir": null, "track": "guided", "workflow": null}`
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
| OpenAI GPT-5.5 | 128 | 472 | 27.1% | 27.1% | 71.8% | 344 | 0 |

## Reliability

| Model | pass@k | pass^k | Tasks | k Range |
| --- | ---: | ---: | ---: | ---: |
| OpenAI GPT-5.5 | 29.7% | 24.6% | 236 | 2 |

## By Difficulty

| Model | Easy | Medium | Hard |
| --- | ---: | ---: | ---: |
| OpenAI GPT-5.5 | 99/110 (90%) | 15/36 (42%) | 14/326 (4%) |

## By Category

| Model | read | single-widget | dashboard | platform | repair |
| --- | ---: | ---: | ---: | ---: | ---: |
| OpenAI GPT-5.5 | - | - | - | 80/384 (21%) | 48/88 (55%) |

## Task Issue Counts

### OpenAI GPT-5.5

| Issue Code | Count |
| --- | ---: |
| `capability_fields_uncovered` | 475 |
| `capability_param_missing` | 431 |
| `endpoint_response_incompatible` | 427 |
| `missing_capability` | 276 |
| `capability_config_missing` | 77 |
| `capability_unconnected` | 72 |
| `widget_list_not_called_before_use` | 65 |
| `unexpected_dashboard_created` | 35 |
| `form_submission_incompatible` | 22 |
| `app_def_mismatch` | 14 |
| `widget_def_mismatch` | 7 |
| `duplicate_custom_backend_name` | 6 |
| `missing_widget` | 3 |
| `endpoint_unreachable` | 3 |
| `too_many_invalid_calls` | 1 |

## Process Failures

| Model | Task | Repeat | Exit Code | Timed Out | Stderr Preview |
| --- | --- | ---: | ---: | --- | --- |
| - | - | - | - | - | No provider or process failures. |

## Task Matrix

| Task | Difficulty | Capability | Workflow | Domain | Subdomain | OpenAI GPT-5.5 |
| --- | --- | --- | --- | --- | --- | ---: |
| build-openbb-apps/forms/access_review_form | easy | widget-building | compliance-surveillance | finance | compliance | 2/2 avg=1.000 |
| build-openbb-apps/extend/add_catalyst_metric | easy | app-building | healthcare-catalyst-review | finance | healthcare | 1/2 avg=0.964 (widget_list_not_called_before_use,missing_widget) |
| build-openbb-apps/extend/add_curve_spread_metric | easy | app-building | macro-rates-review | finance | macro | 1/2 avg=0.964 (widget_list_not_called_before_use,missing_widget) |
| build-openbb-apps/extend/add_exception_metric | easy | app-building | execution-exception-review | finance | execution | 1/2 avg=1.000 (widget_list_not_called_before_use) |
| build-openbb-apps/extend/add_vol_regime_metric | hard | app-building | risk-review | finance | volatility | 0/2 avg=1.000 (widget_list_not_called_before_use) |
| build-openbb-apps/settings/alert_metric_app | easy | widget-building | compliance-surveillance | finance | compliance | 2/2 avg=1.000 |
| build-openbb-apps/settings/alert_metric_room | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.768 (capability_fields_uncovered,missing_capability,capability_param_missing) |
| build-openbb-apps/apps/alert_metric_wrap | easy | app-building | compliance-surveillance | finance | compliance | 2/2 avg=1.000 |
| build-openbb-apps/aggrid/alert_queue_app | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.641 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/settings/auction_cache_grid | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.208 (widget_list_not_called_before_use,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/aggrid/auction_calendar | easy | widget-building | macro-rates-review | finance | macro | 2/2 avg=1.000 |
| build-openbb-apps/aggrid/auction_watch | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.250 (widget_list_not_called_before_use,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/types/call_replay_video | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.708 (capability_fields_uncovered,capability_param_missing,widget_list_not_called_before_use) |
| build-openbb-apps/aggrid/case_aging | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.490 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/apps/case_command | hard | app-building | compliance-surveillance | finance | compliance | 0/2 avg=0.911 (capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/forms/case_escalation_form_app | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.500 (form_submission_incompatible) |
| build-openbb-apps/forms/case_intake_room | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.296 (capability_param_missing,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/params/case_notes | easy | widget-building | compliance-surveillance | finance | compliance | 2/2 avg=1.000 |
| build-openbb-apps/params/case_notes_app | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.344 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/types/case_notes_room | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.502 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/advanced/case_prompt_omni | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.479 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/advanced/case_qa_omni | easy | widget-building | compliance-surveillance | finance | compliance | 2/2 avg=1.000 |
| build-openbb-apps/advanced/case_qa_omni_app | medium | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.875 (capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/advanced/case_qa_omni_ship | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.771 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/advanced/case_room_omni_room | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.569 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/e2e/case_triage | hard | backend-integration | compliance-surveillance | finance | compliance | 0/2 avg=0.758 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/e2e/catalyst_calendar | hard | backend-integration | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.712 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/settings/catalyst_metric_app | easy | widget-building | healthcare-catalyst-review | finance | healthcare | 2/2 avg=1.000 |
| build-openbb-apps/apps/catalyst_metric_wrap | hard | app-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.461 (endpoint_response_incompatible,capability_fields_uncovered,missing_capability) |
| build-openbb-apps/apps/chain_deck | hard | app-building | portfolio-morning-review | finance | crypto | 0/2 avg=0.389 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/charts/chain_flow_highchart | hard | widget-building | portfolio-morning-review | finance | crypto | 0/2 avg=0.786 (capability_fields_uncovered,capability_param_missing,capability_config_missing) |
| build-openbb-apps/aggrid/chain_flows | hard | widget-building | portfolio-morning-review | finance | crypto | 0/2 avg=0.381 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/e2e/chain_flows | hard | backend-integration | portfolio-morning-review | finance | crypto | 0/2 avg=0.379 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/types/chains_heatmap_html | easy | widget-building | portfolio-morning-review | finance | crypto | 2/2 avg=1.000 |
| build-openbb-apps/charts/chains_highchart | easy | widget-building | portfolio-morning-review | finance | crypto | 2/2 avg=1.000 |
| build-openbb-apps/charts/chains_highchart_app | easy | widget-building | portfolio-morning-review | finance | crypto | 1/2 avg=0.965 (app_def_mismatch,missing_widget) |
| build-openbb-apps/charts/chains_highchart_room | hard | widget-building | portfolio-morning-review | finance | crypto | 0/2 avg=0.644 (capability_fields_uncovered,capability_param_missing,capability_unconnected) |
| build-openbb-apps/aggrid/chains_table_app | easy | widget-building | portfolio-morning-review | finance | crypto | 2/2 avg=1.000 |
| build-openbb-apps/grouping/chart_note_board | easy | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.990 (app_def_mismatch) |
| build-openbb-apps/grouping/chart_preview_sync | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.833 (capability_fields_uncovered,capability_param_missing,capability_unconnected) |
| build-openbb-apps/grouping/chart_sync_live | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.333 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/grouping/click_preview_desk | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.523 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/grouping/click_revision_desk | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.380 (missing_capability,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/grouping/click_season_desk | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.292 (missing_capability,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/grouping/click_summary_desk | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.361 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/grouping/click_sync_live | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.573 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/forms/compliance_ship | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.533 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/e2e/compliance_surveillance | hard | backend-integration | compliance-surveillance | finance | compliance | 0/2 avg=0.788 (capability_fields_uncovered,endpoint_response_incompatible,capability_param_missing) |
| build-openbb-apps/forms/curve_comment_form_app | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.344 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/types/curve_monitor_iframe_app | easy | widget-building | macro-rates-review | finance | macro | 2/2 avg=1.000 |
| build-openbb-apps/extend/diagnose_earnings | hard | app-building | earnings-prep | finance | equity-research | 0/2 avg=0.812 (unexpected_dashboard_created,endpoint_response_incompatible) |
| build-openbb-apps/extend/diagnose_healthcare | hard | app-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.938 (unexpected_dashboard_created) |
| build-openbb-apps/extend/diagnose_rates | hard | app-building | macro-rates-review | finance | macro | 0/2 avg=0.804 (unexpected_dashboard_created,endpoint_response_incompatible) |
| build-openbb-apps/extend/diagnose_sla | hard | app-building | vendor-sla-monitoring | finance | operations | 0/2 avg=0.938 (unexpected_dashboard_created) |
| build-openbb-apps/types/earnings_calls_video_app | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.505 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/types/earnings_calls_video_room | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.569 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/charts/earnings_chart | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.986 (widget_def_mismatch,widget_list_not_called_before_use) |
| build-openbb-apps/grouping/earnings_chart_app | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.990 (app_def_mismatch) |
| build-openbb-apps/charts/earnings_chart_app | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.444 (capability_fields_uncovered,capability_param_missing,capability_config_missing) |
| build-openbb-apps/charts/earnings_chart_room | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.662 (capability_param_missing,capability_fields_uncovered,capability_config_missing) |
| build-openbb-apps/apps/earnings_command | hard | app-building | earnings-prep | finance | equity-research | 0/2 avg=0.880 (capability_fields_uncovered,capability_param_missing,capability_unconnected) |
| build-openbb-apps/apps/earnings_desk | hard | app-building | earnings-prep | finance | equity-research | 0/2 avg=0.431 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/grouping/earnings_note_app | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.583 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/params/earnings_param_review | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.333 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/grouping/earnings_review_sync | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.889 (capability_fields_uncovered,capability_param_missing,capability_unconnected) |
| build-openbb-apps/e2e/earnings_season | hard | backend-integration | earnings-prep | finance | equity-research | 0/2 avg=0.761 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/charts/earnings_ship | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.701 (capability_fields_uncovered,endpoint_response_incompatible,capability_param_missing) |
| build-openbb-apps/aggrid/earnings_ship | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.533 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/params/earnings_ship | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.450 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/grouping/earnings_symbol_board | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.990 (app_def_mismatch) |
| build-openbb-apps/grouping/earnings_sync_live | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.333 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/grouping/estimate_revisions_app | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.990 (app_def_mismatch) |
| build-openbb-apps/aggrid/estimates_ssrm | easy | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.500 (endpoint_response_incompatible) |
| build-openbb-apps/types/evidence_files_app | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.568 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/types/evidence_files_room | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.694 (capability_fields_uncovered,capability_param_missing,missing_capability) |
| build-openbb-apps/types/evidence_files_ship | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.900 (capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/forms/exception_intake_room | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.292 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/settings/exception_metric | easy | widget-building | execution-exception-review | finance | execution | 2/2 avg=1.000 |
| build-openbb-apps/settings/exception_refresh_grid | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.208 (missing_capability,capability_fields_uncovered,capability_config_missing) |
| build-openbb-apps/debug/execution_broken_group | hard | backend-repair | diagnose-repair-retest | finance | execution | 2/2 avg=1.000 |
| build-openbb-apps/debug/execution_dangling_app | easy | backend-repair | diagnose-repair-retest | finance | execution | 2/2 avg=1.000 |
| build-openbb-apps/debug/execution_data_mismatch | easy | backend-repair | diagnose-repair-retest | finance | execution | 2/2 avg=1.000 |
| build-openbb-apps/debug/execution_duplicate_backend | hard | backend-repair | diagnose-repair-retest | finance | execution | 0/2 avg=0.967 (duplicate_custom_backend_name) |
| build-openbb-apps/debug/execution_invalid_widget | medium | backend-repair | diagnose-repair-retest | finance | execution | 1/2 avg=1.000 (widget_list_not_called_before_use) |
| build-openbb-apps/e2e/execution_monitor | hard | backend-integration | execution-exception-review | finance | execution | 0/2 avg=0.606 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/settings/execution_ship | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.417 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/forms/execution_ship | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.367 (capability_param_missing,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/aggrid/execution_ship | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.367 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/debug/execution_silent_second_tab | easy | backend-repair | diagnose-repair-retest | finance | execution | 2/2 avg=1.000 |
| build-openbb-apps/debug/execution_wrong_form_endpoint | easy | backend-repair | diagnose-repair-retest | finance | execution | 2/2 avg=1.000 |
| build-openbb-apps/debug/execution_wrong_live_row_id | hard | backend-repair | diagnose-repair-retest | finance | execution | 2/2 avg=1.000 |
| build-openbb-apps/types/fda_newsfeed_room | hard | widget-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.481 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/aggrid/fill_quality | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.293 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/grouping/full_earnings_sync | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.870 (capability_unconnected,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/settings/gas_metric | easy | widget-building | portfolio-morning-review | finance | crypto | 2/2 avg=1.000 |
| build-openbb-apps/types/gas_metric | easy | widget-building | portfolio-morning-review | finance | crypto | 2/2 avg=1.000 |
| build-openbb-apps/settings/gas_metric_room | hard | widget-building | portfolio-morning-review | finance | crypto | 0/2 avg=0.521 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/apps/gas_metric_wrap | easy | app-building | portfolio-morning-review | finance | crypto | 2/2 avg=1.000 |
| build-openbb-apps/types/gas_priority_metric | hard | widget-building | portfolio-morning-review | finance | crypto | 0/2 avg=0.629 (widget_list_not_called_before_use,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/settings/gas_refresh_metric | hard | widget-building | portfolio-morning-review | finance | crypto | 0/2 avg=0.583 (capability_fields_uncovered,capability_config_missing,endpoint_response_incompatible) |
| build-openbb-apps/e2e/healthcare_pipeline | hard | backend-integration | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.629 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/settings/healthcare_ship | hard | widget-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.429 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/forms/healthcare_ship | hard | widget-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.367 (capability_param_missing,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/charts/healthcare_ship | hard | widget-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.458 (endpoint_response_incompatible,capability_fields_uncovered,missing_capability) |
| build-openbb-apps/aggrid/healthcare_ship | hard | widget-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.450 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/params/healthcare_ship | hard | widget-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.367 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/apps/healthcare_ship | hard | app-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.575 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/forms/incident_triage_form | hard | widget-building | vendor-sla-monitoring | finance | operations | 0/2 avg=0.500 (widget_list_not_called_before_use,form_submission_incompatible,endpoint_response_incompatible) |
| build-openbb-apps/params/kpi_param_tabs | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.208 (missing_capability,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/params/kpi_tabs_table | easy | widget-building | earnings-prep | finance | equity-research | 2/2 avg=1.000 |
| build-openbb-apps/aggrid/latency_history | medium | widget-building | vendor-sla-monitoring | finance | operations | 0/2 avg=0.827 (capability_fields_uncovered,missing_capability,endpoint_response_incompatible) |
| build-openbb-apps/advanced/live_orders_grid | easy | widget-building | execution-exception-review | finance | execution | 1/2 avg=0.994 (widget_def_mismatch) |
| build-openbb-apps/advanced/live_orders_grid_app | easy | widget-building | execution-exception-review | finance | execution | 2/2 avg=1.000 |
| build-openbb-apps/advanced/live_orders_grid_ship | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.333 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/advanced/macro_advanced_chart_room | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.479 (capability_fields_uncovered,missing_capability,capability_config_missing) |
| build-openbb-apps/e2e/macro_morning | hard | backend-integration | macro-rates-review | finance | macro | 0/2 avg=0.879 (missing_capability,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/extend/modify_case_notes | hard | app-building | compliance-surveillance | finance | compliance | 0/2 avg=0.812 (capability_fields_uncovered,capability_param_missing,unexpected_dashboard_created) |
| build-openbb-apps/extend/modify_rates_commentary | hard | app-building | macro-rates-review | finance | macro | 0/2 avg=0.778 (capability_fields_uncovered,capability_param_missing,capability_config_missing) |
| build-openbb-apps/extend/modify_trial_catalysts | hard | app-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.938 (unexpected_dashboard_created) |
| build-openbb-apps/extend/modify_vol_screener | hard | app-building | risk-review | finance | volatility | 0/2 avg=0.656 (capability_param_missing,capability_fields_uncovered,unexpected_dashboard_created) |
| build-openbb-apps/grouping/nvda_review_board | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.990 (app_def_mismatch) |
| build-openbb-apps/aggrid/open_orders | easy | widget-building | execution-exception-review | finance | execution | 2/2 avg=1.000 |
| build-openbb-apps/apps/order_watch | easy | app-building | execution-exception-review | finance | execution | 2/2 avg=1.000 |
| build-openbb-apps/advanced/orders_ops_stream_room | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.267 (endpoint_response_incompatible,capability_config_missing,missing_capability) |
| build-openbb-apps/advanced/orders_stream | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.214 (capability_config_missing,widget_list_not_called_before_use,endpoint_response_incompatible) |
| build-openbb-apps/charts/phase_mix_vegalite | hard | widget-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.833 (capability_fields_uncovered,capability_param_missing,widget_list_not_called_before_use) |
| build-openbb-apps/charts/pipeline_vegalite | easy | widget-building | healthcare-catalyst-review | finance | healthcare | 2/2 avg=1.000 |
| build-openbb-apps/charts/pipeline_vegalite_app | hard | widget-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.750 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/charts/pipeline_vegalite_room | hard | widget-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.597 (capability_fields_uncovered,capability_param_missing,missing_capability) |
| build-openbb-apps/extend/place_alert_metric | medium | app-building | compliance-surveillance | finance | compliance | 0/2 avg=0.969 (capability_fields_uncovered) |
| build-openbb-apps/extend/place_breach_metric | medium | app-building | vendor-sla-monitoring | finance | operations | 0/2 avg=0.958 (capability_fields_uncovered,missing_capability) |
| build-openbb-apps/extend/place_curve_spread_metric | easy | app-building | macro-rates-review | finance | macro | 2/2 avg=1.000 |
| build-openbb-apps/extend/place_vol_regime_metric | easy | app-building | risk-review | finance | volatility | 2/2 avg=1.000 |
| build-openbb-apps/types/policy_digest_pdf | medium | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.900 (capability_fields_uncovered) |
| build-openbb-apps/types/policy_digest_pdf_ship | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.925 (capability_param_missing,capability_fields_uncovered) |
| build-openbb-apps/forms/policy_exception_form | hard | widget-building | compliance-surveillance | finance | compliance | 0/2 avg=0.208 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/grouping/preview_sync_live | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.333 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/advanced/rates_advanced_chart | easy | widget-building | macro-rates-review | finance | macro | 2/2 avg=1.000 |
| build-openbb-apps/advanced/rates_advanced_chart_app | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.804 (capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/e2e/rates_auctions | hard | backend-integration | macro-rates-review | finance | macro | 0/2 avg=0.470 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/settings/rates_commentary | easy | widget-building | macro-rates-review | finance | macro | 2/2 avg=1.000 |
| build-openbb-apps/params/rates_commentary_app | easy | widget-building | macro-rates-review | finance | macro | 2/2 avg=1.000 |
| build-openbb-apps/apps/rates_desk | hard | app-building | macro-rates-review | finance | macro | 0/2 avg=0.476 (endpoint_response_incompatible,capability_fields_uncovered,missing_capability) |
| build-openbb-apps/advanced/rates_live_chart_ship | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.718 (capability_fields_uncovered,capability_config_missing,capability_param_missing) |
| build-openbb-apps/apps/rates_morning | easy | app-building | macro-rates-review | finance | macro | 2/2 avg=1.000 |
| build-openbb-apps/settings/rates_ship | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.713 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/charts/rates_ship | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.549 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/aggrid/rates_ship | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.429 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/params/rates_ship | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.754 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/advanced/rates_symbol_chart | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.786 (capability_config_missing,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/aggrid/realized_screen | medium | widget-building | risk-review | finance | volatility | 1/2 avg=0.950 (unexpected_dashboard_created) |
| build-openbb-apps/aggrid/realized_vol_grid | hard | widget-building | risk-review | finance | volatility | 0/2 avg=0.467 (capability_fields_uncovered,missing_capability,endpoint_response_incompatible) |
| build-openbb-apps/extend/repair_compliance | hard | app-building | compliance-surveillance | finance | compliance | 0/2 avg=0.733 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/extend/repair_execution | hard | app-building | execution-exception-review | finance | execution | 0/2 avg=0.367 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/extend/repair_rates | hard | app-building | macro-rates-review | finance | macro | 0/2 avg=0.767 (capability_fields_uncovered,capability_param_missing,missing_capability) |
| build-openbb-apps/extend/repair_vol | hard | app-building | risk-review | finance | volatility | 0/2 avg=0.642 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/e2e/research_room | hard | backend-integration | earnings-prep | finance | equity-research | 0/2 avg=0.758 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/aggrid/revision_grid | medium | widget-building | earnings-prep | finance | equity-research | 1/2 avg=0.625 (widget_list_not_called_before_use,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/grouping/revision_note_board | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.990 (app_def_mismatch) |
| build-openbb-apps/grouping/revision_preview_sync | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.889 (capability_fields_uncovered,capability_param_missing,capability_unconnected) |
| build-openbb-apps/settings/runbook_markdown | hard | widget-building | vendor-sla-monitoring | finance | operations | 0/2 avg=0.833 (capability_fields_uncovered,capability_config_missing) |
| build-openbb-apps/params/series_markdown | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.781 (capability_fields_uncovered,capability_param_missing,unexpected_dashboard_created) |
| build-openbb-apps/types/sla_newsfeed_app | easy | widget-building | vendor-sla-monitoring | finance | operations | 2/2 avg=1.000 |
| build-openbb-apps/types/sla_newsfeed_ship | hard | widget-building | vendor-sla-monitoring | finance | operations | 0/2 avg=0.838 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |
| build-openbb-apps/settings/sla_runbook_app | hard | widget-building | vendor-sla-monitoring | finance | operations | 0/2 avg=0.542 (endpoint_response_incompatible,capability_fields_uncovered,capability_config_missing) |
| build-openbb-apps/forms/sla_ship | hard | widget-building | vendor-sla-monitoring | finance | operations | 0/2 avg=0.617 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/apps/sla_ship | hard | app-building | vendor-sla-monitoring | finance | operations | 0/2 avg=0.717 (capability_fields_uncovered,capability_param_missing,missing_capability) |
| build-openbb-apps/settings/surprise_metric_app | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.393 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/settings/surprise_metric_room | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.361 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/apps/surprise_metric_wrap | medium | app-building | earnings-prep | finance | equity-research | 0/2 avg=0.929 (capability_fields_uncovered) |
| build-openbb-apps/debug/surveillance_broken_group | easy | backend-repair | diagnose-repair-retest | finance | surveillance | 2/2 avg=1.000 |
| build-openbb-apps/debug/surveillance_dangling_app | easy | backend-repair | diagnose-repair-retest | finance | surveillance | 2/2 avg=1.000 |
| build-openbb-apps/debug/surveillance_data_mismatch | medium | backend-repair | diagnose-repair-retest | finance | surveillance | 2/2 avg=1.000 |
| build-openbb-apps/debug/surveillance_duplicate_backend | hard | backend-repair | diagnose-repair-retest | finance | surveillance | 0/2 avg=0.967 (duplicate_custom_backend_name) |
| build-openbb-apps/debug/surveillance_invalid_widget | medium | backend-repair | diagnose-repair-retest | finance | surveillance | 2/2 avg=1.000 |
| build-openbb-apps/apps/surveillance_morning | medium | app-building | compliance-surveillance | finance | compliance | 0/2 avg=0.927 (capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/debug/surveillance_silent_second_tab | hard | backend-repair | diagnose-repair-retest | finance | surveillance | 2/2 avg=1.000 |
| build-openbb-apps/debug/surveillance_wrong_form_endpoint | hard | backend-repair | diagnose-repair-retest | finance | surveillance | 2/2 avg=1.000 |
| build-openbb-apps/debug/surveillance_wrong_live_row_id | easy | backend-repair | diagnose-repair-retest | finance | surveillance | 2/2 avg=1.000 |
| build-openbb-apps/grouping/symbol_click_summary_app | medium | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.885 (unexpected_dashboard_created,endpoint_response_incompatible) |
| build-openbb-apps/charts/symbol_momentum_chart | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.500 (capability_fields_uncovered,capability_param_missing,capability_config_missing) |
| build-openbb-apps/params/symbol_param_desk | hard | widget-building | earnings-prep | finance | equity-research | 0/2 avg=0.328 (missing_capability,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/forms/threshold_update_form | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.500 (endpoint_response_incompatible) |
| build-openbb-apps/forms/trade_break_form | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.208 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/params/trial_catalysts | easy | widget-building | healthcare-catalyst-review | finance | healthcare | 2/2 avg=1.000 |
| build-openbb-apps/aggrid/trial_catalysts_app | hard | widget-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.344 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/params/trial_catalysts_app | easy | widget-building | healthcare-catalyst-review | finance | healthcare | 2/2 avg=1.000 |
| build-openbb-apps/forms/trial_intake_room | hard | widget-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.292 (capability_param_missing,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/params/trial_param_review | hard | widget-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.333 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/forms/trial_readout_form | hard | widget-building | healthcare-catalyst-review | finance | healthcare | 0/2 avg=0.250 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/charts/tvl_ship | hard | widget-building | portfolio-morning-review | finance | crypto | 0/2 avg=0.717 (capability_fields_uncovered,capability_param_missing,missing_capability) |
| build-openbb-apps/apps/tvl_ship | hard | app-building | portfolio-morning-review | finance | crypto | 0/2 avg=0.600 (endpoint_response_incompatible,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/apps/vendor_board | easy | app-building | vendor-sla-monitoring | finance | operations | 2/2 avg=1.000 |
| build-openbb-apps/debug/vendor_broken_group | hard | backend-repair | diagnose-repair-retest | finance | vendor | 2/2 avg=1.000 |
| build-openbb-apps/apps/vendor_command | medium | app-building | vendor-sla-monitoring | finance | operations | 1/2 avg=0.979 (capability_fields_uncovered) |
| build-openbb-apps/debug/vendor_dangling_app | easy | backend-repair | diagnose-repair-retest | finance | vendor | 2/2 avg=1.000 |
| build-openbb-apps/debug/vendor_data_mismatch | medium | backend-repair | diagnose-repair-retest | finance | vendor | 2/2 avg=1.000 |
| build-openbb-apps/debug/vendor_duplicate_backend | hard | backend-repair | diagnose-repair-retest | finance | vendor | 0/2 avg=0.967 (duplicate_custom_backend_name) |
| build-openbb-apps/forms/vendor_intake_form | hard | widget-building | vendor-sla-monitoring | finance | operations | 0/2 avg=0.500 (endpoint_response_incompatible,too_many_invalid_calls) |
| build-openbb-apps/forms/vendor_intake_form_app | hard | widget-building | vendor-sla-monitoring | finance | operations | 0/2 avg=0.500 (form_submission_incompatible,endpoint_response_incompatible) |
| build-openbb-apps/forms/vendor_intake_room | hard | widget-building | vendor-sla-monitoring | finance | operations | 0/2 avg=0.604 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/debug/vendor_invalid_widget | medium | backend-repair | diagnose-repair-retest | finance | vendor | 2/2 avg=1.000 |
| build-openbb-apps/e2e/vendor_ops | hard | backend-integration | vendor-sla-monitoring | finance | operations | 0/2 avg=0.540 (endpoint_response_incompatible,capability_fields_uncovered,missing_capability) |
| build-openbb-apps/forms/vendor_review_form | hard | widget-building | vendor-sla-monitoring | finance | operations | 0/2 avg=0.208 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/debug/vendor_silent_second_tab | easy | backend-repair | diagnose-repair-retest | finance | vendor | 2/2 avg=1.000 |
| build-openbb-apps/aggrid/vendor_sla_table_app | easy | widget-building | vendor-sla-monitoring | finance | operations | 2/2 avg=1.000 |
| build-openbb-apps/params/vendor_sla_table_app | medium | widget-building | vendor-sla-monitoring | finance | operations | 2/2 avg=1.000 |
| build-openbb-apps/debug/vendor_wrong_form_endpoint | hard | backend-repair | diagnose-repair-retest | finance | vendor | 2/2 avg=1.000 |
| build-openbb-apps/debug/vendor_wrong_live_row_id | hard | backend-repair | diagnose-repair-retest | finance | vendor | 2/2 avg=1.000 |
| build-openbb-apps/forms/venue_exception_form_app | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.344 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/types/venue_packet_pdf_ship | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.529 (endpoint_response_incompatible,capability_fields_uncovered,missing_capability) |
| build-openbb-apps/types/venue_pdf | easy | widget-building | execution-exception-review | finance | execution | 2/2 avg=1.000 |
| build-openbb-apps/charts/venue_slippage_chart | hard | widget-building | execution-exception-review | finance | execution | 0/2 avg=0.504 (capability_fields_uncovered,capability_param_missing,capability_config_missing) |
| build-openbb-apps/advanced/vix_advanced | easy | widget-building | risk-review | finance | volatility | 2/2 avg=1.000 |
| build-openbb-apps/advanced/vix_advanced_app | easy | widget-building | risk-review | finance | volatility | 2/2 avg=1.000 |
| build-openbb-apps/advanced/vix_advanced_ship | hard | widget-building | risk-review | finance | volatility | 0/2 avg=0.494 (endpoint_response_incompatible,capability_fields_uncovered,capability_config_missing) |
| build-openbb-apps/aggrid/vix_history | easy | widget-building | risk-review | finance | volatility | 2/2 avg=1.000 |
| build-openbb-apps/params/vix_history | easy | widget-building | risk-review | finance | volatility | 2/2 avg=1.000 |
| build-openbb-apps/advanced/vix_room_chart_room | hard | widget-building | risk-review | finance | volatility | 0/2 avg=0.704 (capability_config_missing,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/e2e/vol_cockpit | hard | backend-integration | risk-review | finance | volatility | 0/2 avg=0.470 (capability_fields_uncovered,endpoint_response_incompatible,missing_capability) |
| build-openbb-apps/types/vol_commentary | easy | widget-building | risk-review | finance | volatility | 1/2 avg=1.000 (widget_list_not_called_before_use) |
| build-openbb-apps/settings/vol_commentary_room | hard | widget-building | risk-review | finance | volatility | 0/2 avg=0.615 (capability_fields_uncovered,endpoint_response_incompatible,capability_param_missing) |
| build-openbb-apps/apps/vol_morning | medium | app-building | risk-review | finance | volatility | 1/2 avg=0.979 (capability_fields_uncovered) |
| build-openbb-apps/apps/vol_overview | easy | app-building | risk-review | finance | volatility | 2/2 avg=1.000 |
| build-openbb-apps/params/vol_param_cockpit | hard | widget-building | risk-review | finance | volatility | 0/2 avg=0.742 (capability_param_missing,capability_fields_uncovered,endpoint_response_incompatible) |
| build-openbb-apps/types/vol_playbook_note | hard | widget-building | risk-review | finance | volatility | 0/2 avg=0.208 (missing_capability,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/settings/vol_regime_metric | easy | widget-building | risk-review | finance | volatility | 1/2 avg=1.000 (widget_list_not_called_before_use) |
| build-openbb-apps/params/vol_screener | hard | widget-building | risk-review | finance | volatility | 0/2 avg=0.250 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/settings/vol_ship | hard | widget-building | risk-review | finance | volatility | 0/2 avg=0.718 (capability_fields_uncovered,capability_param_missing,capability_config_missing) |
| build-openbb-apps/params/vol_ship | hard | widget-building | risk-review | finance | volatility | 0/2 avg=0.458 (endpoint_response_incompatible,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/apps/vol_ship | hard | app-building | risk-review | finance | volatility | 0/2 avg=0.975 (capability_fields_uncovered) |
| build-openbb-apps/advanced/vol_symbol_chart | hard | widget-building | risk-review | finance | volatility | 0/2 avg=0.464 (capability_config_missing,capability_fields_uncovered,capability_param_missing) |
| build-openbb-apps/params/windowed_vix_slice | hard | widget-building | risk-review | finance | volatility | 0/2 avg=0.250 (capability_param_missing,missing_capability,capability_fields_uncovered) |
| build-openbb-apps/charts/yield_curve | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.982 (widget_def_mismatch) |
| build-openbb-apps/charts/yield_curve_app | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.986 (widget_def_mismatch) |
| build-openbb-apps/charts/yield_curve_room | hard | widget-building | macro-rates-review | finance | macro | 0/2 avg=0.592 (capability_fields_uncovered,capability_param_missing,endpoint_response_incompatible) |

## Common Interpretation

- Missing generated-widget failures often mean the model added no note/chart, added it to the wrong tab, or wrote placeholder text that did not include required task facts.
- Missing-widget and missing-tab failures are common on multi-widget dashboard tasks when the model chooses the wrong widget, tab, or data arguments.
- Invalid-call failures usually mean the model emitted a malformed tool name, used unresolved placeholders, or ignored an ID returned by an earlier observation.
- In batch mode, app-template tasks are especially sensitive to backend IDs because the model cannot read `manage_backends` output before calling `manage_apps`.

Raw outputs are under `runs/comparison/build-calibration-202607-regraded`.
