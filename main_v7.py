"""
JARVIS V7 - Main Runtime

V7 runtime integration layer.

Responsibilities:
- Preserve V3 laptop-control behavior.
- Preserve V4 filesystem behavior.
- Preserve V5 web behavior.
- Preserve V6 computer-vision behavior.
- Integrate V7.8 MemoryController.
- Handle safe memory operations.
- Handle memory deletion confirmation.
- Continue using Ollama for normal AI conversation.
- Preserve wake-word and Kokoro voice runtime.

Important V7 behavior:
- Explicit memory commands/questions -> MemoryController.
- V3/V4/V5/V6 commands -> appropriate tool.
- Everything else -> Ollama.
- Persistent memory is NOT searched automatically for
  every normal conversation.

This module does NOT:
- Modify main.py.
- Modify CommandRouter.
- Automatically save normal conversations.
- Automatically retrieve memories for normal conversation.
"""

from __future__ import annotations

import re
import speech_recognition as sr

from voice.listener import Listener
from voice.speaker import Speaker
from voice.wakeword import WakeWordDetector

from core.jarvis import Jarvis

from tools.router import CommandRouter
from tools.router_web import WebRouter
from tools.vision_command_layer import VisionCommandLayer

from security.command_security import CommandSecurity

from memory.memory_controller import MemoryController


# ==========================================
# JARVIS COMPONENTS
# ==========================================

jarvis = None
listener = None
speaker = None
wakeword = None
router = None
security = None
vision_layer = None
memory_controller = None


# ==========================================
# V5 WEB ROUTER
# ==========================================

web_router = WebRouter()


# ==========================================
# MEMORY RESPONSE HELPERS
# ==========================================

def format_memory_for_speech(content):
    """
    Convert stored first-person memory text into a
    natural JARVIS response addressed to the user.

    This function is used only when the user has
    explicitly requested memory retrieval.
    """

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

    # ======================================
    # Natural capitalization
    # ======================================

    if "programming language is python" in content.lower():

        content = re.sub(
            r"\bpython\b",
            "Python",
            content,
            flags=re.IGNORECASE,
        )

    # ======================================
    # Ensure clean punctuation
    # ======================================

    content = content.rstrip(" .!?")

    return f"{content}, sir."


# ==========================================
# MEMORY RESULT FORMATTING
# ==========================================

def handle_memory_result(result):
    """
    Display and speak a structured V7 memory result.

    V7.8 search results may use:

        data = {
            "query": "...",
            "memories": [...],
            "count": ...
        }

    This function extracts the actual memory list and
    uses the strongest ranked memory for the spoken answer.
    """

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

    # ======================================
    # CONSOLE OUTPUT
    # ======================================

    print("\nJARVIS V7 MEMORY:")

    if message:
        print(message)

    # ======================================
    # SAVE
    # ======================================

    if action == "save" and isinstance(data, dict):

        memory_id = data.get("id")
        category = data.get("category")
        content = data.get("content")

        print(
            f"Memory ID: {memory_id}"
        )

        print(
            f"Category: {category}"
        )

        print(
            f"Content: {content}"
        )

    # ======================================
    # SEARCH
    # ======================================

    elif action == "search":

        memories = []

        # V7.8 structured search result.
        if isinstance(data, dict):

            memories = data.get(
                "memories",
                [],
            )

        # Backward compatibility with older
        # list-based search results.
        elif isinstance(data, list):

            memories = data

        if memories:

            print("\nMatching memories:")

            for memory in memories:

                memory_id = memory.get(
                    "id",
                    "?",
                )

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
                    memory.get(
                        "score",
                        "",
                    ),
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

        else:

            print(
                "No matching memories."
            )

    # ======================================
    # LIST
    # ======================================

    elif action == "list" and isinstance(data, list):

        if data:

            print("\nStored memories:")

            for memory in data:

                memory_id = memory.get(
                    "id",
                    "?",
                )

                category = memory.get(
                    "category",
                    "general",
                )

                content = memory.get(
                    "content",
                    "",
                )

                print(
                    f"{memory_id}. "
                    f"[{category}] "
                    f"{content}"
                )

        else:

            print(
                "No memories are currently stored."
            )

    # ======================================
    # DELETE PENDING
    # ======================================

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

    # ======================================
    # DELETE
    # ======================================

    elif (
        action == "delete"
        and isinstance(data, dict)
    ):

        memory_id = data.get(
            "memory_id",
            "?",
        )

        deleted = data.get(
            "deleted",
            False,
        )

        print(
            f"Memory ID: {memory_id}"
        )

        print(
            f"Deleted: {deleted}"
        )

    # ======================================
    # UPDATE
    # ======================================

    elif (
        action == "update"
        and isinstance(data, dict)
    ):

        memory_id = data.get(
            "id",
            "?",
        )

        category = data.get(
            "category",
            "general",
        )

        content = data.get(
            "content",
            "",
        )

        print(
            f"Memory ID: {memory_id}"
        )

        print(
            f"Category: {category}"
        )

        print(
            f"Content: {content}"
        )

    # ======================================
    # VOICE RESPONSE - SEARCH
    # ======================================

    if action == "search":

        memories = []

        if isinstance(data, dict):

            memories = data.get(
                "memories",
                [],
            )

        elif isinstance(data, list):

            memories = data

        # ----------------------------------
        # Speak strongest matching memory.
        # ----------------------------------

        if memories:

            top_memory = memories[0]

            memory_content = top_memory.get(
                "content",
                "",
            )

            if memory_content:

                spoken_response = (
                    format_memory_for_speech(
                        memory_content
                    )
                )

                speaker.speak(
                    spoken_response
                )

            else:

                speaker.speak(
                    "I found the memory, sir."
                )

        else:

            speaker.speak(
                "I don't have any matching "
                "memories, sir."
            )

        return

    # ======================================
    # CONFIRMATION
    # ======================================

    if requires_confirmation:

        speaker.speak(
            message
        )

        return

    # ======================================
    # NORMAL MEMORY RESPONSE
    # ======================================

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


