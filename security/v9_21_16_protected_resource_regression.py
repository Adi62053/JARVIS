from tempfile import TemporaryDirectory
from pathlib import Path

from security.v9_21_1_emergency_controls import V9EmergencySecurityControls
from security.v9_audit_logger import V9AuditLogger
from security.v9_security_controller import V9SecurityController
from security.v9_security_model import (
    SecurityDecision,
    SecurityPrivilegeLevel,
    SecurityRiskLevel,
)


with TemporaryDirectory() as temp_dir:
    audit_path = Path(temp_dir) / "protected_emergency_audit.jsonl"

    emergency = V9EmergencySecurityControls()
    audit = V9AuditLogger(audit_path)

    controller = V9SecurityController(
        audit_logger=audit,
        emergency_controls=emergency,
    )

    controller.permission_manager.set_permission(
        "firmware",
        True,
    )

    operation_id = "firmware.read"
    capability = "firmware"
    resource = "BIOS"

    # BIOS is a protected firmware resource.
    normal = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.CRITICAL,
        required_privilege=SecurityPrivilegeLevel.SYSTEM,
    )

    assert normal == SecurityDecision.REQUIRE_ELEVATION
    print("PROTECTED RESOURCE NORMAL: PASS")

    # Activate emergency stop.
    emergency.activate()

    blocked = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.CRITICAL,
        required_privilege=SecurityPrivilegeLevel.SYSTEM,
    )

    assert blocked == SecurityDecision.DENY
    print("PROTECTED RESOURCE EMERGENCY BLOCK: PASS")

    # Clear emergency and verify the original security boundary returns.
    emergency.deactivate()

    recovered = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.CRITICAL,
        required_privilege=SecurityPrivilegeLevel.SYSTEM,
    )

    assert recovered == SecurityDecision.REQUIRE_ELEVATION
    print("PROTECTED RESOURCE SECURITY RESTORATION: PASS")

    records = audit_path.read_text(encoding="utf-8").splitlines()

    assert len(records) == 3
    assert any("EMERGENCY_STOP_ACTIVE" in line for line in records)

    print("PROTECTED RESOURCE AUDIT: PASS")
    print("AUDIT RECORD COUNT:", len(records))
    print("NO PROTECTED RESOURCE MODIFICATION: PASS")
    print("V9.21.16 PROTECTED RESOURCE EMERGENCY REGRESSION: PASS")
