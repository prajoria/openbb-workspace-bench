"""Shared geometry helpers for Workspace dashboard and app layouts."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def rects_overlap(a: Mapping[str, Any], b: Mapping[str, Any]) -> bool:
    """Return whether two axis-aligned Workspace layout rectangles overlap."""

    try:
        ax, ay, aw, ah = (float(a.get(key, 0)) for key in ("x", "y", "w", "h"))
        bx, by, bw, bh = (float(b.get(key, 0)) for key in ("x", "y", "w", "h"))
    except (TypeError, ValueError):
        return False
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by
