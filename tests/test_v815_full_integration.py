"""
JARVIS V8.15 - Full Integration Test
"""

from automation.automation_executor import AutomationExecutor
from automation.automation_manager import AutomationManager
from automation.automation_memory import AutomationMemory
from automation.automation_model import AutomationStep
from automation.automation_voice import AutomationVoice
from automation.memory_workflow_runner import MemoryWorkflowRunner
from automation.workflow_runner import WorkflowRunner


def main() -> None:
    manager = AutomationManager()

    automation = manager.get("V8.15 Unit Integration Test")

    if automation is None:
        automation = manager.create(
            "V8.15 Unit Integration Test",
            "Full V8.15 integration test",
        )

    automation.steps.clear()
    automation.conditions.clear()

    automation.add_step(
        AutomationStep(
            action="WAIT",
            parameters={"seconds": 0},
        )
    )

    manager.storage.save(manager.list_all())

    executor = AutomationExecutor()

    workflow_runner = WorkflowRunner(
        executor=executor
    )

    memory = AutomationMemory()

    memory_workflow_runner = MemoryWorkflowRunner(
        workflow_runner=workflow_runner,
        memory=memory,
    )

    voice = AutomationVoice()

    context = memory_workflow_runner.get_context(
        "favourite",
        limit=5,
    )

    assert isinstance(context, str)

    results = memory_workflow_runner.run(
        automation,
        memory_query="favourite",
        memory_limit=5,
    )

    assert isinstance(results, list)
    assert len(results) == 1
    assert "DRY RUN" in results[0]

    response = (
        f"V8.15 integration test completed. "
        f"{len(results)} step executed."
    )

    voice.speak(response)

    print("[PASS] Manager integration.")
    print("[PASS] Memory integration.")
    print("[PASS] Workflow integration.")
    print("[PASS] Executor integration.")
    print("[PASS] Voice integration.")
    print("[PASS] V8.15 full-integration test completed.")


if __name__ == "__main__":
    main()
