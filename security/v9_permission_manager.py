"""
JARVIS V9 - Permission Manager

Manages whether JARVIS is permitted to use a defined capability.

This module does not:
- execute system operations
- request Windows elevation
- modify Windows permissions
- modify files or registry
- bypass security boundaries

It only stores and evaluates JARVIS-level capability permissions.
"""

from __future__ import annotations


class V9PermissionManager:
    """Manage owner-controlled JARVIS capability permissions."""

    def __init__(self) -> None:
        self._permissions: dict[str, bool] = {}

    def set_permission(self, capability: str, allowed: bool) -> None:
        """Set whether a capability is permitted."""
        if not isinstance(capability, str):
            raise TypeError("capability must be a string")

        capability = capability.strip()

        if not capability:
            raise ValueError("capability cannot be empty")

        if not isinstance(allowed, bool):
            raise TypeError("allowed must be a boolean")

        self._permissions[capability] = allowed

    def is_allowed(self, capability: str) -> bool:
        """Return whether a capability is explicitly allowed."""
        if not isinstance(capability, str):
            raise TypeError("capability must be a string")

        capability = capability.strip()

        if not capability:
            raise ValueError("capability cannot be empty")

        return self._permissions.get(capability, False)

    def is_configured(self, capability: str) -> bool:
        """Return whether a capability has an explicit permission entry."""
        if not isinstance(capability, str):
            raise TypeError("capability must be a string")

        capability = capability.strip()

        if not capability:
            raise ValueError("capability cannot be empty")

        return capability in self._permissions

    def remove_permission(self, capability: str) -> bool:
        """Remove a configured permission and return whether it existed."""
        if not isinstance(capability, str):
            raise TypeError("capability must be a string")

        capability = capability.strip()

        if not capability:
            raise ValueError("capability cannot be empty")

        return self._permissions.pop(capability, None) is not None

    def get_permissions(self) -> dict[str, bool]:
        """Return a copy of the configured permissions."""
        return dict(self._permissions)
