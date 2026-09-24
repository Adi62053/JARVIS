from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_audit_logger import V9AuditLogger
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_permission_manager import V9PermissionManager
from security.v9_privileged_filesystem import V9PrivilegedFilesystem
from security.v9_security_controller import V9SecurityController


with TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)

    ordinary_file = root / "ordinary_read_test.txt"
    ordinary_file.write_text(
        "V9.15.20 capability test",
        encoding="utf-8",
    )

    sensitive_folder = Path(r"C:\Users")
    critical_folder = Path(r"C:\Windows")

    protected_file = Path(
        r"C:\Windows\System32\notepad.exe"
    )

    with TemporaryDirectory() as audit_dir:
        permission_manager = V9PermissionManager()
        authorization_manager = V9AuthorizationManager()

        # Permit both filesystem capability types.
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
                Path(audit_dir) / "v9_15_20_audit.jsonl"
            )
        )

        controller = V9SecurityController(
            permission_manager=permission_manager,
            authorization_manager=authorization_manager,
            audit_logger=audit_logger,
        )

        fs = V9PrivilegedFilesystem()

        # ---------------------------------------------------------
        # 1. FILE READ
        # ---------------------------------------------------------

        try:
            result = fs.evaluate_security(
                "READ",
                ordinary_file,
                security_controller=controller,
            )

            print(
                "ordinary_file_read:",
                result.value,
            )

        except Exception as exc:
            print(
                "ordinary_file_read: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 2. SENSITIVE FOLDER READ
        # ---------------------------------------------------------

        try:
            result = fs.evaluate_security(
                "READ",
                sensitive_folder,
                security_controller=controller,
            )

            print(
                "sensitive_folder_read:",
                result.value,
            )

        except Exception as exc:
            print(
                "sensitive_folder_read: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 3. CRITICAL FOLDER READ
        #
        # Classification should remain CRITICAL/HIGH.
        # The controller may require authorization depending on
        # the effective V9 policy.
        # ---------------------------------------------------------

        try:
            result = fs.evaluate_security(
                "READ",
                critical_folder,
                security_controller=controller,
            )

            print(
                "critical_folder_read_without_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "critical_folder_read_without_auth: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 4. Explicit authorization for the FOLDER READ operation.
        #
        # The capability model maps READ to FOLDER.READ.
        # ---------------------------------------------------------

        authorization_manager.authorize(
            "FOLDER.READ"
        )

        try:
            result = fs.evaluate_security(
                "READ",
                critical_folder,
                security_controller=controller,
            )

            print(
                "critical_folder_read_with_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "critical_folder_read_with_auth: ERROR",
                type(exc).__name__,
                exc,
            )

        print(
            "FOLDER.READ_authorized_after_use:",
            authorization_manager.is_authorized(
                "FOLDER.READ"
            ),
        )

        # ---------------------------------------------------------
        # 5. Protected file READ.
        #
        # This should pass filesystem validation but require
        # SYSTEM-level access because the current process is only
        # Administrator.
        # ---------------------------------------------------------

        try:
            result = fs.evaluate_security(
                "READ",
                protected_file,
                security_controller=controller,
            )

            print(
                "protected_file_read:",
                result.value,
            )

        except Exception as exc:
            print(
                "protected_file_read: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 6. Confirm classifications.
        # ---------------------------------------------------------

        sensitive_info = fs.get_security_info(
            sensitive_folder,
            "READ",
        )

        critical_info = fs.get_security_info(
            critical_folder,
            "READ",
        )

        protected_info = fs.get_security_info(
            protected_file,
            "READ",
        )

        print(
            "sensitive_folder_protection:",
            sensitive_info.protection_level.value,
        )

        print(
            "sensitive_folder_risk:",
            sensitive_info.risk_level.value,
        )

        print(
            "critical_folder_protection:",
            critical_info.protection_level.value,
        )

        print(
            "critical_folder_risk:",
            critical_info.risk_level.value,
        )

        print(
            "protected_file_protection:",
            protected_info.protection_level.value,
        )

        print(
            "protected_file_risk:",
            protected_info.risk_level.value,
        )

        # ---------------------------------------------------------
        # 7. Confirm no mutation.
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
            "V9.15.20 capability-aware READ test complete"
        )
