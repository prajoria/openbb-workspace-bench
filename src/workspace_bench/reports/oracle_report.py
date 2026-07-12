"""Dataset manifests, baseline reports, and run-result serialization."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from workspace_bench.core.models import (
    BENCHMARK_NAME,
    CANARY_GUID,
    JsonDict,
    RunResult,
    Task,
    TaskSuiteManifest,
)
from workspace_bench.core.provenance import git_provenance
from workspace_bench.core.runner import TaskRunner
from workspace_bench.core.suite_checks import release_checks_for_suite
from workspace_bench.reports.serialization import grade_summary


def task_summary(task: Task) -> dict[str, Any]:
    return {
        "id": task.id,
        "qualified_id": task.qualified_id,
        "title": task.title,
        "family": task.family,
        "capability": task.capability,
        "workflow": task.workflow,
        "domain": task.domain,
        "subdomain": task.subdomain,
        "specification_level": task.specification_level,
        "difficulty": task.difficulty,
        "split": task.split,
        "tags": task.tags,
        "source": task.source,
        "novelty": task.novelty,
        "fixtures": [backend.name for backend in task.fixtures],
        "oracle_tool_call_count": len(task.oracle_tool_calls),
        "code_task": task.code_task is not None,
    }


def result_summary(result: RunResult) -> dict[str, Any]:
    return {
        "id": result.task.id,
        "qualified_id": result.task.qualified_id,
        "category": result.task.category,
        "family": result.task.family,
        "capability": result.task.capability,
        "workflow": result.task.workflow,
        "domain": result.task.domain,
        "subdomain": result.task.subdomain,
        "specification_level": result.task.specification_level,
        "difficulty": result.task.difficulty,
        "split": result.task.split,
        "tags": result.task.tags,
        "novelty": result.task.novelty,
        **grade_summary(result.grade),
    }


def results_summary(results: list[RunResult]) -> dict[str, Any]:
    total = len(results)
    passed = sum(result.grade.passed for result in results)
    mean_score = sum(result.grade.score for result in results) / total if total else 0.0
    state_passed = sum(result.grade.state_passed for result in results)
    trace_passed = sum(result.grade.trace_passed for result in results)
    runtime_results = [result for result in results if result.task.success.runtime is not None]
    polish_results = [result for result in results if result.grade.polish_checks_total > 0]
    runtime_passed = sum(result.grade.runtime_passed for result in runtime_results)
    by_difficulty: dict[str, dict[str, int]] = {}
    for result in results:
        bucket = by_difficulty.setdefault(result.task.difficulty, {"passed": 0, "total": 0})
        bucket["total"] += 1
        if result.grade.passed:
            bucket["passed"] += 1
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "mean_score": mean_score,
        "state_passed": state_passed,
        "state_pass_rate": state_passed / total if total else 0.0,
        "trace_passed": trace_passed,
        "trace_pass_rate": trace_passed / total if total else 0.0,
        "mean_state_score": (
            sum(result.grade.state_score for result in results) / total if total else 0.0
        ),
        "mean_trace_score": (
            sum(result.grade.trace_score for result in results) / total if total else 0.0
        ),
        "runtime_task_count": len(runtime_results),
        "runtime_passed": runtime_passed,
        "runtime_pass_rate": (
            runtime_passed / len(runtime_results) if runtime_results else 1.0
        ),
        "mean_runtime_score": (
            sum(result.grade.runtime_score for result in runtime_results) / len(runtime_results)
            if runtime_results
            else 1.0
        ),
        "polish_task_count": len(polish_results),
        "mean_polish_score": (
            sum(result.grade.polish_score for result in polish_results) / len(polish_results)
            if polish_results
            else 1.0
        ),
        "by_difficulty": by_difficulty,
    }


def build_manifest(
    tasks: list[Task], task_suite: TaskSuiteManifest | None = None
) -> dict[str, Any]:
    """Build a machine-readable dataset manifest."""

    redacted = task_suite is not None and task_suite.visibility == "hidden"
    payload: dict[str, Any] = {
        "name": BENCHMARK_NAME,
        **git_provenance(source_paths=[task.source_path for task in tasks if task.source_path]),
        "canary_guid": CANARY_GUID,
        "redacted": redacted,
        "task_count": len(tasks),
        "families": sorted({task.family for task in tasks}),
        "capabilities": sorted({task.capability for task in tasks}),
        "workflows": sorted({task.workflow for task in tasks}),
        "domains": sorted({task.domain for task in tasks}),
        "subdomains": sorted({task.subdomain for task in tasks}),
        "specification_levels": sorted({task.specification_level for task in tasks}),
        "difficulties": sorted({task.difficulty for task in tasks}),
        "splits": sorted({task.split for task in tasks}),
        "tags": sorted({tag for task in tasks for tag in task.tags}),
        "tasks": [task_summary(task) for task in tasks],
    }
    if task_suite:
        payload["task_suite"] = {
            "suite_id": task_suite.suite_id,
            "content_sha256": task_suite.content_sha256,
            "visibility": task_suite.visibility,
            "default_split": task_suite.default_split,
            "description": task_suite.description,
        }
    return payload


def build_report(
    tasks: list[Task],
    task_suite: TaskSuiteManifest | None = None,
    release_profile: str | None = None,
) -> dict[str, Any]:
    """Run built-in baselines and return a release-style report payload."""

    runner = TaskRunner()
    oracle_results = [runner.run(task, "oracle") for task in tasks]
    noop_results = [runner.run(task, "noop") for task in tasks]
    release_checks = {
        "oracle_all_pass": all(result.grade.passed for result in oracle_results),
        "noop_all_fail": all(not result.grade.passed for result in noop_results),
    }
    release_checks.update(release_checks_for_suite(release_profile, tasks, oracle_results))
    return {
        "manifest": build_manifest(tasks, task_suite),
        "baselines": {
            "oracle": results_summary(oracle_results),
            "noop": results_summary(noop_results),
        },
        "oracle_results": [result_summary(result) for result in oracle_results],
        "noop_results": [result_summary(result) for result in noop_results],
        "release_checks": release_checks,
    }


def render_markdown_report(report: dict[str, Any]) -> str:
    manifest = report["manifest"]
    oracle = report["baselines"]["oracle"]
    noop = report["baselines"]["noop"]
    checks = report["release_checks"]
    lines = [
        "# OpenBB Workspace Bench Report",
        "",
        f"Git commit: `{manifest['git_commit']}`",
        f"Git dirty: `{manifest['git_dirty']}`",
        f"Tasks: `{manifest['task_count']}`",
        f"Canary: `{manifest['canary_guid']}`",
        f"Redacted: `{manifest.get('redacted', False)}`",
        "",
        "## Coverage",
        "",
        f"- Families: {', '.join(manifest['families'])}",
        f"- Capabilities: {', '.join(manifest['capabilities'])}",
        f"- Workflows: {', '.join(manifest['workflows'])}",
        f"- Domains: {', '.join(manifest['domains'])}",
        f"- Subdomains: {', '.join(manifest['subdomains'])}",
        f"- Specification levels: {', '.join(manifest['specification_levels'])}",
        f"- Difficulties: {', '.join(manifest['difficulties'])}",
        f"- Splits: {', '.join(manifest['splits'])}",
        f"- Tags: {', '.join(manifest['tags'])}",
        "",
        "## Baselines",
        "",
        "| Baseline | Passed | Total | Mean Score |",
        "| --- | ---: | ---: | ---: |",
        f"| oracle | {oracle['passed']} | {oracle['total']} | {oracle['mean_score']:.3f} |",
        f"| noop | {noop['passed']} | {noop['total']} | {noop['mean_score']:.3f} |",
        "",
        "## Release Checks",
        "",
    ]
    for check_name, passed in checks.items():
        lines.append(f"- {'PASS' if passed else 'FAIL'}: `{check_name}`")
    lines.extend(
        [
            "",
            "## Task Results",
            "",
            "| Task | Split | Capability | Workflow | Domain | Subdomain | Specification | Difficulty | Oracle | Noop |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: |",
        ]
    )
    noop_by_id = {result["id"]: result for result in report["noop_results"]}
    for oracle_result in report["oracle_results"]:
        noop_result = noop_by_id[oracle_result["id"]]
        lines.append(
            "| "
            f"{oracle_result['id']} | {oracle_result['split']} | "
            f"{oracle_result['capability']} | {oracle_result['workflow']} | "
            f"{oracle_result['domain']} | {oracle_result['subdomain']} | "
            f"{oracle_result['specification_level']} | {oracle_result['difficulty']} | "
            f"{oracle_result['score']:.3f} | {noop_result['score']:.3f} |"
        )
    return "\n".join(lines)


def write_trace_artifacts(
    trace_dir: Path, results: list[RunResult], *, redact_prompts: bool = False
) -> None:
    trace_dir.mkdir(parents=True, exist_ok=True)
    id_counts = {
        task_id: sum(result.task.id == task_id for result in results)
        for task_id in {result.task.id for result in results}
    }
    for result in results:
        task_payload: JsonDict = {
            "id": result.task.id,
            "qualified_id": result.task.qualified_id,
            "title": result.task.title,
            "family": result.task.family,
            "capability": result.task.capability,
            "workflow": result.task.workflow,
            "domain": result.task.domain,
            "subdomain": result.task.subdomain,
            "difficulty": result.task.difficulty,
            "split": result.task.split,
            "tags": result.task.tags,
            "novelty": result.task.novelty,
        }
        task_payload["prompt_redacted" if redact_prompts else "prompt"] = (
            True if redact_prompts else result.task.prompt
        )
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
        filename = (
            f"{result.task.family}__{result.task.id}.json"
            if id_counts[result.task.id] > 1
            else f"{result.task.id}.json"
        )
        (trace_dir / filename).write_text(
            json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
        )
