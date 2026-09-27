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
    audit_path = Path(temp_dir) / "emergency_audit.jsonl"

    emergency = V9EmergencySecurityControls()
    audit = V9AuditLogger(audit_path)

    controller = V9SecurityController(
        audit_logger=audit,
        emergency_controls=emergency,
    )

    capability = "firmware"
    operation_id = "firmware.read"
    resource = "BIOS"

    controller.permission_manager.set_permission(
        capability,
        True,
    )

    # Normal operation must require authorization.
    normal = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.ADMINISTRATOR,
    )

    assert normal == SecurityDecision.REQUIRE_AUTHORIZATION
    print("NORMAL CONTROLLER EVALUATION: PASS")

    # Activate the real emergency control.
    emergency.activate()

    assert emergency.is_active()

    blocked = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.ADMINISTRATOR,
    )

    assert blocked == SecurityDecision.DENY
    print("REAL EMERGENCY CONTROLLER BLOCK: PASS")

    # Emergency decision must be independent of authorization.
    controller.authorization_manager.authorize(operation_id)

    blocked_with_authorization = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.ADMINISTRATOR,
    )

    assert blocked_with_authorization == SecurityDecision.DENY
    print("EMERGENCY OVERRIDES AUTHORIZATION: PASS")

    # Clear emergency state.
    emergency.deactivate()

    assert not emergency.is_active()

    recovered = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.ADMINISTRATOR,
    )

    assert recovered == SecurityDecision.ALLOW
    print("EMERGENCY CLEAR + CONTROLLER RECOVERY: PASS")

    # Emergency-blocked evaluations must be auditable.
    records = audit_path.read_text(encoding="utf-8").splitlines()

    assert len(records) == 4
    assert any("EMERGENCY_STOP_ACTIVE" in line for line in records)

    print("EMERGENCY AUDIT RECORDING: PASS")
    print("AUDIT RECORD COUNT:", len(records))
    print("V9.21.15 REAL EMERGENCY CONTROLLER INTEGRATION: PASS")
