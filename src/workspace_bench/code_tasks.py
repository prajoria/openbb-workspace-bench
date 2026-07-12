"""Execution and grading for experimental real-code backend tasks."""

from __future__ import annotations

import json
import os
import shutil
import signal
import socket
import subprocess
import tempfile
import time
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from workspace_bench.core.models import CodeProbe, CodeTaskSpec, JsonDict, Task
from workspace_bench.workspace.backend_validation import validate_apps_json, validate_widgets_json
from workspace_bench.workspace.runtime import contains_placeholder, response_shape_error
from workspace_bench.workspace.widget_params import flatten_params


CODE_RECEIPT_SCHEMA_VERSION = "workspace-bench-code-receipt/v0"
CODE_RESULT_SCHEMA_VERSION = "workspace-bench-code-result/v0"


@dataclass(frozen=True)
class CodeIssue:
    """One failed code-task evaluator check."""

    code: str
    message: str


@dataclass(frozen=True)
class CodeGrade:
    """Strict grade over installation, deployment, HTTP behavior, and tests."""

    score: float
    passed: bool
    checks_passed: int
    checks_total: int
    issues: tuple[CodeIssue, ...]


@dataclass(frozen=True)
class CodeEvaluation:
    """Evaluation output for one instantiated code repository."""

    task: Task
    grade: CodeGrade
    receipt: JsonDict
    workdir: Path


@dataclass(frozen=True)
class CodeAgentRun:
    """External agent process metadata plus its evaluated repository."""

    evaluation: CodeEvaluation
    command: str
    exit_code: int | None
    timed_out: bool
    stdout: str
    stderr: str
    task_path: Path
    brief_path: Path


def code_task_root(task: Task) -> Path:
    """Return the directory against which a code task's fixture paths resolve."""

    if task.code_task is None or task.source_path is None:
        raise ValueError(f"{task.qualified_id} is not a source-backed code task")
    return task.source_path.parent.resolve()


def instantiate_code_task(
    task: Task,
    *,
    workdir: Path | None = None,
    oracle: bool = False,
) -> Path:
    """Copy the starter repository and optionally apply the committed oracle overlay."""

    spec = _code_spec(task)
    root = code_task_root(task)
    starter = _safe_fixture_path(root, spec.starter_path)
    oracle_dir = _safe_fixture_path(root, spec.oracle_path)
    if not starter.is_dir() or not oracle_dir.is_dir():
        raise FileNotFoundError(f"missing code-task fixture for {task.qualified_id}")
    destination = workdir or Path(tempfile.mkdtemp(prefix=f"workspace-bench-code-{task.id}-"))
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError(f"code-task workdir must be empty: {destination}")
    shutil.copytree(starter, destination, dirs_exist_ok=True)
    if oracle:
        apply_oracle_overlay(task, destination)
    return destination


def apply_oracle_overlay(task: Task, workdir: Path) -> None:
    """Apply the committed solved-file overlay to an instantiated repository."""

    spec = _code_spec(task)
    oracle_dir = _safe_fixture_path(code_task_root(task), spec.oracle_path)
    shutil.copytree(oracle_dir, workdir, dirs_exist_ok=True)


def build_code_task_envelope(task: Task) -> JsonDict:
    """Build the public, oracle-free payload handed to a filesystem agent."""

    spec = _code_spec(task)
    return {
        "schema_version": "workspace-bench-code-envelope/v0",
        "task": {
            "id": task.id,
            "qualified_id": task.qualified_id,
            "title": task.title,
            "prompt": task.prompt,
            "specification_level": task.specification_level,
            "difficulty": task.difficulty,
            "family": task.family,
            "tags": list(task.tags),
        },
        "repository": {
            "start_command": list(spec.start_command),
            "test_command": list(spec.test_command),
            "health_path": spec.health_path,
        },
        "success": {
            "requires_apps_json": spec.require_apps,
            "probes": [asdict(probe) for probe in spec.probes],
            "tests_must_pass": True,
            "tests_must_reject_garbage_endpoint_logic": True,
        },
    }


