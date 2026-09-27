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
from automation.v9_automation_security import V9AutomationSecurity

from security.v9_security_controller import V9SecurityController

from jarvis_unified_automation import (
    is_automation_command,
    handle_automation_command as _handle_automation_command,
)


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
v9_security_controller = None


# ============================================================
# V5 WEB ROUTER
# ============================================================

web_router = WebRouter()


# ============================================================
# MEMORY SPEECH FORMATTING
# ============================================================

from jarvis_unified_memory import (
    format_memory_for_speech,
    handle_memory_result as _handle_memory_result,
)


def handle_memory_result(result):
    return _handle_memory_result(result, speaker)


# ============================================================
# TOOL COMMAND DETECTION
# ============================================================

def is_tool_command(command: str) -> bool:
    """
    Preserve the V7 command ownership order.

    V8 is inserted before V3/V4 so that automation
    commands cannot be intercepted by the generic
    CommandRouter.

    V4 filesystem commands are checked before generic
    V5 web detection because both systems intentionally
    recognize natural-language search commands such as
    "search for ...".

    Explicit web commands retain V5 ownership.
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
    # V5 WEATHER
    # ========================================================

    if web_router._is_weather_command(command):

        return True

    # ========================================================
    # V8 AUTOMATION
    # ========================================================

    if is_automation_command(command):

        return True

    # ========================================================
    # V5 EXPLICIT WEB COMMANDS
    # ========================================================

    explicit_web_prefixes = [

        "search the web for ",
        "search the internet for ",
        "search online for ",
        "find online ",
        "find on the internet ",
        "google ",
        "web search ",
        "internet search ",
    ]

    if any(
        command.startswith(prefix)
        for prefix in explicit_web_prefixes
    ):

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
    global v9_security_controller

    automation_manager = AutomationManager()

    automation_handler = AutomationCommandHandler(
        manager=automation_manager
    )

    v9_security_controller = V9SecurityController()

    v9_automation_security = V9AutomationSecurity(
        controller=v9_security_controller
    )

    executor = AutomationExecutor(
        v9_security=v9_automation_security
    )

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

    print("==========================================")
    print("          JARVIS V1-V8")
    print("==========================================")
    print("Persistent Memory: ACTIVE")
    print("Computer Vision: ACTIVE")
    print("Browser Control: ACTIVE")
    print("Personal Automation: ACTIVE")
    print()
    print("Say 'Hey Jarvis' to activate.")
    print(
        "Say 'goodbye' or 'talk to you later' "
        "to end a conversation."
    )
    print("Say 'exit' to shut down JARVIS.")
    print("Press Ctrl+C to stop.")
    print()

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

    try:

        automation_count = len(
            automation_manager.list_all()
        )

        print(
            f"Automations loaded: {automation_count}"
        )

    except Exception as exc:

        print(
            "JARVIS V8 automation startup error:",
            type(exc).__name__,
            repr(exc),
        )

    print()

    from jarvis_unified_runtime import run_unified_runtime

    run_unified_runtime(
        jarvis=jarvis,
        listener=listener,
        speaker=speaker,
        wakeword=wakeword,
        router=router,
        security=security,
        vision_layer=vision_layer,
        memory_controller=memory_controller,
        automation_manager=automation_manager,
        automation_handler=automation_handler,
        automation_workflow_runner=automation_workflow_runner,
        web_router=web_router,
        CommandSecurity=CommandSecurity,
        sr=sr,
        is_tool_command=is_tool_command,
        handle_pending_memory_confirmation=(
            handle_pending_memory_confirmation
        ),
        handle_memory_result=handle_memory_result,
        handle_vision_result=handle_vision_result,
        handle_tool_result=handle_tool_result,
        confirm_risky_command=confirm_risky_command,
        is_automation_command=is_automation_command,
        handle_automation_command=(
            _handle_automation_command
        ),
    )


if __name__ == "__main__":

    main()