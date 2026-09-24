from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_audit_logger import V9AuditLogger
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_permission_manager import V9PermissionManager
from security.v9_privileged_filesystem import V9PrivilegedFilesystem
from security.v9_security_controller import V9SecurityController


with TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)

    ordinary_target = root / "ordinary_create_test.txt"

    critical_target = Path(
        r"C:\Program Files\JARVIS_V91518_TEST.txt"
    )

    protected_target = Path(
        r"C:\Windows\System32\JARVIS_V91518_TEST.txt"
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
                Path(audit_dir) / "v9_15_18_audit.jsonl"
            )
        )

        controller = V9SecurityController(
            permission_manager=permission_manager,
            authorization_manager=authorization_manager,
            audit_logger=audit_logger,
        )

        fs = V9PrivilegedFilesystem()

        # ---------------------------------------------------------
        # 1. Verify target classifications.
        # ---------------------------------------------------------

        ordinary_info = fs.get_security_info(
            ordinary_target,
            "CREATE",
        )

        critical_info = fs.get_security_info(
            critical_target,
            "CREATE",
        )

        protected_info = fs.get_security_info(
            protected_target,
            "CREATE",
        )

        print(
            "ordinary_target_protection:",
            ordinary_info.protection_level.value,
        )

        print(
            "ordinary_target_risk:",
            ordinary_info.risk_level.value,
        )

        print(
            "critical_target_protection:",
            critical_info.protection_level.value,
        )

        print(
            "critical_target_risk:",
            critical_info.risk_level.value,
        )

        print(
            "protected_target_protection:",
            protected_info.protection_level.value,
        )

        print(
            "protected_target_risk:",
            protected_info.risk_level.value,
        )

        # ---------------------------------------------------------
        # 2. Ordinary CREATE.
        # ---------------------------------------------------------

        try:
            result = fs.evaluate_security(
                "CREATE",
                ordinary_target,
                security_controller=controller,
            )

            print(
                "ordinary_create:",
                result.value,
            )

        except Exception as exc:
            print(
                "ordinary_create: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 3. CRITICAL CREATE without authorization.
        # ---------------------------------------------------------

        try:
            result = fs.evaluate_security(
                "CREATE",
                critical_target,
                security_controller=controller,
            )

            print(
                "critical_create_without_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "critical_create_without_auth: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 4. CRITICAL CREATE with authorization.
        #
        # CREATE maps to FILE.CREATE.
        # ---------------------------------------------------------

        authorization_manager.authorize("FILE.CREATE")

        try:
            result = fs.evaluate_security(
                "CREATE",
                critical_target,
                security_controller=controller,
            )

            print(
                "critical_create_with_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "critical_create_with_auth: ERROR",
                type(exc).__name__,
                exc,
            )

        print(
            "FILE.CREATE_authorized_after_critical_use:",
            authorization_manager.is_authorized(
                "FILE.CREATE"
            ),
        )

        # ---------------------------------------------------------
        # 5. Verify effective CREATE risk directly.
        #
        # CREATE has no destination.
        # ---------------------------------------------------------

        ordinary_effective_risk = (
            fs.get_effective_risk_level(
                "CREATE",
                ordinary_target,
            )
        )

        critical_effective_risk = (
            fs.get_effective_risk_level(
                "CREATE",
                critical_target,
            )
        )

        print(
            "ordinary_create_effective_risk:",
            ordinary_effective_risk.value,
        )

        print(
            "critical_create_effective_risk:",
            critical_effective_risk.value,
        )

        # ---------------------------------------------------------
        # 6. PROTECTED CREATE must remain hard-blocked.
        # Even explicit authorization must not override it.
        # ---------------------------------------------------------

        authorization_manager.authorize("FILE.CREATE")

        try:
            fs.evaluate_security(
                "CREATE",
                protected_target,
                security_controller=controller,
            )

            print(
                "protected_create_with_auth:",
                "UNEXPECTED_ALLOW",
            )

        except PermissionError as exc:
            print(
                "protected_create_with_auth:",
                "BLOCKED",
            )

            print(
                "message:",
                exc,
            )

        # ---------------------------------------------------------
        # 7. Confirm no filesystem mutation occurred.
        # ---------------------------------------------------------

        print(
            "ordinary_target_exists:",
            ordinary_target.exists(),
        )

        print(
            "critical_target_exists:",
            critical_target.exists(),
        )

        print(
            "protected_target_exists:",
            protected_target.exists(),
        )

        print(
            "V9.15.18 CREATE risk-boundary test complete"
        )
