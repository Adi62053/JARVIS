"""
JARVIS V8.11 - Failure Handling Unit Tests
"""

from automation.automation_failure import AutomationFailure
from automation.automation_failure_handler import AutomationFailureHandler
from automation.automation_failure_result import AutomationFailureResult
from automation.failure_policy import FailurePolicy


def test_failure_model() -> None:
    failure = AutomationFailure(
        automation_name="Test Automation",
        action="WAIT",
        message="Test failure",
        step_number=1,
        parameters={"seconds": 0},
    )

    assert failure.automation_name == "Test Automation"
    assert failure.action == "WAIT"
    assert failure.message == "Test failure"
    assert failure.step_number == 1
    assert failure.parameters == {"seconds": 0}

    print("[PASS] AutomationFailure model.")


def test_failure_handler() -> None:
    failure = AutomationFailureHandler.capture(
        automation_name="Test Automation",
        action="WAIT",
        error=RuntimeError("Execution failed"),
        step_number=1,
        parameters={"seconds": 0},
    )

    assert isinstance(failure, AutomationFailure)
    assert failure.automation_name == "Test Automation"
    assert failure.action == "WAIT"
    assert failure.step_number == 1
    assert "Execution failed" in failure.message

    print("[PASS] AutomationFailureHandler capture.")


def test_failure_result_stop_policy() -> None:
    result = AutomationFailureResult(
        successful_steps=1
    )

    result.add_failure(
        AutomationFailure(
            automation_name="Test Automation",
            action="WAIT",
            message="Failure",
            step_number=2,
        )
    )

    result.apply_policy(FailurePolicy.STOP)

    assert result.success_count() == 1
    assert result.failure_count() == 1
    assert result.has_failures() is True
    assert result.stopped is True

    print("[PASS] Failure result STOP policy.")


def test_failure_result_continue_policy() -> None:
    result = AutomationFailureResult(
        successful_steps=1
    )

    result.add_failure(
        AutomationFailure(
            automation_name="Test Automation",
            action="WAIT",
            message="Failure",
            step_number=2,
        )
    )

    result.apply_policy(FailurePolicy.CONTINUE)

    assert result.success_count() == 1
    assert result.failure_count() == 1
    assert result.has_failures() is True
    assert result.stopped is False

    print("[PASS] Failure result CONTINUE policy.")


def main() -> None:
    test_failure_model()
    test_failure_handler()
    test_failure_result_stop_policy()
    test_failure_result_continue_policy()

    print("[PASS] V8.11 failure-handling unit test completed.")


if __name__ == "__main__":
    main()
