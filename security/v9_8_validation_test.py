import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from security.v9_capability_model import (
    SecurityCapability,
    SecurityOperation,
    SecurityResource,
    SecurityCapabilityRequest,
)


def check_rejected(name, function):
    try:
        function()
    except (TypeError, ValueError):
        print(f"{name}: PASS")
        return

    print(f"{name}: FAIL")


check_rejected(
    "empty_resource",
    lambda: SecurityResource(
        SecurityCapability.FILE,
        SecurityOperation.READ,
        "",
    ),
)

check_rejected(
    "bad_capability",
    lambda: SecurityResource(
        "FILE",
        SecurityOperation.READ,
        r"C:\Test\file.txt",
    ),
)

check_rejected(
    "bad_operation",
    lambda: SecurityResource(
        SecurityCapability.FILE,
        "DELETE",
        r"C:\Test\file.txt",
    ),
)

check_rejected(
    "empty_operation_id",
    lambda: SecurityCapabilityRequest(
        "",
        SecurityResource(
            SecurityCapability.FILE,
            SecurityOperation.READ,
            r"C:\Test\file.txt",
        ),
    ),
)

print("V9.8 validation test complete")