# ==========================================
# TOOL COMMAND DETECTION
# ==========================================

def is_tool_command(command):
    """
    Determine whether a command belongs to a
    non-Ollama tool subsystem.

    Memory commands are handled explicitly.

    Normal conversation is NOT searched against
    persistent memory.
    """

    command = command.lower().strip()

    # ======================================
    # V7 MEMORY COMMANDS
    # ======================================

    if memory_controller is not None:

        try:

            if memory_controller.is_memory_command(
                command
            ):
                return True

        except Exception as e:

            print(
                "JARVIS V7 memory detection error:",
                e,
            )

    # ======================================
    # V6 VISION COMMANDS
    # ======================================

    if vision_layer is not None:

        try:

            vision_result = (
                vision_layer.execute(
                    command
                )
            )

            if (
                vision_result["action"]
                != "unknown"
            ):
                return True

        except Exception as e:

            print(
                "JARVIS V6 vision detection error:",
                e,
            )

    # ======================================
    # V5 WEB COMMANDS
    # ======================================

    if web_router.is_web_command(
        command
    ):
        return True

    # ======================================
    # V4 FILESYSTEM2 COMMANDS
    # ======================================

    if router._is_filesystem2_command(
        command
    ):
        return True

    # ======================================
    # V4 FILESYSTEM COMMANDS
    # ======================================

    if router._is_filesystem_command(
        command
    ):
        return True

    # ======================================
    # APP COMMANDS
    # ======================================

    if (
        command.startswith("open ")
        or command.startswith("launch ")
        or command.startswith("start ")
        or command.startswith("close ")
        or command.startswith("terminate ")
        or command.startswith("kill ")
    ):
        return True

    # ======================================
    # V3 VOLUME COMMANDS
    # ======================================

    volume_commands = [

        "volume up",
        "volume increase",
        "volume increased",
        "increase volume",
        "increase the volume",
        "turn up volume",
        "turn up the volume",
        "make it louder",
        "louder",

        "volume down",
        "volume decrease",
        "volume decreased",
        "decrease volume",
        "decrease the volume",
        "turn down volume",
        "turn down the volume",
        "make it quieter",
        "quieter",

        "mute",
        "mute volume",
        "mute the volume",

        "unmute",
        "unmute volume",
        "unmute the volume",
    ]

    if command in volume_commands:
        return True

    # ======================================
    # V3 VOLUME PREFIXES
    # ======================================

    volume_prefixes = [

        "set volume",
        "set the volume",

        "volume to",
        "volume at",

        "volume up to",
        "volume down to",

        "volume increase to",
        "volume decrease to",

        "increase volume to",
        "increase the volume to",

        "decrease volume to",
        "decrease the volume to",

        "reduce volume to",
        "reduce the volume to",

        "turn volume to",
        "turn the volume to",

        "make volume",
        "make the volume",

        "set it to",
        "set it at",
        "put it at",
        "put volume at",

        "change volume to",
        "change the volume to",

        "change it to",
        "make it",
    ]

    for prefix in volume_prefixes:

        if command.startswith(prefix):

            if command in [
                "make it louder",
                "make it quieter",
            ]:
                continue

            remaining = command[
                len(prefix):
            ].strip()

            if remaining:

                match = re.match(
                    r"^(\d{1,3})%?$",
                    remaining,
                )

                if match:

                    value = int(
                        match.group(1)
                    )

                    if 0 <= value <= 100:
                        return True

    # ======================================
    # V3 LOCK COMMANDS
    # ======================================

    lock_commands = [

        "lock",
        "lock computer",
        "lock my computer",
        "lock the computer",
        "lock pc",
        "lock my pc",
    ]

    if command in lock_commands:
        return True

    # ======================================
    # V3 WINDOW COMMANDS
    # ======================================

    window_commands = [

        "minimize",
        "minimize window",
        "minimize the window",

        "minimise",
        "minimise window",
        "minimise the window",

        "maximize",
        "maximize window",
        "maximize the window",

        "maximise",
        "maximise window",
        "maximise the window",

        "restore",
        "restore window",
        "restore the window",

        "show desktop",
        "show the desktop",
        "desktop",

        "minimize all windows",
        "minimise all windows",

        "switch window",
        "switch windows",
        "switch to next window",
        "next window",
        "change window",
    ]

    if command in window_commands:
        return True

    # ======================================
    # EXACT VOLUME PERCENTAGE
    # ======================================

    if command.endswith("%"):

        percentage = command[
            :-1
        ].strip()

        if percentage.isdigit():

            value = int(
                percentage
            )

            if 0 <= value <= 100:
                return True

    return False


