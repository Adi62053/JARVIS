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
    audit_path = Path(temp_dir) / "v9_21_25_audit.jsonl"

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

    operation = {
        "operation_id": "firmware.read",
        "capability": "firmware",
        "resource": "BIOS",
        "risk_level": SecurityRiskLevel.HIGH,
        "required_privilege": SecurityPrivilegeLevel.ADMINISTRATOR,
    }

    normal = controller.evaluate(**operation)

    assert normal == SecurityDecision.REQUIRE_AUTHORIZATION

    print("NORMAL AUDIT DECISION: PASS")

    emergency.activate()

    blocked = controller.evaluate(**operation)

    assert blocked == SecurityDecision.DENY

    print("EMERGENCY BLOCK DECISION: PASS")

    emergency.deactivate()

    recovered = controller.evaluate(**operation)

    assert recovered == SecurityDecision.REQUIRE_AUTHORIZATION

    print("POST-EMERGENCY DECISION: PASS")

    records = audit_path.read_text(
        encoding="utf-8"
    ).splitlines()

    assert len(records) == 3

    emergency_records = [
        line
        for line in records
        if "EMERGENCY_STOP_ACTIVE" in line
    ]

    assert len(emergency_records) == 1

    print("EMERGENCY AUDIT RECORD: PASS")
    print("AUDIT RECORD COUNT:", len(records))
    print("AUDIT INTEGRITY: PASS")
    print("V9.21.25 EMERGENCY + AUDIT INTEGRITY REGRESSION: PASS")
