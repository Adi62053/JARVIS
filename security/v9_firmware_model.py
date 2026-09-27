from dataclasses import dataclass
from enum import Enum


class FirmwareResourceType(str, Enum):
    BIOS = "BIOS"
    UEFI = "UEFI"
    SYSTEM_FIRMWARE = "SYSTEM_FIRMWARE"
    SECURE_BOOT = "SECURE_BOOT"
    SMBIOS = "SMBIOS"
    ACPI = "ACPI"
    BCD_FIRMWARE = "BCD_FIRMWARE"


class FirmwareOperation(str, Enum):
    READ = "READ"
    CONFIGURE = "CONFIGURE"
    UPDATE = "UPDATE"
    FLASH = "FLASH"
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"


@dataclass(frozen=True)
class FirmwareResource:
    resource_type: FirmwareResourceType
    identifier: str
    description: str


@dataclass(frozen=True)
class FirmwareAccessRequest:
    operation: FirmwareOperation
    resource: FirmwareResource

    @property
    def resource_type(self) -> FirmwareResourceType:
        return self.resource.resource_type

    @property
    def identifier(self) -> str:
        return self.resource.identifier


@dataclass(frozen=True)
class BIOSInfo:
    manufacturer: str
    version: str
    release_date: str
    serial_number: str


@dataclass(frozen=True)
class UEFIInfo:
    firmware_type: str
    secure_boot_enabled: bool


@dataclass(frozen=True)
class FirmwareDeviceInfo:
    name: str
    status: str
    instance_id: str


@dataclass(frozen=True)
class BCDFirmwareInfo:
    identifier: str
    description: str
    device: str
    path: str
