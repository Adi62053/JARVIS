import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tempfile import TemporaryDirectory

from security.v9_audit_logger import V9AuditLogger
from security.v9_device_state_security import V9DeviceStateSecurityBoundary
from security.v9_network_device_operations import V9NetworkDeviceSecurityController
from security.v9_network_device_model import DeviceOperation, NetworkOperation
from security.v9_network_inspector import V9DeviceInspector, V9NetworkInspector
from security.v9_security_controller import V9SecurityController


with TemporaryDirectory() as temp_dir:
    audit_path = Path(temp_dir) / "v9_16_audit.jsonl"

    audit_logger = V9AuditLogger(log_path=audit_path)
    controller = V9SecurityController(audit_logger=audit_logger)

    network_security = V9NetworkDeviceSecurityController(controller)
    device_security = V9DeviceStateSecurityBoundary(controller)

    network = V9NetworkInspector()
    devices = V9DeviceInspector()

    adapter = network.list_adapters()[0]
    device_list = devices.list_devices()

    ordinary = next(
        device for device in device_list
        if device_security.classify(device).value == "ordinary"
    )

    sensitive = next(
        device for device in device_list
        if device_security.classify(device).value == "sensitive"
    )

    protected = next(
        device for device in device_list
        if device_security.classify(device).value == "protected"
    )

    controller.permission_manager.set_permission("NETWORK", True)
    controller.permission_manager.set_permission("DEVICE", True)

    network_decision = network_security.evaluate_network(
        NetworkOperation.READ,
        adapter,
    )

    device_read = device_security.evaluate(
        DeviceOperation.READ,
        ordinary,
    )

    device_sensitive = device_security.evaluate(
        DeviceOperation.ENABLE,
        sensitive,
    )

    device_protected = device_security.evaluate(
        DeviceOperation.DISABLE,
        protected,
    )

    lines = audit_path.read_text(encoding="utf-8").splitlines()

    print("AUDIT FILE EXISTS:", audit_path.exists())
    print("AUDIT RECORD COUNT:", len(lines))

    for index, line in enumerate(lines, 1):
        print(f"AUDIT {index}: {line}")

    print("NETWORK READ DECISION:", network_decision[3].value)
    print("ORDINARY DEVICE READ:", device_read[3].value)
    print("SENSITIVE DEVICE ENABLE:", device_sensitive[3].value)
    print("PROTECTED DEVICE DISABLE:", device_protected[3].value)

    decisions = [
        network_decision[3].value,
        device_read[3].value,
        device_sensitive[3].value,
        device_protected[3].value,
    ]

    expected = {
        "ALLOW",
        "REQUIRE_AUTHORIZATION",
        "REQUIRE_ELEVATION",
    }

    audit_ok = (
        audit_path.exists()
        and len(lines) >= 4
        and expected.issubset(set(decisions))
    )

    print(
        "V9.16.15 AUDIT INTEGRITY: PASS"
        if audit_ok
        else "V9.16.15 AUDIT INTEGRITY: FAIL"
    )
