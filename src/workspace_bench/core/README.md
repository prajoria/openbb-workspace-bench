# Core

`workspace_bench.core` is the benchmark source of truth.

It owns the scenario dataclasses, bundled task loading, episode lifecycle,
deterministic grading, and the baseline runner. Code in this package should not
know about a specific model provider, export format, or training loop.

Use this package when you need to:

- load bundled or private scenarios
- run oracle or noop baselines
- step through one Workspace episode
- grade a final snapshot and trace
- inspect scenario/result dataclasses

The top-level compatibility modules still work, for example
`workspace_bench.runner` and `workspace_bench.models`.

