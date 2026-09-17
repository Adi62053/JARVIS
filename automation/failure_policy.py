"""
JARVIS V8 - Automation Failure Policy

Defines what should happen after an automation step fails.

Supported policies:
- STOP
- CONTINUE

This module does not execute actions.
"""


class FailurePolicy:
    """Supported automation failure policies."""

    STOP = "STOP"
    CONTINUE = "CONTINUE"

    _SUPPORTED = {
        STOP,
        CONTINUE,
    }

    @classmethod
    def is_valid(cls, policy: str) -> bool:
        """Return True when the policy is supported."""
        if not isinstance(policy, str):
            return False

        return policy.strip().upper() in cls._SUPPORTED

    @classmethod
    def normalize(cls, policy: str) -> str:
        """Validate and normalize a failure policy."""
        if not isinstance(policy, str):
            raise TypeError(
                "failure policy must be a string"
            )

        normalized = policy.strip().upper()

        if normalized not in cls._SUPPORTED:
            raise ValueError(
                f"Unsupported failure policy: {policy}"
            )

        return normalized
