"""Canonical Workspace tool surface used by tasks, runners, and audits."""

from __future__ import annotations


WORKSPACE_TOOL_NAMES = (
    "get_workspace_snapshot",
    "manage_dashboard",
    "manage_navigation_bar",
    "navigate_workspace",
    "list_available_widgets",
    "get_widget_schema",
    "get_params_options",
    "get_widget_data",
    "create_widget",
    "update_widget",
    "update_widget_layout",
    "delete_widget",
    "add_generative_widget",
    "read_widget",
    "manage_backends",
    "manage_apps",
    "get_skill_content",
    "read_workspace_resource",
    "get_workspace_prompt",
    "assign_tasks_to_agents",
)

WORKSPACE_TOOL_NAME_SET = frozenset(WORKSPACE_TOOL_NAMES)
