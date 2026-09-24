import json
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
        "V9.15.22 audit test",
        encoding="utf-8",
    )

    critical_file = Path(
        r"C:\Windows\notepad.exe"
    )

    protected_file = Path(
        r"C:\Windows\System32\notepad.exe"
    )

    protected_destination = Path(
        r"C:\Windows\System32\JARVIS_V91522_TEST.txt"
    )

    ordinary_destination = root / "ordinary_destination.txt"

    audit_path = Path(temp_dir) / "v9_15_22_audit.jsonl"

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

    # ---------------------------------------------------------
    # 1. ALLOW
    # ---------------------------------------------------------

    allow_result = fs.evaluate_security(
        "READ",
        ordinary_file,
        security_controller=controller,
    )

    print(
        "allow_decision:",
        allow_result.value,
    )

    # ---------------------------------------------------------
    # 2. REQUIRE_AUTHORIZATION
    # ---------------------------------------------------------

    auth_required_result = fs.evaluate_security(
        "DELETE",
        ordinary_file,
        security_controller=controller,
    )

    print(
        "authorization_required_decision:",
        auth_required_result.value,
    )

    # ---------------------------------------------------------
    # 3. REQUIRE_ELEVATION
    # ---------------------------------------------------------

    elevation_result = fs.evaluate_security(
        "READ",
        protected_file,
        security_controller=controller,
    )

    print(
        "elevation_required_decision:",
        elevation_result.value,
    )

    # ---------------------------------------------------------
    # 4. HARD BLOCK
    #
    # This should be blocked before the controller evaluates
    # the request, so we verify that explicitly.
    # ---------------------------------------------------------

    try:
        fs.evaluate_security(
            "COPY",
            ordinary_file,
            destination=protected_destination,
            security_controller=controller,
        )

        print(
            "protected_destination_result:",
            "UNEXPECTED_ALLOW",
        )

    except PermissionError as exc:
        print(
            "protected_destination_result:",
            "BLOCKED",
        )

        print(
            "protected_destination_message:",
            exc,
        )

    # ---------------------------------------------------------
    # 5. CRITICAL destination requiring authorization.
    # ---------------------------------------------------------

    critical_destination = Path(
        r"C:\Program Files\JARVIS_V91522_TEST.txt"
    )

    critical_result = fs.evaluate_security(
        "COPY",
        ordinary_file,
        destination=critical_destination,
        security_controller=controller,
    )

    print(
        "critical_destination_decision:",
        critical_result.value,
    )

    # ---------------------------------------------------------
    # 6. Read and inspect the audit JSONL.
    # ---------------------------------------------------------

    print(
        "audit_file_exists:",
        audit_path.exists(),
    )

    audit_lines = []

    if audit_path.exists():
        audit_lines = [
            line.strip()
            for line in audit_path.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        ]

    print(
        "audit_record_count:",
        len(audit_lines),
    )

    for index, line in enumerate(audit_lines, start=1):
        record = json.loads(line)

        print(
            f"audit_{index}_operation_id:",
            record.get("operation_id"),
        )

        print(
            f"audit_{index}_capability:",
            record.get("capability"),
        )

        print(
            f"audit_{index}_resource:",
            record.get("resource"),
        )

        print(
            f"audit_{index}_risk_level:",
            record.get("risk_level"),
        )

        print(
            f"audit_{index}_required_privilege:",
            record.get("required_privilege"),
        )

        print(
            f"audit_{index}_current_privilege:",
            record.get("current_privilege"),
        )

        print(
            f"audit_{index}_authorization_state:",
            record.get("authorization_state"),
        )

        print(
            f"audit_{index}_decision:",
            record.get("decision"),
        )

        print(
            f"audit_{index}_result:",
            record.get("result"),
        )

        print(
            f"audit_{index}_has_timestamp:",
            bool(record.get("timestamp")),
        )

    # ---------------------------------------------------------
    # 7. Basic audit integrity checks.
    # ---------------------------------------------------------

    required_fields = {
        "timestamp",
        "operation_id",
        "capability",
        "resource",
        "risk_level",
        "required_privilege",
        "current_privilege",
        "authorization_state",
        "decision",
        "result",
    }

    all_required_fields_present = True
    all_records_valid_json = True

    for line in audit_lines:
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            all_records_valid_json = False
            continue

        if not required_fields.issubset(record.keys()):
            all_required_fields_present = False

    print(
        "all_records_valid_json:",
        all_records_valid_json,
    )

    print(
        "all_required_fields_present:",
        all_required_fields_present,
    )

    # ---------------------------------------------------------
    # 8. Verify protected-destination hard block does not create
    #    a normal controller audit record.
    # ---------------------------------------------------------

    protected_block_audit_present = any(
        "JARVIS_V91522_TEST.txt" in line
        for line in audit_lines
    )

    print(
        "protected_destination_audit_record_present:",
        protected_block_audit_present,
    )

    # ---------------------------------------------------------
    # 9. Confirm no filesystem mutation.
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
        "ordinary_destination_exists:",
        ordinary_destination.exists(),
    )

    print(
        "critical_destination_exists:",
        critical_destination.exists(),
    )

    print(
        "protected_destination_exists:",
        protected_destination.exists(),
    )

    print(
        "V9.15.22 audit-integrity test complete"
    )
