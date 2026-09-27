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
    FirmwareResourceType.BIOS,
    "BIOS-PROTECTED",
    "Protected BIOS resource",
)

request = FirmwareAccessRequest(
    FirmwareOperation.READ,
    resource,
)


# 1. Protected BIOS access must require elevation normally.
normal = controller.evaluate(request)
assert normal == SecurityDecision.REQUIRE_ELEVATION


# 2. Activate emergency stop.
emergency.activate()

assert emergency.is_active()
assert not emergency.allow_operation()


# 3. Emergency stop must enforce its own boundary.
try:
    emergency.require_emergency_clear()
except PermissionError:
    blocked = True
else:
    blocked = False

assert blocked


# 4. Protected-resource security decision remains unchanged.
protected_decision = controller.evaluate(request)
assert protected_decision == SecurityDecision.REQUIRE_ELEVATION


# 5. Clear emergency stop.
emergency.deactivate()

assert not emergency.is_active()
assert emergency.allow_operation()


# 6. Protected-resource boundary must still remain enforced.
restored = controller.evaluate(request)
assert restored == SecurityDecision.REQUIRE_ELEVATION


print("PROTECTED RESOURCE SECURITY: PASS")
print("EMERGENCY STOP ACTIVATION: PASS")
print("EMERGENCY STOP ENFORCEMENT: PASS")
print("PROTECTED RESOURCE DURING EMERGENCY: PASS")
print("EMERGENCY STOP CLEAR: PASS")
print("PROTECTED RESOURCE RESTORATION: PASS")
print("V9.21.4 PROTECTED RESOURCE REGRESSION: PASS")
