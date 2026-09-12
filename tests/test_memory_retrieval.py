"""
JARVIS V7.7 - Advanced Memory Retrieval Tests
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from memory.memory_manager import MemoryManager
from memory.memory_retrieval import MemoryRetrieval
from memory.memory_search import MemorySearch
from memory.memory_store import MemoryStore


def create_retrieval() -> tuple[
    MemoryRetrieval,
    MemoryManager,
    tempfile.TemporaryDirectory,
]:
    """Create an isolated retrieval system."""

    temp_dir = tempfile.TemporaryDirectory()

    database_path = (
        Path(temp_dir.name)
        / "test_memory.db"
    )

    store = MemoryStore(
        database_path
    )

    manager = MemoryManager(
        store
    )

    search = MemorySearch(
        store
    )

    retrieval = MemoryRetrieval(
        search
    )

    return (
        retrieval,
        manager,
        temp_dir,
    )


def test_exact_phrase_bonus() -> None:
    """Verify exact phrase matches rank strongly."""

    retrieval, manager, temp_dir = (
        create_retrieval()
    )

    manager.save_memory(
        "I prefer Python programming.",
        category="preference",
    )

    manager.save_memory(
        "Python is installed on my computer.",
        category="fact",
    )

    results = retrieval.search_content(
        "I prefer Python programming"
    )

    assert results

    assert (
        results[0]["content"]
        == "I prefer Python programming."
    )

    assert (
        "retrieval_score"
        in results[0]
    )

    temp_dir.cleanup()


def test_meaningful_term_matching() -> None:
    """Verify meaningful terms contribute to ranking."""

    retrieval, manager, temp_dir = (
        create_retrieval()
    )

    manager.save_memory(
        "I use Python for JARVIS development.",
        category="project",
    )

    manager.save_memory(
        "JARVIS uses Ollama.",
        category="project",
    )

    results = retrieval.search(
        "Python JARVIS"
    )

    assert results

    assert (
        "Python"
        in results[0]["content"]
    )

    temp_dir.cleanup()


def test_category_relevance() -> None:
    """Verify category terms influence retrieval."""

    retrieval, manager, temp_dir = (
        create_retrieval()
    )

    manager.save_memory(
        "I use a local database.",
        category="project",
    )

    manager.save_memory(
        "SQLite is installed.",
        category="system",
    )

    results = retrieval.search(
        "project"
    )

    assert results

    assert (
        results[0]["category"]
        == "project"
    )

    temp_dir.cleanup()


def test_best_match() -> None:
    """Verify best_match returns one result."""

    retrieval, manager, temp_dir = (
        create_retrieval()
    )

    manager.save_memory(
        "My preferred language is Python.",
        category="preference",
    )

    result = retrieval.best_match(
        "preferred language Python"
    )

    assert result is not None
    assert (
        "Python"
        in result["content"]
    )

    temp_dir.cleanup()


def test_no_match() -> None:
    """Verify no-match queries return no result."""

    retrieval, manager, temp_dir = (
        create_retrieval()
    )

    manager.save_memory(
        "I prefer Python.",
        category="preference",
    )

    result = retrieval.best_match(
        "quantum physics"
    )

    assert result is None

    temp_dir.cleanup()


def test_result_limit() -> None:
    """Verify result limits."""

    retrieval, manager, temp_dir = (
        create_retrieval()
    )

    manager.save_memory(
        "Python is useful.",
        category="fact",
    )

    manager.save_memory(
        "Python is installed.",
        category="system",
    )

    manager.save_memory(
        "I use Python daily.",
        category="preference",
    )

    results = retrieval.search(
        "Python",
        limit=2,
    )

    assert len(results) <= 2

    temp_dir.cleanup()


def test_maximum_limit() -> None:
    """Verify excessive limits are capped."""

    retrieval, manager, temp_dir = (
        create_retrieval()
    )

    manager.save_memory(
        "Python is useful.",
        category="fact",
    )

    results = retrieval.search(
        "Python",
        limit=100,
    )

    assert len(results) <= (
        MemoryRetrieval.MAX_LIMIT
    )

    temp_dir.cleanup()


def test_empty_query_rejected() -> None:
    """Verify empty queries are rejected."""

    retrieval, manager, temp_dir = (
        create_retrieval()
    )

    try:
        retrieval.search("")
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty query should raise ValueError."
        )

    temp_dir.cleanup()


def test_invalid_query_type_rejected() -> None:
    """Verify invalid query types are rejected."""

    retrieval, manager, temp_dir = (
        create_retrieval()
    )

    try:
        retrieval.search(123)
    except TypeError:
        pass
    else:
        raise AssertionError(
            "Invalid query type should raise TypeError."
        )

    temp_dir.cleanup()


def test_deterministic_order() -> None:
    """Verify repeated searches return the same order."""

    retrieval, manager, temp_dir = (
        create_retrieval()
    )

    manager.save_memory(
        "Python project development.",
        category="project",
    )

    manager.save_memory(
        "Python personal preference.",
        category="preference",
    )

    first = retrieval.search(
        "Python"
    )

    second = retrieval.search(
        "Python"
    )

    assert [
        item["id"]
        for item in first
    ] == [
        item["id"]
        for item in second
    ]

    temp_dir.cleanup()


def run_tests() -> None:
    """Run all V7.7 tests."""

    print(
        "[V7.7] Advanced Memory Retrieval Tests"
    )
    print()

    test_exact_phrase_bonus()
    print("[PASS] Exact phrase ranking")

    test_meaningful_term_matching()
    print("[PASS] Meaningful term matching")

    test_category_relevance()
    print("[PASS] Category relevance")

    test_best_match()
    print("[PASS] Best memory match")

    test_no_match()
    print("[PASS] No-match handling")

    test_result_limit()
    print("[PASS] Result limit")

    test_maximum_limit()
    print("[PASS] Maximum limit")

    test_empty_query_rejected()
    print("[PASS] Empty query rejection")

    test_invalid_query_type_rejected()
    print("[PASS] Invalid query type rejection")

    test_deterministic_order()
    print("[PASS] Deterministic ordering")

    print()
    print(
        "[V7.7] ALL MEMORY RETRIEVAL TESTS PASSED"
    )


if __name__ == "__main__":
    run_tests()