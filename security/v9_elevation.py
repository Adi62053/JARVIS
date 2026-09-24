"""
JARVIS V9 - Windows Privilege / Elevation Layer

Detection-only privilege boundary for V9.

This module:
- identifies whether the current privilege is sufficient
- identifies when elevation is required
- does not perform elevation
- does not bypass Windows security
- does not modify system state
"""

from __future__ import annotations

from security.v9_privilege_manager import V9PrivilegeManager
from security.v9_security_model import SecurityPrivilegeLevel


class V9ElevationManager:
    """Detect whether an operation requires additional privilege."""

    _PRIVILEGE_ORDER = {
        SecurityPrivilegeLevel.USER: 0,
        SecurityPrivilegeLevel.ADMINISTRATOR: 1,
        SecurityPrivilegeLevel.SYSTEM: 2,
        SecurityPrivilegeLevel.FIRMWARE: 3,
        SecurityPrivilegeLevel.HARDWARE: 4,
    }

    def __init__(
        self,
        privilege_manager: V9PrivilegeManager | None = None,
    ) -> None:
        self.privilege_manager = (
            privilege_manager or V9PrivilegeManager()
        )

    def get_current_privilege(self) -> SecurityPrivilegeLevel:
        """Return the privilege detected for the current process."""

        return self.privilege_manager.get_current_privilege()

    def requires_elevation(
        self,
        required_privilege: SecurityPrivilegeLevel,
    ) -> bool:
        """
        Return True when the requested privilege exceeds the
        current process privilege.
        """

        if not isinstance(
            required_privilege,
            SecurityPrivilegeLevel,
        ):
            raise TypeError(
                "required_privilege must be a SecurityPrivilegeLevel"
            )

        current_privilege = self.get_current_privilege()

        current_level = self._PRIVILEGE_ORDER[current_privilege]
        required_level = self._PRIVILEGE_ORDER[required_privilege]

        return required_level > current_level

    def can_access(
        self,
        required_privilege: SecurityPrivilegeLevel,
    ) -> bool:
        """Return whether the current privilege meets the requirement."""

        return not self.requires_elevation(required_privilege)

    def get_status(
        self,
        required_privilege: SecurityPrivilegeLevel,
    ) -> dict[str, str | bool]:
        """Return a structured privilege comparison."""

        if not isinstance(
            required_privilege,
            SecurityPrivilegeLevel,
        ):
            raise TypeError(
                "required_privilege must be a SecurityPrivilegeLevel"
            )

        current_privilege = self.get_current_privilege()
        elevation_required = self.requires_elevation(
            required_privilege
        )

        return {
            "current_privilege": current_privilege.value,
            "required_privilege": required_privilege.value,
            "elevation_required": elevation_required,
            "access_available": not elevation_required,
        }
