"""
JARVIS V8 - Automation Dispatcher

Maps approved automation actions to the existing JARVIS
subsystems.

Current stage:
- Resolves approved actions.
- Provides executable handlers for integrated actions.
- Does not modify existing V3/V4/V5 subsystems.
"""

from automation.automation_actions import AutomationAction
from automation.automation_app_handler import AutomationAppHandler
from automation.automation_wait_handler import AutomationWaitHandler


class AutomationDispatcher:
    """Route V8 automation actions to their handlers."""

    ACTION_HANDLERS = {
        AutomationAction.OPEN_APP.value: "V3 AppControl",
        AutomationAction.OPEN_FILE.value: "V4 FileSystemControl",
        AutomationAction.OPEN_FOLDER.value: "V4 FileSystemControl",
        AutomationAction.CREATE_FILE.value: "V4 FileSystemControl",
        AutomationAction.CREATE_FOLDER.value: "V4 FileSystemControl",
        AutomationAction.MOVE_FILE.value: "V4 FileSystemControl",
        AutomationAction.COPY_FILE.value: "V4 FileSystemControl",
        AutomationAction.RENAME_FILE.value: "V4 FileSystemControl",
        AutomationAction.OPEN_URL.value: "V5 WebRouter",
        AutomationAction.WAIT.value: "V8 Execution Engine",
    }

    def __init__(self) -> None:
        self._handlers = {
            AutomationAction.OPEN_APP.value: AutomationAppHandler(),
            AutomationAction.WAIT.value: AutomationWaitHandler(),
        }

    def resolve(self, action: str) -> str | None:
        """Return the subsystem responsible for an action."""
        if not isinstance(action, str):
            return None

        return self.ACTION_HANDLERS.get(action.strip().upper())

    def get_handler(self, action: str):
        """Return an executable handler for an integrated action."""
        if not isinstance(action, str):
            return None

        return self._handlers.get(action.strip().upper())

    def is_supported(self, action: str) -> bool:
        """Return True when an action has a registered handler."""
        return self.resolve(action) is not None
