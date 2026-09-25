"""
JARVIS V9.16.9 - Device Risk Evaluation

Read-only risk evaluation for Plug-and-Play device operations.
"""

from __future__ import annotations

from security.v9_device_protection import (
    DeviceProtectionCategory,
    V9DeviceProtectionManager,
)
from security.v9_network_device_model import (
    DeviceInfo,
    DeviceOperation,
)
from security.v9_security_model import (
    SecurityPrivilegeLevel,
    SecurityRiskLevel,
)


class V9DeviceRiskEvaluator:
    """Evaluate security risk before device operations."""

    def __init__(self) -> None:
        self._protection = V9DeviceProtectionManager()

    def get_risk_level(
        self,
        device: DeviceInfo,
        operation: DeviceOperation,
    ) -> SecurityRiskLevel:
        if not isinstance(device, DeviceInfo):
            raise TypeError("device must be a DeviceInfo")

        if not isinstance(operation, DeviceOperation):
            raise TypeError("operation must be a DeviceOperation")

        category = self._protection.classify_device(device)

        if category == DeviceProtectionCategory.PROTECTED:
            return SecurityRiskLevel.CRITICAL

        if category == DeviceProtectionCategory.CRITICAL:
            return SecurityRiskLevel.HIGH

        if category == DeviceProtectionCategory.SENSITIVE:
            if operation == DeviceOperation.READ:
                return SecurityRiskLevel.SAFE

            return SecurityRiskLevel.HIGH

        if operation == DeviceOperation.READ:
            return SecurityRiskLevel.SAFE

        return SecurityRiskLevel.CAUTION

    def get_required_privilege(
        self,
        device: DeviceInfo,
        operation: DeviceOperation,
    ) -> SecurityPrivilegeLevel:
        if not isinstance(device, DeviceInfo):
            raise TypeError("device must be a DeviceInfo")

        if not isinstance(operation, DeviceOperation):
            raise TypeError("operation must be a DeviceOperation")

        category = self._protection.classify_device(device)

        if category == DeviceProtectionCategory.PROTECTED:
            return SecurityPrivilegeLevel.SYSTEM

        if category == DeviceProtectionCategory.CRITICAL:
            return SecurityPrivilegeLevel.ADMINISTRATOR

        if category == DeviceProtectionCategory.SENSITIVE:
            if operation == DeviceOperation.READ:
                return SecurityPrivilegeLevel.USER

            return SecurityPrivilegeLevel.ADMINISTRATOR

        return SecurityPrivilegeLevel.USER

    def evaluate(
        self,
        device: DeviceInfo,
        operation: DeviceOperation,
    ) -> tuple[SecurityRiskLevel, SecurityPrivilegeLevel]:
        return (
            self.get_risk_level(device, operation),
            self.get_required_privilege(device, operation),
        )
