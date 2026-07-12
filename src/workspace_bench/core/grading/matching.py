"""Value matching rules shared by grading sections."""

from __future__ import annotations

import re

from workspace_bench.core.models import JsonDict


STOPWORDS = {"a", "an", "and", "for", "of", "the"}


def meaningful_tokens(text: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in STOPWORDS]


def normalized_text(text: str) -> str:
    return " ".join(meaningful_tokens(text.replace("_", " ")))


def phrase_matches(actual: str, expected: str) -> bool:
    actual_lower = actual.lower()
    expected_lower = expected.lower()
    if expected_lower in actual_lower:
        return True
    actual_tokens = meaningful_tokens(actual_lower)
    expected_tokens = meaningful_tokens(expected_lower)
    if not expected_tokens:
        return False
    index = 0
    for token in actual_tokens:
        if index < len(expected_tokens) and token == expected_tokens[index]:
            index += 1
    return index == len(expected_tokens)


def _normalized_render_fns(value: object) -> list[str]:
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    if isinstance(value, list):
        return [str(part).strip() for part in value]
    return []


def subset_matches(spec: JsonDict, candidate: JsonDict) -> bool:
    # Definition specs describe one flat param/column/group record. Unlike
    # data_args they stay shallow, while renderFn accepts equivalent list and
    # comma-separated representations and therefore needs set containment.
    for key, expected in spec.items():
        if key == "renderFn":
            expected_fns = set(_normalized_render_fns(expected))
            if expected_fns - set(_normalized_render_fns(candidate.get(key))):
                return False
            continue
        if candidate.get(key) != expected:
            return False
    return True
