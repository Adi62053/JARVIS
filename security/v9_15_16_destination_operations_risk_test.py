from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_audit_logger import V9AuditLogger
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_permission_manager import V9PermissionManager
from security.v9_privileged_filesystem import V9PrivilegedFilesystem
from security.v9_security_controller import V9SecurityController


with TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)

    # Separate source files so every operation remains independent.
    copy_source = root / "copy_source.txt"
    move_source = root / "move_source.txt"
    rename_source = root / "rename_source.txt"

    copy_source.write_text("COPY test", encoding="utf-8")
    move_source.write_text("MOVE test", encoding="utf-8")
    rename_source.write_text("RENAME test", encoding="utf-8")

    ordinary_copy_destination = root / "copy_destination.txt"
    ordinary_move_destination = root / "move_destination.txt"
    ordinary_rename_destination = root / "rename_destination.txt"

    critical_destination = Path(
        r"C:\Program Files\JARVIS_V91516_TEST.txt"
    )

    protected_destination = Path(
        r"C:\Windows\System32\JARVIS_V91516_TEST.txt"
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
                Path(audit_dir) / "v9_15_16_audit.jsonl"
            )
        )

        controller = V9SecurityController(
            permission_manager=permission_manager,
            authorization_manager=authorization_manager,
            audit_logger=audit_logger,
        )

        fs = V9PrivilegedFilesystem()

        # ---------------------------------------------------------
        # 1. COPY: ordinary -> ordinary
        # ---------------------------------------------------------
        try:
            result = fs.evaluate_security(
                "COPY",
                copy_source,
                destination=ordinary_copy_destination,
                security_controller=controller,
            )

            print(
                "COPY_ordinary_to_ordinary:",
                result.value,
            )

        except Exception as exc:
            print(
                "COPY_ordinary_to_ordinary: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 2. COPY: ordinary -> CRITICAL, no authorization
        # ---------------------------------------------------------
        try:
            result = fs.evaluate_security(
                "COPY",
                copy_source,
                destination=critical_destination,
                security_controller=controller,
            )

            print(
                "COPY_ordinary_to_critical_without_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "COPY_ordinary_to_critical_without_auth: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 3. MOVE: ordinary -> CRITICAL, no authorization
        # ---------------------------------------------------------
        try:
            result = fs.evaluate_security(
                "MOVE",
                move_source,
                destination=critical_destination,
                security_controller=controller,
            )

            print(
                "MOVE_ordinary_to_critical_without_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "MOVE_ordinary_to_critical_without_auth: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 4. RENAME: ordinary -> CRITICAL, no authorization
        # ---------------------------------------------------------
        try:
            result = fs.evaluate_security(
                "RENAME",
                rename_source,
                destination=critical_destination,
                security_controller=controller,
            )

            print(
                "RENAME_ordinary_to_critical_without_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "RENAME_ordinary_to_critical_without_auth: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 5. Authorize each mapped FILE operation separately.
        #
        # COPY   -> FILE.CREATE
        # MOVE   -> FILE.MODIFY
        # RENAME -> FILE.MODIFY
        # ---------------------------------------------------------

        authorization_manager.authorize("FILE.CREATE")

        try:
            result = fs.evaluate_security(
                "COPY",
                copy_source,
                destination=critical_destination,
                security_controller=controller,
            )

            print(
                "COPY_ordinary_to_critical_with_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "COPY_ordinary_to_critical_with_auth: ERROR",
                type(exc).__name__,
                exc,
            )

        authorization_manager.authorize("FILE.MODIFY")

        try:
            result = fs.evaluate_security(
                "MOVE",
                move_source,
                destination=critical_destination,
                security_controller=controller,
            )

            print(
                "MOVE_ordinary_to_critical_with_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "MOVE_ordinary_to_critical_with_auth: ERROR",
                type(exc).__name__,
                exc,
            )

        authorization_manager.authorize("FILE.MODIFY")

        try:
            result = fs.evaluate_security(
                "RENAME",
                rename_source,
                destination=critical_destination,
                security_controller=controller,
            )

            print(
                "RENAME_ordinary_to_critical_with_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "RENAME_ordinary_to_critical_with_auth: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 6. Protected destination must remain hard-blocked even
        #    when authorization is present.
        # ---------------------------------------------------------

        authorization_manager.authorize("FILE.CREATE")

        try:
            fs.evaluate_security(
                "COPY",
                copy_source,
                destination=protected_destination,
                security_controller=controller,
            )

            print(
                "COPY_to_protected_with_auth:",
                "UNEXPECTED_ALLOW",
            )

        except PermissionError as exc:
            print(
                "COPY_to_protected_with_auth:",
                "BLOCKED",
            )
            print("message:", exc)

        authorization_manager.authorize("FILE.MODIFY")

        try:
            fs.evaluate_security(
                "MOVE",
                move_source,
                destination=protected_destination,
                security_controller=controller,
            )

            print(
                "MOVE_to_protected_with_auth:",
                "UNEXPECTED_ALLOW",
            )

        except PermissionError as exc:
            print(
                "MOVE_to_protected_with_auth:",
                "BLOCKED",
            )
            print("message:", exc)

        authorization_manager.authorize("FILE.MODIFY")

        try:
            fs.evaluate_security(
                "RENAME",
                rename_source,
                destination=protected_destination,
                security_controller=controller,
            )

            print(
                "RENAME_to_protected_with_auth:",
                "UNEXPECTED_ALLOW",
            )

        except PermissionError as exc:
            print(
                "RENAME_to_protected_with_auth:",
                "BLOCKED",
            )
            print("message:", exc)

        # ---------------------------------------------------------
        # 7. Verify that the test performed no filesystem mutation.
        # ---------------------------------------------------------

        print("copy_source_exists:", copy_source.exists())
        print("move_source_exists:", move_source.exists())
        print("rename_source_exists:", rename_source.exists())

        print(
            "ordinary_copy_destination_exists:",
            ordinary_copy_destination.exists(),
        )

        print(
            "ordinary_move_destination_exists:",
            ordinary_move_destination.exists(),
        )

        print(
            "ordinary_rename_destination_exists:",
            ordinary_rename_destination.exists(),
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
            "V9.15.16 all-destination-operation risk test complete"
        )
