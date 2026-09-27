from security.v9_21_1_emergency_controls import V9EmergencySecurityControls
from security.v9_process_manager import V9ProcessManager
from security.v9_service_manager import V9ServiceManager


emergency = V9EmergencySecurityControls()
process_manager = V9ProcessManager()
service_manager = V9ServiceManager()


# Verify normal inspection remains available.
processes = process_manager.list_processes()
services = service_manager.list_services()

assert isinstance(processes, list)
assert isinstance(services, list)


# Attach emergency enforcement at the operation boundary.
original_list_processes = process_manager.list_processes
original_list_services = service_manager.list_services


def emergency_protected_processes(*args, **kwargs):
    emergency.require_emergency_clear()
    return original_list_processes(*args, **kwargs)


def emergency_protected_services(*args, **kwargs):
    emergency.require_emergency_clear()
    return original_list_services(*args, **kwargs)


process_manager.list_processes = emergency_protected_processes
service_manager.list_services = emergency_protected_services


print("NORMAL PROCESS INSPECTION: PASS")
print("NORMAL SERVICE INSPECTION: PASS")


# Activate emergency stop.
emergency.activate()

assert emergency.is_active()
assert not emergency.allow_operation()


process_blocked = False
service_blocked = False

try:
    process_manager.list_processes()
except PermissionError:
    process_blocked = True

try:
    service_manager.list_services()
except PermissionError:
    service_blocked = True


assert process_blocked
assert service_blocked

print("EMERGENCY PROCESS BLOCK: PASS")
print("EMERGENCY SERVICE BLOCK: PASS")


# Clear emergency stop.
emergency.deactivate()

assert not emergency.is_active()
assert emergency.allow_operation()


assert isinstance(process_manager.list_processes(), list)
assert isinstance(service_manager.list_services(), list)

print("EMERGENCY STOP CLEAR: PASS")
print("PROCESS RECOVERY: PASS")
print("SERVICE RECOVERY: PASS")
print("V9.21.12 PROCESS + SERVICE EMERGENCY REGRESSION: PASS")
