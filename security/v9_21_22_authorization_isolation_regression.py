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
    "operation_id": "firmware.read",
    "capability": "firmware",
    "resource": "BIOS",
    "risk_level": SecurityRiskLevel.HIGH,
    "required_privilege": SecurityPrivilegeLevel.ADMINISTRATOR,
}


# Authorization must initially be required.
normal = controller.evaluate(**operation)

assert normal == SecurityDecision.REQUIRE_AUTHORIZATION

print("INITIAL AUTHORIZATION REQUIREMENT: PASS")


# Explicitly authorize the operation.
controller.authorization_manager.authorize(
    operation["operation_id"]
)

assert controller.authorization_manager.is_authorized(
    operation["operation_id"]
)

print("AUTHORIZATION CREATED: PASS")


# Emergency stop must override the authorization.
emergency.activate()

blocked = controller.evaluate(**operation)

assert blocked == SecurityDecision.DENY

print("EMERGENCY OVERRIDES AUTHORIZATION: PASS")


# Authorization must still exist because the emergency block
# happens before authorization consumption.
assert controller.authorization_manager.is_authorized(
    operation["operation_id"]
)

print("AUTHORIZATION PRESERVED DURING EMERGENCY: PASS")


# Clear emergency and retry.
emergency.deactivate()

recovered = controller.evaluate(**operation)

assert recovered == SecurityDecision.ALLOW

print("POST-EMERGENCY AUTHORIZED OPERATION: PASS")


# Authorization is one-shot and must now be consumed.
assert not controller.authorization_manager.is_authorized(
    operation["operation_id"]
)

print("AUTHORIZATION CONSUMED AFTER RECOVERY: PASS")


# A second attempt must require fresh authorization.
second_attempt = controller.evaluate(**operation)

assert second_attempt == SecurityDecision.REQUIRE_AUTHORIZATION

print("FRESH AUTHORIZATION REQUIRED: PASS")

print("NO AUTHORIZATION STATE CORRUPTION: PASS")
print("V9.21.22 EMERGENCY + AUTHORIZATION ISOLATION REGRESSION: PASS")
