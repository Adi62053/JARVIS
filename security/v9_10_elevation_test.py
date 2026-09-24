import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from security.v9_elevation import V9ElevationManager
from security.v9_security_model import SecurityPrivilegeLevel


manager = V9ElevationManager()

current = manager.get_current_privilege()

print("current_privilege:", current.value)

print(
    "user_access:",
    manager.can_access(SecurityPrivilegeLevel.USER),
)

print(
    "administrator_access:",
    manager.can_access(
        SecurityPrivilegeLevel.ADMINISTRATOR
    ),
)

print(
    "system_access:",
    manager.can_access(
        SecurityPrivilegeLevel.SYSTEM
    ),
)

status = manager.get_status(
    SecurityPrivilegeLevel.ADMINISTRATOR
)

print("administrator_status:", status)

print("V9.10 detection test complete")
