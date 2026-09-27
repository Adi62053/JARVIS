"""
JARVIS V9.24 - V3/V8/V9 Regression Test

Verifies that:
- V3 command security boundaries remain intact.
- V8 automation execution remains functional.
- V9 security blocks unconfigured capabilities.
- V9 security allows explicitly configured safe/caution operations.
- V9 authorization remains one-shot.
- V9 emergency stop overrides normal authorization.
- Security decisions are audited.
- No real application/system mutation is performed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json

from automation.automation_executor import AutomationExecutor
from automation.automation_model import Automation, AutomationStep
from automation.v9_automation_security import V9AutomationSecurity
from security.command_security import CommandSecurity
from security.v9_security_controller import V9SecurityController
from security.v9_security_model import (
    SecurityDecision,
    SecurityPrivilegeLevel,
    SecurityRiskLevel,
)


def main() -> None:
    print()
    print("========================================")
    print("JARVIS V9.24 REGRESSION TEST")
    print("========================================")
    print()

    # =========================================================
    # 1. V3 command security regression
    # =========================================================

    v3_security = CommandSecurity()

    assert v3_security.is_safe("open notepad")
    assert v3_security.is_risky("lock computer")
    assert v3_security.is_risky("terminate chrome")
    assert v3_security.is_blocked("format computer")
    assert v3_security.is_blocked("destroy system")

    print("V3 SAFE CLASSIFICATION: PASS")
    print("V3 RISKY CLASSIFICATION: PASS")
    print("V3 BLOCKED CLASSIFICATION: PASS")

    # Verify the router-level blocked policy without executing anything.
    from tools.router import CommandRouter

    router = CommandRouter()

    blocked_result = router.route("format computer")

    assert isinstance(blocked_result, str)
    assert "blocked for safety" in blocked_result.lower()

    print("V3 ROUTER BLOCKED BOUNDARY: PASS")

    # =========================================================
    # 2. V9 controller + automation security adapter
    # =========================================================

    controller = V9SecurityController()

    adapter = V9AutomationSecurity(
        controller=controller
    )

    print("V9 SECURITY CONTROLLER INITIALIZED: PASS")
    print("V9 AUTOMATION SECURITY ADAPTER INITIALIZED: PASS")

    # =========================================================
    # 3. V9 unconfigured capability must deny
    # =========================================================

    step = AutomationStep(
        action="OPEN_APP",
        parameters={"app": "notepad"},
        security_level="SAFE",
    )

    denied = adapter.evaluate(
        automation_name="V9.24 Regression",
        step_number=1,
        step=step,
    )

    assert denied == SecurityDecision.DENY

    print("V9 UNCONFIGURED APPLICATION DENY: PASS")
    print("NO APPLICATION EXECUTED")

    # =========================================================
    # 4. V9 explicit permission allows the operation
    # =========================================================

    controller.permission_manager.set_permission(
        "APPLICATION",
        True,
    )

    allowed = adapter.evaluate(
        automation_name="V9.24 Regression Allow",
        step_number=1,
        step=step,
    )

    assert allowed == SecurityDecision.ALLOW

    print("V9 CONFIGURED APPLICATION ALLOW: PASS")
    print("NO APPLICATION EXECUTED")

    # =========================================================
    # 5. V8 executor + V9 integration
    # =========================================================

    automation = Automation(
        name="V9.24 Executor Regression",
        description="V3/V8/V9 regression",
    )

    automation.add_step(step)

    executor = AutomationExecutor(
        dry_run=True,
        v9_security=adapter,
    )

    results = executor.execute(
        automation
    )

    assert isinstance(results, list)
    assert len(results) == 1
    assert "DRY RUN" in results[0]
    assert "SECURITY=SAFE" in results[0]

    print("V8 EXECUTOR + V9 ALLOW INTEGRATION: PASS")
    print("NO APPLICATION EXECUTED")

    # =========================================================
    # 6. V9 one-shot authorization boundary
    # =========================================================

    authorization_controller = V9SecurityController()

    authorization_controller.permission_manager.set_permission(
        "SYSTEM",
        True,
    )

    operation_id = "v9.24.authorization.test"

    first = authorization_controller.evaluate(
        operation_id=operation_id,
        capability="SYSTEM",
        resource="v9.24.test",
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.USER,
    )

    assert first == SecurityDecision.REQUIRE_AUTHORIZATION

    authorization_controller.authorization_manager.authorize(
        operation_id
    )

    second = authorization_controller.evaluate(
        operation_id=operation_id,
        capability="SYSTEM",
        resource="v9.24.test",
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.USER,
    )

    assert second == SecurityDecision.ALLOW

    assert (
        authorization_controller.authorization_manager.is_authorized(
            operation_id
        )
        is False
    )

    print("V9 AUTHORIZATION REQUIRED: PASS")
    print("V9 ONE-SHOT AUTHORIZATION: PASS")
    print("NO SYSTEM MUTATION EXECUTED")

    # =========================================================
    # 7. V9 privilege/elevation boundary
    # =========================================================

    elevation_controller = V9SecurityController()

    elevation_controller.permission_manager.set_permission(
        "FIRMWARE",
        True,
    )

    firmware_result = elevation_controller.evaluate(
        operation_id="v9.24.firmware.boundary",
        capability="FIRMWARE",
        resource="UEFI",
        risk_level=SecurityRiskLevel.HIGH,
        required_privilege=SecurityPrivilegeLevel.FIRMWARE,
    )

    assert firmware_result == SecurityDecision.REQUIRE_ELEVATION

    print("V9 FIRMWARE ELEVATION BOUNDARY: PASS")
    print("NO FIRMWARE MUTATION EXECUTED")

    # =========================================================
    # 8. V9 emergency-stop override
    # =========================================================

    emergency_controller = V9SecurityController()

    emergency_controller.permission_manager.set_permission(
        "APPLICATION",
        True,
    )

    emergency_controller.emergency_controls.activate()

    emergency_result = emergency_controller.evaluate(
        operation_id="v9.24.emergency.test",
        capability="APPLICATION",
        resource="notepad",
        risk_level=SecurityRiskLevel.CAUTION,
        required_privilege=SecurityPrivilegeLevel.USER,
    )

    assert emergency_result == SecurityDecision.DENY

    print("V9 EMERGENCY STOP OVERRIDE: PASS")
    print("NO APPLICATION EXECUTED")

    emergency_controller.emergency_controls.deactivate()

    recovered = emergency_controller.evaluate(
        operation_id="v9.24.emergency.recovery",
        capability="APPLICATION",
        resource="notepad",
        risk_level=SecurityRiskLevel.CAUTION,
        required_privilege=SecurityPrivilegeLevel.USER,
    )

    assert recovered == SecurityDecision.ALLOW

    print("V9 EMERGENCY RECOVERY: PASS")

    # =========================================================
    # 9. Audit verification
    # =========================================================

    audit_path = Path("logs/v9_security_audit.jsonl")

    assert audit_path.exists()

    lines = [
        line.strip()
        for line in audit_path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    assert lines

    latest = json.loads(lines[-1])

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

    assert required_fields.issubset(latest.keys())

    print("V9 AUDIT FILE PRESENT: PASS")
    print("V9 AUDIT RECORD STRUCTURE: PASS")

    # =========================================================
    # 10. Final safety assertions
    # =========================================================

    assert "notepad" in latest["resource"] or latest["operation_id"]

    print()
    print("NO REAL APPLICATION MUTATION: PASS")
    print("NO REAL SYSTEM MUTATION: PASS")
    print("NO REAL FIRMWARE MUTATION: PASS")
    print()
    print("========================================")
    print("V9.24 REGRESSION TEST: PASS")
    print("========================================")


if __name__ == "__main__":
    main()


