"""
JARVIS V7.8 - Memory Controller

Integration layer between the V7 memory modules and the JARVIS runtime.

Responsibilities:
- Detect memory commands.
- Execute safe memory operations.
- Prepare destructive memory operations for confirmation.
- Execute confirmed memory deletion.
- Provide clean structured results for main_v7.py.
- Route memory searches through MemoryRetrieval.

This module does NOT:
- Modify main.py.
- Modify CommandRouter.
- Call Ollama.
- Perform speech recognition.
- Perform text-to-speech.
- Automatically save normal conversations.
"""

from __future__ import annotations

from typing import Any

from memory.memory_commands import MemoryCommandLayer
from memory.memory_manager import MemoryManager
from memory.memory_retrieval import MemoryRetrieval
from memory.memory_context import MemoryContext


class MemoryController:
    """V7 integration controller for persistent JARVIS memory."""

    def __init__(
        self,
        manager: MemoryManager | None = None,
        commands: MemoryCommandLayer | None = None,
        retrieval: MemoryRetrieval | None = None,
        context: MemoryContext | None = None,
    ) -> None:
        """Initialize the V7 memory controller."""

        self.manager = manager or MemoryManager()

        self.commands = (
            commands
            or MemoryCommandLayer(
                manager=self.manager
            )
        )

        self.retrieval = (
            retrieval
            or MemoryRetrieval(
                search=self.commands.search
            )
        )

        self.context = (
            context
            or MemoryContext(
                search=self.commands.search
            )
        )

        # Pending destructive operation.
        self.pending_delete_id: int | None = None

    # ------------------------------------------------------------------
    # COMMAND DETECTION
    # ------------------------------------------------------------------

    @staticmethod
    def is_memory_command(command: str) -> bool:
        """Return True when a command belongs to the memory system."""

        return MemoryCommandLayer.is_memory_command(command)

    # ------------------------------------------------------------------
    # PENDING STATE
    # ------------------------------------------------------------------

    def has_pending_confirmation(self) -> bool:
        """Return True when a memory deletion is awaiting confirmation."""

        return self.pending_delete_id is not None

    def clear_pending_confirmation(self) -> None:
        """Clear any pending destructive memory operation."""

        self.pending_delete_id = None

    # ------------------------------------------------------------------
    # DELETE PREPARATION
    # ------------------------------------------------------------------

    def _prepare_delete(
        self,
        command: str,
    ) -> dict[str, Any]:
        """
        Prepare a memory deletion without executing it.

        The existing V7.4 command layer performs deletion immediately.
        V7.8 intentionally intercepts the operation before calling it.
        """

        normalized = " ".join(
            command.strip().split()
        )

        patterns = self.commands.FORGET_PATTERNS

        memory_id: int | None = None

        for pattern in patterns:
            import re

            match = re.match(
                pattern,
                normalized.lower(),
                re.IGNORECASE,
            )

            if match:
                memory_id = int(match.group(1))
                break

        if memory_id is None:
            return {
                "success": False,
                "action": "delete",
                "message": "Please specify the memory number.",
                "data": None,
                "requires_confirmation": False,
            }

        memory = self.manager.get_memory(memory_id)

        if memory is None:
            return {
                "success": False,
                "action": "delete",
                "message": (
                    f"Memory {memory_id} was not found."
                ),
                "data": {
                    "memory_id": memory_id,
                    "memory": None,
                },
                "requires_confirmation": False,
            }

        self.pending_delete_id = memory_id

        return {
            "success": True,
            "action": "delete_pending",
            "message": (
                f"Sir, memory {memory_id} is selected for deletion. "
                "Please confirm."
            ),
            "data": {
                "memory_id": memory_id,
                "memory": memory,
            },
            "requires_confirmation": True,
        }

    # ------------------------------------------------------------------
    # CONFIRM DELETE
    # ------------------------------------------------------------------

    def confirm_delete(self) -> dict[str, Any]:
        """Execute the pending memory deletion."""

        if self.pending_delete_id is None:
            return {
                "success": False,
                "action": "delete",
                "message": (
                    "There is no memory deletion awaiting confirmation."
                ),
                "data": None,
                "requires_confirmation": False,
            }

        memory_id = self.pending_delete_id

        self.pending_delete_id = None

        deleted = self.manager.delete_memory(
            memory_id
        )

        if deleted:
            return {
                "success": True,
                "action": "delete",
                "message": (
                    f"Memory {memory_id} deleted successfully."
                ),
                "data": {
                    "memory_id": memory_id,
                    "deleted": True,
                },
                "requires_confirmation": False,
            }

        return {
            "success": False,
            "action": "delete",
            "message": (
                f"Memory {memory_id} was not found."
            ),
            "data": {
                "memory_id": memory_id,
                "deleted": False,
            },
            "requires_confirmation": False,
        }

    # ------------------------------------------------------------------
    # CANCEL DELETE
    # ------------------------------------------------------------------

    def cancel_delete(self) -> dict[str, Any]:
        """Cancel the pending memory deletion."""

        if self.pending_delete_id is None:
            return {
                "success": False,
                "action": "delete_cancel",
                "message": (
                    "There is no memory deletion awaiting confirmation."
                ),
                "data": None,
                "requires_confirmation": False,
            }

        memory_id = self.pending_delete_id

        self.pending_delete_id = None

        return {
            "success": True,
            "action": "delete_cancel",
            "message": (
                f"Memory {memory_id} deletion cancelled."
            ),
            "data": {
                "memory_id": memory_id,
                "deleted": False,
            },
            "requires_confirmation": False,
        }

    # ------------------------------------------------------------------
    # NORMAL MEMORY COMMANDS
    # ------------------------------------------------------------------

    def execute(
        self,
        command: str,
    ) -> dict[str, Any]:
        """
        Execute a memory command.

        Delete operations are intercepted and placed into a
        confirmation state instead of being immediately executed.

        Search operations are routed through MemoryRetrieval so
        natural memory questions receive deterministic reranking.
        """

        if not isinstance(command, str):
            return {
                "success": False,
                "action": None,
                "message": "Memory command must be a string.",
                "data": None,
                "requires_confirmation": False,
            }

        normalized = " ".join(
            command.strip().split()
        )

        if not normalized:
            return {
                "success": False,
                "action": None,
                "message": "Memory command cannot be empty.",
                "data": None,
                "requires_confirmation": False,
            }

        action = self.commands.classify(
            normalized
        )

        if action is None:
            return {
                "success": False,
                "action": None,
                "message": "Not a memory command.",
                "data": None,
                "requires_confirmation": False,
            }

        # --------------------------------------------------------------
        # DESTRUCTIVE OPERATION
        # --------------------------------------------------------------

        if action == "delete":
            return self._prepare_delete(
                normalized
            )

        # --------------------------------------------------------------
        # MEMORY SEARCH
        # --------------------------------------------------------------

        if action == "search":
            query = self.commands._extract_search_query(
                normalized
            )

            if not query:
                return {
                    "success": False,
                    "action": "search",
                    "message": (
                        "Please specify what memory you want me to search for."
                    ),
                    "data": {
                        "query": "",
                        "memories": [],
                        "count": 0,
                    },
                    "requires_confirmation": False,
                }

            memories = self.retrieval.search(
                query,
                limit=5,
            )

            return {
                "success": True,
                "action": "search",
                "message": (
                    f"Found {len(memories)} matching memories."
                    if memories
                    else "No matching memories found."
                ),
                "data": {
                    "query": query,
                    "memories": memories,
                    "count": len(memories),
                },
                "requires_confirmation": False,
            }

        # --------------------------------------------------------------
        # ALL OTHER SAFE MEMORY OPERATIONS
        # --------------------------------------------------------------

        result = self.commands.execute(
            normalized
        )

        result.setdefault(
            "requires_confirmation",
            False,
        )

        return result

    # ------------------------------------------------------------------
    # ADVANCED RETRIEVAL
    # ------------------------------------------------------------------

    def search_relevant(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Return reranked memories relevant to a query."""

        return self.retrieval.search(
            query,
            limit=limit,
        )

    # ------------------------------------------------------------------
    # CONTEXT
    # ------------------------------------------------------------------

    def build_context(
        self,
        query: str,
        limit: int = 5,
    ) -> str:
        """Build temporary relevant-memory context."""

        return self.context.build_context(
            query,
            limit=limit,
        )

    def get_context_data(
        self,
        query: str,
        limit: int = 5,
    ) -> dict[str, Any]:
        """Return structured relevant-memory context."""

        return self.context.get_context_data(
            query,
            limit=limit,
        )

    # ------------------------------------------------------------------
    # MEMORY INFORMATION
    # ------------------------------------------------------------------

    def get_memory_count(self) -> int:
        """Return the total number of persistent memories."""

        return self.manager.count_memories()

    def get_memory(
        self,
        memory_id: int,
    ) -> dict[str, Any] | None:
        """Return one memory by ID."""

        return self.manager.get_memory(
            memory_id
        )