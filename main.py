import speech_recognition as sr

from voice.listener import Listener
from voice.speaker import Speaker
from voice.wakeword import WakeWordDetector
from core.jarvis import Jarvis
from tools.router import CommandRouter
from security.command_security import CommandSecurity


# ==========================================
# JARVIS SETUP
# ==========================================

jarvis = Jarvis()
listener = Listener()
speaker = Speaker()
wakeword = WakeWordDetector()
router = CommandRouter()
security = CommandSecurity()


print("==========================================")
print("          JARVIS V3")
print("==========================================")
print("Say 'Hey Jarvis' to activate.")
print("Say 'goodbye' or 'talk to you later' to end a conversation.")
print("Say 'exit' to shut down JARVIS.")
print("Press Ctrl+C to stop.")
print()


# ==========================================
# TOOL COMMAND DETECTION
# ==========================================

def is_tool_command(command):
    """
    Determines whether a command should be handled
    by JARVIS tools instead of the AI.

    V3 currently supports:
    - Opening applications
    - Closing applications
    - Opening Windows utilities
    - Volume control
    - Mute / unmute
    - Lock computer
    - Window management
    """

    # --------------------------------------
    # APP CONTROL
    # --------------------------------------

    if (
        command.startswith("open ")
        or command.startswith("launch ")
        or command.startswith("start ")
        or command.startswith("close ")
        or command.startswith("terminate ")
        or command.startswith("kill ")
    ):
        return True

    # --------------------------------------
    # DIRECT VOLUME COMMANDS
    # --------------------------------------

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
        "unmute the volume"
    ]

    if command in volume_commands:
        return True

    # --------------------------------------
    # EXACT / TARGET VOLUME COMMANDS
    # --------------------------------------

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
        "make the volume"
    ]

    for prefix in volume_prefixes:

        if command.startswith(prefix):
            return True

    # --------------------------------------
    # LOCK COMPUTER
    # --------------------------------------

    lock_commands = [
        "lock",
        "lock computer",
        "lock my computer",
        "lock the computer",
        "lock pc",
        "lock my pc"
    ]

    if command in lock_commands:
        return True

    # --------------------------------------
    # WINDOW CONTROL
    # --------------------------------------

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
        "change window"
    ]

    if command in window_commands:
        return True

    # --------------------------------------
    # DIRECT PERCENTAGE
    # --------------------------------------

    if command.endswith("%"):

        percentage = command[:-1].strip()

        if percentage.isdigit():

            value = int(percentage)

            if 0 <= value <= 100:
                return True

    return False


# ==========================================
# CONFIRMATION DETECTION
# ==========================================

def is_confirmation(command):
    """
    Detects positive confirmation responses.
    """

    confirmation_commands = [
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
        "sure"
    ]

    return command in confirmation_commands


def is_cancellation(command):
    """
    Detects negative confirmation responses.
    """

    cancellation_commands = [
        "no",
        "no jarvis",
        "cancel",
        "cancel it",
        "don't",
        "do not",
        "stop",
        "never mind",
        "nevermind"
    ]

    return command in cancellation_commands


# ==========================================
# ASK FOR CONFIRMATION
# ==========================================

def confirm_risky_command(command):
    """
    Asks the user to confirm a risky command.

    Returns:
        True  -> user confirmed
        False -> user cancelled or did not confirm
    """

    # --------------------------------------
    # LOCK COMPUTER
    # --------------------------------------

    lock_commands = [
        "lock",
        "lock computer",
        "lock my computer",
        "lock the computer",
        "lock pc",
        "lock my pc"
    ]

    if command in lock_commands:

        speaker.speak(
            "Sir, locking the computer will lock your "
            "current Windows session. Should I continue?"
        )

    # --------------------------------------
    # CLOSE / TERMINATE / KILL
    # --------------------------------------

    else:

        speaker.speak(
            "Sir, this action may close an application "
            "and could affect unsaved work. Should I continue?"
        )

    # --------------------------------------
    # LISTEN FOR CONFIRMATION
    # --------------------------------------

    try:

        confirmation = listener.listen()

        confirmation = confirmation.lower().strip()

        # ----------------------------------
        # CONFIRMED
        # ----------------------------------

        if is_confirmation(confirmation):

            speaker.speak("Confirmed, sir.")

            return True

        # ----------------------------------
        # CANCELLED
        # ----------------------------------

        if is_cancellation(confirmation):

            speaker.speak("Cancelled, sir.")

            return False

        # ----------------------------------
        # UNKNOWN ANSWER
        # ----------------------------------

        speaker.speak(
            "I didn't receive a clear confirmation, sir. "
            "The action has been cancelled."
        )

        return False

    except sr.UnknownValueError:

        speaker.speak(
            "I couldn't understand your confirmation, sir. "
            "The action has been cancelled."
        )

        return False

    except sr.RequestError as e:

        print(
            "JARVIS: Speech recognition error during confirmation:",
            e
        )

        speaker.speak(
            "Speech recognition is unavailable, sir. "
            "The action has been cancelled."
        )

        return False

    except Exception as e:

        print(
            "JARVIS confirmation error:",
            e
        )

        speaker.speak(
            "Something went wrong during confirmation, sir. "
            "The action has been cancelled."
        )

        return False


