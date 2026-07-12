"""Compatibility entry point for measured-difficulty proposals."""

from workspace_bench.reports.difficulty import discover_results, main, propose, render_markdown

__all__ = ["discover_results", "main", "propose", "render_markdown"]


if __name__ == "__main__":
    raise SystemExit(main())
