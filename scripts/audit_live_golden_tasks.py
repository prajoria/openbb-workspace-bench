"""Run deterministic golden tasks through the real Workspace MCP sidecar.

The sidecar is exercised over HTTP/WebSocket while the browser bridge is backed
by the benchmark simulator, so this checks transport and command translation
parity without touching a user's Workspace account.
"""

from __future__ import annotations

import argparse
import asyncio

from workspace_bench.core.runner import find_task
from workspace_bench.workspace.live_mcp import run_workspace_mcp_smoke


DEFAULT_GOLDENS = (
    ("core", "core/create/price_performance_aapl"),
    ("core", "core/layout/arrange_split_macro"),
    ("build-openbb-apps", "build-openbb-apps/types/vol_commentary"),
)


async def audit(url: str, goldens: list[tuple[str, str]]) -> int:
    failed = False
    for suite, task_id in goldens:
        result = await run_workspace_mcp_smoke(
            task=find_task(task_id, suite=suite),
            base_url=url,
            agent="oracle",
            replace_existing_session=True,
            check_surface=True,
        )
        passed = result.run_result.grade.passed and not result.surface_issues
        failed = failed or not passed
        status = "PASS" if passed else "FAIL"
        print(f"{status} {suite}/{task_id}")
        for issue in result.surface_issues:
            print(f"  surface: {issue}")
        for issue in result.run_result.grade.issues:
            print(f"  grade: {issue.code}: {issue.message}")
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8787")
    parser.add_argument(
        "--task",
        action="append",
        metavar="SUITE:TASK_ID",
        help="Override the default golden set; repeat for multiple tasks.",
    )
    args = parser.parse_args()
    goldens = list(DEFAULT_GOLDENS)
    if args.task:
        goldens = []
        for value in args.task:
            suite, separator, task_id = value.partition(":")
            if not separator:
                parser.error("--task must be SUITE:TASK_ID")
            goldens.append((suite, task_id))
    return asyncio.run(audit(args.url, goldens))


if __name__ == "__main__":
    raise SystemExit(main())
