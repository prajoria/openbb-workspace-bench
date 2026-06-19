"""Scenario loading and execution."""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path

from workspace_bench.agents import BenchAgent, build_agent
from workspace_bench.episode import WorkspaceEpisode
from workspace_bench.models import (
    RunResult,
    Scenario,
    TaskPackManifest,
)
from workspace_bench.simulated_workspace import SimulatedWorkspace


SCENARIO_PACKAGE = "workspace_bench.core.scenarios"
TASK_PACK_MANIFEST = "task_pack.json"


class ScenarioRunner:
    """Run Workspace Bench scenarios against a simulated Workspace."""

    def __init__(self, workspace: SimulatedWorkspace | None = None):
        self.workspace = workspace or SimulatedWorkspace()

    def run(self, scenario: Scenario, agent: BenchAgent | str = "oracle") -> RunResult:
        if isinstance(agent, str):
            agent = build_agent(agent)

        episode = WorkspaceEpisode(scenario=scenario, workspace=self.workspace)
        for call in agent.tool_calls(scenario):
            episode.step(call)

        final_snapshot = episode.snapshot()
        grade = episode.grade()
        return RunResult(
            scenario=scenario,
            grade=grade,
            trace=tuple(episode.trace),
            final_snapshot=final_snapshot,
        )


def load_builtin_scenarios() -> list[Scenario]:
    """Load bundled JSON scenarios."""

    scenario_files = sorted(resources.files(SCENARIO_PACKAGE).glob("*.json"))
    return [load_scenario_file(Path(path)) for path in scenario_files]


def load_scenario_file(path: Path, default_split: str = "dev") -> Scenario:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return Scenario.from_dict(payload, source_path=path, default_split=default_split)


def load_task_pack_manifest(path: Path) -> TaskPackManifest | None:
    manifest_path = path / TASK_PACK_MANIFEST
    if not manifest_path.exists():
        return None
    with manifest_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{manifest_path} must contain a JSON object")
    return TaskPackManifest.from_dict(payload)


def load_scenario_directory(path: Path) -> list[Scenario]:
    if not path.exists():
        raise FileNotFoundError(f"scenario directory does not exist: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"scenario directory is not a directory: {path}")
    manifest = load_task_pack_manifest(path)
    default_split = manifest.default_split if manifest else "dev"
    scenario_paths = sorted(
        candidate for candidate in path.glob("*.json") if candidate.name != TASK_PACK_MANIFEST
    )
    return [
        load_scenario_file(scenario_path, default_split=default_split)
        for scenario_path in scenario_paths
    ]


def find_scenario(scenario_id: str) -> Scenario:
    for scenario in load_builtin_scenarios():
        if scenario.id == scenario_id:
            return scenario
    raise KeyError(f"Unknown scenario {scenario_id!r}")
