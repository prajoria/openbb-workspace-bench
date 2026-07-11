"""Task loading and execution."""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path

from workspace_bench.agents import BenchAgent, build_agent
from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import RunResult, Task, TaskSuiteManifest
from workspace_bench.workspace.simulated_workspace import SimulatedWorkspace


WORKSPACE_BENCH_V1_PACKAGE = "workspace_bench.core.task_suites.workspace_bench_v1"
WORKSPACE_BENCH_V2_BUILD_APPS_PACKAGE = (
    "workspace_bench.core.task_suites.workspace_bench_v2_build_openbb_apps"
)
TASK_SUITE_MANIFEST = "task_suite.json"
BUILTIN_TASK_SUITES = {
    "core": WORKSPACE_BENCH_V1_PACKAGE,
    "build-openbb-apps": WORKSPACE_BENCH_V2_BUILD_APPS_PACKAGE,
}
BUILTIN_TASK_SUITE_ORDER = ("core", "build-openbb-apps")


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


def load_builtin_tasks(suite: str = "core") -> list[Task]:
    """Load bundled JSON tasks for a named suite."""

    if suite == "all":
        return load_builtin_tasks("core")
    try:
        package = BUILTIN_TASK_SUITES[suite]
    except KeyError as error:
        available = ", ".join(BUILTIN_TASK_SUITE_ORDER)
        raise KeyError(f"Unknown built-in task suite {suite!r}. Available: {available}") from error
    task_files = sorted(
        path
        for path in resources.files(package).glob("*.json")
        if path.name != TASK_SUITE_MANIFEST
    )
    manifest = load_builtin_task_suite_manifest(suite)
    default_split = manifest.default_split if manifest else "dev"
    return [load_task_file(Path(path), default_split=default_split) for path in task_files]


def load_builtin_task_suite_manifest(suite: str = "core") -> TaskSuiteManifest | None:
    """Load a bundled task-suite manifest when one exists."""

    if suite == "all":
        return load_builtin_task_suite_manifest("core")
    package = BUILTIN_TASK_SUITES[suite]
    manifest = resources.files(package) / TASK_SUITE_MANIFEST
    if not manifest.is_file():
        return None
    with manifest.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{manifest} must contain a JSON object")
    return TaskSuiteManifest.from_dict(payload)


def load_task_file(path: Path, default_split: str = "dev") -> Task:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return Task.from_dict(payload, source_path=path, default_split=default_split)


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
    default_split = manifest.default_split if manifest else "dev"
    task_paths = sorted(
        candidate for candidate in path.glob("*.json") if candidate.name != TASK_SUITE_MANIFEST
    )
    return [
        load_task_file(task_path, default_split=default_split)
        for task_path in task_paths
    ]


def find_task(task_id: str, suite: str = "all") -> Task:
    for task in load_builtin_tasks(suite):
        if task.id == task_id:
            return task
    raise KeyError(f"Unknown task {task_id!r}")
