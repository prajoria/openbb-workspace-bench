"""Shared generator-time assembly helpers for WorkspaceBench task suites."""

from .harness import (
    ArtifactDiscriminator,
    CheckTypePolicy,
    NoveltyPolicy,
    PhrasingSelector,
    SplitAssigner,
    TaskAssembler,
    build_matrix,
    difficulty_for,
    snap,
    uniform_four_way_pattern,
)

__all__ = [
    "ArtifactDiscriminator",
    "CheckTypePolicy",
    "NoveltyPolicy",
    "PhrasingSelector",
    "SplitAssigner",
    "TaskAssembler",
    "build_matrix",
    "difficulty_for",
    "snap",
    "uniform_four_way_pattern",
]
