"""
JARVIS Unified Runtime

Based on the proven JARVIS V7 runtime architecture.

Preserves:
- V1 Ollama conversation
- V2 wake word
- V3 laptop control
- V4 filesystem
- V5 web intelligence
- V6 computer vision/browser control
- V7 persistent memory

Adds:
- V8 personal automation

Important:
- main.py remains unchanged.
- main_v7.py remains frozen.
- main_v8.py remains frozen.
- This file is integration-only.
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

from automation.automation_command_handler import (
    AutomationCommandHandler,
)
from automation.automation_executor import AutomationExecutor
from automation.automation_manager import AutomationManager
from automation.memory_workflow_runner import (
    MemoryWorkflowRunner,
)
from automation.schedule_runner import ScheduleRunner
from automation.workflow_runner import WorkflowRunner


# ============================================================
# JARVIS COMPONENTS
# ============================================================

jarvis = None
listener = None
speaker = None
wakeword = None
router = None
security = None
vision_layer = None
memory_controller = None

automation_manager = None
automation_handler = None
automation_workflow_runner = None
automation_scheduler = None


# ============================================================
# V5 WEB ROUTER
# ============================================================

web_router = WebRouter()


# ============================================================
# V8 AUTOMATION DETECTION
# ============================================================

def is_automation_command(command: str) -> bool:
    """
    Determine whether a command belongs to V8 automation.

    V8 management commands are checked before V3/V4 because
    commands such as "open ..." are handled by the older
    CommandRouter and must not steal V8 commands.
    """

    command = command.lower().strip()

    automation_prefixes = [
        "create automation ",
        "show automation ",
        "enable automation ",
        "disable automation ",
        "delete automation ",
        "add step to automation ",
        "remove step from automation ",
        "add condition to automation ",
        "remove condition from automation ",
        "show conditions for automation ",
        "run automation ",
    ]

    automation_exact = [
        "list automations",
        "show automations",
    ]

    if command in automation_exact:
        return True

    for prefix in automation_prefixes:
        if command.startswith(prefix):
            return True

    return False


# ============================================================
# V8 AUTOMATION EXECUTION
# ============================================================

def handle_automation_command(command: str) -> str:
    """
    Execute a V8 automation command.

    V8 management remains delegated to the frozen
    AutomationCommandHandler.

    Automation execution uses the existing:
        AutomationManager
        MemoryWorkflowRunner
        WorkflowRunner
        AutomationExecutor
    """

    if (
        automation_manager is None
        or automation_handler is None
        or automation_workflow_runner is None
    ):
        return (
            "The automation system is not initialized, sir."
        )

    normalized = command.strip()

    # --------------------------------------------------------
    # RUN AUTOMATION
    # --------------------------------------------------------

    if normalized.lower().startswith(
        "run automation "
    ):

        automation_name = normalized[
            len("run automation "):
        ].strip()

        if not automation_name:
            return (
                "Please tell me which automation to run, sir."
            )

        automation = automation_manager.get(
            automation_name
        )

        if automation is None:
            return (
                f"Automation '{automation_name}' "
                "was not found."
            )

        try:

            results = automation_workflow_runner.run(
                automation,
                memory_query=automation.description,
            )

            response = (
                f"Automation '{automation.name}' "
                "completed."
            )

            if results:

                response += "\n" + "\n".join(
                    results
                )

            return response

        except Exception as exc:

            return (
                f"Automation '{automation.name}' "
                f"failed: {type(exc).__name__}: {exc!r}"
            )

    # --------------------------------------------------------
    # V8 MANAGEMENT
    # --------------------------------------------------------

    try:

        return automation_handler.handle(
            normalized
        )

    except Exception as exc:

        return (
            "The automation command failed: "
            f"{type(exc).__name__}: {exc!r}"
        )


# ============================================================
# MEMORY SPEECH FORMATTING
# ============================================================

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


# ============================================================
# MEMORY RESULT HANDLER
# ============================================================

def handle_memory_result(result):

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

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    if action == "save" and isinstance(data, dict):

        print(
            f"Memory ID: {data.get('id')}"
        )

        print(
            f"Category: {data.get('category')}"
        )

        print(
            f"Content: {data.get('content')}"
        )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

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

        if memories:

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

            speaker.speak(
                "I don't have any matching "
                "memories, sir."
            )

        return

    # --------------------------------------------------------
    # LIST
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # DELETE PENDING
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # CONFIRMATION
    # --------------------------------------------------------

    if requires_confirmation:

        speaker.speak(
            message
        )

        return

    # --------------------------------------------------------
    # NORMAL MEMORY RESPONSE
    # --------------------------------------------------------

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


# ============================================================
# TOOL COMMAND DETECTION
# ============================================================

def is_tool_command(command: str) -> bool:
    """
    Preserve the V7 command ownership order.

    V8 is inserted before V3/V4 so that automation
    commands cannot be intercepted by the generic
    CommandRouter.
    """

    command = command.lower().strip()

    # ========================================================
    # V7 MEMORY
    # ========================================================

    if memory_controller is not None:

        try:

            if memory_controller.is_memory_command(
                command
            ):
                return True

        except Exception as exc:

            print(
                "JARVIS V7 memory detection error:",
                type(exc).__name__,
                repr(exc),
            )

    # ========================================================
    # V6 VISION
    # ========================================================

    if vision_layer is not None:

        try:

            vision_result = vision_layer.execute(
                command
            )

            if (
                vision_result["action"]
                != "unknown"
            ):

                return True

        except Exception as exc:

            print(
                "JARVIS V6 vision detection error:",
                type(exc).__name__,
                repr(exc),
            )

    # ========================================================
    # V8 AUTOMATION
    # ========================================================

    if is_automation_command(command):

        return True

    # ========================================================
    # V5 WEB
    # ========================================================

    if web_router.is_web_command(command):

        return True

    # ========================================================
    # V4 FILESYSTEM2
    # ========================================================

    if router._is_filesystem2_command(command):

        return True

    # ========================================================
    # V4 FILESYSTEM
    # ========================================================

    if router._is_filesystem_command(command):

        return True

    # ========================================================
    # V3 APP COMMANDS
    # ========================================================

    if (
        command.startswith("open ")
        or command.startswith("launch ")
        or command.startswith("start ")
        or command.startswith("close ")
        or command.startswith("terminate ")
        or command.startswith("kill ")
    ):

        return True

    # ========================================================
    # V3 VOLUME
    # ========================================================

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

    # ========================================================
    # V3 VOLUME PREFIXES
    # ========================================================

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

    # ========================================================
    # V3 LOCK
    # ========================================================

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

    # ========================================================
    # V3 WINDOW
    # ========================================================

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

    # ========================================================
    # EXACT VOLUME PERCENTAGE
    # ========================================================

    if command.endswith("%"):

        percentage = command[:-1].strip()

        if percentage.isdigit():

            value = int(percentage)

            if 0 <= value <= 100:
                return True

    return False


# ============================================================
# CONFIRMATION
# ============================================================

def is_confirmation(command: str) -> bool:

    return command.lower().strip() in [

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


def is_cancellation(command: str) -> bool:

    return command.lower().strip() in [

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


# ============================================================
# RISKY COMMAND CONFIRMATION
# ============================================================

def confirm_risky_command(command: str) -> bool:

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

        if is_confirmation(confirmation):

            speaker.speak(
                "Confirmed, sir."
            )

            return True

        if is_cancellation(confirmation):

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

    except sr.RequestError as exc:

        print(
            "JARVIS: Speech recognition error "
            "during confirmation:",
            exc,
        )

        speaker.speak(
            "Speech recognition is unavailable, "
            "sir. The action has been cancelled."
        )

        return False

    except Exception as exc:

        print(
            "JARVIS confirmation error:",
            type(exc).__name__,
            repr(exc),
        )

        speaker.speak(
            "Something went wrong during "
            "confirmation, sir. The action "
            "has been cancelled."
        )

        return False


# ============================================================
# MEMORY PENDING CONFIRMATION
# ============================================================

def handle_pending_memory_confirmation(
    command: str,
) -> bool:

    if memory_controller is None:
        return False

    if not memory_controller.has_pending_confirmation():
        return False

    if is_confirmation(command):

        result = (
            memory_controller.confirm_delete()
        )

        handle_memory_result(result)

        return True

    if is_cancellation(command):

        result = (
            memory_controller.cancel_delete()
        )

        handle_memory_result(result)

        return True

    speaker.speak(
        "Sir, a memory deletion is awaiting "
        "confirmation. Please say yes to "
        "confirm or no to cancel."
    )

    return True


# ============================================================
# NORMAL TOOL RESULT
# ============================================================

def handle_tool_result(result):

    if not result:
        return

    if isinstance(result, str):

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

        speaker.speak(result)

        return

    # Safety fallback for unexpected tool output.
    speaker.speak(
        str(result)
    )


# ============================================================
# V6 RESULT
# ============================================================

def handle_vision_result(result):

    if not result:
        return

    response = result.get(
        "response",
        "",
    )

    if response:

        # Preserve V6's useful console result.
        print(
            "\nJARVIS V6:"
        )

        print(response)

        speaker.speak(response)

    else:

        speaker.speak(
            "The vision command completed, sir."
        )


# ============================================================
# V8 INITIALIZATION
# ============================================================

def initialize_v8():

    global automation_manager
    global automation_handler
    global automation_workflow_runner
    global automation_scheduler

    automation_manager = AutomationManager()

    automation_handler = AutomationCommandHandler(
        manager=automation_manager
    )

    executor = AutomationExecutor()

    workflow_runner = WorkflowRunner(
        executor=executor
    )

    automation_memory = __import__(
        "automation.automation_memory",
        fromlist=["AutomationMemory"],
    ).AutomationMemory()

    automation_workflow_runner = (
        MemoryWorkflowRunner(
            workflow_runner=workflow_runner,
            memory=automation_memory,
        )
    )

    automation_scheduler = ScheduleRunner(
        automation_manager=automation_manager,
        workflow_runner=automation_workflow_runner,
    )


# ============================================================
# MAIN
# ============================================================

def main():

    global jarvis
    global listener
    global speaker
    global wakeword
    global router
    global security
    global vision_layer
    global memory_controller

    # ========================================================
    # SAME V7 INITIALIZATION
    # ========================================================

    jarvis = Jarvis()

    listener = Listener()

    speaker = Speaker()

    wakeword = WakeWordDetector()

    router = CommandRouter()

    security = CommandSecurity()

    vision_layer = VisionCommandLayer()

    memory_controller = MemoryController()

    # ========================================================
    # V8 ADDITION
    # ========================================================

    initialize_v8()

    # ========================================================
    # STARTUP
    # ========================================================

    print(
        "=========================================="
    )

    print(
        "          JARVIS V1-V8"
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

    print(
        "Personal Automation: ACTIVE"
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

    # ========================================================
    # MEMORY STATUS
    # ========================================================

    try:

        memory_count = (
            memory_controller.get_memory_count()
        )

        print(
            f"Stored memories: {memory_count}"
        )

    except Exception as exc:

        print(
            "JARVIS V7 memory startup error:",
            type(exc).__name__,
            repr(exc),
        )

    # ========================================================
    # V8 STATUS
    # ========================================================

    try:

        automation_count = len(
            automation_manager.list_all()
        )

        print(
            f"Automations loaded: "
            f"{automation_count}"
        )

    except Exception as exc:

        print(
            "JARVIS V8 automation startup error:",
            type(exc).__name__,
            repr(exc),
        )

    print()

    running = True

    # ========================================================
    # OUTER WAKE-WORD LOOP
    # ========================================================

    while running:

        try:

            wakeword.wait_for_wake_word()

            print(
                "\n>>> HEY JARVIS DETECTED <<<"
            )

            speaker.speak(
                "Yes, sir."
            )

            conversation_active = True

            # =================================================
            # CONVERSATION LOOP
            # =================================================

            while conversation_active:

                try:

                    command = (
                        listener.listen()
                        .lower()
                        .strip()
                    )

                    if not command:
                        continue

                    # =========================================
                    # V7 MEMORY DELETE CONFIRMATION
                    # =========================================

                    if (
                        memory_controller is not None
                        and memory_controller.has_pending_confirmation()
                    ):

                        if handle_pending_memory_confirmation(
                            command
                        ):
                            continue

                    # =========================================
                    # EXIT
                    # =========================================

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

                    # =========================================
                    # END CONVERSATION
                    # =========================================

                    if command in [

                        "bye",
                        "goodbye",
                        "talk to you later",

                    ]:

                        speaker.speak(
                            "Goodbye, sir."
                        )

                        conversation_active = False

                        continue

                    # =========================================
                    # TOOL COMMAND
                    # =========================================

                    if is_tool_command(command):

                        # =====================================
                        # V7 MEMORY
                        # =====================================

                        if (
                            memory_controller is not None
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

                        # =====================================
                        # V6
                        # =====================================

                        vision_result = (
                            vision_layer.execute(
                                command
                            )
                        )

                        if (
                            vision_result["action"]
                            != "unknown"
                        ):

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

                                if not confirm_risky_command(
                                    command
                                ):
                                    continue

                            handle_vision_result(
                                vision_result
                            )

                            continue

                        # =====================================
                        # V8
                        # =====================================

                        if is_automation_command(command):

                            result = (
                                handle_automation_command(
                                    command
                                )
                            )

                            handle_tool_result(
                                result
                            )

                            continue

                        # =====================================
                        # V5 / V3 / V4 SECURITY
                        # =====================================

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

                            if not confirm_risky_command(
                                command
                            ):
                                continue

                        # =====================================
                        # V5 WEB
                        # =====================================

                        if web_router.is_web_command(
                            command
                        ):

                            result = (
                                web_router.execute(
                                    command
                                )
                            )

                        # =====================================
                        # V3 / V4
                        # =====================================

                        else:

                            result = (
                                router.route(
                                    command
                                )
                            )

                        if result:

                            handle_tool_result(
                                result
                            )

                        continue

                    # =========================================
                    # NORMAL V1 AI CONVERSATION
                    # =========================================

                    response = (
                        jarvis.respond(
                            command
                        )
                    )

                    speaker.speak(
                        response
                    )

                # =================================================
                # SPEECH RECOGNITION ERRORS
                # =================================================

                except sr.UnknownValueError:

                    speaker.speak(
                        "Sorry, sir. I didn't "
                        "understand that."
                    )

                    continue

                except sr.RequestError as exc:

                    print(
                        "JARVIS: Speech recognition error:",
                        exc,
                    )

                    speaker.speak(
                        "Sorry, sir. Speech recognition "
                        "is currently unavailable."
                    )

                    continue

                # =================================================
                # CONVERSATION ERROR
                # =================================================

                except Exception as exc:

                    print(
                        "JARVIS conversation error:",
                        type(exc).__name__,
                        repr(exc),
                    )

                    speaker.speak(
                        "Sorry, sir. Something went wrong."
                    )

                    continue

            # ====================================================
            # RETURN TO WAKE WORD
            # ====================================================

            if running:

                print(
                    "\nWaiting for 'Hey Jarvis'..."
                )

        # ========================================================
        # CTRL+C
        # ========================================================

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

        # ========================================================
        # OUTER ERROR
        # ========================================================

        except Exception as exc:

            print(
                "JARVIS error:",
                type(exc).__name__,
                repr(exc),
            )

    # ============================================================
    # SHUTDOWN
    # ============================================================

    print(
        "\nJARVIS has been shut down."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()