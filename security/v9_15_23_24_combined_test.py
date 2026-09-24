from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_privileged_filesystem import V9PrivilegedFilesystem
from security.v9_security_controller import V9SecurityController
from security.v9_permission_manager import V9PermissionManager
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_audit_logger import V9AuditLogger


with TemporaryDirectory() as temp_dir:
    root = Path(temp_dir)

    source = root / "source.txt"
    source.write_text(
        "V9.15.23-24 regression test",
        encoding="utf-8",
    )

    second_source = root / "second.txt"
    second_source.write_text(
        "second test file",
        encoding="utf-8",
    )

    ordinary_destination = root / "destination.txt"

    nonexistent_source = root / "does_not_exist.txt"

    protected_file = Path(
        r"C:\Windows\System32\notepad.exe"
    )

    protected_destination = Path(
        r"C:\Windows\System32\JARVIS_V91523_TEST.txt"
    )

    critical_destination = Path(
        r"C:\Program Files\JARVIS_V91523_TEST.txt"
    )

    # ---------------------------------------------------------
    # Security controller
    # ---------------------------------------------------------

    permission_manager = V9PermissionManager()
    authorization_manager = V9AuthorizationManager()

    permission_manager.set_permission(
        "FILE",
        True,
    )

    audit_logger = V9AuditLogger(
        log_path=str(
            root / "audit.jsonl"
        )
    )

    controller = V9SecurityController(
        permission_manager=permission_manager,
        authorization_manager=authorization_manager,
        audit_logger=audit_logger,
    )

    fs = V9PrivilegedFilesystem()

    # =========================================================
    # V9.15.23 — ERROR / EDGE CASE VALIDATION
    # =========================================================

    print("=== V9.15.23 ERROR / EDGE CASES ===")

    # 1. Invalid operation
    try:
        fs.validate_operation(
            "INVALID_OPERATION",
            source,
        )
        print(
            "invalid_operation: UNEXPECTED_ALLOW"
        )
    except ValueError as exc:
        print(
            "invalid_operation: REJECTED"
        )
        print(
            "invalid_operation_message:",
            exc,
        )

    # 2. Empty operation
    try:
        fs.validate_operation(
            "",
            source,
        )
        print(
            "empty_operation: UNEXPECTED_ALLOW"
        )
    except ValueError as exc:
        print(
            "empty_operation: REJECTED"
        )
        print(
            "empty_operation_message:",
            exc,
        )

    # 3. Missing source
    try:
        fs.validate_operation(
            "READ",
            nonexistent_source,
        )
        print(
            "missing_source: UNEXPECTED_ALLOW"
        )
    except FileNotFoundError as exc:
        print(
            "missing_source: REJECTED"
        )
        print(
            "missing_source_message:",
            exc,
        )

    # 4. COPY without destination
    try:
        fs.validate_operation(
            "COPY",
            source,
        )
        print(
            "copy_without_destination: UNEXPECTED_ALLOW"
        )
    except ValueError as exc:
        print(
            "copy_without_destination: REJECTED"
        )
        print(
            "copy_without_destination_message:",
            exc,
        )

    # 5. MOVE without destination
    try:
        fs.validate_operation(
            "MOVE",
            source,
        )
        print(
            "move_without_destination: UNEXPECTED_ALLOW"
        )
    except ValueError as exc:
        print(
            "move_without_destination: REJECTED"
        )
        print(
            "move_without_destination_message:",
            exc,
        )

    # 6. RENAME without destination
    try:
        fs.validate_operation(
            "RENAME",
            source,
        )
        print(
            "rename_without_destination: UNEXPECTED_ALLOW"
        )
    except ValueError as exc:
        print(
            "rename_without_destination: REJECTED"
        )
        print(
            "rename_without_destination_message:",
            exc,
        )

    # 7. Destination supplied to READ
    try:
        fs.validate_operation(
            "READ",
            source,
            destination=ordinary_destination,
        )
        print(
            "read_with_destination: UNEXPECTED_ALLOW"
        )
    except ValueError as exc:
        print(
            "read_with_destination: REJECTED"
        )
        print(
            "read_with_destination_message:",
            exc,
        )

    # 8. CREATE on nonexistent target should validate
    create_target = root / "create_target.txt"

    try:
        create_info = fs.validate_operation(
            "CREATE",
            create_target,
        )

        print(
            "create_nonexistent_target:",
            "VALIDATED",
        )

        print(
            "create_target_exists:",
            create_info.exists,
        )

    except Exception as exc:
        print(
            "create_nonexistent_target: UNEXPECTED_FAILURE"
        )
        print(
            "create_nonexistent_target_message:",
            exc,
        )

    # 9. Protected source mutation
    try:
        fs.validate_operation(
            "DELETE",
            protected_file,
        )
        print(
            "protected_source_mutation: UNEXPECTED_ALLOW"
        )
    except PermissionError as exc:
        print(
            "protected_source_mutation: BLOCKED"
        )
        print(
            "protected_source_mutation_message:",
            exc,
        )

    # 10. Protected destination
    try:
        fs.validate_operation(
            "COPY",
            source,
            destination=protected_destination,
        )
        print(
            "protected_destination: UNEXPECTED_ALLOW"
        )
    except PermissionError as exc:
        print(
            "protected_destination: BLOCKED"
        )
        print(
            "protected_destination_message:",
            exc,
        )

    # =========================================================
    # V9.15.24 — SECURITY REGRESSION MATRIX
    # =========================================================

    print()
    print("=== V9.15.24 SECURITY REGRESSION MATRIX ===")

    # READ
    read_result = fs.evaluate_security(
        "READ",
        source,
        security_controller=controller,
    )

    print(
        "READ_ordinary:",
        read_result.value,
    )

    # WRITE
    write_result = fs.evaluate_security(
        "WRITE",
        source,
        security_controller=controller,
    )

    print(
        "WRITE_ordinary_without_auth:",
        write_result.value,
    )

    # MODIFY
    modify_result = fs.evaluate_security(
        "MODIFY",
        source,
        security_controller=controller,
    )

    print(
        "MODIFY_ordinary_without_auth:",
        modify_result.value,
    )

    # DELETE
    delete_result = fs.evaluate_security(
        "DELETE",
        source,
        security_controller=controller,
    )

    print(
        "DELETE_ordinary_without_auth:",
        delete_result.value,
    )

    # COPY ordinary -> ordinary
    copy_result = fs.evaluate_security(
        "COPY",
        source,
        destination=ordinary_destination,
        security_controller=controller,
    )

    print(
        "COPY_ordinary_to_ordinary:",
        copy_result.value,
    )

    # COPY ordinary -> critical
    critical_result = fs.evaluate_security(
        "COPY",
        source,
        destination=critical_destination,
        security_controller=controller,
    )

    print(
        "COPY_ordinary_to_critical_without_auth:",
        critical_result.value,
    )

    # Authorize FILE.CREATE for critical COPY
    authorization_manager.authorize(
        "FILE.CREATE"
    )

    critical_authorized_result = fs.evaluate_security(
        "COPY",
        source,
        destination=critical_destination,
        security_controller=controller,
    )

    print(
        "COPY_ordinary_to_critical_with_auth:",
        critical_authorized_result.value,
    )

    print(
        "FILE.CREATE_authorized_after_use:",
        authorization_manager.is_authorized(
            "FILE.CREATE"
        ),
    )

    # MOVE ordinary -> critical
    move_result = fs.evaluate_security(
        "MOVE",
        second_source,
        destination=critical_destination,
        security_controller=controller,
    )

    print(
        "MOVE_ordinary_to_critical_without_auth:",
        move_result.value,
    )

    # Authorize FILE.MODIFY
    authorization_manager.authorize(
        "FILE.MODIFY"
    )

    move_authorized_result = fs.evaluate_security(
        "MOVE",
        second_source,
        destination=critical_destination,
        security_controller=controller,
    )

    print(
        "MOVE_ordinary_to_critical_with_auth:",
        move_authorized_result.value,
    )

    print(
        "FILE.MODIFY_authorized_after_use:",
        authorization_manager.is_authorized(
            "FILE.MODIFY"
        ),
    )

    # RENAME ordinary -> critical
    rename_result = fs.evaluate_security(
        "RENAME",
        source,
        destination=critical_destination,
        security_controller=controller,
    )

    print(
        "RENAME_ordinary_to_critical_without_auth:",
        rename_result.value,
    )

    # Protected READ
    protected_read_result = fs.evaluate_security(
        "READ",
        protected_file,
        security_controller=controller,
    )

    print(
        "READ_protected:",
        protected_read_result.value,
    )

    # Protected DELETE with authorization attempt
    authorization_manager.authorize(
        "FILE.DELETE"
    )

    try:
        fs.evaluate_security(
            "DELETE",
            protected_file,
            security_controller=controller,
        )

        print(
            "DELETE_protected_with_auth:",
            "UNEXPECTED_ALLOW",
        )

    except PermissionError as exc:
        print(
            "DELETE_protected_with_auth:",
            "BLOCKED",
        )

        print(
            "DELETE_protected_message:",
            exc,
        )

    # Protected destination with authorization
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

        print(
            "COPY_to_protected_with_auth:",
            "UNEXPECTED_ALLOW",
        )

    except PermissionError as exc:
        print(
            "COPY_to_protected_with_auth:",
            "BLOCKED",
        )

        print(
            "COPY_to_protected_message:",
            exc,
        )

    # =========================================================
    # No mutation verification
    # =========================================================

    print()
    print("=== NO-MUTATION VERIFICATION ===")

    print(
        "source_exists:",
        source.exists(),
    )

    print(
        "source_content:",
        source.read_text(
            encoding="utf-8"
        ),
    )

    print(
        "second_source_exists:",
        second_source.exists(),
    )

    print(
        "ordinary_destination_exists:",
        ordinary_destination.exists(),
    )

    print(
        "create_target_exists:",
        create_target.exists(),
    )

    print(
        "critical_test_target_exists:",
        critical_destination.exists(),
    )

    print(
        "protected_test_target_exists:",
        protected_destination.exists(),
    )

    print()
    print(
        "V9.15.23 + V9.15.24 combined test complete"
    )
