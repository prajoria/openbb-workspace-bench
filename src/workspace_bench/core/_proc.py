"""Shared helpers for captured subprocess output."""

from __future__ import annotations

from typing import Any


def decode_output(value: Any) -> str:
    """Normalize optional text or byte subprocess output to text."""

    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def truncate_output(value: str, max_chars: int = 4000) -> str:
    """Limit captured subprocess output while marking truncated values."""

    if len(value) <= max_chars:
        return value
    return value[:max_chars] + "\n...[truncated]"
