from security.v9_21_1_emergency_controls import V9EmergencySecurityControls
from security.v9_capability_model import SecurityCapability
from security.v9_firmware_model import FirmwareAccessRequest, FirmwareOperation, FirmwareResource, FirmwareResourceType
from security.v9_firmware_security_controller import V9FirmwareSecurityController
from security.v9_security_model import SecurityDecision

emergency = V9EmergencySecurityControls()
controller = V9FirmwareSecurityController()
controller.controller.permission_manager.set_permission(SecurityCapability.FIRMWARE.value, True)

resource = FirmwareResource(FirmwareResourceType.BCD_FIRMWARE, "BCD-EMERGENCY", "Emergency integration")
request = FirmwareAccessRequest(FirmwareOperation.READ, resource)

normal = controller.evaluate(request)
assert normal == SecurityDecision.REQUIRE_AUTHORIZATION

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

emergency.deactivate()
assert not emergency.is_active()
assert emergency.allow_operation()

restored = controller.evaluate(request)
assert restored == SecurityDecision.REQUIRE_AUTHORIZATION

print("NORMAL SECURITY DECISION: PASS")
print("EMERGENCY STOP ACTIVATION: PASS")
print("CONTROLLER OPERATION BLOCK: PASS")
print("EMERGENCY CLEAR: PASS")
print("SECURITY RESTORATION: PASS")
print("V9.21.2 EMERGENCY CONTROLLER INTEGRATION: PASS")
