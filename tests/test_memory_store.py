"""
JARVIS V7.1 - Memory Store Tests

Tests the low-level SQLite memory foundation.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from memory.memory_store import MemoryStore


def test_database_initialization() -> None:
    """Verify database and memories table creation."""

    with tempfile.TemporaryDirectory() as temp_dir:
        database_path = Path(temp_dir) / "test_memory.db"

        store = MemoryStore(database_path)

        assert not store.database_exists()

        store.initialize()

        assert store.database_exists()
        assert store.table_exists()


def test_database_persistence() -> None:
    """Verify that the database remains usable after reopening."""

    with tempfile.TemporaryDirectory() as temp_dir:
        database_path = Path(temp_dir) / "test_memory.db"

        first_store = MemoryStore(database_path)

        first_store.initialize()

        with first_store.get_connection() as connection:
            connection.execute(
                """
                INSERT INTO memories (category, content)
                VALUES (?, ?)
                """,
                (
                    "test",
                    "JARVIS V7 memory persistence test",
                ),
            )

            connection.commit()

        second_store = MemoryStore(database_path)

        assert second_store.database_exists()
        assert second_store.table_exists()

        with second_store.get_connection() as connection:
            row = connection.execute(
                """
                SELECT category, content
                FROM memories
                WHERE category = ?
                """,
                ("test",),
            ).fetchone()

        assert row is not None
        assert row["category"] == "test"
        assert row["content"] == "JARVIS V7 memory persistence test"


def run_tests() -> None:
    """Run V7.1 memory store tests."""

    print("[V7.1] Memory Store Tests")
    print()

    test_database_initialization()
    print("[PASS] Database initialization")

    test_database_persistence()
    print("[PASS] Database persistence")

    print()
    print("[V7.1] ALL MEMORY STORE TESTS PASSED")


if __name__ == "__main__":
    run_tests()