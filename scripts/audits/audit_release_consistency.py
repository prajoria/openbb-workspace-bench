#!/usr/bin/env python3
"""Audit release-facing counts and terminology for cross-phase drift."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from workspace_bench.core.adversarial import ADVERSARIAL_ARCHETYPES
from workspace_bench.core.runner import BUILTIN_TASK_SUITES

REPO = Path(__file__).resolve().parents[2]
TASK_SUITE_ROOT = REPO / "src/workspace_bench/task_suites"
BUILTIN_SUITE_READMES = {
    suite: TASK_SUITE_ROOT / package.rsplit(".", 1)[-1] / "README.md"
    for suite, package in BUILTIN_TASK_SUITES.items()
}

AUDITED_FILES = (
    REPO / "README.md",
    REPO / "CONTRIBUTING.md",
    REPO / "RELEASE_CHECKLIST.md",
    REPO / "pyproject.toml",
    REPO / ".github/workflows/ci.yml",
    REPO / "src/workspace_bench/cli.py",
    REPO / "runs/README.md",
    REPO / "runs/reports/task-catalog.md",
    REPO / "runs/reports/tool-coverage-matrix.md",
    *BUILTIN_SUITE_READMES.values(),
    *sorted((REPO / "tests").glob("test_*.py")),
)

# These generated tables contain ordinal row numbers and task payload examples,
# so historical count tokens are not release-count claims there.
COUNT_SCAN_EXCLUSIONS = {
    REPO / "runs/reports/task-catalog.md",
    REPO / "runs/reports/tool-coverage-matrix.md",
}

STALE_COUNT_RE = re.compile(r"\b(?:212|512)\b|60/80/72")
STALE_CLAIMS = {
    "exact completion notes": re.compile(r"exact completion notes", re.IGNORECASE),
    "runtime_verification_denial": re.compile(r"no runtime verification", re.IGNORECASE),
    "hand-assigned difficulty": re.compile(
        r"difficulty\s+(?:is|remains)\s+hand[- ]assigned", re.IGNORECASE
    ),
    "browser_harness_outdated": re.compile(
        r"(?:future browser(?: runner)?|no browser harness)", re.IGNORECASE
    ),
}

NUMBER_WORDS = (
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
    "twenty",
)
ARCHETYPE_COUNT = len(ADVERSARIAL_ARCHETYPES)
ARCHETYPE_COUNT_WORD = NUMBER_WORDS[ARCHETYPE_COUNT - 1]
ARCHETYPE_COUNT_RE = re.compile(
    rf"\b(?P<count>\d+|{'|'.join(NUMBER_WORDS)})\s+"
    r"(?:adversarial(?:-candidate)?\s+)?archetypes?\b",
    re.IGNORECASE,
)
SUITE_TASK_COUNT_RE = re.compile(r"^Tasks: (?P<count>\d+)$", re.MULTILINE)
SUITE_TERMINOLOGY_RE = re.compile(
    r"\b(?:scenarios?|collections?|tiers?|packs?|authoring)\b", re.IGNORECASE
)

REQUIRED_FACTS = {
    REPO / "README.md": (
        "338 deterministic simulator tasks",
        f"{ARCHETYPE_COUNT_WORD} archetypes",
    ),
    REPO / "RELEASE_CHECKLIST.md": (
        "338 tasks",
    ),
    REPO / "runs/README.md": (
        "GPT-5.1, GPT-5.4 mini, and GPT-5.5",
    ),
    REPO / "src/workspace_bench/cli.py": (
        "operating the workspace (120).",
    ),
}


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    reason: str


def audit_text(path: Path, content: str) -> list[Finding]:
    """Return stale-count and stale-claim findings for one file."""

    findings: list[Finding] = []
    in_archived_readme = False
    for line_number, line in enumerate(content.splitlines(), start=1):
        if path.name == "README.md" and line == "## Archived Baselines":
            in_archived_readme = True
        elif path.name == "README.md" and line == "## Evaluate Your Agent":
            in_archived_readme = False
        scan_line = "tests" not in path.parts or "assert" in line
        if (
            scan_line
            and path not in COUNT_SCAN_EXCLUSIONS
            and STALE_COUNT_RE.search(line)
            and not in_archived_readme
        ):
            findings.append(Finding(path, line_number, f"stale active count: {line.strip()}"))
        for label, pattern in STALE_CLAIMS.items():
            if not scan_line:
                continue
            if pattern.search(line):
                findings.append(Finding(path, line_number, f"stale claim ({label})"))
        for match in ARCHETYPE_COUNT_RE.finditer(line) if scan_line else ():
            raw_count = match.group("count").lower()
            parsed_count = (
                int(raw_count)
                if raw_count.isdigit()
                else NUMBER_WORDS.index(raw_count) + 1
            )
            if parsed_count != ARCHETYPE_COUNT:
                findings.append(
                    Finding(
                        path,
                        line_number,
                        "wrong adversarial archetype count: "
                        f"{raw_count} (expected {ARCHETYPE_COUNT_WORD})",
                    )
                )
    return findings


def audit_release_consistency() -> list[Finding]:
    """Audit all release-facing files and required canonical facts."""

    findings: list[Finding] = []
    for path in AUDITED_FILES:
        if not path.is_file():
            findings.append(Finding(path, 0, "required release-facing file is missing"))
            continue
        content = path.read_text(encoding="utf-8")
        findings.extend(audit_text(path, content))
        if path in BUILTIN_SUITE_READMES.values():
            for line_number, line in enumerate(content.splitlines(), start=1):
                if SUITE_TERMINOLOGY_RE.search(line):
                    findings.append(
                        Finding(path, line_number, f"non-canonical suite terminology: {line.strip()}")
                    )
    for suite, readme in BUILTIN_SUITE_READMES.items():
        if not readme.is_file():
            continue
        content = readme.read_text(encoding="utf-8")
        match = SUITE_TASK_COUNT_RE.search(content)
        if match is None:
            findings.append(Finding(readme, 0, "missing required `Tasks: <N>` line"))
            continue
        # Suite-root JSON (manifest, reference answer corpora) is metadata,
        # not a task; tasks live only in family subdirectories.
        actual = sum(
            path.parent != readme.parent for path in readme.parent.rglob("*.json")
        )
        stated = int(match.group("count"))
        if stated != actual:
            findings.append(
                Finding(
                    readme,
                    content[: match.start()].count("\n") + 1,
                    f"stated task count {stated} does not match {actual} files for {suite}",
                )
            )
    for path, required in REQUIRED_FACTS.items():
        content = path.read_text(encoding="utf-8")
        for fact in required:
            if fact not in content:
                findings.append(Finding(path, 0, f"missing canonical fact: {fact}"))
    return findings


def main() -> int:
    findings = audit_release_consistency()
    for finding in findings:
        relative = finding.path.relative_to(REPO)
        print(f"{relative}:{finding.line}: {finding.reason}")
    if findings:
        print(f"FAIL: {len(findings)} release consistency finding(s)")
        return 1
    print(f"PASS: 0 release consistency findings across {len(AUDITED_FILES)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
