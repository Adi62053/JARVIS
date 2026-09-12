"""
JARVIS V7.6 - Real Ollama Memory E2E Test

Tests the complete local chain:

SQLite Memory
    ->
Memory Search
    ->
Memory Context
    ->
MemoryOllama
    ->
Ollama llama3.2:3b

This test requires:
- Ollama to be running
- llama3.2:3b to be installed locally

The test uses a temporary database so the real JARVIS
memory database is NOT modified.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from memory.memory_context import MemoryContext
from memory.memory_manager import MemoryManager
from memory.memory_ollama import MemoryOllama
from memory.memory_search import MemorySearch
from memory.memory_store import MemoryStore


def create_test_system() -> tuple[
    MemoryOllama,
    MemoryManager,
    tempfile.TemporaryDirectory,
]:
    """Create an isolated memory/Ollama system."""

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

    context = MemoryContext(
        search
    )

    ollama = MemoryOllama(
        memory_context=context,
        host="http://127.0.0.1:11434",
        model="llama3.2:3b",
    )

    return (
        ollama,
        manager,
        temp_dir,
    )


@pytest.fixture
def ollama() -> tuple[MemoryOllama, tempfile.TemporaryDirectory]:
    """Provide an isolated Ollama memory system for pytest."""

    ollama_instance, _, temp_dir = create_test_system()

    yield ollama_instance, temp_dir

    temp_dir.cleanup()


@pytest.fixture
def memory_system() -> tuple[
    MemoryOllama,
    MemoryManager,
    tempfile.TemporaryDirectory,
]:
    """Provide the complete isolated memory/Ollama system."""

    ollama_instance, manager, temp_dir = create_test_system()

    yield ollama_instance, manager, temp_dir

    temp_dir.cleanup()


def test_ollama_available(
    ollama: tuple[
        MemoryOllama,
        tempfile.TemporaryDirectory,
    ],
) -> None:
    """Verify the local Ollama service is reachable."""

    ollama_instance, _ = ollama

    print("[TEST] Checking Ollama service...")

    if not ollama_instance.is_available():
        raise RuntimeError(
            "Ollama is not reachable at "
            "http://127.0.0.1:11434"
        )

    print("[PASS] Ollama service is available")


def test_model_memory_response(
    memory_system: tuple[
        MemoryOllama,
        MemoryManager,
        tempfile.TemporaryDirectory,
    ],
) -> None:
    """
    Verify that Ollama receives and uses relevant memory context.
    """

    ollama, manager, _ = memory_system

    print(
        "[TEST] Testing memory-aware Ollama response..."
    )

    manager.save_memory(
        "My preferred programming language is Python.",
        category="preference",
    )

    manager.save_memory(
        "JARVIS uses the local Ollama llama3.2:3b model.",
        category="project",
    )

    result = ollama.respond(
        "What programming language do I prefer?"
    )

    assert result["success"] is True

    assert result["model"] == "llama3.2:3b"

    assert isinstance(
        result["memory_context"],
        str,
    )

    assert (
        "Python"
        in result["memory_context"]
    )

    assert isinstance(
        result["prompt"],
        str,
    )

    assert (
        "My preferred programming language is Python."
        in result["prompt"]
    )

    response = result["response"]

    assert isinstance(
        response,
        str,
    )

    assert response.strip()

    print("[PASS] Memory context reached Ollama")
    print("[PASS] Ollama returned a response")
    print()
    print("[OLLAMA RESPONSE]")
    print(response)


def test_no_memory_does_not_fail(
    ollama: tuple[
        MemoryOllama,
        tempfile.TemporaryDirectory,
    ],
) -> None:
    """
    Verify that Ollama can answer when no relevant memory exists.
    """

    ollama_instance, _ = ollama

    print()
    print(
        "[TEST] Testing Ollama without relevant memory..."
    )

    result = ollama_instance.respond(
        "What is the Python programming language?"
    )

    assert result["success"] is True

    assert isinstance(
        result["response"],
        str,
    )

    assert result["response"].strip()

    print(
        "[PASS] Ollama responds without relevant memory"
    )


def run_tests() -> None:
    """Run the complete V7.6 real Ollama E2E test."""

    print(
        "[V7.6] REAL OLLAMA MEMORY E2E TEST"
    )
    print()
    print(
        "Model: llama3.2:3b"
    )
    print(
        "Host: http://127.0.0.1:11434"
    )
    print()

    ollama, manager, temp_dir = (
        create_test_system()
    )

    try:
        test_ollama_available(
            (ollama, temp_dir)
        )

        test_model_memory_response(
            (ollama, manager, temp_dir)
        )

        test_no_memory_does_not_fail(
            (ollama, temp_dir)
        )

        print()
        print(
            "[V7.6] REAL OLLAMA MEMORY E2E TEST PASSED"
        )

    finally:
        temp_dir.cleanup()


if __name__ == "__main__":
    run_tests()

