"""
JARVIS V9 - Security Model

Defines the core security vocabulary used by the V9 security system.

This module does not execute commands, request elevation, modify the
system, or make authorization decisions.

It only defines strongly typed security states.
"""

from enum import Enum


class SecurityRiskLevel(str, Enum):
    """Risk classification for JARVIS operations."""

    SAFE = "SAFE"
    CAUTION = "CAUTION"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SecurityPrivilegeLevel(str, Enum):
    """Privilege level required by an operation."""

    USER = "USER"
    ADMINISTRATOR = "ADMINISTRATOR"
    SYSTEM = "SYSTEM"
    FIRMWARE = "FIRMWARE"
    HARDWARE = "HARDWARE"


class AuthorizationState(str, Enum):
    """Authorization state for a security-sensitive operation."""

    NOT_REQUIRED = "NOT_REQUIRED"
    REQUIRED = "REQUIRED"
    AUTHORIZED = "AUTHORIZED"
    DENIED = "DENIED"


class SecurityDecision(str, Enum):
    """Final security decision before an operation executes."""

    ALLOW = "ALLOW"
    REQUIRE_AUTHORIZATION = "REQUIRE_AUTHORIZATION"
    REQUIRE_ELEVATION = "REQUIRE_ELEVATION"
    DENY = "DENY"
