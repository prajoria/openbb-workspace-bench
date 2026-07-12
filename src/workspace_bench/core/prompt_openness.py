"""Difficulty-aware checks for implementation details leaked into build prompts."""

from __future__ import annotations

from dataclasses import dataclass
import re

from workspace_bench.core.models import JsonDict, Task
from workspace_bench.workspace.widget_params import flatten_params


@dataclass(frozen=True)
class PromptOpennessIssue:
    """One prompt-contract violation."""

    code: str
    detail: str


def _definitions(payload: JsonDict) -> tuple[list[tuple[str, JsonDict]], list[JsonDict]]:
    widgets: list[tuple[str, JsonDict]] = []
    apps: list[JsonDict] = []
    for call in payload.get("oracle_tool_calls", []):
        if not isinstance(call, dict) or call.get("tool") != "manage_backends":
            continue
        args = call.get("args") or {}
        for widget_id, definition in (args.get("widgets_json") or {}).items():
            if isinstance(definition, dict):
                widgets.append((str(widget_id), definition))
        apps.extend(app for app in (args.get("apps_json") or []) if isinstance(app, dict))
    for backend in (payload.get("initial_state") or {}).get("custom_backends", []) or []:
        if not isinstance(backend, dict):
            continue
        for widget_id, definition in (backend.get("widgets_json") or {}).items():
            if isinstance(definition, dict):
                widgets.append((str(widget_id), definition))
        apps.extend(app for app in (backend.get("apps_json") or []) if isinstance(app, dict))
    return widgets, apps


def _duration_phrases(milliseconds: object) -> set[str]:
    if not isinstance(milliseconds, (int, float)):
        return set()
    value = int(milliseconds)
    phrases = {str(value)}
    if value % 60000 == 0:
        amount = value // 60000
        phrases.update({f"{amount} minute", f"{amount}-minute"})
    elif value % 1000 == 0:
        amount = value // 1000
        phrases.update({f"{amount} second", f"{amount}-second"})
    return phrases


def _implementation_identifiers(payload: JsonDict) -> list[tuple[str, str]]:
    widgets, apps = _definitions(payload)
    identifiers: set[tuple[str, str]] = set()
    for widget_id, definition in widgets:
        identifiers.add(("widget id", widget_id))
        widget_type = definition.get("type")
        if widget_type:
            identifiers.add(("widget type", str(widget_type)))
        for key in ("endpoint", "wsEndpoint"):
            if definition.get(key):
                identifiers.add(("endpoint path", str(definition[key])))
        for key in ("staleTime", "refetchInterval"):
            for phrase in _duration_phrases(definition.get(key)):
                identifiers.add(("refresh interval", phrase))
        for param in flatten_params(definition, recurse=True):
            param_name = str(param.get("paramName", ""))
            if "_" in param_name:
                identifiers.add(("parameter id", param_name))
            for key in ("endpoint", "optionsEndpoint"):
                if param.get(key):
                    identifiers.add(("endpoint path", str(param[key])))
        columns = ((definition.get("data") or {}).get("table") or {}).get("columnsDefs") or []
        for column in columns:
            field = str(column.get("field", "")) if isinstance(column, dict) else ""
            if "_" in field:
                identifiers.add(("snake_case column field", field))
    for app in apps:
        if app.get("name"):
            identifiers.add(("app name", str(app["name"])))
        if app.get("template_id"):
            identifiers.add(("app id", str(app["template_id"])))
    for call in payload.get("oracle_tool_calls", []):
        if not isinstance(call, dict) or call.get("tool") != "manage_backends":
            continue
        args = call.get("args") or {}
        if args.get("name"):
            identifiers.add(("backend name", str(args["name"])))
        if args.get("url"):
            identifiers.add(("backend URL", str(args["url"])))
    return sorted(identifiers)


def _masked_prompt(prompt: str, terms: list[str]) -> str:
    masked = prompt.casefold()
    for term in sorted(terms, key=len, reverse=True):
        masked = masked.replace(term.casefold(), " " * len(term))
    return masked


def _contains_identifier(prompt: str, identifier: str) -> bool:
    escaped = re.escape(identifier.casefold())
    if re.fullmatch(r"[a-z0-9_]+", identifier.casefold()):
        return re.search(rf"(?<![a-z0-9_]){escaped}(?![a-z0-9_])", prompt) is not None
    return identifier.casefold() in prompt


def prompt_openness_issues(payload: JsonDict) -> list[PromptOpennessIssue]:
    """Return openness violations for one raw task payload."""

    specification_level = str(payload.get("specification_level", ""))
    if not specification_level:
        specification_level = {
            "easy": "explicit",
            "medium": "partially-specified",
            "hard": "open-brief",
        }.get(str(payload.get("difficulty", "")), "")
    if specification_level == "explicit":
        return []
    prompt = str(payload.get("prompt", ""))
    raw_terms = payload.get("business_terms", [])
    if not isinstance(raw_terms, list) or not all(
        isinstance(term, str) and term.strip() for term in raw_terms
    ):
        return [PromptOpennessIssue("business_terms_invalid", "must be non-empty strings")]
    terms = [term.strip() for term in raw_terms]
    issues: list[PromptOpennessIssue] = []
    if len({term.casefold() for term in terms}) != len(terms):
        issues.append(PromptOpennessIssue("business_terms_duplicate", "terms must be unique"))
    for term in terms:
        if term.casefold() not in prompt.casefold():
            issues.append(
                PromptOpennessIssue(
                    "business_term_not_in_prompt", f"declared term {term!r} is absent"
                )
            )
    masked = _masked_prompt(prompt, terms)
    for kind, identifier in _implementation_identifiers(payload):
        if identifier and _contains_identifier(masked, identifier):
            issues.append(
                PromptOpennessIssue("implementation_identifier_leak", f"{kind} {identifier!r}")
            )
    if specification_level == "open-brief" and re.search(
        r"(?:\{|,)\s*[\"']?[xywh][\"']?\s*[:=]\s*\d+", prompt, re.IGNORECASE
    ):
        issues.append(PromptOpennessIssue("layout_coordinate_leak", "explicit x/y/w/h coordinate"))
    if specification_level == "open-brief" and re.search(
        r"\btabs?\b", masked, re.IGNORECASE
    ):
        issues.append(PromptOpennessIssue("tab_name_leak", "prompt names an app tab"))
    return issues


def task_prompt_openness_issues(task: Task) -> list[PromptOpennessIssue]:
    """Adapt a loaded task to the raw-payload openness check."""

    payload: JsonDict = {
        "specification_level": task.specification_level,
        "prompt": task.prompt,
        "business_terms": list(task.business_terms),
        "initial_state": task.initial_state,
        "oracle_tool_calls": [
            {"tool": call.name, "args": call.args} for call in task.oracle_tool_calls
        ],
    }
    return prompt_openness_issues(payload)
