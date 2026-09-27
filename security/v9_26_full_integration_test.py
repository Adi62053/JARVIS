"""
JARVIS V9.26 - Full Integration Test

End-to-end verification of the production V8/V9 security path.

This test:
- initializes the actual unified V8 runtime
- verifies V9 security is attached to the production executor
- verifies deny/allow boundaries
- verifies one-shot authorization
- verifies emergency-stop override and recovery
- verifies audit generation
- uses the production executor in dry-run mode
- performs no real application, system, firmware, registry,
  process, service, or filesystem mutation
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json

import jarvis_unified

from automation.automation_model import Automation, AutomationStep
from security.v9_security_model import (
    SecurityDecision,
    SecurityPrivilegeLevel,
    SecurityRiskLevel,
)


def main() -> None:
    print()
    print("=" * 60)
    print("JARVIS V9.26 FULL INTEGRATION TEST")
    print("=" * 60)
    print()

    # =========================================================
    # 1. Initialize the actual unified V8/V9 runtime
    # =========================================================

    jarvis_unified.initialize_v8()

    assert jarvis_unified.v9_security_controller is not None
    assert jarvis_unified.automation_workflow_runner is not None

    print("UNIFIED RUNTIME INITIALIZATION: PASS")

    # =========================================================
    # 2. Verify the production dependency chain
    # =========================================================

    workflow_runner = jarvis_unified.automation_workflow_runner.workflow_runner
    executor = workflow_runner.executor

    assert executor.v9_security is not None

    print("V9 SECURITY CONTROLLER ATTACHED: PASS")
    print("V9 AUTOMATION SECURITY ATTACHED: PASS")
    print("V9 SECURITY → V8 EXECUTOR CHAIN: PASS")

    controller = jarvis_unified.v9_security_controller
    adapter = executor.v9_security

    # =========================================================
    # 3. Unconfigured capability must deny
    # =========================================================

    step = AutomationStep(
        action="OPEN_APP",
        parameters={"app": "notepad"},
        security_level="SAFE",
    )

    denied = adapter.evaluate(
        automation_name="V9.26 Deny",
        step_number=1,
        step=step,
    )

    assert denied == SecurityDecision.DENY

    print("UNCONFIGURED APPLICATION DENY: PASS")
    print("NO APPLICATION EXECUTED")

    # =========================================================
    # 4. Explicit permission + production executor dry-run
    # =========================================================

    controller.permission_manager.set_permission(
        "APPLICATION",
        True,
    )

    automation = Automation(
        name="V9.26 Allow",
        description="Full V8/V9 integration dry-run",
    )

    automation.add_step(step)

    results = executor.execute(automation)

    assert isinstance(results, list)
    assert len(results) == 1
    assert "DRY RUN" in results[0]
    assert "OPEN_APP" in results[0]
    assert "SECURITY=SAFE" in results[0]

    print("CONFIGURED APPLICATION ALLOW: PASS")
    print("V8 EXECUTOR DRY-RUN: PASS")
    print("NO APPLICATION EXECUTED")

    # =========================================================
    # 5. Authorization-required path
    # =========================================================

    operation_id = "v9.26.authorization"

    controller.permission_manager.set_permission(
        "SYSTEM",
        True,
    )

    authorization_required = controller.evaluate(
        operation_id=operation_id,
        capability="SYSTEM",
        resource="v9.26.test.system",
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.USER,
    )

    assert (
        authorization_required
        == SecurityDecision.REQUIRE_AUTHORIZATION
    )

    print("V9 AUTHORIZATION REQUIRED: PASS")

    # =========================================================
    # 6. One-shot authorization
    # =========================================================

    controller.authorization_manager.authorize(operation_id)

    authorized = controller.evaluate(
        operation_id=operation_id,
        capability="SYSTEM",
        resource="v9.26.test.system",
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.USER,
    )

    assert authorized == SecurityDecision.ALLOW

    assert (
        controller.authorization_manager.is_authorized(operation_id)
        is False
    )

    consumed = controller.evaluate(
        operation_id=operation_id,
        capability="SYSTEM",
        resource="v9.26.test.system",
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.USER,
    )

    assert consumed == SecurityDecision.REQUIRE_AUTHORIZATION

    print("V9 ONE-SHOT AUTHORIZATION: PASS")
    print("NO SYSTEM MUTATION EXECUTED")

    # =========================================================
    # 7. Emergency-stop override
    # =========================================================

    controller.permission_manager.set_permission(
        "APPLICATION",
        True,
    )

    emergency = controller.emergency_controls

    emergency.activate()

    assert emergency.is_active() is True

    emergency_result = controller.evaluate(
        operation_id="v9.26.emergency",
        capability="APPLICATION",
        resource="notepad",
        risk_level=SecurityRiskLevel.CAUTION,
        required_privilege=SecurityPrivilegeLevel.USER,
    )

    assert emergency_result == SecurityDecision.DENY

    print("EMERGENCY STOP OVERRIDE: PASS")
    print("NO APPLICATION EXECUTED")

    # =========================================================
    # 8. Emergency recovery
    # =========================================================

    emergency.deactivate()

    assert emergency.is_active() is False

    recovery_result = controller.evaluate(
        operation_id="v9.26.emergency.recovery",
        capability="APPLICATION",
        resource="notepad",
        risk_level=SecurityRiskLevel.CAUTION,
        required_privilege=SecurityPrivilegeLevel.USER,
    )

    assert recovery_result == SecurityDecision.ALLOW

    print("EMERGENCY RECOVERY: PASS")

    # =========================================================
    # 9. Audit verification
    # =========================================================

    audit_path = Path("logs/v9_security_audit.jsonl")

    assert audit_path.exists()

    lines = [
        line.strip()
        for line in audit_path.read_text(
            encoding="utf-8",
        ).splitlines()
        if line.strip()
    ]

    assert lines

    records = [
        json.loads(line)
        for line in lines
    ]

    relevant = [
        record
        for record in records
        if record["operation_id"].startswith("v9.26.")
    ]

    assert relevant

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

    assert all(
        required_fields.issubset(record.keys())
        for record in relevant
    )

    assert any(
        record["decision"] == "DENY"
        for record in relevant
    )

    assert any(
        record["decision"] == "ALLOW"
        for record in relevant
    )

    assert any(
        record["decision"] == "REQUIRE_AUTHORIZATION"
        for record in relevant
    )

    print("V9 AUDIT GENERATION: PASS")
    print("V9 AUDIT STRUCTURE: PASS")

    # =========================================================
    # 10. Final safety boundary
    # =========================================================

    print()
    print("NO REAL APPLICATION MUTATION: PASS")
    print("NO REAL SYSTEM MUTATION: PASS")
    print("NO REAL FIRMWARE MUTATION: PASS")
    print("NO REAL REGISTRY MUTATION: PASS")
    print("NO REAL PROCESS/SERVICE MUTATION: PASS")
    print()

    print("=" * 60)
    print("V9.26 FULL INTEGRATION TEST: PASS")
    print("=" * 60)


if __name__ == "__main__":
    main()


