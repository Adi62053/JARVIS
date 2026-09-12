"""
JARVIS V7.5 - Memory Context

Builds relevant memory context for the current user query.

Responsibilities:
- Search stored memories.
- Filter weak or irrelevant results.
- Limit the amount of memory returned.
- Build a clean context string.
- Keep memory retrieval separate from Ollama and main.py.

This module does NOT:
- Call Ollama.
- Modify main.py.
- Modify CommandRouter.
- Perform speech recognition.
- Perform text-to-speech.
- Automatically save memories.
"""

from __future__ import annotations

from typing import Any

from memory.memory_search import MemorySearch


class MemoryContext:
    """Build relevant memory context for JARVIS."""

    DEFAULT_LIMIT = 5
    MAX_LIMIT = 10

    MIN_SCORE = 1

    def __init__(
        self,
        search: MemorySearch | None = None,
    ) -> None:
        """Initialize the memory context layer."""

        self.search = search or MemorySearch()

    # ------------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_query(query: str) -> str:
        """Validate and normalize a context query."""

        if not isinstance(query, str):
            raise TypeError(
                "Memory context query must be a string."
            )

        normalized = " ".join(query.strip().split())

        if not normalized:
            raise ValueError(
                "Memory context query cannot be empty."
            )

        return normalized

    @classmethod
    def _validate_limit(cls, limit: int) -> int:
        """Validate the requested result limit."""

        if not isinstance(limit, int):
            raise TypeError(
                "Memory context limit must be an integer."
            )

        if limit < 1:
            raise ValueError(
                "Memory context limit must be at least 1."
            )

        return min(limit, cls.MAX_LIMIT)

    # ------------------------------------------------------------------
    # MEMORY RETRIEVAL
    # ------------------------------------------------------------------

    def get_relevant_memories(
        self,
        query: str,
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict[str, Any]]:
        """
        Return memories relevant to the supplied query.

        The existing V7.3 MemorySearch engine performs the actual
        matching and scoring.
        """

        normalized_query = self._validate_query(query)
        validated_limit = self._validate_limit(limit)

        results = self.search.search_content(
            normalized_query,
            limit=validated_limit,
        )

        return [
            memory
            for memory in results
            if memory.get("score", 0) >= self.MIN_SCORE
        ]

    # ------------------------------------------------------------------
    # CONTEXT BUILDING
    # ------------------------------------------------------------------

    def build_context(
        self,
        query: str,
        limit: int = DEFAULT_LIMIT,
    ) -> str:
        """
        Build a clean text context from relevant memories.

        Example output:

            Relevant memories:
            - I prefer Python.
            - JARVIS uses Ollama.
        """

        memories = self.get_relevant_memories(
            query,
            limit=limit,
        )

        if not memories:
            return ""

        lines = ["Relevant memories:"]

        for memory in memories:
            content = str(
                memory.get("content", "")
            ).strip()

            if not content:
                continue

            lines.append(
                f"- {content}"
            )

        if len(lines) == 1:
            return ""

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # STRUCTURED CONTEXT
    # ------------------------------------------------------------------

    def get_context_data(
        self,
        query: str,
        limit: int = DEFAULT_LIMIT,
    ) -> dict[str, Any]:
        """
        Return structured context information.

        This is useful for future integration with Ollama,
        logging, testing, and debugging.
        """

        normalized_query = self._validate_query(query)
        memories = self.get_relevant_memories(
            normalized_query,
            limit=limit,
        )

        context = self.build_context(
            normalized_query,
            limit=limit,
        )

        return {
            "query": normalized_query,
            "count": len(memories),
            "memories": memories,
            "context": context,
        }

    # ------------------------------------------------------------------
    # CONTEXT AVAILABILITY
    # ------------------------------------------------------------------

    def has_relevant_memory(
        self,
        query: str,
    ) -> bool:
        """Return True if relevant memory exists."""

        return bool(
            self.get_relevant_memories(
                query,
                limit=1,
            )
        )