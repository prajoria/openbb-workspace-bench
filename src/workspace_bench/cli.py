"""Command line interface for Workspace Bench."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import asdict
from pathlib import Path
from threading import Event

from workspace_bench.agents.agent_command import (
    AgentCommandRun,
    run_agent_command,
    write_task_envelope,
)
from workspace_bench.agents import build_agent
from workspace_bench.workspace.fixtures import get_fixture_backend, make_fixture_server
from workspace_bench.core.models import (
    BENCHMARK_NAME,
    CANARY_GUID,
    Task,
    TaskSuiteManifest,
    VALID_TASK_SPLITS,
)
from workspace_bench.core.provenance import git_provenance
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
from workspace_bench.reports.oracle_report import (
    build_manifest,
    build_report,
    render_markdown_report as _render_markdown_report,
    result_summary as _result_summary,
    results_summary as _results_summary,
    task_summary as _task_summary,
    write_trace_artifacts as _write_trace_artifacts,
)
from workspace_bench.reports.validation import validate_tasks


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
    show_parser.add_argument("--suite", default="core", choices=list(BUILTIN_TASK_SUITE_ORDER))

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

    manifest_parser = subparsers.add_parser("manifest", help="Print a benchmark dataset manifest.")
    _add_task_collection_args(manifest_parser)
    manifest_parser.add_argument("--json", action="store_true", help="Emit JSON.")

    report_parser = subparsers.add_parser(
        "report", help="Generate a benchmark report from built-in baselines."
    )
    _add_task_collection_args(report_parser)
    report_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    report_parser.add_argument("--output", help="Write report to a file.")

    compile_parser = subparsers.add_parser(
        "compile",
        help="Compile analysis reports from stored run results.",
    )
    compile_parser.add_argument(
        "kind",
        choices=["calibration", "suites", "significance", "difficulty"],
        help="Which report to compile.",
    )
    compile_parser.add_argument(
        "compile_args",
        nargs=argparse.REMAINDER,
        help="Arguments forwarded to the report compiler (see its --help).",
    )

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

    serve_parser = subparsers.add_parser("serve-fixture", help="Serve a fixture backend over HTTP.")
    serve_parser.add_argument("--backend", default="equities")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=9101)

    task_backend_parser = subparsers.add_parser(
        "serve-task-backend",
        help="Serve one task's oracle backend and runtime datasets over HTTP.",
    )
    task_backend_parser.add_argument("--task", required=True)
    task_backend_parser.add_argument("--backend-name")
    task_backend_parser.add_argument("--host", default="127.0.0.1")
    task_backend_parser.add_argument("--port", type=int, default=9102)
    task_backend_parser.add_argument(
        "--cors-origin",
        default="*",
        help="Allowed Workspace origin. Defaults to all origins for local certification.",
    )

    browser_parser = subparsers.add_parser(
        "browser-cert",
        help="Run the browser-backed oracle certification subset.",
    )
    browser_parser.add_argument("--task", help="Qualified task ref from the subset.")
    browser_parser.add_argument("--all", action="store_true", help="Run the full subset.")
    browser_parser.add_argument("--headed", action="store_true")
    browser_parser.add_argument("--workspace-url", default="https://pro.openbb.co")
    browser_parser.add_argument("--auth-state", type=Path)
    browser_parser.add_argument("--setup-auth", action="store_true")
    browser_parser.add_argument("--self-test", action="store_true")
    browser_parser.add_argument("--dry-run", action="store_true")
    browser_parser.add_argument("--selectors", type=Path, help="Local selector JSON override.")
    browser_parser.add_argument(
        "--code-task-backend",
        help="Optional running flagship backend URL to add to --self-test.",
    )
    browser_parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("runs/browser-cert"),
    )

    runtime_parser = subparsers.add_parser(
        "runtime-probe",
        help="Run oracle fixture-backed HTTP endpoint probes for a task suite.",
    )
    _add_task_collection_args(runtime_parser)
    _add_task_filters(runtime_parser)
    runtime_parser.add_argument("--json", action="store_true", help="Emit JSON.")

    adversarial_parser = subparsers.add_parser(
        "adversarial",
        help="Run systematic invalid-candidate grader checks for a task suite.",
    )
    _add_task_collection_args(adversarial_parser)
    _add_task_filters(adversarial_parser)
    adversarial_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    adversarial_parser.add_argument(
        "--runtime-sample-per-family",
        type=int,
        default=3,
        help="Runtime-mutant sample per applicable family and archetype (default: 3).",
    )

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
    smoke_parser.add_argument("--task", default="core/create/price_performance_aapl")
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
    export_parser.add_argument("--suite", default="core", choices=list(BUILTIN_TASK_SUITE_ORDER))
    export_parser.add_argument("--output", required=True)

    migrate_parser = subparsers.add_parser(
        "migrate-task", help="Migrate one pre-versioned task JSON to the strict schema."
    )
    migrate_parser.add_argument("--input", required=True)
    migrate_parser.add_argument("--output", required=True)

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

    code_parser = subparsers.add_parser(
        "run-code-task",
        help="Run an external coding agent in a real backend starter repository.",
    )
    code_parser.add_argument("--task", required=True, help="Code task id or qualified ref.")
    code_parser.add_argument("--agent-command", required=True)
    code_parser.add_argument("--timeout", type=float, default=300)
    code_parser.add_argument("--run-dir", type=Path)
    code_parser.add_argument("--json", action="store_true", help="Emit the result and receipt JSON.")

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
    if args.command == "compile":
        return _cmd_compile(args)
    if args.command == "run":
        return _cmd_run(args)
    if args.command == "serve-fixture":
        return _cmd_serve_fixture(args.backend, args.host, args.port)
    if args.command == "serve-task-backend":
        return _cmd_serve_task_backend(args)
    if args.command == "browser-cert":
        return _cmd_browser_cert(args)
    if args.command == "runtime-probe":
        return _cmd_runtime_probe(args)
    if args.command == "adversarial":
        return _cmd_adversarial(args)
    if args.command == "smoke-workspace-mcp":
        return _cmd_smoke_workspace_mcp(args)
    if args.command == "export-task":
        return _cmd_export_task(args)
    if args.command == "migrate-task":
        return _cmd_migrate_task(args)
    if args.command == "export-rollouts":
        return _cmd_export_rollouts(args)
    if args.command == "export-sft":
        return _cmd_export_sft(args)
    if args.command == "export-preferences":
        return _cmd_export_preferences(args)
    if args.command == "run-agent-command":
        return _cmd_run_agent_command(args)
    if args.command == "run-code-task":
        return _cmd_run_code_task(args)
    if args.command == "canary":
        print(CANARY_GUID)
        return 0
    parser.error(f"Unknown command {args.command}")
    return 2


def _add_task_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--family", help="Filter by task family, e.g. create or forms.")
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
            "(300); build-openbb-apps = building and debugging custom backend apps (236); "
            "build-openbb-backends = experimental real-code FastAPI tasks (12)."
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
            f"{task.qualified_id}\t{task.difficulty}\t"
            f"{task.split}\t"
            f"{task.capability}\t{task.workflow}\t"
            f"{task.domain}\t{task.subdomain}\t{tags}\t{task.title}"
        )
    return 0


def _cmd_show(args: argparse.Namespace) -> int:
    task = _task_from_file_or_builtin(args.task_id, args.task_file, args.suite)
    payload = _task_summary(task)
    payload.update(
        {
            "prompt": task.prompt,
            "allowed_tools": task.allowed_tools,
            "limits": task.limits,
            "success": {
                "required_tabs": task.success.required_tabs,
                "required_widget_count": len(task.success.required_widgets),
                "required_generated_widget_count": len(task.success.required_generated_widgets),
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
    print(f"task_count\t{manifest['task_count']}")
    print(f"git_commit\t{manifest['git_commit']}")
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


def _cmd_compile(args: argparse.Namespace) -> int:
    if args.kind == "calibration":
        from workspace_bench.reports.calibration import main as compile_main
    elif args.kind == "suites":
        from workspace_bench.reports.suites import main as compile_main
    elif args.kind == "significance":
        from workspace_bench.reports.significance import main as compile_main
    else:
        from workspace_bench.reports.difficulty import main as compile_main
    return compile_main(list(args.compile_args))


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


def _cmd_runtime_probe(args: argparse.Namespace) -> int:
    tasks = [task for task in _filtered_tasks(args) if task.success.runtime is not None]
    runner = TaskRunner()
    results = [runner.run(task, "oracle") for task in tasks]
    families: dict[str, dict[str, int]] = {}
    for result in results:
        row = families.setdefault(
            result.task.family,
            {"tasks": 0, "passed": 0, "probes": 0, "checks_passed": 0},
        )
        row["tasks"] += 1
        row["passed"] += int(result.grade.runtime_passed)
        row["probes"] += result.grade.runtime_checks_total
        row["checks_passed"] += result.grade.runtime_checks_passed
    passed_total = sum(result.grade.runtime_passed for result in results)
    runtime_issues = [
        {
            "task_id": result.task.id,
            "code": issue.code,
            "message": issue.message,
        }
        for result in results
        for issue in result.grade.issues
        if issue.code.startswith("endpoint_")
        or issue.code == "form_submission_incompatible"
    ]
    payload = {
        "suite": getattr(args, "suite", "custom"),
        "task_count": len(results),
        "passed": passed_total,
        "families": families,
        "issues": runtime_issues,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"{'family':14s} {'tasks':>7s} {'passed':>8s} {'probes':>8s}")
        for family, row in sorted(families.items()):
            print(
                f"{family:14s} {row['tasks']:7d} "
                f"{row['passed']:8d} {row['probes']:8d}"
            )
        print(
            f"TOTAL          {len(results):7d} "
            f"{passed_total:8d} {sum(row['probes'] for row in families.values()):8d}"
        )
        for issue in runtime_issues[:20]:
            print(f"  - {issue['task_id']}: {issue['code']}: {issue['message']}")
    return 0 if passed_total == len(results) else 1


def _cmd_adversarial(args: argparse.Namespace) -> int:
    from workspace_bench.core.adversarial import run_adversarial_matrix

    tasks = _filtered_tasks(args)
    matrix = run_adversarial_matrix(
        tasks,
        runtime_sample_per_family=args.runtime_sample_per_family,
    )
    failures = [
        {
            "task_id": result.task_id,
            "family": result.family,
            "archetype": result.candidate.archetype,
            "candidate": result.candidate.name,
            "oracle_clean": result.oracle_clean,
            "candidate_passed": result.candidate_grade.passed,
            "primary_code": result.candidate.primary_code,
            "expected_codes": list(result.candidate.expected_codes),
            "observed_codes": list(result.observed_codes),
        }
        for result in matrix.results
        if not result.passed
    ]
    payload = {
        "suite": getattr(args, "suite", "custom"),
        "task_count": len(tasks),
        "passed": matrix.passed,
        "runtime_sample_per_family": matrix.runtime_sample_per_family,
        "candidate_count": len(matrix.results),
        "applicable_count": sum(matrix.applicable.values()),
        "survivor_count": len(matrix.survivors),
        "wrong_reason_count": len(matrix.wrong_reason),
        "dirty_oracle_count": len(matrix.dirty_oracles),
        "matrix": matrix.rows(),
        "examples": matrix.examples(),
        "failures": failures,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(
            f"suite={payload['suite']} tasks={len(tasks)} "
            f"candidates={len(matrix.results)}/{sum(matrix.applicable.values())} applicable"
        )
        print(
            f"{'family':14s} {'archetype':28s} {'app':>4s} {'run':>4s} "
            f"{'reject':>6s} {'wrong':>5s} {'survive':>7s}"
        )
        for row in matrix.rows():
            print(
                f"{row['family']:14s} {row['archetype']:28s} "
                f"{row['applicable']:4d} {row['exercised']:4d} "
                f"{row['rejected']:6d} {row['wrong_reason']:5d} "
                f"{row['survivors']:7d}"
            )
        status = "PASS" if matrix.passed else "FAIL"
        print(
            f"{status}: survivors={len(matrix.survivors)} "
            f"wrong_reason={len(matrix.wrong_reason)} "
            f"dirty_oracles={len(matrix.dirty_oracles)}"
        )
        for failure in failures[:20]:
            print(
                f"  - {failure['task_id']} {failure['archetype']}: "
                f"primary={failure['primary_code']} "
                f"secondary={failure['expected_codes']} observed={failure['observed_codes']}"
            )
    return 0 if matrix.passed else 1


def _cmd_export_task(args: argparse.Namespace) -> int:
    if args.task_file and not args.task:
        task = _load_task_file_with_suite(Path(args.task_file))
        write_task_envelope(Path(args.output), task)
        print(f"Wrote task envelope for {task.id} to {args.output}")
        return 0
    task_id = args.task or "core/create/price_performance_aapl"
    task = _task_from_file_or_builtin(task_id, args.task_file, args.suite)
    write_task_envelope(Path(args.output), task)
    print(f"Wrote task envelope for {task.id} to {args.output}")
    return 0


def _cmd_migrate_task(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    migrated = Task.migrate_legacy_payload(payload)
    # Load before writing so migration never emits a task the strict loader
    # would reject.
    Task.from_dict(migrated, source_path=input_path)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(migrated, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Migrated {migrated['id']} to {output_path}")
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
        task_run_dir = base_run_dir / task.family / task.id if base_run_dir else None
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
                        **git_provenance(),
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


def _cmd_run_code_task(args: argparse.Namespace) -> int:
    from workspace_bench.code_tasks import run_code_task

    task = find_task(args.task, suite="build-openbb-backends")
    run = run_code_task(
        task=task,
        agent_command=args.agent_command,
        timeout_seconds=args.timeout,
        workdir=args.run_dir,
    )
    grade = run.evaluation.grade
    process_ok = run.exit_code == 0 and not run.timed_out
    passed = process_ok and grade.passed
    receipt_path = run.evaluation.workdir / ".workspace-bench" / "deployment-receipt.json"
    payload = {
        "schema_version": "workspace-bench-code-result/v0",
        "task": {
            "id": task.id,
            "qualified_id": task.qualified_id,
            "specification_level": task.specification_level,
            "difficulty": task.difficulty,
        },
        "agent": {
            "command": run.command,
            "exit_code": run.exit_code,
            "timed_out": run.timed_out,
            "stdout": run.stdout,
            "stderr": run.stderr,
        },
        "passed": passed,
        "grade": asdict(grade),
        "deployment_receipt": run.evaluation.receipt,
        "artifacts": {
            "workdir": str(run.evaluation.workdir),
            "task_json": str(run.task_path),
            "task_brief": str(run.brief_path),
            "receipt": str(receipt_path),
        },
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        status = "PASS" if passed else "FAIL"
        print(
            f"{status}\t{task.id}\t{grade.score:.2f}\t"
            f"{grade.checks_passed}/{grade.checks_total}\t"
            f"exit={run.exit_code}\ttimeout={run.timed_out}"
        )
        print(f"  workdir: {run.evaluation.workdir}")
        print(f"  receipt: {receipt_path}")
        for issue in grade.issues:
            print(f"  - {issue.code}: {issue.message}")
    return 0 if passed else 1


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
            getattr(args, "family", None),
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


def _filtered_tasks(args: argparse.Namespace) -> list[Task]:
    tasks = _task_collection(args)
    if getattr(args, "family", None):
        tasks = [task for task in tasks if task.family == args.family]
    if getattr(args, "category", None):
        tasks = [task for task in tasks if task.category == args.category]
    if getattr(args, "capability", None):
        tasks = [task for task in tasks if task.capability == args.capability]
    if getattr(args, "workflow", None):
        tasks = [task for task in tasks if task.workflow == args.workflow]
    if getattr(args, "domain", None):
        tasks = [task for task in tasks if task.domain == args.domain]
    if getattr(args, "subdomain", None):
        tasks = [task for task in tasks if task.subdomain == args.subdomain]
    if getattr(args, "difficulty", None):
        tasks = [task for task in tasks if task.difficulty == args.difficulty]
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


def _task_from_file_or_builtin(task_id: str, task_file: str | None, suite: str = "core") -> Task:
    if task_file:
        task = _load_task_file_with_suite(Path(task_file))
        if task_id and task.id != task_id:
            raise ValueError(f"task file contains {task.id!r}, not requested {task_id!r}")
        return task
    return find_task(task_id, suite=suite)


def _load_task_file_with_suite(path: Path) -> Task:
    """Load a task and attach the nearest ancestor suite manifest."""

    manifest = None
    for directory in (path.parent, *path.parents):
        manifest = load_task_suite_manifest(directory)
        if manifest:
            break
    return load_task_file(path, task_suite=manifest)


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
    summary["process_failures"] = sum(run.exit_code != 0 or run.timed_out for run in runs)
    return summary


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


def _cmd_serve_task_backend(args: argparse.Namespace) -> int:
    from workspace_bench.browser.task_backend import TaskBackendServer

    task = find_task(args.task)
    server = TaskBackendServer(
        task,
        backend_name=args.backend_name,
        host=args.host,
        port=args.port,
        cors_origin=args.cors_origin,
    ).start()
    print(f"Serving {server.model.backend_name} for {task.qualified_id} at {server.base_url}")
    print(f"  widgets: {server.base_url}/widgets.json")
    print(f"  apps:    {server.base_url}/apps.json")
    try:
        Event().wait()
    except KeyboardInterrupt:
        print("\nStopping task backend.")
    finally:
        server.close()
    return 0


def _cmd_browser_cert(args: argparse.Namespace) -> int:
    from workspace_bench.browser.certification import browser_certify, setup_browser_auth

    if args.setup_auth:
        if args.auth_state is None:
            raise ValueError("--setup-auth requires --auth-state PATH")
        setup_browser_auth(workspace_url=args.workspace_url, auth_state=args.auth_state)
        print(f"Saved Workspace browser state to {args.auth_state}")
        return 0
    result = browser_certify(
        task_ref=args.task,
        all_entries=args.all,
        headed=args.headed,
        workspace_url=args.workspace_url,
        auth_state=args.auth_state,
        self_test=args.self_test,
        dry_run=args.dry_run,
        selectors_path=args.selectors,
        output_root=args.output_root,
        code_task_backend=args.code_task_backend,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
