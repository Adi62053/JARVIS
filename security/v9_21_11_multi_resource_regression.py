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


resources = [
    FirmwareResource(
        FirmwareResourceType.BIOS,
        "BIOS-V9211",
        "BIOS resource",
    ),
    FirmwareResource(
        FirmwareResourceType.UEFI,
        "UEFI-V9211",
        "UEFI resource",
    ),
    FirmwareResource(
        FirmwareResourceType.SYSTEM_FIRMWARE,
        "SYSTEM-FIRMWARE-V9211",
        "System firmware resource",
    ),
    FirmwareResource(
        FirmwareResourceType.SECURE_BOOT,
        "SECURE-BOOT-V9211",
        "Secure Boot resource",
    ),
    FirmwareResource(
        FirmwareResourceType.BCD_FIRMWARE,
        "BCD-V9211",
        "BCD firmware resource",
    ),
]


requests = [
    FirmwareAccessRequest(
        FirmwareOperation.READ,
        resource,
    )
    for resource in resources
]


# 1. Every firmware resource must produce a valid
# security decision before emergency activation.
normal_decisions = [
    controller.evaluate(request)
    for request in requests
]

assert all(
    decision in (
        SecurityDecision.REQUIRE_ELEVATION,
        SecurityDecision.REQUIRE_AUTHORIZATION,
    )
    for decision in normal_decisions
)


# 2. Attach emergency enforcement.
original_evaluate = controller.evaluate

def emergency_protected_evaluate(request):
    emergency.require_emergency_clear()
    return original_evaluate(request)

controller.evaluate = emergency_protected_evaluate


# 3. Activate emergency stop.
emergency.activate()

assert emergency.is_active()
assert not emergency.allow_operation()


# 4. Every resource must be blocked by emergency enforcement.
blocked_count = 0

for request in requests:
    try:
        controller.evaluate(request)
    except PermissionError:
        blocked_count += 1

assert blocked_count == len(requests)


# 5. Clear emergency stop.
emergency.deactivate()

assert not emergency.is_active()
assert emergency.allow_operation()


# 6. Every resource must recover to its original security decision.
recovered_decisions = [
    controller.evaluate(request)
    for request in requests
]

assert recovered_decisions == normal_decisions


print("MULTI-RESOURCE SECURITY: PASS")
print("EMERGENCY STOP ACTIVATION: PASS")
print("ALL FIRMWARE RESOURCES BLOCKED: PASS")
print("EMERGENCY STOP CLEAR: PASS")
print("SECURITY DECISION RESTORATION: PASS")
print("RESOURCE COUNT:", len(requests))
print("V9.21.11 MULTI-RESOURCE EMERGENCY REGRESSION: PASS")
