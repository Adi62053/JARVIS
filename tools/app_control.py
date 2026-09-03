import subprocess

from tools.base import Tool


class AppControl(Tool):
    """
    Safely launches and closes approved Windows applications
    and common Windows utilities.
    """

    def __init__(self):
        self.apps = {

            # ======================================
            # APPROVED APPLICATIONS
            # ======================================

            "notepad": {
                "launch": "notepad.exe",
                "process": "notepad.exe",
            },

            "calculator": {
                "launch": "calc.exe",
                "process": "CalculatorApp.exe",
            },

            "file explorer": {
                "launch": "explorer.exe",
                "process": "explorer.exe",
            },

            "explorer": {
                "launch": "explorer.exe",
                "process": "explorer.exe",
            },

            "chrome": {
                "launch": (
                    r"C:\Program Files\Google\Chrome"
                    r"\Application\chrome.exe"
                ),
                "process": "chrome.exe",
            },

            # ======================================
            # WINDOWS UTILITIES
            # ======================================

            "settings": {
                "launch": "ms-settings:",
                "process": "SystemSettings.exe",
            },

            "task manager": {
                "launch": "taskmgr.exe",
                "process": "Taskmgr.exe",
            },

            "control panel": {
                "launch": "control.exe",
                "process": "control.exe",
            },

            "command prompt": {
                "launch": "cmd.exe",
                "process": "cmd.exe",
            },

            "cmd": {
                "launch": "cmd.exe",
                "process": "cmd.exe",
            },

            "powershell": {
                "launch": "powershell.exe",
                "process": "powershell.exe",
            },

            "device manager": {
                "launch": "devmgmt.msc",
                "process": "mmc.exe",
            },
        }

    @property
    def name(self):
        return "app_control"

    @property
    def description(self):
        return (
            "Launch and close approved Windows applications "
            "and utilities."
        )

    # ==========================================
    # OPEN APPLICATION / UTILITY
    # ==========================================

    def execute(self, app_name):
        """
        Launch an approved application or Windows utility.
        """

        app_name = app_name.lower().strip()

        if app_name not in self.apps:
            return f"Application '{app_name}' is not approved."

        try:
            launch_command = self.apps[app_name]["launch"]

            # Windows URI such as ms-settings:
            if launch_command.endswith(":"):

                subprocess.Popen(
                    ["cmd", "/c", "start", "", launch_command],
                    shell=False
                )

            else:

                subprocess.Popen(launch_command)

            return f"Opening {app_name}."

        except Exception as e:

            return f"Could not open {app_name}: {e}"

    # ==========================================
    # CLOSE APPLICATION / UTILITY
    # ==========================================

    def close(self, app_name):
        """
        Close an approved application or Windows utility.
        """

        app_name = app_name.lower().strip()

        if app_name not in self.apps:
            return f"Application '{app_name}' is not approved."

        process_name = self.apps[app_name]["process"]

        # --------------------------------------
        # NO SAFE PROCESS
        # --------------------------------------

        if process_name is None:

            return (
                f"I cannot safely close {app_name} yet."
            )

        # --------------------------------------
        # PROTECT WINDOWS EXPLORER
        # --------------------------------------

        if process_name == "explorer.exe":

            return (
                "I won't close File Explorer because it is "
                "also a Windows system process."
            )

        # --------------------------------------
        # CLOSE PROCESS
        # --------------------------------------

        try:

            result = subprocess.run(
                [
                    "taskkill",
                    "/IM",
                    process_name,
                    "/F"
                ],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:

                return f"Closed {app_name}."

            return (
                f"{app_name} is not currently running."
            )

        except Exception as e:

            return (
                f"Could not close {app_name}: {e}"
            )
