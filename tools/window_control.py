import ctypes

from tools.base import Tool


class WindowControl(Tool):
    """
    Controls the currently active Windows window.
    
    V3 supports:
    - Minimize window
    - Maximize window
    - Restore window
    - Show desktop
    - Switch between windows
    """

    @property
    def name(self):
        return "window_control"

    @property
    def description(self):
        return "Controls the active Windows window."

    def execute(self, command):
        """
        Execute a Windows window-management command.
        """

        command = command.lower().strip()

        # ======================================
        # MINIMIZE
        # ======================================

        if command in [
            "minimize",
            "minimize window",
            "minimize the window",
            "minimise",
            "minimise window",
            "minimise the window"
        ]:
            return self.minimize_window()

        # ======================================
        # MAXIMIZE
        # ======================================

        if command in [
            "maximize",
            "maximize window",
            "maximize the window",
            "maximise",
            "maximise window",
            "maximise the window"
        ]:
            return self.maximize_window()

        # ======================================
        # RESTORE
        # ======================================

        if command in [
            "restore",
            "restore window",
            "restore the window"
        ]:
            return self.restore_window()

        # ======================================
        # SHOW DESKTOP
        # ======================================

        if command in [
            "show desktop",
            "show the desktop",
            "desktop",
            "minimize all windows",
            "minimise all windows"
        ]:
            return self.show_desktop()

        # ======================================
        # SWITCH WINDOW
        # ======================================

        if command in [
            "switch window",
            "switch windows",
            "switch to next window",
            "next window",
            "change window"
        ]:
            return self.switch_window()

        return "I don't have a window control for that command yet."

    # ==========================================
    # MINIMIZE WINDOW
    # ==========================================

    def minimize_window(self):
        """
        Minimize the currently active window.
        """

        try:
            user32 = ctypes.windll.user32

            hwnd = user32.GetForegroundWindow()

            if not hwnd:
                return "I could not find the active window."

            user32.ShowWindow(hwnd, 6)

            return "Minimized the active window, sir."

        except Exception as e:

            return f"Could not minimize the window: {e}"

    # ==========================================
    # MAXIMIZE WINDOW
    # ==========================================

    def maximize_window(self):
        """
        Maximize the currently active window.
        """

        try:
            user32 = ctypes.windll.user32

            hwnd = user32.GetForegroundWindow()

            if not hwnd:
                return "I could not find the active window."

            user32.ShowWindow(hwnd, 3)

            return "Maximized the active window, sir."

        except Exception as e:

            return f"Could not maximize the window: {e}"

    # ==========================================
    # RESTORE WINDOW
    # ==========================================

    def restore_window(self):
        """
        Restore the currently active window.
        """

        try:
            user32 = ctypes.windll.user32

            hwnd = user32.GetForegroundWindow()

            if not hwnd:
                return "I could not find the active window."

            user32.ShowWindow(hwnd, 9)

            return "Restored the active window, sir."

        except Exception as e:

            return f"Could not restore the window: {e}"

    # ==========================================
    # SHOW DESKTOP
    # ==========================================

    def show_desktop(self):
        """
        Show the Windows desktop.
        """

        try:
            user32 = ctypes.windll.user32

            # Win + D
            user32.keybd_event(0x5B, 0, 0, 0)
            user32.keybd_event(0x44, 0, 0, 0)
            user32.keybd_event(0x44, 0, 2, 0)
            user32.keybd_event(0x5B, 0, 2, 0)

            return "Showing the desktop, sir."

        except Exception as e:

            return f"Could not show the desktop: {e}"

    # ==========================================
    # SWITCH WINDOW
    # ==========================================

    def switch_window(self):
        """
        Switch to the next Windows application window.
        """

        try:
            user32 = ctypes.windll.user32

            # Alt + Tab
            user32.keybd_event(0x12, 0, 0, 0)
            user32.keybd_event(0x09, 0, 0, 0)
            user32.keybd_event(0x09, 0, 2, 0)
            user32.keybd_event(0x12, 0, 2, 0)

            return "Switching to the next window, sir."

        except Exception as e:

            return f"Could not switch windows: {e}"

