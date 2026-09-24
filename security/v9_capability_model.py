"""
JARVIS V9 - Capability / Resource Model

Defines the security vocabulary used by V9 for capabilities,
operations, resources, and security requirements.

This module contains data definitions only.
It performs no system actions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SecurityCapability(str, Enum):
    """Security capability categories."""

    APPLICATION = "APPLICATION"
    FILE = "FILE"
    FOLDER = "FOLDER"
    PROCESS = "PROCESS"
    SERVICE = "SERVICE"
    REGISTRY = "REGISTRY"
    STORAGE = "STORAGE"
    NETWORK = "NETWORK"
    DEVICE = "DEVICE"
    SYSTEM = "SYSTEM"
    SECURITY = "SECURITY"
    FIRMWARE = "FIRMWARE"
    HARDWARE = "HARDWARE"


class SecurityOperation(str, Enum):
    """Operations that can be performed on a capability."""

    READ = "READ"
    WRITE = "WRITE"
    CREATE = "CREATE"
    MODIFY = "MODIFY"
    DELETE = "DELETE"
    START = "START"
    STOP = "STOP"
    TERMINATE = "TERMINATE"
    CONFIGURE = "CONFIGURE"
    EXECUTE = "EXECUTE"


@dataclass(frozen=True)
class SecurityResource:
    """A resource targeted by a security operation."""

    capability: SecurityCapability
    operation: SecurityOperation
    resource: str

    def __post_init__(self) -> None:
        if not isinstance(self.capability, SecurityCapability):
            raise TypeError("capability must be a SecurityCapability")

        if not isinstance(self.operation, SecurityOperation):
            raise TypeError("operation must be a SecurityOperation")

        if not isinstance(self.resource, str) or not self.resource.strip():
            raise ValueError("resource cannot be empty")

    @property
    def capability_id(self) -> str:
        return self.capability.value

    @property
    def operation_id(self) -> str:
        return self.operation.value

    def identifier(self) -> str:
        return f"{self.capability.value}.{self.operation.value}"


@dataclass(frozen=True)
class SecurityCapabilityRequest:
    """Complete security request for a targeted resource."""

    operation_id: str
    resource: SecurityResource

    def __post_init__(self) -> None:
        if not isinstance(self.operation_id, str):
            raise TypeError("operation_id must be a string")

        if not self.operation_id.strip():
            raise ValueError("operation_id cannot be empty")

        if not isinstance(self.resource, SecurityResource):
            raise TypeError("resource must be a SecurityResource")

    @property
    def capability(self) -> SecurityCapability:
        return self.resource.capability

    @property
    def operation(self) -> SecurityOperation:
        return self.resource.operation

    @property
    def target(self) -> str:
        return self.resource.resource
