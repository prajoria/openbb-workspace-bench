from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

pytest.importorskip("fastmcp")

from fastmcp.server.middleware import MiddlewareContext  # noqa: E402
from mcp.types import CallToolRequestParams  # noqa: E402

from workspace_bench.core.episode import WorkspaceEpisode  # noqa: E402
from workspace_bench.core.runner import find_task  # noqa: E402
from workspace_bench.integrations.harbor.runtime import (  # noqa: E402
    EpisodeMiddleware,
    EpisodeRecorder,
    call_error,
    structured_result,
    tool_result_payload,
)


TASK_REF = (
    "enterprise-apps-default/compliance_surveillance_hub/"
    "compliance_surveillance_hub_p3_x"
)


def _runtime(tmp_path: Path) -> tuple[EpisodeRecorder, EpisodeMiddleware]:
    episode = WorkspaceEpisode(find_task(TASK_REF))
    recorder = EpisodeRecorder(
        episode=episode,
        artifact_path=tmp_path / "episode.json",
        metadata={"qualified_id": episode.task.qualified_id},
    )
    return recorder, EpisodeMiddleware(recorder)


def _context(name: str, args: dict) -> MiddlewareContext:
    return MiddlewareContext(
        message=CallToolRequestParams(name=name, arguments=args),
        method="tools/call",
    )


def test_tool_result_payload_prefers_structured_content() -> None:
    result = structured_result({"ok": True, "command": "example", "data": {"x": 1}})
    assert tool_result_payload(result, "example")["data"] == {"x": 1}


def test_middleware_records_pre_validation_failure(tmp_path: Path) -> None:
    recorder, middleware = _runtime(tmp_path)

    async def fail(_context: object) -> object:
        raise ValueError("bad arguments")

    result = asyncio.run(
        middleware.on_call_tool(_context("get_widget_data", {}), fail)
    )
    payload = tool_result_payload(result, "get_widget_data")
    assert payload["ok"] is False
    assert payload["error"]["code"] == "mcp_call_failed"
    assert len(recorder.trace) == 1
    assert recorder.trace[0].call.args == {}
    saved = json.loads(recorder.artifact_path.read_text(encoding="utf-8"))
    assert saved["trace"][0]["result"]["message"] == "bad arguments"


def test_middleware_rejects_calls_after_final_answer_without_changing_trace(
    tmp_path: Path,
) -> None:
    recorder, middleware = _runtime(tmp_path)

    async def answer(_context: object) -> object:
        return structured_result(
            {
                "ok": True,
                "command": "final_answer",
                "request_id": None,
                "message": "Final answer recorded; the episode is complete.",
                "data": None,
            }
        )

    asyncio.run(
        middleware.on_call_tool(
            _context("final_answer", {"text": "done"}),
            answer,
        )
    )

    async def should_not_run(_context: object) -> object:
        raise AssertionError("terminal call was dispatched")

    rejected = asyncio.run(
        middleware.on_call_tool(
            _context("get_workspace_snapshot", {}),
            should_not_run,
        )
    )
    payload = tool_result_payload(rejected, "get_workspace_snapshot")
    assert payload == call_error(
        "get_workspace_snapshot",
        "episode_completed",
        "A final answer was already submitted; the episode is complete.",
    )
    assert len(recorder.trace) == 1
    assert len(recorder.rejections) == 1

