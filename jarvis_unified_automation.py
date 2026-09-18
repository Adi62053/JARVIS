"""
JARVIS Unified V8 Automation Layer

Extracted from jarvis_unified.py.

This module preserves the existing V8 automation behavior.
"""

from __future__ import annotations


def is_automation_command(command: str) -> bool:
    """
    Determine whether a command belongs to V8 automation.
    """

    command = command.lower().strip()

    automation_prefixes = [
        "create automation ",
        "show automation ",
        "enable automation ",
        "disable automation ",
        "delete automation ",
        "add step to automation ",
        "remove step from automation ",
        "add condition to automation ",
        "remove condition from automation ",
        "show conditions for automation ",
        "run automation ",
    ]

    automation_exact = [
        "list automations",
        "show automations",
    ]

    if command in automation_exact:
        return True

    for prefix in automation_prefixes:
        if command.startswith(prefix):
            return True

    return False


def handle_automation_command(
    command: str,
    automation_manager,
    automation_handler,
    automation_workflow_runner,
) -> str:
    """
    Execute a V8 automation command.

    V8 management remains delegated to the existing
    AutomationCommandHandler.

    Automation execution uses the existing:
        AutomationManager
        MemoryWorkflowRunner
        WorkflowRunner
        AutomationExecutor
    """

    if (
        automation_manager is None
        or automation_handler is None
        or automation_workflow_runner is None
    ):
        return "The automation system is not initialized, sir."

    normalized = command.strip()

    if normalized.lower().startswith("run automation "):
        automation_name = normalized[
            len("run automation "):
        ].strip()

        if not automation_name:
            return "Please tell me which automation to run, sir."

        automation = automation_manager.get(automation_name)

        if automation is None:
            return (
                f"Automation '{automation_name}' "
                "was not found."
            )

        try:
            results = automation_workflow_runner.run(
                automation,
                memory_query=automation.description,
            )

            response = (
                f"Automation '{automation.name}' "
                "completed."
            )

            if results:
                response += "\n" + "\n".join(results)

            return response

        except Exception as exc:
            return (
                f"Automation '{automation.name}' "
                f"failed: {type(exc).__name__}: {exc!r}"
            )

    try:
        return automation_handler.handle(normalized)

    except Exception as exc:
        return (
            "The automation command failed: "
            f"{type(exc).__name__}: {exc!r}"
        )
