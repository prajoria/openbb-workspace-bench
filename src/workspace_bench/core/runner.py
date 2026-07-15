"""Task loading and execution."""

from __future__ import annotations

import json
from dataclasses import replace
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path

from workspace_bench.agents import BenchAgent, build_agent
from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import RunResult, Task, TaskSuiteManifest
from workspace_bench.workspace.simulated_workspace import SimulatedWorkspace


USAGE_TASKS_PACKAGE = "workspace_bench.task_suites.enterprise_apps_usage"
BUILD_APPS_TASKS_PACKAGE = "workspace_bench.task_suites.build_openbb_apps"
APPS_DEFAULT_TASKS_PACKAGE = "workspace_bench.task_suites.enterprise_apps_default"
SMOKE_TASKS_PACKAGE = "workspace_bench.task_suites.smoke"
TASK_SUITE_MANIFEST = "task_suite.json"
BUILTIN_TASK_SUITES = {
    "enterprise-apps-usage": USAGE_TASKS_PACKAGE,
    "build-openbb-apps": BUILD_APPS_TASKS_PACKAGE,
    "enterprise-apps-default": APPS_DEFAULT_TASKS_PACKAGE,
    "smoke": SMOKE_TASKS_PACKAGE,
}
BUILTIN_TASK_SUITE_ORDER = (
    "enterprise-apps-usage",
    "enterprise-apps-default",
    "build-openbb-apps",
    "smoke",
)


def _resource_task_files(root: Traversable) -> list[Traversable]:
    """Return task JSON resources recursively, preserving filename ordering.

    Tasks live only in family subdirectories; JSON files at the suite root
    (the manifest, reference answer corpora, and other suite metadata) are
    never tasks.
    """

    files: list[Traversable] = []

    def visit(directory: Traversable, at_root: bool) -> None:
        for child in directory.iterdir():
            if child.is_dir():
                visit(child, False)
            elif not at_root and child.name.endswith(".json"):
                files.append(child)

    visit(root, True)
    return sorted(files, key=lambda path: path.name)


class TaskRunner:
    """Run Workspace Bench tasks against a simulated Workspace."""

    def __init__(self, workspace: SimulatedWorkspace | None = None):
        self.workspace = workspace or SimulatedWorkspace()

    def run(self, task: Task, agent: BenchAgent | str = "oracle") -> RunResult:
        if isinstance(agent, str):
            agent = build_agent(agent)

        episode = WorkspaceEpisode(task=task, workspace=self.workspace)
        for call in agent.tool_calls(task):
            episode.step(call)

        final_snapshot = episode.snapshot()
        grade = episode.grade()
        return RunResult(
            task=task,
            grade=grade,
            trace=tuple(episode.trace),
            final_snapshot=final_snapshot,
        )


def load_builtin_tasks(suite: str = "enterprise-apps-usage") -> list[Task]:
    """Load bundled JSON tasks for a named suite."""

    try:
        package = BUILTIN_TASK_SUITES[suite]
    except KeyError as error:
        available = ", ".join(BUILTIN_TASK_SUITE_ORDER)
        raise KeyError(f"Unknown built-in task suite {suite!r}. Available: {available}") from error
    task_files = _resource_task_files(resources.files(package))
    manifest = load_builtin_task_suite_manifest(suite)
    return [
        load_task_file(Path(str(path)), task_suite=manifest)
        for path in task_files
    ]


def load_builtin_task_suite_manifest(suite: str = "enterprise-apps-usage") -> TaskSuiteManifest | None:
    """Load a bundled task-suite manifest when one exists."""

    package = BUILTIN_TASK_SUITES[suite]
    manifest = resources.files(package) / TASK_SUITE_MANIFEST
    if not manifest.is_file():
        return None
    with manifest.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{manifest} must contain a JSON object")
    return TaskSuiteManifest.from_dict(payload)


