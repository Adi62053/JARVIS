from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_audit_logger import V9AuditLogger
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_permission_manager import V9PermissionManager
from security.v9_privileged_filesystem import V9PrivilegedFilesystem
from security.v9_security_controller import V9SecurityController


with TemporaryDirectory() as audit_dir:
    permission_manager = V9PermissionManager()
    authorization_manager = V9AuthorizationManager()

    permission_manager.set_permission(
        "FILE",
        True,
    )

    audit_logger = V9AuditLogger(
        log_path=str(
            Path(audit_dir) / "v9_15_11_audit.jsonl"
        )
    )

    controller = V9SecurityController(
        permission_manager=permission_manager,
        authorization_manager=authorization_manager,
        audit_logger=audit_logger,
    )

    fs = V9PrivilegedFilesystem()

    # Existing protected Windows file.
    # Security evaluation only; this file will NOT be modified.
    protected_path = Path(
        r"C:\Windows\System32\notepad.exe"
    )

    operation_id = "FILE.DELETE"

    # Explicitly authorize the dangerous operation first.
    authorization_manager.authorize(operation_id)

    try:
        fs.evaluate_security(
            "DELETE",
            protected_path,
            security_controller=controller,
        )

        print("protected_with_authorization: UNEXPECTED_ALLOW")

    except PermissionError as exc:
        print("protected_with_authorization: BLOCKED")
        print("message:", exc)

    print(
        "authorization_still_configured:",
        authorization_manager.is_authorized(operation_id),
    )

    print("V9.15.11 protected-boundary test complete")
