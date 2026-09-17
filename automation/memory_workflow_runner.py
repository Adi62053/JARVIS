"""
JARVIS V8 - Memory Workflow Runner

Adds persistent-memory context to V8 workflow execution.

This module reuses:
- V8 WorkflowRunner
- V8 AutomationMemory
- Frozen V7 MemoryController through AutomationMemory

It does not modify V7 or the core executor.
"""

from automation.automation_memory import AutomationMemory
from automation.automation_model import Automation
from automation.workflow_runner import WorkflowRunner


class MemoryWorkflowRunner:
    """Run an automation with optional relevant memory context."""

    def __init__(
        self,
        workflow_runner: WorkflowRunner | None = None,
        memory: AutomationMemory | None = None,
    ) -> None:
        self.workflow_runner = (
            workflow_runner or WorkflowRunner()
        )
        self.memory = memory or AutomationMemory()

    def get_context(
        self,
        query: str,
        limit: int = 5,
    ) -> str:
        """Return relevant persistent-memory context."""
        return self.memory.build_context(
            query,
            limit=limit,
        )

    def run(
        self,
        automation: Automation,
        memory_query: str | None = None,
        memory_limit: int = 5,
    ) -> list[str]:
        """
        Run an automation with optional memory lookup.

        Memory is read-only during workflow execution.
        """
        if not isinstance(automation, Automation):
            raise TypeError(
                "automation must be an Automation"
            )

        if memory_query is not None:
            if not isinstance(memory_query, str):
                raise TypeError(
                    "memory_query must be a string or None"
                )

            memory_query = memory_query.strip()

            if memory_query:
                context = self.get_context(
                    memory_query,
                    limit=memory_limit,
                )

                if context:
                    print(
                        "JARVIS Memory Context:"
                    )
                    print(context)

        return self.workflow_runner.run(
            automation
        )