def load_task_file(
    path: Path,
    task_suite: TaskSuiteManifest | None = None,
) -> Task:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if task_suite and task_suite.task_defaults:
        # Suite-wide labels apply only where the task file omits the field.
        defaults = dict(task_suite.task_defaults)
        eval_defaults = defaults.pop("eval", None)
        payload = {**defaults, **payload}
        if eval_defaults and isinstance(payload.get("eval"), dict):
            # Suite policy criteria (layout hygiene, trace discipline,
            # preservation) apply wherever the task's eval omits the key.
            payload = {
                **payload,
                "eval": {**eval_defaults, **payload["eval"]},
            }
    task = Task.from_dict(payload, source_path=path)
    return replace(task, suite=task_suite) if task_suite else task


def load_task_suite_manifest(path: Path) -> TaskSuiteManifest | None:
    manifest_path = path / TASK_SUITE_MANIFEST
    if not manifest_path.exists():
        return None
    with manifest_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{manifest_path} must contain a JSON object")
    return TaskSuiteManifest.from_dict(payload)


def load_task_directory(path: Path) -> list[Task]:
    if not path.exists():
        raise FileNotFoundError(f"task directory does not exist: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"task directory is not a directory: {path}")
    manifest = load_task_suite_manifest(path)
    # Tasks live only in family subdirectories; suite-root JSON files (the
    # manifest, reference answer corpora, and other metadata) are never tasks.
    task_paths = sorted(
        (
            candidate
            for candidate in path.rglob("*.json")
            if candidate.parent != path
        ),
        key=lambda candidate: candidate.name,
    )
    return [
        load_task_file(task_path, task_suite=manifest)
        for task_path in task_paths
    ]


def task_workspace_baseline(task: Task) -> str:
    """Return the explicit label for the baseline applied to a task."""

    if task.workspace_baseline is not None:
        return task.workspace_baseline or "minimal"
    if task.suite is None or not task.suite.workspace_baseline:
        return "minimal"
    return task.suite.workspace_baseline


def task_workspace_backends(task: Task) -> tuple[str, ...] | None:
    """Return the explicit backend set applied to a task, if any was chosen."""

    if task.workspace_backends is not None:
        return task.workspace_backends
    if task.suite is None:
        return None
    return task.suite.workspace_backends


def task_workspace_skills(task: Task) -> tuple[str, ...] | None:
    """Return the explicit skill selection applied to a task, if any."""

    if task.workspace_skills is not None:
        return task.workspace_skills
    if task.suite is None:
        return None
    return task.suite.workspace_skills


def tasks_workspace_baseline(tasks: list[Task]) -> str:
    """Return one baseline label for a task set, or ``mixed`` when needed."""

    baselines = {task_workspace_baseline(task) for task in tasks}
    if not baselines:
        return "minimal"
    if len(baselines) == 1:
        return baselines.pop()
    return "mixed"


def find_task(task_id: str, suite: str | None = None, family: str | None = None) -> Task:
    """Find a task by local id or ``suite/family/task`` reference."""

    parts = task_id.split("/")
    if len(parts) == 3:
        qualified_suite, qualified_family, task_id = parts
        if suite and suite != qualified_suite:
            raise KeyError(f"Task reference selects suite {qualified_suite!r}, not {suite!r}")
        suite, family = qualified_suite, qualified_family
    elif len(parts) != 1:
        raise KeyError(f"Invalid task reference {task_id!r}; expected suite/family/task")

    suites = (suite,) if suite else BUILTIN_TASK_SUITE_ORDER
    matches: list[Task] = []
    for name in suites:
        for task in load_builtin_tasks(name):
            if task.id == task_id and (family is None or task.family == family):
                matches.append(task)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        candidates = ", ".join(task.qualified_id for task in matches)
        raise KeyError(f"Ambiguous task {task_id!r}; use one of: {candidates}")
    raise KeyError(f"Unknown task {task_id!r}")
