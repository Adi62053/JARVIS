from dataclasses import dataclass

from security.v9_firmware_model import FirmwareAccessRequest, FirmwareOperation, FirmwareResource
from security.v9_firmware_security_controller import V9FirmwareSecurityController


@dataclass(frozen=True)
class FirmwareOperationResult:
    operation: FirmwareOperation
    resource_identifier: str
    executed: bool
    allowed: bool
    decision: str
    message: str


class V9ControlledFirmwareOperations:
    def __init__(self, security_controller=None):
        self.security_controller = security_controller or V9FirmwareSecurityController()

    def evaluate(self, request: FirmwareAccessRequest):
        return self.security_controller.evaluate(request)

    def execute(self, request: FirmwareAccessRequest, execute=False):
        if not isinstance(request, FirmwareAccessRequest):
            raise TypeError("request must be a FirmwareAccessRequest")

        decision = self.evaluate(request)

        if request.operation == FirmwareOperation.READ:
            return FirmwareOperationResult(
                operation=request.operation,
                resource_identifier=request.resource.identifier,
                executed=bool(execute),
                allowed=decision.value == "ALLOW",
                decision=decision.value,
                message="READ operation requires the firmware inspector for data acquisition.",
            )

        if execute:
            raise RuntimeError(
                "Firmware mutation is not implemented in V9.18.9. "
                "No firmware state was changed."
            )

        return FirmwareOperationResult(
            operation=request.operation,
            resource_identifier=request.resource.identifier,
            executed=False,
            allowed=decision.value == "ALLOW",
            decision=decision.value,
            message="AUTHORIZED DRY-RUN" if decision.value == "ALLOW" else "OPERATION NOT EXECUTED",
        )
