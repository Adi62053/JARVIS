import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import py_compile

from security.v9_network_inspector import (
    V9NetworkInspector,
    V9DeviceInspector,
)
from security.v9_network_device_model import (
    NetworkOperation,
    DeviceOperation,
)
from security.v9_network_device_operations import (
    V9ControlledNetworkOperations,
)
from security.v9_device_state_security import (
    V9DeviceStateSecurityBoundary,
    V9AuthorizedDeviceOperations,
)


# =========================================================
# 1. Compile all V9.16 production modules
# =========================================================

modules = [
    "security/v9_network_device_model.py",
    "security/v9_network_device_capability.py",
    "security/v9_network_inspector.py",
    "security/v9_device_protection.py",
    "security/v9_network_risk.py",
    "security/v9_device_risk.py",
    "security/v9_network_device_security.py",
    "security/v9_network_device_operations.py",
    "security/v9_device_state_security.py",
]

for module in modules:
    py_compile.compile(module, doraise=True)

print("V9.16 PRODUCTION COMPILE: PASS")


# =========================================================
# 2. Network inspection
# =========================================================

network = V9NetworkInspector()

adapters = network.list_adapters()
ip_configurations = network.get_ip_configuration()
tcp_connections = network.get_tcp_connections()

assert len(adapters) > 0
assert len(ip_configurations) > 0
assert len(tcp_connections) > 0

print("NETWORK ADAPTERS:", len(adapters))
print("IP CONFIGURATIONS:", len(ip_configurations))
print("TCP CONNECTIONS:", len(tcp_connections))
print("NETWORK INSPECTION: PASS")


# =========================================================
# 3. Device enumeration
# =========================================================

device_inspector = V9DeviceInspector()
devices = device_inspector.list_devices()

assert len(devices) > 0

print("DEVICES:", len(devices))
print("DEVICE ENUMERATION: PASS")


# =========================================================
# 4. Device protection classification
# =========================================================

device_security = V9DeviceStateSecurityBoundary()

categories = {
    "ordinary": 0,
    "sensitive": 0,
    "critical": 0,
    "protected": 0,
}

for device in devices:
    category = device_security.classify(device).value

    assert category in categories

    categories[category] += 1

print("DEVICE CATEGORIES:", categories)

assert categories["sensitive"] > 0
assert categories["critical"] > 0
assert categories["protected"] > 0

print("DEVICE PROTECTION: PASS")


# =========================================================
# 5. Device authorization boundary
# =========================================================

ordinary = next(
    device
    for device in devices
    if device_security.classify(device).value == "ordinary"
)

sensitive = next(
    device
    for device in devices
    if device_security.classify(device).value == "sensitive"
)

protected = next(
    device
    for device in devices
    if device_security.classify(device).value == "protected"
)

controller = device_security.controller

controller.permission_manager.set_permission(
    "DEVICE",
    True,
)

operations = V9AuthorizedDeviceOperations(
    device_security
)


# Ordinary READ
ordinary_result = operations.execute(
    DeviceOperation.READ,
    ordinary,
)

assert ordinary_result.decision == "ALLOW"
assert ordinary_result.allowed is True
assert ordinary_result.executed is False

print("ORDINARY DEVICE READ: PASS")


# Sensitive mutation without authorization
sensitive_before = operations.execute(
    DeviceOperation.ENABLE,
    sensitive,
)

assert sensitive_before.decision == "REQUIRE_AUTHORIZATION"
assert sensitive_before.allowed is False
assert sensitive_before.executed is False

print("SENSITIVE DEVICE WITHOUT AUTH: PASS")


# Create one-shot authorization
operation_id = operations.authorize(
    DeviceOperation.ENABLE,
    sensitive,
)

assert operation_id == "device.ENABLE"

print("DEVICE AUTHORIZATION CREATED:", operation_id)


# Authorized operation remains dry-run
sensitive_after = operations.execute(
    DeviceOperation.ENABLE,
    sensitive,
)

assert sensitive_after.decision == "ALLOW"
assert sensitive_after.allowed is True
assert sensitive_after.executed is False

print("SENSITIVE DEVICE WITH AUTH: PASS")


# Authorization consumed
assert (
    controller.authorization_manager.is_authorized(operation_id)
    is False
)

print("ONE-SHOT AUTHORIZATION CONSUMED: PASS")


# Protected mutation requires SYSTEM
protected_result = operations.execute(
    DeviceOperation.DISABLE,
    protected,
)

assert protected_result.decision == "REQUIRE_ELEVATION"
assert protected_result.allowed is False
assert protected_result.executed is False

print("PROTECTED DEVICE ELEVATION BOUNDARY: PASS")


# =========================================================
# 6. Network security evaluation
# =========================================================

network_operations = V9ControlledNetworkOperations()

adapter = adapters[0]

network_controller = network_operations._security
network_v9_controller = network_controller._controller

network_v9_controller.permission_manager.set_permission(
    "NETWORK",
    True,
)

# READ is SAFE and should be allowed by policy.
network_request, network_risk, network_privilege, network_decision = (
    network_controller.evaluate_network(
        NetworkOperation.READ,
        adapter,
    )
)

assert network_decision.value == "ALLOW"
assert network_risk.value == "SAFE"
assert network_privilege.value == "USER"

print("NETWORK READ SECURITY: PASS")


# =========================================================
# 7. Network dry-run boundary
# =========================================================

network_result = network_operations.set_adapter_state(
    adapter,
    NetworkOperation.ENABLE,
    execute=False,
)

assert network_result.executed is False
assert network_result.allowed is False
assert "REQUIRE_AUTHORIZATION" in network_result.message

print("NETWORK AUTHORIZATION BOUNDARY: PASS")


# =========================================================
# 8. Explicit network authorization + dry-run
# =========================================================

network_v9_controller.authorization_manager.authorize(
    "network.ENABLE"
)

authorized_network_result = network_operations.set_adapter_state(
    adapter,
    NetworkOperation.ENABLE,
    execute=False,
)

assert authorized_network_result.executed is False
assert authorized_network_result.allowed is True
assert "DRY-RUN" in authorized_network_result.message

print("NETWORK AUTHORIZED DRY-RUN: PASS")


# One-shot network authorization must be consumed.
assert (
    network_v9_controller.authorization_manager.is_authorized(
        "network.ENABLE"
    )
    is False
)

print("NETWORK ONE-SHOT AUTHORIZATION CONSUMED: PASS")


# =========================================================
# 9. Final mutation safety assertions
# =========================================================

assert ordinary_result.executed is False
assert sensitive_before.executed is False
assert sensitive_after.executed is False
assert protected_result.executed is False
assert network_result.executed is False
assert authorized_network_result.executed is False

print("NO REAL NETWORK/DEVICE MUTATION: PASS")


# =========================================================
# Final result
# =========================================================

print()
print("========================================")
print("V9.16.16 FULL REGRESSION: PASS")
print("========================================")
print()
print("V9.16 NETWORK & DEVICE ACCESS: COMPLETE")
print("16/16 SUBSTEPS COMPLETE")
