import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from security.v9_process_manager import V9ProcessManager
from security.v9_protection_manager import ProtectionLevel


manager = V9ProcessManager()

processes = manager.list_processes()

print("process_count:", len(processes))

print(
    "process_list_available:",
    len(processes) > 0,
)

protected = [
    process
    for process in processes
    if process.protection_level == ProtectionLevel.PROTECTED
]

print(
    "protected_process_count:",
    len(protected),
)

notepad_pid = manager.start_process(
    "notepad.exe"
)

print("started_notepad_pid:", notepad_pid)

time.sleep(2)

notepad = manager.get_process(notepad_pid)

print(
    "notepad_found:",
    notepad is not None,
)

if notepad is None:
    raise RuntimeError(
        "Started Notepad could not be found"
    )

print(
    "notepad_protection:",
    notepad.protection_level.value,
)

if notepad.protection_level != ProtectionLevel.ORDINARY:
    raise RuntimeError(
        "Notepad should be classified as ORDINARY"
    )

found = manager.find_processes("notepad.exe")

print(
    "find_notepad_count:",
    len(found),
)

terminated = manager.terminate_process(
    notepad_pid
)

print(
    "notepad_terminated:",
    terminated,
)

time.sleep(1)

after = manager.get_process(notepad_pid)

print(
    "notepad_after_termination:",
    after,
)

lsass = manager.find_processes("lsass.exe")

print(
    "lsass_found:",
    len(lsass) > 0,
)

if lsass:
    print(
        "lsass_protection:",
        lsass[0].protection_level.value,
    )

    try:
        manager.terminate_process(
            lsass[0].pid
        )
    except PermissionError:
        print(
            "protected_process_termination:",
            "BLOCKED",
        )
    else:
        raise RuntimeError(
            "Protected process termination was not blocked"
        )

print("V9.12 process management test complete")
