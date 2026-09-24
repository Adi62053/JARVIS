import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from security.v9_process_manager import V9ProcessManager


manager = V9ProcessManager()

process = manager.start_process(
    "cmd.exe",
    "/c",
    "timeout",
    "/t",
    "30",
    "/nobreak",
)

print("started_process_pid:", process)

time.sleep(2)

found = manager.get_process(process)

print(
    "process_found:",
    found is not None,
)

if found is None:
    raise RuntimeError(
        "Started cmd.exe could not be found"
    )

normal_result = manager.terminate_process(
    process,
    force=False,
)

print(
    "normal_termination_result:",
    normal_result,
)

still_running = manager.get_process(process)

print(
    "still_running_after_normal:",
    still_running is not None,
)

if still_running is None:
    raise RuntimeError(
        "Process unexpectedly disappeared during "
        "normal termination test"
    )

force_result = manager.terminate_process(
    process,
    force=True,
)

print(
    "force_termination_result:",
    force_result,
)

time.sleep(1)

after_force = manager.get_process(process)

print(
    "process_after_force:",
    after_force,
)

if after_force is not None:
    raise RuntimeError(
        "Process still exists after force termination"
    )

print("V9.12 termination test complete")
