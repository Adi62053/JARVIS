from .v9_capability_model import SecurityCapability, SecurityOperation
from .v9_hardware_capability_model import (
    HardwareOperation,
    HardwareResourceType,
)


def map_hardware_operation(operation: HardwareOperation) -> SecurityOperation:
    if operation == HardwareOperation.READ:
        return SecurityOperation.READ

    if operation in {
        HardwareOperation.CONFIGURE,
        HardwareOperation.ENABLE,
        HardwareOperation.DISABLE,
    }:
        return SecurityOperation.CONFIGURE

    raise ValueError(f"Unsupported hardware operation: {operation}")


def get_hardware_capability() -> SecurityCapability:
    return SecurityCapability.HARDWARE


def get_hardware_resource_identifier(
    resource_type: HardwareResourceType,
    identifier: str,
) -> str:
    if not isinstance(resource_type, HardwareResourceType):
        raise TypeError("resource_type must be HardwareResourceType.")

    if not isinstance(identifier, str) or not identifier.strip():
        raise ValueError("identifier must be a non-empty string.")

    return f"{resource_type.value}:{identifier.strip()}"
