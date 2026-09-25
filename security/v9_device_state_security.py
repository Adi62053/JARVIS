"""
JARVIS V9.16.13 + V9.16.14
Device State-Control Security Boundary.

V9.16.13:
- Defines the security boundary for PnP device state operations.
- Does not bypass Windows device security.
- Does not execute device state changes by default.

V9.16.14:
- Integrates explicit authorization with the existing V9
  Security Controller.
- Authorization is operation-specific and one-shot.
- Authorization cannot override an elevation requirement.
"""

from __future__ import annotations

from dataclasses import dataclass

from security.v9_device_protection import V9DeviceProtectionManager
from security.v9_network_device_model import (
    DeviceInfo,
    DeviceOperation,
)
from security.v9_network_device_security import (
    V9NetworkDeviceSecurityRequestBuilder,
)
from security.v9_security_controller import V9SecurityController


@dataclass(frozen=True)
class DeviceOperationResult:
    operation: DeviceOperation
    device_name: str
    executed: bool
    allowed: bool
    decision: str
    risk_level: str
    required_privilege: str
    message: str


class V9DeviceStateSecurityBoundary:
    """
    V9.16.13 device state-control boundary.

    This layer evaluates device operations through the existing
    V9 security architecture before any Windows PnP mutation.
    """

    def __init__(
        self,
        controller: V9SecurityController | None = None,
    ) -> None:
        self.controller = controller or V9SecurityController()
        self.builder = V9NetworkDeviceSecurityRequestBuilder()
        self.protection = V9DeviceProtectionManager()

    def evaluate(
        self,
        operation: DeviceOperation,
        device: DeviceInfo,
    ):
        if not isinstance(operation, DeviceOperation):
            raise TypeError("operation must be a DeviceOperation")

        if not isinstance(device, DeviceInfo):
            raise TypeError("device must be DeviceInfo")

        request = self.builder.build_device_request(
            operation,
            device,
        )

        risk, privilege = self.builder.evaluate_device(
            operation,
            device,
        )

        decision = self.controller.evaluate(
            operation_id=request.operation_id,
            capability=request.capability,
            resource=request.target,
            risk_level=risk,
            required_privilege=privilege,
        )

        return request, risk, privilege, decision

    def classify(self, device: DeviceInfo):
        return self.protection.classify_device(device)

    def is_protected(self, device: DeviceInfo) -> bool:
        return self.protection.is_protected(device)


class V9AuthorizedDeviceOperations:
    """
    V9.16.14 authorization-aware device operation boundary.

    execute=False is always the default.

    This class intentionally does not contain a Windows PnP mutation
    implementation yet. V9.16.13/14 establishes the security gate
    first; actual mutation remains outside this test path.
    """

    def __init__(
        self,
        security: V9DeviceStateSecurityBoundary | None = None,
    ) -> None:
        self.security = (
            security or V9DeviceStateSecurityBoundary()
        )

    def authorize(
        self,
        operation: DeviceOperation,
        device: DeviceInfo,
    ) -> str:
        request, risk, privilege, _ = self.security.evaluate(
            operation,
            device,
        )

        operation_id = request.operation_id

        self.security.controller.authorization_manager.authorize(
            operation_id
        )

        return operation_id

    def execute(
        self,
        operation: DeviceOperation,
        device: DeviceInfo,
        *,
        execute: bool = False,
    ) -> DeviceOperationResult:
        request, risk, privilege, decision = (
            self.security.evaluate(operation, device)
        )

        if decision.value != "ALLOW":
            return DeviceOperationResult(
                operation=operation,
                device_name=device.name,
                executed=False,
                allowed=False,
                decision=decision.value,
                risk_level=risk.value,
                required_privilege=privilege.value,
                message=(
                    f"Security decision: {decision.value}; "
                    f"risk={risk.value}; "
                    f"required_privilege={privilege.value}"
                ),
            )

        if not execute:
            return DeviceOperationResult(
                operation=operation,
                device_name=device.name,
                executed=False,
                allowed=True,
                decision=decision.value,
                risk_level=risk.value,
                required_privilege=privilege.value,
                message=(
                    f"DRY-RUN: {operation.value} would be "
                    f"executed on device '{device.name}'"
                ),
            )

        raise RuntimeError(
            "V9.16.14 device mutation execution is intentionally "
            "not implemented in this security-boundary milestone"
        )
