"""
JARVIS V8 - Application Handler

Bridge between the V8 Personal Automation system
and the existing V3 AppControl subsystem.

This module does not replace or modify V3 AppControl.
"""

from tools.app_control import AppControl


class AutomationAppHandler:
    """Handle V8 OPEN_APP actions through V3 AppControl."""

    def __init__(self) -> None:
        self.app_control = AppControl()

    def execute(self, parameters: dict) -> str:
        """Execute an OPEN_APP action through V3 AppControl."""
        if not isinstance(parameters, dict):
            raise ValueError(
                "OPEN_APP parameters must be a dictionary."
            )

        app_name = parameters.get("app")

        if not isinstance(app_name, str) or not app_name.strip():
            raise ValueError(
                "OPEN_APP requires an 'app' parameter."
            )

        return self.app_control.execute(app_name)
