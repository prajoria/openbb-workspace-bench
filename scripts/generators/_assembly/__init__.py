"""Shared generator-time assembly helpers for WorkspaceBench task suites."""

from .harness import (
    ArtifactDiscriminator,
    CheckTypePolicy,
    NoveltyPolicy,
    PhrasingSelector,
    TaskAssembler,
    build_matrix,
    difficulty_for,
    diversify_generated_widget_proof,
    slim_task_payload,
    snap,
)

__all__ = [
    "ArtifactDiscriminator",
    "CheckTypePolicy",
    "NoveltyPolicy",
    "PhrasingSelector",
    "TaskAssembler",
    "build_matrix",
    "difficulty_for",
    "diversify_generated_widget_proof",
    "slim_task_payload",
    "snap",
]
