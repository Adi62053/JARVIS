from security.v9_capability_model import SecurityCapability
from security.v9_firmware_model import FirmwareAccessRequest, FirmwareOperation, FirmwareResource, FirmwareResourceType
from security.v9_firmware_security_controller import V9FirmwareSecurityController
from security.v9_security_model import SecurityDecision

c = V9FirmwareSecurityController()
c.controller.permission_manager.set_permission(SecurityCapability.FIRMWARE.value, True)

r = FirmwareResource(FirmwareResourceType.BCD_FIRMWARE, "BCD-REGRESSION", "Authorization regression")
q = FirmwareAccessRequest(FirmwareOperation.READ, r)

d1 = c.evaluate(q)
assert d1 == SecurityDecision.REQUIRE_AUTHORIZATION

c.controller.authorization_manager.authorize("firmware.READ")
d2 = c.evaluate(q)
assert d2 == SecurityDecision.ALLOW
assert not c.controller.authorization_manager.is_authorized("firmware.READ")

d3 = c.evaluate(q)
assert d3 == SecurityDecision.REQUIRE_AUTHORIZATION

c.controller.authorization_manager.deny("firmware.READ")
assert not c.controller.authorization_manager.is_authorized("firmware.READ")

d4 = c.evaluate(q)
assert d4 == SecurityDecision.REQUIRE_AUTHORIZATION

print("INITIAL AUTHORIZATION: PASS")
print("CONFIRMED OPERATION: PASS")
print("ONE-SHOT CONSUMPTION: PASS")
print("DENIAL STATE: PASS")
print("RECONFIRMATION REQUIRED: PASS")
print("V9.19.3 AUTHORIZATION + CONFIRMATION REGRESSION: PASS")
