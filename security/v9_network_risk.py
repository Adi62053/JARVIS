"""
JARVIS V9.16.8 - Network Risk Evaluation

Read-only risk evaluation for network operations.

This module determines security risk and required privilege.
It performs no network modifications.
"""

from __future__ import annotations

from security.v9_network_device_model import (
    NetworkAdapterInfo,
    NetworkOperation,
)
from security.v9_security_model import (
    SecurityPrivilegeLevel,
    SecurityRiskLevel,
)


class V9NetworkRiskEvaluator:
    """Evaluate security risk for network operations."""

    def get_risk_level(
        self,
        operation: NetworkOperation,
        adapter: NetworkAdapterInfo | None = None,
    ) -> SecurityRiskLevel:
        """Return the security risk associated with a network operation."""

        if not isinstance(operation, NetworkOperation):
            raise TypeError("operation must be a NetworkOperation")

        if operation == NetworkOperation.READ:
            return SecurityRiskLevel.SAFE

        if operation == NetworkOperation.CONFIGURE:
            return SecurityRiskLevel.HIGH

        if operation in {
            NetworkOperation.ENABLE,
            NetworkOperation.DISABLE,
        }:
            return SecurityRiskLevel.HIGH

        if operation in {
            NetworkOperation.CONNECT,
            NetworkOperation.DISCONNECT,
        }:
            return SecurityRiskLevel.CAUTION

        return SecurityRiskLevel.HIGH

    def get_required_privilege(
        self,
        operation: NetworkOperation,
        adapter: NetworkAdapterInfo | None = None,
    ) -> SecurityPrivilegeLevel:
        """Return the minimum JARVIS privilege required."""

        if not isinstance(operation, NetworkOperation):
            raise TypeError("operation must be a NetworkOperation")

        if operation == NetworkOperation.READ:
            return SecurityPrivilegeLevel.USER

        if operation in {
            NetworkOperation.CONNECT,
            NetworkOperation.DISCONNECT,
        }:
            return SecurityPrivilegeLevel.USER

        if operation in {
            NetworkOperation.ENABLE,
            NetworkOperation.DISABLE,
            NetworkOperation.CONFIGURE,
        }:
            return SecurityPrivilegeLevel.ADMINISTRATOR

        return SecurityPrivilegeLevel.ADMINISTRATOR

    def evaluate(
        self,
        operation: NetworkOperation,
        adapter: NetworkAdapterInfo | None = None,
    ) -> tuple[SecurityRiskLevel, SecurityPrivilegeLevel]:
        """Return risk and required privilege without executing anything."""

        return (
            self.get_risk_level(operation, adapter),
            self.get_required_privilege(operation, adapter),
        )
