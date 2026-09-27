from dataclasses import dataclass
from enum import Enum


class HardwareResourceType(str, Enum):
    CPU = "CPU"
    MEMORY = "MEMORY"
    GPU = "GPU"
    STORAGE = "STORAGE"
    MOTHERBOARD = "MOTHERBOARD"
    BIOS = "BIOS"
    BATTERY = "BATTERY"
    USB = "USB"


class HardwareOperation(str, Enum):
    READ = "READ"
    CONFIGURE = "CONFIGURE"
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"


@dataclass(frozen=True)
class HardwareResource:
    resource_type: HardwareResourceType
    identifier: str
    description: str


@dataclass(frozen=True)
class HardwareAccessRequest:
    operation: HardwareOperation
    resource: HardwareResource

    @property
    def resource_type(self) -> HardwareResourceType:
        return self.resource.resource_type

    @property
    def identifier(self) -> str:
        return self.resource.identifier


@dataclass(frozen=True)
class CPUInfo:
    name: str
    cores: int
    logical_processors: int
    max_clock_speed_mhz: int


@dataclass(frozen=True)
class MemoryInfo:
    total_physical_bytes: int


@dataclass(frozen=True)
class GPUInfo:
    name: str
    adapter_ram_bytes: int | None
    driver_version: str | None
    status: str


@dataclass(frozen=True)
class StorageInfo:
    model: str
    interface_type: str | None
    media_type: str | None
    size_bytes: int | None
    status: str


@dataclass(frozen=True)
class MotherboardInfo:
    manufacturer: str
    product: str | None
    serial_number: str | None


@dataclass(frozen=True)
class BIOSInfo:
    manufacturer: str
    version: str
    release_date: str | None


@dataclass(frozen=True)
class BatteryInfo:
    name: str
    status_code: int | None
    charge_percent: int | None


@dataclass(frozen=True)
class USBDeviceInfo:
    name: str
    status: str
    instance_id: str
