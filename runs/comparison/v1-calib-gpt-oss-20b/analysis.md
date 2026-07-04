# Workspace Bench Model Comparison

- Benchmark: `openbb-workspace-bench`
- Release: `workspace-bench-v1`
- Scenarios: `300`
- Attempts: `300`
- Filters: `{"capability": null, "difficulty": "all", "domain": null, "level": null, "pack": "all", "scenario_dir": null, "split": null, "subdomain": null, "tags": [], "workflow": null}`
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
| Ollama gpt-oss:20b | 178 | 300 | 59.3% | 64.0% | 91.8% | 100 | 22 |

## By Difficulty

| Model | Easy | Medium | Hard |
| --- | ---: | ---: | ---: |
| Ollama gpt-oss:20b | 76/90 (84%) | 67/120 (56%) | 35/90 (39%) |

## By Level

| Model | L0 | L1 | L2 | L3 | L4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Ollama gpt-oss:20b | 13/28 (46%) | 90/124 (73%) | 29/76 (38%) | 31/40 (78%) | 15/32 (47%) |

## Task Issue Counts

### Ollama gpt-oss:20b

| Issue Code | Count |
| --- | ---: |
| `too_many_invalid_calls` | 78 |
| `missing_generated_widget` | 42 |
| `missing_widget` | 37 |
| `missing_tool_call` | 21 |
| `layout_mismatch` | 13 |
| `schema_not_called_before_create` | 9 |
| `missing_tool_result` | 4 |
| `dashboard_name` | 4 |
| `missing_tab` | 3 |
| `too_many_widgets` | 1 |

## Process Failures

