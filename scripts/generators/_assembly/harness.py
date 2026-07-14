"""Policy-driven assembly machinery shared by WorkspaceBench suite generators.

These helpers deliberately live under ``scripts``: they author bundled data but
are not part of the runtime package. Suite policy (identity cleanup, categories,
and suite-specific artifacts) is supplied through callbacks
instead of being copied into parallel harnesses.
"""

from __future__ import annotations

import hashlib
import re
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

Task = dict[str, Any]
CellCounts = dict[tuple[str, str], int]

# The shipped task-file schema. Generators author richer intermediate payloads
# (titles, taxonomy, novelty rationales) for their own asserts and reports;
# only this projection is written to disk.
TASK_EXPORT_FIELDS = (
    "id",
    "category",
    "family",
    "specification_level",
    "difficulty",
    "prompt",
    "business_terms",
    "fixtures",
    "initial_state",
    "allowed_tools",
    "success",
    "oracle_tool_calls",
    "limits",
)
DEFAULT_SPECIFICATION_LEVEL = {
    "easy": "explicit",
    "medium": "partially-specified",
    "hard": "open-brief",
}
# July 2026 guided calibration p95s were 13 calls for passing
# partially-specified attempts and 14 for open briefs. These rung budgets are
# intentionally independent of any one oracle architecture; the oracle-derived
# budget remains only a safety floor.
FLEXIBLE_RUNG_TURN_BUDGETS = {
    "r0": 8,
    "r1": 13,
    "r2": 13,
    "r3": 14,
    "r4": 14,
}


def slim_task_payload(task: Task) -> Task:
    """Project one authored task onto the shipped task-file schema."""

    payload = {key: task[key] for key in TASK_EXPORT_FIELDS if key in task}
    if payload.get("specification_level") == DEFAULT_SPECIFICATION_LEVEL.get(
        str(payload.get("difficulty"))
    ):
        payload.pop("specification_level", None)
    if not payload.get("business_terms"):
        payload.pop("business_terms", None)
    return payload


def diversify_generated_widget_proof(
    task: Task, *, share: int = 4, selected_buckets: int = 1
) -> None:
    """Deterministically turn roughly one ``note`` proof in ``share`` into HTML.

    HTML remains a natural semantic evidence card for the same business facts,
    but prevents the benchmark from teaching one memorized proof mechanism.
    """

    required = task.get("success", {}).get("required_generated_widgets", [])
    bucket = int(hashlib.sha256(str(task["id"]).encode()).hexdigest(), 16) % share
    if not required or bucket >= selected_buckets:
        return
    converted = False
    for item in required:
        if item.get("widget_type") == "note":
            item["widget_type"] = "html"
            converted = True
            break
    if not converted:
        return
    for call in task.get("oracle_tool_calls", []):
        args = call.get("args", {})
        if call.get("tool") == "add_generative_widget" and args.get("widget_type") == "note":
            args["widget_type"] = "html"
            if isinstance(args.get("data"), str):
                args["data"] = f"<section>{args['data']}</section>"
            break
    prompt = str(task.get("prompt", ""))
    prompt = re.sub(r"\bnotes\b", "HTML cards", prompt, flags=re.IGNORECASE)
    prompt = re.sub(r"\bnote\b", "HTML card", prompt, flags=re.IGNORECASE)
    task["prompt"] = prompt
CategorySetter = Callable[[Task, str], None]
IdentityNormalizer = Callable[[Task], None]
TaskStage = Callable[[Task, str, str, int], None]
DifficultySetter = Callable[[Task, str, str, int], None]
TagPrefixes = Callable[[str, str, int], Sequence[str]]
ArtifactParts = Callable[[Task], list[str]]
TaskInspector = Callable[[Task], Any]


