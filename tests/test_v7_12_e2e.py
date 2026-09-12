"""
JARVIS V7.12 - End-to-End Memory Test

Tests the complete persistent-memory lifecycle through MemoryController:

1. Save memory
2. Retrieve/search memory
3. Update memory
4. Verify updated memory
5. Request deletion
6. Verify deletion requires confirmation
7. Cancel deletion
8. Verify memory still exists
9. Request deletion again
10. Confirm deletion
11. Verify memory is removed
12. Verify pending confirmation state is cleared

The test uses a temporary SQLite database and never touches
the real JARVIS memory database.
"""

from __future__ import annotations

from pathlib import Path

from memory.memory_controller import MemoryController
from memory.memory_manager import MemoryManager
from memory.memory_store import MemoryStore


def test_v7_12_complete_memory_lifecycle(tmp_path: Path) -> None:
    """Verify the complete V7 memory lifecycle through the controller."""

    # --------------------------------------------------------------
    # ISOLATED TEST DATABASE
    # --------------------------------------------------------------

    database_path = tmp_path / "jarvis_memory_test.db"

    store = MemoryStore(
        database_path=database_path
    )

    manager = MemoryManager(
        store=store
    )

    controller = MemoryController(
        manager=manager
    )

    # --------------------------------------------------------------
    # INITIAL STATE
    # --------------------------------------------------------------

    assert store.database_exists()
    assert store.table_exists()
    assert controller.get_memory_count() == 0
    assert not controller.has_pending_confirmation()

    # --------------------------------------------------------------
    # 1. SAVE MEMORY
    # --------------------------------------------------------------

    save_result = controller.execute(
        "always remember that my favourite programming language is Python"
    )

    assert save_result["success"] is True
    assert save_result["action"] == "save"
    assert save_result["requires_confirmation"] is False

    saved_memory = save_result["data"]

    assert saved_memory is not None
    assert saved_memory["content"] == (
        "my favourite programming language is Python"
    )

    memory_id = saved_memory["id"]

    assert isinstance(memory_id, int)
    assert controller.get_memory_count() == 1

    # --------------------------------------------------------------
    # 2. RETRIEVE MEMORY
    # --------------------------------------------------------------

    retrieve_result = controller.execute(
        "what is my favourite programming language"
    )

    assert retrieve_result["success"] is True
    assert retrieve_result["action"] == "search"

    search_data = retrieve_result["data"]

    assert search_data is not None
    assert search_data["count"] >= 1

    memories = search_data["memories"]

    assert memories
    assert memories[0]["id"] == memory_id
    assert memories[0]["content"] == (
        "my favourite programming language is Python"
    )

    # --------------------------------------------------------------
    # 3. DIRECT RETRIEVAL CHECK
    # --------------------------------------------------------------

    retrieved_memory = controller.get_memory(
        memory_id
    )

    assert retrieved_memory is not None
    assert retrieved_memory["id"] == memory_id
    assert retrieved_memory["content"] == (
        "my favourite programming language is Python"
    )

    # --------------------------------------------------------------
    # 4. UPDATE MEMORY
    # --------------------------------------------------------------

    update_result = controller.execute(
        f"update memory {memory_id} to "
        "my favourite programming language is Java"
    )

    assert update_result["success"] is True
    assert update_result["action"] == "update"
    assert update_result["requires_confirmation"] is False

    updated_memory = update_result["data"]

    assert updated_memory is not None
    assert updated_memory["id"] == memory_id
    assert updated_memory["content"] == (
        "my favourite programming language is Java"
    )

    # --------------------------------------------------------------
    # 5. VERIFY UPDATED MEMORY
    # --------------------------------------------------------------

    updated_retrieval = controller.execute(
        "what is my favourite programming language"
    )

    assert updated_retrieval["success"] is True

    updated_memories = (
        updated_retrieval["data"]["memories"]
    )

    assert updated_memories
    assert updated_memories[0]["id"] == memory_id
    assert updated_memories[0]["content"] == (
        "my favourite programming language is Java"
    )

    # --------------------------------------------------------------
    # 6. REQUEST DELETION
    # --------------------------------------------------------------

    delete_request = controller.execute(
        f"delete memory {memory_id}"
    )

    assert delete_request["success"] is True
    assert delete_request["action"] == "delete_pending"
    assert delete_request["requires_confirmation"] is True

    assert controller.has_pending_confirmation()
    assert controller.pending_delete_id == memory_id

    # The memory must still exist because deletion has not
    # been confirmed yet.
    assert controller.get_memory(memory_id) is not None

    # --------------------------------------------------------------
    # 7. CANCEL DELETION
    # --------------------------------------------------------------

    cancel_result = controller.cancel_delete()

    assert cancel_result["success"] is True
    assert cancel_result["action"] == "delete_cancel"
    assert cancel_result["requires_confirmation"] is False

    assert not controller.has_pending_confirmation()
    assert controller.pending_delete_id is None

    # --------------------------------------------------------------
    # 8. VERIFY MEMORY STILL EXISTS
    # --------------------------------------------------------------

    memory_after_cancel = controller.get_memory(
        memory_id
    )

    assert memory_after_cancel is not None
    assert memory_after_cancel["content"] == (
        "my favourite programming language is Java"
    )

    assert controller.get_memory_count() == 1

    # --------------------------------------------------------------
    # 9. REQUEST DELETION AGAIN
    # --------------------------------------------------------------

    second_delete_request = controller.execute(
        f"delete memory number {memory_id}"
    )

    assert second_delete_request["success"] is True
    assert second_delete_request["action"] == "delete_pending"
    assert second_delete_request["requires_confirmation"] is True

    assert controller.has_pending_confirmation()
    assert controller.pending_delete_id == memory_id

    # --------------------------------------------------------------
    # 10. CONFIRM DELETION
    # --------------------------------------------------------------

    confirm_result = controller.confirm_delete()

    assert confirm_result["success"] is True
    assert confirm_result["action"] == "delete"
    assert confirm_result["requires_confirmation"] is False

    assert confirm_result["data"]["memory_id"] == memory_id
    assert confirm_result["data"]["deleted"] is True

    # --------------------------------------------------------------
    # 11. VERIFY DELETION
    # --------------------------------------------------------------

    assert not controller.has_pending_confirmation()
    assert controller.pending_delete_id is None

    assert controller.get_memory(memory_id) is None
    assert controller.get_memory_count() == 0

    # --------------------------------------------------------------
    # 12. VERIFY SEARCH NO LONGER FINDS MEMORY
    # --------------------------------------------------------------

    final_search = controller.execute(
        "what is my favourite programming language"
    )

    assert final_search["success"] is True
    assert final_search["action"] == "search"

    final_memories = final_search["data"]["memories"]

    assert all(
        memory["id"] != memory_id
        for memory in final_memories
    )