import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from security.v9_permission_policy import V9PermissionPolicy


policy = V9PermissionPolicy()

policy.set_policy(
    "FILE.DELETE",
    r"C:\Test\allowed.txt",
    True,
)

policy.set_policy(
    "FILE.DELETE",
    r"C:\Windows\protected.txt",
    False,
)

print(
    "allowed_resource:",
    policy.is_allowed(
        "FILE.DELETE",
        r"C:\Test\allowed.txt",
    ),
)

print(
    "protected_resource:",
    policy.is_allowed(
        "FILE.DELETE",
        r"C:\Windows\protected.txt",
    ),
)

print(
    "unconfigured_resource:",
    policy.is_allowed(
        "FILE.DELETE",
        r"C:\Test\unknown.txt",
    ),
)

print(
    "has_allowed_policy:",
    policy.has_policy(
        "FILE.DELETE",
        r"C:\Test\allowed.txt",
    ),
)

print(
    "remove_result:",
    policy.remove_policy(
        "FILE.DELETE",
        r"C:\Test\allowed.txt",
    ),
)

print(
    "after_remove:",
    policy.is_allowed(
        "FILE.DELETE",
        r"C:\Test\allowed.txt",
    ),
)
