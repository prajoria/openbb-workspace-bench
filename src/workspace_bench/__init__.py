"""OpenBB Workspace Bench package."""

from workspace_bench.core.episode import WorkspaceEpisode
from workspace_bench.core.models import BENCHMARK_RELEASE_ID, BENCHMARK_VERSION
from workspace_bench.core.runner import RunResult, TaskRunner

__version__ = BENCHMARK_VERSION
__release_id__ = BENCHMARK_RELEASE_ID

__all__ = [
    "RunResult",
    "TaskRunner",
    "WorkspaceEpisode",
    "__release_id__",
    "__version__",
]
