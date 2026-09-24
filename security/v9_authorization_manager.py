"""
JARVIS V9 - Authorization Manager

Tracks explicit authorization for individual security-sensitive
operations.

This module does not:
- execute operations
- request Windows elevation
- modify system permissions
- bypass security controls

Authorization is operation-specific and consumed when used.
"""

from __future__ import annotations


class V9AuthorizationManager:
    """Manage temporary authorization for security-sensitive operations."""

    def __init__(self) -> None:
        self._authorized: set[str] = set()

    @staticmethod
    def _normalize(operation_id: str) -> str:
        """Validate and normalize an operation identifier."""
        if not isinstance(operation_id, str):
            raise TypeError("operation_id must be a string")

        operation_id = operation_id.strip()

        if not operation_id:
            raise ValueError("operation_id cannot be empty")

        return operation_id

    def authorize(self, operation_id: str) -> None:
        """Grant authorization for one specific operation."""
        operation_id = self._normalize(operation_id)
        self._authorized.add(operation_id)

    def is_authorized(self, operation_id: str) -> bool:
        """Return whether an operation is currently authorized."""
        operation_id = self._normalize(operation_id)
        return operation_id in self._authorized

    def consume(self, operation_id: str) -> bool:
        """
        Consume authorization for one operation.

        Returns True when authorization existed and was consumed.
        """
        operation_id = self._normalize(operation_id)

        if operation_id not in self._authorized:
            return False

        self._authorized.remove(operation_id)
        return True

    def deny(self, operation_id: str) -> bool:
        """
        Remove authorization for one operation.

        Returns True when an authorization entry existed and was removed.
        """
        operation_id = self._normalize(operation_id)

        if operation_id not in self._authorized:
            return False

        self._authorized.remove(operation_id)
        return True

    def clear(self) -> None:
        """Remove all outstanding authorizations."""
        self._authorized.clear()

    def get_authorized_operations(self) -> set[str]:
        """Return a copy of currently authorized operations."""
        return set(self._authorized)
