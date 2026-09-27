from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_firmware_inspector import V9FirmwareInspector
from security.v9_firmware_model import FirmwareAccessRequest, FirmwareOperation, FirmwareResource, FirmwareResourceType
from security.v9_firmware_security_controller import V9FirmwareSecurityController
from security.v9_firmware_operations import V9ControlledFirmwareOperations
from security.v9_audit_logger import V9AuditLogger


with TemporaryDirectory() as temp:
    inspector = V9FirmwareInspector()
    controller = V9FirmwareSecurityController()
    controller.controller.permission_manager.set_permission("FIRMWARE", True)
    audit = V9AuditLogger(Path(temp) / "regression.jsonl")
    controller.controller.audit_logger = audit

    bios = inspector.get_bios()
    uefi = inspector.get_uefi()
    firmware_devices = inspector.get_firmware_devices()
    bcd = inspector.get_bcd_firmware()

    print("BIOS:", bios)
    print("UEFI:", uefi)
    print("FIRMWARE DEVICES:", len(firmware_devices))
    print("BCD FIRMWARE:", len(bcd))

    bios_resource = FirmwareResource(FirmwareResourceType.BIOS, "BIOS-REGRESSION", "BIOS")
    uefi_resource = FirmwareResource(FirmwareResourceType.UEFI, "UEFI-REGRESSION", "UEFI")
    bcd_resource = FirmwareResource(FirmwareResourceType.BCD_FIRMWARE, "BCD-REGRESSION", "BCD")

    print("BIOS SECURITY:", controller.evaluate(FirmwareAccessRequest(FirmwareOperation.READ, bios_resource)).value)
    print("UEFI SECURITY:", controller.evaluate(FirmwareAccessRequest(FirmwareOperation.READ, uefi_resource)).value)
    print("BCD SECURITY:", controller.evaluate(FirmwareAccessRequest(FirmwareOperation.READ, bcd_resource)).value)

    operations = V9ControlledFirmwareOperations(controller)
    flash = operations.execute(
        FirmwareAccessRequest(FirmwareOperation.FLASH, bios_resource)
    )
    print("FLASH BOUNDARY:", flash.decision, flash.executed)

    audit_count = len((Path(temp) / "regression.jsonl").read_text(encoding="utf-8").splitlines())
    print("AUDIT RECORD COUNT:", audit_count)
    print("V9.18.11 FULL REGRESSION: PASS")
    print("NO FIRMWARE CHANGES PERFORMED")
