# Reports

`workspace_bench.reports` contains comparison, metrics, charting, and analysis
helpers.

It sits after scenario execution. The benchmark produces graded run results;
this package aggregates those results into model summaries, reliability metrics,
Markdown analysis, and chart artifacts.

Use this package when you need to:

- compare multiple model adapters across scenario slices
- run repeated attempts for reliability metrics
- compute pass rate, task pass rate, mean score, pass@k, and pass^k
- generate comparison JSON, Markdown, SVG, and PNG artifacts
- separate task failures from provider/process failures

Module responsibilities:

- `model_compare.py`: interactive/batch comparison runner, model adapter config, charts, and reports.
- `metrics.py`: shared benchmark reliability metrics.

Reports should not change grading semantics. They should summarize results
produced by the core runner, external-agent harness, or interactive comparison
runner.

