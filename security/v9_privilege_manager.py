"""
JARVIS V9 - Privilege Manager

Detects the effective Windows privilege level of the current JARVIS
process.

This module does not:
- request elevation
- bypass Windows security
- modify permissions
- execute privileged operations

It only reports the current process privilege state.
"""

from __future__ import annotations

import ctypes
import os

from security.v9_security_model import SecurityPrivilegeLevel


class V9PrivilegeManager:
    """Detect the current Windows privilege level."""

    def get_current_privilege(self) -> SecurityPrivilegeLevel:
        """Return the effective privilege level of the current process."""

        if os.name != "nt":
            return SecurityPrivilegeLevel.USER

        if self._is_system():
            return SecurityPrivilegeLevel.SYSTEM

        if self._is_administrator():
            return SecurityPrivilegeLevel.ADMINISTRATOR

        return SecurityPrivilegeLevel.USER

    @staticmethod
    def _is_administrator() -> bool:
        """Return True when the process has administrator privileges."""
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except (AttributeError, OSError):
            return False

    @staticmethod
    def _is_system() -> bool:
        """Return True when the current account is LocalSystem."""
        try:
            username = os.environ.get("USERNAME", "")
            return username.strip().upper() == "SYSTEM"
        except Exception:
            return False
