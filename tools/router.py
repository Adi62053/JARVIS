import re

from tools.window_control import WindowControl
from tools.app_control import AppControl
from tools.system_control import SystemControl
from security.command_security import CommandSecurity


class CommandRouter:
    """
    Routes recognized commands to the appropriate JARVIS tool.

    V3 supports:
    - Opening approved applications
    - Closing approved applications
    - Remembering the last opened application
    - Volume up/down
    - Exact volume control
    - Mute/unmute
    - Lock computer
    - Window management
    - Basic command security
    """

    def __init__(self):
        self.app_control = AppControl()
        self.system_control = SystemControl()
        self.window_control = WindowControl()

        self.security = CommandSecurity()

        self.last_opened_app = None

    def route(self, command):
        command = command.lower().strip()

        # ======================================
        # SECURITY CHECK
        # ======================================

        security_level = self.security.check(command)

        if security_level == CommandSecurity.BLOCKED:
            return (
                "I cannot perform that command because "
                "it is blocked for safety."
            )

        # ======================================
        # EXACT VOLUME
        # ======================================

        exact_volume = self._extract_volume_percentage(command)

        if exact_volume is not None:
            return self.system_control.set_volume(exact_volume)

        # ======================================
        # VOLUME UP
        # ======================================

        volume_up_commands = [
            "volume up",
            "volume increase",
            "volume increased",
            "increase volume",
            "increase the volume",
            "turn up volume",
            "turn up the volume",
            "make it louder",
            "louder"
        ]

        if command in volume_up_commands:
            return self.system_control.volume_up()

        # ======================================
        # VOLUME DOWN
        # ======================================

        volume_down_commands = [
            "volume down",
            "volume decrease",
            "volume decreased",
            "decrease volume",
            "decrease the volume",
            "turn down volume",
            "turn down the volume",
            "make it quieter",
            "quieter"
        ]

        if command in volume_down_commands:
            return self.system_control.volume_down()

        # ======================================
        # MUTE
        # ======================================

        mute_commands = [
            "mute",
            "mute volume",
            "mute the volume"
        ]

        if command in mute_commands:
            return self.system_control.mute()

        # ======================================
        # UNMUTE
        # ======================================

        unmute_commands = [
            "unmute",
            "unmute volume",
            "unmute the volume"
        ]

        if command in unmute_commands:
            return self.system_control.unmute()

        # ======================================
        # LOCK COMPUTER
        # ======================================

        lock_commands = [
            "lock",
            "lock computer",
            "lock my computer",
            "lock the computer",
            "lock pc",
            "lock my pc"
        ]

        if command in lock_commands:
            return self.system_control.lock_computer()

        # ======================================
        # OPEN / LAUNCH / START
        # ======================================

        open_prefixes = [
            "open ",
            "launch ",
            "start "
        ]

        for prefix in open_prefixes:

            if command.startswith(prefix):

                app_name = command[len(prefix):].strip()

                result = self.app_control.execute(app_name)

                # Remember the last successfully opened app.
                if result.startswith("Opening"):
                    self.last_opened_app = app_name

                return result

        # ======================================
        # CLOSE / TERMINATE / KILL
        # ======================================

        close_phrases = [
            "close ",
            "terminate ",
            "kill "
        ]

        for phrase in close_phrases:

            if command.startswith(phrase):

                app_name = command[len(phrase):].strip()

                if app_name in [
                    "it",
                    "that",
                    "this"
                ]:

                    if self.last_opened_app is None:
                        return (
                            "I don't know which application "
                            "you want me to close."
                        )

                    app_name = self.last_opened_app

                if app_name.startswith("the "):
                    app_name = app_name[4:].strip()

                result = self.app_control.close(app_name)

                if result.startswith("Closed"):
                    self.last_opened_app = None

                return result

        # ======================================
        # WINDOW CONTROL
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
            "change window"
        ]

        if command in window_commands:
            return self.window_control.execute(command)

        # ======================================
        # UNKNOWN TOOL COMMAND
        # ======================================

        return "I don't have a tool for that command yet."

    # ==========================================
    # EXTRACT EXACT VOLUME
    # ==========================================

    def _extract_volume_percentage(self, command):
        """
        Detects natural volume commands such as:

        set volume to 30
        set volume to 30%
        set the volume to 50
        volume to 60
        volume at 40
        volume up to 70%
        volume down to 20%
        volume increase to 50%
        volume decrease to 30%
        turn volume to 10%
        turn the volume to 10%
        increase volume to 70%
        decrease volume to 20%
        reduce volume to 10%
        reduce the volume to 10%
        make volume 40%
        make the volume 40%
        """

        patterns = [

            # Standard commands
            r"^set volume to (\d{1,3})%?$",
            r"^set the volume to (\d{1,3})%?$",
            r"^set volume (\d{1,3})%?$",

            # Short commands
            r"^volume to (\d{1,3})%?$",
            r"^volume at (\d{1,3})%?$",

            # Volume up/down to exact level
            r"^volume up to (\d{1,3})%?$",
            r"^volume down to (\d{1,3})%?$",
            r"^volume increase to (\d{1,3})%?$",
            r"^volume decrease to (\d{1,3})%?$",

            # Increase/decrease
            r"^increase volume to (\d{1,3})%?$",
            r"^increase the volume to (\d{1,3})%?$",

            r"^decrease volume to (\d{1,3})%?$",
            r"^decrease the volume to (\d{1,3})%?$",

            # Reduce
            r"^reduce volume to (\d{1,3})%?$",
            r"^reduce the volume to (\d{1,3})%?$",

            # Turn volume
            r"^turn volume to (\d{1,3})%?$",
            r"^turn the volume to (\d{1,3})%?$",

            # Make volume
            r"^make volume (\d{1,3})%?$",
            r"^make the volume (\d{1,3})%?$",

            # Direct percentage
            r"^(\d{1,3})%$"
        ]

        for pattern in patterns:

            match = re.match(pattern, command)

            if match:

                percentage = int(match.group(1))

                # Keep volume safely between 0 and 100.
                percentage = max(
                    0,
                    min(100, percentage)
                )

                return percentage

        return None
