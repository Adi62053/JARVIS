"""
JARVIS V8 - WAIT Handler

Provides controlled waiting for V8 automation workflows.

This module does not perform computer control.
"""

import time


class AutomationWaitHandler:
    """Handle WAIT actions inside V8 automations."""

    def execute(self, parameters: dict) -> str:
        """Wait for the requested number of seconds."""
        if not isinstance(parameters, dict):
            raise ValueError(
                "WAIT parameters must be a dictionary."
            )

        seconds = parameters.get("seconds")

        if isinstance(seconds, bool) or not isinstance(
            seconds,
            (int, float),
        ):
            raise ValueError(
                "WAIT requires a numeric 'seconds' parameter."
            )

        if seconds < 0:
            raise ValueError(
                "WAIT seconds cannot be negative."
            )

        time.sleep(seconds)

        return f"Waited {seconds} seconds."
