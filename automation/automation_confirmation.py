"""
JARVIS V8 - Automation Confirmation

Manages explicit confirmation state for automation steps.

This module does not execute actions.
It only records whether a specific step has been explicitly approved.
"""


class AutomationConfirmation:
    """Manage explicit confirmations for automation steps."""

    def __init__(self) -> None:
        self._confirmed: set[str] = set()

    def request(self, automation_name: str, step_index: int) -> str:
        """Create a confirmation key for a specific automation step."""
        return self._key(automation_name, step_index)

    def confirm(self, automation_name: str, step_index: int) -> None:
        """Explicitly approve a specific automation step."""
        self._confirmed.add(
            self._key(automation_name, step_index)
        )

    def is_confirmed(
        self,
        automation_name: str,
        step_index: int,
    ) -> bool:
        """Return True when the step has been explicitly approved."""
        return (
            self._key(automation_name, step_index)
            in self._confirmed
        )

    def consume(
        self,
        automation_name: str,
        step_index: int,
    ) -> bool:
        """
        Consume a confirmation.

        Returns True only when a matching confirmation existed.
        """
        key = self._key(automation_name, step_index)

        if key not in self._confirmed:
            return False

        self._confirmed.remove(key)
        return True

    @staticmethod
    def _key(automation_name: str, step_index: int) -> str:
        """Build a stable confirmation key."""
        return f"{automation_name.strip().lower()}:{step_index}"
