"""
JARVIS V8 - Automation Condition Context

Provides runtime values used when evaluating automation conditions.

This module does not execute automation actions.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ConditionContext:
    """
    Runtime values available to automation conditions.

    Values are supplied explicitly by the caller so condition
    evaluation remains deterministic and testable.
    """

    values: dict[str, Any]

    def get(self, name: str, default: Any = None) -> Any:
        """Return one named condition value."""
        if not isinstance(name, str):
            raise TypeError("name must be a string")

        return self.values.get(
            name.strip(),
            default,
        )