# ==========================================
# MAIN LOOP
# ==========================================

running = True

while running:

    try:

        # --------------------------------------
        # WAIT FOR WAKE WORD
        # --------------------------------------

        wakeword.wait_for_wake_word()

        print("\n>>> HEY JARVIS DETECTED <<<")

        speaker.speak("Yes, sir.")

        # --------------------------------------
        # ACTIVE CONVERSATION
        # --------------------------------------

        conversation_active = True

        while conversation_active:

            try:

                # ----------------------------------
                # LISTEN
                # ----------------------------------

                command = listener.listen()

                command = command.lower().strip()

                # ----------------------------------
                # COMPLETELY SHUT DOWN JARVIS
                # ----------------------------------

                if command in [
                    "exit",
                    "shut down",
                    "shutdown",
                    "terminate"
                ]:

                    speaker.speak("Goodbye, sir.")

                    running = False
                    conversation_active = False

                    continue

                # ----------------------------------
                # END CURRENT CONVERSATION ONLY
                # ----------------------------------

                elif command in [
                    "bye",
                    "goodbye",
                    "talk to you later"
                ]:

                    speaker.speak("Goodbye, sir.")

                    conversation_active = False

                    continue

                # ----------------------------------
                # V3 TOOL COMMANDS
                # ----------------------------------

                elif is_tool_command(command):

                    # ----------------------------------
                    # SECURITY CHECK
                    # ----------------------------------

                    security_level = security.check(command)

                    # ----------------------------------
                    # BLOCKED COMMAND
                    # ----------------------------------

                    if security_level == CommandSecurity.BLOCKED:

                        speaker.speak(
                            "I cannot perform that command "
                            "because it is blocked for safety, sir."
                        )

                        continue

                    # ----------------------------------
                    # RISKY COMMAND
                    # ----------------------------------

                    if security_level == CommandSecurity.RISKY:

                        confirmed = confirm_risky_command(command)

                        if not confirmed:
                            continue

                    # ----------------------------------
                    # EXECUTE TOOL
                    # ----------------------------------

                    result = router.route(command)

                    speaker.speak(result)

                # ----------------------------------
                # JARVIS AI RESPONSE
                # ----------------------------------

                else:

                    response = jarvis.respond(command)

                    speaker.speak(response)

            # --------------------------------------
            # SPEECH NOT UNDERSTOOD
            # --------------------------------------

            except sr.UnknownValueError:

                speaker.speak(
                    "Sorry, sir. I didn't understand that."
                )

                continue

            # --------------------------------------
            # GOOGLE SPEECH ERROR
            # --------------------------------------

            except sr.RequestError as e:

                print(
                    "JARVIS: Speech recognition error:",
                    e
                )

                speaker.speak(
                    "Sorry, sir. Speech recognition is currently unavailable."
                )

                continue

            # --------------------------------------
            # OTHER CONVERSATION ERRORS
            # --------------------------------------

            except Exception as e:

                print(
                    "JARVIS conversation error:",
                    e
                )

                speaker.speak(
                    "Sorry, sir. Something went wrong."
                )

                continue

        # --------------------------------------
        # RETURN TO WAKE-WORD MODE
        # --------------------------------------

        if running:

            print("\nWaiting for 'Hey Jarvis'...")

    # ------------------------------------------
    # CTRL + C
    # ------------------------------------------

    except KeyboardInterrupt:

        print("\n\nShutting down JARVIS.")

        try:
            speaker.speak("Goodbye, sir.")
        except Exception:
            pass

        running = False

    # ------------------------------------------
    # OTHER MAIN ERRORS
    # ------------------------------------------

    except Exception as e:

        print(
            "JARVIS error:",
            e
        )


# ==========================================
# SHUTDOWN
# ==========================================

print("\nJARVIS has been shut down.")

