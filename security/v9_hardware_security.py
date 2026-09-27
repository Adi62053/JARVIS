from .v9_capability_model import (
    SecurityCapability,
    SecurityCapabilityRequest,
    SecurityResource,
    SecurityOperation,
)
from .v9_hardware_capability import (
    get_hardware_capability,
    map_hardware_operation,
)
from .v9_hardware_capability_model import (
    HardwareOperation,
    HardwareResource,
    HardwareResourceType,
)
from .v9_hardware_protection import (
    HardwareProtectionCategory,
    V9HardwareProtectionManager,
)
from .v9_hardware_risk import V9HardwareRiskEvaluator


class V9HardwareSecurityRequestBuilder:
    """Builds V9 security requests for hardware resources."""

    def __init__(
        self,
        protection_manager: V9HardwareProtectionManager | None = None,
        risk_evaluator: V9HardwareRiskEvaluator | None = None,
    ) -> None:
        self._protection = (
            protection_manager or V9HardwareProtectionManager()
        )
        self._risk = risk_evaluator or V9HardwareRiskEvaluator()

    def build_request(
        self,
        operation: HardwareOperation,
        resource: HardwareResource,
    ) -> SecurityCapabilityRequest:
        if not isinstance(operation, HardwareOperation):
            raise TypeError("operation must be HardwareOperation.")

        if not isinstance(resource, HardwareResource):
            raise TypeError("resource must be HardwareResource.")

        security_operation = map_hardware_operation(operation)

        security_resource = SecurityResource(
            capability=get_hardware_capability(),
            operation=security_operation,
            resource=resource.identifier,
        )

        return SecurityCapabilityRequest(
            operation_id=f"hardware.{operation.value}",
            resource=security_resource,
        )

    def evaluate_risk(
        self,
        operation: HardwareOperation,
        resource: HardwareResource,
    ) -> tuple[str, str]:
        category = self._protection.classify(
            resource.resource_type,
            resource.identifier,
        )

        return self._risk.evaluate(
            operation,
            protected=(
                category == HardwareProtectionCategory.PROTECTED
            ),
            critical=(
                category == HardwareProtectionCategory.CRITICAL
            ),
            sensitive=(
                category == HardwareProtectionCategory.SENSITIVE
            ),
        )

    def build_and_evaluate(
        self,
        operation: HardwareOperation,
        resource: HardwareResource,
    ) -> tuple[SecurityCapabilityRequest, str, str]:
        request = self.build_request(operation, resource)
        risk_level, required_privilege = self.evaluate_risk(
            operation,
            resource,
        )

        return request, risk_level, required_privilege
