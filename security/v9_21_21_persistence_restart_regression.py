from security.v9_21_1_emergency_controls import V9EmergencySecurityControls


# Fresh security-control instance must start in a safe, cleared state.
controls = V9EmergencySecurityControls()

assert controls.is_active() is False
assert controls.allow_operation() is True

print("FRESH INSTANCE STATE: PASS")

# Activate emergency stop.
controls.activate()

assert controls.is_active() is True
assert controls.allow_operation() is False

print("EMERGENCY STATE ACTIVATION: PASS")

# A new instance represents a fresh security-control state.
fresh_controls = V9EmergencySecurityControls()

assert fresh_controls.is_active() is False
assert fresh_controls.allow_operation() is True

print("FRESH INSTANCE CLEARS EMERGENCY STATE: PASS")

# Original instance must remain stopped.
assert controls.is_active() is True
assert controls.allow_operation() is False

print("ORIGINAL INSTANCE STATE ISOLATION: PASS")

# Clear original instance and verify recovery.
controls.deactivate()

assert controls.is_active() is False
assert controls.allow_operation() is True

print("ORIGINAL INSTANCE RECOVERY: PASS")

# New instance remains unaffected.
assert fresh_controls.is_active() is False
assert fresh_controls.allow_operation() is True

print("NEW INSTANCE STATE INTEGRITY: PASS")

print("NO PERSISTENT EMERGENCY STATE LEAK: PASS")
print("V9.21.21 EMERGENCY PERSISTENCE + RESTART REGRESSION: PASS")
