"""
JARVIS V7.1 - Memory Store

Provides the low-level SQLite storage layer for JARVIS persistent memory.

Responsibilities:
- Create/open the local SQLite database.
- Create the memories table.
- Provide safely managed database connections.
- Keep database initialization separate from higher-level memory logic.

This module intentionally does NOT:
- Interpret voice commands.
- Call Ollama.
- Search the web.
- Generate responses.
- Decide what JARVIS should remember.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Final, Iterator


class MemoryStore:
    """Low-level SQLite storage manager for JARVIS memory."""

    DATABASE_DIRECTORY: Final[Path] = (
        Path(__file__).resolve().parent / "data"
    )

    DATABASE_PATH: Final[Path] = (
        DATABASE_DIRECTORY / "jarvis_memory.db"
    )

    def __init__(self, database_path: Path | str | None = None) -> None:
        """
        Initialize the memory store.

        Args:
            database_path:
                Optional custom database path, primarily useful for testing.
                If omitted, the normal JARVIS memory database is used.
        """
        self.database_path = Path(
            database_path
            if database_path is not None
            else self.DATABASE_PATH
        )

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    @contextmanager
    def get_connection(self) -> Iterator[sqlite3.Connection]:
        """
        Provide a safely managed SQLite connection.

        The connection is automatically closed when the context exits.
        """
        connection = sqlite3.connect(str(self.database_path))

        connection.row_factory = sqlite3.Row

        try:
            yield connection
        finally:
            connection.close()

    def initialize(self) -> None:
        """Create the required memory database schema."""
        with self.get_connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.commit()

    def database_exists(self) -> bool:
        """Return True if the SQLite database file exists."""
        return self.database_path.exists()

    def table_exists(self) -> bool:
        """Return True if the memories table exists."""
        with self.get_connection() as connection:
            row = connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                  AND name = 'memories'
                """
            ).fetchone()

        return row is not None