# ==========================================
# CONFIRMATION
# ==========================================

def is_confirmation(command):

    command = command.lower().strip()

    return command in [

        "yes",
        "yes jarvis",

        "confirm",
        "confirmed",

        "do it",
        "proceed",
        "go ahead",
        "continue",

        "okay",
        "ok",
        "sure",
    ]


def is_cancellation(command):

    command = command.lower().strip()

    return command in [

        "no",
        "no jarvis",

        "cancel",
        "cancel it",

        "don't",
        "do not",

        "stop",

        "never mind",
        "nevermind",
    ]


# ==========================================
# RISKY COMMAND CONFIRMATION
# ==========================================

def confirm_risky_command(command):

    command = command.lower().strip()

    lock_commands = [

        "lock",
        "lock computer",
        "lock my computer",
        "lock the computer",
        "lock pc",
        "lock my pc",
    ]

    if command in lock_commands:

        speaker.speak(
            "Sir, locking the computer will "
            "lock your current Windows session. "
            "Should I continue?"
        )

    else:

        speaker.speak(
            "Sir, this action may close an "
            "application and could affect "
            "unsaved work. Should I continue?"
        )

    try:

        confirmation = (
            listener.listen()
            .lower()
            .strip()
        )

        if is_confirmation(
            confirmation
        ):

            speaker.speak(
                "Confirmed, sir."
            )

            return True

        if is_cancellation(
            confirmation
        ):

            speaker.speak(
                "Cancelled, sir."
            )

            return False

        speaker.speak(
            "I didn't receive a clear "
            "confirmation, sir. The action "
            "has been cancelled."
        )

        return False

    except sr.UnknownValueError:

        speaker.speak(
            "I couldn't understand your "
            "confirmation, sir. The action "
            "has been cancelled."
        )

        return False

    except sr.RequestError as e:

        print(
            "JARVIS: Speech recognition error "
            "during confirmation:",
            e,
        )

        speaker.speak(
            "Speech recognition is unavailable, "
            "sir. The action has been cancelled."
        )

        return False

    except Exception as e:

        print(
            "JARVIS confirmation error:",
            e,
        )

        speaker.speak(
            "Something went wrong during "
            "confirmation, sir. The action "
            "has been cancelled."
        )

        return False


# ==========================================
# MEMORY CONFIRMATION
# ==========================================

def handle_pending_memory_confirmation(
    command,
):
    """
    Handle yes/no while a memory deletion is pending.
    """

    if memory_controller is None:
        return False

    if not memory_controller.has_pending_confirmation():
        return False

    # ======================================
    # CONFIRM
    # ======================================

    if is_confirmation(command):

        result = (
            memory_controller.confirm_delete()
        )

        handle_memory_result(
            result
        )

        return True

    # ======================================
    # CANCEL
    # ======================================

    if is_cancellation(command):

        result = (
            memory_controller.cancel_delete()
        )

        handle_memory_result(
            result
        )

        return True

    # ======================================
    # ANY OTHER COMMAND
    # ======================================

    speaker.speak(
        "Sir, a memory deletion is awaiting "
        "confirmation. Please say yes to "
        "confirm or no to cancel."
    )

    return True


