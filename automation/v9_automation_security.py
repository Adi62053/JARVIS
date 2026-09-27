"""
JARVIS V9 - V8 Automation Security Adapter

Bridges executable V8 automation actions into the V9 security
decision pipeline.

This module does not execute automation actions and does not grant
permissions. It only translates an automation step into a V9
security evaluation.
"""

from __future__ import annotations

from automation.automation_model import AutomationStep
from security.v9_security_controller import V9SecurityController
from security.v9_security_model import (
    SecurityDecision,
    SecurityPrivilegeLevel,
    SecurityRiskLevel,
)


class V9AutomationSecurity:
    """Evaluate V8 automation steps through V9 security."""

    def __init__(
        self,
        controller: V9SecurityController,
    ) -> None:
        if not isinstance(controller, V9SecurityController):
            raise TypeError(
                "controller must be a V9SecurityController"
            )

        self.controller = controller

    def evaluate(
        self,
        *,
        automation_name: str,
        step_number: int,
        step: AutomationStep,
    ) -> SecurityDecision:
        """Evaluate one executable V8 automation step."""

        if not isinstance(automation_name, str) or not automation_name.strip():
            raise ValueError("automation_name cannot be empty")

        if not isinstance(step_number, int) or step_number < 1:
            raise ValueError("step_number must be a positive integer")

        if not isinstance(step, AutomationStep):
            raise TypeError("step must be an AutomationStep")

        if step.action == "OPEN_APP":
            app_name = step.parameters.get("app")

            if not isinstance(app_name, str) or not app_name.strip():
                raise ValueError(
                    "OPEN_APP requires a non-empty 'app' parameter"
                )

            return self.controller.evaluate(
                operation_id=(
                    f"automation:{automation_name.strip().lower()}"
                    f":step:{step_number}:open_app"
                ),
                capability="APPLICATION",
                resource=app_name.strip(),
                risk_level=SecurityRiskLevel.CAUTION,
                required_privilege=SecurityPrivilegeLevel.USER,
            )

        if step.action == "WAIT":
            return self.controller.evaluate(
                operation_id=(
                    f"automation:{automation_name.strip().lower()}"
                    f":step:{step_number}:wait"
                ),
                capability="SYSTEM",
                resource="automation.wait",
                risk_level=SecurityRiskLevel.SAFE,
                required_privilege=SecurityPrivilegeLevel.USER,
            )

        raise ValueError(
            f"V9 security mapping is not defined for action: {step.action}"
        )
