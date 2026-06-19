"""Regression tests for the example comparison runner."""

from __future__ import annotations

import sys
from pathlib import Path


EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"
sys.path.insert(0, str(EXAMPLES_DIR))

from compare_models import (  # noqa: E402
    colorize,
    format_result_cell,
    is_transient_http_status,
    normalize_interactive_args,
    normalize_tool_name,
    parse_interactive_action,
)


def test_parse_interactive_action_unwraps_nested_tool_name() -> None:
    action = parse_interactive_action(
        '{"done": false, "tool": "tool_name", '
        '"args": {"done": false, "tool": "get_widget_schema", '
        '"args": {"origin": "equities", "widget_id": "price_performance"}}}'
    )

    assert action == {
        "done": False,
        "tool": "get_widget_schema",
        "args": {"origin": "equities", "widget_id": "price_performance"},
    }


def test_parse_interactive_action_normalizes_native_ollama_tool_call() -> None:
    action = parse_interactive_action(
        '{"tool_calls": [{"function": {"name": "tool.get_widget_schema", '
        '"arguments": {"origin": "equities", "widget_id": "price_performance"}}}]}'
    )

    assert action == {
        "done": False,
        "tool": "get_widget_schema",
        "args": {"origin": "equities", "widget_id": "price_performance"},
    }


def test_normalize_interactive_args_maps_fixture_origin_slug() -> None:
    assert normalize_interactive_args(
        {"origin": "equities", "widget_id": "price_performance"},
        {"equities": "Bench Equities"},
    ) == {"origin": "Bench Equities", "widget_id": "price_performance"}


def test_colorize_wraps_enabled_status() -> None:
    assert colorize("[PASS]", "green", enabled=True) == "\033[32m[PASS]\033[0m"
    assert colorize("[FAIL]", "red", enabled=False) == "[FAIL]"


def test_normalize_tool_name_accepts_tool_prefix_alias() -> None:
    assert normalize_tool_name("tool_get_widget_schema") == "get_widget_schema"


def test_http_520_is_transient() -> None:
    assert is_transient_http_status(520) is True
    assert is_transient_http_status(400) is False


def test_format_result_cell_aggregates_repeats() -> None:
    cell = format_result_cell(
        [
            {
                "passed": True,
                "score": 1.0,
                "process_failed": False,
                "issues": [],
            },
            {
                "passed": False,
                "score": 0.5,
                "process_failed": True,
                "issues": [{"code": "missing_widget"}],
            },
        ]
    )

    assert cell == "1/2 avg=0.750, proc=1 (missing_widget)"
