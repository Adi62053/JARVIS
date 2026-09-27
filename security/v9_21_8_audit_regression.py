from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_21_1_emergency_controls import V9EmergencySecurityControls
from security.v9_audit_logger import V9AuditLogger
from security.v9_capability_model import SecurityCapability
from security.v9_firmware_model import (
    FirmwareAccessRequest,
    FirmwareOperation,
    FirmwareResource,
    FirmwareResourceType,
)
from security.v9_firmware_security_controller import V9FirmwareSecurityController
from security.v9_security_model import SecurityDecision


with TemporaryDirectory() as temp_dir:
    audit_path = Path(temp_dir) / "emergency_audit.jsonl"

    emergency = V9EmergencySecurityControls()
    audit_logger = V9AuditLogger(audit_path)

    controller = V9FirmwareSecurityController()

    # Replace only the controller's audit logger for this isolated test.
    controller.controller.audit_logger = audit_logger

    controller.controller.permission_manager.set_permission(
        SecurityCapability.FIRMWARE.value,
        True
    )

    resource = FirmwareResource(
        FirmwareResourceType.BCD_FIRMWARE,
        "BCD-V9218",
        "Emergency audit regression",
    )

    request = FirmwareAccessRequest(
        FirmwareOperation.READ,
        resource,
    )

    # Normal evaluation.
    normal = controller.evaluate(request)
    assert normal == SecurityDecision.REQUIRE_AUTHORIZATION

    # Attach emergency enforcement.
    original_evaluate = controller.evaluate

    def emergency_protected_evaluate(request):
        emergency.require_emergency_clear()
        return original_evaluate(request)

    controller.evaluate = emergency_protected_evaluate

    # Emergency stop.
    emergency.activate()

    try:
        controller.evaluate(request)
    except PermissionError:
        blocked = True
    else:
        blocked = False

    assert blocked

    # Clear emergency stop.
    emergency.deactivate()

    restored = controller.evaluate(request)
    assert restored == SecurityDecision.REQUIRE_AUTHORIZATION

    # Audit file must exist.
    assert audit_path.exists()

    lines = audit_path.read_text(encoding="utf-8").splitlines()

    # Two security evaluations should be audited:
    # normal evaluation + post-emergency evaluation.
    assert len(lines) == 2

    print("NORMAL AUDIT RECORD: PASS")
    print("EMERGENCY BLOCK: PASS")
    print("AUDIT FILE CREATION: PASS")
    print("AUDIT RECORD COUNT: PASS")
    print("EMERGENCY CLEAR: PASS")
    print("POST-EMERGENCY AUDIT: PASS")
    print("V9.21.8 EMERGENCY + AUDIT REGRESSION: PASS")
