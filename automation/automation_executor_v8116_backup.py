"""
JARVIS V8 - Automation Executor

Controlled execution layer for V8 automations.

Current stage:
- Validates automation steps.
- Checks security levels.
- Requires explicit confirmation for dangerous steps.
- Supports dry-run execution.
- Executes only explicitly integrated actions.
- Resolves each action to the appropriate JARVIS subsystem.
"""

from automation.automation_confirmation import AutomationConfirmation
from automation.automation_dispatcher import AutomationDispatcher
from automation.automation_model import Automation
from automation.automation_security import requires_confirmation


class AutomationExecutor:
    """Safely process automation steps."""

    def __init__(
        self,
        dry_run: bool = True,
        dispatcher: AutomationDispatcher | None = None,
        confirmation: AutomationConfirmation | None = None,
    ) -> None:
        self.dry_run = dry_run
        self.dispatcher = dispatcher or AutomationDispatcher()
        self.confirmation = confirmation or AutomationConfirmation()

    def execute(self, automation: Automation) -> list[str]:
        """
        Process an automation.

        Dangerous steps require explicit confirmation.
        Integrated actions may execute only when dry_run is False.
        """
        if not automation.enabled:
            raise RuntimeError(
                f"Automation is disabled: {automation.name}"
            )

        results = []

        for index, step in enumerate(automation.steps, start=1):
            subsystem = self.dispatcher.resolve(step.action)

            if subsystem is None:
                raise RuntimeError(
                    f"Unsupported automation action: {step.action}"
                )

            security_note = ""

            if requires_confirmation(step.security_level):
                if not self.confirmation.consume(
                    automation.name,
                    index,
                ):
                    raise RuntimeError(
                        f"Confirmation required for dangerous step "
                        f"{index}: {step.action}"
                    )

                security_note = " [CONFIRMED]"

            message = (
                f"Step {index}: {step.action} "
                f"{step.parameters} -> {subsystem}"
                f" | SECURITY={step.security_level}"
                f"{security_note}"
            )

            if self.dry_run:
                results.append(f"DRY RUN - {message}")
                continue

            handler = self.dispatcher.get_handler(step.action)

            if handler is None:
                raise RuntimeError(
                    f"Real execution is not yet integrated for: "
                    f"{step.action}"
                )

            try:
                execution_result = handler.execute(
                    step.parameters
                )
            except Exception as exc:
                raise RuntimeError(
                    f"Execution failed for step {index} "
                    f"({step.action}): {exc}"
                ) from exc

            results.append(
                f"EXECUTED - {message} -> {execution_result}"
            )

        return results
