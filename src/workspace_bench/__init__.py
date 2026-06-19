"""OpenBB Workspace Bench package."""

from workspace_bench.episode import WorkspaceEpisode
from workspace_bench.envs import WorkspaceGymEnv
from workspace_bench.models import BENCHMARK_RELEASE_ID, BENCHMARK_VERSION
from workspace_bench.runner import RunResult, ScenarioRunner

__version__ = BENCHMARK_VERSION
__release_id__ = BENCHMARK_RELEASE_ID

__all__ = [
    "RunResult",
    "ScenarioRunner",
    "WorkspaceEpisode",
    "WorkspaceGymEnv",
    "__release_id__",
    "__version__",
]
