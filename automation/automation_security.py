"""
JARVIS V8 - Automation Security

Defines security levels and validation rules for automation steps.

This module does not execute actions.
It only classifies and validates automation security levels.
"""

from enum import Enum


class AutomationSecurityLevel(str, Enum):
    """Approved security levels for automation actions."""

    SAFE = "SAFE"
    CAUTION = "CAUTION"
    DANGEROUS = "DANGEROUS"


def is_valid_security_level(level: str) -> bool:
    """Return True when the security level is approved."""
    if not isinstance(level, str):
        return False

    return level.strip().upper() in {
        item.value for item in AutomationSecurityLevel
    }


def normalize_security_level(level: str) -> str:
    """Normalize and validate a security level."""
    if not isinstance(level, str):
        raise ValueError(
            f"Invalid security level: {level}"
        )

    normalized = level.strip().upper()

    if not is_valid_security_level(normalized):
        raise ValueError(
            f"Unsupported security level: {level}"
        )

    return normalized


def requires_confirmation(level: str) -> bool:
    """Return True when explicit confirmation is required."""
    normalized = normalize_security_level(level)

    return normalized == AutomationSecurityLevel.DANGEROUS.value
