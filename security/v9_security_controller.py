"""
JARVIS V9 - Security Controller

Coordinates the V9 permission, privilege, policy, authorization,
and audit components.

This module does not execute system operations or request elevation.
It only evaluates and records security decisions.
"""

from __future__ import annotations

from security.v9_audit_logger import V9AuditLogger
from security.v9_authorization_manager import V9AuthorizationManager
from security.v9_permission_manager import V9PermissionManager
from security.v9_policy_engine import V9PolicyEngine
from security.v9_privilege_manager import V9PrivilegeManager
from security.v9_security_model import (
    AuthorizationState,
    SecurityDecision,
    SecurityPrivilegeLevel,
    SecurityRiskLevel,
)


class V9SecurityController:
    """Coordinate the V9 security decision pipeline."""

    def __init__(
        self,
        *,
        permission_manager: V9PermissionManager | None = None,
        privilege_manager: V9PrivilegeManager | None = None,
        policy_engine: V9PolicyEngine | None = None,
        authorization_manager: V9AuthorizationManager | None = None,
        audit_logger: V9AuditLogger | None = None,
    ) -> None:
        self.permission_manager = (
            permission_manager or V9PermissionManager()
        )
        self.privilege_manager = (
            privilege_manager or V9PrivilegeManager()
        )
        self.policy_engine = policy_engine or V9PolicyEngine()
        self.authorization_manager = (
            authorization_manager or V9AuthorizationManager()
        )
        self.audit_logger = audit_logger or V9AuditLogger()

    def evaluate(
        self,
        *,
        operation_id: str,
        capability: str,
        resource: str,
        risk_level: SecurityRiskLevel,
        required_privilege: SecurityPrivilegeLevel,
    ) -> SecurityDecision:
        """
        Evaluate one operation through the V9 security pipeline.

        No system operation is executed.
        """

        if not isinstance(operation_id, str) or not operation_id.strip():
            raise ValueError("operation_id cannot be empty")

        if not isinstance(capability, str) or not capability.strip():
            raise ValueError("capability cannot be empty")

        if not isinstance(resource, str) or not resource.strip():
            raise ValueError("resource cannot be empty")

        if not isinstance(risk_level, SecurityRiskLevel):
            raise TypeError(
                "risk_level must be a SecurityRiskLevel"
            )

        if not isinstance(
            required_privilege,
            SecurityPrivilegeLevel,
        ):
            raise TypeError(
                "required_privilege must be a SecurityPrivilegeLevel"
            )

        current_privilege = (
            self.privilege_manager.get_current_privilege()
        )

        if not self.permission_manager.is_allowed(capability):
            decision = SecurityDecision.DENY
            authorization_state = AuthorizationState.DENIED
            result = "PERMISSION_DENIED"

            self.audit_logger.record(
                operation_id=operation_id,
                capability=capability,
                resource=resource,
                risk_level=risk_level.value,
                required_privilege=required_privilege.value,
                current_privilege=current_privilege.value,
                authorization_state=authorization_state.value,
                decision=decision.value,
                result=result,
            )

            return decision

        if (
            required_privilege.value
            not in {
                current_privilege.value,
                SecurityPrivilegeLevel.USER.value,
            }
            and current_privilege
            not in {
                SecurityPrivilegeLevel.SYSTEM,
                SecurityPrivilegeLevel.FIRMWARE,
                SecurityPrivilegeLevel.HARDWARE,
            }
        ):
            decision = SecurityDecision.REQUIRE_ELEVATION
            authorization_state = AuthorizationState.NOT_REQUIRED
            result = "PRIVILEGE_REQUIRED"

            self.audit_logger.record(
                operation_id=operation_id,
                capability=capability,
                resource=resource,
                risk_level=risk_level.value,
                required_privilege=required_privilege.value,
                current_privilege=current_privilege.value,
                authorization_state=authorization_state.value,
                decision=decision.value,
                result=result,
            )

            return decision

        policy_decision = self.policy_engine.evaluate(
            risk_level,
            current_privilege,
        )

        if policy_decision == SecurityDecision.ALLOW:
            authorization_state = AuthorizationState.NOT_REQUIRED
            result = "AUTHORIZED_BY_POLICY"

        elif policy_decision == SecurityDecision.REQUIRE_AUTHORIZATION:
            if self.authorization_manager.consume(operation_id):
                policy_decision = SecurityDecision.ALLOW
                authorization_state = AuthorizationState.AUTHORIZED
                result = "EXPLICIT_AUTHORIZATION_CONSUMED"
            else:
                authorization_state = AuthorizationState.REQUIRED
                result = "AUTHORIZATION_REQUIRED"

        else:
            authorization_state = AuthorizationState.DENIED
            result = "POLICY_DENIED"

        self.audit_logger.record(
            operation_id=operation_id,
            capability=capability,
            resource=resource,
            risk_level=risk_level.value,
            required_privilege=required_privilege.value,
            current_privilege=current_privilege.value,
            authorization_state=authorization_state.value,
            decision=policy_decision.value,
            result=result,
        )

        return policy_decision
