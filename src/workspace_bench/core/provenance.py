"""Repository and task-content provenance helpers."""

from __future__ import annotations

import subprocess
from pathlib import Path

from workspace_bench.core.models import JsonDict


def git_provenance(
    start: Path | None = None,
    source_paths: list[Path] | None = None,
) -> JsonDict:
    """Describe the checked-out source without a hand-maintained release number."""

    cwd = start or Path.cwd()
    if cwd.is_file():
        cwd = cwd.parent
    try:
        root = _git(cwd, "rev-parse", "--show-toplevel")
        root_path = Path(root)
        commit = _git(root_path, "rev-parse", "HEAD")
        dirty = bool(_git(root_path, "status", "--porcelain"))
    except (OSError, subprocess.CalledProcessError):
        return {"git_commit": None, "git_dirty": None, "source_git_commit": None}
    source_commit = None
    if source_paths:
        relative_paths = [
            str(path.resolve().relative_to(root_path))
            for path in source_paths
            if path.exists() and path.resolve().is_relative_to(root_path)
        ]
        if relative_paths:
            try:
                source_commit = _git(
                    root_path,
                    "log",
                    "-1",
                    "--format=%H",
                    "--",
                    *relative_paths,
                ) or None
            except (OSError, subprocess.CalledProcessError):
                source_commit = None
    return {
        "git_commit": commit,
        "git_dirty": dirty,
        "source_git_commit": source_commit,
    }


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
