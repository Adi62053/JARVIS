"""
JARVIS V8 - Automation Failure Result

Represents the outcome of an automation execution
that may contain captured failures.
"""

from dataclasses import dataclass, field

from automation.automation_failure import AutomationFailure
from automation.failure_policy import FailurePolicy


@dataclass
class AutomationFailureResult:
    """Structured result for automation failure handling."""

    successful_steps: int = 0
    failures: list[AutomationFailure] = field(default_factory=list)
    stopped: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.successful_steps, int):
            raise TypeError("successful_steps must be an integer")

        if self.successful_steps < 0:
            raise ValueError("successful_steps cannot be negative")

        if not isinstance(self.failures, list):
            raise TypeError("failures must be a list")

        for failure in self.failures:
            if not isinstance(failure, AutomationFailure):
                raise TypeError(
                    "failures must contain AutomationFailure objects"
                )

        if not isinstance(self.stopped, bool):
            raise TypeError("stopped must be a boolean")

    def add_failure(self, failure: AutomationFailure) -> None:
        """Add one captured failure."""
        if not isinstance(failure, AutomationFailure):
            raise TypeError(
                "failure must be an AutomationFailure"
            )

        self.failures.append(failure)

    def apply_policy(self, policy: str) -> None:
        """Apply a failure policy to the execution result."""
        normalized_policy = FailurePolicy.normalize(policy)

        if normalized_policy == FailurePolicy.STOP:
            self.stopped = True
        elif normalized_policy == FailurePolicy.CONTINUE:
            self.stopped = False

    def failure_count(self) -> int:
        """Return the number of captured failures."""
        return len(self.failures)

    def success_count(self) -> int:
        """Return the number of successful steps."""
        return self.successful_steps

    def has_failures(self) -> bool:
        """Return True when at least one failure was captured."""
        return bool(self.failures)
