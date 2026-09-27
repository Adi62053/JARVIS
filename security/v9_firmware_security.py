from security.v9_capability_model import SecurityCapability, SecurityOperation, SecurityResource
from security.v9_firmware_capability import get_firmware_capability
from security.v9_firmware_model import FirmwareAccessRequest, FirmwareOperation, FirmwareResource


def map_firmware_operation(operation: FirmwareOperation) -> SecurityOperation:
    if not isinstance(operation, FirmwareOperation):
        raise TypeError("operation must be a FirmwareOperation")

    if operation == FirmwareOperation.READ:
        return SecurityOperation.READ

    return SecurityOperation.CONFIGURE


def build_firmware_security_resource(
    resource: FirmwareResource,
) -> SecurityResource:
    if not isinstance(resource, FirmwareResource):
        raise TypeError("resource must be a FirmwareResource")

    return SecurityResource(
        capability=get_firmware_capability(),
        operation=map_firmware_operation(
            FirmwareOperation.READ
        ),
        resource=resource.identifier,
    )


def build_firmware_security_request(
    request: FirmwareAccessRequest,
) -> tuple[str, SecurityResource]:
    if not isinstance(request, FirmwareAccessRequest):
        raise TypeError("request must be a FirmwareAccessRequest")

    security_operation = map_firmware_operation(request.operation)

    resource = SecurityResource(
        capability=get_firmware_capability(),
        operation=security_operation,
        resource=request.resource.identifier,
    )

    operation_id = f"firmware.{request.operation.value}"

    return operation_id, resource
