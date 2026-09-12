"""
JARVIS V7.5 - Memory Context Tests
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from memory.memory_context import MemoryContext
from memory.memory_manager import MemoryManager
from memory.memory_search import MemorySearch
from memory.memory_store import MemoryStore


def create_context() -> tuple[
    MemoryContext,
    MemoryManager,
    tempfile.TemporaryDirectory,
]:
    """Create an isolated memory context using a temporary DB."""

    temp_dir = tempfile.TemporaryDirectory()

    database_path = Path(
        temp_dir.name
    ) / "test_memory.db"

    store = MemoryStore(database_path)

    manager = MemoryManager(store)
    search = MemorySearch(store)
    context = MemoryContext(search)

    return context, manager, temp_dir


def test_relevant_memory() -> None:
    """Verify relevant memories are returned."""

    context, manager, temp_dir = create_context()

    manager.save_memory(
        "I prefer Python",
        category="preference",
    )

    manager.save_memory(
        "JARVIS uses Ollama",
        category="project",
    )

    results = context.get_relevant_memories(
        "Python"
    )

    assert len(results) >= 1
    assert any(
        "Python" in item["content"]
        for item in results
    )

    temp_dir.cleanup()


def test_irrelevant_memory_filtered() -> None:
    """Verify unrelated memories are not returned."""

    context, manager, temp_dir = create_context()

    manager.save_memory(
        "I prefer Python",
        category="preference",
    )

    manager.save_memory(
        "JARVIS uses Ollama",
        category="project",
    )

    results = context.get_relevant_memories(
        "Python"
    )

    assert all(
        "Python" in item["content"]
        for item in results
    )

    temp_dir.cleanup()


def test_context_string() -> None:
    """Verify clean context text is generated."""

    context, manager, temp_dir = create_context()

    manager.save_memory(
        "I prefer Python",
        category="preference",
    )

    result = context.build_context(
        "Python"
    )

    assert "Relevant memories:" in result
    assert "I prefer Python" in result

    temp_dir.cleanup()


def test_empty_context() -> None:
    """Verify no-match queries return empty context."""

    context, manager, temp_dir = create_context()

    manager.save_memory(
        "I prefer Python",
        category="preference",
    )

    result = context.build_context(
        "JavaScript"
    )

    assert result == ""

    temp_dir.cleanup()


def test_context_data() -> None:
    """Verify structured context data."""

    context, manager, temp_dir = create_context()

    manager.save_memory(
        "I prefer Python",
        category="preference",
    )

    data = context.get_context_data(
        "Python"
    )

    assert data["query"] == "Python"
    assert data["count"] >= 1
    assert isinstance(data["memories"], list)
    assert isinstance(data["context"], str)
    assert "Python" in data["context"]

    temp_dir.cleanup()


def test_has_relevant_memory() -> None:
    """Verify relevance detection."""

    context, manager, temp_dir = create_context()

    manager.save_memory(
        "I prefer Python",
        category="preference",
    )

    assert context.has_relevant_memory(
        "Python"
    )

    assert not context.has_relevant_memory(
        "JavaScript"
    )

    temp_dir.cleanup()


def test_result_limit() -> None:
    """Verify context result limits."""

    context, manager, temp_dir = create_context()

    manager.save_memory(
        "Python is my preferred language",
        category="preference",
    )

    manager.save_memory(
        "I use Python for JARVIS",
        category="project",
    )

    manager.save_memory(
        "Python is installed on my system",
        category="fact",
    )

    results = context.get_relevant_memories(
        "Python",
        limit=2,
    )

    assert len(results) <= 2

    temp_dir.cleanup()


def test_empty_query_rejected() -> None:
    """Verify empty queries are rejected."""

    context, manager, temp_dir = create_context()

    try:
        context.get_relevant_memories("")
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty query should raise ValueError."
        )

    temp_dir.cleanup()


def test_invalid_query_type_rejected() -> None:
    """Verify invalid query types are rejected."""

    context, manager, temp_dir = create_context()

    try:
        context.get_relevant_memories(123)
    except TypeError:
        pass
    else:
        raise AssertionError(
            "Invalid query type should raise TypeError."
        )

    temp_dir.cleanup()


def run_tests() -> None:
    """Run all V7.5 tests."""

    print("[V7.5] Memory Context Tests")
    print()

    test_relevant_memory()
    print("[PASS] Relevant memory retrieval")

    test_irrelevant_memory_filtered()
    print("[PASS] Irrelevant memory filtering")

    test_context_string()
    print("[PASS] Context string generation")

    test_empty_context()
    print("[PASS] Empty context")

    test_context_data()
    print("[PASS] Structured context data")

    test_has_relevant_memory()
    print("[PASS] Relevant memory detection")

    test_result_limit()
    print("[PASS] Result limit")

    test_empty_query_rejected()
    print("[PASS] Empty query rejection")

    test_invalid_query_type_rejected()
    print("[PASS] Invalid query type rejection")

    print()
    print("[V7.5] ALL MEMORY CONTEXT TESTS PASSED")


if __name__ == "__main__":
    run_tests()