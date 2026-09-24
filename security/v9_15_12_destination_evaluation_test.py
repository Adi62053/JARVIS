from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_audit_logger import V9AuditLogger
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_permission_manager import V9PermissionManager
from security.v9_privileged_filesystem import V9PrivilegedFilesystem
from security.v9_security_controller import V9SecurityController


with TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)

    source_copy = root / "copy_source.txt"
    source_move = root / "move_source.txt"
    source_rename = root / "rename_source.txt"

    destination_copy = root / "copy_destination.txt"
    destination_move = root / "move_destination.txt"
    destination_rename = root / "rename_destination.txt"

    source_copy.write_text("copy test", encoding="utf-8")
    source_move.write_text("move test", encoding="utf-8")
    source_rename.write_text("rename test", encoding="utf-8")

    with TemporaryDirectory() as audit_dir:
        permission_manager = V9PermissionManager()
        authorization_manager = V9AuthorizationManager()

        permission_manager.set_permission(
            "FILE",
            True,
        )

        audit_logger = V9AuditLogger(
            log_path=str(
                Path(audit_dir) / "v9_15_12_audit.jsonl"
            )
        )

        controller = V9SecurityController(
            permission_manager=permission_manager,
            authorization_manager=authorization_manager,
            audit_logger=audit_logger,
        )

        fs = V9PrivilegedFilesystem()

        # ---------------------------------------------------------
        # COPY
        # ---------------------------------------------------------
        try:
            result = fs.evaluate_security(
                "COPY",
                source_copy,
                destination=destination_copy,
                security_controller=controller,
            )

            print(
                "ordinary_copy_destination:",
                result.value,
            )

        except Exception as exc:
            print(
                "ordinary_copy_destination: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # MOVE
        # ---------------------------------------------------------
        authorization_manager.authorize("FILE.MODIFY")

        try:
            result = fs.evaluate_security(
                "MOVE",
                source_move,
                destination=destination_move,
                security_controller=controller,
            )

            print(
                "ordinary_move_destination:",
                result.value,
            )

        except Exception as exc:
            print(
                "ordinary_move_destination: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # RENAME
        # ---------------------------------------------------------
        authorization_manager.authorize("FILE.MODIFY")

        try:
            result = fs.evaluate_security(
                "RENAME",
                source_rename,
                destination=destination_rename,
                security_controller=controller,
            )

            print(
                "ordinary_rename_destination:",
                result.value,
            )

        except Exception as exc:
            print(
                "ordinary_rename_destination: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # PROTECTED DESTINATION TESTS
        # ---------------------------------------------------------
        protected_copy_destination = Path(
            r"C:\Windows\System32\jarvis_v91512_copy_test.txt"
        )

        protected_move_destination = Path(
            r"C:\Windows\System32\jarvis_v91512_move_test.txt"
        )

        protected_rename_destination = Path(
            r"C:\Windows\System32\jarvis_v91512_rename_test.txt"
        )

        for operation, source, destination in (
            (
                "COPY",
                source_copy,
                protected_copy_destination,
            ),
            (
                "MOVE",
                source_move,
                protected_move_destination,
            ),
            (
                "RENAME",
                source_rename,
                protected_rename_destination,
            ),
        ):
            try:
                fs.evaluate_security(
                    operation,
                    source,
                    destination=destination,
                    security_controller=controller,
                )

                print(
                    f"protected_{operation.lower()}_destination: "
                    "UNEXPECTED_ALLOW"
                )

            except PermissionError as exc:
                print(
                    f"protected_{operation.lower()}_destination: BLOCKED"
                )
                print("message:", exc)

        # ---------------------------------------------------------
        # NO FILESYSTEM MUTATION CHECK
        # ---------------------------------------------------------
        print(
            "source_copy_exists:",
            source_copy.exists(),
        )

        print(
            "source_move_exists:",
            source_move.exists(),
        )

        print(
            "source_rename_exists:",
            source_rename.exists(),
        )

        print(
            "ordinary_destinations_created:",
            destination_copy.exists()
            or destination_move.exists()
            or destination_rename.exists(),
        )

        print("V9.15.12 destination-aware test complete")