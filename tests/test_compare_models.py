"""Regression tests for the model comparison runner."""

from __future__ import annotations

from workspace_bench.metrics import compute_reliability_metrics
from workspace_bench.model_compare import (
    colorize,
    format_result_cell,
    is_transient_http_status,
    load_model_adapters,
    normalize_interactive_args,
    normalize_tool_name,
    parse_interactive_action,
    process_failure_rows,
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


def test_compute_reliability_metrics_for_repeated_attempts() -> None:
    metrics = compute_reliability_metrics(
        {
            "always_passes": [True, True, True],
            "sometimes_passes": [False, True, False],
            "never_passes": [False, False, False],
        }
    )

    assert metrics["pass_at_k_count"] == 2
    assert metrics["pass_power_k_count"] == 1
    assert metrics["pass_at_k"] == 2 / 3
    assert metrics["pass_power_k"] == 1 / 3
    assert metrics["reliability_min_k"] == 3
    assert metrics["reliability_max_k"] == 3


def test_process_failure_rows_are_separate_from_task_issues() -> None:
    rows = process_failure_rows(
        [
            {
                "model": {"label": "Model A"},
                "results": [
                    {
                        "id": "scenario_a",
                        "repeat": 2,
                        "process_failed": True,
                        "agent_exit_code": 1,
                        "agent_timed_out": False,
                        "agent_stderr": "provider failed\nretry exhausted",
                    },
                    {
                        "id": "scenario_b",
                        "process_failed": False,
                        "issues": [{"code": "missing_widget"}],
                    },
                ],
            }
        ]
    )

    assert rows == [
        {
            "model": "Model A",
            "scenario": "scenario_a",
            "repeat": 2,
            "exit_code": 1,
            "timed_out": False,
            "stderr_preview": "provider failed retry exhausted",
        }
    ]


def test_load_model_adapters_merges_configured_models(tmp_path) -> None:
    config = tmp_path / "models.json"
    config.write_text(
        """
        {
          "models": [
            {
              "slug": "local-openai-compatible",
              "label": "Local OpenAI Compatible",
              "provider": "openai",
              "model": "local-model",
              "command": "python my_agent.py",
              "env": {
                "OPENAI_BASE_URL": "http://127.0.0.1:8000/v1"
              }
            }
          ]
        }
        """,
        encoding="utf-8",
    )

    adapters, configured_slugs = load_model_adapters(str(config))

    assert "openai-gpt-4.1" in adapters
    assert configured_slugs == ["local-openai-compatible"]
    assert adapters["local-openai-compatible"].model == "local-model"
    assert adapters["local-openai-compatible"].env["OPENAI_BASE_URL"].endswith("/v1")


def test_load_model_adapters_rejects_missing_models_list(tmp_path) -> None:
    config = tmp_path / "models.json"
    config.write_text("{}", encoding="utf-8")

    try:
        load_model_adapters(str(config))
    except ValueError as error:
        assert "non-empty models list" in str(error)
    else:
        raise AssertionError("missing models list should fail")
