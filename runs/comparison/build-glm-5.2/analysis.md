# Workspace Bench Model Comparison

- Benchmark: `openbb-workspace-bench`
- Release: `workspace-bench-v2-build-openbb-apps`
- Scenarios: `212`
- Attempts: `212`
- Filters: `{"capability": null, "difficulty": "all", "domain": null, "level": null, "pack": "build-openbb-apps", "scenario_dir": null, "split": null, "subdomain": null, "tags": [], "workflow": null}`
- Runner: `interactive`
- Repeats: `1`

## How To Read This

`pass_rate` is strict scenario success: a scenario counts as passed only when every grader check passes and the agent process exits cleanly.
`task_pass_rate` excludes provider/process failures and asks whether valid attempts satisfied the grader.
`mean_score` is partial credit: it averages each scenario's fraction of passed checks.
`pass@k` counts a scenario when at least one repeat passes. `pass^k` counts it only when every repeat passes.
Two models can therefore have the same pass rate but different mean scores when they pass the same number of scenarios but fail with different severity.

## Summary

| Model | Strict Passed | Attempts | Strict Pass Rate | Task Pass Rate | Mean Score | Task Failures | Process Failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| GLM-5.2 | 210 | 212 | 99.1% | 100.0% | 99.9% | 0 | 2 |

## By Difficulty

| Model | Easy | Medium | Hard |
| --- | ---: | ---: | ---: |
| GLM-5.2 | 60/60 (100%) | 80/80 (100%) | 70/72 (97%) |

## By Level

| Model | L0 | L1 | L2 | L3 | L4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| GLM-5.2 | - | - | - | 190/192 (99%) | 20/20 (100%) |

## Task Issue Counts

### GLM-5.2

| Issue Code | Count |
| --- | ---: |
| `missing_widget` | 2 |
| `missing_generated_widget` | 2 |

## Process Failures

| Model | Scenario | Repeat | Exit Code | Timed Out | Stderr Preview |
| --- | --- | ---: | ---: | --- | --- |
| GLM-5.2 | auth_t4_e2e_healthcare_pipeline | 1 | 1 | False | Expecting value: line 1 column 1 (char 0) |
| GLM-5.2 | auth_t4_grouping_preview_sync_live | 1 | 1 | False | Expecting &#x27;,&#x27; delimiter: line 1 column 1861 (char 1860) |

## Scenario Matrix

