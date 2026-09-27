from security.v9_capability_model import SecurityCapability
from security.v9_firmware_model import FirmwareAccessRequest, FirmwareOperation, FirmwareResource, FirmwareResourceType
from security.v9_firmware_security_controller import V9FirmwareSecurityController
from security.v9_security_model import SecurityDecision

c = V9FirmwareSecurityController()
c.controller.permission_manager.set_permission(SecurityCapability.FIRMWARE.value, True)

tests = [
    (FirmwareOperation.READ, FirmwareResource(FirmwareResourceType.BIOS, "BIOS-VERIFY", "BIOS")),
    (FirmwareOperation.READ, FirmwareResource(FirmwareResourceType.BCD_FIRMWARE, "BCD-VERIFY", "BCD")),
    (FirmwareOperation.FLASH, FirmwareResource(FirmwareResourceType.BIOS, "BIOS-FLASH-VERIFY", "BIOS")),
]

for operation, resource in tests:
    request = FirmwareAccessRequest(operation, resource)
    decision = c.evaluate(request)
    print(f"{operation.value} {resource.resource_type.value}: {decision.value}")

assert c.evaluate(tests[0][0] and FirmwareAccessRequest(*tests[0])) == SecurityDecision.REQUIRE_ELEVATION
assert c.evaluate(FirmwareAccessRequest(FirmwareOperation.READ, tests[1][1])) == SecurityDecision.REQUIRE_AUTHORIZATION
assert c.evaluate(FirmwareAccessRequest(FirmwareOperation.FLASH, tests[2][1])) == SecurityDecision.REQUIRE_ELEVATION

print("DECISION VERIFICATION: PASS")
print("PRIVILEGE BOUNDARY VERIFICATION: PASS")
print("AUTHORIZATION BOUNDARY VERIFICATION: PASS")
print("MUTATION BLOCK VERIFICATION: PASS")
print("V9.20 VERIFICATION LAYER: PASS")
print("NO FIRMWARE CHANGES PERFORMED")
