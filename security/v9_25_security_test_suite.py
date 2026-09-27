"""
JARVIS V9.25 - Master Security Test Suite

Consolidated regression coverage for the V9 security architecture.

This suite:
- tests security decisions without executing privileged operations
- uses temporary audit storage
- verifies the core V9 security contracts
- verifies protected-resource classification
- verifies emergency-stop enforcement
- verifies audit integrity
- performs no real system, firmware, registry, process, or service mutation
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from tempfile import TemporaryDirectory

from security.v9_21_1_emergency_controls import (
    V9EmergencySecurityControls,
)
from security.v9_audit_logger import V9AuditLogger
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_elevation import V9ElevationManager
from security.v9_permission_manager import V9PermissionManager
from security.v9_policy_engine import V9PolicyEngine
from security.v9_privilege_manager import V9PrivilegeManager
from security.v9_protection_manager import (
    ProtectionLevel,
    V9ProtectionManager,
)
from security.v9_security_controller import V9SecurityController
from security.v9_security_model import (
    AuthorizationState,
    SecurityDecision,
    SecurityPrivilegeLevel,
    SecurityRiskLevel,
)


def test_security_model() -> None:
    assert {level.value for level in SecurityRiskLevel} == {
        "SAFE",
        "CAUTION",
        "HIGH",
        "CRITICAL",
    }

    assert {level.value for level in SecurityPrivilegeLevel} == {
        "USER",
        "ADMINISTRATOR",
        "SYSTEM",
        "FIRMWARE",
        "HARDWARE",
    }

    assert {state.value for state in AuthorizationState} == {
        "NOT_REQUIRED",
        "REQUIRED",
        "AUTHORIZED",
        "DENIED",
    }

    assert {decision.value for decision in SecurityDecision} == {
        "ALLOW",
        "REQUIRE_AUTHORIZATION",
        "REQUIRE_ELEVATION",
        "DENY",
    }

    print("SECURITY MODEL: PASS")


def test_permission_manager() -> None:
    manager = V9PermissionManager()

    assert manager.is_allowed("APPLICATION") is False
    assert manager.is_configured("APPLICATION") is False

    manager.set_permission("APPLICATION", True)

    assert manager.is_allowed("APPLICATION") is True
    assert manager.is_configured("APPLICATION") is True

    manager.set_permission("APPLICATION", False)

    assert manager.is_allowed("APPLICATION") is False

    permissions = manager.get_permissions()
    permissions["APPLICATION"] = True

    assert manager.is_allowed("APPLICATION") is False

    assert manager.remove_permission("APPLICATION") is True
    assert manager.remove_permission("APPLICATION") is False
    assert manager.is_configured("APPLICATION") is False

    print("PERMISSION MANAGER: PASS")


def test_policy_engine() -> None:
    policy = V9PolicyEngine()

    expected = {
        SecurityRiskLevel.SAFE: {
            SecurityPrivilegeLevel.USER: SecurityDecision.ALLOW,
            SecurityPrivilegeLevel.ADMINISTRATOR: SecurityDecision.ALLOW,
            SecurityPrivilegeLevel.SYSTEM: SecurityDecision.ALLOW,
            SecurityPrivilegeLevel.FIRMWARE: SecurityDecision.ALLOW,
            SecurityPrivilegeLevel.HARDWARE: SecurityDecision.ALLOW,
        },
        SecurityRiskLevel.CAUTION: {
            SecurityPrivilegeLevel.USER: SecurityDecision.ALLOW,
            SecurityPrivilegeLevel.ADMINISTRATOR: SecurityDecision.ALLOW,
            SecurityPrivilegeLevel.SYSTEM: SecurityDecision.ALLOW,
            SecurityPrivilegeLevel.FIRMWARE: SecurityDecision.ALLOW,
            SecurityPrivilegeLevel.HARDWARE: SecurityDecision.ALLOW,
        },
        SecurityRiskLevel.HIGH: {
            SecurityPrivilegeLevel.USER: SecurityDecision.REQUIRE_AUTHORIZATION,
            SecurityPrivilegeLevel.ADMINISTRATOR: SecurityDecision.REQUIRE_AUTHORIZATION,
            SecurityPrivilegeLevel.SYSTEM: SecurityDecision.REQUIRE_AUTHORIZATION,
            SecurityPrivilegeLevel.FIRMWARE: SecurityDecision.REQUIRE_ELEVATION,
            SecurityPrivilegeLevel.HARDWARE: SecurityDecision.REQUIRE_ELEVATION,
        },
        SecurityRiskLevel.CRITICAL: {
            SecurityPrivilegeLevel.USER: SecurityDecision.REQUIRE_AUTHORIZATION,
            SecurityPrivilegeLevel.ADMINISTRATOR: SecurityDecision.REQUIRE_AUTHORIZATION,
            SecurityPrivilegeLevel.SYSTEM: SecurityDecision.REQUIRE_AUTHORIZATION,
            SecurityPrivilegeLevel.FIRMWARE: SecurityDecision.REQUIRE_AUTHORIZATION,
            SecurityPrivilegeLevel.HARDWARE: SecurityDecision.REQUIRE_AUTHORIZATION,
        },
    }

    for risk, privilege_map in expected.items():
        for privilege, decision in privilege_map.items():
            assert policy.evaluate(risk, privilege) == decision

    print("POLICY ENGINE 20-CASE MATRIX: PASS")


def test_authorization_manager() -> None:
    manager = V9AuthorizationManager()

    operation = "v9.25.authorization"

    assert manager.is_authorized(operation) is False

    manager.authorize(operation)
    assert manager.is_authorized(operation) is True

    assert manager.consume(operation) is True
    assert manager.is_authorized(operation) is False
    assert manager.consume(operation) is False

    manager.authorize(operation)
    assert manager.deny(operation) is True
    assert manager.deny(operation) is False

    manager.authorize("operation.one")
    manager.authorize("operation.two")
    manager.clear()

    assert manager.get_authorized_operations() == set()

    print("AUTHORIZATION MANAGER ONE-SHOT: PASS")


def test_elevation_detection() -> None:
    privilege_manager = V9PrivilegeManager()
    elevation = V9ElevationManager(
        privilege_manager=privilege_manager,
    )

    current = elevation.get_current_privilege()

    assert isinstance(current, SecurityPrivilegeLevel)

    status = elevation.get_status(current)

    assert status["current_privilege"] == current.value
    assert status["required_privilege"] == current.value
    assert status["elevation_required"] is False
    assert status["access_available"] is True

    print("ELEVATION DETECTION: PASS")
    print("CURRENT PRIVILEGE:", current.value)


def test_protection_manager() -> None:
    protection = V9ProtectionManager()

    assert (
        protection.classify_path(r"C:\Windows\System32")
        == ProtectionLevel.PROTECTED
    )

    assert (
        protection.classify_path(r"C:\Windows\SysWOW64")
        == ProtectionLevel.PROTECTED
    )

    assert (
        protection.classify_path(r"C:\Windows\Boot")
        == ProtectionLevel.PROTECTED
    )

    assert (
        protection.classify_path(r"C:\Windows\WinSxS")
        == ProtectionLevel.PROTECTED
    )

    assert (
        protection.classify_path(r"C:\Windows")
        == ProtectionLevel.CRITICAL
    )

    assert (
        protection.classify_path(r"C:\Program Files")
        == ProtectionLevel.CRITICAL
    )

    assert (
        protection.classify_path(r"C:\Users")
        == ProtectionLevel.SENSITIVE
    )

    assert (
        protection.classify_path(r"C:\V9_25_SAFE_TEST")
        == ProtectionLevel.ORDINARY
    )

    assert (
        protection.classify_process("lsass.exe")
        == ProtectionLevel.PROTECTED
    )

    assert (
        protection.classify_process("example.exe")
        == ProtectionLevel.ORDINARY
    )

    assert (
        protection.classify_service("eventlog")
        == ProtectionLevel.PROTECTED
    )

    assert (
        protection.classify_service("v9_25_example_service")
        == ProtectionLevel.ORDINARY
    )

    assert protection.is_protected(ProtectionLevel.PROTECTED) is True
    assert protection.is_protected(ProtectionLevel.ORDINARY) is False

    assert (
        protection.requires_extra_protection(
            ProtectionLevel.SENSITIVE
        )
        is True
    )

    assert (
        protection.requires_extra_protection(
            ProtectionLevel.ORDINARY
        )
        is False
    )

    print("PROTECTION BOUNDARIES: PASS")


def test_controller_and_audit() -> None:
    with TemporaryDirectory() as temp_dir:
        audit_path = Path(temp_dir) / "v9_25_controller.jsonl"

        audit = V9AuditLogger(audit_path)
        emergency = V9EmergencySecurityControls()

        controller = V9SecurityController(
            audit_logger=audit,
            emergency_controls=emergency,
        )

        operation = {
            "operation_id": "v9.25.application.allow",
            "capability": "APPLICATION",
            "resource": "v9_25_test_application",
            "risk_level": SecurityRiskLevel.CAUTION,
            "required_privilege": SecurityPrivilegeLevel.USER,
        }

        assert (
            controller.evaluate(**operation)
            == SecurityDecision.DENY
        )

        controller.permission_manager.set_permission(
            "APPLICATION",
            True,
        )

        assert (
            controller.evaluate(**operation)
            == SecurityDecision.ALLOW
        )

        authorization_operation = {
            "operation_id": "v9.25.application.authorization",
            "capability": "APPLICATION",
            "resource": "v9_25_authorized_application",
            "risk_level": SecurityRiskLevel.HIGH,
            "required_privilege": SecurityPrivilegeLevel.USER,
        }

        assert (
            controller.evaluate(**authorization_operation)
            == SecurityDecision.REQUIRE_AUTHORIZATION
        )

        controller.authorization_manager.authorize(
            authorization_operation["operation_id"]
        )

        assert (
            controller.evaluate(**authorization_operation)
            == SecurityDecision.ALLOW
        )

        assert (
            controller.evaluate(**authorization_operation)
            == SecurityDecision.REQUIRE_AUTHORIZATION
        )

        records = [
            json.loads(line)
            for line in audit_path.read_text(
                encoding="utf-8",
            ).splitlines()
        ]

        assert len(records) == 5

        required_fields = {
            "timestamp",
            "operation_id",
            "capability",
            "resource",
            "risk_level",
            "required_privilege",
            "current_privilege",
            "authorization_state",
            "decision",
            "result",
        }

        for record in records:
            assert required_fields.issubset(record.keys())

        assert records[0]["decision"] == "DENY"
        assert records[0]["result"] == "PERMISSION_DENIED"
        assert records[1]["decision"] == "ALLOW"
        assert records[1]["result"] == "AUTHORIZED_BY_POLICY"
        assert records[2]["decision"] == "REQUIRE_AUTHORIZATION"
        assert records[2]["result"] == "AUTHORIZATION_REQUIRED"
        assert records[3]["decision"] == "ALLOW"
        assert records[3]["result"] == "EXPLICIT_AUTHORIZATION_CONSUMED"
        assert records[4]["decision"] == "REQUIRE_AUTHORIZATION"
        assert records[4]["result"] == "AUTHORIZATION_REQUIRED"

    print("CONTROLLER + AUDIT: PASS")


def test_emergency_controls() -> None:
    with TemporaryDirectory() as temp_dir:
        audit_path = Path(temp_dir) / "v9_25_emergency.jsonl"

        audit = V9AuditLogger(audit_path)
        emergency = V9EmergencySecurityControls()

        controller = V9SecurityController(
            audit_logger=audit,
            emergency_controls=emergency,
        )

        controller.permission_manager.set_permission(
            "APPLICATION",
            True,
        )

        operation = {
            "operation_id": "v9.25.emergency",
            "capability": "APPLICATION",
            "resource": "v9_25_emergency_test",
            "risk_level": SecurityRiskLevel.HIGH,
            "required_privilege": SecurityPrivilegeLevel.USER,
        }

        assert emergency.is_active() is False

        controller.authorization_manager.authorize(
            operation["operation_id"]
        )

        emergency.activate()

        assert emergency.is_active() is True

        assert (
            controller.evaluate(**operation)
            == SecurityDecision.DENY
        )

        assert (
            controller.evaluate(
                operation_id="v9.25.emergency.critical",
                capability="APPLICATION",
                resource="v9_25_critical_test",
                risk_level=SecurityRiskLevel.CRITICAL,
                required_privilege=SecurityPrivilegeLevel.SYSTEM,
            )
            == SecurityDecision.DENY
        )

        emergency.deactivate()

        assert emergency.is_active() is False

        assert (
            controller.evaluate(**operation)
            == SecurityDecision.ALLOW
        )

        assert (
            controller.evaluate(**operation)
            == SecurityDecision.REQUIRE_AUTHORIZATION
        )

        records = [
            json.loads(line)
            for line in audit_path.read_text(
                encoding="utf-8",
            ).splitlines()
        ]

        emergency_records = [
            record
            for record in records
            if record["result"] == "EMERGENCY_STOP_ACTIVE"
        ]

        assert len(emergency_records) == 2
        assert all(
            record["decision"] == "DENY"
            for record in emergency_records
        )

    print("EMERGENCY STOP + RECOVERY: PASS")


def main() -> None:
    print()
    print("=" * 60)
    print("JARVIS V9.25 MASTER SECURITY TEST SUITE")
    print("=" * 60)
    print()

    tests = (
        test_security_model,
        test_permission_manager,
        test_policy_engine,
        test_authorization_manager,
        test_elevation_detection,
        test_protection_manager,
        test_controller_and_audit,
        test_emergency_controls,
    )

    for test in tests:
        test()

    print()
    print("=" * 60)
    print("V9.25 SECURITY TEST SUITE: PASS")
    print("=" * 60)


if __name__ == "__main__":
    main()


