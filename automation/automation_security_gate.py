"""
JARVIS V8 - Automation Security Gate

Centralizes security checks for automation execution.

This module does not execute actions.
It only determines whether a step is allowed to proceed.
"""

from automation.automation_confirmation import AutomationConfirmation
from automation.automation_model import AutomationStep
from automation.automation_security import requires_confirmation


class AutomationSecurityGate:
    """Apply automation security and confirmation rules."""

    def __init__(
        self,
        confirmation: AutomationConfirmation | None = None,
    ) -> None:
        self.confirmation = confirmation or AutomationConfirmation()

    def check(
        self,
        automation_name: str,
        step_number: int,
        step: AutomationStep,
    ) -> str:
        """
        Check whether an automation step is authorized.

        Returns a security note when execution is allowed.
        Raises RuntimeError when explicit confirmation is required
        but has not been provided.
        """
        if not isinstance(step, AutomationStep):
            raise TypeError("step must be an AutomationStep")

        if not isinstance(step_number, int) or step_number < 1:
            raise ValueError(
                "step_number must be an integer greater than zero"
            )

        if requires_confirmation(step.security_level):
            if not self.confirmation.consume(
                automation_name,
                step_number,
            ):
                raise RuntimeError(
                    f"Confirmation required for dangerous step "
                    f"{step_number}: {step.action}"
                )

            return " [CONFIRMED]"

        return ""
