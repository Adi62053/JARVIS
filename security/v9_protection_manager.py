"""
JARVIS V9.11 - Protected System Operations

Resource classification layer for privileged system operations.

This module:
- classifies resources by protection level
- identifies protected Windows/system resources
- does not modify resources
- does not execute privileged operations
- does not bypass Windows security
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path


class ProtectionLevel(str, Enum):
    ORDINARY = "ORDINARY"
    SENSITIVE = "SENSITIVE"
    CRITICAL = "CRITICAL"
    PROTECTED = "PROTECTED"


class V9ProtectionManager:
    """Classify system resources before privileged operations."""

    _PROTECTED_PATHS = (
        Path(r"C:\Windows\System32"),
        Path(r"C:\Windows\SysWOW64"),
        Path(r"C:\Windows\Boot"),
        Path(r"C:\Windows\WinSxS"),
    )

    _CRITICAL_PATHS = (
        Path(r"C:\Windows"),
        Path(r"C:\Program Files"),
        Path(r"C:\Program Files (x86)"),
        Path(r"C:\ProgramData"),
    )

    _SENSITIVE_PATHS = (
        Path(r"C:\Users"),
        Path(r"C:\$Recycle.Bin"),
    )

    _CRITICAL_PROCESS_NAMES = {
        "system",
        "smss.exe",
        "csrss.exe",
        "wininit.exe",
        "services.exe",
        "lsass.exe",
        "winlogon.exe",
        "explorer.exe",
    }

    _CRITICAL_SERVICE_NAMES = {
        "eventlog",
        "rpcss",
        "samss",
        "winmgmt",
        "windefend",
    }

    def classify_path(self, resource: str) -> ProtectionLevel:
        """Classify a filesystem path."""

        if not isinstance(resource, str):
            raise TypeError("resource must be a string")

        resource = resource.strip()

        if not resource:
            raise ValueError("resource must not be empty")

        path = Path(resource)

        for protected in self._PROTECTED_PATHS:
            if self._is_same_or_child(path, protected):
                return ProtectionLevel.PROTECTED

        for critical in self._CRITICAL_PATHS:
            if self._is_same_or_child(path, critical):
                return ProtectionLevel.CRITICAL

        for sensitive in self._SENSITIVE_PATHS:
            if self._is_same_or_child(path, sensitive):
                return ProtectionLevel.SENSITIVE

        return ProtectionLevel.ORDINARY

    def classify_process(self, process_name: str) -> ProtectionLevel:
        """Classify a process name."""

        if not isinstance(process_name, str):
            raise TypeError("process_name must be a string")

        name = process_name.strip().lower()

        if not name:
            raise ValueError("process_name must not be empty")

        if name in self._CRITICAL_PROCESS_NAMES:
            return ProtectionLevel.PROTECTED

        return ProtectionLevel.ORDINARY

    def classify_service(self, service_name: str) -> ProtectionLevel:
        """Classify a Windows service name."""

        if not isinstance(service_name, str):
            raise TypeError("service_name must be a string")

        name = service_name.strip().lower()

        if not name:
            raise ValueError("service_name must not be empty")

        if name in self._CRITICAL_SERVICE_NAMES:
            return ProtectionLevel.PROTECTED

        return ProtectionLevel.ORDINARY

    def is_protected(self, level: ProtectionLevel) -> bool:
        """Return whether a protection level is PROTECTED."""

        if not isinstance(level, ProtectionLevel):
            raise TypeError("level must be a ProtectionLevel")

        return level == ProtectionLevel.PROTECTED

    def requires_extra_protection(self, level: ProtectionLevel) -> bool:
        """Return whether a resource needs additional security handling."""

        if not isinstance(level, ProtectionLevel):
            raise TypeError("level must be a ProtectionLevel")

        return level in {
            ProtectionLevel.SENSITIVE,
            ProtectionLevel.CRITICAL,
            ProtectionLevel.PROTECTED,
        }

    @staticmethod
    def _is_same_or_child(
        path: Path,
        parent: Path,
    ) -> bool:
        """Return True when path is parent itself or inside parent."""

        try:
            path = path.resolve(strict=False)
            parent = parent.resolve(strict=False)
        except OSError:
            path = Path(str(path))
            parent = Path(str(parent))

        try:
            path.relative_to(parent)
            return True
        except ValueError:
            return False
