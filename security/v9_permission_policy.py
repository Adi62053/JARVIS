"""
JARVIS V9 - Advanced Permission Policies

Resource-aware permission rules layered above the V9 permission manager.

This module performs policy evaluation only.
It does not execute, elevate, modify, or delete system resources.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PermissionPolicy:
    """A resource-specific permission rule."""

    capability: str
    resource: str
    allowed: bool

    def __post_init__(self) -> None:
        if not isinstance(self.capability, str) or not self.capability.strip():
            raise ValueError("capability cannot be empty")

        if not isinstance(self.resource, str) or not self.resource.strip():
            raise ValueError("resource cannot be empty")

        if not isinstance(self.allowed, bool):
            raise TypeError("allowed must be a bool")


class V9PermissionPolicy:
    """Manage resource-aware V9 permission policies."""

    def __init__(self) -> None:
        self._policies: dict[tuple[str, str], PermissionPolicy] = {}

    @staticmethod
    def _normalize(value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("value must be a string")

        value = value.strip()

        if not value:
            raise ValueError("value cannot be empty")

        return value.upper()

    @classmethod
    def _key(cls, capability: str, resource: str) -> tuple[str, str]:
        return (
            cls._normalize(capability),
            cls._normalize(resource),
        )

    def set_policy(
        self,
        capability: str,
        resource: str,
        allowed: bool,
    ) -> None:
        """Create or replace a resource-specific policy."""

        policy = PermissionPolicy(
            capability=self._normalize(capability),
            resource=resource.strip(),
            allowed=allowed,
        )

        self._policies[self._key(capability, resource)] = policy

    def remove_policy(
        self,
        capability: str,
        resource: str,
    ) -> bool:
        """Remove a resource-specific policy."""

        key = self._key(capability, resource)

        if key not in self._policies:
            return False

        del self._policies[key]
        return True

    def has_policy(
        self,
        capability: str,
        resource: str,
    ) -> bool:
        """Return whether an explicit resource policy exists."""

        return self._key(capability, resource) in self._policies

    def is_allowed(
        self,
        capability: str,
        resource: str,
    ) -> bool | None:
        """
        Evaluate an explicit resource policy.

        Returns:
            True  -> explicitly allowed
            False -> explicitly denied
            None  -> no resource-specific policy exists
        """

        policy = self._policies.get(
            self._key(capability, resource)
        )

        if policy is None:
            return None

        return policy.allowed

    def get_policies(self) -> list[PermissionPolicy]:
        """Return all configured resource policies."""

        return list(self._policies.values())
