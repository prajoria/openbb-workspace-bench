# Reports

`workspace_bench.reports` contains comparison, metrics, charting, and analysis
helpers.

It sits after task execution. The benchmark produces graded run results;
this package aggregates those results into model summaries, reliability metrics,
Markdown analysis, and chart artifacts.

Use this package when you need to:

- compare multiple model adapters across task slices
- run repeated attempts for reliability metrics
- compute strict/state/runtime/browser pass rates, invalid-call and recovery
  rates, median turns, pairwise repeat flip rate, pass@k, and pass^k
- checkpoint task×repeat cells and account for episode time, tokens, and cost
- generate comparison JSON, Markdown, SVG, and PNG artifacts
- separate task failures from provider/process failures

Module responsibilities:

- `model_compare.py`: interactive/batch comparison runner, model adapter config, charts, and reports.
- `metrics.py`: shared calibration, slicing, and reliability metrics.
- `calibration.py`, `suites.py`, `significance.py`, and `difficulty.py`: typed
  analysis compilers behind the compatibility entry points in `scripts/reports/`.
- `oracle_report.py`: manifests, baseline reports, run summaries, and trace artifacts.
- `validation.py`: task metadata and baseline validation.
- `serialization.py`: canonical grade-dimension serialization shared by CLI and
  model-comparison result rows.

Reports should not change grading semantics. They should summarize results
produced by the core runner, external-agent harness, or interactive comparison
runner.
