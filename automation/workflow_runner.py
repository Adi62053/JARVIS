"""
JARVIS V8 - Workflow Runner

Runs automation steps in order through the V8 execution engine.

Current stage:
- Sequential workflow handling.
- Safe failure reporting.
- Uses the existing dry-run executor.
- Does not perform real computer actions.
"""

from automation.automation_executor import AutomationExecutor
from automation.automation_model import Automation


class WorkflowRunner:
    """Run a complete automation as an ordered workflow."""

    def __init__(
        self,
        executor: AutomationExecutor | None = None,
    ) -> None:
        self.executor = executor or AutomationExecutor()

    def run(self, automation: Automation) -> list[str]:
        """
        Run the automation through the execution engine.

        Returns the execution results.
        Stops immediately if execution fails.
        """
        if not automation.enabled:
            raise RuntimeError(
                f"Automation is disabled: {automation.name}"
            )

        if not automation.steps:
            return []

        try:
            return self.executor.execute(automation)
        except Exception as exc:
            raise RuntimeError(
                f"Workflow failed for '{automation.name}': {exc}"
            ) from exc
