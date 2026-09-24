from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_audit_logger import V9AuditLogger
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_permission_manager import V9PermissionManager
from security.v9_privileged_filesystem import V9PrivilegedFilesystem
from security.v9_security_controller import V9SecurityController


with TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)

    source_file = root / "source.txt"
    ordinary_destination = root / "ordinary_destination.txt"

    source_file.write_text(
        "V9.15.14 risk test",
        encoding="utf-8",
    )

    with TemporaryDirectory() as audit_dir:
        permission_manager = V9PermissionManager()
        authorization_manager = V9AuthorizationManager()

        permission_manager.set_permission(
            "FILE",
            True,
        )

        audit_logger = V9AuditLogger(
            log_path=str(
                Path(audit_dir) / "v9_15_14_audit.jsonl"
            )
        )

        controller = V9SecurityController(
            permission_manager=permission_manager,
            authorization_manager=authorization_manager,
            audit_logger=audit_logger,
        )

        fs = V9PrivilegedFilesystem()

        critical_destination = Path(
            r"C:\Program Files\JARVIS_V91514_TEST.txt"
        )

        # ---------------------------------------------------------
        # 1. Ordinary source -> ordinary destination
        # ---------------------------------------------------------
        try:
            ordinary_result = fs.evaluate_security(
                "COPY",
                source_file,
                destination=ordinary_destination,
                security_controller=controller,
            )

            print(
                "ordinary_to_ordinary:",
                ordinary_result.value,
            )

        except Exception as exc:
            print(
                "ordinary_to_ordinary: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 2. Ordinary source -> CRITICAL destination
        # ---------------------------------------------------------
        try:
            critical_result = fs.evaluate_security(
                "COPY",
                source_file,
                destination=critical_destination,
                security_controller=controller,
            )

            print(
                "ordinary_to_critical:",
                critical_result.value,
            )

        except PermissionError as exc:
            print(
                "ordinary_to_critical: BLOCKED"
            )
            print("message:", exc)

        except Exception as exc:
            print(
                "ordinary_to_critical: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 3. Protection classifications
        #
        # V9ProtectionManager.classify_path() expects strings.
        # ---------------------------------------------------------
        source_protection = (
            fs.protection_manager.classify_path(
                str(source_file)
            )
        )

        ordinary_destination_protection = (
            fs.protection_manager.classify_path(
                str(ordinary_destination)
            )
        )

        critical_destination_protection = (
            fs.protection_manager.classify_path(
                str(critical_destination)
            )
        )

        print(
            "source_protection:",
            source_protection.value,
        )

        print(
            "ordinary_destination_protection:",
            ordinary_destination_protection.value,
        )

        print(
            "critical_destination_protection:",
            critical_destination_protection.value,
        )

        # ---------------------------------------------------------
        # 4. Verify nothing was actually created.
        # ---------------------------------------------------------
        print(
            "source_exists:",
            source_file.exists(),
        )

        print(
            "ordinary_destination_exists:",
            ordinary_destination.exists(),
        )

        print(
            "critical_test_file_exists:",
            critical_destination.exists(),
        )

        print(
            "V9.15.14 source-destination risk consistency test complete"
        )
