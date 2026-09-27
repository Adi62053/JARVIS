from security.v9_firmware_inspector import V9FirmwareInspector
from security.v9_firmware_model import FirmwareAccessRequest, FirmwareOperation, FirmwareResource, FirmwareResourceType
from security.v9_firmware_security_controller import V9FirmwareSecurityController


class V9FirmwareInspectionSecurity:
    def __init__(self, inspector=None, security_controller=None):
        self.inspector = inspector or V9FirmwareInspector()
        self.security_controller = security_controller or V9FirmwareSecurityController()

    def evaluate_bios(self):
        info = self.inspector.get_bios()
        resource = FirmwareResource(
            FirmwareResourceType.BIOS,
            "BIOS",
            f"{info.manufacturer} {info.version}",
        )
        return self.security_controller.evaluate(
            FirmwareAccessRequest(FirmwareOperation.READ, resource)
        )

    def evaluate_uefi(self):
        info = self.inspector.get_uefi()
        resource = FirmwareResource(
            FirmwareResourceType.UEFI,
            "UEFI",
            f"FirmwareType={info.firmware_type}, SecureBoot={info.secure_boot_enabled}",
        )
        return self.security_controller.evaluate(
            FirmwareAccessRequest(FirmwareOperation.READ, resource)
        )

    def evaluate_firmware_devices(self):
        results = []
        for device in self.inspector.get_firmware_devices():
            resource = FirmwareResource(
                FirmwareResourceType.SYSTEM_FIRMWARE,
                device.instance_id,
                device.name,
            )
            results.append(
                self.security_controller.evaluate(
                    FirmwareAccessRequest(FirmwareOperation.READ, resource)
                )
            )
        return results

    def evaluate_bcd_firmware(self):
        results = []
        for entry in self.inspector.get_bcd_firmware():
            resource = FirmwareResource(
                FirmwareResourceType.BCD_FIRMWARE,
                entry.identifier,
                entry.description or entry.path or entry.identifier,
            )
            results.append(
                self.security_controller.evaluate(
                    FirmwareAccessRequest(FirmwareOperation.READ, resource)
                )
            )
        return results
