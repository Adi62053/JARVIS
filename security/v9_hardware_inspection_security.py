from .v9_hardware_capability_model import (
    BIOSInfo,
    BatteryInfo,
    CPUInfo,
    GPUInfo,
    HardwareOperation,
    HardwareResource,
    HardwareResourceType,
    MemoryInfo,
    MotherboardInfo,
    StorageInfo,
    USBDeviceInfo,
)
from .v9_hardware_inspector import V9HardwareInspector
from .v9_hardware_security_controller import V9HardwareSecurityController


class V9HardwareInspectionSecurity:
    """Builds security-aware hardware resources from live inspection data."""

    def __init__(
        self,
        inspector: V9HardwareInspector | None = None,
        security: V9HardwareSecurityController | None = None,
    ) -> None:
        self._inspector = inspector or V9HardwareInspector()
        self._security = security or V9HardwareSecurityController()

    @property
    def inspector(self) -> V9HardwareInspector:
        return self._inspector

    @property
    def security(self) -> V9HardwareSecurityController:
        return self._security

    def build_cpu_resource(self, info: CPUInfo) -> HardwareResource:
        return HardwareResource(
            resource_type=HardwareResourceType.CPU,
            identifier=info.name,
            description="CPU hardware resource",
        )

    def build_memory_resource(self, info: MemoryInfo) -> HardwareResource:
        return HardwareResource(
            resource_type=HardwareResourceType.MEMORY,
            identifier="physical-memory",
            description="Physical memory resource",
        )

    def build_gpu_resource(self, info: GPUInfo) -> HardwareResource:
        return HardwareResource(
            resource_type=HardwareResourceType.GPU,
            identifier=info.name,
            description="GPU hardware resource",
        )

    def build_storage_resource(
        self,
        info: StorageInfo,
    ) -> HardwareResource:
        return HardwareResource(
            resource_type=HardwareResourceType.STORAGE,
            identifier=info.model,
            description="Storage hardware resource",
        )

    def build_motherboard_resource(
        self,
        info: MotherboardInfo,
    ) -> HardwareResource:
        identifier = info.product or info.manufacturer
        return HardwareResource(
            resource_type=HardwareResourceType.MOTHERBOARD,
            identifier=identifier,
            description="Motherboard hardware resource",
        )

    def build_bios_resource(self, info: BIOSInfo) -> HardwareResource:
        return HardwareResource(
            resource_type=HardwareResourceType.BIOS,
            identifier=f"{info.manufacturer}:{info.version}",
            description="BIOS firmware resource",
        )

    def build_battery_resource(
        self,
        info: BatteryInfo,
    ) -> HardwareResource:
        return HardwareResource(
            resource_type=HardwareResourceType.BATTERY,
            identifier=info.name,
            description="Battery hardware resource",
        )

    def build_usb_resource(
        self,
        info: USBDeviceInfo,
    ) -> HardwareResource:
        return HardwareResource(
            resource_type=HardwareResourceType.USB,
            identifier=info.instance_id,
            description=info.name,
        )

    def inspect_and_evaluate_cpu(self):
        info = self._inspector.get_cpu()
        resource = self.build_cpu_resource(info)
        return info, self._security.evaluate(
            HardwareOperation.READ,
            resource,
        )

    def inspect_and_evaluate_memory(self):
        info = self._inspector.get_memory()
        resource = self.build_memory_resource(info)
        return info, self._security.evaluate(
            HardwareOperation.READ,
            resource,
        )

    def inspect_and_evaluate_gpus(self):
        results = []
        for info in self._inspector.get_gpus():
            resource = self.build_gpu_resource(info)
            results.append(
                (
                    info,
                    self._security.evaluate(
                        HardwareOperation.READ,
                        resource,
                    ),
                )
            )
        return results

    def inspect_and_evaluate_storage(self):
        results = []
        for info in self._inspector.get_storage():
            resource = self.build_storage_resource(info)
            results.append(
                (
                    info,
                    self._security.evaluate(
                        HardwareOperation.READ,
                        resource,
                    ),
                )
            )
        return results

    def inspect_and_evaluate_motherboard(self):
        info = self._inspector.get_motherboard()
        resource = self.build_motherboard_resource(info)
        return info, self._security.evaluate(
            HardwareOperation.READ,
            resource,
        )

    def inspect_and_evaluate_bios(self):
        info = self._inspector.get_bios()
        resource = self.build_bios_resource(info)
        return info, self._security.evaluate(
            HardwareOperation.READ,
            resource,
        )

    def inspect_and_evaluate_batteries(self):
        results = []
        for info in self._inspector.get_batteries():
            resource = self.build_battery_resource(info)
            results.append(
                (
                    info,
                    self._security.evaluate(
                        HardwareOperation.READ,
                        resource,
                    ),
                )
            )
        return results

    def inspect_and_evaluate_usb(self):
        results = []
        for info in self._inspector.get_usb_devices():
            resource = self.build_usb_resource(info)
            results.append(
                (
                    info,
                    self._security.evaluate(
                        HardwareOperation.READ,
                        resource,
                    ),
                )
            )
        return results
