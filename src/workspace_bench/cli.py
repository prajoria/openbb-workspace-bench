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
    RunResult,
    Scenario,
    TaskPackManifest,
    VALID_SCENARIO_SPLITS,
)
from workspace_bench.core.runner import (
    BUILTIN_SCENARIO_PACKS,
    BUILTIN_SCENARIO_PACK_ORDER,
    ScenarioRunner,
    find_scenario,
    load_builtin_task_pack_manifest,
    load_builtin_scenarios,
    load_scenario_directory,
    load_scenario_file,
    load_task_pack_manifest,
)


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    if raw_argv[:1] == ["compare-models"]:
        from workspace_bench.reports.model_compare import main as compare_models_main

        return compare_models_main(raw_argv[1:])

    parser = argparse.ArgumentParser(prog="workspace-bench")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List bundled scenarios.")
    _add_scenario_collection_args(list_parser)
    _add_scenario_filters(list_parser)
    list_parser.add_argument("--json", action="store_true", help="Emit JSON.")

    show_parser = subparsers.add_parser("show", help="Show a scenario JSON summary.")
    show_parser.add_argument("scenario_id")
    show_parser.add_argument("--scenario-file", help="Show a scenario JSON file.")

    validate_parser = subparsers.add_parser(
        "validate", help="Validate scenario metadata, oracle traces, and noop baseline."
    )
    _add_scenario_collection_args(validate_parser)
    _add_scenario_filters(validate_parser)
    validate_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    validate_parser.add_argument(
        "--min-scenarios",
        type=int,
        default=1,
        help="Require at least this many scenarios after filters.",
    )

    manifest_parser = subparsers.add_parser(
        "manifest", help="Print a benchmark dataset manifest."
    )
    _add_scenario_collection_args(manifest_parser)
    manifest_parser.add_argument("--json", action="store_true", help="Emit JSON.")

    report_parser = subparsers.add_parser(
        "report", help="Generate a benchmark report from built-in baselines."
    )
    _add_scenario_collection_args(report_parser)
    report_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    report_parser.add_argument("--output", help="Write report to a file.")

    subparsers.add_parser(
        "compare-models",
        help="Compare local model adapters with the interactive benchmark runner.",
    )

    run_parser = subparsers.add_parser("run", help="Run scenarios.")
    run_parser.add_argument("--scenario", help="Scenario id. Runs all when omitted.")
    run_parser.add_argument("--scenario-file", help="Run one scenario JSON file.")
    _add_scenario_collection_args(run_parser)
    _add_scenario_filters(run_parser)
    run_parser.add_argument("--agent", default="oracle", choices=["oracle", "noop"])
    run_parser.add_argument("--json", action="store_true", help="Emit JSON results.")
    run_parser.add_argument(
        "--trace-dir",
        help="Directory where per-scenario trace JSON artifacts will be written.",
    )

    serve_parser = subparsers.add_parser(
        "serve-fixture", help="Serve a fixture backend over HTTP."
    )
    serve_parser.add_argument("--backend", default="equities")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=9101)

    smoke_parser = subparsers.add_parser(
        "smoke-workspace-mcp",
        help="Run one scenario through a live workspace-mcp sidecar.",
    )
    smoke_parser.add_argument("--url", default="http://127.0.0.1:8787")
    smoke_parser.add_argument(
        "--pack",
        default="core",
        choices=["all", *BUILTIN_SCENARIO_PACK_ORDER],
        help="Bundled scenario pack used to resolve --scenario.",
    )
    smoke_parser.add_argument("--scenario", default="l1_add_price_widget")
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
    export_parser.add_argument("--scenario")
    export_parser.add_argument("--scenario-file", help="Export a scenario JSON file.")
    export_parser.add_argument("--output", required=True)

    rollout_parser = subparsers.add_parser(
        "export-rollouts", help="Export normalized rollout JSONL."
    )
    _add_rollout_source_args(rollout_parser)
    _add_scenario_selection_args(rollout_parser)

    sft_parser = subparsers.add_parser(
        "export-sft", help="Export rollout data in an SFT-friendly JSONL format."
    )
    _add_rollout_source_args(sft_parser)
    _add_scenario_selection_args(sft_parser)
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
    _add_scenario_selection_args(preference_parser)

    agent_parser = subparsers.add_parser(
        "run-agent-command",
        help="Run an external command that emits JSONL Workspace tool calls.",
    )
    agent_parser.add_argument("--scenario", help="Scenario id. Runs all when omitted.")
    agent_parser.add_argument("--scenario-file", help="Run one scenario JSON file.")
    _add_scenario_collection_args(agent_parser)
    _add_scenario_filters(agent_parser)
    agent_parser.add_argument("--agent-command", required=True)
    agent_parser.add_argument("--timeout", type=float, default=120)
    agent_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    agent_parser.add_argument("--trace-dir", help="Write per-scenario traces.")
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


