"""Harbor adapter for Workspace Bench.

The adapter keeps Workspace Bench tasks and graders canonical. Generated
Harbor tasks contain a sealed task bundle, run the real Workspace MCP sidecar,
and return a trusted episode artifact to a separate verifier.
"""

from workspace_bench.integrations.harbor.bundle import load_sealed_task
from workspace_bench.integrations.harbor.exporter import export_harbor_task

__all__ = ["export_harbor_task", "load_sealed_task"]

