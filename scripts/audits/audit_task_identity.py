#!/usr/bin/env python3
"""Audit public task identities, titles, prompts, and documentation references.

Usage:
    uv run python scripts/audits/audit_task_identity.py
    uv run python scripts/audits/audit_task_identity.py --json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from workspace_bench.core.prompt_openness import prompt_openness_issues

REPO = Path(__file__).resolve().parents[2]
SUITE_DIRS = {
    "core": REPO / "src/workspace_bench/core/task_suites/core",
    "build-openbb-apps": REPO / "src/workspace_bench/core/task_suites/build_openbb_apps",
    "build-openbb-backends": (
        REPO / "src/workspace_bench/core/task_suites/build_openbb_backends"
    ),
}
REFERENCE_FILES = (
    REPO / "README.md",
    REPO / "RELEASE_CHECKLIST.md",
    REPO / ".github/workflows/ci.yml",
    *sorted((REPO / "docs").glob("*.md")),
)

TOKEN_RE = re.compile(r"[a-z0-9]+")
TASK_ID_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
NUMERIC_SCAR_RE = re.compile(r"_\d+$")
JARGON_RE = re.compile(
    r"(?i)(?:\br[0-4]\b|\bt[0-4]\b|\bgen_|\bfam_|\boracle\b|\bgrader\b|"
    r"\brubric\b|check cap|\bmutation\b)"
)
PLACEHOLDER_RE = re.compile(
    r"(?i)(?:\{\{[^{}]+\}\}|\$\{[^{}]+\}|<placeholder>|\[(?:todo|tbd)\]|"
    r"\b(?:todo|tbd|xxx)\b)"
)
REPEATED_WORD_RE = re.compile(r"(?i)\b([a-z][a-z0-9-]*)\s+\1\b")
REPEATED_BIGRAM_RE = re.compile(r"(?i)\b([a-z][a-z0-9-]*\s+[a-z][a-z0-9-]*)\s+\1\b")
TASK_ARG_RE = re.compile(r"--task\s+([^\s`\"']+)")
QUALIFIED_ID_RE = re.compile(
    r"\b(?:core|build-openbb-apps|build-openbb-backends)/"
    r"[a-z0-9]+(?:[-_][a-z0-9]+)*/"
    r"[a-z0-9]+(?:_[a-z0-9]+)*\b"
)
LEGACY_ID_RE = re.compile(r"\bgen_[a-z0-9_]+\b")


@dataclass(frozen=True)
class Finding:
    suite: str
    family: str
    task_id: str
    field: str
    reason: str


def repeated_token_phrase(tokens: list[str]) -> str | None:
    """Return an immediately repeated one-to-three-token phrase, if present."""

    for width in (3, 2, 1):
        for start in range(len(tokens) - 2 * width + 1):
            phrase = tokens[start : start + width]
            if phrase == tokens[start + width : start + 2 * width]:
                return "_".join(phrase)
    return None


def _add(
    findings: list[Finding],
    *,
    suite: str,
    family: str,
    task_id: str,
    field: str,
    reason: str,
) -> None:
    findings.append(Finding(suite, family, task_id, field, reason))


def audit_task(suite: str, family: str, task: dict[str, Any]) -> list[Finding]:
    """Return identity and prose findings for one generated task."""

    findings: list[Finding] = []
    task_id = str(task.get("id", ""))
    title = str(task.get("title", ""))
    prompt = str(task.get("prompt", ""))
    id_tokens = task_id.split("_")
    title_tokens = TOKEN_RE.findall(title.lower())

    if not TASK_ID_RE.fullmatch(task_id):
        _add(
            findings,
            suite=suite,
            family=family,
            task_id=task_id,
            field="id",
            reason="not a lowercase underscore slug",
        )
    if len(task_id) > 64:
        _add(
            findings,
            suite=suite,
            family=family,
            task_id=task_id,
            field="id",
            reason=f"length {len(task_id)} exceeds 64 characters",
        )
    if len(id_tokens) >= 10:
        _add(
            findings,
            suite=suite,
            family=family,
            task_id=task_id,
            field="id",
            reason=f"triple-compounded slug has {len(id_tokens)} tokens",
        )
    if repeated := repeated_token_phrase(id_tokens):
        _add(
            findings,
            suite=suite,
            family=family,
            task_id=task_id,
            field="id",
            reason=f"repeated token phrase: {repeated}",
        )
    if NUMERIC_SCAR_RE.search(task_id) and not task_id.endswith("client_360"):
        _add(
            findings,
            suite=suite,
            family=family,
            task_id=task_id,
            field="id",
            reason="numeric generator suffix",
        )

    if "  " in title or re.search(r"\s+[,;:]", title):
        _add(
            findings,
            suite=suite,
            family=family,
            task_id=task_id,
            field="title",
            reason="spacing scar",
        )
    if re.search(r"(?:\||/|:|;|,)\s*$", title):
        _add(
            findings,
            suite=suite,
            family=family,
            task_id=task_id,
            field="title",
            reason="dangling separator",
        )
    if repeated := repeated_token_phrase(title_tokens):
        _add(
            findings,
            suite=suite,
            family=family,
            task_id=task_id,
            field="title",
            reason=f"repeated word phrase: {repeated.replace('_', ' ')}",
        )

    prompt_checks = (
        (JARGON_RE, "internal benchmark jargon"),
        (PLACEHOLDER_RE, "placeholder residue"),
        (REPEATED_BIGRAM_RE, "repeated bigram"),
        (REPEATED_WORD_RE, "repeated word"),
        (re.compile(r" {2,}|\s+[,;:.]|(?:;;|,,|::)"), "spacing or join scar"),
    )
    for pattern, reason in prompt_checks:
        if match := pattern.search(prompt):
            _add(
                findings,
                suite=suite,
                family=family,
                task_id=task_id,
                field="prompt",
                reason=f"{reason}: {match.group(0)!r}",
            )
    for identifier in re.findall(r"\b[a-z0-9]+(?:_[a-z0-9]+){2,}\b", prompt):
        if repeated := repeated_token_phrase(identifier.split("_")):
            _add(
                findings,
                suite=suite,
                family=family,
                task_id=task_id,
                field="prompt",
                reason=f"machine-glued identifier repeats: {repeated}",
            )
            break
    return findings


def audit_prompt_openness(suite: str, family: str, task: dict[str, Any]) -> list[Finding]:
    """Return specification-aware implementation-leak findings for build tasks."""

    if suite != "build-openbb-apps":
        return []
    return [
        Finding(
            suite,
            family,
            str(task.get("id", "")),
            "prompt",
            f"{issue.code}: {issue.detail}",
        )
        for issue in prompt_openness_issues(task)
    ]


def load_tasks() -> list[tuple[str, str, dict[str, Any]]]:
    tasks: list[tuple[str, str, dict[str, Any]]] = []
    for suite, directory in SUITE_DIRS.items():
        for path in sorted(directory.glob("*/*.json")):
            task = json.loads(path.read_text())
            tasks.append((suite, str(task.get("family", path.parent.name)), task))
    return tasks


def audit_references(tasks: list[tuple[str, str, dict[str, Any]]]) -> list[Finding]:
    """Find documented task references that do not resolve uniquely."""

    qualified = {f"{suite}/{family}/{task['id']}" for suite, family, task in tasks}
    families = {(suite, family) for suite, family, _ in tasks}
    local_counts = Counter(str(task["id"]) for _, _, task in tasks)
    findings: list[Finding] = []
    for path in REFERENCE_FILES:
        text = path.read_text()
        references = set(TASK_ARG_RE.findall(text))
        references.update(
            reference
            for reference in QUALIFIED_ID_RE.findall(text)
            if tuple(reference.split("/", 2)[:2]) in families
        )
        references.update(LEGACY_ID_RE.findall(text))
        for reference in sorted(references):
            if "/" in reference:
                valid = reference in qualified
            else:
                valid = local_counts[reference] == 1
            if not valid:
                findings.append(
                    Finding(
                        "references",
                        str(path.relative_to(REPO)),
                        reference,
                        "task_id",
                        "does not resolve to exactly one bundled task",
                    )
                )
    return findings


def run_audit() -> list[Finding]:
    tasks = load_tasks()
    findings = [
        finding
        for suite, family, task in tasks
        for finding in (
            audit_task(suite, family, task) + audit_prompt_openness(suite, family, task)
        )
    ]
    prompts = Counter(str(task["prompt"]) for _, _, task in tasks)
    for suite, family, task in tasks:
        if prompts[str(task["prompt"])] > 1:
            findings.append(
                Finding(
                    suite,
                    family,
                    str(task["id"]),
                    "prompt",
                    "prompt is not unique across bundled tasks",
                )
            )
    findings.extend(audit_references(tasks))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON findings.")
    args = parser.parse_args()
    task_count = len(load_tasks())
    findings = run_audit()
    if args.json:
        print(json.dumps([asdict(finding) for finding in findings], indent=2))
    elif findings:
        for finding in findings:
            print(
                f"{finding.suite}/{finding.family}/{finding.task_id}: "
                f"{finding.field}: {finding.reason}"
            )
        print(f"FAIL: {len(findings)} finding(s) across {task_count} tasks")
    else:
        print(f"PASS: 0 findings across {task_count} tasks")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
