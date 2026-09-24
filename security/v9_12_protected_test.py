import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from security.v9_process_manager import V9ProcessManager


manager = V9ProcessManager()

protected = manager.find_processes("lsass.exe")

print("lsass_found:", len(protected) > 0)

if not protected:
    raise RuntimeError(
        "lsass.exe was not found for protection validation"
    )

process = protected[0]

print("lsass_pid:", process.pid)
print("lsass_protection:", process.protection_level.value)

try:
    manager.terminate_process(
        process.pid,
        force=True,
    )
except PermissionError as exc:
    print("protected_termination:", "BLOCKED")
    print("protection_message:", str(exc))
else:
    raise RuntimeError(
        "Protected process termination was not blocked"
    )

print("V9.12 protected process validation complete")
