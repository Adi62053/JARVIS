"""
JARVIS V8 - Automation Executor

Controlled execution layer for V8 automations.

Current stage:
- Validates automation steps.
- Applies centralized security checks.
- Requires explicit confirmation for dangerous steps.
- Supports dry-run execution.
- Executes only explicitly integrated actions.
- Resolves each action to the appropriate JARVIS subsystem.
- Captures execution failures using the V8.11 failure system.
- Reports the latest execution result.
"""

from automation.automation_confirmation import AutomationConfirmation
from automation.automation_dispatcher import AutomationDispatcher
from automation.automation_failure_handler import AutomationFailureHandler
from automation.automation_failure_result import AutomationFailureResult
from automation.automation_model import Automation
from automation.automation_security_gate import AutomationSecurityGate
from automation.failure_policy import FailurePolicy


class AutomationExecutor:
    """Safely process automation steps."""

    def __init__(
        self,
        dry_run: bool = True,
        dispatcher: AutomationDispatcher | None = None,
        confirmation: AutomationConfirmation | None = None,
        failure_policy: str = FailurePolicy.STOP,
        security_gate: AutomationSecurityGate | None = None,
    ) -> None:
        self.dry_run = dry_run
        self.dispatcher = dispatcher or AutomationDispatcher()

        if security_gate is not None:
            self.security_gate = security_gate
            self.confirmation = security_gate.confirmation
        else:
            self.confirmation = (
                confirmation or AutomationConfirmation()
            )
            self.security_gate = AutomationSecurityGate(
                confirmation=self.confirmation
            )

        self.failure_policy = FailurePolicy.normalize(
            failure_policy
        )
        self._last_result = AutomationFailureResult()

    @property
    def last_result(self) -> AutomationFailureResult:
        """Return the result of the most recent execution."""
        return self._last_result

    def execute(self, automation: Automation) -> list[str]:
        """
        Process an automation.

        Dangerous steps require explicit confirmation.
        Integrated actions may execute only when dry_run is False.
        Execution failures follow the configured failure policy.
        """
        if not automation.enabled:
            raise RuntimeError(
                f"Automation is disabled: {automation.name}"
            )

        results = []
        failure_result = AutomationFailureResult()
        self._last_result = failure_result

        for index, step in enumerate(automation.steps, start=1):
            subsystem = self.dispatcher.resolve(step.action)

            if subsystem is None:
                failure = AutomationFailureHandler.capture(
                    automation_name=automation.name,
                    action=step.action,
                    error=RuntimeError(
                        f"Unsupported automation action: {step.action}"
                    ),
                    step_number=index,
                    parameters=step.parameters,
                )

                failure_result.add_failure(failure)
                failure_result.apply_policy(
                    self.failure_policy
                )

                if failure_result.stopped:
                    raise RuntimeError(
                        failure.message
                    )

                continue

            security_note = self.security_gate.check(
                automation.name,
                index,
                step,
            )

            message = (
                f"Step {index}: {step.action} "
                f"{step.parameters} -> {subsystem}"
                f" | SECURITY={step.security_level}"
                f"{security_note}"
            )

            if self.dry_run:
                results.append(f"DRY RUN - {message}")
                failure_result.successful_steps += 1
                continue

            handler = self.dispatcher.get_handler(step.action)

            if handler is None:
                failure = AutomationFailureHandler.capture(
                    automation_name=automation.name,
                    action=step.action,
                    error=RuntimeError(
                        f"Real execution is not yet integrated for: "
                        f"{step.action}"
                    ),
                    step_number=index,
                    parameters=step.parameters,
                )

                failure_result.add_failure(failure)
                failure_result.apply_policy(
                    self.failure_policy
                )

                if failure_result.stopped:
                    raise RuntimeError(
                        failure.message
                    )

                continue

            try:
                execution_result = handler.execute(
                    step.parameters
                )
            except Exception as exc:
                failure = AutomationFailureHandler.capture(
                    automation_name=automation.name,
                    action=step.action,
                    error=exc,
                    step_number=index,
                    parameters=step.parameters,
                )

                failure_result.add_failure(failure)
                failure_result.apply_policy(
                    self.failure_policy
                )

                if failure_result.stopped:
                    raise RuntimeError(
                        f"Execution failed for step {index} "
                        f"({step.action}): {exc}"
                    ) from exc

                results.append(
                    f"FAILED - Step {index}: {step.action} "
                    f"-> {failure.message}"
                )
                continue

            results.append(
                f"EXECUTED - {message} -> {execution_result}"
            )
            failure_result.successful_steps += 1

        return results
