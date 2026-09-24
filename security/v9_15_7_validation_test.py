from security.v9_privileged_filesystem import V9PrivilegedFilesystem

fs = V9PrivilegedFilesystem()

source = r"C:\Windows\notepad.exe"
protected_destination = r"C:\Windows\System32\jarvis_test.exe"
ordinary_destination = r"C:\Users\AdiNew\Desktop\jarvis_test.exe"

for name, operation, destination in [
    ("COPY_PROTECTED_DEST", "COPY", protected_destination),
    ("MOVE_PROTECTED_DEST", "MOVE", protected_destination),
    ("RENAME_PROTECTED_DEST", "RENAME", protected_destination),
]:
    try:
        fs.validate_operation(
            operation,
            source,
            destination,
        )
        print(name + ": UNEXPECTED_ALLOW")
    except PermissionError as exc:
        print(name + ": BLOCKED")
        print("  message:", exc)

try:
    info = fs.validate_operation(
        "COPY",
        source,
        ordinary_destination,
    )
    print("COPY_ORDINARY_DEST: VALIDATED")
    print("  source:", info.path)
    print("  protection:", info.protection_level)
except Exception as exc:
    print("COPY_ORDINARY_DEST: UNEXPECTED_ERROR")
    print("  error:", exc)

print("V9.15.7 validation test complete")
