"""
JARVIS V7.3 - Memory Search Tests

Tests local memory search and relevance ranking.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from memory.memory_manager import MemoryManager
from memory.memory_search import MemorySearch
from memory.memory_store import MemoryStore


def create_test_search() -> tuple[MemorySearch, tempfile.TemporaryDirectory]:
    """Create a search service using a temporary database."""
    temp_dir = tempfile.TemporaryDirectory()

    database_path = Path(temp_dir.name) / "test_memory.db"

    store = MemoryStore(database_path)

    manager = MemoryManager(store)

    manager.save_memory(
        "JARVIS uses Ollama as the local AI brain.",
        "project",
    )

    manager.save_memory(
        "Kokoro am_adam is the preferred JARVIS voice.",
        "preference",
    )

    manager.save_memory(
        "The JARVIS project is currently working on memory.",
        "project",
    )

    manager.save_memory(
        "VS Code is used for development.",
        "preference",
    )

    manager.save_memory(
        "Python is used for JARVIS development.",
        "fact",
    )

    search = MemorySearch(store)

    return search, temp_dir


def test_content_search() -> None:
    """Verify basic content searching."""
    search, temp_dir = create_test_search()

    results = search.search_content("Ollama")

    assert len(results) == 1
    assert "Ollama" in results[0]["content"]
    assert results[0]["score"] > 0

    temp_dir.cleanup()


def test_case_insensitive_search() -> None:
    """Verify search ignores letter case."""
    search, temp_dir = create_test_search()

    results = search.search_content("OLLAMA")

    assert len(results) == 1
    assert "Ollama" in results[0]["content"]

    temp_dir.cleanup()


def test_multi_word_search() -> None:
    """Verify multi-word searches return relevant memories."""
    search, temp_dir = create_test_search()

    results = search.search_content("JARVIS memory")

    assert len(results) >= 1

    contents = [
        result["content"]
        for result in results
    ]

    assert any(
        "JARVIS project is currently working on memory"
        in content
        for content in contents
    )

    temp_dir.cleanup()


def test_category_filter() -> None:
    """Verify category filtering."""
    search, temp_dir = create_test_search()

    results = search.search(
        query="JARVIS",
        category="project",
    )

    assert len(results) >= 1

    for result in results:
        assert result["category"] == "project"

    temp_dir.cleanup()


def test_relevance_score() -> None:
    """Verify that relevant results receive a positive score."""
    search, temp_dir = create_test_search()

    results = search.search_content("JARVIS")

    assert len(results) >= 1

    for result in results:
        assert result["score"] > 0

    temp_dir.cleanup()


def test_result_limit() -> None:
    """Verify result limits."""
    search, temp_dir = create_test_search()

    results = search.search_content(
        "JARVIS",
        limit=2,
    )

    assert len(results) <= 2

    temp_dir.cleanup()


def test_limit_is_capped() -> None:
    """Verify the maximum search limit."""
    search, temp_dir = create_test_search()

    results = search.search_content(
        "JARVIS",
        limit=1000,
    )

    assert len(results) <= MemorySearch.MAX_LIMIT

    temp_dir.cleanup()


def test_empty_query_rejected() -> None:
    """Verify empty queries are rejected."""
    search, temp_dir = create_test_search()

    try:
        search.search_content("   ")
        raise AssertionError("Empty query was accepted.")
    except ValueError:
        pass

    temp_dir.cleanup()


def test_invalid_query_type_rejected() -> None:
    """Verify invalid query types are rejected."""
    search, temp_dir = create_test_search()

    try:
        search.search_content(123)  # type: ignore[arg-type]
        raise AssertionError("Invalid query type was accepted.")
    except TypeError:
        pass

    temp_dir.cleanup()


def test_no_match() -> None:
    """Verify that an unmatched query returns no results."""
    search, temp_dir = create_test_search()

    results = search.search_content(
        "completely nonexistent information"
    )

    assert results == []

    temp_dir.cleanup()


def run_tests() -> None:
    """Run all V7.3 memory search tests."""

    print("[V7.3] Memory Search Tests")
    print()

    test_content_search()
    print("[PASS] Content search")

    test_case_insensitive_search()
    print("[PASS] Case-insensitive search")

    test_multi_word_search()
    print("[PASS] Multi-word search")

    test_category_filter()
    print("[PASS] Category filter")

    test_relevance_score()
    print("[PASS] Relevance scoring")

    test_result_limit()
    print("[PASS] Result limit")

    test_limit_is_capped()
    print("[PASS] Maximum limit")

    test_empty_query_rejected()
    print("[PASS] Empty query rejected")

    test_invalid_query_type_rejected()
    print("[PASS] Invalid query type rejected")

    test_no_match()
    print("[PASS] No-match search")

    print()
    print("[V7.3] ALL MEMORY SEARCH TESTS PASSED")


if __name__ == "__main__":
    run_tests()