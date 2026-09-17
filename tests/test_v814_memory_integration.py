"""
JARVIS V8.14 - Memory Integration Test
"""

from automation.automation_memory import AutomationMemory
from automation.automation_model import Automation, AutomationStep
from automation.memory_workflow_runner import MemoryWorkflowRunner
from automation.workflow_runner import WorkflowRunner


def test_memory_adapter() -> None:
    memory = AutomationMemory()

    count = memory.get_memory_count()

    assert isinstance(count, int)
    assert count >= 0

    context = memory.build_context(
        "favourite fruit",
        limit=5,
    )

    assert isinstance(context, str)

    print("[PASS] AutomationMemory adapter.")


def test_memory_search() -> None:
    memory = AutomationMemory()

    results = memory.search(
        "favourite",
        limit=5,
    )

    assert isinstance(results, list)

    print("[PASS] Memory search integration.")


def test_memory_workflow_runner() -> None:
    workflow_runner = MemoryWorkflowRunner(
        workflow_runner=WorkflowRunner()
    )

    automation = Automation(
        name="V8.14 Memory Test",
        description="Memory integration unit test",
    )

    automation.add_step(
        AutomationStep(
            action="WAIT",
            parameters={"seconds": 0},
        )
    )

    results = workflow_runner.run(
        automation,
        memory_query="favourite",
        memory_limit=5,
    )

    assert isinstance(results, list)
    assert len(results) == 1
    assert "DRY RUN" in results[0]

    print("[PASS] Memory workflow integration.")


def main() -> None:
    test_memory_adapter()
    test_memory_search()
    test_memory_workflow_runner()

    print("[PASS] V8.14 memory-integration test completed.")


if __name__ == "__main__":
    main()
