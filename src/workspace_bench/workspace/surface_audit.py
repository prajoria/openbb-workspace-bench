"""Compatibility checks for live Workspace MCP tool schemas."""

from __future__ import annotations


def compare_tool_schemas(expected: dict, observed: dict) -> list[str]:
    """Report backwards-incompatible input-schema changes.

    Additive optional arguments are accepted. Removing an accepted property,
    adding a required argument, or changing an existing property's schema is a
    release-blocking drift.
    """

    issues: list[str] = []
    for tool_name, expected_schema in expected.items():
        observed_schema = observed.get(tool_name)
        if observed_schema is None:
            continue
        if not isinstance(expected_schema, dict) or not isinstance(observed_schema, dict):
            issues.append(f"{tool_name}: schema must be an object")
            continue
        expected_properties = expected_schema.get("properties") or {}
        observed_properties = observed_schema.get("properties") or {}
        for property_name, property_schema in expected_properties.items():
            if property_name not in observed_properties:
                issues.append(f"{tool_name}.{property_name}: accepted argument was removed")
                continue
            if not _schema_accepts_previous(
                property_schema, observed_properties[property_name]
            ):
                issues.append(f"{tool_name}.{property_name}: schema shape changed")
        added_required = set(observed_schema.get("required") or []) - set(
            expected_schema.get("required") or []
        )
        for property_name in sorted(added_required):
            issues.append(f"{tool_name}.{property_name}: argument became required")
    return issues


def _schema_shape(value: object) -> object:
    if isinstance(value, list):
        return [_schema_shape(item) for item in value]
    if not isinstance(value, dict):
        return value
    ignored = {"title", "description", "default", "examples"}
    return {key: _schema_shape(item) for key, item in sorted(value.items()) if key not in ignored}


def _schema_accepts_previous(previous: object, current: object) -> bool:
    """Return true when every value accepted before remains accepted now."""

    previous_shape = _schema_shape(previous)
    current_shape = _schema_shape(current)
    if previous_shape == current_shape:
        return True
    if not isinstance(previous_shape, dict) or not isinstance(current_shape, dict):
        return False
    for union_key in ("anyOf", "oneOf"):
        current_union = current_shape.get(union_key)
        if isinstance(current_union, list):
            return any(
                _schema_accepts_previous(previous_shape, branch)
                for branch in current_union
            )
    previous_type = previous_shape.get("type")
    current_type = current_shape.get("type")
    if isinstance(current_type, list) and previous_type in current_type:
        return True
    previous_enum = previous_shape.get("enum")
    current_enum = current_shape.get("enum")
    if isinstance(previous_enum, list) and isinstance(current_enum, list):
        return set(previous_enum) <= set(current_enum)
    return False
