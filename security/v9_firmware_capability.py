from security.v9_capability_model import SecurityCapability, SecurityOperation
from security.v9_firmware_model import FirmwareOperation


def map_firmware_operation(operation: FirmwareOperation) -> SecurityOperation:
    if not isinstance(operation, FirmwareOperation):
        raise TypeError("operation must be a FirmwareOperation")

    if operation == FirmwareOperation.READ:
        return SecurityOperation.READ

    return SecurityOperation.CONFIGURE


def get_firmware_capability() -> SecurityCapability:
    return SecurityCapability.FIRMWARE
