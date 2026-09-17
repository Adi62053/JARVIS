"""
JARVIS V8 - Automation Failure Handler

Captures execution failures and converts them into
AutomationFailure objects.

This module does not execute actions or change
automation execution behavior.
"""

from automation.automation_failure import AutomationFailure


class AutomationFailureHandler:
    """Creates structured failure records."""

    @staticmethod
    def capture(
        automation_name: str,
        action: str,
        error: Exception,
        step_number: int | None = None,
        parameters: dict | None = None,
    ) -> AutomationFailure:
        """Capture an exception as an AutomationFailure."""
        if not isinstance(error, Exception):
            raise TypeError("error must be an Exception")

        message = str(error).strip()

        if not message:
            message = error.__class__.__name__

        return AutomationFailure(
            automation_name=automation_name,
            action=action,
            message=message,
            step_number=step_number,
            parameters=parameters,
        )
