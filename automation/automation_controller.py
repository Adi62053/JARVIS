"""
JARVIS V8 - Automation Controller

Manages automation definitions.

This module does not execute automation actions.
Execution will be handled by the V8 execution layer.
"""

from automation.automation_model import Automation


class AutomationController:
    """
    Manages the in-memory collection of automations.
    """

    def __init__(self) -> None:
        self._automations: dict[str, Automation] = {}

    def create(self, automation: Automation) -> bool:
        """
        Create an automation.

        Returns False if an automation with the same name already exists.
        """
        key = automation.name.strip().lower()

        if not key or key in self._automations:
            return False

        self._automations[key] = automation
        return True

    def get(self, name: str) -> Automation | None:
        """Retrieve an automation by name."""
        return self._automations.get(name.strip().lower())

    def list_all(self) -> list[Automation]:
        """Return all stored automations."""
        return list(self._automations.values())

    def enable(self, name: str) -> bool:
        """Enable an automation."""
        automation = self.get(name)

        if automation is None:
            return False

        automation.enabled = True
        return True

    def disable(self, name: str) -> bool:
        """Disable an automation."""
        automation = self.get(name)

        if automation is None:
            return False

        automation.enabled = False
        return True

    def delete(self, name: str) -> bool:
        """Delete an automation from the controller."""
        key = name.strip().lower()

        if key not in self._automations:
            return False

        del self._automations[key]
        return True
