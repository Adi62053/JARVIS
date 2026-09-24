from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_audit_logger import V9AuditLogger
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_permission_manager import V9PermissionManager
from security.v9_privileged_filesystem import V9PrivilegedFilesystem
from security.v9_security_controller import V9SecurityController


with TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)

    ordinary_destination = root / "ordinary_destination.txt"

    # Existing harmless Windows file used only for security classification.
    critical_source = Path(
        r"C:\Windows\notepad.exe"
    )

    protected_source = Path(
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
                Path(audit_dir) / "v9_15_17_audit.jsonl"
            )
        )

        controller = V9SecurityController(
            permission_manager=permission_manager,
            authorization_manager=authorization_manager,
            audit_logger=audit_logger,
        )

        fs = V9PrivilegedFilesystem()

        # ---------------------------------------------------------
        # 1. Verify classifications
        # ---------------------------------------------------------

        critical_info = fs.get_security_info(
            critical_source,
            "COPY",
        )

        protected_info = fs.get_security_info(
            protected_source,
            "COPY",
        )

        print(
            "critical_source_protection:",
            critical_info.protection_level.value,
        )

        print(
            "critical_source_risk:",
            critical_info.risk_level.value,
        )

        print(
            "protected_source_protection:",
            protected_info.protection_level.value,
        )

        print(
            "protected_source_risk:",
            protected_info.risk_level.value,
        )

        # ---------------------------------------------------------
        # 2. CRITICAL source -> ordinary destination
        #
        # No authorization.
        #
        # Critical source risk must propagate.
        # ---------------------------------------------------------

        try:
            result = fs.evaluate_security(
                "COPY",
                critical_source,
                destination=ordinary_destination,
                security_controller=controller,
            )

            print(
                "critical_to_ordinary_without_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "critical_to_ordinary_without_auth: ERROR",
                type(exc).__name__,
                exc,
            )

        # ---------------------------------------------------------
        # 3. Authorize FILE.CREATE.
        #
        # COPY maps to FILE.CREATE.
        # ---------------------------------------------------------

        authorization_manager.authorize("FILE.CREATE")

        try:
            result = fs.evaluate_security(
                "COPY",
                critical_source,
                destination=ordinary_destination,
                security_controller=controller,
            )

            print(
                "critical_to_ordinary_with_auth:",
                result.value,
            )

        except Exception as exc:
            print(
                "critical_to_ordinary_with_auth: ERROR",
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
        # 5. Verify effective risk directly.
        # ---------------------------------------------------------

        effective_risk = fs.get_effective_risk_level(
            "COPY",
            critical_source,
            destination=ordinary_destination,
        )

        print(
            "critical_to_ordinary_effective_risk:",
            effective_risk.value,
        )

        # ---------------------------------------------------------
        # 6. PROTECTED source must remain hard-blocked even with
        #    explicit authorization.
        # ---------------------------------------------------------

        authorization_manager.authorize("FILE.CREATE")

        try:
            fs.evaluate_security(
                "COPY",
                protected_source,
                destination=ordinary_destination,
                security_controller=controller,
            )

            print(
                "protected_to_ordinary_with_auth:",
                "UNEXPECTED_ALLOW",
            )

        except PermissionError as exc:
            print(
                "protected_to_ordinary_with_auth:",
                "BLOCKED",
            )

            print(
                "message:",
                exc,
            )

        # ---------------------------------------------------------
        # 7. No actual filesystem mutation occurred.
        # ---------------------------------------------------------

        print(
            "critical_source_exists:",
            critical_source.exists(),
        )

        print(
            "protected_source_exists:",
            protected_source.exists(),
        )

        print(
            "ordinary_destination_exists:",
            ordinary_destination.exists(),
        )

        print(
            "V9.15.17 source-risk propagation test complete"
        )
