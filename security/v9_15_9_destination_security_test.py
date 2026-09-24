from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_audit_logger import V9AuditLogger
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_permission_manager import V9PermissionManager
from security.v9_privileged_filesystem import V9PrivilegedFilesystem
from security.v9_security_controller import V9SecurityController


with TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)

    source = temp_path / "source.txt"
    ordinary_destination = temp_path / "destination.txt"

    source.write_text(
        "V9.15.9 validation",
        encoding="utf-8",
    )

    permission_manager = V9PermissionManager()
    authorization_manager = V9AuthorizationManager()

    permission_manager.set_permission(
        "FILE",
        True,
    )

    with TemporaryDirectory() as audit_dir:
        audit_logger = V9AuditLogger(
            log_path=str(
                Path(audit_dir) / "v9_15_9_audit.jsonl"
            )
        )

        controller = V9SecurityController(
            permission_manager=permission_manager,
            authorization_manager=authorization_manager,
            audit_logger=audit_logger,
        )

        fs = V9PrivilegedFilesystem()

        try:
            info = fs.validate_operation(
                "COPY",
                source,
                ordinary_destination,
            )

            print("ordinary_destination_validation: PASS")
            print("source_exists:", info.exists)
            print("source_protection:", info.protection_level)

            decision = fs.evaluate_security(
                "COPY",
                source,
                security_controller=controller,
            )

            print("ordinary_source_security_decision:", decision)
            print("ordinary_destination_not_modified:", not ordinary_destination.exists())

        except Exception as exc:
            print("ordinary_destination_validation: FAIL")
            print("error:", exc)

        protected_destination = Path(
            r"C:\Windows\System32\jarvis_v9159_test.txt"
        )

        try:
            fs.validate_operation(
                "COPY",
                source,
                protected_destination,
            )

            print("protected_destination_gate: UNEXPECTED_ALLOW")

        except PermissionError as exc:
            print("protected_destination_gate: PASS")
            print("message:", exc)

        print("V9.15.9 destination security evaluation test complete")
