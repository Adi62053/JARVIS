import re

from tools.window_control import WindowControl
from tools.app_control import AppControl
from tools.system_control import SystemControl
from tools.filesystem_control import FileSystemControl
from tools.filesystem2 import FileSystem2
from security.command_security import CommandSecurity


class CommandRouter:
    """
    Central command router for JARVIS V4.

    V3:
    - Open applications
    - Close applications
    - Volume control
    - Mute/unmute
    - Lock computer
    - Window management

    V4:
    - Search files
    - Search folders
    - Find files
    - Find folders
    - Natural-language file search
    - Inspect files
    - Inspect folders
    - Read files
    - Read files by search-result number
    - Read currently selected file
    - Open files by search-result number
    - Open folders by search-result number
    - Close files by search-result number
    - Close folders
    - Create files
    - Create folders

    V4 Filesystem2:
    - Delete files
    - Delete folders
    - Rename files
    - Rename folders
    - Copy files
    - Copy folders
    - Move files
    - Move folders
    """

    def __init__(self):

        self.app_control = AppControl()

        self.system_control = SystemControl()

        self.window_control = WindowControl()

        # Existing V4 filesystem system
        self.filesystem_control = FileSystemControl()

        # New V4 filesystem operations
        self.filesystem2 = FileSystem2()

        self.security = CommandSecurity()

        self.last_opened_app = None

    # ==========================================
    # MAIN ROUTER
    # ==========================================

    def route(self, command):

        command = command.lower().strip()

        # ======================================
        # SECURITY
        # ======================================

        security_level = self.security.check(command)

        if security_level == CommandSecurity.BLOCKED:

            return (
                "I cannot perform that command because "
                "it is blocked for safety."
            )

        # ======================================
        # FILESYSTEM2 COMMANDS
        #
        # These MUST be checked before the
        # existing filesystem controller because
        # the existing controller does not handle
        # rename/delete/copy/move yet.
        # ======================================

        if self._is_filesystem2_command(command):

            return self.filesystem2.execute(
                command
            )

        # ======================================
        # EXISTING FILESYSTEM COMMANDS
        # ======================================

        if self._is_filesystem_command(command):

            return self.filesystem_control.execute(
                command
            )

        # ======================================
        # EXACT VOLUME
        # ======================================

        exact_volume = self._extract_volume_percentage(
            command
        )

        if exact_volume is not None:

            return self.system_control.set_volume(
                exact_volume
            )

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
            "louder",
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
            "quieter",
        ]

        if command in volume_down_commands:

            return self.system_control.volume_down()

        # ======================================
        # MUTE
        # ======================================

        mute_commands = [
            "mute",
            "mute volume",
            "mute the volume",
        ]

        if command in mute_commands:

            return self.system_control.mute()

        # ======================================
        # UNMUTE
        # ======================================

        unmute_commands = [
            "unmute",
            "unmute volume",
            "unmute the volume",
        ]

        if command in unmute_commands:

            return self.system_control.unmute()

        # ======================================
        # LOCK
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

            return self.system_control.lock_computer()

        # ======================================
        # OPEN APPLICATION
        # ======================================

        open_prefixes = [
            "open ",
            "launch ",
            "start ",
        ]

        for prefix in open_prefixes:

            if command.startswith(prefix):

                app_name = command[
                    len(prefix):
                ].strip()

                result = self.app_control.execute(
                    app_name
                )

                if result.startswith("Opening"):

                    self.last_opened_app = app_name

                return result

        # ======================================
        # CLOSE APPLICATION
        # ======================================

        close_prefixes = [
            "close ",
            "terminate ",
            "kill ",
        ]

        for prefix in close_prefixes:

            if command.startswith(prefix):

                app_name = command[
                    len(prefix):
                ].strip()

                # ------------------------------
                # Close "it"
                # ------------------------------

                if app_name in [
                    "it",
                    "that",
                    "this",
                ]:

                    if self.last_opened_app is None:

                        return (
                            "I don't know which application "
                            "you want me to close."
                        )

                    app_name = self.last_opened_app

                # ------------------------------
                # Remove "the"
                # ------------------------------

                if app_name.startswith("the "):

                    app_name = app_name[
                        4:
                    ].strip()

                result = self.app_control.close(
                    app_name
                )

                if result.startswith("Closed"):

                    self.last_opened_app = None

                return result

        # ======================================
        # WINDOW COMMANDS
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

            return self.window_control.execute(
                command
            )

        # ======================================
        # NO TOOL
        # ======================================

        return (
            "I don't have a tool for that command yet."
        )

    # ==========================================
    # FILESYSTEM2 COMMAND DETECTION
    # ==========================================

    def _is_filesystem2_command(self, command):

        command = command.lower().strip()

        # ======================================
        # RENAME
        # ======================================

        if re.match(
            r"^rename\s+(file|files|folder|folders)\s+.+\s+to\s+.+$",
            command
        ):

            return True

        # ======================================
        # DELETE
        # ======================================

        if re.match(
            r"^(delete|remove)\s+(file|files|folder|folders)\s+.+$",
            command
        ):

            return True

        # ======================================
        # COPY
        # ======================================

        if re.match(
            r"^copy\s+(file|files|folder|folders)\s+.+\s+to\s+.+$",
            command
        ):

            return True

        # ======================================
        # MOVE
        # ======================================

        if re.match(
            r"^move\s+(file|files|folder|folders)\s+.+\s+to\s+.+$",
            command
        ):

            return True

        return False

    # ==========================================
    # EXISTING FILESYSTEM COMMAND DETECTION
    # ==========================================

    def _is_filesystem_command(self, command):

        command = command.lower().strip()

        # ======================================
        # EXACT FILESYSTEM COMMANDS
        # ======================================

        filesystem_exact_commands = [

            # ----------------------------------
            # File search
            # ----------------------------------

            "search file",
            "search files",

            "find file",
            "find files",

            # ----------------------------------
            # Folder search
            # ----------------------------------

            "search folder",
            "search folders",

            "find folder",
            "find folders",

            # ----------------------------------
            # Inspection
            # ----------------------------------

            "inspect file",
            "inspect folder",

            # ----------------------------------
            # Reading
            # ----------------------------------

            "read this file",
            "read the file",
            "read this",
            "read the content",

            "read the content of this file",
            "read contents of this file",
            "read the contents of this file",
            "read content of this file",

            # ----------------------------------
            # Opening
            # ----------------------------------

            "open file",
            "open folder",

            # ----------------------------------
            # Closing files/folders
            # ----------------------------------

            "close file",
            "close files",

            "close file number",
            "close files number",

            "close file no",
            "close files no",

            "close folder",
            "close folders",

            # ----------------------------------
            # Create
            # ----------------------------------

            "create file",
            "create folder",

            "make file",
            "make folder",

            "new file",
            "new folder",
        ]

        if command in filesystem_exact_commands:

            return True

        # ======================================
        # FILESYSTEM PREFIXES
        # ======================================

        filesystem_prefixes = [

            # ----------------------------------
            # Search
            # ----------------------------------

            "search file ",
            "search files ",

            "find file ",
            "find files ",

            "search folder ",
            "search folders ",

            "find folder ",
            "find folders ",

            # ----------------------------------
            # Inspection
            # ----------------------------------

            "inspect file ",
            "inspect folder ",

            # ----------------------------------
            # Reading
            # ----------------------------------

            "read file ",
            "read files ",

            "read my ",
            "read the ",

            # ----------------------------------
            # File result number
            # ----------------------------------

            "file number ",
            "file no ",

            "read file number ",
            "read file no ",

            # ----------------------------------
            # Open result number
            # ----------------------------------

            "open file number ",
            "open file no ",

            "open folder number ",
            "open folder no ",

            # ----------------------------------
            # Close result number
            # ----------------------------------

            "close file number ",
            "close files number ",

            "close file no ",
            "close files no ",

            # ----------------------------------
            # Close folders
            # ----------------------------------

            "close folder ",
            "close folders ",

            # ----------------------------------
            # Natural search
            # ----------------------------------

            "search my ",
            "search for my ",
            "search for ",

            "find my ",
            "find ",

            # ----------------------------------
            # Natural opening
            # ----------------------------------

            "open my ",
            "open the ",

            # ----------------------------------
            # Resume
            # ----------------------------------

            "search resume ",
            "find resume ",

            # ----------------------------------
            # PDF
            # ----------------------------------

            "search pdf ",
            "find pdf ",

            # ----------------------------------
            # Documents
            # ----------------------------------

            "search document ",
            "search documents ",

            "find document ",
            "find documents ",

            "search docx ",
            "find docx ",

            # ----------------------------------
            # CREATE
            # ----------------------------------

            "create file ",
            "create folder ",

            "make file ",
            "make folder ",

            "new file ",
            "new folder ",
        ]

        for prefix in filesystem_prefixes:

            if command.startswith(prefix):

                return True

        # ======================================
        # NUMBER-WORD COMMANDS
        # ======================================

        number_words = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "eleven",
            "twelve",
            "thirteen",
            "fourteen",
            "fifteen",
            "sixteen",
            "seventeen",
            "eighteen",
            "nineteen",
            "twenty",
        ]

        number_word_pattern = "|".join(
            number_words
        )

        if re.match(
            rf"^(read|open|close)\s+file\s+number\s+({number_word_pattern})$",
            command
        ):

            return True

        if re.match(
            rf"^(read|open|close)\s+file\s+no\s+({number_word_pattern})$",
            command
        ):

            return True

        if re.match(
            rf"^close\s+files\s+number\s+({number_word_pattern})$",
            command
        ):

            return True

        if re.match(
            rf"^close\s+files\s+no\s+({number_word_pattern})$",
            command
        ):

            return True

        # ======================================
        # SPECIAL RESUME COMMANDS
        # ======================================

        if "resume" in command:

            resume_triggers = [
                "search",
                "find",
                "read",
                "open",
            ]

            if any(
                command.startswith(trigger)
                for trigger in resume_triggers
            ):

                return True

        # ======================================
        # SHORT RESUME
        # ======================================

        resume_short_forms = [
            "res",
            "resu",
            "resum",
        ]

        words = command.split()

        if any(
            word in resume_short_forms
            for word in words
        ):

            search_find_triggers = [
                "search",
                "find",
            ]

            if any(
                command.startswith(trigger)
                for trigger in search_find_triggers
            ):

                return True

        # ======================================
        # PDF SEARCH
        # ======================================

        if (
            command.startswith("search ")
            and "pdf" in command
        ):

            return True

        if (
            command.startswith("find ")
            and "pdf" in command
        ):

            return True

        # ======================================
        # DOCUMENT SEARCH
        # ======================================

        if (
            command.startswith("search ")
            and (
                "document" in command
                or "documents" in command
                or "docx" in command
            )
        ):

            return True

        if (
            command.startswith("find ")
            and (
                "document" in command
                or "documents" in command
                or "docx" in command
            )
        ):

            return True

        # ======================================
        # GENERAL FILE/FOLDER OPEN
        # ======================================

        if command.startswith(
            (
                "open file ",
                "open folder ",
            )
        ):

            return True

        # ======================================
        # GENERAL FILE READ
        # ======================================

        if command.startswith(
            (
                "read file ",
                "read files ",
            )
        ):

            return True

        # ======================================
        # GENERAL FILE CLOSE
        # ======================================

        if command.startswith(
            (
                "close file ",
                "close files ",
                "close folder ",
                "close folders ",
            )
        ):

            return True

        # ======================================
        # CREATE
        # ======================================

        if command.startswith(
            (
                "create file ",
                "create folder ",
                "make file ",
                "make folder ",
                "new file ",
                "new folder ",
            )
        ):

            return True

        return False

    # ==========================================
    # VOLUME PERCENTAGE EXTRACTION
    # ==========================================

    def _extract_volume_percentage(self, command):

        patterns = [

            r"^set volume to (\d{1,3})%?$",

            r"^set the volume to (\d{1,3})%?$",

            r"^set volume (\d{1,3})%?$",

            r"^volume to (\d{1,3})%?$",

            r"^volume at (\d{1,3})%?$",

            r"^volume up to (\d{1,3})%?$",

            r"^volume down to (\d{1,3})%?$",

            r"^volume increase to (\d{1,3})%?$",

            r"^volume decrease to (\d{1,3})%?$",

            r"^increase volume to (\d{1,3})%?$",

            r"^increase the volume to (\d{1,3})%?$",

            r"^decrease volume to (\d{1,3})%?$",

            r"^decrease the volume to (\d{1,3})%?$",

            r"^reduce volume to (\d{1,3})%?$",

            r"^reduce the volume to (\d{1,3})%?$",

            r"^turn volume to (\d{1,3})%?$",

            r"^turn the volume to (\d{1,3})%?$",

            r"^make volume (\d{1,3})%?$",

            r"^make the volume (\d{1,3})%?$",

            # ----------------------------------
            # Natural spoken volume commands
            # ----------------------------------

            r"^set it to (\d{1,3})%?$",

            r"^set it at (\d{1,3})%?$",

            r"^put it at (\d{1,3})%?$",

            r"^put volume at (\d{1,3})%?$",

            r"^change volume to (\d{1,3})%?$",

            r"^change the volume to (\d{1,3})%?$",

            r"^change it to (\d{1,3})%?$",

            r"^make it (\d{1,3})%?$",

            # ----------------------------------
            # Direct percentage
            # ----------------------------------

            r"^(\d{1,3})%$",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                command
            )

            if match:

                percentage = int(
                    match.group(1)
                )

                percentage = max(
                    0,
                    min(
                        100,
                        percentage
                    )
                )

                return percentage

        return None