from automation.automation_model import Automation, AutomationStep
from automation.automation_executor import AutomationExecutor
from automation.automation_confirmation import AutomationConfirmation

confirmation = AutomationConfirmation()

executor = AutomationExecutor(
    dry_run=True,
    confirmation=confirmation,
)

automation = Automation("Security Test")
automation.add_step(
    AutomationStep(
        "WAIT",
        {"seconds": 0},
        "DANGEROUS",
    )
)

blocked = False

try:
    executor.execute(automation)
except RuntimeError as exc:
    blocked = "Confirmation required" in str(exc)

if blocked:
    print("[PASS] Dangerous step blocked without confirmation.")
else:
    print("[FAIL] Dangerous step was not blocked.")

confirmation.confirm("Security Test", 1)

results = executor.execute(automation)

if results and "[CONFIRMED]" in results[0]:
    print("[PASS] Confirmed dangerous step executed in dry-run.")
else:
    print("[FAIL] Confirmation integration failed.")
