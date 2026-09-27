import json
import tempfile
from pathlib import Path

from .v9_audit_logger import V9AuditLogger
from .v9_hardware_capability_model import (
    HardwareOperation,
    HardwareResource,
    HardwareResourceType,
)
from .v9_hardware_inspection_security import V9HardwareInspectionSecurity
from .v9_hardware_operations import V9ControlledHardwareOperations
from .v9_hardware_security_controller import V9HardwareSecurityController


def _read_audit_records(path: Path) -> list[dict]:
    if not path.exists():
        return []

    records = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))

    return records


def run_audit_test() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        audit_path = Path(temp_dir) / "hardware_audit.jsonl"

        audit_logger = V9AuditLogger(log_path=audit_path)

        controller = V9HardwareSecurityController()

        # Replace only the audit logger inside the existing V9 controller.
        controller.controller.audit_logger = audit_logger

        controller.controller.permission_manager.set_permission(
            "HARDWARE",
            True,
        )

        cpu = HardwareResource(
            HardwareResourceType.CPU,
            "CPU-AUDIT-TEST",
            "CPU audit resource",
        )

        usb = HardwareResource(
            HardwareResourceType.USB,
            "USB-AUDIT-TEST",
            "USB audit resource",
        )

        bios = HardwareResource(
            HardwareResourceType.BIOS,
            "BIOS-AUDIT-TEST",
            "BIOS audit resource",
        )

        _, _, _, cpu_decision = controller.evaluate(
            HardwareOperation.READ,
            cpu,
        )

        _, _, _, usb_decision = controller.evaluate(
            HardwareOperation.CONFIGURE,
            usb,
        )

        _, _, _, bios_decision = controller.evaluate(
            HardwareOperation.CONFIGURE,
            bios,
        )

        assert cpu_decision.value == "ALLOW"
        assert usb_decision.value == "REQUIRE_AUTHORIZATION"
        assert bios_decision.value == "REQUIRE_ELEVATION"

        records = _read_audit_records(audit_path)

        print("AUDIT FILE EXISTS:", audit_path.exists())
        print("AUDIT RECORD COUNT:", len(records))

        for index, record in enumerate(records, start=1):
            print(
                f"AUDIT {index}:",
                record["operation_id"],
                record["capability"],
                record["resource"],
                record["risk_level"],
                record["required_privilege"],
                record["decision"],
                record["result"],
            )

        assert len(records) == 3

        assert records[0]["operation_id"] == "hardware.READ"
        assert records[0]["capability"] == "HARDWARE"
        assert records[0]["decision"] == "ALLOW"

        assert records[1]["operation_id"] == "hardware.CONFIGURE"
        assert records[1]["capability"] == "HARDWARE"
        assert records[1]["decision"] == "REQUIRE_AUTHORIZATION"

        assert records[2]["operation_id"] == "hardware.CONFIGURE"
        assert records[2]["capability"] == "HARDWARE"
        assert records[2]["decision"] == "REQUIRE_ELEVATION"

        print("V9.17.11 AUDIT INTEGRITY: PASS")


