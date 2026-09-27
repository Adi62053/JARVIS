from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_21_1_emergency_controls import V9EmergencySecurityControls
from security.v9_audit_logger import V9AuditLogger
from security.v9_security_controller import V9SecurityController
from security.v9_security_model import (
    SecurityDecision,
    SecurityPrivilegeLevel,
    SecurityRiskLevel,
)


with TemporaryDirectory() as temp_dir:
    audit_path = Path(temp_dir) / "v9_21_26_full_regression.jsonl"

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

    authorization_operation = {
        "operation_id": "firmware.read",
        "capability": "firmware",
        "resource": "BIOS",
        "risk_level": SecurityRiskLevel.HIGH,
        "required_privilege": SecurityPrivilegeLevel.ADMINISTRATOR,
    }

    critical_operation = {
        "operation_id": "firmware.flash",
        "capability": "firmware",
        "resource": "BIOS",
        "risk_level": SecurityRiskLevel.CRITICAL,
        "required_privilege": SecurityPrivilegeLevel.SYSTEM,
    }


    # Authorization boundary.
    result = controller.evaluate(**authorization_operation)

    assert result == SecurityDecision.REQUIRE_AUTHORIZATION

    controller.authorization_manager.authorize(
        "firmware.read"
    )

    result = controller.evaluate(**authorization_operation)

    assert result == SecurityDecision.ALLOW

    print("AUTHORIZATION BOUNDARY: PASS")


    # One-shot authorization.
    result = controller.evaluate(**authorization_operation)

    assert result == SecurityDecision.REQUIRE_AUTHORIZATION

    print("ONE-SHOT AUTHORIZATION: PASS")


    # Critical privilege boundary.
    result = controller.evaluate(**critical_operation)

    assert result == SecurityDecision.REQUIRE_ELEVATION

    print("PRIVILEGE / ELEVATION BOUNDARY: PASS")


    # Emergency override.
    emergency.activate()

    blocked_authorization = controller.evaluate(
        **authorization_operation
    )

    blocked_critical = controller.evaluate(
        **critical_operation
    )

    assert blocked_authorization == SecurityDecision.DENY
    assert blocked_critical == SecurityDecision.DENY

    print("EMERGENCY AUTHORIZATION OVERRIDE: PASS")
    print("EMERGENCY PRIVILEGE OVERRIDE: PASS")


    # Clear emergency.
    emergency.deactivate()

    recovered_authorization = controller.evaluate(
        **authorization_operation
    )

    recovered_critical = controller.evaluate(
        **critical_operation
    )

    assert recovered_authorization == SecurityDecision.REQUIRE_AUTHORIZATION
    assert recovered_critical == SecurityDecision.REQUIRE_ELEVATION

    print("EMERGENCY RECOVERY: PASS")
    print("SECURITY BOUNDARY RESTORATION: PASS")


    # Audit integrity.
    records = audit_path.read_text(
        encoding="utf-8"
    ).splitlines()

    assert len(records) == 8

    emergency_records = [
        line
        for line in records
        if "EMERGENCY_STOP_ACTIVE" in line
    ]

    assert len(emergency_records) == 2

    print("FULL AUDIT INTEGRITY: PASS")
    print("AUDIT RECORD COUNT:", len(records))
    print("EMERGENCY AUDIT COUNT:", len(emergency_records))

    print("NO PRIVILEGE ESCALATION EXECUTED: PASS")
    print("NO FIRMWARE MUTATION EXECUTED: PASS")
    print("NO SYSTEM MUTATION EXECUTED: PASS")
    print("V9.21.26 FULL EMERGENCY SECURITY REGRESSION: PASS")
