# Core

`workspace_bench.core` is the benchmark source of truth.

It owns the task dataclasses, bundled task loading, episode lifecycle,
deterministic grading, and the baseline runner. Code in this package should not
know about a specific model provider, export format, or training loop.

Use this package when you need to:

- load bundled or private task suites
- run oracle or noop baselines
- step through one Workspace episode
- grade a final snapshot and trace
- inspect task/result dataclasses

Use canonical imports such as `workspace_bench.core.runner` and
`workspace_bench.core.models` from implementation code.
