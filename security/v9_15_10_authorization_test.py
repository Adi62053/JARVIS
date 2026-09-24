from pathlib import Path
from tempfile import TemporaryDirectory

from security.v9_audit_logger import V9AuditLogger
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_permission_manager import V9PermissionManager
from security.v9_privileged_filesystem import V9PrivilegedFilesystem
from security.v9_security_controller import V9SecurityController
from security.v9_security_model import SecurityDecision


with TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    source = temp_path / "source.txt"

    source.write_text(
        "V9.15.10 authorization test",
        encoding="utf-8",
    )

    permission_manager = V9PermissionManager()
    authorization_manager = V9AuthorizationManager()

    permission_manager.set_permission(
        "FILE",
        True,
    )

    with TemporaryDirectory() as audit_dir:
        audit_logger = V9AuditLogger(
            log_path=str(
                Path(audit_dir) / "v9_15_10_audit.jsonl"
            )
        )

        controller = V9SecurityController(
            permission_manager=permission_manager,
            authorization_manager=authorization_manager,
            audit_logger=audit_logger,
        )

        fs = V9PrivilegedFilesystem()

        operation_id = "FILE.DELETE"

        first_decision = fs.evaluate_security(
            "DELETE",
            source,
            security_controller=controller,
        )

        print("without_authorization:", first_decision)

        if first_decision != SecurityDecision.REQUIRE_AUTHORIZATION:
            print("authorization_gate: FAIL")
        else:
            print("authorization_gate: PASS")

        authorization_manager.authorize(operation_id)

        authorized_decision = fs.evaluate_security(
            "DELETE",
            source,
            security_controller=controller,
        )

        print("with_authorization:", authorized_decision)

        if authorized_decision == SecurityDecision.ALLOW:
            print("authorized_operation: PASS")
        else:
            print("authorized_operation: FAIL")

        consumed_decision = fs.evaluate_security(
            "DELETE",
            source,
            security_controller=controller,
        )

        print("after_authorization_consumed:", consumed_decision)

        if consumed_decision == SecurityDecision.REQUIRE_AUTHORIZATION:
            print("authorization_consumption: PASS")
        else:
            print("authorization_consumption: FAIL")

        print("filesystem_target_still_exists:", source.exists())
        print("V9.15.10 authorization consumption test complete")
