"""Command line interface for Workspace Bench."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import asdict
from pathlib import Path

from workspace_bench.agents.agent_command import (
    AgentCommandRun,
    run_agent_command,
    write_task_envelope,
)
from workspace_bench.agents import build_agent
from workspace_bench.workspace.fixtures import get_fixture_backend, make_fixture_server
from workspace_bench.core.models import (
    BENCHMARK_NAME,
    BENCHMARK_RELEASE_ID,
    BENCHMARK_VERSION,
    CANARY_GUID,
    JsonDict,
    RunResult,
    Task,
    TaskSuiteManifest,
    VALID_TASK_SPLITS,
)
from workspace_bench.core.runner import (
    BUILTIN_TASK_SUITE_ORDER,
    TaskRunner,
    find_task,
    load_builtin_task_suite_manifest,
    load_builtin_tasks,
    load_task_directory,
    load_task_file,
    load_task_suite_manifest,
)
from workspace_bench.core.suite_checks import release_checks_for_suite


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    # Evaluating IS the tool's function, so it takes no subcommand:
    # `workspace-bench --model openai:gpt-4.1-mini --task <id>` (or
    # --models-file / --suite / any runner flag) routes straight to the
    # interactive runner. Bare `workspace-bench` prints the help below.
    if raw_argv and raw_argv[0].startswith("-") and raw_argv[0] not in ("-h", "--help"):
        from workspace_bench.reports.model_compare import main as compare_models_main

        return compare_models_main(raw_argv)

    parser = argparse.ArgumentParser(prog="workspace-bench")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List bundled tasks.")
    _add_task_collection_args(list_parser)
    _add_task_filters(list_parser)
    list_parser.add_argument("--json", action="store_true", help="Emit JSON.")

    show_parser = subparsers.add_parser("show", help="Show a task JSON summary.")
    show_parser.add_argument("task_id")
    show_parser.add_argument("--task-file", help="Show a task JSON file.")

    validate_parser = subparsers.add_parser(
        "validate", help="Validate task metadata, oracle traces, and noop baseline."
    )
    _add_task_collection_args(validate_parser)
    _add_task_filters(validate_parser)
    validate_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    validate_parser.add_argument(
        "--min-tasks",
        type=int,
        default=1,
        help="Require at least this many tasks after filters.",
    )

    manifest_parser = subparsers.add_parser(
        "manifest", help="Print a benchmark dataset manifest."
    )
    _add_task_collection_args(manifest_parser)
    manifest_parser.add_argument("--json", action="store_true", help="Emit JSON.")

    report_parser = subparsers.add_parser(
        "report", help="Generate a benchmark report from built-in baselines."
    )
    _add_task_collection_args(report_parser)
    report_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    report_parser.add_argument("--output", help="Write report to a file.")



    run_parser = subparsers.add_parser("run", help="Run tasks.")
    run_parser.add_argument("--task", help="Task id. Runs all when omitted.")
    run_parser.add_argument("--task-file", help="Run one task JSON file.")
    _add_task_collection_args(run_parser)
    _add_task_filters(run_parser)
    run_parser.add_argument("--agent", default="oracle", choices=["oracle", "noop"])
    run_parser.add_argument("--json", action="store_true", help="Emit JSON results.")
    run_parser.add_argument(
        "--trace-dir",
        help="Directory where per-task trace JSON artifacts will be written.",
    )

    serve_parser = subparsers.add_parser(
        "serve-fixture", help="Serve a fixture backend over HTTP."
    )
    serve_parser.add_argument("--backend", default="equities")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=9101)

    smoke_parser = subparsers.add_parser(
        "smoke-workspace-mcp",
        help="Run one task through a live workspace-mcp sidecar.",
    )
    smoke_parser.add_argument("--url", default="http://127.0.0.1:8787")
    smoke_parser.add_argument(
        "--suite",
        default="core",
        choices=list(BUILTIN_TASK_SUITE_ORDER),
        help="Bundled task suite used to resolve --task.",
    )
    smoke_parser.add_argument("--task", default="gen_t0_create_price_performance_aapl")
    smoke_parser.add_argument("--agent", default="oracle", choices=["oracle", "noop"])
    smoke_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    smoke_parser.add_argument(
        "--check-surface",
        action="store_true",
        help="Also verify expected Workspace MCP tools, prompts, and resources.",
    )
    smoke_parser.add_argument(
        "--replace-browser-session",
        action="store_true",
        help="Allow the smoke bridge to replace an already connected Workspace browser.",
    )

    export_parser = subparsers.add_parser(
        "export-task", help="Export one public task envelope for an external agent."
    )
    export_parser.add_argument("--task")
    export_parser.add_argument("--task-file", help="Export a task JSON file.")
    export_parser.add_argument("--output", required=True)

    rollout_parser = subparsers.add_parser(
        "export-rollouts", help="Export normalized rollout JSONL."
    )
    _add_rollout_source_args(rollout_parser)
    _add_task_selection_args(rollout_parser)

    sft_parser = subparsers.add_parser(
        "export-sft", help="Export rollout data in an SFT-friendly JSONL format."
    )
    _add_rollout_source_args(sft_parser)
    _add_task_selection_args(sft_parser)
    sft_parser.add_argument(
        "--format",
        choices=["sharegpt", "openai_messages", "tool_call_jsonl"],
        default="openai_messages",
        help="SFT output format.",
    )
    sft_parser.add_argument(
        "--include-failures",
        action="store_true",
        help="Include failed attempts. By default only passing attempts are exported.",
    )

    preference_parser = subparsers.add_parser(
        "export-preferences",
        help="Export chosen/rejected preference pairs from repeated attempts.",
    )
    preference_parser.add_argument("--comparison-dir", required=True)
    preference_parser.add_argument("--output", required=True)
    _add_task_selection_args(preference_parser)

    agent_parser = subparsers.add_parser(
        "run-agent-command",
        help="Run an external command that emits JSONL Workspace tool calls.",
    )
    agent_parser.add_argument("--task", help="Task id. Runs all when omitted.")
    agent_parser.add_argument("--task-file", help="Run one task JSON file.")
    _add_task_collection_args(agent_parser)
    _add_task_filters(agent_parser)
    agent_parser.add_argument("--agent-command", required=True)
    agent_parser.add_argument("--timeout", type=float, default=120)
    agent_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    agent_parser.add_argument("--trace-dir", help="Write per-task traces.")
    agent_parser.add_argument("--run-dir", help="Directory for task/output files.")

    subparsers.add_parser("canary", help="Print the benchmark contamination canary.")

    args = parser.parse_args(raw_argv)

    if args.command == "list":
        return _cmd_list(args)
    if args.command == "show":
        return _cmd_show(args)
    if args.command == "validate":
        return _cmd_validate(args)
    if args.command == "manifest":
        return _cmd_manifest(args)
    if args.command == "report":
        return _cmd_report(args)
    if args.command == "run":
        return _cmd_run(args)
    if args.command == "serve-fixture":
        return _cmd_serve_fixture(args.backend, args.host, args.port)
    if args.command == "smoke-workspace-mcp":
        return _cmd_smoke_workspace_mcp(args)
    if args.command == "export-task":
        return _cmd_export_task(args)
    if args.command == "export-rollouts":
        return _cmd_export_rollouts(args)
    if args.command == "export-sft":
        return _cmd_export_sft(args)
    if args.command == "export-preferences":
        return _cmd_export_preferences(args)
    if args.command == "run-agent-command":
        return _cmd_run_agent_command(args)
    if args.command == "canary":
        print(CANARY_GUID)
        return 0
    parser.error(f"Unknown command {args.command}")
    return 2


def _add_task_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--level", help="Filter by difficulty level, e.g. t2.")
    parser.add_argument("--category", help="Filter by task category, e.g. dashboard.")
    parser.add_argument("--capability", help="Filter by agent/workspace capability.")
    parser.add_argument("--workflow", help="Filter by business or finance workflow.")
    parser.add_argument("--domain", help="Filter by broad domain.")
    parser.add_argument("--subdomain", help="Filter by narrower domain area.")
    parser.add_argument("--difficulty", help="Filter by difficulty.")
    parser.add_argument(
        "--split",
        choices=sorted(VALID_TASK_SPLITS),
        help="Filter by task split.",
    )
    parser.add_argument("--tag", action="append", default=[], help="Require a tag.")


def _add_task_collection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--suite",
        dest="suite",
        default="core",
        choices=list(BUILTIN_TASK_SUITE_ORDER),
        help=(
            "Bundled task suite. core = operating the workspace "
            "(300); build-openbb-apps = building custom backend apps (212); "
            "valid values: core, build-openbb-apps."
        ),
    )
    parser.add_argument(
        "--task-dir",
        help="Directory of task JSON files. Overrides --suite.",
    )


def _add_task_selection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--task", help="Task id. Uses all when omitted.")
    parser.add_argument("--task-file", help="Use one task JSON file.")
    _add_task_collection_args(parser)
    _add_task_filters(parser)


def _add_rollout_source_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--output", required=True)
    parser.add_argument("--comparison-dir", help="Read an evaluator output directory.")
    parser.add_argument("--trace-dir", help="Read trace artifacts from this directory.")
    parser.add_argument(
        "--oracle",
        action="store_true",
        help="Export oracle traces for the selected tasks.",
    )


def _cmd_list(args: argparse.Namespace) -> int:
    tasks = _filtered_tasks(args)
    if args.json:
        print(
            json.dumps(
                [_task_summary(task) for task in tasks],
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    for task in tasks:
        tags = ",".join(task.tags) if task.tags else "-"
        print(
            f"{task.id}\t{task.level}\t{task.difficulty}\t"
            f"{task.split}\t"
            f"{task.capability}\t{task.workflow}\t"
            f"{task.domain}\t{task.subdomain}\t{tags}\t{task.title}"
        )
    return 0


def _cmd_show(args: argparse.Namespace) -> int:
    task = _task_from_file_or_builtin(args.task_id, args.task_file)
    payload = _task_summary(task)
    payload.update(
        {
            "prompt": task.prompt,
            "allowed_tools": task.allowed_tools,
            "limits": task.limits,
            "success": {
                "required_tabs": task.success.required_tabs,
                "required_widget_count": len(task.success.required_widgets),
                "required_generated_widget_count": len(
                    task.success.required_generated_widgets
                ),
                "required_layout_count": len(task.success.required_layouts),
            },
        }
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    tasks = _filtered_tasks(args)
    validation = validate_tasks(
        tasks,
        min_tasks=args.min_tasks,
        release_profile=_release_profile(args),
    )
    if args.json:
        print(json.dumps(validation, indent=2, sort_keys=True))
    else:
        status = "PASS" if validation["passed"] else "FAIL"
        print(
            f"{status}\t{validation['task_count']} tasks\t"
            f"{validation['oracle_passed']}/{validation['task_count']} oracle passed\t"
            f"{validation['noop_failed']}/{validation['task_count']} noop failed"
        )
        for issue in validation["issues"]:
            print(f"  - {issue['task_id']}: {issue['message']}")
    return 0 if validation["passed"] else 1


def _cmd_manifest(args: argparse.Namespace) -> int:
    manifest = build_manifest(_task_collection(args), _task_suite_manifest(args))
    if args.json:
        print(json.dumps(manifest, indent=2, sort_keys=True))
        return 0
    print(f"name\t{manifest['name']}")
    print(f"version\t{manifest['version']}")
    print(f"task_count\t{manifest['task_count']}")
    print(f"levels\t{','.join(manifest['levels'])}")
    print(f"capabilities\t{','.join(manifest['capabilities'])}")
    print(f"workflows\t{','.join(manifest['workflows'])}")
    print(f"domains\t{','.join(manifest['domains'])}")
    print(f"subdomains\t{','.join(manifest['subdomains'])}")
    print(f"difficulties\t{','.join(manifest['difficulties'])}")
    print(f"splits\t{','.join(manifest['splits'])}")
    print(f"canary\t{manifest['canary_guid']}")
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    tasks = _task_collection(args)
    report = build_report(
        tasks,
        _task_suite_manifest(args),
        release_profile=_release_profile(args),
    )
    rendered = (
        json.dumps(report, indent=2, sort_keys=True)
        if args.json
        else _render_markdown_report(report)
    )
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


def build_manifest(
    tasks: list[Task],
    task_suite: TaskSuiteManifest | None = None,
) -> dict:
    """Build a machine-readable dataset manifest."""

    redacted = _task_suite_is_hidden(task_suite)
    payload = {
        "name": BENCHMARK_NAME,
        "version": task_suite.version if task_suite else BENCHMARK_VERSION,
        "release_id": task_suite.release_id if task_suite else BENCHMARK_RELEASE_ID,
        "canary_guid": CANARY_GUID,
        "redacted": redacted,
        "task_count": len(tasks),
        "levels": sorted({task.level for task in tasks}),
        "capabilities": sorted({task.capability for task in tasks}),
        "workflows": sorted({task.workflow for task in tasks}),
        "domains": sorted({task.domain for task in tasks}),
        "subdomains": sorted({task.subdomain for task in tasks}),
        "difficulties": sorted({task.difficulty for task in tasks}),
        "splits": sorted({task.split for task in tasks}),
        "tags": sorted({tag for task in tasks for tag in task.tags}),
        "tasks": [_task_summary(task) for task in tasks],
    }
    if task_suite:
        payload["task_suite"] = {
            "suite_id": task_suite.suite_id,
            "release_id": task_suite.release_id,
            "version": task_suite.version,
            "visibility": task_suite.visibility,
            "default_split": task_suite.default_split,
            "description": task_suite.description,
        }
    return payload


def build_report(
    tasks: list[Task],
    task_suite: TaskSuiteManifest | None = None,
    release_profile: str | None = None,
) -> dict:
    """Run built-in baselines and return a release-style report payload."""

    runner = TaskRunner()
    oracle_results = [runner.run(task, "oracle") for task in tasks]
    noop_results = [runner.run(task, "noop") for task in tasks]
    release_checks = {
        "oracle_all_pass": all(result.grade.passed for result in oracle_results),
        "noop_all_fail": all(not result.grade.passed for result in noop_results),
    }
    release_checks.update(
        release_checks_for_suite(release_profile, tasks, oracle_results)
    )
    return {
        "manifest": build_manifest(tasks, task_suite),
        "baselines": {
            "oracle": _results_summary(oracle_results),
            "noop": _results_summary(noop_results),
        },
        "oracle_results": [_result_summary(result) for result in oracle_results],
        "noop_results": [_result_summary(result) for result in noop_results],
        "release_checks": release_checks,
    }


def _cmd_run(args: argparse.Namespace) -> int:
    tasks = _selected_tasks(args)
    agent = build_agent(args.agent)
    runner = TaskRunner()
    results = [runner.run(task, agent) for task in tasks]
    if args.trace_dir:
        _write_trace_artifacts(
            Path(args.trace_dir),
            results,
            redact_prompts=_should_redact_task_suite(args),
        )

    if args.json:
        print(
            json.dumps(
                {
                    "summary": _results_summary(results),
                    "results": [_result_summary(result) for result in results],
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        for result in results:
            status = "PASS" if result.grade.passed else "FAIL"
            print(
                f"{status}\t{result.task.id}\t"
                f"{result.grade.score:.2f}\t"
                f"{result.grade.checks_passed}/{result.grade.checks_total}"
            )
            for issue in result.grade.issues:
                print(f"  - {issue.code}: {issue.message}")
        summary = _results_summary(results)
        print(
            f"SUMMARY\t{summary['passed']}/{summary['total']} passed\t"
            f"mean_score={summary['mean_score']:.3f}"
        )

    return 0 if all(result.grade.passed for result in results) else 1


def _cmd_export_task(args: argparse.Namespace) -> int:
    if args.task_file and not args.task:
        task = load_task_file(Path(args.task_file))
        write_task_envelope(Path(args.output), task)
        print(f"Wrote task envelope for {task.id} to {args.output}")
        return 0
    task_id = args.task or "gen_t0_create_price_performance_aapl"
    task = _task_from_file_or_builtin(task_id, args.task_file)
    write_task_envelope(Path(args.output), task)
    print(f"Wrote task envelope for {task.id} to {args.output}")
    return 0


def _cmd_export_rollouts(args: argparse.Namespace) -> int:
    from workspace_bench.exports import write_rollouts_jsonl

    records = _load_export_rollouts(args)
    count = write_rollouts_jsonl(records, Path(args.output))
    print(f"Wrote {count} rollout record(s) to {args.output}")
    return 0


def _cmd_export_sft(args: argparse.Namespace) -> int:
    from workspace_bench.exports import write_sft_jsonl

    records = _load_export_rollouts(args)
    count = write_sft_jsonl(
        records,
        Path(args.output),
        fmt=args.format,
        include_failures=args.include_failures,
    )
    print(f"Wrote {count} SFT record(s) to {args.output}")
    return 0


def _cmd_export_preferences(args: argparse.Namespace) -> int:
    from workspace_bench.exports import write_preferences_jsonl

    records = _load_export_rollouts(args)
    count = write_preferences_jsonl(records, Path(args.output))
    print(f"Wrote {count} preference pair(s) to {args.output}")
    return 0


def _cmd_run_agent_command(args: argparse.Namespace) -> int:
    tasks = _selected_tasks(args)
    base_run_dir = Path(args.run_dir) if args.run_dir else None
    runs: list[AgentCommandRun] = []
    for task in tasks:
        task_run_dir = base_run_dir / task.id if base_run_dir else None
        runs.append(
            run_agent_command(
                task=task,
                command=args.agent_command,
                timeout_seconds=args.timeout,
                run_dir=task_run_dir,
            )
        )
    results = [run.run_result for run in runs]
    if args.trace_dir:
        _write_trace_artifacts(
            Path(args.trace_dir),
            results,
            redact_prompts=_should_redact_task_suite(args),
        )

    if args.json:
        print(
            json.dumps(
                {
                    "benchmark": {
                        "name": BENCHMARK_NAME,
                        "version": BENCHMARK_VERSION,
                        "release_id": BENCHMARK_RELEASE_ID,
                    },
                    "summary": _agent_runs_summary(runs),
                    "results": [_agent_run_summary(run) for run in runs],
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        for run in runs:
            passed = _agent_run_passed(run)
            status = "PASS" if passed else "FAIL"
            result = run.run_result
            print(
                f"{status}\t{result.task.id}\t"
                f"{result.grade.score:.2f}\t"
                f"{result.grade.checks_passed}/{result.grade.checks_total}\t"
                f"exit={run.exit_code}\ttimeout={run.timed_out}"
            )
            for issue in result.grade.issues:
                print(f"  - {issue.code}: {issue.message}")
        summary = _agent_runs_summary(runs)
        print(
            f"SUMMARY\t{summary['passed']}/{summary['total']} passed\t"
            f"mean_score={summary['mean_score']:.3f}"
        )
    return 0 if all(_agent_run_passed(run) for run in runs) else 1


def _cmd_smoke_workspace_mcp(args: argparse.Namespace) -> int:
    from workspace_bench.workspace.live_mcp import run_workspace_mcp_smoke

    task = find_task(args.task, suite=args.suite)
    try:
        result = asyncio.run(
            run_workspace_mcp_smoke(
                task=task,
                base_url=args.url,
                agent=args.agent,
                replace_existing_session=args.replace_browser_session,
                check_surface=args.check_surface,
            )
        )
    except RuntimeError as error:
        print(f"ERROR\t{error}", file=sys.stderr)
        return 2

    run_result = result.run_result
    if args.json:
        print(
            json.dumps(
                {
                    "result": _result_summary(run_result),
                    "mcp_tool_count": len(result.mcp_tools),
                    "mcp_tools": result.mcp_tools,
                    "mcp_prompts": result.mcp_prompts,
                    "mcp_resources": result.mcp_resources,
                    "surface_issues": result.surface_issues,
                    "bridge_commands": result.bridge_commands,
                    "health_before": result.health_before,
                    "health_with_bridge": result.health_with_bridge,
                    "health_after": result.health_after,
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        status = "PASS" if run_result.grade.passed else "FAIL"
        print(
            f"{status}\t{run_result.task.id}\t"
            f"{run_result.grade.score:.2f}\t"
            f"{run_result.grade.checks_passed}/{run_result.grade.checks_total}"
        )
        print(f"MCP_TOOLS\t{len(result.mcp_tools)}")
        print(f"MCP_PROMPTS\t{len(result.mcp_prompts)}")
        print(f"MCP_RESOURCES\t{len(result.mcp_resources)}")
        for surface_issue in result.surface_issues:
            print(f"  - surface: {surface_issue}")
        print(f"BRIDGE_COMMANDS\t{','.join(result.bridge_commands)}")
        print(
            "HEALTH\t"
            f"before_browser={result.health_before.get('browser_connected')}\t"
            f"during_browser={result.health_with_bridge.get('browser_connected')}\t"
            f"after_browser={result.health_after.get('browser_connected')}"
        )
        for issue in run_result.grade.issues:
            print(f"  - {issue.code}: {issue.message}")

    return 0 if run_result.grade.passed and not result.surface_issues else 1


def _render_markdown_report(report: dict) -> str:
    manifest = report["manifest"]
    oracle = report["baselines"]["oracle"]
    noop = report["baselines"]["noop"]
    checks = report["release_checks"]
    lines = [
        "# OpenBB Workspace Bench Report",
        "",
        f"Version: `{manifest['version']}`",
        f"Release: `{manifest['release_id']}`",
        f"Tasks: `{manifest['task_count']}`",
        f"Canary: `{manifest['canary_guid']}`",
        f"Redacted: `{manifest.get('redacted', False)}`",
        "",
        "## Coverage",
        "",
        f"- Levels: {', '.join(manifest['levels'])}",
        f"- Capabilities: {', '.join(manifest['capabilities'])}",
        f"- Workflows: {', '.join(manifest['workflows'])}",
        f"- Domains: {', '.join(manifest['domains'])}",
        f"- Subdomains: {', '.join(manifest['subdomains'])}",
        f"- Difficulties: {', '.join(manifest['difficulties'])}",
        f"- Splits: {', '.join(manifest['splits'])}",
        f"- Tags: {', '.join(manifest['tags'])}",
        "",
        "## Baselines",
        "",
        "| Baseline | Passed | Total | Mean Score |",
        "| --- | ---: | ---: | ---: |",
        (
            f"| oracle | {oracle['passed']} | {oracle['total']} | "
            f"{oracle['mean_score']:.3f} |"
        ),
        (
            f"| noop | {noop['passed']} | {noop['total']} | "
            f"{noop['mean_score']:.3f} |"
        ),
        "",
        "## Release Checks",
        "",
    ]
    for check_name, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        lines.append(f"- {status}: `{check_name}`")
    lines.extend(
        [
            "",
            "## Task Results",
            "",
            "| Task | Split | Level | Capability | Workflow | Domain | Subdomain | Difficulty | Oracle | Noop |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: |",
        ]
    )
    noop_by_id = {result["id"]: result for result in report["noop_results"]}
    for oracle_result in report["oracle_results"]:
        noop_result = noop_by_id[oracle_result["id"]]
        lines.append(
            "| "
            f"{oracle_result['id']} | "
            f"{oracle_result['split']} | "
            f"{oracle_result['level']} | "
            f"{oracle_result['capability']} | "
            f"{oracle_result['workflow']} | "
            f"{oracle_result['domain']} | "
            f"{oracle_result['subdomain']} | "
            f"{oracle_result['difficulty']} | "
            f"{oracle_result['score']:.3f} | "
            f"{noop_result['score']:.3f} |"
        )
    return "\n".join(lines)


def validate_tasks(
    tasks: list[Task],
    min_tasks: int = 1,
    release_profile: str | None = None,
) -> dict:
    """Validate task loadability, metadata, oracle pass, and noop failure.

    ``release_profile`` names a bundled suite whose coverage quotas should
    also be enforced; private task directories pass ``None`` and are only
    held to the universal gates.
    """

    runner = TaskRunner()
    oracle_results = [runner.run(task, "oracle") for task in tasks]
    noop_results = [runner.run(task, "noop") for task in tasks]
    issues = []
    seen_ids: set[str] = set()
    duplicate_ids: set[str] = set()
    for task in tasks:
        if task.id in seen_ids:
            duplicate_ids.add(task.id)
        seen_ids.add(task.id)
    for task_id in sorted(duplicate_ids):
        issues.append(
            {
                "task_id": task_id,
                "message": "task id must be unique within the selected suite",
            }
        )
    if len(tasks) < min_tasks:
        issues.append(
            {
                "task_id": "benchmark",
                "message": (
                    f"expected at least {min_tasks} task(s), "
                    f"found {len(tasks)}"
                ),
            }
        )
    release_checks = release_checks_for_suite(release_profile, tasks, oracle_results)
    for check_name, passed in release_checks.items():
        if not passed:
            issues.append(
                {
                    "task_id": "benchmark",
                    "message": f"release check failed: {check_name}",
                }
            )
    for task, oracle_result, noop_result in zip(
        tasks, oracle_results, noop_results
    ):
        for message in _task_metadata_issues(task):
            issues.append({"task_id": task.id, "message": message})
        if not oracle_result.grade.passed:
            issues.append(
                {
                    "task_id": task.id,
                    "message": "oracle trace does not pass task grader",
                }
            )
        if noop_result.grade.passed:
            issues.append(
                {
                    "task_id": task.id,
                    "message": "noop baseline passed; task is too weak",
                }
            )
    return {
        "passed": not issues,
        "task_count": len(tasks),
        "oracle_passed": sum(result.grade.passed for result in oracle_results),
        "noop_failed": sum(not result.grade.passed for result in noop_results),
        "release_checks": release_checks,
        "issues": issues,
    }


def _release_profile(args: argparse.Namespace) -> str | None:
    """Resolve which bundled suite's release quotas apply, if any.

    Quotas hold for a full bundled suite only: a private ``--task-dir`` suite
    or a filtered slice is validated for the universal gates alone.
    """

    if getattr(args, "task_dir", None):
        return None
    if _filters_active(args):
        return None
    return getattr(args, "suite", "core")


def _filters_active(args: argparse.Namespace) -> bool:
    return any(
        [
            getattr(args, "level", None),
            getattr(args, "category", None),
            getattr(args, "capability", None),
            getattr(args, "workflow", None),
            getattr(args, "domain", None),
            getattr(args, "subdomain", None),
            getattr(args, "difficulty", None),
            getattr(args, "split", None),
            getattr(args, "tag", []),
        ]
    )


def _task_metadata_issues(task: Task) -> list[str]:
    issues = []
    if task.difficulty not in {"easy", "medium", "hard"}:
        issues.append("difficulty must be one of easy, medium, hard")
    if task.split not in VALID_TASK_SPLITS:
        issues.append(
            f"split must be one of {', '.join(sorted(VALID_TASK_SPLITS))}"
        )
    if not task.capability:
        issues.append("capability must be non-empty")
    if not task.workflow:
        issues.append("workflow must be non-empty")
    if not task.domain:
        issues.append("domain must be non-empty")
    if not task.subdomain:
        issues.append("subdomain must be non-empty")
    if not task.tags:
        issues.append("at least one tag is required")
    if not task.oracle_tool_calls:
        issues.append("oracle_tool_calls must be non-empty")
    if not task.allowed_tools:
        issues.append("allowed_tools must be non-empty")
    return issues


def _filtered_tasks(args: argparse.Namespace) -> list[Task]:
    tasks = _task_collection(args)
    if getattr(args, "level", None):
        tasks = [
            task for task in tasks if task.level == args.level
        ]
    if getattr(args, "category", None):
        tasks = [
            task for task in tasks if task.category == args.category
        ]
    if getattr(args, "capability", None):
        tasks = [
            task for task in tasks if task.capability == args.capability
        ]
    if getattr(args, "workflow", None):
        tasks = [
            task for task in tasks if task.workflow == args.workflow
        ]
    if getattr(args, "domain", None):
        tasks = [task for task in tasks if task.domain == args.domain]
    if getattr(args, "subdomain", None):
        tasks = [
            task for task in tasks if task.subdomain == args.subdomain
        ]
    if getattr(args, "difficulty", None):
        tasks = [
            task
            for task in tasks
            if task.difficulty == args.difficulty
        ]
    if getattr(args, "split", None):
        tasks = [task for task in tasks if task.split == args.split]
    for tag in getattr(args, "tag", []) or []:
        tasks = [task for task in tasks if tag in task.tags]
    return tasks


def _selected_tasks(args: argparse.Namespace) -> list[Task]:
    if getattr(args, "task_file", None):
        return [load_task_file(Path(args.task_file))]
    tasks = _filtered_tasks(args)
    task_id = getattr(args, "task", None)
    if task_id:
        tasks = [task for task in tasks if task.id == task_id]
        if (
            not tasks
            and not getattr(args, "task_dir", None)
            and getattr(args, "suite", "core") == "core"
        ):
            # A task id should just work without naming the suite (mirrors
            # the evaluator): fall back to searching every bundled suite.
            return [find_task(task_id)]
        if not tasks:
            raise KeyError(f"Unknown task {task_id!r}")
    return tasks


def _load_export_rollouts(args: argparse.Namespace):
    from workspace_bench.exports import annotate_rollouts
    from workspace_bench.exports import (
        load_comparison_rollouts,
        load_trace_dir_rollouts,
        rollouts_from_oracle,
    )

    source_count = sum(
        [
            bool(getattr(args, "comparison_dir", None)),
            bool(getattr(args, "trace_dir", None)),
            bool(getattr(args, "oracle", False)),
        ]
    )
    if source_count != 1:
        raise SystemExit(
            "Choose exactly one rollout source: --oracle, --comparison-dir, or --trace-dir"
        )

    tasks = _selected_tasks(args)
    if getattr(args, "oracle", False):
        records = rollouts_from_oracle(tasks)
        return annotate_rollouts(records, task_suite=_task_suite_manifest(args))
    if getattr(args, "comparison_dir", None):
        records = load_comparison_rollouts(Path(args.comparison_dir), tasks)
        return annotate_rollouts(records, task_suite=_task_suite_manifest(args))
    records = load_trace_dir_rollouts(Path(args.trace_dir), tasks)
    return annotate_rollouts(records, task_suite=_task_suite_manifest(args))


def _task_collection(args: argparse.Namespace) -> list[Task]:
    task_dir = getattr(args, "task_dir", None)
    if not task_dir:
        return load_builtin_tasks(getattr(args, "suite", "core"))
    return load_task_directory(Path(task_dir))


def _task_suite_manifest(args: argparse.Namespace) -> TaskSuiteManifest | None:
    task_dir = getattr(args, "task_dir", None)
    if not task_dir:
        return load_builtin_task_suite_manifest(getattr(args, "suite", "core"))
    return load_task_suite_manifest(Path(task_dir))


def _should_redact_task_suite(args: argparse.Namespace) -> bool:
    return _task_suite_is_hidden(_task_suite_manifest(args))


def _task_suite_is_hidden(task_suite: TaskSuiteManifest | None) -> bool:
    return task_suite is not None and task_suite.visibility == "hidden"


def _task_from_file_or_builtin(
    task_id: str, task_file: str | None
) -> Task:
    if task_file:
        task = load_task_file(Path(task_file))
        if task_id and task.id != task_id:
            raise ValueError(
                f"task file contains {task.id!r}, not requested {task_id!r}"
            )
        return task
    return find_task(task_id)


def _task_summary(task: Task) -> dict:
    return {
        "id": task.id,
        "title": task.title,
        "level": task.level,
        "capability": task.capability,
        "workflow": task.workflow,
        "domain": task.domain,
        "subdomain": task.subdomain,
        "difficulty": task.difficulty,
        "split": task.split,
        "tags": task.tags,
        "source": task.source,
        "novelty": task.novelty,
        "fixtures": [backend.name for backend in task.fixtures],
        "oracle_tool_call_count": len(task.oracle_tool_calls),
    }


def _result_summary(result: RunResult) -> dict:
    return {
        "id": result.task.id,
        "category": result.task.category,
        "level": result.task.level,
        "capability": result.task.capability,
        "workflow": result.task.workflow,
        "domain": result.task.domain,
        "subdomain": result.task.subdomain,
        "difficulty": result.task.difficulty,
        "split": result.task.split,
        "tags": result.task.tags,
        "novelty": result.task.novelty,
        "score": result.grade.score,
        "passed": result.grade.passed,
        "checks_passed": result.grade.checks_passed,
        "checks_total": result.grade.checks_total,
        "issues": [
            {"code": issue.code, "message": issue.message}
            for issue in result.grade.issues
        ],
    }


def _results_summary(results: list[RunResult]) -> dict:
    total = len(results)
    passed = sum(result.grade.passed for result in results)
    mean_score = (
        sum(result.grade.score for result in results) / total if total else 0.0
    )
    by_level: dict[str, dict[str, int]] = {}
    for result in results:
        bucket = by_level.setdefault(result.task.level, {"passed": 0, "total": 0})
        bucket["total"] += 1
        if result.grade.passed:
            bucket["passed"] += 1
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "mean_score": mean_score,
        "by_level": by_level,
    }


def _agent_run_passed(run: AgentCommandRun) -> bool:
    return run.run_result.grade.passed and run.exit_code == 0 and not run.timed_out


def _agent_run_summary(run: AgentCommandRun) -> dict:
    payload = _result_summary(run.run_result)
    payload.update(
        {
            "passed": _agent_run_passed(run),
            "grade_passed": run.run_result.grade.passed,
            "agent_command": run.command,
            "agent_exit_code": run.exit_code,
            "agent_timed_out": run.timed_out,
            "agent_stdout": run.stdout,
            "agent_stderr": run.stderr,
            "run_dir": str(run.run_dir),
            "task_path": str(run.task_path),
            "output_path": str(run.output_path),
        }
    )
    return payload


def _agent_runs_summary(runs: list[AgentCommandRun]) -> dict:
    results = [run.run_result for run in runs]
    summary = _results_summary(results)
    summary["passed"] = sum(_agent_run_passed(run) for run in runs)
    summary["failed"] = len(runs) - summary["passed"]
    summary["process_failures"] = sum(
        run.exit_code != 0 or run.timed_out for run in runs
    )
    return summary


def _write_trace_artifacts(
    trace_dir: Path,
    results: list[RunResult],
    *,
    redact_prompts: bool = False,
) -> None:
    trace_dir.mkdir(parents=True, exist_ok=True)
    for result in results:
        task_payload: JsonDict = {
            "id": result.task.id,
            "title": result.task.title,
            "level": result.task.level,
            "capability": result.task.capability,
            "workflow": result.task.workflow,
            "domain": result.task.domain,
            "subdomain": result.task.subdomain,
            "difficulty": result.task.difficulty,
            "split": result.task.split,
            "tags": result.task.tags,
            "novelty": result.task.novelty,
        }
        if redact_prompts:
            task_payload["prompt_redacted"] = True
        else:
            task_payload["prompt"] = result.task.prompt
        payload = {
            "task": task_payload,
            "grade": asdict(result.grade),
            "trace": [
                {
                    "index": event.index,
                    "tool": event.call.name,
                    "args": event.call.args,
                    "ok": event.ok,
                    "result": event.result,
                }
                for event in result.trace
            ],
            "final_snapshot": result.final_snapshot,
        }
        output_path = trace_dir / f"{result.task.id}.json"
        output_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )


def _cmd_serve_fixture(backend_name: str, host: str, port: int) -> int:
    backend = get_fixture_backend(backend_name)
    server = make_fixture_server(backend, host=host, port=port)
    print(f"Serving {backend.name} at http://{host}:{port}")
    print(f"  widgets: http://{host}:{port}/widgets.json")
    print(f"  apps:    http://{host}:{port}/apps.json")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping fixture backend.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
