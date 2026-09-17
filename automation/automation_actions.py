"""
JARVIS V8 - Automation Actions

Defines the controlled action types available to the
Personal Automation system.

This module does not execute actions.
"""

from enum import Enum


class AutomationAction(str, Enum):
    """Approved actions that an automation may contain."""

    OPEN_APP = "OPEN_APP"
    OPEN_FILE = "OPEN_FILE"
    OPEN_FOLDER = "OPEN_FOLDER"
    OPEN_URL = "OPEN_URL"

    CREATE_FILE = "CREATE_FILE"
    CREATE_FOLDER = "CREATE_FOLDER"

    MOVE_FILE = "MOVE_FILE"
    COPY_FILE = "COPY_FILE"
    RENAME_FILE = "RENAME_FILE"

    WAIT = "WAIT"


def is_valid_action(action: str) -> bool:
    """Return True when the action is an approved automation action."""
    if not isinstance(action, str):
        return False

    return action.strip().upper() in {
        item.value for item in AutomationAction
    }
