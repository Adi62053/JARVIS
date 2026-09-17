from automation.automation_conditions import AutomationCondition
from automation.automation_model import Automation, AutomationStep
from automation.automation_storage import AutomationStorage


class AutomationManager:
    """High-level management of persistent automations."""

    def __init__(self, storage=None) -> None:
        self.storage = storage or AutomationStorage()
        self._automations = self._load()

    def _load(self) -> list[Automation]:
        """Load automations from persistent storage."""
        return self.storage.load()

    def _save(self) -> None:
        """Persist current automations."""
        self.storage.save(self._automations)

    def create(
        self,
        name: str,
        description: str = "",
    ) -> Automation:
        """Create and persist a new automation."""
        if self.get(name) is not None:
            raise ValueError(
                f"Automation already exists: {name}"
            )

        automation = Automation(
            name=name,
            description=description,
        )

        self._automations.append(automation)
        self._save()

        return automation

    def get(self, name: str) -> Automation | None:
        """Return an automation by name."""
        normalized_name = name.strip().lower()

        for automation in self._automations:
            if automation.name.lower() == normalized_name:
                return automation

        return None

    def list_all(self) -> list[Automation]:
        """Return all managed automations."""
        return list(self._automations)

    def add_step(
        self,
        name: str,
        step: AutomationStep,
    ) -> Automation:
        """Add a step to an existing automation."""
        automation = self.get(name)

        if automation is None:
            raise ValueError(
                f"Automation not found: {name}"
            )

        automation.add_step(step)
        self._save()

        return automation

    def add_condition(
        self,
        name: str,
        condition: AutomationCondition,
    ) -> Automation:
        """Add a condition to an existing automation."""
        automation = self.get(name)

        if automation is None:
            raise ValueError(
                f"Automation not found: {name}"
            )

        automation.add_condition(condition)
        self._save()

        return automation

    def remove_condition(
        self,
        name: str,
        condition_number: int,
    ) -> Automation:
        """Remove a condition using its 1-based number."""
        automation = self.get(name)

        if automation is None:
            raise ValueError(
                f"Automation not found: {name}"
            )

        if not isinstance(condition_number, int):
            raise TypeError(
                "condition_number must be an integer"
            )

        if condition_number < 1:
            raise ValueError(
                "condition_number must be at least 1"
            )

        index = condition_number - 1

        if index >= len(automation.conditions):
            raise IndexError(
                f"Condition {condition_number} does not exist "
                f"in {automation.name}."
            )

        automation.conditions.pop(index)
        self._save()

        return automation

    def update_description(
        self,
        name: str,
        description: str,
    ) -> Automation:
        """Update an automation description."""
        automation = self.get(name)

        if automation is None:
            raise ValueError(
                f"Automation not found: {name}"
            )

        automation.description = description
        self._save()

        return automation

    def remove_step(
        self,
        name: str,
        step_number: int,
    ) -> Automation:
        """Remove a step using its 1-based number."""
        automation = self.get(name)

        if automation is None:
            raise ValueError(
                f"Automation not found: {name}"
            )

        if not isinstance(step_number, int):
            raise TypeError(
                "step_number must be an integer"
            )

        if step_number < 1:
            raise ValueError(
                "step_number must be at least 1"
            )

        index = step_number - 1

        if index >= len(automation.steps):
            raise IndexError(
                f"Step {step_number} does not exist "
                f"in {automation.name}."
            )

        automation.steps.pop(index)
        self._save()

        return automation

    def enable(self, name: str) -> Automation:
        """Enable an automation."""
        automation = self.get(name)

        if automation is None:
            raise ValueError(
                f"Automation not found: {name}"
            )

        automation.enabled = True
        self._save()

        return automation

    def disable(self, name: str) -> Automation:
        """Disable an automation."""
        automation = self.get(name)

        if automation is None:
            raise ValueError(
                f"Automation not found: {name}"
            )

        automation.enabled = False
        self._save()

        return automation

    def delete(self, name: str) -> None:
        """Delete an automation."""
        automation = self.get(name)

        if automation is None:
            raise ValueError(
                f"Automation not found: {name}"
            )

        self._automations.remove(automation)
        self._save()
