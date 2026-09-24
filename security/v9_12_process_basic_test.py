import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from security.v9_process_manager import V9ProcessManager
from security.v9_protection_manager import ProtectionLevel


manager = V9ProcessManager()

process = manager.start_process(
    "cmd.exe",
    "/c",
    "timeout",
    "/t",
    "10",
    "/nobreak",
)

print("started_process_pid:", process)

time.sleep(2)

found = manager.get_process(process)

print("process_found:", found is not None)

if found is None:
    raise RuntimeError(
        "Started cmd.exe could not be found"
    )

print("process_name:", found.name)
print("process_protection:", found.protection_level.value)

if found.protection_level != ProtectionLevel.ORDINARY:
    raise RuntimeError(
        "cmd.exe should be classified as ORDINARY"
    )

terminated = manager.terminate_process(process)

print("process_terminated:", terminated)

time.sleep(1)

after = manager.get_process(process)

print("process_after_termination:", after)

print("V9.12 process start/find/terminate test complete")
