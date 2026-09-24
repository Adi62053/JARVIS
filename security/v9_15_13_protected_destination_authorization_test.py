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
                Path(audit_dir) / "v9_15_13_audit.jsonl"
            )
        )

        controller = V9SecurityController(
            permission_manager=permission_manager,
            authorization_manager=authorization_manager,
            audit_logger=audit_logger,
        )

        fs = V9PrivilegedFilesystem()

        protected_copy_destination = Path(
            r"C:\Windows\System32\jarvis_v91513_copy_test.txt"
        )

        protected_move_destination = Path(
            r"C:\Windows\System32\jarvis_v91513_move_test.txt"
        )

        protected_rename_destination = Path(
            r"C:\Windows\System32\jarvis_v91513_rename_test.txt"
        )

        # ---------------------------------------------------------
        # Explicitly authorize every dangerous filesystem operation.
        # ---------------------------------------------------------
        authorization_manager.authorize("FILE.CREATE")
        authorization_manager.authorize("FILE.MODIFY")
        authorization_manager.authorize("FILE.DELETE")

        # ---------------------------------------------------------
        # COPY — protected destination must still be blocked.
        # ---------------------------------------------------------
        try:
            fs.evaluate_security(
                "COPY",
                source_copy,
                destination=protected_copy_destination,
                security_controller=controller,
            )

            print(
                "authorized_protected_copy: UNEXPECTED_ALLOW"
            )

        except PermissionError as exc:
            print(
                "authorized_protected_copy: BLOCKED"
            )
            print("message:", exc)

        # ---------------------------------------------------------
        # MOVE — protected destination must still be blocked.
        # ---------------------------------------------------------
        try:
            fs.evaluate_security(
                "MOVE",
                source_move,
                destination=protected_move_destination,
                security_controller=controller,
            )

            print(
                "authorized_protected_move: UNEXPECTED_ALLOW"
            )

        except PermissionError as exc:
            print(
                "authorized_protected_move: BLOCKED"
            )
            print("message:", exc)

        # ---------------------------------------------------------
        # RENAME — protected destination must still be blocked.
        # ---------------------------------------------------------
        try:
            fs.evaluate_security(
                "RENAME",
                source_rename,
                destination=protected_rename_destination,
                security_controller=controller,
            )

            print(
                "authorized_protected_rename: UNEXPECTED_ALLOW"
            )

        except PermissionError as exc:
            print(
                "authorized_protected_rename: BLOCKED"
            )
            print("message:", exc)

        # ---------------------------------------------------------
        # Verify authorization remains configured.
        # ---------------------------------------------------------
        print(
            "FILE.CREATE_authorized:",
            authorization_manager.is_authorized("FILE.CREATE"),
        )

        print(
            "FILE.MODIFY_authorized:",
            authorization_manager.is_authorized("FILE.MODIFY"),
        )

        print(
            "FILE.DELETE_authorized:",
            authorization_manager.is_authorized("FILE.DELETE"),
        )

        # ---------------------------------------------------------
        # Verify no filesystem mutation occurred.
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
            "V9.15.13 protected-destination authorization test complete"
        )
