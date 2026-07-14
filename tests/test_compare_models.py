"""Regression tests for the model comparison runner."""

from __future__ import annotations

import shlex
import sys
from types import SimpleNamespace
import urllib.error

from workspace_bench.agents.agent_command import build_task_envelope
from workspace_bench.agents.model_adapter_helpers import TOOL_REFERENCE
from workspace_bench.reports.metrics import compute_reliability_metrics
from workspace_bench.reports.model_compare import (
    ModelAdapter,
    TransientModelError,
    benchmark_metadata,
    build_interactive_messages,
    colorize,
    format_result_cell,
    is_transient_http_status,
    load_model_adapters,
    main,
    normalize_interactive_args,
    normalize_tool_name,
    parse_interactive_action,
    post_json,
    process_failure_rows,
    resolve_repo_root,
    run_adapter,
    validate_adapters_for_runner,
)
from workspace_bench.core.runner import find_task
from workspace_bench.workspace.simulated_workspace import SimulatedWorkspace


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


def test_stark_interactive_prompt_uses_display_origin_and_widget_hints() -> None:
    task = find_task("discover_schema_then_options_for_exposure_summary")

    messages = build_interactive_messages(build_task_envelope(task))
    prompt = messages[1]["content"]

    assert '"stark-enterprise": "Bench Stark Enterprise"' in prompt
    assert "client_360_portfolio_view_exposure_summary" in prompt


def test_non_widget_stark_prompt_omits_widget_hints() -> None:
    task = find_task("earnings_single")

    messages = build_interactive_messages(build_task_envelope(task))
    prompt = messages[1]["content"]

    assert '"widget_hints": {}' in prompt


def test_widget_hints_can_be_ablated() -> None:
    task = find_task("discover_schema_then_options_for_exposure_summary")

    messages = build_interactive_messages(build_task_envelope(task), include_widget_hints=False)
    prompt = messages[1]["content"]

    assert '"widget_hints": {}' in prompt

    system = messages[0]["content"]
    assert "Before create_widget" not in system
    assert "origin_hints" not in system


def test_batch_runner_executes_one_real_jsonl_agent_attempt(tmp_path) -> None:
    adapter = ModelAdapter(
        slug="jsonl-rule-agent",
        label="JSONL rule agent",
        command=(
            f"{shlex.quote(sys.executable)} "
            "-m workspace_bench.agents.rule_agent"
        ),
        env={},
        provider="custom",
        model="rule-agent",
    )
    task = find_task("price_performance_aapl")

    runs, metadata = run_adapter(
        adapter,
        [task],
        tmp_path,
        timeout=5,
        episode_timeout=30,
        runner="batch",
        max_turns_override=None,
        repeats=1,
        model_retries=0,
        retry_backoff=0,
        color=False,
    )

    assert metadata["completed_cells"] == 1
    assert len(runs) == 1
    assert runs[0].runner == "batch"
    assert runs[0].exit_code == 0
    assert runs[0].run_result.grade.passed
    assert runs[0].output_path.read_text(encoding="utf-8").strip()


def test_run_metadata_snapshot_records_effective_settings(monkeypatch) -> None:
    from workspace_bench.reports.model_compare import effective_settings, harness_metadata

    monkeypatch.setenv("OPENAI_BASE_URL", "http://127.0.0.1:9/v1")
    args = SimpleNamespace(
        runner="interactive",
        timeout=240.0,
        repeats=1,
        model_retries=2,
        retry_backoff=1.0,
        max_turns=None,
        no_widget_hints=True,
        malformed_retries=0,
    )

    settings = effective_settings(args)
    harness = harness_metadata()

    assert settings["widget_hints"] is False
    assert settings["malformed_retries"] == 0
    assert settings["openai_base_url"] == "http://127.0.0.1:9/v1"
    assert "git_commit" in harness
    assert "git_dirty" in harness


def test_release_run_requires_repeated_attempts(capsys) -> None:
    assert main(["--release-run", "--repeats", "1", "--dry-run"]) == 2
    assert "requires --repeats >= 3" in capsys.readouterr().err


def test_comparison_metadata_uses_core_suite_content_provenance() -> None:
    metadata = benchmark_metadata(SimpleNamespace(task_dir=None, suite="enterprise-apps-usage"))

    assert metadata["suite_id"] == "enterprise-apps-usage"
    assert len(metadata["content_sha256"]) == 64
    assert "git_commit" in metadata


def test_comparison_metadata_records_workspace_baseline_override() -> None:
    metadata = benchmark_metadata(
        SimpleNamespace(
            task_dir=None,
            suite="enterprise-apps-usage",
            workspace_baseline="all-stark-enterprise-apps",
        )
    )

    assert metadata["workspace_baseline"] == "all-stark-enterprise-apps"


def test_colorize_wraps_enabled_status() -> None:
    assert colorize("[PASS]", "green", enabled=True) == "\033[32m[PASS]\033[0m"
    assert colorize("[FAIL]", "red", enabled=False) == "[FAIL]"


def test_normalize_tool_name_accepts_tool_prefix_alias() -> None:
    assert normalize_tool_name("tool_get_widget_schema") == "get_widget_schema"


def test_tool_reference_documents_every_simulator_tool() -> None:
    simulator_tools = {
        name.removeprefix("_tool_") for name in dir(SimulatedWorkspace) if name.startswith("_tool_")
    }

    assert simulator_tools <= set(TOOL_REFERENCE)


def test_http_520_is_transient() -> None:
    assert is_transient_http_status(520) is True
    assert is_transient_http_status(400) is False


def test_transport_errors_are_transient(monkeypatch) -> None:
    def fail(*args, **kwargs):
        raise urllib.error.URLError("connection reset")

    monkeypatch.setattr("urllib.request.urlopen", fail)

    try:
        post_json("https://api.openai.com/v1/chat/completions", {}, timeout=1)
    except TransientModelError as error:
        assert "could not reach model API" in str(error)
    else:
        raise AssertionError("transport failures should be retryable")


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
                        "id": "task_a",
                        "repeat": 2,
                        "process_failed": True,
                        "agent_exit_code": 1,
                        "agent_timed_out": False,
                        "agent_stderr": "provider failed\nretry exhausted",
                    },
                    {
                        "id": "task_b",
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
            "task": "task_a",
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


def test_resolve_repo_root_finds_checkout_from_nested_path() -> None:
    root = resolve_repo_root()

    assert (root / "pyproject.toml").exists()
    assert (root / "src" / "workspace_bench" / "task_suites").exists()


def test_validate_adapters_for_runner_rejects_unsupported_interactive_provider() -> None:
    adapter = ModelAdapter(
        slug="custom-agent",
        label="Custom Agent",
        command="python my_agent.py",
        env={},
        provider="custom",
        model="custom-model",
    )

    error = validate_adapters_for_runner([adapter], runner="interactive")

    assert error is not None
    assert "Interactive runner only supports" in error


def test_validate_adapters_for_runner_requires_batch_command() -> None:
    adapter = ModelAdapter(
        slug="openai-compatible",
        label="OpenAI Compatible",
        command="",
        env={},
        provider="openai",
        model="local-model",
    )

    error = validate_adapters_for_runner([adapter], runner="batch")

    assert (
        error
        == "Batch runner requires command for every adapter; missing command for openai-compatible"
    )
