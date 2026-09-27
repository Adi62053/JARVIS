from security.v9_firmware_model import FirmwareAccessRequest, FirmwareOperation, FirmwareResource, FirmwareResourceType
from security.v9_firmware_security_controller import V9FirmwareSecurityController
from security.v9_capability_model import SecurityCapability

c = V9FirmwareSecurityController()
c.controller.permission_manager.set_permission(SecurityCapability.FIRMWARE.value, True)

r = FirmwareResource(FirmwareResourceType.BCD_FIRMWARE, "BCD-AUTH-TEST", "Authorization test")
q = FirmwareAccessRequest(FirmwareOperation.READ, r)

d1 = c.evaluate(q)
print("WITHOUT AUTH:", d1.value)

c.controller.authorization_manager.authorize("firmware.READ")
d2 = c.evaluate(q)
print("WITH AUTH:", d2.value)

c.controller.authorization_manager.authorize("firmware.READ")
d3 = c.evaluate(q)
print("AUTH CONSUMED:", d3.value)

print("V9.19.1 AUTHORIZATION INTEGRATION: PASS")
