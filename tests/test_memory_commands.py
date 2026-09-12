"""
JARVIS V7.4 - Memory Command Tests
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from memory.memory_commands import MemoryCommandLayer
from memory.memory_manager import MemoryManager
from memory.memory_store import MemoryStore


def create_command_layer() -> tuple[
    MemoryCommandLayer,
    tempfile.TemporaryDirectory,
]:
    """Create a command layer using a temporary database."""
    temp_dir = tempfile.TemporaryDirectory()

    database_path = Path(temp_dir.name) / "test_memory.db"

    store = MemoryStore(database_path)
    manager = MemoryManager(store)

    return MemoryCommandLayer(manager), temp_dir


def test_save_command() -> None:
    """Verify natural-language memory saving."""
    layer, temp_dir = create_command_layer()

    result = layer.execute(
        "remember that I prefer Python"
    )

    assert result["success"] is True
    assert result["action"] == "save"
    assert result["data"]["content"] == (
        "I prefer Python"
    )
    assert result["data"]["category"] == "general"

    temp_dir.cleanup()


def test_categorized_save_command() -> None:
    """Verify categorized memory saving."""
    layer, temp_dir = create_command_layer()

    result = layer.execute(
        "remember this as preference: I prefer VS Code"
    )

    assert result["success"] is True
    assert result["data"]["category"] == "preference"
    assert result["data"]["content"] == (
        "I prefer VS Code"
    )

    temp_dir.cleanup()


def test_search_command() -> None:
    """Verify natural-language memory searching."""
    layer, temp_dir = create_command_layer()

    layer.execute(
        "remember that I prefer Python"
    )

    result = layer.execute(
        "what do you remember about Python"
    )

    assert result["success"] is True
    assert result["action"] == "search"
    assert len(result["data"]) == 1
    assert "Python" in result["data"][0]["content"]

    temp_dir.cleanup()


def test_list_command() -> None:
    """Verify listing memories."""
    layer, temp_dir = create_command_layer()

    layer.execute("remember that I use Python")
    layer.execute("remember that JARVIS uses Ollama")

    result = layer.execute("show my memories")

    assert result["success"] is True
    assert result["action"] == "list"
    assert len(result["data"]) == 2

    temp_dir.cleanup()


def test_delete_command() -> None:
    """Verify memory deletion."""
    layer, temp_dir = create_command_layer()

    saved = layer.execute(
        "remember that this should be deleted"
    )

    memory_id = saved["data"]["id"]

    result = layer.execute(
        f"forget memory number {memory_id}"
    )

    assert result["success"] is True
    assert result["action"] == "delete"
    assert result["data"]["deleted"] is True

    temp_dir.cleanup()


def test_update_command() -> None:
    """Verify memory updates."""
    layer, temp_dir = create_command_layer()

    saved = layer.execute(
        "remember that I use Python"
    )

    memory_id = saved["data"]["id"]

    result = layer.execute(
        f"update memory number {memory_id} "
        "to I use Python 3.12"
    )

    assert result["success"] is True
    assert result["action"] == "update"
    assert result["data"]["content"] == (
        "I use Python 3.12"
    )

    temp_dir.cleanup()


def test_non_memory_command() -> None:
    """Verify unrelated commands are rejected."""
    layer, temp_dir = create_command_layer()

    result = layer.execute("open Google")

    assert result["success"] is False
    assert result["action"] is None

    temp_dir.cleanup()


def test_is_memory_command() -> None:
    """Verify memory command detection."""
    assert MemoryCommandLayer.is_memory_command(
        "remember that I like Python"
    )

    assert MemoryCommandLayer.is_memory_command(
        "what do you remember about Python"
    )

    assert MemoryCommandLayer.is_memory_command(
        "show my memories"
    )

    assert not MemoryCommandLayer.is_memory_command(
        "open Google"
    )


def test_empty_remember_command() -> None:
    """Verify incomplete save commands are rejected."""
    layer, temp_dir = create_command_layer()

    result = layer.execute("remember")

    assert result["success"] is False
    assert result["action"] == "save"

    temp_dir.cleanup()


def test_empty_search_command() -> None:
    """Verify incomplete search commands are rejected."""
    layer, temp_dir = create_command_layer()

    result = layer.execute(
        "what do you remember about"
    )

    assert result["success"] is False
    assert result["action"] == "search"

    temp_dir.cleanup()


def run_tests() -> None:
    """Run all V7.4 tests."""

    print("[V7.4] Memory Command Tests")
    print()

    test_save_command()
    print("[PASS] Save command")

    test_categorized_save_command()
    print("[PASS] Categorized save")

    test_search_command()
    print("[PASS] Search command")

    test_list_command()
    print("[PASS] List command")

    test_delete_command()
    print("[PASS] Delete command")

    test_update_command()
    print("[PASS] Update command")

    test_non_memory_command()
    print("[PASS] Non-memory command detection")

    test_is_memory_command()
    print("[PASS] Memory command detection")

    test_empty_remember_command()
    print("[PASS] Empty remember command")

    test_empty_search_command()
    print("[PASS] Empty search command")

    print()
    print("[V7.4] ALL MEMORY COMMAND TESTS PASSED")


if __name__ == "__main__":
    run_tests()