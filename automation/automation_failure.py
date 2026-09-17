"""
JARVIS V8 - Automation Failure Handling

Defines the data model used to represent automation failures.

This module does not execute actions and does not change
existing automation behavior.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AutomationFailure:
    """Represents one failure during automation execution."""

    automation_name: str
    action: str
    message: str
    step_number: int | None = None
    parameters: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        """Validate failure information."""
        if not isinstance(self.automation_name, str):
            raise TypeError(
                "automation_name must be a string"
            )

        if not self.automation_name.strip():
            raise ValueError(
                "automation_name cannot be empty"
            )

        if not isinstance(self.action, str):
            raise TypeError(
                "action must be a string"
            )

        if not self.action.strip():
            raise ValueError(
                "action cannot be empty"
            )

        if not isinstance(self.message, str):
            raise TypeError(
                "message must be a string"
            )

        if not self.message.strip():
            raise ValueError(
                "message cannot be empty"
            )

        if self.step_number is not None:
            if not isinstance(self.step_number, int):
                raise TypeError(
                    "step_number must be an integer"
                )

            if self.step_number < 1:
                raise ValueError(
                    "step_number must be at least 1"
                )

        if self.parameters is not None:
            if not isinstance(self.parameters, dict):
                raise TypeError(
                    "parameters must be a dictionary"
                )
