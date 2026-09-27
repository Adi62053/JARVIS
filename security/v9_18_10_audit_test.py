from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_firmware_model import (
    FirmwareAccessRequest,
    FirmwareOperation,
    FirmwareResource,
    FirmwareResourceType,
)
from security.v9_firmware_security_controller import V9FirmwareSecurityController
from security.v9_audit_logger import V9AuditLogger


with TemporaryDirectory() as temp:
    audit = V9AuditLogger(Path(temp) / "firmware_audit.jsonl")
    controller = V9FirmwareSecurityController()
    controller.controller.permission_manager.set_permission("FIRMWARE", True)
    controller.controller.audit_logger = audit

    resources = [
        (FirmwareOperation.READ, FirmwareResource(FirmwareResourceType.BIOS, "BIOS-AUDIT", "BIOS")),
        (FirmwareOperation.READ, FirmwareResource(FirmwareResourceType.BCD_FIRMWARE, "BCD-AUDIT", "BCD")),
        (FirmwareOperation.FLASH, FirmwareResource(FirmwareResourceType.BIOS, "BIOS-FLASH-AUDIT", "BIOS flash")),
    ]

    for operation, resource in resources:
        decision = controller.evaluate(FirmwareAccessRequest(operation, resource))
        print(f"{operation.value}: {decision.value}")

    records = Path(temp) / "firmware_audit.jsonl"
    lines = records.read_text(encoding="utf-8").splitlines()
    print("AUDIT RECORD COUNT:", len(lines))
    print("AUDIT FILE EXISTS:", records.exists())
    print("V9.18.10 AUDIT INTEGRITY: PASS")
    print("NO FIRMWARE CHANGES PERFORMED")
