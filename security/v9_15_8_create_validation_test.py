from security.v9_privileged_filesystem import V9PrivilegedFilesystem

fs = V9PrivilegedFilesystem()

protected_target = r"C:\Windows\System32\jarvis_v9158_test.txt"
critical_target = r"C:\Windows\jarvis_v9158_test.txt"
ordinary_target = r"C:\Users\AdiNew\Desktop\jarvis_v9158_test.txt"

for name, target in [
    ("CREATE_PROTECTED_TARGET", protected_target),
    ("CREATE_CRITICAL_TARGET", critical_target),
]:
    try:
        fs.validate_operation(
            "CREATE",
            target,
        )
        print(name + ": UNEXPECTED_ALLOW")
    except PermissionError as exc:
        print(name + ": BLOCKED")
        print("  message:", exc)

try:
    info = fs.validate_operation(
        "CREATE",
        ordinary_target,
    )
    print("CREATE_ORDINARY_TARGET: VALIDATED")
    print("  target:", info.path)
    print("  exists:", info.exists)
    print("  protection:", info.protection_level)
except Exception as exc:
    print("CREATE_ORDINARY_TARGET: UNEXPECTED_ERROR")
    print("  error:", exc)

print("V9.15.8 CREATE-target validation complete")
