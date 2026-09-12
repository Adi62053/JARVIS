"""
JARVIS V7.2 - Memory Manager Tests

Tests CRUD operations and validation for persistent JARVIS memory.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from memory.memory_manager import MemoryManager
from memory.memory_store import MemoryStore


def create_test_manager() -> MemoryManager:
    """Create a MemoryManager backed by a temporary database."""
    temp_dir = tempfile.TemporaryDirectory()

    # Store the temporary directory on the manager so its lifetime
    # extends until the test manager is no longer needed.
    database_path = Path(temp_dir.name) / "test_memory.db"

    store = MemoryStore(database_path)

    manager = MemoryManager(store)

    manager._test_temp_dir = temp_dir

    return manager


def test_save_memory() -> None:
    """Verify that a memory can be created."""

    manager = create_test_manager()

    memory = manager.save_memory(
        "JARVIS V7 memory test",
        "project",
    )

    assert memory["id"] > 0
    assert memory["category"] == "project"
    assert memory["content"] == "JARVIS V7 memory test"
    assert memory["created_at"]
    assert memory["updated_at"]

    assert manager.count_memories() == 1

    manager._test_temp_dir.cleanup()


def test_get_memory() -> None:
    """Verify retrieval of a memory by ID."""

    manager = create_test_manager()

    created = manager.save_memory(
        "Retrieve this memory",
        "fact",
    )

    retrieved = manager.get_memory(created["id"])

    assert retrieved is not None
    assert retrieved["id"] == created["id"]
    assert retrieved["content"] == "Retrieve this memory"
    assert retrieved["category"] == "fact"

    manager._test_temp_dir.cleanup()


def test_get_all_memories() -> None:
    """Verify retrieval of all memories."""

    manager = create_test_manager()

    manager.save_memory("Memory one", "general")
    manager.save_memory("Memory two", "project")
    manager.save_memory("Memory three", "preference")

    memories = manager.get_all_memories()

    assert len(memories) == 3
    assert memories[0]["content"] == "Memory one"
    assert memories[1]["content"] == "Memory two"
    assert memories[2]["content"] == "Memory three"

    manager._test_temp_dir.cleanup()


def test_update_memory() -> None:
    """Verify that an existing memory can be updated."""

    manager = create_test_manager()

    created = manager.save_memory(
        "Original memory",
        "general",
    )

    updated = manager.update_memory(
        created["id"],
        content="Updated memory",
        category="project",
    )

    assert updated is not None
    assert updated["id"] == created["id"]
    assert updated["content"] == "Updated memory"
    assert updated["category"] == "project"

    manager._test_temp_dir.cleanup()


def test_delete_memory() -> None:
    """Verify that a memory can be deleted."""

    manager = create_test_manager()

    created = manager.save_memory(
        "Delete this memory",
        "general",
    )

    assert manager.delete_memory(created["id"]) is True
    assert manager.get_memory(created["id"]) is None
    assert manager.count_memories() == 0

    manager._test_temp_dir.cleanup()


def test_delete_nonexistent_memory() -> None:
    """Verify deletion of a nonexistent memory."""

    manager = create_test_manager()

    assert manager.delete_memory(999999) is False

    manager._test_temp_dir.cleanup()


def test_empty_content_rejected() -> None:
    """Verify that empty memory content is rejected."""

    manager = create_test_manager()

    try:
        manager.save_memory("   ")
        raise AssertionError("Empty memory was accepted.")
    except ValueError:
        pass

    manager._test_temp_dir.cleanup()


def test_invalid_content_type_rejected() -> None:
    """Verify that non-string content is rejected."""

    manager = create_test_manager()

    try:
        manager.save_memory(123)  # type: ignore[arg-type]
        raise AssertionError("Invalid content type was accepted.")
    except TypeError:
        pass

    manager._test_temp_dir.cleanup()


def test_update_requires_changes() -> None:
    """Verify that an empty update request is rejected."""

    manager = create_test_manager()

    created = manager.save_memory(
        "Existing memory",
        "general",
    )

    try:
        manager.update_memory(created["id"])
        raise AssertionError("Empty update was accepted.")
    except ValueError:
        pass

    manager._test_temp_dir.cleanup()


def run_tests() -> None:
    """Run all V7.2 memory manager tests."""

    print("[V7.2] Memory Manager Tests")
    print()

    test_save_memory()
    print("[PASS] Save memory")

    test_get_memory()
    print("[PASS] Get memory")

    test_get_all_memories()
    print("[PASS] Get all memories")

    test_update_memory()
    print("[PASS] Update memory")

    test_delete_memory()
    print("[PASS] Delete memory")

    test_delete_nonexistent_memory()
    print("[PASS] Delete nonexistent memory")

    test_empty_content_rejected()
    print("[PASS] Empty content rejected")

    test_invalid_content_type_rejected()
    print("[PASS] Invalid content type rejected")

    test_update_requires_changes()
    print("[PASS] Empty update rejected")

    print()
    print("[V7.2] ALL MEMORY MANAGER TESTS PASSED")


if __name__ == "__main__":
    run_tests()