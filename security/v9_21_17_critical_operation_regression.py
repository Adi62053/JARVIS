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
    audit_path = Path(temp_dir) / "critical_emergency_audit.jsonl"

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

    operation_id = "firmware.flash"
    capability = "firmware"
    resource = "BIOS"

    # Critical firmware mutation must remain elevation protected.
    normal = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.CRITICAL,
        required_privilege=SecurityPrivilegeLevel.SYSTEM,
    )

    assert normal == SecurityDecision.REQUIRE_ELEVATION
    print("CRITICAL OPERATION NORMAL: PASS")

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
    print("CRITICAL OPERATION EMERGENCY BLOCK: PASS")

    # Even explicit authorization cannot bypass emergency stop.
    controller.authorization_manager.authorize(operation_id)

    blocked_with_auth = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.CRITICAL,
        required_privilege=SecurityPrivilegeLevel.SYSTEM,
    )

    assert blocked_with_auth == SecurityDecision.DENY
    print("EMERGENCY OVERRIDES CRITICAL AUTHORIZATION: PASS")

    # No actual firmware operation is performed by this test.
    mutation_executed = False

    assert mutation_executed is False
    print("NO FIRMWARE MUTATION EXECUTED: PASS")

    # Clear emergency stop.
    emergency.deactivate()

    restored = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.CRITICAL,
        required_privilege=SecurityPrivilegeLevel.SYSTEM,
    )

    assert restored == SecurityDecision.REQUIRE_ELEVATION
    print("CRITICAL SECURITY BOUNDARY RESTORATION: PASS")

    records = audit_path.read_text(encoding="utf-8").splitlines()

    assert len(records) == 4
    assert any("EMERGENCY_STOP_ACTIVE" in line for line in records)

    print("CRITICAL OPERATION AUDIT: PASS")
    print("AUDIT RECORD COUNT:", len(records))
    print("V9.21.17 CRITICAL OPERATION EMERGENCY REGRESSION: PASS")
