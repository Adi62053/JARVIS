"""
JARVIS V8 - Automation Model

Defines the data structures used by the Personal Automation system.

This module does not execute automations.
It only describes and validates automation steps, conditions,
and automation definitions.
"""

from dataclasses import dataclass, field
from typing import Any

from automation.automation_actions import is_valid_action
from automation.automation_conditions import AutomationCondition
from automation.automation_security import normalize_security_level


@dataclass
class AutomationStep:
    """
    Represents one validated action inside an automation.
    """

    action: str
    parameters: dict[str, Any] = field(default_factory=dict)
    security_level: str = "SAFE"

    def __post_init__(self) -> None:
        """Validate and normalize the step."""
        normalized_action = self.action.strip().upper()

        if not is_valid_action(normalized_action):
            raise ValueError(
                f"Unsupported automation action: {self.action}"
            )

        self.action = normalized_action
        self.security_level = normalize_security_level(
            self.security_level
        )


@dataclass
class Automation:
    """
    Represents a complete reusable automation.
    """

    name: str
    description: str = ""
    steps: list[AutomationStep] = field(default_factory=list)
    conditions: list[AutomationCondition] = field(default_factory=list)
    enabled: bool = True

    def add_step(self, step: AutomationStep) -> None:
        """Add one validated step to the automation."""
        if not isinstance(step, AutomationStep):
            raise TypeError("step must be an AutomationStep")

        self.steps.append(step)

    def add_condition(
        self,
        condition: AutomationCondition,
    ) -> None:
        """Add one validated condition to the automation."""
        if not isinstance(condition, AutomationCondition):
            raise TypeError(
                "condition must be an AutomationCondition"
            )

        self.conditions.append(condition)

    def step_count(self) -> int:
        """Return the number of steps in the automation."""
        return len(self.steps)

    def condition_count(self) -> int:
        """Return the number of conditions in the automation."""
        return len(self.conditions)