| Model | Scenario | Repeat | Exit Code | Timed Out | Stderr Preview |
| --- | --- | ---: | ---: | --- | --- |
| Ollama gpt-oss:20b | gen_t1_backends_add_widget_earnings_estimates_monitor_post_earnings_post_earnings_checklist_3 | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T03:56:23.23588Z&#x27;, &#x27;message&#x27;: {&#x27;ro |
| Ollama gpt-oss:20b | gen_t1_backends_add_widget_holdings_table_2 | 1 | 1 | False | model API request failed: HTTP 500: {&quot;error&quot;:&quot;error parsing tool call: raw=&#x27;&#x27;, err=unexpected end of JSON input&quot;} |
| Ollama gpt-oss:20b | gen_t1_create_estimate_history_nvda | 1 | 1 | False | model API request failed: HTTP 500: {&quot;error&quot;:&quot;error parsing tool call: raw=&#x27;&#x27;, err=unexpected end of JSON input&quot;} |
| Ollama gpt-oss:20b | gen_t1_inspect_fix_macro_timeseries_2 | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T03:58:43.992713Z&#x27;, &#x27;message&#x27;: {&#x27;r |
| Ollama gpt-oss:20b | gen_t1_note_fact_top_holding | 1 | 1 | False | model API request failed: HTTP 500: {&quot;error&quot;:&quot;error parsing tool call: raw=&#x27;&#x27;, err=unexpected end of JSON input&quot;} |
| Ollama gpt-oss:20b | gen_t1_params_schema_sector_client_360_portfolio_view_exposure_summary_7 | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:00:47.910553Z&#x27;, &#x27;message&#x27;: {&#x27;r |
| Ollama gpt-oss:20b | gen_t1_prompts_tool_usage_healthcare_research_dashboard_documents_healthcare_thesis_note_3 | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:01:32.074308Z&#x27;, &#x27;message&#x27;: {&#x27;r |
| Ollama gpt-oss:20b | gen_t2_backends_cross_equity_research_workbench_company_ownership_snapshot_risk_metrics_2 | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:05:50.588743Z&#x27;, &#x27;message&#x27;: {&#x27;r |
| Ollama gpt-oss:20b | gen_t2_params_place_sector_compliance_surveillance_hub_audit_access_and_export_logs_11 | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:13:35.563893Z&#x27;, &#x27;message&#x27;: {&#x27;r |
| Ollama gpt-oss:20b | gen_t2_prompts_session_tab_ops_liquidity_tca_workbench_tca_slippage_by_algo | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:15:48.388835Z&#x27;, &#x27;message&#x27;: {&#x27;r |
| Ollama gpt-oss:20b | gen_t3_backends_refresh_earnings_estimates_monitor_post_earnings_post_earnings_checklist_3 | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:20:56.316925Z&#x27;, &#x27;message&#x27;: {&#x27;r |
| Ollama gpt-oss:20b | gen_t3_params_companion_sector_corporate_access_meeting_notes_claims_evidence_and_sign_off_history_3 | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:28:36.3601Z&#x27;, &#x27;message&#x27;: {&#x27;rol |
| Ollama gpt-oss:20b | gen_t3_prompts_dashboard_stark_prompt_dashboard | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:32:07.88172Z&#x27;, &#x27;message&#x27;: {&#x27;ro |
| Ollama gpt-oss:20b | gen_t3_resources_skill_build_finance_guidance_tracker | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:33:49.175431Z&#x27;, &#x27;message&#x27;: {&#x27;r |
| Ollama gpt-oss:20b | gen_t4_app_full_crypto_research_dashboard | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:36:21.75571Z&#x27;, &#x27;message&#x27;: {&#x27;ro |
| Ollama gpt-oss:20b | gen_t4_backends_multi_stark_portfolio | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:38:57.964486Z&#x27;, &#x27;message&#x27;: {&#x27;r |
| Ollama gpt-oss:20b | gen_t4_delegate_build_earnings_build | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:41:03.904187Z&#x27;, &#x27;message&#x27;: {&#x27;r |
| Ollama gpt-oss:20b | gen_t4_delegate_build_exec_build | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:41:18.489486Z&#x27;, &#x27;message&#x27;: {&#x27;r |
| Ollama gpt-oss:20b | gen_t4_delegate_build_risk_build | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:41:41.896434Z&#x27;, &#x27;message&#x27;: {&#x27;r |
| Ollama gpt-oss:20b | gen_t4_delegate_build_vendor_build | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:41:56.27473Z&#x27;, &#x27;message&#x27;: {&#x27;ro |
| Ollama gpt-oss:20b | gen_t4_params_cross_stark_sector | 1 | 1 | False | Ollama returned no message content: {&#x27;model&#x27;: &#x27;gpt-oss:20b&#x27;, &#x27;created_at&#x27;: &#x27;2026-07-04T04:50:21.666735Z&#x27;, &#x27;message&#x27;: {&#x27;r |
| Ollama gpt-oss:20b | gen_t4_prompts_cross_prompt_cross_stark_risk | 1 | 1 | False | model API request failed: HTTP 500: {&quot;error&quot;:&quot;error parsing tool call: raw=&#x27;&#x27;, err=unexpected end of JSON input&quot;} |

## Scenario Matrix

| Scenario | Level | Difficulty | Capability | Workflow | Domain | Subdomain | Ollama gpt-oss:20b |
| --- | --- | --- | --- | --- | --- | --- | ---: |
| gen_t0_app_client_360 | L3 | easy | app-instantiation | client-meeting-prep | finance | client-ir | PASS 1.000 |
| gen_t0_app_execution_desk | L3 | easy | app-instantiation | execution-exception-review | finance | execution | PASS 1.000 |
| gen_t0_app_risk_exposure_monitor | L3 | easy | app-instantiation | risk-review | finance | risk | PASS 1.000 |
| gen_t0_app_vendor_dataset_monitor | L3 | easy | app-instantiation | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |
| gen_t0_backends_add_equities | L2 | easy | dashboard-construction | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_backends_add_macro | L2 | easy | dashboard-construction | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t0_backends_add_portfolio | L2 | easy | dashboard-construction | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t0_backends_add_stark_enterprise | L2 | easy | dashboard-construction | earnings-prep | finance | equity-research | PASS 1.000 |
| gen_t0_create_latest_news_aapl | L1 | easy | widget-creation | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_create_price_performance_aapl | L1 | easy | widget-creation | equity-tearsheet | finance | equity-research | FAIL 0.800 (too_many_invalid_calls) |
| gen_t0_create_risk_metrics_plain | L1 | easy | widget-creation | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t0_create_yield_curve_plain | L1 | easy | widget-creation | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t0_delegate_client_single | L3 | easy | mcp-tool-use | client-meeting-prep | finance | client-ir | PASS 1.000 |
| gen_t0_delegate_earnings_single | L3 | easy | mcp-tool-use | earnings-prep | finance | equity-research | PASS 1.000 |
| gen_t0_delegate_risk_single | L3 | easy | mcp-tool-use | risk-review | finance | risk | PASS 1.000 |
| gen_t0_delegate_vendor_single | L3 | easy | mcp-tool-use | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |
| gen_t0_delete_alerts_47 | L1 | easy | widget-update | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t0_delete_news_12 | L1 | easy | widget-update | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_delete_performance_18 | L1 | easy | widget-update | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_delete_timeseries_17 | L1 | easy | widget-update | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t0_inspect_read_holdings_table_2 | L0 | easy | workspace-inspection | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t0_inspect_read_macro_timeseries_1 | L0 | easy | workspace-inspection | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t0_inspect_read_portfolio_command_center_overview_workflow_overview_3 | L0 | easy | workspace-inspection | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t0_inspect_read_price_performance_0 | L0 | easy | workspace-inspection | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_layout_halve_price_msft | L1 | easy | layout-management | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_layout_move_news_right | L1 | easy | layout-management | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_layout_shorten_estimates_nvda | L1 | easy | layout-management | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_layout_widen_fundamentals_aapl | L1 | easy | layout-management | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_nav_rename_compliance_day | L1 | easy | workspace-navigation | compliance-surveillance | finance | compliance | FAIL 0.833 (too_many_invalid_calls) |
| gen_t0_nav_rename_equity_desk | L1 | easy | workspace-navigation | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_nav_rename_execution_open | L1 | easy | workspace-navigation | execution-exception-review | finance | execution | PASS 1.000 |
| gen_t0_nav_rename_macro_watch | L1 | easy | workspace-navigation | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t0_note_handover | L1 | easy | workspace-inspection | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t0_note_outage | L1 | easy | workspace-inspection | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t0_note_reminder | L1 | easy | workspace-inspection | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t0_note_standup | L1 | easy | workspace-inspection | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t0_params_sector_client_360_meeting_prep_relationship_metrics_3 | L1 | easy | parameter-discovery | client-meeting-prep | finance | client-ir | PASS 1.000 |
| gen_t0_params_sector_sector_exposure_2 | L1 | easy | parameter-discovery | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t0_params_series_macro_timeseries_1 | L1 | easy | parameter-discovery | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t0_params_symbol_price_performance_0 | L1 | easy | parameter-discovery | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_prompts_fetch_workspace_session_context_1 | L0 | easy | prompt-access | workspace-guidance | workspace-usability | mcp-prompts | PASS 1.000 |
| gen_t0_prompts_fetch_workspace_session_context_3 | L0 | easy | prompt-access | workspace-guidance | workspace-usability | mcp-prompts | PASS 1.000 |
| gen_t0_prompts_fetch_workspace_tool_usage_0 | L0 | easy | prompt-access | workspace-guidance | workspace-usability | mcp-prompts | PASS 1.000 |
| gen_t0_prompts_fetch_workspace_tool_usage_2 | L0 | easy | prompt-access | workspace-guidance | workspace-usability | mcp-prompts | PASS 1.000 |
| gen_t0_read_attribution | L1 | easy | data-reading | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t0_read_latency | L1 | easy | data-reading | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |
| gen_t0_read_limits | L1 | easy | data-reading | risk-review | finance | risk | PASS 1.000 |
| gen_t0_read_order_status | L1 | easy | data-reading | execution-exception-review | finance | execution | FAIL 0.833 (missing_generated_widget) |
| gen_t0_resources_skill_finance_comps | L0 | easy | resource-access | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_resources_skill_finance_earnings_prep | L0 | easy | resource-access | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_resources_skill_finance_guidance_tracker | L0 | easy | resource-access | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_resources_skill_finance_tearsheet | L0 | easy | resource-access | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_skill_finance_comps | L1 | easy | skill-access | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_skill_finance_earnings_prep | L1 | easy | skill-access | earnings-prep | finance | equity-research | PASS 1.000 |
| gen_t0_skill_finance_guidance_tracker | L1 | easy | skill-access | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_skill_finance_tearsheet | L1 | easy | skill-access | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t0_update_period_mtd_56 | L1 | easy | widget-update | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t0_update_series_dgs10_17 | L1 | easy | widget-update | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t0_update_symbol_aapl_18 | L1 | easy | widget-update | equity-tearsheet | finance | equity-research | FAIL 0.750 (too_many_invalid_calls) |
| gen_t0_update_symbol_msft_12 | L1 | easy | widget-update | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t1_app_compliance_surveillance_hub | L3 | easy | app-instantiation | compliance-surveillance | finance | compliance | PASS 1.000 |
| gen_t1_app_earnings_estimates_monitor | L3 | medium | app-instantiation | earnings-prep | finance | equity-research | PASS 1.000 |
| gen_t1_app_equity_research_workbench | L3 | easy | app-instantiation | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t1_app_executive_investment_dashboard | L3 | medium | app-instantiation | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t1_backends_add_widget_earnings_estimates_monitor_post_earnings_post_earnings_checklist_3 | L2 | medium | dashboard-construction | earnings-prep | finance | equity-research | FAIL 0.750 (missing_widget) |
| gen_t1_backends_add_widget_holdings_table_2 | L2 | medium | dashboard-construction | portfolio-risk-review | finance | portfolio-management | FAIL 0.750 (missing_widget) |
| gen_t1_backends_add_widget_macro_timeseries_1 | L2 | easy | dashboard-construction | macro-rates-review | finance | macro | FAIL 0.889 (too_many_invalid_calls) |
| gen_t1_backends_add_widget_price_performance_0 | L2 | easy | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.889 (too_many_invalid_calls) |
| gen_t1_create_estimate_history_nvda | L1 | easy | widget-creation | equity-tearsheet | finance | equity-research | FAIL 0.333 (missing_widget,too_many_invalid_calls) |
| gen_t1_create_macro_timeseries_dgs10 | L1 | medium | widget-creation | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t1_create_price_performance_msft | L1 | easy | widget-creation | equity-tearsheet | finance | equity-research | FAIL 0.875 (too_many_invalid_calls) |
| gen_t1_create_sector_exposure_plain | L1 | medium | widget-creation | portfolio-risk-review | finance | portfolio-management | FAIL 0.875 (too_many_invalid_calls) |
| gen_t1_delegate_client_pair | L3 | medium | mcp-tool-use | client-meeting-prep | finance | client-ir | PASS 1.000 |
| gen_t1_delegate_compliance_pair | L3 | medium | mcp-tool-use | compliance-surveillance | finance | compliance | PASS 1.000 |
| gen_t1_delegate_earnings_pair | L3 | easy | mcp-tool-use | earnings-prep | finance | equity-research | PASS 1.000 |
| gen_t1_delegate_risk_pair | L3 | easy | mcp-tool-use | risk-review | finance | risk | PASS 1.000 |
| gen_t1_delete_dup_news_12 | L1 | easy | widget-update | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t1_delete_dup_performance_18 | L1 | easy | widget-update | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t1_delete_dup_status_48 | L1 | medium | widget-update | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |
| gen_t1_delete_dup_timeseries_17 | L1 | medium | widget-update | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t1_inspect_fix_estimate_history_1 | L1 | easy | workspace-repair | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t1_inspect_fix_macro_timeseries_2 | L1 | medium | workspace-repair | macro-rates-review | finance | macro | FAIL 0.600 (missing_widget,missing_tool_call) |
| gen_t1_inspect_fix_price_performance_0 | L1 | easy | workspace-repair | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t1_inspect_fix_quant_research_backtest_lab_risk_model_factor_exposure_table_3 | L1 | medium | workspace-repair | risk-review | finance | risk | PASS 1.000 |
| gen_t1_layout_preserve_estimates_fundamentals_msft | L1 | easy | layout-management | equity-tearsheet | finance | equity-research | FAIL 0.857 (too_many_invalid_calls) |
| gen_t1_layout_preserve_macro_pair | L1 | medium | layout-management | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t1_layout_preserve_portfolio_pair | L1 | medium | layout-management | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t1_layout_preserve_price_news_aapl | L1 | easy | layout-management | equity-tearsheet | finance | equity-research | FAIL 0.857 (too_many_invalid_calls) |
| gen_t1_nav_rename_both_client_review | L1 | easy | workspace-navigation | client-meeting-prep | finance | client-ir | PASS 1.000 |
| gen_t1_nav_rename_both_earnings_week | L1 | medium | workspace-navigation | earnings-prep | finance | equity-research | PASS 1.000 |
| gen_t1_nav_rename_both_ops_close | L1 | easy | workspace-navigation | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |
| gen_t1_nav_rename_both_pm_morning | L1 | medium | workspace-navigation | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t1_note_fact_close_aapl | L0 | easy | workspace-inspection | equity-tearsheet | finance | equity-research | FAIL 0.833 (too_many_invalid_calls) |
| gen_t1_note_fact_close_msft | L0 | easy | workspace-inspection | equity-tearsheet | finance | equity-research | FAIL 0.833 (missing_generated_widget) |
| gen_t1_note_fact_macro_10y | L0 | medium | workspace-inspection | macro-rates-review | finance | macro | FAIL 0.833 (missing_generated_widget) |
| gen_t1_note_fact_top_holding | L0 | medium | workspace-inspection | portfolio-risk-review | finance | portfolio-management | FAIL 0.600 (missing_generated_widget,too_many_invalid_calls) |
| gen_t1_params_schema_sector_client_360_portfolio_view_exposure_summary_7 | L1 | medium | parameter-discovery | client-meeting-prep | finance | client-ir | FAIL 0.667 (missing_widget,missing_tool_call,missing_tool_result) |
| gen_t1_params_schema_sector_sector_exposure_6 | L1 | medium | parameter-discovery | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t1_params_schema_series_macro_timeseries_5 | L1 | easy | parameter-discovery | macro-rates-review | finance | macro | FAIL 0.900 (too_many_invalid_calls) |
| gen_t1_params_schema_symbol_price_performance_4 | L1 | easy | parameter-discovery | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t1_prompts_tool_usage_healthcare_research_dashboard_documents_healthcare_thesis_note_3 | L2 | medium | dashboard-construction | healthcare-catalyst-review | workspace-usability | healthcare-research | FAIL 0.875 (missing_widget) |
| gen_t1_prompts_tool_usage_macro_timeseries_1 | L2 | easy | dashboard-construction | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t1_prompts_tool_usage_price_performance_0 | L2 | easy | dashboard-construction | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t1_prompts_tool_usage_risk_metrics_2 | L2 | medium | dashboard-construction | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t1_read_alert_trend | L1 | easy | data-reading | compliance-surveillance | finance | compliance | PASS 1.000 |
| gen_t1_read_break_aging | L1 | medium | data-reading | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |
| gen_t1_read_pipeline | L1 | easy | data-reading | client-meeting-prep | finance | client-ir | PASS 1.000 |
| gen_t1_read_strategy_health | L1 | medium | data-reading | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t1_resources_index_client_360 | L2 | medium | dashboard-construction | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t1_resources_index_equity_earnings_review | L2 | easy | dashboard-construction | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t1_resources_index_portfolio_command_center | L2 | easy | dashboard-construction | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t1_resources_index_risk_exposure_monitor | L2 | medium | dashboard-construction | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t1_skill_finance_comps | L1 | medium | skill-access | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t1_skill_finance_earnings_prep | L1 | easy | skill-access | earnings-prep | finance | equity-research | PASS 1.000 |
| gen_t1_skill_finance_guidance_tracker | L1 | medium | skill-access | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t1_skill_finance_tearsheet | L1 | easy | skill-access | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t1_update_series_fedfunds_17 | L1 | medium | widget-update | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t1_update_status_escalated_44 | L1 | medium | widget-update | execution-exception-review | finance | execution | FAIL 0.833 (too_many_invalid_calls) |
| gen_t1_update_symbol_nvda_17 | L1 | easy | widget-update | equity-tearsheet | finance | equity-research | FAIL 0.500 (missing_widget,too_many_widgets,too_many_invalid_calls) |
| gen_t1_update_symbol_nvda_20 | L1 | easy | widget-update | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t2_app_note_nav_fees_close_dashboard | L3 | medium | app-instantiation | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |
| gen_t2_app_note_quant_research_backtest_lab | L3 | medium | app-instantiation | risk-review | finance | risk | PASS 1.000 |
| gen_t2_app_note_reporting_factsheet_studio | L3 | medium | app-instantiation | client-meeting-prep | finance | client-ir | FAIL 0.957 (too_many_invalid_calls) |
| gen_t2_app_note_stress_liquidity_lab | L3 | medium | app-instantiation | risk-review | finance | risk | PASS 1.000 |
| gen_t2_backends_cross_equity_research_workbench_company_ownership_snapshot_risk_metrics_2 | L2 | medium | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.600 (missing_widget,missing_widget) |
| gen_t2_backends_cross_fundamental_metrics_holdings_table_3 | L2 | medium | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.929 (too_many_invalid_calls) |
| gen_t2_backends_cross_latest_news_yield_curve_0 | L2 | medium | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.929 (too_many_invalid_calls) |
| gen_t2_backends_cross_sector_exposure_macro_timeseries_1 | L2 | medium | dashboard-construction | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t2_create_place_fundamental_metrics_aapl | L1 | medium | widget-creation | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t2_create_place_latest_news_msft | L1 | medium | widget-creation | equity-tearsheet | finance | equity-research | FAIL 0.800 (missing_widget,too_many_invalid_calls) |
| gen_t2_create_place_macro_timeseries_fedfunds | L1 | medium | widget-creation | macro-rates-review | finance | macro | FAIL 0.900 (too_many_invalid_calls) |
| gen_t2_create_place_price_performance_nvda | L1 | medium | widget-creation | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t2_delegate_client_note | L3 | medium | mcp-tool-use | client-meeting-prep | finance | client-ir | FAIL 0.875 (missing_generated_widget) |
| gen_t2_delegate_earnings_note | L3 | medium | mcp-tool-use | earnings-prep | finance | equity-research | PASS 1.000 |
| gen_t2_delegate_ops_note | L3 | medium | mcp-tool-use | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |
| gen_t2_delegate_risk_note | L3 | medium | mcp-tool-use | risk-review | finance | risk | PASS 1.000 |
| gen_t2_delete_similar_estimate_history_msft | L1 | medium | widget-update | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t2_delete_similar_latest_news_nvda | L1 | medium | widget-update | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t2_delete_similar_macro_timeseries_dgs10 | L1 | medium | widget-update | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t2_delete_similar_price_performance_aapl | L1 | medium | widget-update | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t2_inspect_deduplicate_latest_news_0 | L2 | medium | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.800 (missing_tool_call,too_many_invalid_calls) |
| gen_t2_inspect_deduplicate_macro_timeseries_1 | L2 | medium | dashboard-construction | macro-rates-review | finance | macro | FAIL 0.900 (missing_tool_call) |
| gen_t2_inspect_deduplicate_rebalance_scenario_lab_drift_drift_by_sleeve_3 | L2 | medium | dashboard-construction | portfolio-morning-review | finance | portfolio-management | FAIL 0.900 (missing_tool_call) |
| gen_t2_inspect_deduplicate_risk_metrics_2 | L2 | medium | dashboard-construction | portfolio-risk-review | finance | portfolio-management | FAIL 0.800 (missing_tool_call,too_many_invalid_calls) |
| gen_t2_layout_arrange_split_macro | L1 | medium | layout-management | macro-rates-review | finance | macro | FAIL 0.714 (layout_mismatch,layout_mismatch) |
| gen_t2_layout_arrange_split_portfolio | L1 | medium | layout-management | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t2_layout_arrange_split_price_news_aapl | L1 | medium | layout-management | equity-tearsheet | finance | equity-research | FAIL 0.714 (layout_mismatch,layout_mismatch) |
| gen_t2_layout_arrange_stack_price_news_nvda | L1 | medium | layout-management | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t2_nav_expand_client_expansion | L1 | medium | workspace-navigation | client-meeting-prep | finance | client-ir | PASS 1.000 |
| gen_t2_nav_expand_research_expansion | L1 | medium | workspace-navigation | equity-tearsheet | finance | equity-research | FAIL 0.900 (too_many_invalid_calls) |
| gen_t2_nav_expand_risk_expansion | L1 | medium | workspace-navigation | risk-review | finance | risk | PASS 1.000 |
| gen_t2_nav_expand_vendor_expansion | L1 | medium | workspace-navigation | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |
| gen_t2_note_twofacts_estimates_aapl | L0 | medium | workspace-inspection | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t2_note_twofacts_estimates_msft | L0 | medium | workspace-inspection | equity-tearsheet | finance | equity-research | FAIL 0.714 (missing_generated_widget,too_many_invalid_calls) |
| gen_t2_note_twofacts_fundamentals_aapl | L0 | medium | workspace-inspection | equity-tearsheet | finance | equity-research | FAIL 0.857 (missing_generated_widget) |
| gen_t2_note_twofacts_fundamentals_nvda | L0 | medium | workspace-inspection | equity-tearsheet | finance | equity-research | FAIL 0.714 (missing_generated_widget,too_many_invalid_calls) |
| gen_t2_params_place_sector_compliance_surveillance_hub_audit_access_and_export_logs_11 | L2 | medium | dashboard-construction | compliance-surveillance | finance | compliance | FAIL 0.667 (missing_widget,layout_mismatch,too_many_invalid_calls) |
| gen_t2_params_place_sector_sector_exposure_10 | L2 | medium | dashboard-construction | portfolio-risk-review | finance | portfolio-management | FAIL 0.600 (missing_widget,layout_mismatch,missing_tool_result) |
| gen_t2_params_place_series_macro_timeseries_9 | L2 | medium | dashboard-construction | macro-rates-review | finance | macro | FAIL 0.900 (too_many_invalid_calls) |
| gen_t2_params_place_symbol_price_performance_8 | L2 | medium | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.900 (too_many_invalid_calls) |
| gen_t2_prompts_session_tab_estimates_estimate_history | L2 | medium | dashboard-construction | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t2_prompts_session_tab_exposure_sector_exposure | L2 | medium | dashboard-construction | portfolio-risk-review | finance | portfolio-management | FAIL 0.909 (too_many_invalid_calls) |
| gen_t2_prompts_session_tab_ops_liquidity_tca_workbench_tca_slippage_by_algo | L2 | medium | dashboard-construction | execution-exception-review | finance | execution | FAIL 0.818 (missing_widget,missing_generated_widget) |
| gen_t2_prompts_session_tab_rates_yield_curve | L2 | medium | dashboard-construction | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t2_read_broker_scorecard | L1 | medium | data-reading | execution-exception-review | finance | execution | PASS 1.000 |
| gen_t2_read_issuer_conc | L1 | medium | data-reading | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t2_read_sla_metrics | L1 | medium | data-reading | vendor-sla-monitoring | finance | data-platform | FAIL 0.667 (missing_generated_widget,too_many_invalid_calls) |
| gen_t2_read_var_trend | L1 | medium | data-reading | risk-review | finance | risk | PASS 1.000 |
| gen_t2_resources_instantiate_compliance_surveillance_hub | L2 | medium | dashboard-construction | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t2_resources_instantiate_equity_earnings_review | L2 | medium | dashboard-construction | earnings-prep | finance | equity-research | PASS 1.000 |
| gen_t2_resources_instantiate_execution_desk | L2 | medium | dashboard-construction | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t2_resources_instantiate_vendor_dataset_monitor | L2 | medium | dashboard-construction | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t2_skill_finance_comps | L1 | medium | skill-access | equity-tearsheet | finance | equity-research | FAIL 0.900 (too_many_invalid_calls) |
| gen_t2_skill_finance_earnings_prep | L1 | medium | skill-access | earnings-prep | finance | equity-research | PASS 1.000 |
| gen_t2_skill_finance_guidance_tracker | L1 | medium | skill-access | equity-tearsheet | finance | equity-research | FAIL 0.900 (too_many_invalid_calls) |
| gen_t2_skill_finance_tearsheet | L1 | medium | skill-access | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t2_update_pick_series_dgs2_17 | L1 | medium | widget-update | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t2_update_pick_symbol_msft_18 | L1 | medium | widget-update | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t2_update_pick_symbol_nvda_12 | L1 | medium | widget-update | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t2_update_pick_vendor_factset_48 | L1 | medium | widget-update | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |
| gen_t3_app_extend_fund_operations_control_tower | L3 | hard | app-instantiation | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |
| gen_t3_app_extend_portfolio_command_center | L3 | medium | app-instantiation | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t3_app_extend_rebalance_scenario_lab | L3 | medium | app-instantiation | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t3_app_extend_strategy_health_monitor | L3 | hard | app-instantiation | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t3_backends_refresh_earnings_estimates_monitor_post_earnings_post_earnings_checklist_3 | L2 | hard | dashboard-construction | earnings-prep | finance | equity-research | FAIL 0.600 (missing_widget,missing_generated_widget) |
| gen_t3_backends_refresh_holdings_table_2 | L2 | hard | dashboard-construction | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t3_backends_refresh_macro_timeseries_1 | L2 | medium | dashboard-construction | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t3_backends_refresh_price_performance_0 | L2 | medium | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.900 (schema_not_called_before_create) |
| gen_t3_create_preserve_fundamental_metrics_msft | L1 | hard | widget-creation | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t3_create_preserve_latest_news_aapl | L1 | medium | widget-creation | equity-tearsheet | finance | equity-research | FAIL 0.800 (missing_widget,schema_not_called_before_create) |
| gen_t3_create_preserve_risk_metrics_plain | L1 | hard | widget-creation | portfolio-risk-review | finance | portfolio-management | FAIL 0.909 (too_many_invalid_calls) |
| gen_t3_create_preserve_yield_curve_plain | L1 | medium | widget-creation | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t3_delegate_skill_comps_skill | L3 | hard | mcp-tool-use | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t3_delegate_skill_earnings_skill | L3 | medium | mcp-tool-use | earnings-prep | finance | equity-research | PASS 1.000 |
| gen_t3_delegate_skill_guidance_skill | L3 | hard | mcp-tool-use | equity-tearsheet | finance | equity-research | FAIL 0.900 (missing_generated_widget) |
| gen_t3_delegate_skill_tearsheet_skill | L3 | medium | mcp-tool-use | equity-tearsheet | finance | equity-research | FAIL 0.900 (missing_generated_widget) |
| gen_t3_delete_note_exposure_16 | L4 | hard | workspace-repair | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t3_delete_note_history_17 | L4 | medium | workspace-repair | equity-tearsheet | finance | equity-research | FAIL 0.875 (too_many_invalid_calls) |
| gen_t3_delete_note_metrics_20 | L4 | medium | workspace-repair | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t3_delete_note_orders_36 | L4 | hard | workspace-repair | execution-exception-review | finance | execution | PASS 1.000 |
| gen_t3_inspect_overlap_holdings_table_2 | L4 | hard | workspace-repair | portfolio-risk-review | finance | portfolio-management | FAIL 0.750 (missing_tool_call,too_many_invalid_calls) |
| gen_t3_inspect_overlap_macro_timeseries_1 | L4 | medium | workspace-repair | macro-rates-review | finance | macro | FAIL 0.875 (missing_tool_call) |
| gen_t3_inspect_overlap_price_performance_0 | L4 | medium | workspace-repair | equity-tearsheet | finance | equity-research | FAIL 0.875 (missing_tool_call) |
| gen_t3_inspect_overlap_reporting_factsheet_studio_commentary_disclosure_checklist_3 | L4 | hard | workspace-repair | client-meeting-prep | finance | client-ir | FAIL 0.875 (missing_tool_call) |
| gen_t3_layout_overlap_overlap_estimates_fund_msft | L4 | medium | workspace-repair | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t3_layout_overlap_overlap_macro | L4 | hard | workspace-repair | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t3_layout_overlap_overlap_portfolio | L4 | hard | workspace-repair | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t3_layout_overlap_overlap_price_news_aapl | L4 | medium | workspace-repair | equity-tearsheet | finance | equity-research | FAIL 0.857 (too_many_invalid_calls) |
| gen_t3_nav_addtab_curve | L4 | hard | workspace-repair | macro-rates-review | finance | macro | FAIL 0.833 (missing_widget,too_many_invalid_calls) |
| gen_t3_nav_addtab_estimates_msft | L4 | medium | workspace-repair | equity-tearsheet | finance | equity-research | FAIL 0.944 (missing_widget) |
| gen_t3_nav_addtab_fundamentals_aapl | L4 | medium | workspace-repair | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t3_nav_addtab_risk | L4 | hard | workspace-repair | portfolio-risk-review | finance | portfolio-management | FAIL 0.941 (schema_not_called_before_create) |
| gen_t3_note_synthesis_aapl_msft_closes | L0 | medium | workspace-inspection | equity-tearsheet | finance | equity-research | FAIL 0.714 (missing_generated_widget,too_many_invalid_calls) |
| gen_t3_note_synthesis_fed_vs_10y | L0 | hard | workspace-inspection | macro-rates-review | finance | macro | FAIL 0.714 (missing_generated_widget,too_many_invalid_calls) |
| gen_t3_note_synthesis_holdings_beta | L0 | hard | workspace-inspection | portfolio-risk-review | finance | portfolio-management | FAIL 0.714 (missing_generated_widget,too_many_invalid_calls) |
| gen_t3_note_synthesis_nvda_close_eps | L0 | medium | workspace-inspection | equity-tearsheet | finance | equity-research | FAIL 0.714 (missing_generated_widget,too_many_invalid_calls) |
| gen_t3_params_companion_sector_corporate_access_meeting_notes_claims_evidence_and_sign_off_history_3 | L2 | hard | dashboard-construction | compliance-surveillance | finance | compliance | FAIL 0.545 (missing_widget,missing_widget,layout_mismatch) |
| gen_t3_params_companion_sector_sector_exposure_2 | L2 | hard | dashboard-construction | portfolio-risk-review | finance | portfolio-management | FAIL 0.812 (layout_mismatch,layout_mismatch,too_many_invalid_calls) |
| gen_t3_params_companion_series_macro_timeseries_1 | L2 | medium | dashboard-construction | macro-rates-review | finance | macro | FAIL 0.800 (layout_mismatch,too_many_invalid_calls,schema_not_called_before_create) |
| gen_t3_params_companion_symbol_price_performance_0 | L2 | medium | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.733 (layout_mismatch,layout_mismatch,too_many_invalid_calls) |
| gen_t3_prompts_dashboard_aapl_prompt_dashboard | L2 | medium | dashboard-construction | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t3_prompts_dashboard_macro_prompt_dashboard | L2 | medium | dashboard-construction | macro-rates-review | finance | macro | FAIL 0.938 (schema_not_called_before_create) |
| gen_t3_prompts_dashboard_portfolio_prompt_dashboard | L2 | hard | dashboard-construction | portfolio-risk-review | finance | portfolio-management | FAIL 0.941 (too_many_invalid_calls) |
| gen_t3_prompts_dashboard_stark_prompt_dashboard | L2 | hard | dashboard-construction | compliance-surveillance | finance | compliance | FAIL 0.571 (missing_widget,missing_widget,missing_generated_widget) |
| gen_t3_read_client_pair | L1 | hard | data-reading | client-meeting-prep | finance | client-ir | PASS 1.000 |
| gen_t3_read_exec_pair | L1 | medium | data-reading | execution-exception-review | finance | execution | PASS 1.000 |
| gen_t3_read_risk_pair | L1 | medium | data-reading | risk-review | finance | risk | PASS 1.000 |
| gen_t3_read_vendor_pair | L1 | hard | data-reading | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |
| gen_t3_resources_skill_build_finance_comps | L2 | hard | dashboard-construction | portfolio-risk-review | finance | portfolio-management | FAIL 0.909 (too_many_invalid_calls) |
| gen_t3_resources_skill_build_finance_earnings_prep | L2 | medium | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.909 (too_many_invalid_calls) |
| gen_t3_resources_skill_build_finance_guidance_tracker | L2 | hard | dashboard-construction | portfolio-morning-review | finance | portfolio-management | FAIL 0.778 (missing_widget,missing_generated_widget) |
| gen_t3_resources_skill_build_finance_tearsheet | L2 | medium | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.909 (too_many_invalid_calls) |
| gen_t3_skill_finance_comps | L1 | hard | skill-access | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t3_skill_finance_earnings_prep | L1 | medium | skill-access | earnings-prep | finance | equity-research | FAIL 0.917 (too_many_invalid_calls) |
| gen_t3_skill_finance_guidance_tracker | L1 | hard | skill-access | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t3_skill_finance_tearsheet | L1 | medium | skill-access | equity-tearsheet | finance | equity-research | FAIL 0.917 (too_many_invalid_calls) |
| gen_t3_update_repair_news_msft_aapl | L4 | medium | workspace-repair | equity-tearsheet | finance | equity-research | FAIL 0.875 (too_many_invalid_calls) |
| gen_t3_update_repair_risk_fund | L4 | hard | workspace-repair | risk-review | finance | risk | PASS 1.000 |
| gen_t3_update_repair_series_fedfunds_cpi | L4 | hard | workspace-repair | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t3_update_repair_ticker_nvda_msft | L4 | medium | workspace-repair | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t4_app_full_corporate_access_meeting_notes | L3 | hard | app-instantiation | compliance-surveillance | finance | compliance | PASS 1.000 |
| gen_t4_app_full_crypto_research_dashboard | L3 | hard | app-instantiation | equity-tearsheet | finance | equity-research | FAIL 0.111 (dashboard_name,missing_tab,missing_tab) |
| gen_t4_app_full_healthcare_research_dashboard | L3 | hard | app-instantiation | healthcare-catalyst-review | finance | healthcare-research | PASS 1.000 |
| gen_t4_app_full_mnpi_research_review | L3 | hard | app-instantiation | compliance-surveillance | finance | compliance | PASS 1.000 |
| gen_t4_backends_multi_equities_macro | L2 | hard | dashboard-construction | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t4_backends_multi_equities_portfolio | L2 | hard | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.938 (too_many_invalid_calls) |
| gen_t4_backends_multi_portfolio_macro | L2 | hard | dashboard-construction | portfolio-risk-review | finance | portfolio-management | FAIL 0.938 (too_many_invalid_calls) |
| gen_t4_backends_multi_stark_portfolio | L2 | hard | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.500 (missing_widget,missing_widget,missing_generated_widget) |
| gen_t4_create_cross_aapl_rates | L2 | hard | widget-creation | equity-tearsheet | finance | equity-research | FAIL 0.933 (too_many_invalid_calls) |
| gen_t4_create_cross_book_inflation | L2 | hard | widget-creation | macro-rates-review | finance | macro | FAIL 0.857 (too_many_invalid_calls,schema_not_called_before_create) |
| gen_t4_create_cross_msft_exposure | L2 | hard | widget-creation | equity-tearsheet | finance | equity-research | FAIL 0.857 (too_many_invalid_calls,schema_not_called_before_create) |
| gen_t4_create_cross_nvda_curve | L2 | hard | widget-creation | equity-tearsheet | finance | equity-research | FAIL 0.700 (missing_widget,missing_generated_widget,too_many_invalid_calls) |
| gen_t4_delegate_build_earnings_build | L3 | hard | mcp-tool-use | earnings-prep | finance | equity-research | FAIL 0.700 (missing_widget,missing_generated_widget,too_many_invalid_calls) |
| gen_t4_delegate_build_exec_build | L3 | hard | mcp-tool-use | execution-exception-review | finance | execution | FAIL 0.800 (missing_widget,missing_generated_widget) |
| gen_t4_delegate_build_risk_build | L3 | hard | mcp-tool-use | risk-review | finance | risk | FAIL 0.700 (missing_widget,missing_generated_widget,too_many_invalid_calls) |
| gen_t4_delegate_build_vendor_build | L3 | hard | mcp-tool-use | vendor-sla-monitoring | finance | data-platform | FAIL 0.700 (missing_widget,missing_generated_widget,too_many_invalid_calls) |
| gen_t4_delete_then_fix_news_aapl_12 | L4 | hard | workspace-repair | equity-tearsheet | finance | equity-research | FAIL 0.900 (too_many_invalid_calls) |
| gen_t4_delete_then_fix_performance_nvda_18 | L4 | hard | workspace-repair | equity-tearsheet | finance | equity-research | FAIL 0.900 (too_many_invalid_calls) |
| gen_t4_delete_then_fix_status_escalated_48 | L4 | hard | workspace-repair | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |
| gen_t4_delete_then_fix_timeseries_dgs2_17 | L4 | hard | workspace-repair | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t4_inspect_repair_brief_macro_timeseries_1 | L4 | hard | workspace-repair | macro-rates-review | finance | macro | FAIL 0.917 (missing_tool_call) |
| gen_t4_inspect_repair_brief_price_performance_0 | L4 | hard | workspace-repair | equity-tearsheet | finance | equity-research | FAIL 0.917 (missing_tool_call) |
| gen_t4_inspect_repair_brief_reporting_factsheet_studio_factsheets_risk_stats_3 | L4 | hard | workspace-repair | client-meeting-prep | finance | client-ir | FAIL 0.917 (missing_tool_call) |
| gen_t4_inspect_repair_brief_sector_exposure_2 | L4 | hard | workspace-repair | portfolio-risk-review | finance | portfolio-management | FAIL 0.750 (missing_generated_widget,missing_tool_call,too_many_invalid_calls) |
| gen_t4_layout_grid_grid_eq | L1 | hard | layout-management | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t4_layout_grid_grid_eq_mixed | L1 | hard | layout-management | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t4_layout_grid_grid_macro | L1 | hard | layout-management | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t4_layout_grid_grid_portfolio | L1 | hard | layout-management | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t4_nav_hub_book_hub | L2 | hard | workspace-navigation | portfolio-risk-review | finance | portfolio-management | FAIL 0.923 (too_many_invalid_calls) |
| gen_t4_nav_hub_desk_hub | L2 | hard | workspace-navigation | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t4_nav_hub_earnings_hub | L2 | hard | workspace-navigation | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t4_nav_hub_rates_hub | L2 | hard | workspace-navigation | macro-rates-review | finance | macro | FAIL 0.923 (too_many_invalid_calls) |
| gen_t4_note_crossbackend_aapl_vs_rates | L0 | hard | workspace-inspection | portfolio-risk-review | finance | portfolio-management | FAIL 0.750 (missing_generated_widget,too_many_invalid_calls) |
| gen_t4_note_crossbackend_book_vs_fed | L0 | hard | workspace-inspection | portfolio-risk-review | finance | portfolio-management | FAIL 0.714 (missing_generated_widget,too_many_invalid_calls) |
| gen_t4_note_crossbackend_exposure_cpi | L0 | hard | workspace-inspection | portfolio-risk-review | finance | portfolio-management | FAIL 0.750 (missing_generated_widget,too_many_invalid_calls) |
| gen_t4_note_crossbackend_msft_vs_curve | L0 | hard | workspace-inspection | portfolio-risk-review | finance | portfolio-management | FAIL 0.875 (too_many_invalid_calls) |
| gen_t4_params_cross_aapl_macro | L2 | hard | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.769 (missing_widget,missing_generated_widget,too_many_invalid_calls) |
| gen_t4_params_cross_nvda_rates | L2 | hard | dashboard-construction | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t4_params_cross_portfolio_sector | L2 | hard | dashboard-construction | portfolio-risk-review | finance | portfolio-management | FAIL 0.812 (missing_tool_call,missing_tool_call,schema_not_called_before_create) |
| gen_t4_params_cross_stark_sector | L2 | hard | dashboard-construction | equity-tearsheet | finance | equity-research | FAIL 0.143 (missing_widget,missing_widget,missing_generated_widget) |
| gen_t4_prompts_cross_prompt_cross_aapl_rates | L2 | hard | dashboard-construction | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t4_prompts_cross_prompt_cross_book_cpi | L2 | hard | dashboard-construction | portfolio-risk-review | finance | portfolio-management | PASS 1.000 |
| gen_t4_prompts_cross_prompt_cross_nvda_holdings | L2 | hard | dashboard-construction | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t4_prompts_cross_prompt_cross_stark_risk | L2 | hard | dashboard-construction | portfolio-morning-review | finance | portfolio-management | FAIL 0.375 (dashboard_name,missing_widget,missing_widget) |
| gen_t4_read_pm_values | L1 | hard | data-reading | portfolio-morning-review | finance | portfolio-management | FAIL 0.500 (missing_generated_widget,missing_tool_call,missing_tool_result) |
| gen_t4_read_quant_values | L1 | hard | data-reading | risk-review | finance | risk | FAIL 0.889 (missing_generated_widget) |
| gen_t4_read_risk_values | L1 | hard | data-reading | risk-review | finance | risk | FAIL 0.778 (missing_generated_widget,too_many_invalid_calls) |
| gen_t4_read_stress_values | L1 | hard | data-reading | risk-review | finance | risk | FAIL 0.889 (missing_generated_widget) |
| gen_t4_resources_full_client_360 | L2 | hard | dashboard-construction | client-meeting-prep | finance | client-ir | FAIL 0.947 (dashboard_name) |
| gen_t4_resources_full_portfolio_command_center | L2 | hard | dashboard-construction | portfolio-morning-review | finance | portfolio-management | PASS 1.000 |
| gen_t4_resources_full_risk_exposure_monitor | L2 | hard | dashboard-construction | risk-review | finance | risk | FAIL 0.950 (missing_generated_widget) |
| gen_t4_resources_full_vendor_dataset_monitor | L2 | hard | dashboard-construction | vendor-sla-monitoring | finance | data-platform | FAIL 0.947 (dashboard_name) |
| gen_t4_skill_finance_comps | L1 | hard | skill-access | equity-tearsheet | finance | equity-research | FAIL 0.750 (missing_generated_widget,missing_tool_call,too_many_invalid_calls) |
| gen_t4_skill_finance_earnings_prep | L1 | hard | skill-access | earnings-prep | finance | equity-research | FAIL 0.923 (missing_generated_widget) |
| gen_t4_skill_finance_guidance_tracker | L1 | hard | skill-access | equity-tearsheet | finance | equity-research | FAIL 0.846 (missing_generated_widget,too_many_invalid_calls) |
| gen_t4_skill_finance_tearsheet | L1 | hard | skill-access | equity-tearsheet | finance | equity-research | FAIL 0.846 (missing_generated_widget,too_many_invalid_calls) |
| gen_t4_update_double_aapl_desk | L4 | hard | workspace-repair | equity-tearsheet | finance | equity-research | PASS 1.000 |
| gen_t4_update_double_nvda_switch | L4 | hard | workspace-repair | equity-tearsheet | finance | equity-research | FAIL 0.917 (too_many_invalid_calls) |
| gen_t4_update_double_rates_switch | L4 | hard | workspace-repair | macro-rates-review | finance | macro | PASS 1.000 |
| gen_t4_update_double_stark_ops | L4 | hard | workspace-repair | vendor-sla-monitoring | finance | data-platform | PASS 1.000 |

## Common Interpretation

- Missing generated-widget failures often mean the model added no note/chart, added it to the wrong tab, or wrote placeholder text that did not include required task facts.
- Missing-widget and missing-tab failures are common on multi-widget dashboard tasks when the model chooses the wrong widget, tab, or data arguments.
- Invalid-call failures usually mean the model emitted a malformed tool name, used unresolved placeholders, or ignored an ID returned by an earlier observation.
- In batch mode, app-template tasks are especially sensitive to backend IDs because the model cannot read `manage_backends` output before calling `manage_apps`.

Raw outputs are under `runs/comparison/v1-calib-gpt-oss-20b`.