def _add_scenario_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--level", help="Filter by level, e.g. L2.")
    parser.add_argument("--capability", help="Filter by agent/workspace capability.")
    parser.add_argument("--workflow", help="Filter by business or finance workflow.")
    parser.add_argument("--domain", help="Filter by broad domain.")
    parser.add_argument("--subdomain", help="Filter by narrower domain area.")
    parser.add_argument("--difficulty", help="Filter by difficulty.")
    parser.add_argument(
        "--split",
        choices=sorted(VALID_SCENARIO_SPLITS),
        help="Filter by scenario split.",
    )
    parser.add_argument("--tag", action="append", default=[], help="Require a tag.")


def _add_scenario_collection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--pack",
        default="core",
        choices=["all", *BUILTIN_SCENARIO_PACK_ORDER],
        help=(
            "Bundled scenario pack. Defaults to core. Use all to run every "
            "bundled pack."
        ),
    )
    parser.add_argument(
        "--scenario-dir",
        help="Directory of scenario JSON files. Overrides --pack.",
    )


def _add_scenario_selection_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--scenario", help="Scenario id. Uses all when omitted.")
    parser.add_argument("--scenario-file", help="Use one scenario JSON file.")
    _add_scenario_collection_args(parser)
    _add_scenario_filters(parser)


def _add_rollout_source_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--output", required=True)
    parser.add_argument("--comparison-dir", help="Read a compare-models output directory.")
    parser.add_argument("--trace-dir", help="Read trace artifacts from this directory.")
    parser.add_argument(
        "--oracle",
        action="store_true",
        help="Export oracle traces for the selected scenarios.",
    )


