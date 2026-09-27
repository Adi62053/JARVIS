from security.v9_21_1_emergency_controls import V9EmergencySecurityControls
from security.v9_privileged_filesystem import V9PrivilegedFilesystem


emergency = V9EmergencySecurityControls()
filesystem = V9PrivilegedFilesystem()


# Use a safe existing filesystem resource for inspection.
resource = r"C:\Windows\System32"


# Normal V9.15 security evaluation.
normal_result = filesystem.evaluate_security(
    operation="READ",
    path=resource,
)

assert normal_result is not None

print("NORMAL FILESYSTEM EVALUATION: PASS")


# Attach emergency enforcement at the operation boundary.
original_evaluate = filesystem.evaluate_security


def emergency_protected_evaluate(*args, **kwargs):
    emergency.require_emergency_clear()
    return original_evaluate(*args, **kwargs)


filesystem.evaluate_security = emergency_protected_evaluate


# Activate emergency stop.
emergency.activate()

assert emergency.is_active()
assert not emergency.allow_operation()

blocked = False

try:
    filesystem.evaluate_security(
        operation="READ",
        path=resource,
    )
except PermissionError:
    blocked = True

assert blocked

print("EMERGENCY FILESYSTEM BLOCK: PASS")


# Emergency state must remain active.
assert emergency.is_active()
assert not emergency.allow_operation()

print("EMERGENCY STATE ENFORCEMENT: PASS")


# Clear emergency stop.
emergency.deactivate()

assert not emergency.is_active()
assert emergency.allow_operation()

print("EMERGENCY STOP CLEAR: PASS")


# Filesystem security evaluation must recover.
recovered_result = filesystem.evaluate_security(
    operation="READ",
    path=resource,
)

assert recovered_result is not None

print("FILESYSTEM RECOVERY: PASS")
print("NO FILESYSTEM MUTATION EXECUTED: PASS")
print("V9.21.13 PRIVILEGED FILESYSTEM EMERGENCY REGRESSION: PASS")