| Scenario | Level | Difficulty | Capability | Workflow | Domain | Subdomain | GLM-5.2 |
| --- | --- | --- | --- | --- | --- | --- | ---: |
| auth_t0_advanced_case_qa_omni | L3 | easy | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t0_advanced_live_orders_grid | L3 | easy | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t0_advanced_rates_advanced_chart | L3 | easy | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t0_advanced_vix_advanced | L3 | easy | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t0_aggrid_auction_calendar | L3 | easy | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t0_aggrid_estimates_ssrm | L3 | easy | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t0_aggrid_open_orders | L3 | easy | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t0_aggrid_vix_history | L3 | easy | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t0_apps_order_watch | L3 | easy | app-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t0_apps_rates_morning | L3 | easy | app-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t0_apps_vendor_board | L3 | easy | app-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t0_apps_vol_overview | L3 | easy | app-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t0_charts_chains_highchart | L3 | easy | widget-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t0_charts_earnings_chart | L3 | easy | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t0_charts_pipeline_vegalite | L3 | easy | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t0_charts_yield_curve | L3 | easy | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t0_extend_add_catalyst_metric | L4 | easy | app-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t0_extend_add_curve_spread_metric | L4 | easy | app-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t0_extend_add_exception_metric | L4 | easy | app-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t0_extend_add_vol_regime_metric | L4 | easy | app-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t0_forms_access_review_form | L3 | easy | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t0_forms_incident_triage_form | L3 | easy | widget-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t0_forms_threshold_update_form | L3 | easy | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t0_forms_vendor_intake_form | L3 | easy | widget-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t0_grouping_chart_note_board | L3 | easy | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t0_grouping_earnings_symbol_board | L3 | easy | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t0_grouping_nvda_review_board | L3 | easy | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t0_grouping_revision_note_board | L3 | easy | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t0_params_case_notes | L3 | easy | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t0_params_kpi_tabs_table | L3 | easy | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t0_params_trial_catalysts | L3 | easy | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t0_params_vix_history | L3 | easy | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t0_settings_exception_metric | L3 | easy | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t0_settings_gas_metric | L3 | easy | widget-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t0_settings_rates_commentary | L3 | easy | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t0_settings_vol_regime_metric | L3 | easy | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t0_types_chains_heatmap_html | L3 | easy | widget-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t0_types_gas_metric | L3 | easy | widget-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t0_types_venue_pdf | L3 | easy | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t0_types_vol_commentary | L3 | easy | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t1_advanced_case_qa_omni_app | L3 | medium | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t1_advanced_live_orders_grid_app | L3 | easy | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t1_advanced_rates_advanced_chart_app | L3 | medium | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t1_advanced_vix_advanced_app | L3 | easy | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t1_aggrid_alert_queue_app | L3 | medium | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t1_aggrid_chains_table_app | L3 | easy | widget-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t1_aggrid_trial_catalysts_app | L3 | medium | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t1_aggrid_vendor_sla_table_app | L3 | easy | widget-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t1_apps_alert_metric_wrap | L3 | easy | app-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t1_apps_catalyst_metric_wrap | L3 | medium | app-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t1_apps_gas_metric_wrap | L3 | easy | app-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t1_apps_surprise_metric_wrap | L3 | medium | app-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t1_charts_chains_highchart_app | L3 | easy | widget-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t1_charts_earnings_chart_app | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t1_charts_pipeline_vegalite_app | L3 | medium | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t1_charts_yield_curve_app | L3 | easy | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t1_extend_place_alert_metric | L4 | medium | app-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t1_extend_place_breach_metric | L4 | medium | app-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t1_extend_place_curve_spread_metric | L4 | easy | app-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t1_extend_place_vol_regime_metric | L4 | easy | app-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t1_forms_case_escalation_form_app | L3 | easy | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t1_forms_curve_comment_form_app | L3 | medium | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t1_forms_vendor_intake_form_app | L3 | easy | widget-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t1_forms_venue_exception_form_app | L3 | medium | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t1_grouping_earnings_chart_app | L3 | easy | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t1_grouping_earnings_note_app | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t1_grouping_estimate_revisions_app | L3 | easy | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t1_grouping_symbol_click_summary_app | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t1_params_case_notes_app | L3 | medium | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t1_params_rates_commentary_app | L3 | easy | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t1_params_trial_catalysts_app | L3 | easy | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t1_params_vendor_sla_table_app | L3 | medium | widget-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t1_settings_alert_metric_app | L3 | easy | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t1_settings_catalyst_metric_app | L3 | easy | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t1_settings_sla_runbook_app | L3 | medium | widget-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t1_settings_surprise_metric_app | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t1_types_curve_monitor_iframe_app | L3 | easy | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t1_types_earnings_calls_video_app | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t1_types_evidence_files_app | L3 | medium | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t1_types_sla_newsfeed_app | L3 | easy | widget-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t2_advanced_case_prompt_omni | L3 | medium | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t2_advanced_orders_stream | L3 | medium | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t2_advanced_rates_symbol_chart | L3 | medium | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t2_advanced_vol_symbol_chart | L3 | medium | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t2_aggrid_auction_watch | L3 | medium | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t2_aggrid_fill_quality | L3 | medium | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t2_aggrid_realized_screen | L3 | medium | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t2_aggrid_revision_grid | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t2_apps_earnings_command | L3 | medium | app-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t2_apps_surveillance_morning | L3 | medium | app-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t2_apps_vendor_command | L3 | medium | app-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t2_apps_vol_morning | L3 | medium | app-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t2_charts_chain_flow_highchart | L3 | medium | widget-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t2_charts_phase_mix_vegalite | L3 | medium | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t2_charts_symbol_momentum_chart | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t2_charts_venue_slippage_chart | L3 | medium | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t2_extend_modify_case_notes | L4 | medium | app-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t2_extend_modify_rates_commentary | L4 | medium | app-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t2_extend_modify_trial_catalysts | L4 | medium | app-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t2_extend_modify_vol_screener | L4 | medium | app-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t2_forms_policy_exception_form | L3 | medium | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t2_forms_trade_break_form | L3 | medium | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t2_forms_trial_readout_form | L3 | medium | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t2_forms_vendor_review_form | L3 | medium | widget-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t2_grouping_chart_preview_sync | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t2_grouping_earnings_review_sync | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t2_grouping_full_earnings_sync | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t2_grouping_revision_preview_sync | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t2_params_kpi_param_tabs | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t2_params_series_markdown | L3 | medium | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t2_params_vol_screener | L3 | medium | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t2_params_windowed_vix_slice | L3 | medium | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t2_settings_auction_cache_grid | L3 | medium | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t2_settings_exception_refresh_grid | L3 | medium | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t2_settings_gas_refresh_metric | L3 | medium | widget-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t2_settings_runbook_markdown | L3 | medium | widget-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t2_types_call_replay_video | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t2_types_gas_priority_metric | L3 | medium | widget-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t2_types_policy_digest_pdf | L3 | medium | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t2_types_vol_playbook_note | L3 | medium | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t3_advanced_case_room_omni_room | L3 | hard | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t3_advanced_macro_advanced_chart_room | L3 | hard | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t3_advanced_orders_ops_stream_room | L3 | medium | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t3_advanced_vix_room_chart_room | L3 | medium | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t3_aggrid_case_aging | L3 | hard | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t3_aggrid_chain_flows | L3 | medium | widget-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t3_aggrid_latency_history | L3 | medium | widget-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t3_aggrid_realized_vol_grid | L3 | hard | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t3_apps_case_command | L3 | hard | app-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t3_apps_chain_deck | L3 | medium | app-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t3_apps_earnings_desk | L3 | hard | app-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t3_apps_rates_desk | L3 | medium | app-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t3_charts_chains_highchart_room | L3 | medium | widget-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t3_charts_earnings_chart_room | L3 | hard | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t3_charts_pipeline_vegalite_room | L3 | hard | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t3_charts_yield_curve_room | L3 | medium | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t3_extend_diagnose_earnings | L4 | medium | app-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t3_extend_diagnose_healthcare | L4 | medium | app-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t3_extend_diagnose_rates | L4 | hard | app-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t3_extend_diagnose_sla | L4 | hard | app-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t3_forms_case_intake_room | L3 | medium | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t3_forms_exception_intake_room | L3 | hard | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t3_forms_trial_intake_room | L3 | hard | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t3_forms_vendor_intake_room | L3 | medium | widget-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t3_grouping_click_preview_desk | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t3_grouping_click_revision_desk | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t3_grouping_click_season_desk | L3 | hard | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t3_grouping_click_summary_desk | L3 | hard | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t3_params_earnings_param_review | L3 | medium | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t3_params_symbol_param_desk | L3 | hard | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t3_params_trial_param_review | L3 | medium | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t3_params_vol_param_cockpit | L3 | hard | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t3_settings_alert_metric_room | L3 | hard | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t3_settings_gas_metric_room | L3 | medium | widget-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t3_settings_surprise_metric_room | L3 | hard | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t3_settings_vol_commentary_room | L3 | medium | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t3_types_case_notes_room | L3 | medium | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t3_types_earnings_calls_video_room | L3 | hard | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t3_types_evidence_files_room | L3 | hard | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t3_types_fda_newsfeed_room | L3 | medium | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t4_advanced_case_qa_omni_ship | L3 | hard | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t4_advanced_live_orders_grid_ship | L3 | hard | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t4_advanced_rates_live_chart_ship | L3 | hard | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t4_advanced_vix_advanced_ship | L3 | hard | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t4_aggrid_earnings_ship | L3 | hard | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t4_aggrid_execution_ship | L3 | hard | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t4_aggrid_healthcare_ship | L3 | hard | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t4_aggrid_rates_ship | L3 | hard | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t4_apps_healthcare_ship | L3 | hard | app-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t4_apps_sla_ship | L3 | hard | app-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t4_apps_tvl_ship | L3 | hard | app-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t4_apps_vol_ship | L3 | hard | app-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t4_charts_earnings_ship | L3 | hard | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t4_charts_healthcare_ship | L3 | hard | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t4_charts_rates_ship | L3 | hard | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t4_charts_tvl_ship | L3 | hard | widget-building | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t4_e2e_case_triage | L3 | hard | backend-integration | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t4_e2e_catalyst_calendar | L3 | hard | backend-integration | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t4_e2e_chain_flows | L3 | hard | backend-integration | portfolio-morning-review | finance | crypto | PASS 1.000 |
| auth_t4_e2e_compliance_surveillance | L3 | hard | backend-integration | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t4_e2e_earnings_season | L3 | hard | backend-integration | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t4_e2e_execution_monitor | L3 | hard | backend-integration | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t4_e2e_healthcare_pipeline | L3 | hard | backend-integration | healthcare-catalyst-review | finance | healthcare | FAIL 0.920 (missing_widget,missing_generated_widget) |
| auth_t4_e2e_macro_morning | L3 | hard | backend-integration | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t4_e2e_rates_auctions | L3 | hard | backend-integration | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t4_e2e_research_room | L3 | hard | backend-integration | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t4_e2e_vendor_ops | L3 | hard | backend-integration | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t4_e2e_vol_cockpit | L3 | hard | backend-integration | risk-review | finance | volatility | PASS 1.000 |
| auth_t4_extend_repair_compliance | L4 | hard | app-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t4_extend_repair_execution | L4 | hard | app-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t4_extend_repair_rates | L4 | hard | app-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t4_extend_repair_vol | L4 | hard | app-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t4_forms_compliance_ship | L3 | hard | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t4_forms_execution_ship | L3 | hard | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t4_forms_healthcare_ship | L3 | hard | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t4_forms_sla_ship | L3 | hard | widget-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t4_grouping_chart_sync_live | L3 | hard | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t4_grouping_click_sync_live | L3 | hard | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t4_grouping_earnings_sync_live | L3 | hard | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t4_grouping_preview_sync_live | L3 | hard | widget-building | earnings-prep | finance | equity-research | FAIL 0.895 (missing_widget,missing_generated_widget) |
| auth_t4_params_earnings_ship | L3 | hard | widget-building | earnings-prep | finance | equity-research | PASS 1.000 |
| auth_t4_params_healthcare_ship | L3 | hard | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t4_params_rates_ship | L3 | hard | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t4_params_vol_ship | L3 | hard | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t4_settings_execution_ship | L3 | hard | widget-building | execution-exception-review | finance | execution | PASS 1.000 |
| auth_t4_settings_healthcare_ship | L3 | hard | widget-building | healthcare-catalyst-review | finance | healthcare | PASS 1.000 |
| auth_t4_settings_rates_ship | L3 | hard | widget-building | macro-rates-review | finance | macro | PASS 1.000 |
| auth_t4_settings_vol_ship | L3 | hard | widget-building | risk-review | finance | volatility | PASS 1.000 |
| auth_t4_types_evidence_files_ship | L3 | hard | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t4_types_policy_digest_pdf_ship | L3 | hard | widget-building | compliance-surveillance | finance | compliance | PASS 1.000 |
| auth_t4_types_sla_newsfeed_ship | L3 | hard | widget-building | vendor-sla-monitoring | finance | operations | PASS 1.000 |
| auth_t4_types_venue_packet_pdf_ship | L3 | hard | widget-building | execution-exception-review | finance | execution | PASS 1.000 |

## Common Interpretation

- Missing generated-widget failures often mean the model added no note/chart, added it to the wrong tab, or wrote placeholder text that did not include required task facts.
- Missing-widget and missing-tab failures are common on multi-widget dashboard tasks when the model chooses the wrong widget, tab, or data arguments.
- Invalid-call failures usually mean the model emitted a malformed tool name, used unresolved placeholders, or ignored an ID returned by an earlier observation.
- In batch mode, app-template tasks are especially sensitive to backend IDs because the model cannot read `manage_backends` output before calling `manage_apps`.

Raw outputs are under `runs/comparison/build-glm-5.2`.
