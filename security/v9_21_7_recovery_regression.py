from security.v9_21_1_emergency_controls import V9EmergencySecurityControls
from security.v9_capability_model import SecurityCapability
from security.v9_firmware_model import (
    FirmwareAccessRequest,
    FirmwareOperation,
    FirmwareResource,
    FirmwareResourceType,
)
from security.v9_firmware_security_controller import V9FirmwareSecurityController
from security.v9_security_model import SecurityDecision


emergency = V9EmergencySecurityControls()
controller = V9FirmwareSecurityController()

controller.controller.permission_manager.set_permission(
    SecurityCapability.FIRMWARE.value,
    True
)

resource = FirmwareResource(
    FirmwareResourceType.BCD_FIRMWARE,
    "BCD-V9217",
    "Emergency recovery state regression",
)

request = FirmwareAccessRequest(
    FirmwareOperation.READ,
    resource,
)


# Attach emergency enforcement to the controller boundary.
original_evaluate = controller.evaluate

def emergency_protected_evaluate(request):
    emergency.require_emergency_clear()
    return original_evaluate(request)

controller.evaluate = emergency_protected_evaluate


# 1. Normal state requires authorization.
normal = controller.evaluate(request)
assert normal == SecurityDecision.REQUIRE_AUTHORIZATION


# 2. Authorize and consume authorization.
controller.controller.authorization_manager.authorize(
    "firmware.READ"
)

authorized = controller.evaluate(request)
assert authorized == SecurityDecision.ALLOW

assert not controller.controller.authorization_manager.is_authorized(
    "firmware.READ"
)


# 3. Activate emergency stop.
emergency.activate()

try:
    controller.evaluate(request)
except PermissionError:
    blocked = True
else:
    blocked = False

assert blocked


# 4. Emergency state must not recreate authorization.
assert not controller.controller.authorization_manager.is_authorized(
    "firmware.READ"
)


# 5. Clear emergency stop.
emergency.deactivate()

assert not emergency.is_active()
assert emergency.allow_operation()


# 6. Security must return to normal authorization-required state.
recovered = controller.evaluate(request)
assert recovered == SecurityDecision.REQUIRE_AUTHORIZATION


# 7. Fresh authorization must be required.
assert not controller.controller.authorization_manager.is_authorized(
    "firmware.READ"
)


print("NORMAL STATE: PASS")
print("AUTHORIZATION CONSUMPTION: PASS")
print("EMERGENCY BLOCK: PASS")
print("NO STALE AUTHORIZATION: PASS")
print("EMERGENCY CLEAR: PASS")
print("SECURITY STATE RECOVERY: PASS")
print("FRESH AUTHORIZATION REQUIRED: PASS")
print("V9.21.7 EMERGENCY RECOVERY STATE REGRESSION: PASS")
