"""
JARVIS V7.2 - Memory Manager

Provides high-level CRUD operations for persistent JARVIS memories.

Responsibilities:
- Save memories.
- Retrieve memories.
- List memories.
- Update memories.
- Delete memories.
- Count memories.
- Validate memory input.

Database connection and schema management remain the responsibility
of memory.memory_store.MemoryStore.
"""

from __future__ import annotations

from typing import Any

from memory.memory_store import MemoryStore


class MemoryManager:
    """High-level manager for JARVIS persistent memories."""

    VALID_CATEGORIES = {
        "preference",
        "project",
        "fact",
        "instruction",
        "person",
        "system",
        "general",
    }

    def __init__(self, store: MemoryStore | None = None) -> None:
        """
        Initialize the memory manager.

        Args:
            store:
                Optional MemoryStore instance. A default store is created
                when one is not supplied.
        """
        self.store = store or MemoryStore()
        self.store.initialize()

    @staticmethod
    def _validate_content(content: str) -> str:
        """Validate and normalize memory content."""
        if not isinstance(content, str):
            raise TypeError("Memory content must be a string.")

        normalized = content.strip()

        if not normalized:
            raise ValueError("Memory content cannot be empty.")

        return normalized

    @staticmethod
    def _validate_category(category: str) -> str:
        """Validate and normalize a memory category."""
        if not isinstance(category, str):
            raise TypeError("Memory category must be a string.")

        normalized = category.strip().lower()

        if not normalized:
            raise ValueError("Memory category cannot be empty.")

        return normalized

    @staticmethod
    def _row_to_dict(row: Any) -> dict[str, Any] | None:
        """Convert a SQLite row into a normal dictionary."""
        if row is None:
            return None

        return dict(row)

    def save_memory(
        self,
        content: str,
        category: str = "general",
    ) -> dict[str, Any]:
        """
        Save a new persistent memory.

        Returns:
            The newly created memory as a dictionary.
        """
        normalized_content = self._validate_content(content)
        normalized_category = self._validate_category(category)

        with self.store.get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO memories (category, content)
                VALUES (?, ?)
                """,
                (
                    normalized_category,
                    normalized_content,
                ),
            )

            memory_id = cursor.lastrowid

            connection.commit()

            row = connection.execute(
                """
                SELECT id, category, content, created_at, updated_at
                FROM memories
                WHERE id = ?
                """,
                (memory_id,),
            ).fetchone()

        result = self._row_to_dict(row)

        if result is None:
            raise RuntimeError("Memory was created but could not be retrieved.")

        return result

    def get_memory(self, memory_id: int) -> dict[str, Any] | None:
        """
        Retrieve one memory by ID.

        Returns:
            Memory dictionary or None if the memory does not exist.
        """
        if not isinstance(memory_id, int):
            raise TypeError("Memory ID must be an integer.")

        with self.store.get_connection() as connection:
            row = connection.execute(
                """
                SELECT id, category, content, created_at, updated_at
                FROM memories
                WHERE id = ?
                """,
                (memory_id,),
            ).fetchone()

        return self._row_to_dict(row)

    def get_all_memories(self) -> list[dict[str, Any]]:
        """Return all stored memories ordered by ID."""
        with self.store.get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, category, content, created_at, updated_at
                FROM memories
                ORDER BY id ASC
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def update_memory(
        self,
        memory_id: int,
        content: str | None = None,
        category: str | None = None,
    ) -> dict[str, Any] | None:
        """
        Update an existing memory.

        Args:
            memory_id:
                ID of the memory to update.
            content:
                New content. If None, existing content is preserved.
            category:
                New category. If None, existing category is preserved.

        Returns:
            Updated memory dictionary or None if not found.
        """
        if not isinstance(memory_id, int):
            raise TypeError("Memory ID must be an integer.")

        if content is None and category is None:
            raise ValueError(
                "At least content or category must be provided."
            )

        if content is not None:
            content = self._validate_content(content)

        if category is not None:
            category = self._validate_category(category)

        existing = self.get_memory(memory_id)

        if existing is None:
            return None

        new_content = (
            content
            if content is not None
            else existing["content"]
        )

        new_category = (
            category
            if category is not None
            else existing["category"]
        )

        with self.store.get_connection() as connection:
            connection.execute(
                """
                UPDATE memories
                SET category = ?,
                    content = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    new_category,
                    new_content,
                    memory_id,
                ),
            )

            connection.commit()

        return self.get_memory(memory_id)

    def delete_memory(self, memory_id: int) -> bool:
        """
        Delete a memory by ID.

        Returns:
            True if a memory was deleted, otherwise False.
        """
        if not isinstance(memory_id, int):
            raise TypeError("Memory ID must be an integer.")

        with self.store.get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM memories
                WHERE id = ?
                """,
                (memory_id,),
            )

            connection.commit()

        return cursor.rowcount > 0

    def count_memories(self) -> int:
        """Return the total number of stored memories."""
        with self.store.get_connection() as connection:
            row = connection.execute(
                """
                SELECT COUNT(*) AS memory_count
                FROM memories
                """
            ).fetchone()

        if row is None:
            return 0

        return int(row["memory_count"])