def run_full_regression() -> None:
    security = V9HardwareInspectionSecurity()

    security.security.controller.permission_manager.set_permission(
        "HARDWARE",
        True,
    )

    print("=== LIVE HARDWARE INVENTORY ===")

    cpu = security.inspector.get_cpu()
    memory = security.inspector.get_memory()
    gpus = security.inspector.get_gpus()
    storage = security.inspector.get_storage()
    motherboard = security.inspector.get_motherboard()
    bios = security.inspector.get_bios()
    batteries = security.inspector.get_batteries()
    usb_devices = security.inspector.get_usb_devices()

    print("CPU:", cpu.name)
    print("LOGICAL PROCESSORS:", cpu.logical_processors)
    print("MEMORY BYTES:", memory.total_physical_bytes)
    print("GPU COUNT:", len(gpus))
    print("STORAGE COUNT:", len(storage))
    print("MOTHERBOARD:", motherboard.manufacturer)
    print("BIOS:", bios.manufacturer, bios.version)
    print("BATTERY COUNT:", len(batteries))
    print("USB COUNT:", len(usb_devices))

    assert cpu.name
    assert cpu.logical_processors > 0
    assert memory.total_physical_bytes > 0
    assert len(gpus) >= 0
    assert len(storage) >= 0
    assert motherboard.manufacturer
    assert bios.manufacturer
    assert bios.version
    assert len(batteries) >= 0
    assert len(usb_devices) >= 0

    print("LIVE INSPECTION: PASS")

    print("\n=== SECURITY EVALUATION ===")

    cpu_info, cpu_eval = security.inspect_and_evaluate_cpu()
    memory_info, memory_eval = security.inspect_and_evaluate_memory()
    bios_info, bios_eval = security.inspect_and_evaluate_bios()

    print(
        "CPU:",
        cpu_info.name,
        "->",
        cpu_eval[3].value,
        cpu_eval[1],
        cpu_eval[2],
    )

    print(
        "MEMORY:",
        memory_info.total_physical_bytes,
        "->",
        memory_eval[3].value,
        memory_eval[1],
        memory_eval[2],
    )

    print(
        "BIOS:",
        bios_info.manufacturer,
        bios_info.version,
        "->",
        bios_eval[3].value,
        bios_eval[1],
        bios_eval[2],
    )

    assert cpu_eval[3].value == "ALLOW"
    assert memory_eval[3].value == "ALLOW"
    assert bios_eval[3].value == "REQUIRE_ELEVATION"

    gpu_results = security.inspect_and_evaluate_gpus()
    storage_results = security.inspect_and_evaluate_storage()
    battery_results = security.inspect_and_evaluate_batteries()
    usb_results = security.inspect_and_evaluate_usb()

    print("GPU SECURITY RESULTS:", len(gpu_results))
    print("STORAGE SECURITY RESULTS:", len(storage_results))
    print("BATTERY SECURITY RESULTS:", len(battery_results))
    print("USB SECURITY RESULTS:", len(usb_results))

    for _, evaluation in gpu_results:
        assert evaluation[3].value == "ALLOW"

    for _, evaluation in storage_results:
        assert evaluation[3].value == "ALLOW"

    for _, evaluation in battery_results:
        assert evaluation[3].value == "ALLOW"

    for _, evaluation in usb_results:
        assert evaluation[3].value == "ALLOW"

    print("HARDWARE READ SECURITY: PASS")

    print("\n=== CONTROLLED OPERATION REGRESSION ===")

    operations = V9ControlledHardwareOperations(
        security_controller=security.security,
    )

    cpu_resource = security.build_cpu_resource(cpu)
    usb_resource = security.build_usb_resource(
        usb_devices[0]
    ) if usb_devices else HardwareResource(
        HardwareResourceType.USB,
        "USB-REGRESSION",
        "USB regression resource",
    )
    bios_resource = security.build_bios_resource(bios)

    cpu_result = operations.execute(
        HardwareOperation.READ,
        cpu_resource,
    )

    print("CPU READ:", cpu_result)

    assert cpu_result.allowed
    assert not cpu_result.executed
    assert cpu_result.decision == "ALLOW"

    usb_result = operations.execute(
        HardwareOperation.CONFIGURE,
        usb_resource,
    )

    print("USB CONFIGURE WITHOUT AUTH:", usb_result)

    assert usb_result.decision == "REQUIRE_AUTHORIZATION"
    assert not usb_result.executed

    operations.security.controller.authorization_manager.authorize(
        "hardware.CONFIGURE"
    )

    usb_authorized = operations.execute(
        HardwareOperation.CONFIGURE,
        usb_resource,
    )

    print("USB CONFIGURE WITH AUTH:", usb_authorized)

    assert usb_authorized.allowed
    assert not usb_authorized.executed

    assert not (
        operations.security.controller.authorization_manager.is_authorized(
            "hardware.CONFIGURE"
        )
    )

    bios_result = operations.execute(
        HardwareOperation.CONFIGURE,
        bios_resource,
    )

    print("BIOS CONFIGURE:", bios_result)

    assert bios_result.decision == "REQUIRE_ELEVATION"
    assert not bios_result.executed

    print("CONTROLLED HARDWARE BOUNDARY: PASS")
    print("NO HARDWARE MUTATION: PASS")

    print("\n========================================")
    print("V9.17.12 FULL REGRESSION: PASS")
    print("========================================")


if __name__ == "__main__":
    run_audit_test()
    run_full_regression()
