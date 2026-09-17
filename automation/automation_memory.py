"""
JARVIS V8 - Memory Integration

V8 adapter around the frozen V7 MemoryController.

V7 memory modules remain unchanged.
"""

from typing import Any

from memory.memory_controller import MemoryController


class AutomationMemory:
    """Provide V8-safe access to the existing JARVIS memory system."""

    def __init__(
        self,
        controller: MemoryController | None = None,
    ) -> None:
        self.controller = controller or MemoryController()

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Search persistent JARVIS memories."""
        if not isinstance(query, str):
            raise TypeError("query must be a string")

        query = query.strip()

        if not query:
            return []

        return self.controller.search_relevant(
            query,
            limit=limit,
        )

    def build_context(
        self,
        query: str,
        limit: int = 5,
    ) -> str:
        """Build relevant memory context for an automation."""
        if not isinstance(query, str):
            raise TypeError("query must be a string")

        return self.controller.build_context(
            query,
            limit=limit,
        )

    def get_memory_count(self) -> int:
        """Return the number of persistent memories."""
        return self.controller.get_memory_count()

    def execute_memory_command(
        self,
        command: str,
    ) -> dict[str, Any]:
        """Execute an existing V7 memory command through its controller."""
        return self.controller.execute(command)
