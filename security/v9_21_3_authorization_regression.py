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
    "BCD-AUTH-REGRESSION",
    "Emergency authorization regression",
)

request = FirmwareAccessRequest(
    FirmwareOperation.READ,
    resource,
)


# 1. Normal operation must require authorization.
normal = controller.evaluate(request)
assert normal == SecurityDecision.REQUIRE_AUTHORIZATION


# 2. Authorize the operation.
controller.controller.authorization_manager.authorize(
    "firmware.READ"
)

authorized = controller.evaluate(request)
assert authorized == SecurityDecision.ALLOW


# 3. Authorization must be consumed.
remaining = controller.controller.authorization_manager.is_authorized(
    "firmware.READ"
)
assert not remaining


# 4. Emergency stop must block operation enforcement.
emergency.activate()

assert emergency.is_active()
assert not emergency.allow_operation()

try:
    emergency.require_emergency_clear()
except PermissionError:
    blocked = True
else:
    blocked = False

assert blocked


# 5. Clear emergency stop.
emergency.deactivate()

assert not emergency.is_active()
assert emergency.allow_operation()


# 6. Authorization must still be required after clearing.
restored = controller.evaluate(request)
assert restored == SecurityDecision.REQUIRE_AUTHORIZATION


# 7. Re-authorize and verify normal operation works again.
controller.controller.authorization_manager.authorize(
    "firmware.READ"
)

recovered = controller.evaluate(request)
assert recovered == SecurityDecision.ALLOW


print("NORMAL AUTHORIZATION: PASS")
print("AUTHORIZATION CONSUMPTION: PASS")
print("EMERGENCY STOP BLOCK: PASS")
print("EMERGENCY STOP CLEAR: PASS")
print("AUTHORIZATION RESTORATION: PASS")
print("POST-EMERGENCY OPERATION: PASS")
print("V9.21.3 EMERGENCY + AUTHORIZATION REGRESSION: PASS")
