# `enterprise-apps-default` task suite

Tasks: 69

## Purpose

A pass means the agent can answer every bundled Stark enterprise-app product prompt from the seeded default workspace and leave the required evidence note, graded only on the resulting artifact rather than on a prescribed tool sequence.

## Workspace baseline

The manifest declares `default-v1` because every task depends on the complete default workspace: 23 seeded enterprise apps and their deterministic reference widgets provide the product context and data the verbatim prompts assume.

## Generation method

`product-verbatim-prompts + reviewed-derived-rubrics`. `scripts/generators/generate_apps_default_suite.py` copies prompts byte-for-byte from the Stark app catalog. Widget targets and note anchors are derived from the product definitions and then reviewed through explicit `RUBRIC_OVERRIDES`; grading remains outcomes-only. Difficulty is a placeholder pending empirical measurement.

## Axes

Family is the source enterprise app, with exactly three product prompts per family. Category is uniformly read because tasks synthesize seeded information into an evidence note. All tasks currently carry the medium difficulty placeholder; the suite does not declare a separate specification-level field.

| Axis | File-derived counts |
| --- | --- |
| `family` | 23 families, 3 tasks each: `cio_investment_committee_pack`, `client_360`, `compliance_surveillance_hub`, `corporate_access_meeting_notes`, `crypto_research_dashboard`, `earnings_estimates_monitor`, `equity_research_workbench`, `execution_desk`, `executive_investment_dashboard`, `fund_operations_control_tower`, `healthcare_research_dashboard`, `liquidity_tca_workbench`, `mnpi_research_review`, `nav_fees_close_dashboard`, `portfolio_command_center`, `quant_research_backtest_lab`, `rebalance_scenario_lab`, `reporting_factsheet_studio`, `risk_exposure_monitor`, `strategy_health_monitor`, `stress_liquidity_lab`, `vendor_dataset_monitor`, `workspace_data_control_center` |
| `category` | `read` 69 |
| `difficulty` | `medium` 69 (placeholder) |
| `specification_level` | omitted 69 |

## Gates

This suite uses two grading keys: deterministic grounding verifies the required workspace evidence, and judged answerness verifies that the note consults the competent-analyst data, reflects it with the right analytical mindset, and answers the product prompt. Strict task pass requires both keys. The open-weight judge model and prompt-template hash are pinned and recorded per run; replay uses the cached verdict and never calls a model. CI and `workspace-bench validate --suite enterprise-apps-default` certify the deterministic key only, while judge calibration is a separate local gate.

Generation verifies that every prompt is byte-verbatim from the product catalog, every success contract contains only the required generated-note outcome, reviewed anchor counts stay capped, every reference trace passes, every no-op trace fails, task ids are unique, and all 69 product prompts are represented. Validation rechecks task loading, reference success, and no-op failure against `default-v1`.

## Limitations

Rubric widgets and note anchors are derived from product definitions and reviewed, not product-verbatim ground truth. Fixture data makes results deterministic but does not establish live-data or browser parity. The uniform medium label has not been measured empirically and should not be interpreted as calibrated difficulty.
