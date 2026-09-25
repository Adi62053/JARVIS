"""
JARVIS V9.16 - Network & Device Access
Data model layer.

This module defines structured representations for network and device
resources. It performs no system changes and no privileged operations.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class NetworkResourceType(str, Enum):
    ADAPTER = "ADAPTER"
    IP_CONFIGURATION = "IP_CONFIGURATION"
    TCP_CONNECTION = "TCP_CONNECTION"


class DeviceResourceType(str, Enum):
    PNP_DEVICE = "PNP_DEVICE"


class NetworkOperation(str, Enum):
    READ = "READ"
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    CONFIGURE = "CONFIGURE"
    CONNECT = "CONNECT"
    DISCONNECT = "DISCONNECT"


class DeviceOperation(str, Enum):
    READ = "READ"
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    CONFIGURE = "CONFIGURE"


@dataclass(frozen=True)
class NetworkResource:
    resource_type: NetworkResourceType
    identifier: str
    description: str = ""


@dataclass(frozen=True)
class DeviceResource:
    resource_type: DeviceResourceType
    identifier: str
    device_class: str = ""
    description: str = ""


@dataclass(frozen=True)
class NetworkAccessRequest:
    operation: NetworkOperation
    resource: NetworkResource


@dataclass(frozen=True)
class DeviceAccessRequest:
    operation: DeviceOperation
    resource: DeviceResource


@dataclass(frozen=True)
class NetworkAdapterInfo:
    name: str
    status: str
    interface_description: str
    mac_address: Optional[str] = None
    link_speed: Optional[str] = None


@dataclass(frozen=True)
class DeviceInfo:
    name: str
    status: str
    device_class: str
    instance_id: str
    manufacturer: Optional[str] = None
