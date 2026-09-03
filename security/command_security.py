class CommandSecurity:
    """
    Basic security checks for JARVIS V3 commands.

    The purpose of this class is to identify commands
    that require additional protection before execution.

    V3 security categories:

    SAFE
        Normal low-risk actions.

    RISKY
        Actions that can affect applications or the
        Windows session and may later require confirmation.

    BLOCKED
        Actions that JARVIS should refuse to perform.
    """

    SAFE = "safe"
    RISKY = "risky"
    BLOCKED = "blocked"

    def check(self, command):
        """
        Check the security level of a command.

        Returns:
            "safe"
            "risky"
            "blocked"
        """

        command = command.lower().strip()

        # ======================================
        # BLOCKED COMMANDS
        # ======================================

        blocked_commands = [
            "format computer",
            "format pc",
            "delete windows",
            "remove windows",
            "destroy system",
            "wipe computer",
            "wipe pc"
        ]

        if command in blocked_commands:
            return self.BLOCKED

        # ======================================
        # RISKY COMMANDS
        # ======================================

        risky_commands = [
            "lock",
            "lock computer",
            "lock my computer",
            "lock the computer",
            "lock pc",
            "lock my pc"
        ]

        if command in risky_commands:
            return self.RISKY

        # Closing applications can affect user work.
        if (
            command.startswith("close ")
            or command.startswith("terminate ")
            or command.startswith("kill ")
        ):
            return self.RISKY

        # ======================================
        # SAFE BY DEFAULT
        # ======================================

        return self.SAFE

    def is_safe(self, command):
        return self.check(command) == self.SAFE

    def is_risky(self, command):
        return self.check(command) == self.RISKY

    def is_blocked(self, command):
        return self.check(command) == self.BLOCKED