def difficulty_for(level: str, cell_index: int) -> str:
    """Map a structural rung and its one-based cell index to a difficulty band."""

    if level == "r0":
        return "easy"
    if level == "r1":
        return "easy" if cell_index <= 2 else "medium"
    if level == "r2":
        return "medium"
    if level == "r3":
        return "medium" if cell_index <= 2 else "hard"
    return "hard"


def snap() -> Task:
    """Return the canonical Workspace snapshot tool call."""

    return {"tool": "get_workspace_snapshot", "args": {}}


def build_matrix(tasks: Sequence[Task]) -> dict[str, dict[str, int]]:
    """Count authored tasks by private family and rung coordinates."""

    matrix: dict[str, dict[str, int]] = {}
    for task in tasks:
        family, level = task["_family"], task["_rung"]
        matrix.setdefault(family, {})[level] = matrix.setdefault(family, {}).get(level, 0) + 1
    return matrix


@dataclass
class PhrasingSelector:
    """Select deterministic prompt variants and audit each source prompt pool."""

    pool_sizes: dict[str, int]
    normalize_id: Callable[[str], str] = lambda task_id: task_id

    def __call__(self, task_id: str, variants: list[str]) -> str:
        assert isinstance(variants, list), f"{task_id} prompt pool must be a list"
        assert len(variants) >= 3, f"{task_id} prompt pool has {len(variants)} variants"
        frame = sys._getframe(1)
        site = f"{Path(frame.f_code.co_filename).name}:{frame.f_lineno}"
        previous = self.pool_sizes.setdefault(site, len(variants))
        assert previous == len(variants), (
            f"prompt site {site} used pool sizes {previous} and {len(variants)}"
        )
        stable_id = self.normalize_id(task_id)
        index = int(hashlib.md5(stable_id.encode()).hexdigest(), 16) % len(variants)
        return variants[index]


@dataclass
class TaskAssembler:
    """Apply common task metadata and ordered suite policy stages."""

    scenarios: list[Task]
    cell_counts: CellCounts
    source: str
    rung_slack: Mapping[str, int]
    set_category: CategorySetter
    normalize_identity: IdentityNormalizer
    after_identity: TaskStage
    set_difficulty: DifficultySetter
    tag_prefixes: TagPrefixes
    finalize_task: TaskStage

    def add(self, family: str, level: str, task: Task) -> None:
        self.cell_counts[(family, level)] = self.cell_counts.get((family, level), 0) + 1
        cell_index = self.cell_counts[(family, level)]
        task.setdefault("domain", "finance")
        task.setdefault("source", self.source)
        self.set_category(task, family)
        task["family"] = family
        self.normalize_identity(task)
        assert re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", task["id"]), task["id"]
        self.after_identity(task, family, level, cell_index)
        self.set_difficulty(task, family, level, cell_index)
        tags = task.setdefault("tags", [])
        tags[0:0] = self.tag_prefixes(family, level, cell_index)
        self.finalize_task(task, family, level, cell_index)
        oracle_floor = len(task["oracle_tool_calls"]) + self.rung_slack[level]
        specification_level = str(task.get("specification_level", "explicit"))
        task.setdefault("limits", {})["max_turns"] = (
            oracle_floor
            if specification_level == "explicit"
            else max(FLEXIBLE_RUNG_TURN_BUDGETS[level], oracle_floor)
        )
        task["_family"], task["_rung"] = family, level
        self.scenarios.append(task)


