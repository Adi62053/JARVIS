"""
JARVIS V8 - Automation Conditions

Defines reusable condition types for Personal Automation.

Current stage:
- Condition data model.
- Condition validation.
- Condition context integration.
- No action execution.
"""

from dataclasses import dataclass
from typing import Any

from automation.condition_context import ConditionContext


@dataclass(frozen=True)
class AutomationCondition:
    """
    Represents one condition used by an automation.

    Supported condition types:
    - ALWAYS
    - VALUE_EQUALS
    - VALUE_NOT_EQUALS

    value_name identifies the value read from ConditionContext.
    """

    condition_type: str
    expected_value: Any = None
    value_name: str = "value"

    def __post_init__(self) -> None:
        """Validate and normalize the condition."""
        normalized_type = self.condition_type.strip().upper()

        supported_types = {
            "ALWAYS",
            "VALUE_EQUALS",
            "VALUE_NOT_EQUALS",
        }

        if normalized_type not in supported_types:
            raise ValueError(
                f"Unsupported condition type: {self.condition_type}"
            )

        if (
            normalized_type != "ALWAYS"
            and self.expected_value is None
        ):
            raise ValueError(
                f"{normalized_type} requires expected_value"
            )

        if not isinstance(self.value_name, str):
            raise TypeError("value_name must be a string")

        normalized_value_name = self.value_name.strip()

        if not normalized_value_name:
            raise ValueError("value_name cannot be empty")

        object.__setattr__(
            self,
            "condition_type",
            normalized_type,
        )

        object.__setattr__(
            self,
            "value_name",
            normalized_value_name,
        )


class ConditionEvaluator:
    """Evaluate automation conditions."""

    @staticmethod
    def evaluate(
        condition: AutomationCondition,
        actual_value: Any = None,
        context: ConditionContext | None = None,
    ) -> bool:
        """
        Return True when the supplied condition is satisfied.

        When a ConditionContext is supplied, the condition's
        value_name is used to obtain the actual value.
        """
        if not isinstance(condition, AutomationCondition):
            raise TypeError(
                "condition must be an AutomationCondition"
            )

        if condition.condition_type == "ALWAYS":
            return True

        if context is not None:
            if not isinstance(context, ConditionContext):
                raise TypeError(
                    "context must be a ConditionContext"
                )

            actual_value = context.get(
                condition.value_name
            )

        if condition.condition_type == "VALUE_EQUALS":
            return actual_value == condition.expected_value

        if condition.condition_type == "VALUE_NOT_EQUALS":
            return actual_value != condition.expected_value

        return False
