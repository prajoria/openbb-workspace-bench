"""Shared naming helpers for Workspace entities."""

from __future__ import annotations

import re


def slugify(value: str, *, fallback: str = "app") -> str:
    """Convert a display name to a lowercase slug with a caller-selected fallback."""

    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or fallback