@dataclass(frozen=True)
class CheckTypePolicy:
    """Extract grader issue kinds while retaining suite-specific check policy."""

    success_checks: Mapping[str, str]
    widget_mode: Literal["collection", "cardinality"]
    within_grid_default: bool
    max_invalid_tool_calls_default: int | None
    include_forbid_invented_widget_ids: bool = False

    def __call__(self, task: Task) -> tuple[str, ...]:
        success = task.get("success", {})
        kinds = {
            kind for key, kind in self.success_checks.items() if success.get(key)
        }
        required_widgets = success.get("required_widgets", [])
        if self.widget_mode == "collection":
            if required_widgets:
                kinds.add("missing_widget")
        else:
            for requirement in required_widgets:
                if int(requirement.get("min_count", 1)) > 0:
                    kinds.add("missing_widget")
                if requirement.get("max_count") is not None:
                    kinds.add("too_many_widgets")
        if success.get("required_dashboard_name_contains"):
            kinds.add("dashboard_name")
        layout = success.get("layout", {})
        if layout.get("within_grid", self.within_grid_default):
            kinds.add("layout_out_of_grid")
        if layout.get("no_overlaps"):
            kinds.add("layout_overlap")
        trace = success.get("trace_checks", {})
        if (
            trace.get(
                "max_invalid_tool_calls", self.max_invalid_tool_calls_default
            )
            is not None
        ):
            kinds.add("too_many_invalid_calls")
        if trace.get("must_call_schema_before_create"):
            kinds.add("schema_not_called_before_create")
        if (
            self.include_forbid_invented_widget_ids
            and trace.get("forbid_invented_widget_ids")
        ):
            kinds.add("unlisted_widget_id")
        if trace.get("max_repeated_snapshots") is not None:
            kinds.add("repeated_snapshots")
        return tuple(sorted(kinds))


@dataclass(frozen=True)
class ArtifactDiscriminator:
    """Build a stable artifact identity from suite-specific and common parts."""

    leading_parts: ArtifactParts
    include_layouts: bool = False

    def __call__(self, task: Task) -> str:
        success = task.get("success", {})
        parts = self.leading_parts(task)
        widgets = [
            f"{req.get('origin')}/{req.get('widget_id')}@{req.get('tab_id', '*')}"
            for req in success.get("required_widgets", [])
            if int(req.get("min_count", 1)) > 0
        ]
        if widgets:
            parts.append("widgets:" + ",".join(sorted(widgets)))
        if self.include_layouts:
            layouts = [
                ":".join(
                    str(req.get(key, ""))
                    for key in ("widget_id", "widget_uuid", "tab_id", "x", "y", "w", "h")
                )
                for req in success.get("required_layouts", [])
            ]
            if layouts:
                parts.append("layouts:" + ",".join(sorted(layouts)))
        tabs = success.get("required_tabs", [])
        if tabs:
            parts.append("tabs:" + ",".join(sorted(tabs)))
        generated = [
            f"{req.get('widget_type')}@{req.get('tab_id', '*')}:"
            f"{','.join(req.get('data_contains', [])[:2])}"
            for req in success.get("required_generated_widgets", [])
        ]
        if generated:
            parts.append("generated:" + ",".join(sorted(generated)))
        if not parts:
            parts.append("id:" + task["id"])
        return "|".join(parts)


@dataclass(frozen=True)
class NoveltyPolicy:
    """Fingerprint tasks and render their human-readable novelty rationale."""

    check_types: TaskInspector
    task_backends: TaskInspector
    artifact_discriminator: TaskInspector
    exercise_label: str = "exercise"

    def fingerprint(self, task: Task) -> tuple[Any, ...]:
        oracle_tools = tuple(sorted({call["tool"] for call in task["oracle_tool_calls"]}))
        return (
            task["_family"],
            task["_rung"],
            oracle_tools,
            self.check_types(task),
            tuple(sorted(self.task_backends(task))),
            self.artifact_discriminator(task),
        )

    def add_description(self, task: Task) -> None:
        tools = ", ".join(sorted({call["tool"] for call in task["oracle_tool_calls"]}))
        checks = ", ".join(self.check_types(task))
        backends = ", ".join(sorted(self.task_backends(task))) or "no preloaded backend"
        artifact = self.artifact_discriminator(task).replace("|", "; ")
        task["novelty"] = (
            f"Unique {task['_family']}/{task['id']} {self.exercise_label} using "
            f"{tools} with checks {checks} on {backends}; artifact {artifact}."
        )
