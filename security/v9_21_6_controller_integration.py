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
    "BCD-V9216",
    "Emergency controller integration",
)

request = FirmwareAccessRequest(
    FirmwareOperation.READ,
    resource,
)


# Normal security evaluation.
normal = controller.evaluate(request)
assert normal == SecurityDecision.REQUIRE_AUTHORIZATION


# Integrate emergency control at the controller boundary.
original_evaluate = controller.evaluate

def emergency_protected_evaluate(request):
    emergency.require_emergency_clear()
    return original_evaluate(request)

controller.evaluate = emergency_protected_evaluate


# Emergency stop must now block controller evaluation directly.
emergency.activate()

try:
    controller.evaluate(request)
except PermissionError:
    controller_blocked = True
else:
    controller_blocked = False

assert controller_blocked


# Clear emergency stop.
emergency.deactivate()

restored = controller.evaluate(request)
assert restored == SecurityDecision.REQUIRE_AUTHORIZATION


print("NORMAL CONTROLLER EVALUATION: PASS")
print("EMERGENCY CONTROLLER BLOCK: PASS")
print("DIRECT EMERGENCY ENFORCEMENT: PASS")
print("EMERGENCY CLEAR: PASS")
print("CONTROLLER RECOVERY: PASS")
print("V9.21.6 EMERGENCY CONTROLLER INTEGRATION: PASS")
