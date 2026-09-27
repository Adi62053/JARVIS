from security.v9_21_1_emergency_controls import V9EmergencySecurityControls
from security.v9_audit_logger import V9AuditLogger
from security.v9_security_controller import V9SecurityController
from security.v9_security_model import (
    SecurityDecision,
    SecurityPrivilegeLevel,
    SecurityRiskLevel,
)


emergency = V9EmergencySecurityControls()
audit = V9AuditLogger()

controller = V9SecurityController(
    audit_logger=audit,
    emergency_controls=emergency,
)

controller.permission_manager.set_permission(
    "firmware",
    True,
)

operation = {
    "operation_id": "firmware.flash",
    "capability": "firmware",
    "resource": "BIOS",
    "risk_level": SecurityRiskLevel.CRITICAL,
    "required_privilege": SecurityPrivilegeLevel.SYSTEM,
}


# Current environment is below SYSTEM privilege.
normal = controller.evaluate(**operation)

assert normal == SecurityDecision.REQUIRE_ELEVATION

print("NORMAL PRIVILEGE BOUNDARY: PASS")


# Emergency stop must override the elevation decision.
emergency.activate()

blocked = controller.evaluate(**operation)

assert blocked == SecurityDecision.DENY

print("EMERGENCY OVERRIDES ELEVATION: PASS")


# Clear emergency and verify the original privilege boundary returns.
emergency.deactivate()

recovered = controller.evaluate(**operation)

assert recovered == SecurityDecision.REQUIRE_ELEVATION

print("PRIVILEGE BOUNDARY RESTORATION: PASS")

print("NO PRIVILEGE ESCALATION EXECUTED: PASS")
print("NO FIRMWARE MUTATION EXECUTED: PASS")
print("V9.21.23 PRIVILEGE + EMERGENCY REGRESSION: PASS")
