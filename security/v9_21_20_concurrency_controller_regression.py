from concurrent.futures import ThreadPoolExecutor
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
    audit_path = Path(temp_dir) / "concurrent_controller_audit.jsonl"

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

    def activate():
        emergency.activate()
        return emergency.is_active()

    with ThreadPoolExecutor(max_workers=32) as executor:
        activation_results = list(
            executor.map(
                lambda _: activate(),
                range(32),
            )
        )

    assert all(activation_results)
    assert emergency.is_active()

    print("CONCURRENT EMERGENCY ACTIVATION: PASS")

    def evaluate_blocked():
        return controller.evaluate(**operation)

    with ThreadPoolExecutor(max_workers=32) as executor:
        blocked_results = list(
            executor.map(
                lambda _: evaluate_blocked(),
                range(32),
            )
        )

    assert all(
        result == SecurityDecision.DENY
        for result in blocked_results
    )

    print("CONCURRENT CONTROLLER EMERGENCY BLOCK: PASS")

    def deactivate():
        emergency.deactivate()
        return emergency.is_active()

    with ThreadPoolExecutor(max_workers=32) as executor:
        clear_results = list(
            executor.map(
                lambda _: deactivate(),
                range(32),
            )
        )

    assert not emergency.is_active()
    assert not any(clear_results)

    print("CONCURRENT EMERGENCY CLEAR: PASS")

    recovered = controller.evaluate(**operation)

    assert recovered == SecurityDecision.REQUIRE_AUTHORIZATION

    print("CONTROLLER RECOVERY AFTER CONCURRENCY: PASS")

    records = audit_path.read_text(
        encoding="utf-8"
    ).splitlines()

    emergency_records = [
        line
        for line in records
        if "EMERGENCY_STOP_ACTIVE" in line
    ]

    print("AUDIT RECORD COUNT:", len(records))
    print(
        "EMERGENCY AUDIT RECORD COUNT:",
        len(emergency_records),
    )
    print("CONCURRENT AUDIT DIAGNOSTIC: COMPLETE")
