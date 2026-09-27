from concurrent.futures import ThreadPoolExecutor

from security.v9_21_1_emergency_controls import V9EmergencySecurityControls


emergency = V9EmergencySecurityControls()


def activate_and_check():
    emergency.activate()
    return emergency.is_active()


def deactivate_and_check():
    emergency.deactivate()
    return not emergency.is_active()


# 1. Concurrent activation checks.
with ThreadPoolExecutor(max_workers=8) as executor:
    activation_results = list(
        executor.map(
            lambda _: activate_and_check(),
            range(32),
        )
    )

assert all(activation_results)
assert emergency.is_active()


# 2. Concurrent clear checks.
with ThreadPoolExecutor(max_workers=8) as executor:
    clear_results = list(
        executor.map(
            lambda _: deactivate_and_check(),
            range(32),
        )
    )

assert all(clear_results)
assert not emergency.is_active()


# 3. Final state must be safe and deterministic.
assert emergency.allow_operation()


# 4. Repeated concurrent state transitions.
def transition(_):
    emergency.activate()
    active = emergency.is_active()
    emergency.deactivate()
    cleared = not emergency.is_active()
    return active, cleared


with ThreadPoolExecutor(max_workers=8) as executor:
    transition_results = list(
        executor.map(
            transition,
            range(64),
        )
    )

assert all(active for active, cleared in transition_results)
assert all(cleared for active, cleared in transition_results)


print("CONCURRENT ACTIVATION: PASS")
print("CONCURRENT CLEAR: PASS")
print("THREAD-SAFE STATE ACCESS: PASS")
print("FINAL STATE CONSISTENCY: PASS")
print("CONCURRENT STATE TRANSITIONS: PASS")
print("V9.21.9 EMERGENCY CONCURRENCY REGRESSION: PASS")
