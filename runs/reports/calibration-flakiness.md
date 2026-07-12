# Build calibration flakiness triage

Source: guided/current `build-calibration-202607-regraded`, two repeats per task,
restricted to the three complete OpenAI runs. The audit found 29 model-task
flips across 26 tasks. No archived or cold-track result is pooled here.

`max_turns` was not the sole cause of any flexible-specification flip. The
three flexible-budget rungs that flipped completed normally; the new rung
floors therefore address the prior architectural coupling without relabeling
these model-behavior differences as harness failures.

| Task | Model | Disposition |
| --- | --- | --- |
| `advanced/case_qa_omni` | GPT-5.4 mini | Trace-discipline variance: identical outcome score; one repeat skipped required pre-use discovery. |
| `advanced/live_orders_grid` | GPT-5.5 | Exact-contract variance: one repeat omitted one widget-definition field. |
| `advanced/rates_advanced_chart` | GPT-5.4 mini | Trace-discipline variance: identical outcome score; one repeat skipped required pre-use discovery. |
| `advanced/vix_advanced` | GPT-5.4 mini | Trace-discipline variance: identical outcome score; one repeat skipped required pre-use discovery. |
| `aggrid/realized_screen` | GPT-5.5 | Preservation variance: one otherwise complete attempt created an unrelated dashboard. |
| `aggrid/revision_grid` | GPT-5.5 | Implementation variance: one repeat missed capability fields/config and runtime compatibility. |
| `apps/vendor_board` | GPT-5.1 | Implementation variance: one repeat never produced the named app/dashboard and exceeded invalid-call tolerance. |
| `apps/vendor_board` | GPT-5.4 mini | Budget-adjacent but not budget-caused: the capped repeat was already missing the app and both widgets. |
| `apps/vendor_command` | GPT-5.5 | Architecture variance: one repeat omitted required consumed fields; flexible budget was not reached. |
| `apps/vol_morning` | GPT-5.5 | Architecture variance: one repeat omitted required consumed fields; flexible budget was not reached. |
| `charts/chains_highchart_app` | GPT-5.5 | Exact-contract variance: one repeat omitted a widget and app-definition anchors. |
| `charts/pipeline_vegalite` | GPT-5.4 mini | Trace-discipline variance: identical outcome score; one repeat skipped required pre-use discovery. |
| `debug/execution_broken_group` | GPT-5.1 | Genuine repair variance: one repeat left capability, connection, and endpoint defects; budget was not reached. |
| `debug/surveillance_data_mismatch` | GPT-5.1 | Genuine repair variance: one repeat left two required capabilities incomplete. |
| `debug/vendor_wrong_form_endpoint` | GPT-5.1 | Genuine repair variance: one repeat left the form submission and capability contract broken. |
| `extend/add_catalyst_metric` | GPT-5.4 mini | Implementation variance: one repeat did not add the requested widget. |
| `extend/add_catalyst_metric` | GPT-5.5 | Budget-adjacent but not budget-caused: the capped repeat omitted the widget and violated discovery order. |
| `extend/add_curve_spread_metric` | GPT-5.5 | Budget-adjacent but not budget-caused: the capped repeat omitted the widget and violated discovery order. |
| `extend/add_exception_metric` | GPT-5.5 | Trace-discipline variance: both repeats reached the explicit-task cap, but only one obeyed discovery-before-use. |
| `extend/place_curve_spread_metric` | GPT-5.1 | Implementation variance: one repeat missed the dashboard, widgets, backend definition, and app anchors. |
| `extend/place_curve_spread_metric` | GPT-5.4 mini | Exact-contract/trace variance: one repeat missed an app anchor and discovery order. |
| `grouping/chart_note_board` | GPT-5.4 mini | Implementation variance: one repeat omitted widgets and app/group anchors. |
| `grouping/symbol_click_summary_app` | GPT-5.1 | Runtime variance: one repeat published an endpoint-incompatible result. |
| `params/kpi_tabs_table` | GPT-5.4 mini | Process failure: one repeat ended without the backend/widget; excluded from capability-noise conclusions. |
| `params/vendor_sla_table_app` | GPT-5.1 | Architecture variance: one repeat omitted fields and a required parameter kind. |
| `settings/catalyst_metric_app` | GPT-5.1 | Exact-contract variance: one repeat missed the widget and app anchors. |
| `settings/exception_metric` | GPT-5.4 mini | Trace-discipline variance: identical outcome score; one repeat skipped required pre-use discovery. |
| `settings/vol_regime_metric` | GPT-5.5 | Trace-discipline variance: identical outcome score; one repeat skipped required pre-use discovery. |
| `types/vol_commentary` | GPT-5.5 | Trace-discipline variance: identical outcome score; one repeat skipped required pre-use discovery. |

The dispositions separate genuine behavioral variance from one process failure
and from trace-only strict failures. None justifies weakening a business
rubric; intermediate difficulty relabels use the complete repeated evidence.
