"""
JARVIS V9 - Risk and Policy Engine

Combines operation risk and current privilege into a preliminary
security decision.

This module does not execute operations, request elevation, or grant
authorization. It only evaluates the defined V9 security policy.
"""

from __future__ import annotations

from security.v9_security_model import (
    AuthorizationState,
    SecurityDecision,
    SecurityPrivilegeLevel,
    SecurityRiskLevel,
)


class V9PolicyEngine:
    """Evaluate V9 risk and privilege policy."""

    def evaluate(
        self,
        risk: SecurityRiskLevel,
        privilege: SecurityPrivilegeLevel,
    ) -> SecurityDecision:
        """Return the preliminary security decision."""

        if not isinstance(risk, SecurityRiskLevel):
            raise TypeError("risk must be a SecurityRiskLevel")

        if not isinstance(privilege, SecurityPrivilegeLevel):
            raise TypeError(
                "privilege must be a SecurityPrivilegeLevel"
            )

        if risk == SecurityRiskLevel.SAFE:
            return SecurityDecision.ALLOW

        if risk == SecurityRiskLevel.CAUTION:
            return SecurityDecision.ALLOW

        if risk == SecurityRiskLevel.HIGH:
            if privilege in {
                SecurityPrivilegeLevel.USER,
                SecurityPrivilegeLevel.ADMINISTRATOR,
                SecurityPrivilegeLevel.SYSTEM,
            }:
                return SecurityDecision.REQUIRE_AUTHORIZATION

            return SecurityDecision.REQUIRE_ELEVATION

        if risk == SecurityRiskLevel.CRITICAL:
            return SecurityDecision.REQUIRE_AUTHORIZATION

        return SecurityDecision.DENY
