from threading import Lock


class V9EmergencySecurityControls:
    def __init__(self):
        self._lock = Lock()
        self._emergency_stop = False

    def activate(self):
        with self._lock:
            self._emergency_stop = True

    def deactivate(self):
        with self._lock:
            self._emergency_stop = False

    def is_active(self):
        with self._lock:
            return self._emergency_stop

    def allow_operation(self):
        return not self.is_active()

    def require_emergency_clear(self):
        if self.is_active():
            raise PermissionError("Emergency security stop is active")


controls = V9EmergencySecurityControls()
controls.activate()
assert controls.is_active()
assert not controls.allow_operation()

try:
    controls.require_emergency_clear()
except PermissionError:
    pass
else:
    raise AssertionError("Emergency stop failed")

controls.deactivate()
assert not controls.is_active()
assert controls.allow_operation()

print("EMERGENCY STOP ACTIVATION: PASS")
print("OPERATION BLOCK: PASS")
print("EMERGENCY STOP ENFORCEMENT: PASS")
print("EMERGENCY STOP CLEAR: PASS")
print("V9.21.1 EMERGENCY SECURITY CONTROLS: PASS")
