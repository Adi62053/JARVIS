"""
JARVIS V7.6 - Ollama Memory Integration Tests

These tests verify the memory/Ollama integration layer without
requiring Ollama to be running.

Actual Ollama communication is tested separately.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from memory.memory_context import MemoryContext
from memory.memory_manager import MemoryManager
from memory.memory_ollama import MemoryOllama
from memory.memory_search import MemorySearch
from memory.memory_store import MemoryStore


def create_ollama() -> tuple[
    MemoryOllama,
    MemoryManager,
    tempfile.TemporaryDirectory,
]:
    """Create an isolated MemoryOllama instance."""

    temp_dir = tempfile.TemporaryDirectory()

    database_path = Path(
        temp_dir.name
    ) / "test_memory.db"

    store = MemoryStore(
        database_path
    )

    manager = MemoryManager(
        store
    )

    search = MemorySearch(
        store
    )

    context = MemoryContext(
        search
    )

    ollama = MemoryOllama(
        memory_context=context
    )

    return (
        ollama,
        manager,
        temp_dir,
    )


def test_memory_context_retrieval() -> None:
    """Verify Ollama integration can retrieve memory."""

    ollama, manager, temp_dir = create_ollama()

    manager.save_memory(
        "I prefer Python",
        category="preference",
    )

    context = ollama.get_memory_context(
        "What programming language do I prefer?"
    )

    assert "I prefer Python" in context

    temp_dir.cleanup()


def test_prompt_contains_memory() -> None:
    """Verify stored memory is inserted into the prompt."""

    ollama, manager, temp_dir = create_ollama()

    manager.save_memory(
        "I prefer Python",
        category="preference",
    )

    memory_context = ollama.get_memory_context(
        "Python"
    )

    prompt = ollama.build_prompt(
        "What language do I prefer?",
        memory_context,
    )

    assert "I prefer Python" in prompt
    assert "What language do I prefer?" in prompt
    assert "Stored memories" in prompt

    temp_dir.cleanup()


def test_prompt_without_memory() -> None:
    """Verify prompt generation without relevant memory."""

    ollama, manager, temp_dir = create_ollama()

    prompt = ollama.build_prompt(
        "What is Python?"
    )

    assert "What is Python?" in prompt
    assert "No relevant stored memory was found" in prompt

    temp_dir.cleanup()


def test_prompt_rejects_empty_query() -> None:
    """Verify empty user queries are rejected."""

    ollama, manager, temp_dir = create_ollama()

    try:
        ollama.build_prompt("")
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty query should raise ValueError."
        )

    temp_dir.cleanup()


def test_prompt_rejects_invalid_query_type() -> None:
    """Verify invalid query types are rejected."""

    ollama, manager, temp_dir = create_ollama()

    try:
        ollama.build_prompt(123)
    except TypeError:
        pass
    else:
        raise AssertionError(
            "Invalid query type should raise TypeError."
        )

    temp_dir.cleanup()


def test_custom_model() -> None:
    """Verify custom Ollama model configuration."""

    ollama, manager, temp_dir = create_ollama()

    custom = MemoryOllama(
        memory_context=ollama.memory_context,
        model="llama3.2:3b",
    )

    assert custom.model == "llama3.2:3b"

    temp_dir.cleanup()


def test_custom_host() -> None:
    """Verify custom Ollama host configuration."""

    ollama, manager, temp_dir = create_ollama()

    custom = MemoryOllama(
        memory_context=ollama.memory_context,
        host="http://localhost:11434/",
    )

    assert custom.host == (
        "http://localhost:11434"
    )

    temp_dir.cleanup()


def test_empty_model_rejected() -> None:
    """Verify empty model configuration is rejected."""

    ollama, manager, temp_dir = create_ollama()

    try:
        MemoryOllama(
            memory_context=ollama.memory_context,
            model="",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty model should raise ValueError."
        )

    temp_dir.cleanup()


def test_empty_host_rejected() -> None:
    """Verify empty host configuration is rejected."""

    ollama, manager, temp_dir = create_ollama()

    try:
        MemoryOllama(
            memory_context=ollama.memory_context,
            host="",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty host should raise ValueError."
        )

    temp_dir.cleanup()


def test_model_default() -> None:
    """Verify the JARVIS Ollama model."""

    ollama, manager, temp_dir = create_ollama()

    assert ollama.model == "llama3.2:3b"

    temp_dir.cleanup()


def run_tests() -> None:
    """Run all V7.6 integration tests."""

    print("[V7.6] Ollama Memory Integration Tests")
    print()

    test_memory_context_retrieval()
    print("[PASS] Memory context retrieval")

    test_prompt_contains_memory()
    print("[PASS] Memory inserted into prompt")

    test_prompt_without_memory()
    print("[PASS] Prompt without memory")

    test_prompt_rejects_empty_query()
    print("[PASS] Empty query rejection")

    test_prompt_rejects_invalid_query_type()
    print("[PASS] Invalid query type rejection")

    test_custom_model()
    print("[PASS] Custom model configuration")

    test_custom_host()
    print("[PASS] Custom host configuration")

    test_empty_model_rejected()
    print("[PASS] Empty model rejection")

    test_empty_host_rejected()
    print("[PASS] Empty host rejection")

    test_model_default()
    print("[PASS] Default model configuration")

    print()
    print(
        "[V7.6] ALL OLLAMA MEMORY INTEGRATION "
        "TESTS PASSED"
    )


if __name__ == "__main__":
    run_tests()