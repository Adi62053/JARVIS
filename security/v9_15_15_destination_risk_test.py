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
        "V9.15.15 risk propagation test",
        encoding="utf-8",
    )

    critical_destination = Path(
        r"C:\Program Files\JARVIS_V91515_TEST.txt"
    )

    protected_destination = Path(
        r"C:\Windows\System32\JARVIS_V91515_TEST.txt"
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
                Path(audit_dir) / "v9_15_15_audit.jsonl"
            )
        )

        controller = V9SecurityController(
            permission_manager=permission_manager,
            authorization_manager=authorization_manager,
            audit_logger=audit_logger,
        )

        fs = V9PrivilegedFilesystem()

        # ---------------------------------------------------------
        # 1. Ordinary -> Ordinary
        # ---------------------------------------------------------
        try:
            result = fs.evaluate_security(
                "COPY",
                source_file,
                destination=ordinary_destination,
                security_controller=controller,
            )

            print(
                "ordinary_to_ordinary:",
                result.value,
            )

        except Exception as exc:
            print(
                "ordinary_to_ordinary: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 2. Ordinary -> CRITICAL, without authorization
        # ---------------------------------------------------------
        try:
            result = fs.evaluate_security(
                "COPY",
                source_file,
                destination=critical_destination,
                security_controller=controller,
            )

            print(
                "ordinary_to_critical_without_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "ordinary_to_critical_without_auth: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 3. Authorize the mapped COPY operation.
        #
        # COPY maps to SecurityOperation.CREATE.
        # ---------------------------------------------------------
        authorization_manager.authorize("FILE.CREATE")

        try:
            result = fs.evaluate_security(
                "COPY",
                source_file,
                destination=critical_destination,
                security_controller=controller,
            )

            print(
                "ordinary_to_critical_with_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "ordinary_to_critical_with_auth: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 4. Verify authorization was consumed.
        # ---------------------------------------------------------
        print(
            "FILE.CREATE_authorized_after_use:",
            authorization_manager.is_authorized(
                "FILE.CREATE"
            ),
        )

        # ---------------------------------------------------------
        # 5. Protected destination must remain hard-blocked.
        # ---------------------------------------------------------
        authorization_manager.authorize("FILE.CREATE")

        try:
            fs.evaluate_security(
                "COPY",
                source_file,
                destination=protected_destination,
                security_controller=controller,
            )

            print(
                "ordinary_to_protected_with_auth:",
                "UNEXPECTED_ALLOW",
            )

        except PermissionError as exc:
            print(
                "ordinary_to_protected_with_auth:",
                "BLOCKED",
            )
            print(
                "message:",
                exc,
            )

        # ---------------------------------------------------------
        # 6. Verify no actual filesystem mutation occurred.
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
            "protected_test_file_exists:",
            protected_destination.exists(),
        )

        print(
            "V9.15.15 destination-risk propagation test complete"
        )
