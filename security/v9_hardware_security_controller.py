from .v9_hardware_capability_model import (
    HardwareOperation,
    HardwareResource,
)
from .v9_hardware_security import V9HardwareSecurityRequestBuilder
from .v9_security_controller import V9SecurityController
from .v9_security_model import (
    SecurityDecision,
    SecurityPrivilegeLevel,
    SecurityRiskLevel,
)


class V9HardwareSecurityController:
    """Connects hardware requests to the existing V9 security controller."""

    def __init__(
        self,
        controller: V9SecurityController | None = None,
    ) -> None:
        self._controller = controller or V9SecurityController()
        self._builder = V9HardwareSecurityRequestBuilder()

    @property
    def controller(self) -> V9SecurityController:
        return self._controller

    def evaluate(
        self,
        operation: HardwareOperation,
        resource: HardwareResource,
    ) -> tuple[
        object,
        str,
        str,
        SecurityDecision,
    ]:
        request, risk_level, required_privilege = (
            self._builder.build_and_evaluate(
                operation,
                resource,
            )
        )

        decision = self._controller.evaluate(
            operation_id=request.operation_id,
            capability=request.resource.capability,
            resource=request.resource.resource,
            risk_level=SecurityRiskLevel(risk_level),
            required_privilege=SecurityPrivilegeLevel(
                required_privilege
            ),
        )

        return (
            request,
            risk_level,
            required_privilege,
            decision,
        )