def write_code_task_files(task: Task, workdir: Path) -> tuple[Path, Path]:
    """Write the JSON envelope and human-readable brief into the agent workdir."""

    task_path = workdir / "WORKSPACE_BENCH_TASK.json"
    brief_path = workdir / "TASK_BRIEF.md"
    task_path.write_text(
        json.dumps(build_code_task_envelope(task), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    brief_path.write_text(
        f"# {task.title}\n\n{task.prompt.strip()}\n\n"
        "## Evaluator contract\n\n"
        "Keep the task-local pinned environment and start command working. The evaluator "
        "will launch the backend on an injected ephemeral port, validate widgets.json and "
        "apps.json when required, exercise every declared HTTP probe, run pytest, and verify "
        "that the tests fail when app.py is replaced by garbage endpoint logic.\n",
        encoding="utf-8",
    )
    return task_path, brief_path


def run_code_task(
    *,
    task: Task,
    agent_command: str,
    timeout_seconds: float = 300,
    workdir: Path | None = None,
) -> CodeAgentRun:
    """Instantiate a starter, run one external coding agent, then evaluate its code."""

    resolved = instantiate_code_task(task, workdir=workdir)
    task_path, brief_path = write_code_task_files(task, resolved)
    env = os.environ.copy()
    env.update(
        {
            "WORKSPACE_BENCH_WORKDIR": str(resolved),
            "WORKSPACE_BENCH_TASK_BRIEF": str(brief_path),
            "WORKSPACE_BENCH_TASK_JSON": str(task_path),
            "WORKSPACE_BENCH_TASK_ID": task.id,
        }
    )
    timed_out = False
    exit_code: int | None
    stdout = ""
    stderr = ""
    try:
        completed = subprocess.run(
            agent_command,
            shell=True,
            cwd=resolved,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        exit_code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        exit_code = None
        stdout = _decode_output(error.stdout)
        stderr = _decode_output(error.stderr)
    evaluation = evaluate_code_repository(task, resolved)
    return CodeAgentRun(
        evaluation=evaluation,
        command=agent_command,
        exit_code=exit_code,
        timed_out=timed_out,
        stdout=_truncate(stdout),
        stderr=_truncate(stderr),
        task_path=task_path,
        brief_path=brief_path,
    )


def evaluate_code_repository(task: Task, workdir: Path) -> CodeEvaluation:
    """Install, start, probe, test, and reliably tear down an agent repository."""

    spec = _code_spec(task)
    checks: list[tuple[bool, CodeIssue]] = []
    probe_receipts: list[JsonDict] = []
    process: subprocess.Popen[str] | None = None
    port = _ephemeral_port()
    state_dir = workdir / ".workspace-bench"
    state_dir.mkdir(exist_ok=True)
    server_stdout = state_dir / "server.stdout.log"
    server_stderr = state_dir / "server.stderr.log"
    receipt: JsonDict = {
        "schema_version": CODE_RECEIPT_SCHEMA_VERSION,
        "task_ref": task.qualified_id,
        "workdir": str(workdir),
        "port": port,
        "install": {},
        "server": {},
        "manifests": {},
        "probes": probe_receipts,
        "tests": {},
        "cleanup": {},
    }

    def record(condition: bool, code: str, message: str) -> bool:
        checks.append((condition, CodeIssue(code=code, message=message)))
        return condition

    install = _run_argv(
        _expand_command(spec.install_command, workdir=workdir, port=port),
        cwd=workdir,
        timeout=spec.command_timeout_ms / 1000,
    )
    receipt["install"] = _command_receipt(install)
    installed = record(
        install.returncode == 0,
        "code_install_failed",
        f"dependency installation exited {install.returncode}: {_tail(install.stderr)}",
    )

    widgets: dict[str, JsonDict] = {}
    if installed:
        with server_stdout.open("w", encoding="utf-8") as stdout_handle, server_stderr.open(
            "w", encoding="utf-8"
        ) as stderr_handle:
            start_argv = _expand_command(spec.start_command, workdir=workdir, port=port)
            process = _start_process(
                start_argv,
                cwd=workdir,
                env={**os.environ, "WORKSPACE_BENCH_PORT": str(port)},
                stdout=stdout_handle,
                stderr=stderr_handle,
            )
            receipt["server"] = {"argv": start_argv, "pid": process.pid}
            started = _wait_for_health(
                f"http://127.0.0.1:{port}{spec.health_path}",
                process,
                timeout=spec.startup_timeout_ms / 1000,
            )
            record(
                started,
                "code_server_startup_failed",
                "backend did not become healthy before the startup deadline",
            )
            if started:
                widgets = _evaluate_manifests(
                    spec=spec,
                    port=port,
                    receipt=receipt,
                    record=record,
                )
                _evaluate_probes(
                    spec=spec,
                    widgets=widgets,
                    port=port,
                    receipt=receipt,
                    record=record,
                )
                _evaluate_repo_tests(
                    spec=spec,
                    workdir=workdir,
                    port=port,
                    receipt=receipt,
                    record=record,
                )

    terminated = True
    if process is not None:
        terminated = _terminate_process(process)
    receipt["cleanup"] = {
        "pid": process.pid if process is not None else None,
        "terminated": terminated,
        "orphan_process": not terminated,
    }
    record(terminated, "code_server_orphaned", "spawned backend process survived teardown")
    receipt["server"]["stdout_tail"] = _tail_file(server_stdout)
    receipt["server"]["stderr_tail"] = _tail_file(server_stderr)

    issues = tuple(issue for passed, issue in checks if not passed)
    passed_count = sum(passed for passed, _ in checks)
    grade = CodeGrade(
        score=passed_count / len(checks) if checks else 0.0,
        passed=not issues,
        checks_passed=passed_count,
        checks_total=len(checks),
        issues=issues,
    )
    receipt["grade"] = {
        "passed": grade.passed,
        "score": grade.score,
        "checks_passed": grade.checks_passed,
        "checks_total": grade.checks_total,
        "issues": [asdict(issue) for issue in issues],
    }
    (state_dir / "deployment-receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return CodeEvaluation(task=task, grade=grade, receipt=receipt, workdir=workdir)


def validate_code_tasks(tasks: list[Task], *, min_tasks: int = 1) -> JsonDict:
    """Certify starters, oracle overlays, teardown, and a focused mutation slice."""

    issues: list[JsonDict] = []
    oracle_passed = 0
    noop_failed = 0
    oracle_cleanup = True
    starter_cleanup = True
    oracle_probe_count = 0
    oracle_test_count = 0
    mutation_endpoint_removed = False
    mutation_placeholder = False

    if len(tasks) < min_tasks:
        issues.append(
            {
                "task_id": "benchmark",
                "message": f"expected at least {min_tasks} task(s), found {len(tasks)}",
            }
        )
    seen: set[str] = set()
    for task in tasks:
        if task.id in seen:
            issues.append({"task_id": task.id, "message": "duplicate code-task id"})
        seen.add(task.id)
        if task.code_task is None:
            issues.append({"task_id": task.id, "message": "missing code_task contract"})
            continue
        with tempfile.TemporaryDirectory(prefix=f"workspace-bench-cert-{task.id}-") as raw:
            workdir = Path(raw) / "repo"
            instantiate_code_task(task, workdir=workdir)
            starter = evaluate_code_repository(task, workdir)
            noop_failed += int(not starter.grade.passed)
            starter_cleanup = starter_cleanup and not bool(
                starter.receipt["cleanup"]["orphan_process"]
            )
            if starter.grade.passed:
                issues.append({"task_id": task.id, "message": "starter no-op unexpectedly passed"})

            apply_oracle_overlay(task, workdir)
            oracle = evaluate_code_repository(task, workdir)
            oracle_passed += int(oracle.grade.passed)
            oracle_cleanup = oracle_cleanup and not bool(
                oracle.receipt["cleanup"]["orphan_process"]
            )
            oracle_probe_count += sum(bool(item["passed"]) for item in oracle.receipt["probes"])
            oracle_test_count += int(oracle.receipt["tests"].get("test_count", 0))
            if not oracle.grade.passed:
                codes = ", ".join(issue.code for issue in oracle.grade.issues)
                issues.append(
                    {"task_id": task.id, "message": f"oracle overlay failed: {codes}"}
                )

            if task.id == "market_movers_table" and oracle.grade.passed:
                app_path = workdir / "app.py"
                original = app_path.read_text(encoding="utf-8")
                try:
                    removed = original.replace(
                        "@app.get('/movers')", "@app.get('/removed-movers')", 1
                    )
                    app_path.write_text(removed, encoding="utf-8")
                    removed_grade = evaluate_code_repository(task, workdir).grade
                    mutation_endpoint_removed = (
                        not removed_grade.passed
                        and any(
                            issue.code == "code_endpoint_unreachable"
                            for issue in removed_grade.issues
                        )
                    )
                    placeholder = original.replace(
                        "return MOVERS",
                        "return [{'symbol': 'TODO', 'change_pct': 0.0, 'volume': 1}]",
                        1,
                    )
                    app_path.write_text(placeholder, encoding="utf-8")
                    placeholder_grade = evaluate_code_repository(task, workdir).grade
                    mutation_placeholder = (
                        not placeholder_grade.passed
                        and any(
                            issue.code == "code_endpoint_placeholder"
                            for issue in placeholder_grade.issues
                        )
                    )
                finally:
                    app_path.write_text(original, encoding="utf-8")

    difficulties = {name: sum(task.difficulty == name for task in tasks) for name in (
        "easy",
        "medium",
        "hard",
    )}
    release_checks = {
        "task_count_is_12": len(tasks) == 12,
        "all_tasks_are_experimental_v0_code_tasks": all(
            task.code_task is not None and "experimental-v0" in task.tags for task in tasks
        ),
        "difficulty_spread_3_6_3": difficulties == {"easy": 3, "medium": 6, "hard": 3},
        "oracle_all_pass": oracle_passed == len(tasks),
        "starter_all_fail": noop_failed == len(tasks),
        "oracle_http_probes_all_pass": oracle_probe_count
        == sum(len(task.code_task.probes) for task in tasks if task.code_task is not None),
        "oracle_test_suites_non_empty": oracle_test_count >= len(tasks),
        "oracle_process_cleanup": oracle_cleanup,
        "starter_process_cleanup": starter_cleanup,
        "mutation_removed_endpoint_rejected": mutation_endpoint_removed,
        "mutation_placeholder_payload_rejected": mutation_placeholder,
    }
    for check_name, passed in release_checks.items():
        if not passed:
            issues.append(
                {"task_id": "benchmark", "message": f"release check failed: {check_name}"}
            )
    return {
        "passed": not issues,
        "task_count": len(tasks),
        "oracle_passed": oracle_passed,
        "noop_failed": noop_failed,
        "release_checks": release_checks,
        "oracle_probe_count": oracle_probe_count,
        "oracle_test_count": oracle_test_count,
        "issues": issues,
    }


def _evaluate_manifests(
    *,
    spec: CodeTaskSpec,
    port: int,
    receipt: JsonDict,
    record: Callable[[bool, str, str], bool],
) -> dict[str, JsonDict]:
    widgets_payload, widgets_error, widgets_cors = _http_json(
        port, "GET", "/widgets.json", {}, {}, spec.request_timeout_ms / 1000
    )
    widget_errors: list[str] = []
    widget_warnings: list[str] = []
    widgets: dict[str, JsonDict] = {}
    if widgets_error is None:
        widget_errors, widget_warnings, widgets = validate_widgets_json(widgets_payload)
    widget_ok = widgets_error is None and not widget_errors and not widget_warnings
    receipt["manifests"]["widgets"] = {
        "passed": widget_ok,
        "errors": ([widgets_error] if widgets_error else []) + widget_errors,
        "warnings": widget_warnings,
        "widget_ids": sorted(widgets),
    }
    record(widget_ok, "code_widgets_invalid", "widgets.json failed strict backend validation")
    record(widgets_cors, "code_cors_missing", "widgets.json did not expose a CORS allow-origin header")

    apps: list[JsonDict] = []
    if spec.require_apps:
        apps_payload, apps_error, apps_cors = _http_json(
            port, "GET", "/apps.json", {}, {}, spec.request_timeout_ms / 1000
        )
        app_errors: list[str] = []
        app_warnings: list[str] = []
        if apps_error is None:
            app_errors, app_warnings, apps = validate_apps_json(apps_payload, set(widgets))
        apps_ok = apps_error is None and not app_errors and not app_warnings and bool(apps)
        receipt["manifests"]["apps"] = {
            "passed": apps_ok,
            "errors": ([apps_error] if apps_error else []) + app_errors,
            "warnings": app_warnings,
            "app_ids": [app.get("template_id") for app in apps],
        }
        record(apps_ok, "code_apps_invalid", "apps.json failed strict backend validation")
        record(apps_cors, "code_cors_missing", "apps.json did not expose a CORS allow-origin header")

    declared: set[tuple[str, str]] = set()
    for definition in widgets.values():
        endpoint = definition.get("endpoint")
        if isinstance(endpoint, str):
            method = "POST" if definition.get("type") == "ssrm_table" else "GET"
            declared.add((method, endpoint))
        for param in flatten_params(definition, recurse=True):
            if param.get("type") == "form" and isinstance(param.get("endpoint"), str):
                declared.add((str(param.get("method", "POST")), str(param["endpoint"])))
    covered = {(probe.method, probe.path) for probe in spec.probes}
    record(
        bool(declared) and declared.issubset(covered),
        "code_probe_coverage_missing",
        f"declared manifest endpoints not covered by evaluator probes: {sorted(declared - covered)}",
    )
    return widgets


def _evaluate_probes(
    *,
    spec: CodeTaskSpec,
    widgets: dict[str, JsonDict],
    port: int,
    receipt: JsonDict,
    record: Callable[[bool, str, str], bool],
) -> None:
    for probe in spec.probes:
        payload, error, cors = _http_json(
            port,
            probe.method,
            probe.path,
            probe.query,
            probe.json_body,
            spec.request_timeout_ms / 1000,
        )
        code = "code_endpoint_unreachable"
        message = error or ""
        if error is None:
            message = _probe_payload_error(probe, payload, widgets)
            code = (
                "code_endpoint_placeholder"
                if contains_placeholder(payload)
                else "code_endpoint_incompatible"
            )
        passed = error is None and not message and cors
        if not cors and error is None and not message:
            code = "code_cors_missing"
            message = "response did not expose a CORS allow-origin header"
        item = {
            "name": probe.name,
            "method": probe.method,
            "path": probe.path,
            "widget_id": probe.widget_id,
            "passed": passed,
            "issue_code": None if passed else code,
            "message": message,
        }
        receipt["probes"].append(item)
        record(passed, code, f"{probe.name}: {message}")


def _probe_payload_error(
    probe: CodeProbe,
    payload: Any,
    widgets: dict[str, JsonDict],
) -> str:
    if contains_placeholder(payload):
        return "response contains placeholder data"
    if probe.widget_id is not None:
        definition = widgets.get(probe.widget_id)
        if definition is None:
            return f"widgets.json does not define {probe.widget_id!r}"
        shape_error = response_shape_error(definition, payload)
        if shape_error:
            return shape_error
    records = _payload_records(payload)
    if probe.minimum_items and len(records) < probe.minimum_items:
        return f"response contains {len(records)} item(s), expected at least {probe.minimum_items}"
    for field_name in probe.required_fields:
        values = _values_for_key(payload, field_name)
        if not values or all(value is None for value in values):
            return f"required field {field_name!r} is missing or null"
    for field_name, expected_type in probe.field_types.items():
        values = _values_for_key(payload, field_name)
        if not values or any(not _matches_type(value, str(expected_type)) for value in values):
            return f"field {field_name!r} does not have sane {expected_type} values"
    for field_name, expected in probe.expected_values.items():
        if expected not in _values_for_key(payload, field_name):
            return f"field {field_name!r} does not reflect requested value {expected!r}"
    return ""


def _evaluate_repo_tests(
    *,
    spec: CodeTaskSpec,
    workdir: Path,
    port: int,
    receipt: JsonDict,
    record: Callable[[bool, str, str], bool],
) -> None:
    junit = workdir / ".workspace-bench" / "pytest.xml"
    test_result = _run_argv(
        _expand_command(spec.test_command, workdir=workdir, port=port, junit=junit),
        cwd=workdir,
        timeout=spec.command_timeout_ms / 1000,
    )
    test_count, failures = _junit_counts(junit)
    tests_green = test_result.returncode == 0 and test_count > 0 and failures == 0
    receipt["tests"] = {
        "command": _command_receipt(test_result),
        "test_count": test_count,
        "failure_count": failures,
    }
    record(tests_green, "code_tests_failed", "repository pytest suite is not green and non-empty")

    mutation_rejected = False
    core_path = workdir / spec.core_module
    if tests_green and core_path.is_file():
        original = core_path.read_text(encoding="utf-8")
        mutation_junit = workdir / ".workspace-bench" / "pytest-mutation.xml"
        try:
            core_path.write_text(_garbage_fastapi_module(), encoding="utf-8")
            mutation_result = _run_argv(
                _expand_command(
                    spec.test_command,
                    workdir=workdir,
                    port=port,
                    junit=mutation_junit,
                ),
                cwd=workdir,
                timeout=spec.command_timeout_ms / 1000,
            )
            mutation_rejected = mutation_result.returncode != 0
            receipt["tests"]["garbage_mutation"] = _command_receipt(mutation_result)
        finally:
            core_path.write_text(original, encoding="utf-8")
    record(
        mutation_rejected,
        "code_tests_insensitive",
        "repository tests did not reject garbage endpoint logic",
    )
    receipt["tests"]["garbage_mutation_rejected"] = mutation_rejected


def _http_json(
    port: int,
    method: str,
    path: str,
    query: JsonDict,
    json_body: JsonDict,
    timeout: float,
) -> tuple[Any, str | None, bool]:
    suffix = f"?{urlencode(query, doseq=True)}" if query else ""
    url = f"http://127.0.0.1:{port}{path}{suffix}"
    data = json.dumps(json_body).encode("utf-8") if method == "POST" else None
    request = Request(url, data=data, method=method)
    request.add_header("Origin", "http://localhost")
    if data is not None:
        request.add_header("Content-Type", "application/json")
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read()
            cors = response.headers.get("Access-Control-Allow-Origin") is not None
            return json.loads(raw.decode("utf-8")), None, cors
    except HTTPError as error:
        return None, f"HTTP {error.code}", error.headers.get("Access-Control-Allow-Origin") is not None
    except (URLError, TimeoutError, OSError) as error:
        return None, f"request failed: {error}", False
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        return None, f"response is not valid JSON: {error}", False


def _wait_for_health(url: str, process: subprocess.Popen[str], *, timeout: float) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            return False
        try:
            with urlopen(url, timeout=0.25) as response:
                if 200 <= response.status < 300:
                    return True
        except (HTTPError, URLError, TimeoutError, OSError):
            pass
        time.sleep(0.05)
    return False


def _start_process(
    argv: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    stdout: Any,
    stderr: Any,
) -> subprocess.Popen[str]:
    kwargs: JsonDict = {"start_new_session": True} if os.name != "nt" else {}
    if os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    return subprocess.Popen(
        argv,
        cwd=cwd,
        env=env,
        stdout=stdout,
        stderr=stderr,
        text=True,
        **kwargs,
    )


def _terminate_process(process: subprocess.Popen[str]) -> bool:
    if process.poll() is None:
        try:
            if os.name == "nt":
                process.terminate()
            else:
                os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                process.kill()
            else:
                os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
        except ProcessLookupError:
            pass
    return process.poll() is not None


def _run_argv(argv: list[str], *, cwd: Path, timeout: float) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            argv,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        return subprocess.CompletedProcess(argv, 127, "", str(error))


def _expand_command(
    command: tuple[str, ...],
    *,
    workdir: Path,
    port: int,
    junit: Path | None = None,
) -> list[str]:
    python = workdir / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    values = {
        "workdir": str(workdir),
        "port": str(port),
        "python": str(python),
        "junit": str(junit or workdir / ".workspace-bench" / "pytest.xml"),
    }
    return [part.format(**values) for part in command]


def _command_receipt(result: subprocess.CompletedProcess[str]) -> JsonDict:
    return {
        "argv": list(result.args) if isinstance(result.args, (list, tuple)) else [str(result.args)],
        "exit_code": result.returncode,
        "stdout_tail": _tail(result.stdout),
        "stderr_tail": _tail(result.stderr),
    }


def _junit_counts(path: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return 0, 0
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    tests = sum(int(suite.attrib.get("tests", 0)) for suite in suites)
    failures = sum(
        int(suite.attrib.get("failures", 0)) + int(suite.attrib.get("errors", 0))
        for suite in suites
    )
    return tests, failures


def _payload_records(payload: Any) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("rows", "data", "items", "results"):
            if isinstance(payload.get(key), list):
                return list(payload[key])
        return [payload]
    return []


def _values_for_key(payload: Any, key: str) -> list[Any]:
    values: list[Any] = []
    if isinstance(payload, dict):
        if key in payload:
            values.append(payload[key])
        for value in payload.values():
            values.extend(_values_for_key(value, key))
    elif isinstance(payload, list):
        for value in payload:
            values.extend(_values_for_key(value, key))
    return values


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "string":
        return isinstance(value, str) and bool(value.strip())
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "object":
        return isinstance(value, dict) and bool(value)
    if expected == "array":
        return isinstance(value, list) and bool(value)
    return False


def _garbage_fastapi_module() -> str:
    return (
        "from fastapi import FastAPI\n\n"
        "app = FastAPI()\n\n"
        "@app.api_route('/{path:path}', methods=['GET', 'POST', 'PUT', 'OPTIONS'])\n"
        "def garbage(path: str):\n"
        "    return {'status': 'TODO'}\n"
    )


def _safe_fixture_path(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"code-task fixture escapes suite root: {relative}")
    return path


def _code_spec(task: Task) -> CodeTaskSpec:
    if task.code_task is None:
        raise ValueError(f"{task.qualified_id} is not a code task")
    return task.code_task


def _ephemeral_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _decode_output(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _truncate(value: str, max_chars: int = 4000) -> str:
    return value if len(value) <= max_chars else value[:max_chars] + "\n...[truncated]"


def _tail(value: str, max_chars: int = 1200) -> str:
    return value[-max_chars:]


def _tail_file(path: Path) -> str:
    return _tail(path.read_text(encoding="utf-8", errors="replace")) if path.exists() else ""
