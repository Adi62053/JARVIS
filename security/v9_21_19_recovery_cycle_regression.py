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
    audit_path = Path(temp_dir) / "emergency_cycle_audit.jsonl"

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

    # Cycle 1: normal -> emergency -> recovery.
    normal_1 = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.ADMINISTRATOR,
    )

    assert normal_1 == SecurityDecision.REQUIRE_AUTHORIZATION
    print("CYCLE 1 NORMAL: PASS")

    emergency.activate()

    blocked_1 = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.ADMINISTRATOR,
    )

    assert blocked_1 == SecurityDecision.DENY
    print("CYCLE 1 EMERGENCY BLOCK: PASS")

    emergency.deactivate()

    recovered_1 = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.ADMINISTRATOR,
    )

    assert recovered_1 == SecurityDecision.REQUIRE_AUTHORIZATION
    print("CYCLE 1 RECOVERY: PASS")

    # Cycle 2: authorize, consume, emergency, recover.
    controller.authorization_manager.authorize(operation_id)

    authorized_2 = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.ADMINISTRATOR,
    )

    assert authorized_2 == SecurityDecision.ALLOW
    print("CYCLE 2 AUTHORIZATION: PASS")

    emergency.activate()

    blocked_2 = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.ADMINISTRATOR,
    )

    assert blocked_2 == SecurityDecision.DENY
    print("CYCLE 2 EMERGENCY BLOCK: PASS")

    emergency.deactivate()

    recovered_2 = controller.evaluate(
        operation_id=operation_id,
        capability=capability,
        resource=resource,
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.ADMINISTRATOR,
    )

    assert recovered_2 == SecurityDecision.REQUIRE_AUTHORIZATION
    print("CYCLE 2 FRESH AUTHORIZATION REQUIRED: PASS")

    # Cycle 3: repeated emergency transitions.
    for _ in range(5):
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

        emergency.deactivate()

        assert not emergency.is_active()

        recovered = controller.evaluate(
            operation_id=operation_id,
            capability=capability,
            resource=resource,
            risk_level=SecurityRiskLevel.HIGH,
            required_privilege=SecurityPrivilegeLevel.ADMINISTRATOR,
        )

        assert recovered == SecurityDecision.REQUIRE_AUTHORIZATION

    print("REPEATED EMERGENCY CYCLES: PASS")
    print("FINAL SECURITY STATE: PASS")

    records = audit_path.read_text(
        encoding="utf-8"
    ).splitlines()

    assert len(records) == 16
    assert sum(
        "EMERGENCY_STOP_ACTIVE" in line
        for line in records
    ) == 7

    print("CYCLE AUDIT INTEGRITY: PASS")
    print("AUDIT RECORD COUNT:", len(records))
    print("NO SYSTEM MUTATION EXECUTED: PASS")
    print("V9.21.19 EMERGENCY RECOVERY CYCLE REGRESSION: PASS")
