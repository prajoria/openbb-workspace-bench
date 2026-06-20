"""OpenBB Workspace Bench package."""

from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.rl.env import WorkspaceGymEnv
from workspace_bench.core.models import BENCHMARK_RELEASE_ID, BENCHMARK_VERSION
from workspace_bench.core.runner import RunResult, ScenarioRunner

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
