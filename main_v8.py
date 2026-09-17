"""
JARVIS V8 - Main Runtime

V8 Personal Automation runtime.

V7 remains frozen and unchanged.
"""

import sys

from automation.automation_command_handler import (
    AutomationCommandHandler,
)
from automation.automation_executor import AutomationExecutor
from automation.automation_manager import AutomationManager
from automation.automation_memory import AutomationMemory
from automation.automation_voice import AutomationVoice
from automation.memory_workflow_runner import MemoryWorkflowRunner
from automation.schedule_runner import ScheduleRunner
from automation.workflow_runner import WorkflowRunner


def main(command: str | None = None) -> None:
    """Start the V8 runtime."""

    manager = AutomationManager()

    command_handler = AutomationCommandHandler(
        manager=manager
    )

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

    scheduler = ScheduleRunner(
        automation_manager=manager,
        workflow_runner=memory_workflow_runner,
    )

    print("JARVIS V8")
    print("Personal Automation: READY")
    print(
        f"Automations loaded: "
        f"{len(manager.list_all())}"
    )
    print(
        f"Memories available: "
        f"{memory.get_memory_count()}"
    )

    if command:
        normalized_command = command.strip()

        if normalized_command.lower().startswith(
            "run automation "
        ):
            automation_name = normalized_command[
                len("run automation "):
            ].strip()

            automation = manager.get(automation_name)

            if automation is None:
                response = (
                    f"Automation '{automation_name}' "
                    "was not found."
                )
            else:
                try:
                    results = memory_workflow_runner.run(
                        automation,
                        memory_query=automation.description,
                    )

                    response = (
                        f"Automation '{automation.name}' "
                        "completed."
                    )

                    if results:
                        response += "\n" + "\n".join(
                            results
                        )

                except Exception as exc:
                    response = (
                        f"Automation '{automation.name}' "
                        f"failed: {exc}"
                    )

        else:
            response = command_handler.handle(
                normalized_command
            )

        print(response)

        voice.speak(response)
        return

    print("V8 integration systems: READY")
    print(
        "Commands: automation management available."
    )
    print("Scheduler: READY")
    print("Memory: READY")
    print("Voice: READY")


if __name__ == "__main__":
    command = " ".join(sys.argv[1:]).strip()
    main(command if command else None)
