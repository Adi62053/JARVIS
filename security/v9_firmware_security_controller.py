from security.v9_firmware_model import FirmwareAccessRequest, FirmwareOperation, FirmwareResource
from security.v9_firmware_protection import V9FirmwareProtectionManager
from security.v9_firmware_risk import V9FirmwareRiskEvaluator
from security.v9_firmware_security import build_firmware_security_request
from security.v9_security_controller import V9SecurityController
from security.v9_security_model import SecurityPrivilegeLevel, SecurityRiskLevel


class V9FirmwareSecurityController:
    """Evaluate firmware operations through the existing V9 security controller."""

    def __init__(
        self,
        controller: V9SecurityController | None = None,
        *,
        protection_manager: V9FirmwareProtectionManager | None = None,
        risk_evaluator: V9FirmwareRiskEvaluator | None = None,
    ) -> None:
        self.controller = controller or V9SecurityController()
        self.protection_manager = protection_manager or V9FirmwareProtectionManager()
        self.risk_evaluator = risk_evaluator or V9FirmwareRiskEvaluator()

    def evaluate(
        self,
        request: FirmwareAccessRequest,
    ):
        if not isinstance(request, FirmwareAccessRequest):
            raise TypeError("request must be a FirmwareAccessRequest")

        protection_level = self.protection_manager.get_protection_level(
            request.resource.resource_type,
            request.resource.identifier,
        )

        risk_level, required_privilege = self.risk_evaluator.evaluate(
            request.operation,
            protection_level=protection_level,
        )

        operation_id, security_resource = build_firmware_security_request(request)

        return self.controller.evaluate(
            operation_id=operation_id,
            capability=security_resource.capability,
            resource=security_resource.resource,
            risk_level=SecurityRiskLevel(risk_level),
            required_privilege=SecurityPrivilegeLevel(required_privilege),
        )