def _cmd_list(args: argparse.Namespace) -> int:
    scenarios = _filtered_scenarios(args)
    if args.json:
        print(
            json.dumps(
                [_scenario_summary(scenario) for scenario in scenarios],
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    for scenario in scenarios:
        tags = ",".join(scenario.tags) if scenario.tags else "-"
        print(
            f"{scenario.id}\t{scenario.level}\t{scenario.difficulty}\t"
            f"{scenario.split}\t"
            f"{scenario.capability}\t{scenario.workflow}\t"
            f"{scenario.domain}\t{scenario.subdomain}\t{tags}\t{scenario.title}"
        )
    return 0


def _cmd_show(args: argparse.Namespace) -> int:
    scenario = _scenario_from_file_or_builtin(args.scenario_id, args.scenario_file)
    payload = _scenario_summary(scenario)
    payload.update(
        {
            "prompt": scenario.prompt,
            "allowed_tools": scenario.allowed_tools,
            "limits": scenario.limits,
            "success": {
                "required_tabs": scenario.success.required_tabs,
                "required_widget_count": len(scenario.success.required_widgets),
                "required_generated_widget_count": len(
                    scenario.success.required_generated_widgets
                ),
                "required_layout_count": len(scenario.success.required_layouts),
            },
        }
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    scenarios = _filtered_scenarios(args)
    validation = validate_scenarios(scenarios, min_scenarios=args.min_scenarios)
    if args.json:
        print(json.dumps(validation, indent=2, sort_keys=True))
    else:
        status = "PASS" if validation["passed"] else "FAIL"
        print(
            f"{status}\t{validation['scenario_count']} scenarios\t"
            f"{validation['oracle_passed']}/{validation['scenario_count']} oracle passed\t"
            f"{validation['noop_failed']}/{validation['scenario_count']} noop failed"
        )
        for issue in validation["issues"]:
            print(f"  - {issue['scenario_id']}: {issue['message']}")
    return 0 if validation["passed"] else 1


def _cmd_manifest(args: argparse.Namespace) -> int:
    manifest = build_manifest(_scenario_collection(args), _task_pack_manifest(args))
    if args.json:
        print(json.dumps(manifest, indent=2, sort_keys=True))
        return 0
    print(f"name\t{manifest['name']}")
    print(f"version\t{manifest['version']}")
    print(f"scenario_count\t{manifest['scenario_count']}")
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
    scenarios = _scenario_collection(args)
    report = build_report(scenarios, _task_pack_manifest(args))
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
    scenarios: list[Scenario],
    task_pack: TaskPackManifest | None = None,
) -> dict:
    """Build a machine-readable dataset manifest."""

    redacted = _task_pack_is_hidden(task_pack)
    payload = {
        "name": BENCHMARK_NAME,
        "version": task_pack.version if task_pack else BENCHMARK_VERSION,
        "release_id": task_pack.release_id if task_pack else BENCHMARK_RELEASE_ID,
        "canary_guid": CANARY_GUID,
        "redacted": redacted,
        "scenario_count": len(scenarios),
        "levels": sorted({scenario.level for scenario in scenarios}),
        "capabilities": sorted({scenario.capability for scenario in scenarios}),
        "workflows": sorted({scenario.workflow for scenario in scenarios}),
        "domains": sorted({scenario.domain for scenario in scenarios}),
        "subdomains": sorted({scenario.subdomain for scenario in scenarios}),
        "difficulties": sorted({scenario.difficulty for scenario in scenarios}),
        "splits": sorted({scenario.split for scenario in scenarios}),
        "tags": sorted({tag for scenario in scenarios for tag in scenario.tags}),
        "scenarios": [_scenario_summary(scenario) for scenario in scenarios],
    }
    if task_pack:
        payload["task_pack"] = {
            "pack_id": task_pack.pack_id,
            "release_id": task_pack.release_id,
            "version": task_pack.version,
            "visibility": task_pack.visibility,
            "default_split": task_pack.default_split,
            "description": task_pack.description,
        }
    return payload


def build_report(
    scenarios: list[Scenario],
    task_pack: TaskPackManifest | None = None,
) -> dict:
    """Run built-in baselines and return a release-style report payload."""

    runner = ScenarioRunner()
    oracle_results = [runner.run(scenario, "oracle") for scenario in scenarios]
    noop_results = [runner.run(scenario, "noop") for scenario in scenarios]
    return {
        "manifest": build_manifest(scenarios, task_pack),
        "baselines": {
            "oracle": _results_summary(oracle_results),
            "noop": _results_summary(noop_results),
        },
        "oracle_results": [_result_summary(result) for result in oracle_results],
        "noop_results": [_result_summary(result) for result in noop_results],
        "release_checks": {
            "oracle_all_pass": all(result.grade.passed for result in oracle_results),
            "noop_all_fail": all(not result.grade.passed for result in noop_results),
            "scenario_count_at_least_25": len(scenarios) >= 25,
        },
    }


def _cmd_run(args: argparse.Namespace) -> int:
    scenarios = _selected_scenarios(args)
    agent = build_agent(args.agent)
    runner = ScenarioRunner()
    results = [runner.run(scenario, agent) for scenario in scenarios]
    if args.trace_dir:
        _write_trace_artifacts(
            Path(args.trace_dir),
            results,
            redact_prompts=_should_redact_task_pack(args),
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
                f"{status}\t{result.scenario.id}\t"
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
    if args.scenario_file and not args.scenario:
        scenario = load_scenario_file(Path(args.scenario_file))
        write_task_envelope(Path(args.output), scenario)
        print(f"Wrote task envelope for {scenario.id} to {args.output}")
        return 0
    scenario_id = args.scenario or "l1_add_price_widget"
    scenario = _scenario_from_file_or_builtin(scenario_id, args.scenario_file)
    write_task_envelope(Path(args.output), scenario)
    print(f"Wrote task envelope for {scenario.id} to {args.output}")
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
    scenarios = _selected_scenarios(args)
    base_run_dir = Path(args.run_dir) if args.run_dir else None
    runs: list[AgentCommandRun] = []
    for scenario in scenarios:
        scenario_run_dir = base_run_dir / scenario.id if base_run_dir else None
        runs.append(
            run_agent_command(
                scenario=scenario,
                command=args.agent_command,
                timeout_seconds=args.timeout,
                run_dir=scenario_run_dir,
            )
        )
    results = [run.run_result for run in runs]
    if args.trace_dir:
        _write_trace_artifacts(
            Path(args.trace_dir),
            results,
            redact_prompts=_should_redact_task_pack(args),
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
                f"{status}\t{result.scenario.id}\t"
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

    scenario = find_scenario(args.scenario, pack=args.pack)
    try:
        result = asyncio.run(
            run_workspace_mcp_smoke(
                scenario=scenario,
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
            f"{status}\t{run_result.scenario.id}\t"
            f"{run_result.grade.score:.2f}\t"
            f"{run_result.grade.checks_passed}/{run_result.grade.checks_total}"
        )
        print(f"MCP_TOOLS\t{len(result.mcp_tools)}")
        print(f"MCP_PROMPTS\t{len(result.mcp_prompts)}")
        print(f"MCP_RESOURCES\t{len(result.mcp_resources)}")
        for issue in result.surface_issues:
            print(f"  - surface: {issue}")
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
        f"Scenarios: `{manifest['scenario_count']}`",
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
            "## Scenario Results",
            "",
            "| Scenario | Split | Level | Capability | Workflow | Domain | Subdomain | Difficulty | Oracle | Noop |",
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


def validate_scenarios(scenarios: list[Scenario], min_scenarios: int = 1) -> dict:
    """Validate scenario loadability, metadata, oracle pass, and noop failure."""

    runner = ScenarioRunner()
    oracle_results = [runner.run(scenario, "oracle") for scenario in scenarios]
    noop_results = [runner.run(scenario, "noop") for scenario in scenarios]
    issues = []
    seen_ids: set[str] = set()
    duplicate_ids: set[str] = set()
    for scenario in scenarios:
        if scenario.id in seen_ids:
            duplicate_ids.add(scenario.id)
        seen_ids.add(scenario.id)
    for scenario_id in sorted(duplicate_ids):
        issues.append(
            {
                "scenario_id": scenario_id,
                "message": "scenario id must be unique within the selected pack",
            }
        )
    if len(scenarios) < min_scenarios:
        issues.append(
            {
                "scenario_id": "benchmark",
                "message": (
                    f"expected at least {min_scenarios} scenario(s), "
                    f"found {len(scenarios)}"
                ),
            }
        )
    for scenario, oracle_result, noop_result in zip(
        scenarios, oracle_results, noop_results
    ):
        for message in _scenario_metadata_issues(scenario):
            issues.append({"scenario_id": scenario.id, "message": message})
        if not oracle_result.grade.passed:
            issues.append(
                {
                    "scenario_id": scenario.id,
                    "message": "oracle trace does not pass scenario grader",
                }
            )
        if noop_result.grade.passed:
            issues.append(
                {
                    "scenario_id": scenario.id,
                    "message": "noop baseline passed; scenario is too weak",
                }
            )
    return {
        "passed": not issues,
        "scenario_count": len(scenarios),
        "oracle_passed": sum(result.grade.passed for result in oracle_results),
        "noop_failed": sum(not result.grade.passed for result in noop_results),
        "issues": issues,
    }


def _scenario_metadata_issues(scenario: Scenario) -> list[str]:
    issues = []
    if scenario.difficulty not in {"easy", "medium", "hard"}:
        issues.append("difficulty must be one of easy, medium, hard")
    if scenario.split not in VALID_SCENARIO_SPLITS:
        issues.append(
            f"split must be one of {', '.join(sorted(VALID_SCENARIO_SPLITS))}"
        )
    if not scenario.capability:
        issues.append("capability must be non-empty")
    if not scenario.workflow:
        issues.append("workflow must be non-empty")
    if not scenario.domain:
        issues.append("domain must be non-empty")
    if not scenario.subdomain:
        issues.append("subdomain must be non-empty")
    if not scenario.tags:
        issues.append("at least one tag is required")
    if not scenario.oracle_tool_calls:
        issues.append("oracle_tool_calls must be non-empty")
    if not scenario.allowed_tools:
        issues.append("allowed_tools must be non-empty")
    return issues


def _filtered_scenarios(args: argparse.Namespace) -> list[Scenario]:
    scenarios = _scenario_collection(args)
    if getattr(args, "level", None):
        scenarios = [
            scenario for scenario in scenarios if scenario.level == args.level
        ]
    if getattr(args, "capability", None):
        scenarios = [
            scenario for scenario in scenarios if scenario.capability == args.capability
        ]
    if getattr(args, "workflow", None):
        scenarios = [
            scenario for scenario in scenarios if scenario.workflow == args.workflow
        ]
    if getattr(args, "domain", None):
        scenarios = [scenario for scenario in scenarios if scenario.domain == args.domain]
    if getattr(args, "subdomain", None):
        scenarios = [
            scenario for scenario in scenarios if scenario.subdomain == args.subdomain
        ]
    if getattr(args, "difficulty", None):
        scenarios = [
            scenario
            for scenario in scenarios
            if scenario.difficulty == args.difficulty
        ]
    if getattr(args, "split", None):
        scenarios = [scenario for scenario in scenarios if scenario.split == args.split]
    for tag in getattr(args, "tag", []) or []:
        scenarios = [scenario for scenario in scenarios if tag in scenario.tags]
    return scenarios


def _selected_scenarios(args: argparse.Namespace) -> list[Scenario]:
    if getattr(args, "scenario_file", None):
        return [load_scenario_file(Path(args.scenario_file))]
    scenarios = _filtered_scenarios(args)
    scenario_id = getattr(args, "scenario", None)
    if scenario_id:
        scenarios = [scenario for scenario in scenarios if scenario.id == scenario_id]
        if not scenarios:
            raise KeyError(f"Unknown scenario {scenario_id!r}")
    return scenarios


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

    scenarios = _selected_scenarios(args)
    if getattr(args, "oracle", False):
        records = rollouts_from_oracle(scenarios)
        return annotate_rollouts(records, task_pack=_task_pack_manifest(args))
    if getattr(args, "comparison_dir", None):
        records = load_comparison_rollouts(Path(args.comparison_dir), scenarios)
        return annotate_rollouts(records, task_pack=_task_pack_manifest(args))
    records = load_trace_dir_rollouts(Path(args.trace_dir), scenarios)
    return annotate_rollouts(records, task_pack=_task_pack_manifest(args))


def _scenario_collection(args: argparse.Namespace) -> list[Scenario]:
    scenario_dir = getattr(args, "scenario_dir", None)
    if not scenario_dir:
        return load_builtin_scenarios(getattr(args, "pack", "core"))
    return load_scenario_directory(Path(scenario_dir))


def _task_pack_manifest(args: argparse.Namespace) -> TaskPackManifest | None:
    scenario_dir = getattr(args, "scenario_dir", None)
    if not scenario_dir:
        return load_builtin_task_pack_manifest(getattr(args, "pack", "core"))
    return load_task_pack_manifest(Path(scenario_dir))


def _should_redact_task_pack(args: argparse.Namespace) -> bool:
    return _task_pack_is_hidden(_task_pack_manifest(args))


def _task_pack_is_hidden(task_pack: TaskPackManifest | None) -> bool:
    return task_pack is not None and task_pack.visibility == "hidden"


def _scenario_from_file_or_builtin(
    scenario_id: str, scenario_file: str | None
) -> Scenario:
    if scenario_file:
        scenario = load_scenario_file(Path(scenario_file))
        if scenario_id and scenario.id != scenario_id:
            raise ValueError(
                f"scenario file contains {scenario.id!r}, not requested {scenario_id!r}"
            )
        return scenario
    return find_scenario(scenario_id)


def _scenario_summary(scenario: Scenario) -> dict:
    return {
        "id": scenario.id,
        "title": scenario.title,
        "level": scenario.level,
        "capability": scenario.capability,
        "workflow": scenario.workflow,
        "domain": scenario.domain,
        "subdomain": scenario.subdomain,
        "difficulty": scenario.difficulty,
        "split": scenario.split,
        "tags": scenario.tags,
        "source": scenario.source,
        "fixtures": [backend.name for backend in scenario.fixtures],
        "oracle_tool_call_count": len(scenario.oracle_tool_calls),
    }


def _result_summary(result: RunResult) -> dict:
    return {
        "id": result.scenario.id,
        "level": result.scenario.level,
        "capability": result.scenario.capability,
        "workflow": result.scenario.workflow,
        "domain": result.scenario.domain,
        "subdomain": result.scenario.subdomain,
        "difficulty": result.scenario.difficulty,
        "split": result.scenario.split,
        "tags": result.scenario.tags,
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
        bucket = by_level.setdefault(result.scenario.level, {"passed": 0, "total": 0})
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
        scenario_payload = {
            "id": result.scenario.id,
            "title": result.scenario.title,
            "level": result.scenario.level,
            "capability": result.scenario.capability,
            "workflow": result.scenario.workflow,
            "domain": result.scenario.domain,
            "subdomain": result.scenario.subdomain,
            "difficulty": result.scenario.difficulty,
            "split": result.scenario.split,
            "tags": result.scenario.tags,
        }
        if redact_prompts:
            scenario_payload["prompt_redacted"] = True
        else:
            scenario_payload["prompt"] = result.scenario.prompt
        payload = {
            "scenario": scenario_payload,
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
        output_path = trace_dir / f"{result.scenario.id}.json"
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
