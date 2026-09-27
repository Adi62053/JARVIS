from dataclasses import dataclass

from .v9_hardware_capability_model import (
    HardwareOperation,
    HardwareResource,
)
from .v9_hardware_security_controller import V9HardwareSecurityController


@dataclass(frozen=True)
class HardwareOperationResult:
    operation: HardwareOperation
    resource_identifier: str
    executed: bool
    allowed: bool
    decision: str
    risk_level: str
    required_privilege: str
    message: str


class V9ControlledHardwareOperations:
    """Controlled hardware boundary with safe dry-run behavior."""

    def __init__(
        self,
        security_controller: V9HardwareSecurityController | None = None,
    ) -> None:
        self._security = (
            security_controller
            or V9HardwareSecurityController()
        )

    @property
    def security(self) -> V9HardwareSecurityController:
        return self._security

    def evaluate(
        self,
        operation: HardwareOperation,
        resource: HardwareResource,
    ) -> HardwareOperationResult:
        (
            _request,
            risk_level,
            required_privilege,
            decision,
        ) = self._security.evaluate(
            operation,
            resource,
        )

        allowed = decision.value == "ALLOW"

        return HardwareOperationResult(
            operation=operation,
            resource_identifier=resource.identifier,
            executed=False,
            allowed=allowed,
            decision=decision.value,
            risk_level=risk_level,
            required_privilege=required_privilege,
            message=(
                "AUTHORIZED DRY-RUN"
                if allowed
                else f"SECURITY BLOCK: {decision.value}"
            ),
        )

    def execute(
        self,
        operation: HardwareOperation,
        resource: HardwareResource,
        *,
        execute: bool = False,
    ) -> HardwareOperationResult:
        result = self.evaluate(operation, resource)

        if not result.allowed:
            return result

        if not execute:
            return result

        if operation == HardwareOperation.READ:
            return HardwareOperationResult(
                operation=operation,
                resource_identifier=resource.identifier,
                executed=True,
                allowed=True,
                decision=result.decision,
                risk_level=result.risk_level,
                required_privilege=result.required_privilege,
                message="READ operation authorized; use V9.17 inspector for data acquisition.",
            )

        raise RuntimeError(
            "Hardware mutation is not implemented in V9.17.10. "
            "No hardware state was changed."
        )
