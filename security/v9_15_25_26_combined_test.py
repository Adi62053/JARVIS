from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_audit_logger import V9AuditLogger
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_permission_manager import V9PermissionManager
from security.v9_privileged_filesystem import V9PrivilegedFilesystem
from security.v9_security_controller import V9SecurityController


def show(label, value):
    print(f"{label}: {value}")


with TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)

    source = root / "source.txt"
    source.write_text(
        "V9.15.25-26 integration test",
        encoding="utf-8",
    )

    second_source = root / "second.txt"
    second_source.write_text(
        "second source",
        encoding="utf-8",
    )

    ordinary_destination = root / "ordinary_destination.txt"
    critical_destination = Path(
        r"C:\Program Files\JARVIS_V91525_TEST.txt"
    )
    protected_destination = Path(
        r"C:\Windows\System32\JARVIS_V91525_TEST.txt"
    )
    protected_file = Path(
        r"C:\Windows\System32\notepad.exe"
    )

    nonexistent_source = root / "missing.txt"

    audit_path = root / "audit.jsonl"

    permission_manager = V9PermissionManager()
    authorization_manager = V9AuthorizationManager()

    permission_manager.set_permission(
        "FILE",
        True,
    )

    audit_logger = V9AuditLogger(
        log_path=str(audit_path)
    )

    controller = V9SecurityController(
        permission_manager=permission_manager,
        authorization_manager=authorization_manager,
        audit_logger=audit_logger,
    )

    fs = V9PrivilegedFilesystem()

    print("=== V9.15.25 FULL INTEGRATION TEST ===")

    # ---------------------------------------------------------
    # READ
    # ---------------------------------------------------------

    read_result = fs.evaluate_security(
        "READ",
        source,
        security_controller=controller,
    )

    show(
        "integration_read",
        read_result.value,
    )

    # ---------------------------------------------------------
    # WRITE -> authorization -> ALLOW
    # ---------------------------------------------------------

    write_result = fs.evaluate_security(
        "WRITE",
        source,
        security_controller=controller,
    )

    show(
        "integration_write_without_auth",
        write_result.value,
    )

    authorization_manager.authorize(
        "FILE.WRITE"
    )

    write_authorized = fs.evaluate_security(
        "WRITE",
        source,
        security_controller=controller,
    )

    show(
        "integration_write_with_auth",
        write_authorized.value,
    )

    show(
        "FILE.WRITE_authorized_after_use",
        authorization_manager.is_authorized(
            "FILE.WRITE"
        ),
    )

    # ---------------------------------------------------------
    # MODIFY -> authorization -> ALLOW
    # ---------------------------------------------------------

    modify_result = fs.evaluate_security(
        "MODIFY",
        source,
        security_controller=controller,
    )

    show(
        "integration_modify_without_auth",
        modify_result.value,
    )

    authorization_manager.authorize(
        "FILE.MODIFY"
    )

    modify_authorized = fs.evaluate_security(
        "MODIFY",
        source,
        security_controller=controller,
    )

    show(
        "integration_modify_with_auth",
        modify_authorized.value,
    )

    show(
        "FILE.MODIFY_authorized_after_use",
        authorization_manager.is_authorized(
            "FILE.MODIFY"
        ),
    )

    # ---------------------------------------------------------
    # DELETE -> authorization -> ALLOW
    # ---------------------------------------------------------

    delete_result = fs.evaluate_security(
        "DELETE",
        source,
        security_controller=controller,
    )

    show(
        "integration_delete_without_auth",
        delete_result.value,
    )

    authorization_manager.authorize(
        "FILE.DELETE"
    )

    delete_authorized = fs.evaluate_security(
        "DELETE",
        source,
        security_controller=controller,
    )

    show(
        "integration_delete_with_auth",
        delete_authorized.value,
    )

    show(
        "FILE.DELETE_authorized_after_use",
        authorization_manager.is_authorized(
            "FILE.DELETE"
        ),
    )

    # ---------------------------------------------------------
    # COPY ordinary -> ordinary
    # ---------------------------------------------------------

    copy_result = fs.evaluate_security(
        "COPY",
        source,
        destination=ordinary_destination,
        security_controller=controller,
    )

    show(
        "integration_copy_ordinary_to_ordinary",
        copy_result.value,
    )

    # ---------------------------------------------------------
    # COPY ordinary -> critical
    # ---------------------------------------------------------

    critical_copy_result = fs.evaluate_security(
        "COPY",
        source,
        destination=critical_destination,
        security_controller=controller,
    )

    show(
        "integration_copy_to_critical_without_auth",
        critical_copy_result.value,
    )

    authorization_manager.authorize(
        "FILE.CREATE"
    )

    critical_copy_authorized = fs.evaluate_security(
        "COPY",
        source,
        destination=critical_destination,
        security_controller=controller,
    )

    show(
        "integration_copy_to_critical_with_auth",
        critical_copy_authorized.value,
    )

    show(
        "FILE.CREATE_authorized_after_use",
        authorization_manager.is_authorized(
            "FILE.CREATE"
        ),
    )

    # ---------------------------------------------------------
    # MOVE ordinary -> critical
    # ---------------------------------------------------------

    move_result = fs.evaluate_security(
        "MOVE",
        second_source,
        destination=critical_destination,
        security_controller=controller,
    )

    show(
        "integration_move_to_critical_without_auth",
        move_result.value,
    )

    authorization_manager.authorize(
        "FILE.MODIFY"
    )

    move_authorized = fs.evaluate_security(
        "MOVE",
        second_source,
        destination=critical_destination,
        security_controller=controller,
    )

    show(
        "integration_move_to_critical_with_auth",
        move_authorized.value,
    )

    show(
        "FILE.MODIFY_authorized_after_move",
        authorization_manager.is_authorized(
            "FILE.MODIFY"
        ),
    )

    # ---------------------------------------------------------
    # RENAME ordinary -> critical
    # ---------------------------------------------------------

    rename_result = fs.evaluate_security(
        "RENAME",
        source,
        destination=critical_destination,
        security_controller=controller,
    )

    show(
        "integration_rename_to_critical_without_auth",
        rename_result.value,
    )

    # ---------------------------------------------------------
    # Protected READ -> elevation
    # ---------------------------------------------------------

    protected_read = fs.evaluate_security(
        "READ",
        protected_file,
        security_controller=controller,
    )

    show(
        "integration_protected_read",
        protected_read.value,
    )

    # ---------------------------------------------------------
    # Protected DELETE -> hard block
    # ---------------------------------------------------------

    authorization_manager.authorize(
        "FILE.DELETE"
    )

    try:
        fs.evaluate_security(
            "DELETE",
            protected_file,
            security_controller=controller,
        )

        show(
            "integration_protected_delete_with_auth",
            "UNEXPECTED_ALLOW",
        )

    except PermissionError as exc:
        show(
            "integration_protected_delete_with_auth",
            "BLOCKED",
        )
        show(
            "integration_protected_delete_message",
            exc,
        )

    # ---------------------------------------------------------
    # Protected destination -> hard block
    # ---------------------------------------------------------

    authorization_manager.authorize(
        "FILE.CREATE"
    )

    try:
        fs.evaluate_security(
            "COPY",
            source,
            destination=protected_destination,
            security_controller=controller,
        )

        show(
            "integration_copy_to_protected_with_auth",
            "UNEXPECTED_ALLOW",
        )

    except PermissionError as exc:
        show(
            "integration_copy_to_protected_with_auth",
            "BLOCKED",
        )
        show(
            "integration_copy_to_protected_message",
            exc,
        )

    # =========================================================
    # V9.15.26 SECURITY HARDENING REVIEW
    # =========================================================

    print()
    print("=== V9.15.26 SECURITY HARDENING REVIEW ===")

    # 1. Invalid operation cannot pass.
    try:
        fs.validate_operation(
            "FORMAT_DRIVE",
            source,
        )
        show(
            "hardening_invalid_operation",
            "UNEXPECTED_ALLOW",
        )
    except ValueError:
        show(
            "hardening_invalid_operation",
            "BLOCKED",
        )

    # 2. Missing source cannot pass.
    try:
        fs.validate_operation(
            "READ",
            nonexistent_source,
        )
        show(
            "hardening_missing_source",
            "UNEXPECTED_ALLOW",
        )
    except FileNotFoundError:
        show(
            "hardening_missing_source",
            "BLOCKED",
        )

    # 3. COPY requires destination.
    try:
        fs.validate_operation(
            "COPY",
            source,
        )
        show(
            "hardening_copy_without_destination",
            "UNEXPECTED_ALLOW",
        )
    except ValueError:
        show(
            "hardening_copy_without_destination",
            "BLOCKED",
        )

    # 4. READ cannot receive destination.
    try:
        fs.validate_operation(
            "READ",
            source,
            destination=ordinary_destination,
        )
        show(
            "hardening_read_with_destination",
            "UNEXPECTED_ALLOW",
        )
    except ValueError:
        show(
            "hardening_read_with_destination",
            "BLOCKED",
        )

    # 5. Protected source cannot be overridden by authorization.
    authorization_manager.authorize(
        "FILE.MODIFY"
    )

    try:
        fs.evaluate_security(
            "MODIFY",
            protected_file,
            security_controller=controller,
        )
        show(
            "hardening_protected_source_override",
            "UNEXPECTED_ALLOW",
        )
    except PermissionError:
        show(
            "hardening_protected_source_override",
            "BLOCKED",
        )

    # 6. Protected destination cannot be overridden.
    authorization_manager.authorize(
        "FILE.CREATE"
    )

    try:
        fs.evaluate_security(
            "COPY",
            source,
            destination=protected_destination,
            security_controller=controller,
        )
        show(
            "hardening_protected_destination_override",
            "UNEXPECTED_ALLOW",
        )
    except PermissionError:
        show(
            "hardening_protected_destination_override",
            "BLOCKED",
        )

    # 7. Authorization is one-shot.
    authorization_manager.authorize(
        "FILE.CREATE"
    )

    first_authorized = fs.evaluate_security(
        "COPY",
        source,
        destination=critical_destination,
        security_controller=controller,
    )

    second_authorized = fs.evaluate_security(
        "COPY",
        source,
        destination=critical_destination,
        security_controller=controller,
    )

    show(
        "hardening_first_authorized_operation",
        first_authorized.value,
    )

    show(
        "hardening_authorization_reuse",
        second_authorized.value,
    )

    # 8. Effective-risk calculation.
    effective_risk = fs.get_effective_risk_level(
        "COPY",
        source,
        destination=critical_destination,
    )

    show(
        "hardening_effective_copy_risk",
        effective_risk.value,
    )

    # ---------------------------------------------------------
    # Audit existence
    # ---------------------------------------------------------

    print()
    print("=== FINAL INTEGRITY CHECK ===")

    show(
        "audit_file_exists",
        audit_path.exists(),
    )

    audit_lines = []

    if audit_path.exists():
        audit_lines = [
            line
            for line in audit_path.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        ]

    show(
        "audit_record_count",
        len(audit_lines),
    )

    # No filesystem mutation should have happened.
    show(
        "source_exists",
        source.exists(),
    )

    show(
        "source_content",
        source.read_text(
            encoding="utf-8"
        ),
    )

    show(
        "second_source_exists",
        second_source.exists(),
    )

    show(
        "ordinary_destination_exists",
        ordinary_destination.exists(),
    )

    show(
        "critical_destination_exists",
        critical_destination.exists(),
    )

    show(
        "protected_destination_exists",
        protected_destination.exists(),
    )

    print()
    print(
        "V9.15.25 + V9.15.26 combined test complete"
    )
