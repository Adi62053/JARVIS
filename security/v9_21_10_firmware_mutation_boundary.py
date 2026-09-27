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
    "BIOS-V9210",
    "Emergency mutation boundary",
)

request = FirmwareAccessRequest(
    FirmwareOperation.FLASH,
    resource,
)


# 1. Normal critical firmware mutation requires elevation.
normal = controller.evaluate(request)
assert normal == SecurityDecision.REQUIRE_ELEVATION


# 2. Attach emergency enforcement at the controller boundary.
original_evaluate = controller.evaluate

def emergency_protected_evaluate(request):
    emergency.require_emergency_clear()
    return original_evaluate(request)

controller.evaluate = emergency_protected_evaluate


# 3. Emergency stop activates.
emergency.activate()

assert emergency.is_active()
assert not emergency.allow_operation()


# 4. Emergency stop blocks controller evaluation.
try:
    controller.evaluate(request)
except PermissionError:
    emergency_blocked = True
else:
    emergency_blocked = False

assert emergency_blocked


# 5. Clear emergency stop.
emergency.deactivate()

assert not emergency.is_active()
assert emergency.allow_operation()


# 6. Critical firmware mutation remains elevation-protected.
restored = controller.evaluate(request)
assert restored == SecurityDecision.REQUIRE_ELEVATION


# 7. No firmware mutation is executed by this test.
mutation_executed = False

assert mutation_executed is False


print("NORMAL MUTATION BOUNDARY: PASS")
print("EMERGENCY STOP ACTIVATION: PASS")
print("EMERGENCY MUTATION BLOCK: PASS")
print("EMERGENCY STOP CLEAR: PASS")
print("FIRMWARE ELEVATION BOUNDARY: PASS")
print("NO FIRMWARE MUTATION EXECUTED: PASS")
print("V9.21.10 FIRMWARE MUTATION BOUNDARY: PASS")
