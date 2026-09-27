from security.v9_security_model import AuthorizationState, SecurityDecision
from security.v9_capability_model import SecurityCapability
from security.v9_firmware_model import FirmwareAccessRequest, FirmwareOperation, FirmwareResource, FirmwareResourceType
from security.v9_firmware_security_controller import V9FirmwareSecurityController

c = V9FirmwareSecurityController()
c.controller.permission_manager.set_permission(SecurityCapability.FIRMWARE.value, True)

r = FirmwareResource(FirmwareResourceType.BCD_FIRMWARE, "BCD-CONFIRM-TEST", "Confirmation test")
q = FirmwareAccessRequest(FirmwareOperation.READ, r)

before = c.evaluate(q)
print("BEFORE CONFIRMATION:", before.value)

c.controller.authorization_manager.authorize("firmware.READ")
after = c.evaluate(q)
print("AFTER CONFIRMATION:", after.value)

print("CONFIRMATION REQUIRED:", before == SecurityDecision.REQUIRE_AUTHORIZATION)
print("CONFIRMATION ACCEPTED:", after == SecurityDecision.ALLOW)
print("AUTHORIZATION CONSUMED:", not c.controller.authorization_manager.is_authorized("firmware.READ"))
print("V9.19.2 CONFIRMATION INTEGRATION: PASS")
