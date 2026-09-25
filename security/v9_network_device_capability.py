"""
JARVIS V9.16 - Network & Device Capability Mapping

Maps V9.16-specific network and device operations to the existing
V9 SecurityCapability / SecurityOperation vocabulary.

This module performs no system actions.
"""

from __future__ import annotations

from security.v9_capability_model import (
    SecurityCapability,
    SecurityOperation,
)
from security.v9_network_device_model import (
    DeviceOperation,
    NetworkOperation,
)


def map_network_operation(
    operation: NetworkOperation,
) -> SecurityOperation:
    """
    Map a V9.16 network operation to the V9 security operation model.
    """

    if not isinstance(operation, NetworkOperation):
        raise TypeError("operation must be a NetworkOperation")

    mapping = {
        NetworkOperation.READ: SecurityOperation.READ,
        NetworkOperation.ENABLE: SecurityOperation.CONFIGURE,
        NetworkOperation.DISABLE: SecurityOperation.CONFIGURE,
        NetworkOperation.CONFIGURE: SecurityOperation.CONFIGURE,
        NetworkOperation.CONNECT: SecurityOperation.EXECUTE,
        NetworkOperation.DISCONNECT: SecurityOperation.EXECUTE,
    }

    return mapping[operation]


def map_device_operation(
    operation: DeviceOperation,
) -> SecurityOperation:
    """
    Map a V9.16 device operation to the V9 security operation model.
    """

    if not isinstance(operation, DeviceOperation):
        raise TypeError("operation must be a DeviceOperation")

    mapping = {
        DeviceOperation.READ: SecurityOperation.READ,
        DeviceOperation.ENABLE: SecurityOperation.CONFIGURE,
        DeviceOperation.DISABLE: SecurityOperation.CONFIGURE,
        DeviceOperation.CONFIGURE: SecurityOperation.CONFIGURE,
    }

    return mapping[operation]


def get_network_capability() -> SecurityCapability:
    """Return the V9 security capability for network resources."""

    return SecurityCapability.NETWORK


def get_device_capability() -> SecurityCapability:
    """Return the V9 security capability for device resources."""

    return SecurityCapability.DEVICE
