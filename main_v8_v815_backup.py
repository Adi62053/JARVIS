"""
JARVIS V8 - Main Runtime

V8 Personal Automation runtime.

This runtime is developed independently from V7.
V7 remains frozen and unchanged.
"""

from automation.automation_manager import AutomationManager
from automation.automation_model import AutomationStep
from automation.automation_executor import AutomationExecutor
from automation.workflow_runner import WorkflowRunner
from automation.automation_command_handler import AutomationCommandHandler


def main(command: str | None = None) -> None:
    """Start the V8 runtime."""
    manager = AutomationManager()

    command_handler = AutomationCommandHandler(
        manager=manager
    )

    if command:
        print(
            command_handler.handle(command)
        )
        return

    workflow_runner = WorkflowRunner(
        executor=AutomationExecutor()
    )

    test_automation = manager.get("V8 Test Automation")

    if test_automation is None:
        test_automation = manager.create(
            name="V8 Test Automation",
            description="Initial V8 integration test",
        )

    if not test_automation.steps:
        test_automation.add_step(
            AutomationStep(
                "OPEN_APP",
                {"app": "notepad"},
            )
        )
        test_automation.add_step(
            AutomationStep(
                "WAIT",
                {"seconds": 2},
            )
        )
        manager.storage.save(manager.list_all())

    print("JARVIS V8")
    print("Personal Automation: READY")
    print(f"Automations loaded: {len(manager.list_all())}")

    results = workflow_runner.run(test_automation)

    for result in results:
        print(result)


if __name__ == "__main__":
    main()
