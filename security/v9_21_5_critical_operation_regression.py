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
    "BIOS-CRITICAL",
    "Critical BIOS operation",
)

request = FirmwareAccessRequest(
    FirmwareOperation.FLASH,
    resource,
)


# 1. Critical firmware mutation must require elevation.
normal = controller.evaluate(request)
assert normal == SecurityDecision.REQUIRE_ELEVATION


# 2. Activate emergency stop.
emergency.activate()

assert emergency.is_active()
assert not emergency.allow_operation()


# 3. Emergency enforcement must block execution.
try:
    emergency.require_emergency_clear()
except PermissionError:
    blocked = True
else:
    blocked = False

assert blocked


# 4. Critical security decision must remain protected.
critical_decision = controller.evaluate(request)
assert critical_decision == SecurityDecision.REQUIRE_ELEVATION


# 5. Clear emergency stop.
emergency.deactivate()

assert not emergency.is_active()
assert emergency.allow_operation()


# 6. Critical operation must still require elevation.
restored = controller.evaluate(request)
assert restored == SecurityDecision.REQUIRE_ELEVATION


print("CRITICAL OPERATION SECURITY: PASS")
print("EMERGENCY STOP ACTIVATION: PASS")
print("EMERGENCY STOP ENFORCEMENT: PASS")
print("CRITICAL OPERATION DURING EMERGENCY: PASS")
print("EMERGENCY STOP CLEAR: PASS")
print("CRITICAL OPERATION RESTORATION: PASS")
print("V9.21.5 CRITICAL OPERATION REGRESSION: PASS")