# ==========================================
# HANDLE TOOL RESULT
# ==========================================

def handle_tool_result(result):

    if not result:
        return

    # ======================================
    # SPECIAL FILESYSTEM RESULT
    # ======================================

    if "|||VOICE|||" in result:

        console_output, voice_output = (
            result.split(
                "|||VOICE|||",
                1,
            )
        )

        print(
            "\n" + console_output
        )

        speaker.speak(
            voice_output.strip()
        )

        return

    # ======================================
    # NORMAL TOOL RESULT
    # ======================================

    speaker.speak(
        result
    )


# ==========================================
# HANDLE V6 RESULT
# ==========================================

def handle_vision_result(result):

    if not result:
        return

    response = result.get(
        "response",
        "",
    )

    if response:

        print(
            "\nJARVIS V6:"
        )

        print(
            response
        )

        speaker.speak(
            response
        )

    else:

        speaker.speak(
            "The vision command completed, sir."
        )


# ==========================================
# MAIN JARVIS LOOP
# ==========================================

def main():

    global jarvis
    global listener
    global speaker
    global wakeword
    global router
    global security
    global vision_layer
    global memory_controller

    # ======================================
    # JARVIS SETUP
    # ======================================

    jarvis = Jarvis()

    listener = Listener()

    speaker = Speaker()

    wakeword = WakeWordDetector()

    router = CommandRouter()

    security = CommandSecurity()

    vision_layer = VisionCommandLayer()

    memory_controller = MemoryController()

    # ======================================
    # STARTUP
    # ======================================

    print(
        "=========================================="
    )

    print(
        "             JARVIS V7"
    )

    print(
        "=========================================="
    )

    print(
        "Persistent Memory: ACTIVE"
    )

    print(
        "Computer Vision: ACTIVE"
    )

    print(
        "Browser Control: ACTIVE"
    )

    print()

    print(
        "Say 'Hey Jarvis' to activate."
    )

    print(
        "Say 'goodbye' or 'talk to you later' "
        "to end a conversation."
    )

    print(
        "Say 'exit' to shut down JARVIS."
    )

    print(
        "Press Ctrl+C to stop."
    )

    print()

    # ======================================
    # MEMORY STATUS
    # ======================================

    try:

        memory_count = (
            memory_controller.get_memory_count()
        )

        print(
            f"Stored memories: {memory_count}"
        )

    except Exception as e:

        print(
            "JARVIS V7 memory startup error:",
            e,
        )

    print()

    running = True

    # ======================================
    # OUTER LOOP
    # ======================================

    while running:

        try:

            # ==================================
            # WAIT FOR WAKE WORD
            # ==================================

            wakeword.wait_for_wake_word()

            print(
                "\n>>> HEY JARVIS DETECTED <<<"
            )

            speaker.speak(
                "Yes, sir."
            )

            conversation_active = True

            # ==================================
            # CONVERSATION LOOP
            # ==================================

            while conversation_active:

                try:

                    command = (
                        listener.listen()
                        .lower()
                        .strip()
                    )

                    # ==================================
                    # EMPTY COMMAND
                    # ==================================

                    if not command:
                        continue

                    # ==================================
                    # PENDING MEMORY DELETE
                    # ==================================

                    if (
                        memory_controller
                        is not None
                        and memory_controller.has_pending_confirmation()
                    ):

                        if handle_pending_memory_confirmation(
                            command
                        ):
                            continue

                    # ==================================
                    # EXIT JARVIS
                    # ==================================

                    if command in [

                        "exit",
                        "shut down",
                        "shutdown",
                        "terminate",

                    ]:

                        speaker.speak(
                            "Goodbye, sir."
                        )

                        running = False

                        conversation_active = False

                        continue

                    # ==================================
                    # END CURRENT CONVERSATION
                    # ==================================

                    elif command in [

                        "bye",
                        "goodbye",
                        "talk to you later",

                    ]:

                        speaker.speak(
                            "Goodbye, sir."
                        )

                        conversation_active = False

                        continue

                    # ==================================
                    # TOOL COMMAND
                    # ==================================

                    elif is_tool_command(
                        command
                    ):

                        # ==================================
                        # V7 MEMORY COMMAND
                        # ==================================

                        if (
                            memory_controller
                            is not None
                            and memory_controller.is_memory_command(
                                command
                            )
                        ):

                            result = (
                                memory_controller.execute(
                                    command
                                )
                            )

                            handle_memory_result(
                                result
                            )

                            continue

                        # ==================================
                        # CHECK V6 FIRST
                        # ==================================

                        vision_result = (
                            vision_layer.execute(
                                command
                            )
                        )

                        if (
                            vision_result["action"]
                            != "unknown"
                        ):

                            # ----------------------------------
                            # SECURITY CHECK
                            # ----------------------------------

                            security_level = (
                                security.check(
                                    command
                                )
                            )

                            if (
                                security_level
                                == CommandSecurity.BLOCKED
                            ):

                                speaker.speak(
                                    "I cannot perform that "
                                    "command because it is "
                                    "blocked for safety, sir."
                                )

                                continue

                            if (
                                security_level
                                == CommandSecurity.RISKY
                            ):

                                confirmed = (
                                    confirm_risky_command(
                                        command
                                    )
                                )

                                if not confirmed:
                                    continue

                            handle_vision_result(
                                vision_result
                            )

                            continue

                        # ==================================
                        # SECURITY CHECK V3/V4/V5
                        # ==================================

                        security_level = (
                            security.check(
                                command
                            )
                        )

                        if (
                            security_level
                            == CommandSecurity.BLOCKED
                        ):

                            speaker.speak(
                                "I cannot perform that "
                                "command because it is "
                                "blocked for safety, sir."
                            )

                            continue

                        if (
                            security_level
                            == CommandSecurity.RISKY
                        ):

                            confirmed = (
                                confirm_risky_command(
                                    command
                                )
                            )

                            if not confirmed:
                                continue

                        # ==================================
                        # V5 WEB
                        # ==================================

                        if web_router.is_web_command(
                            command
                        ):

                            result = (
                                web_router.execute(
                                    command
                                )
                            )

                        # ==================================
                        # V3/V4
                        # ==================================

                        else:

                            result = (
                                router.route(
                                    command
                                )
                            )

                        # ==================================
                        # HANDLE RESULT
                        # ==================================

                        if result:

                            handle_tool_result(
                                result
                            )

                    # ==================================
                    # NORMAL AI CONVERSATION
                    # ==================================

                    else:

                        # ==================================
                        # IMPORTANT V7 RULE
                        # ==================================
                        #
                        # Do NOT automatically search
                        # persistent memory here.
                        #
                        # Memory is accessed only when
                        # MemoryController explicitly
                        # identifies the user's command
                        # as a memory command/question.
                        #
                        # This prevents stored memories
                        # from hijacking ordinary
                        # conversation.
                        #
                        # Examples:
                        #
                        # "What should I work on today?"
                        #       -> Ollama
                        #
                        # "Help me plan my JARVIS tasks."
                        #       -> Ollama
                        #
                        # "Tell me something interesting."
                        #       -> Ollama
                        #
                        # Explicit memory questions such as
                        # "Do you remember my favourite dish?"
                        # are handled above by
                        # MemoryController.
                        # ==================================

                        response = (
                            jarvis.respond(
                                command
                            )
                        )

                        speaker.speak(
                            response
                        )

                # ======================================
                # SPEECH RECOGNITION ERROR
                # ======================================

                except sr.UnknownValueError:

                    speaker.speak(
                        "Sorry, sir. I didn't "
                        "understand that."
                    )

                    continue

                except sr.RequestError as e:

                    print(
                        "JARVIS: Speech recognition "
                        "error:",
                        e,
                    )

                    speaker.speak(
                        "Sorry, sir. Speech recognition "
                        "is currently unavailable."
                    )

                    continue

                # ======================================
                # CONVERSATION ERROR
                # ======================================

                except Exception as e:

                    print(
                        "JARVIS conversation error:",
                        e,
                    )

                    speaker.speak(
                        "Sorry, sir. Something went wrong."
                    )

                    continue

            # ==================================
            # WAIT FOR NEXT WAKE WORD
            # ==================================

            if running:

                print(
                    "\nWaiting for 'Hey Jarvis'..."
                )

        # ======================================
        # CTRL+C
        # ======================================

        except KeyboardInterrupt:

            print(
                "\n\nShutting down JARVIS."
            )

            try:

                speaker.speak(
                    "Goodbye, sir."
                )

            except Exception:
                pass

            running = False

        # ======================================
        # GENERAL ERROR
        # ======================================

        except Exception as e:

            print(
                "JARVIS error:",
                e,
            )

    # ==========================================
    # SHUTDOWN
    # ==========================================

    print(
        "\nJARVIS has been shut down."
    )


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()

