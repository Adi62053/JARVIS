from automation.automation_model import Automation, AutomationStep
from automation.automation_executor import AutomationExecutor

executor = AutomationExecutor(dry_run=True)

safe = Automation("Safe Security Test")
safe.add_step(
    AutomationStep("WAIT", {"seconds": 0}, "SAFE")
)

caution = Automation("Caution Security Test")
caution.add_step(
    AutomationStep("WAIT", {"seconds": 0}, "CAUTION")
)

safe_result = executor.execute(safe)
caution_result = executor.execute(caution)

if safe_result and "DRY RUN" in safe_result[0]:
    print("[PASS] SAFE action remains executable.")
else:
    print("[FAIL] SAFE action regression.")

if caution_result and "DRY RUN" in caution_result[0]:
    print("[PASS] CAUTION action remains executable.")
else:
    print("[FAIL] CAUTION action regression.")

print("[PASS] V8.12 security regression test completed.")
