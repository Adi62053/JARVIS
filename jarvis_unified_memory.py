"""
JARVIS Unified V7 Memory Layer

Extracted from jarvis_unified.py.

Preserves the existing V7 memory presentation and speech behavior.
"""

from __future__ import annotations

import re


def format_memory_for_speech(content: str) -> str:
    if not content:
        return "I found the memory, sir."

    content = content.strip()

    replacements = [
        (
            "my favourite programming language is ",
            "Your favourite programming language is ",
        ),
        (
            "my favorite programming language is ",
            "Your favorite programming language is ",
        ),
        (
            "my favourite language is ",
            "Your favourite language is ",
        ),
        (
            "my favorite language is ",
            "Your favorite language is ",
        ),
        (
            "my favourite dish is ",
            "Your favourite dish is ",
        ),
        (
            "my favorite dish is ",
            "Your favorite dish is ",
        ),
        (
            "my favourite fruit is ",
            "Your favourite fruit is ",
        ),
        (
            "my favorite fruit is ",
            "Your favorite fruit is ",
        ),
        (
            "my name is ",
            "Your name is ",
        ),
        (
            "my preferred ",
            "Your preferred ",
        ),
        (
            "i prefer ",
            "You prefer ",
        ),
        (
            "i like ",
            "You like ",
        ),
        (
            "i love ",
            "You love ",
        ),
    ]

    lowered = content.lower()

    for old_text, new_text in replacements:
        if lowered.startswith(old_text):
            content = (
                new_text
                + content[len(old_text):]
            )
            break

    if "programming language is python" in content.lower():
        content = re.sub(
            r"\bpython\b",
            "Python",
            content,
            flags=re.IGNORECASE,
        )

    content = content.rstrip(" .!?")

    return f"{content}, sir."


def handle_memory_result(result, speaker) -> None:
    if not result:
        return

    message = result.get(
        "message",
        "",
    )

    action = result.get(
        "action",
        "",
    )

    data = result.get(
        "data"
    )

    success = result.get(
        "success",
        False,
    )

    requires_confirmation = result.get(
        "requires_confirmation",
        False,
    )

    print("\nJARVIS V7 MEMORY:")

    if message:
        print(message)

    if action == "save" and isinstance(data, dict):
        print(f"Memory ID: {data.get('id')}")
        print(f"Category: {data.get('category')}")
        print(f"Content: {data.get('content')}")

    elif action == "search":
        memories = []

        if isinstance(data, dict):
            memories = data.get(
                "memories",
                [],
            )

        elif isinstance(data, list):
            memories = data

        if memories:
            print("\nMatching memories:")

            for memory in memories:
                memory_id = memory.get("id", "?")
                category = memory.get(
                    "category",
                    "general",
                )
                content = memory.get(
                    "content",
                    "",
                )
                score = memory.get(
                    "retrieval_score",
                    memory.get("score", ""),
                )

                if score != "":
                    print(
                        f"{memory_id}. "
                        f"[{category}] "
                        f"{content} "
                        f"(score: {score})"
                    )
                else:
                    print(
                        f"{memory_id}. "
                        f"[{category}] "
                        f"{content}"
                    )

            top_memory = memories[0]
            memory_content = top_memory.get(
                "content",
                "",
            )

            if memory_content:
                speaker.speak(
                    format_memory_for_speech(
                        memory_content
                    )
                )
            else:
                speaker.speak(
                    "I found the memory, sir."
                )

        else:
            print("No matching memories.")
            speaker.speak(
                "I don't have any matching memories, sir."
            )

        return

    elif action == "list" and isinstance(data, list):

        if data:
            print("\nStored memories:")

            for memory in data:
                print(
                    f"{memory.get('id', '?')}. "
                    f"[{memory.get('category', 'general')}] "
                    f"{memory.get('content', '')}"
                )

        else:
            print(
                "No memories are currently stored."
            )

    elif (
        action == "delete_pending"
        and isinstance(data, dict)
    ):
        memory_id = data.get(
            "memory_id",
            "?",
        )

        memory = data.get(
            "memory"
        )

        print(
            f"Pending deletion: Memory {memory_id}"
        )

        if isinstance(memory, dict):
            print(
                f"Category: "
                f"{memory.get('category', 'general')}"
            )

            print(
                f"Content: "
                f"{memory.get('content', '')}"
            )

        print(
            "Waiting for confirmation."
        )

    elif (
        action == "delete"
        and isinstance(data, dict)
    ):
        print(
            f"Memory ID: "
            f"{data.get('memory_id', '?')}"
        )

        print(
            f"Deleted: "
            f"{data.get('deleted', False)}"
        )

    elif (
        action == "update"
        and isinstance(data, dict)
    ):
        print(
            f"Memory ID: "
            f"{data.get('id', '?')}"
        )

        print(
            f"Category: "
            f"{data.get('category', 'general')}"
        )

        print(
            f"Content: "
            f"{data.get('content', '')}"
        )

    if requires_confirmation:
        speaker.speak(
            message
        )
        return

    if message:
        speaker.speak(
            message
        )

    elif success:
        speaker.speak(
            "Memory operation completed, sir."
        )

    else:
        speaker.speak(
            "The memory operation could not "
            "be completed, sir."
        )
