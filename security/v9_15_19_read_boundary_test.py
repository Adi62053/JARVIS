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
        "V9.15.19 read test",
        encoding="utf-8",
    )

    sensitive_path = Path(
        r"C:\Users"
    )

    critical_path = Path(
        r"C:\Windows"
    )

    protected_path = Path(
        r"C:\Windows\System32\notepad.exe"
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
                Path(audit_dir) / "v9_15_19_audit.jsonl"
            )
        )

        controller = V9SecurityController(
            permission_manager=permission_manager,
            authorization_manager=authorization_manager,
            audit_logger=audit_logger,
        )

        fs = V9PrivilegedFilesystem()

        # ---------------------------------------------------------
        # 1. Read classifications.
        # ---------------------------------------------------------

        ordinary_info = fs.get_security_info(
            ordinary_file,
            "READ",
        )

        sensitive_info = fs.get_security_info(
            sensitive_path,
            "READ",
        )

        critical_info = fs.get_security_info(
            critical_path,
            "READ",
        )

        protected_info = fs.get_security_info(
            protected_path,
            "READ",
        )

        print(
            "ordinary_read_protection:",
            ordinary_info.protection_level.value,
        )

        print(
            "ordinary_read_risk:",
            ordinary_info.risk_level.value,
        )

        print(
            "sensitive_read_protection:",
            sensitive_info.protection_level.value,
        )

        print(
            "sensitive_read_risk:",
            sensitive_info.risk_level.value,
        )

        print(
            "critical_read_protection:",
            critical_info.protection_level.value,
        )

        print(
            "critical_read_risk:",
            critical_info.risk_level.value,
        )

        print(
            "protected_read_protection:",
            protected_info.protection_level.value,
        )

        print(
            "protected_read_risk:",
            protected_info.risk_level.value,
        )

        # ---------------------------------------------------------
        # 2. Verify hard operation-protection semantics.
        #
        # READ must not be treated as a protected mutation.
        # ---------------------------------------------------------

        print(
            "sensitive_read_operation_protected:",
            fs.is_operation_protected(
                sensitive_path,
                "READ",
            ),
        )

        print(
            "critical_read_operation_protected:",
            fs.is_operation_protected(
                critical_path,
                "READ",
            ),
        )

        print(
            "protected_read_operation_protected:",
            fs.is_operation_protected(
                protected_path,
                "READ",
            ),
        )

        # ---------------------------------------------------------
        # 3. Validate protected READ directly.
        # ---------------------------------------------------------

        try:
            protected_read_validation = fs.validate_operation(
                "READ",
                protected_path,
            )

            print(
                "protected_read_validation:",
                "ALLOWED",
            )

            print(
                "protected_read_validation_level:",
                protected_read_validation.protection_level.value,
            )

        except Exception as exc:
            print(
                "protected_read_validation: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 4. Evaluate READ through the complete V9 controller.
        # ---------------------------------------------------------

        for label, path in (
            ("ordinary", ordinary_file),
            ("sensitive", sensitive_path),
            ("critical", critical_path),
            ("protected", protected_path),
        ):
            try:
                result = fs.evaluate_security(
                    "READ",
                    path,
                    security_controller=controller,
                )

                print(
                    f"{label}_read_decision:",
                    result.value,
                )

            except Exception as exc:
                print(
                    f"{label}_read_decision: ERROR",
                    type(exc).__name__,
                    exc,
                )

        # ---------------------------------------------------------
        # 5. Verify READ does not consume authorization.
        #
        # No authorization is intentionally configured here.
        # ---------------------------------------------------------

        print(
            "FILE.READ_authorized:",
            authorization_manager.is_authorized(
                "FILE.READ"
            ),
        )

        # ---------------------------------------------------------
        # 6. Confirm the test file remains unchanged.
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
            "protected_file_exists:",
            protected_path.exists(),
        )

        print(
            "V9.15.19 READ protection-boundary test complete"
        )
