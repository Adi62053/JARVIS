from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_audit_logger import V9AuditLogger
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_permission_manager import V9PermissionManager
from security.v9_privileged_filesystem import V9PrivilegedFilesystem
from security.v9_security_controller import V9SecurityController


with TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)

    ordinary_file = root / "ordinary.txt"
    ordinary_file.write_text(
        "V9.15.21 mutation test",
        encoding="utf-8",
    )

    ordinary_folder = root / "ordinary_folder"
    ordinary_folder.mkdir()

    sensitive_file = Path(
        r"C:\Users\Public"
    )

    critical_file = Path(
        r"C:\Windows\notepad.exe"
    )

    critical_folder = Path(
        r"C:\Windows"
    )

    protected_file = Path(
        r"C:\Windows\System32\notepad.exe"
    )

    protected_folder = Path(
        r"C:\Windows\System32"
    )

    with TemporaryDirectory() as audit_dir:
        permission_manager = V9PermissionManager()
        authorization_manager = V9AuthorizationManager()

        permission_manager.set_permission(
            "FILE",
            True,
        )

        permission_manager.set_permission(
            "FOLDER",
            True,
        )

        audit_logger = V9AuditLogger(
            log_path=str(
                Path(audit_dir) / "v9_15_21_audit.jsonl"
            )
        )

        controller = V9SecurityController(
            permission_manager=permission_manager,
            authorization_manager=authorization_manager,
            audit_logger=audit_logger,
        )

        fs = V9PrivilegedFilesystem()

        # ---------------------------------------------------------
        # 1. Classification matrix
        # ---------------------------------------------------------

        test_targets = (
            ("ordinary_file", ordinary_file),
            ("ordinary_folder", ordinary_folder),
            ("sensitive_file", sensitive_file),
            ("critical_file", critical_file),
            ("critical_folder", critical_folder),
            ("protected_file", protected_file),
            ("protected_folder", protected_folder),
        )

        for label, path in test_targets:
            info = fs.get_security_info(
                path,
                "WRITE",
            )

            print(
                f"{label}_protection:",
                info.protection_level.value,
            )

            print(
                f"{label}_write_risk:",
                info.risk_level.value,
            )

        # ---------------------------------------------------------
        # 2. Verify ordinary FILE mutation decisions.
        # ---------------------------------------------------------

        for operation in (
            "WRITE",
            "MODIFY",
            "DELETE",
        ):
            try:
                result = fs.evaluate_security(
                    operation,
                    ordinary_file,
                    security_controller=controller,
                )

                print(
                    f"ordinary_file_{operation.lower()}:",
                    result.value,
                )

            except Exception as exc:
                print(
                    f"ordinary_file_{operation.lower()}: ERROR",
                    type(exc).__name__,
                    exc,
                )

        # ---------------------------------------------------------
        # 3. Verify ordinary FOLDER mutation decisions.
        # ---------------------------------------------------------

        for operation in (
            "WRITE",
            "MODIFY",
            "DELETE",
        ):
            try:
                result = fs.evaluate_security(
                    operation,
                    ordinary_folder,
                    resource_type="FOLDER",
                    security_controller=controller,
                )

                print(
                    f"ordinary_folder_{operation.lower()}:",
                    result.value,
                )

            except Exception as exc:
                print(
                    f"ordinary_folder_{operation.lower()}: ERROR",
                    type(exc).__name__,
                    exc,
                )

        # ---------------------------------------------------------
        # 4. CRITICAL FILE mutations without authorization.
        # ---------------------------------------------------------

        for operation in (
            "WRITE",
            "MODIFY",
            "DELETE",
        ):
            try:
                result = fs.evaluate_security(
                    operation,
                    critical_file,
                    security_controller=controller,
                )

                print(
                    f"critical_file_{operation.lower()}_without_auth:",
                    result.value,
                )

            except Exception as exc:
                print(
                    f"critical_file_{operation.lower()}_without_auth: ERROR",
                    type(exc).__name__,
                    exc,
                )

        # ---------------------------------------------------------
        # 5. CRITICAL FOLDER mutations without authorization.
        # ---------------------------------------------------------

        for operation in (
            "WRITE",
            "MODIFY",
            "DELETE",
        ):
            try:
                result = fs.evaluate_security(
                    operation,
                    critical_folder,
                    resource_type="FOLDER",
                    security_controller=controller,
                )

                print(
                    f"critical_folder_{operation.lower()}_without_auth:",
                    result.value,
                )

            except Exception as exc:
                print(
                    f"critical_folder_{operation.lower()}_without_auth: ERROR",
                    type(exc).__name__,
                    exc,
                )

        # ---------------------------------------------------------
        # 6. Authorize and verify CRITICAL FILE mutations.
        # ---------------------------------------------------------

        for operation in (
            "WRITE",
            "MODIFY",
            "DELETE",
        ):
            authorization_manager.authorize(
                f"FILE.{operation}"
            )

            try:
                result = fs.evaluate_security(
                    operation,
                    critical_file,
                    security_controller=controller,
                )

                print(
                    f"critical_file_{operation.lower()}_with_auth:",
                    result.value,
                )

            except Exception as exc:
                print(
                    f"critical_file_{operation.lower()}_with_auth: ERROR",
                    type(exc).__name__,
                    exc,
                )

            print(
                f"FILE.{operation}_authorized_after_use:",
                authorization_manager.is_authorized(
                    f"FILE.{operation}"
                ),
            )

        # ---------------------------------------------------------
        # 7. Authorize and verify CRITICAL FOLDER mutations.
        # ---------------------------------------------------------

        for operation in (
            "WRITE",
            "MODIFY",
            "DELETE",
        ):
            authorization_manager.authorize(
                f"FOLDER.{operation}"
            )

            try:
                result = fs.evaluate_security(
                    operation,
                    critical_folder,
                    resource_type="FOLDER",
                    security_controller=controller,
                )

                print(
                    f"critical_folder_{operation.lower()}_with_auth:",
                    result.value,
                )

            except Exception as exc:
                print(
                    f"critical_folder_{operation.lower()}_with_auth: ERROR",
                    type(exc).__name__,
                    exc,
                )

            print(
                f"FOLDER.{operation}_authorized_after_use:",
                authorization_manager.is_authorized(
                    f"FOLDER.{operation}"
                ),
            )

        # ---------------------------------------------------------
        # 8. PROTECTED FILE mutations must be hard-blocked.
        # ---------------------------------------------------------

        for operation in (
            "WRITE",
            "MODIFY",
            "DELETE",
        ):
            authorization_manager.authorize(
                f"FILE.{operation}"
            )

            try:
                fs.evaluate_security(
                    operation,
                    protected_file,
                    security_controller=controller,
                )

                print(
                    f"protected_file_{operation.lower()}_with_auth:",
                    "UNEXPECTED_ALLOW",
                )

            except PermissionError as exc:
                print(
                    f"protected_file_{operation.lower()}_with_auth:",
                    "BLOCKED",
                )

                print(
                    "message:",
                    exc,
                )

        # ---------------------------------------------------------
        # 9. PROTECTED FOLDER mutations must be hard-blocked.
        # ---------------------------------------------------------

        for operation in (
            "WRITE",
            "MODIFY",
            "DELETE",
        ):
            authorization_manager.authorize(
                f"FOLDER.{operation}"
            )

            try:
                fs.evaluate_security(
                    operation,
                    protected_folder,
                    resource_type="FOLDER",
                    security_controller=controller,
                )

                print(
                    f"protected_folder_{operation.lower()}_with_auth:",
                    "UNEXPECTED_ALLOW",
                )

            except PermissionError as exc:
                print(
                    f"protected_folder_{operation.lower()}_with_auth:",
                    "BLOCKED",
                )

                print(
                    "message:",
                    exc,
                )

        # ---------------------------------------------------------
        # 10. Direct operation protection checks.
        # ---------------------------------------------------------

        for label, path in (
            ("critical_file", critical_file),
            ("critical_folder", critical_folder),
            ("protected_file", protected_file),
            ("protected_folder", protected_folder),
        ):
            for operation in (
                "WRITE",
                "MODIFY",
                "DELETE",
            ):
                print(
                    f"{label}_{operation.lower()}_protected:",
                    fs.is_operation_protected(
                        path,
                        operation,
                    ),
                )

        # ---------------------------------------------------------
        # 11. Confirm no filesystem mutation occurred.
        # ---------------------------------------------------------

        print(
            "ordinary_file_exists:",
            ordinary_file.exists(),
        )

        print(
            "ordinary_file_content:",
            ordinary_file.read_text(
                encoding="utf-8"
            ),
        )

        print(
            "ordinary_folder_exists:",
            ordinary_folder.exists(),
        )

        print(
            "critical_file_exists:",
            critical_file.exists(),
        )

        print(
            "critical_folder_exists:",
            critical_folder.exists(),
        )

        print(
            "protected_file_exists:",
            protected_file.exists(),
        )

        print(
            "protected_folder_exists:",
            protected_folder.exists(),
        )

        print(
            "V9.15.21 mutation-operation security matrix test complete"
        )
