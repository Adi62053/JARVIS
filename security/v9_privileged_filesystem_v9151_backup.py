"""
JARVIS V9.15 - Privileged Filesystem Security Layer

Provides security classification and validation for filesystem resources.

This module does not execute filesystem operations.
It does not request elevation.
It does not bypass Windows security.

Actual authorization remains the responsibility of the existing
V9 security pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from security.v9_protection_manager import (
    ProtectionLevel,
    V9ProtectionManager,
)
from security.v9_security_model import (
    SecurityPrivilegeLevel,
    SecurityRiskLevel,
)


@dataclass(frozen=True)
class FilesystemSecurityInfo:
    """Security information for one filesystem resource."""

    path: str
    exists: bool
    is_file: bool
    is_directory: bool
    protection_level: ProtectionLevel
    required_privilege: SecurityPrivilegeLevel
    risk_level: SecurityRiskLevel


class V9PrivilegedFilesystem:
    """
    Security/resource validation layer for privileged filesystem access.

    This class does not perform filesystem mutations.
    """

    _OPERATIONS = frozenset(
        {
            "READ",
            "WRITE",
            "CREATE",
            "MODIFY",
            "DELETE",
            "RENAME",
            "COPY",
            "MOVE",
        }
    )

    def __init__(
        self,
        *,
        protection_manager: V9ProtectionManager | None = None,
    ) -> None:
        self.protection_manager = (
            protection_manager or V9ProtectionManager()
        )

    @staticmethod
    def normalize_path(path: str | Path) -> Path:
        """Normalize a filesystem path without requiring it to exist."""

        if isinstance(path, Path):
            candidate = path
        elif isinstance(path, str):
            if not path.strip():
                raise ValueError("path cannot be empty")
            candidate = Path(path.strip().strip('"'))
        else:
            raise TypeError("path must be a string or Path")

        return candidate.expanduser().resolve(strict=False)

    def classify_path(self, path: str | Path) -> ProtectionLevel:
        """Return the V9 protection classification for a filesystem path."""

        normalized = self.normalize_path(path)
        return self.protection_manager.classify_path(str(normalized))

    def is_protected(self, path: str | Path) -> bool:
        """Return True when the path is V9 protected."""

        level = self.classify_path(path)
        return self.protection_manager.is_protected(level)

    def get_required_privilege(
        self,
        path: str | Path,
        operation: str,
    ) -> SecurityPrivilegeLevel:
        """
        Determine the minimum V9 privilege boundary for an operation.

        This method only describes the required boundary.
        It does not elevate the current process.
        """

        operation_name = self._normalize_operation(operation)
        level = self.classify_path(path)

        if level == ProtectionLevel.PROTECTED:
            return SecurityPrivilegeLevel.SYSTEM

        if level == ProtectionLevel.CRITICAL:
            return SecurityPrivilegeLevel.ADMINISTRATOR

        if level == ProtectionLevel.SENSITIVE:
            if operation_name in {"DELETE", "MOVE", "MODIFY", "WRITE"}:
                return SecurityPrivilegeLevel.ADMINISTRATOR
            return SecurityPrivilegeLevel.USER

        if operation_name in {"DELETE", "MOVE", "MODIFY"}:
            return SecurityPrivilegeLevel.USER

        return SecurityPrivilegeLevel.USER

    def get_risk_level(
        self,
        path: str | Path,
        operation: str,
    ) -> SecurityRiskLevel:
        """Determine the security risk classification of an operation."""

        operation_name = self._normalize_operation(operation)
        level = self.classify_path(path)

        if level == ProtectionLevel.PROTECTED:
            return SecurityRiskLevel.CRITICAL

        if level == ProtectionLevel.CRITICAL:
            return SecurityRiskLevel.HIGH

        if operation_name in {"DELETE", "MOVE", "MODIFY", "WRITE"}:
            return SecurityRiskLevel.HIGH

        if operation_name in {"CREATE", "RENAME", "COPY"}:
            return SecurityRiskLevel.CAUTION

        return SecurityRiskLevel.SAFE

    def validate_source(
        self,
        path: str | Path,
        *,
        require_exists: bool = True,
    ) -> Path:
        """
        Validate a source filesystem path.

        No filesystem modification is performed.
        """

        normalized = self.normalize_path(path)

        if require_exists and not normalized.exists():
            raise FileNotFoundError(
                f"Filesystem source does not exist: {normalized}"
            )

        return normalized

    def validate_destination(
        self,
        path: str | Path,
        *,
        require_exists: bool = False,
    ) -> Path:
        """
        Validate a destination filesystem path.

        The destination is not created or modified.
        """

        normalized = self.normalize_path(path)

        if require_exists and not normalized.exists():
            raise FileNotFoundError(
                f"Filesystem destination does not exist: {normalized}"
            )

        return normalized

    def validate_operation(
        self,
        operation: str,
        source: str | Path,
        destination: str | Path | None = None,
    ) -> FilesystemSecurityInfo:
        """
        Validate and describe a filesystem security operation.

        This performs validation/classification only.
        """

        operation_name = self._normalize_operation(operation)

        source_path = self.validate_source(
            source,
            require_exists=operation_name
            not in {"CREATE"},
        )

        if operation_name in {"RENAME", "COPY", "MOVE"}:
            if destination is None:
                raise ValueError(
                    f"{operation_name} requires a destination"
                )

            self.validate_destination(destination)

        elif destination is not None:
            raise ValueError(
                f"{operation_name} does not accept a destination"
            )

        return self.get_security_info(source_path, operation_name)

    def get_security_info(
        self,
        path: str | Path,
        operation: str,
    ) -> FilesystemSecurityInfo:
        """Return complete security information for a filesystem path."""

        operation_name = self._normalize_operation(operation)
        normalized = self.normalize_path(path)

        exists = normalized.exists()
        is_file = normalized.is_file() if exists else False
        is_directory = normalized.is_dir() if exists else False

        return FilesystemSecurityInfo(
            path=str(normalized),
            exists=exists,
            is_file=is_file,
            is_directory=is_directory,
            protection_level=self.classify_path(normalized),
            required_privilege=self.get_required_privilege(
                normalized,
                operation_name,
            ),
            risk_level=self.get_risk_level(
                normalized,
                operation_name,
            ),
        )

    @classmethod
    def _normalize_operation(cls, operation: str) -> str:
        """Validate and normalize a filesystem operation."""

        if not isinstance(operation, str):
            raise TypeError("operation must be a string")

        operation_name = operation.strip().upper()

        if operation_name not in cls._OPERATIONS:
            raise ValueError(
                f"Unsupported filesystem operation: {operation}"
            )

        return operation_name
