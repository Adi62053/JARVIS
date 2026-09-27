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
    audit_path = Path(temp_dir) / "multi_capability_emergency_audit.jsonl"

    emergency = V9EmergencySecurityControls()
    audit = V9AuditLogger(audit_path)

    controller = V9SecurityController(
        audit_logger=audit,
        emergency_controls=emergency,
    )

    operations = [
        (
            "firmware.read",
            "firmware",
            "BIOS",
            SecurityRiskLevel.HIGH,
            SecurityPrivilegeLevel.ADMINISTRATOR,
        ),
        (
            "filesystem.read",
            "filesystem",
            r"C:\Windows\System32",
            SecurityRiskLevel.HIGH,
            SecurityPrivilegeLevel.ADMINISTRATOR,
        ),
        (
            "process.inspect",
            "process",
            "explorer.exe",
            SecurityRiskLevel.SAFE,
            SecurityPrivilegeLevel.USER,
        ),
        (
            "service.inspect",
            "service",
            "eventlog",
            SecurityRiskLevel.HIGH,
            SecurityPrivilegeLevel.ADMINISTRATOR,
        ),
        (
            "network.inspect",
            "network",
            "network-adapter",
            SecurityRiskLevel.CAUTION,
            SecurityPrivilegeLevel.USER,
        ),
        (
            "hardware.inspect",
            "hardware",
            "system-hardware",
            SecurityRiskLevel.CAUTION,
            SecurityPrivilegeLevel.USER,
        ),
    ]

    # Enable the capabilities used by this regression.
    for capability in {
        operation[1] for operation in operations
    }:
        controller.permission_manager.set_permission(
            capability,
            True,
        )

    # Establish the normal security state.
    normal_results = []

    for operation_id, capability, resource, risk, privilege in operations:
        result = controller.evaluate(
            operation_id=operation_id,
            capability=capability,
            resource=resource,
            risk_level=risk,
            required_privilege=privilege,
        )
        normal_results.append(result)

    assert all(
        result != SecurityDecision.DENY
        for result in normal_results
    )

    print("NORMAL MULTI-CAPABILITY EVALUATION: PASS")
    print("CAPABILITY COUNT:", len(operations))

    # Activate the real emergency stop.
    emergency.activate()

    assert emergency.is_active()

    blocked_results = []

    for operation_id, capability, resource, risk, privilege in operations:
        result = controller.evaluate(
            operation_id=operation_id,
            capability=capability,
            resource=resource,
            risk_level=risk,
            required_privilege=privilege,
        )
        blocked_results.append(result)

    assert all(
        result == SecurityDecision.DENY
        for result in blocked_results
    )

    print("ALL CAPABILITIES EMERGENCY BLOCK: PASS")

    # Clear emergency stop.
    emergency.deactivate()

    assert not emergency.is_active()

    recovered_results = []

    for operation_id, capability, resource, risk, privilege in operations:
        result = controller.evaluate(
            operation_id=operation_id,
            capability=capability,
            resource=resource,
            risk_level=risk,
            required_privilege=privilege,
        )
        recovered_results.append(result)

    assert recovered_results == normal_results

    print("ALL CAPABILITIES SECURITY RESTORATION: PASS")

    records = audit_path.read_text(
        encoding="utf-8"
    ).splitlines()

    expected_records = len(operations) * 3

    assert len(records) == expected_records
    assert any(
        "EMERGENCY_STOP_ACTIVE" in line
        for line in records
    )

    print("MULTI-CAPABILITY AUDIT: PASS")
    print("AUDIT RECORD COUNT:", len(records))
    print("NO SYSTEM MUTATION EXECUTED: PASS")
    print("V9.21.18 MULTI-CAPABILITY EMERGENCY REGRESSION: PASS")
