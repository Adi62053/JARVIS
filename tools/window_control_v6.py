"""
JARVIS V6.4 - Active Window Detection

Provides Windows active/foreground window information using
native Windows APIs through ctypes.

No third-party package is required.
"""

from pathlib import Path
import ctypes
from ctypes import wintypes


class WindowControlV6:
    """
    JARVIS V6.4 window detection and inspection.

    Detects the currently active Windows window and returns:
        - window handle
        - title
        - process ID
        - process name
        - process path
        - window class
        - visibility
        - maximized/minimized state
        - position
        - size
    """

    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

    def __init__(self):
        """Initialize required Windows APIs."""

        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32

        self.user32.GetForegroundWindow.restype = wintypes.HWND

        self.user32.GetWindowTextLengthW.argtypes = [
            wintypes.HWND
        ]
        self.user32.GetWindowTextLengthW.restype = ctypes.c_int

        self.user32.GetWindowTextW.argtypes = [
            wintypes.HWND,
            wintypes.LPWSTR,
            ctypes.c_int,
        ]
        self.user32.GetWindowTextW.restype = ctypes.c_int

        self.user32.GetClassNameW.argtypes = [
            wintypes.HWND,
            wintypes.LPWSTR,
            ctypes.c_int,
        ]
        self.user32.GetClassNameW.restype = ctypes.c_int

        self.user32.GetWindowRect.argtypes = [
            wintypes.HWND,
            ctypes.POINTER(wintypes.RECT),
        ]
        self.user32.GetWindowRect.restype = wintypes.BOOL

        self.user32.IsWindow.argtypes = [
            wintypes.HWND
        ]
        self.user32.IsWindow.restype = wintypes.BOOL

        self.user32.IsWindowVisible.argtypes = [
            wintypes.HWND
        ]
        self.user32.IsWindowVisible.restype = wintypes.BOOL

        self.user32.IsZoomed.argtypes = [
            wintypes.HWND
        ]
        self.user32.IsZoomed.restype = wintypes.BOOL

        self.user32.IsIconic.argtypes = [
            wintypes.HWND
        ]
        self.user32.IsIconic.restype = wintypes.BOOL

        self.user32.GetWindowThreadProcessId.argtypes = [
            wintypes.HWND,
            ctypes.POINTER(wintypes.DWORD),
        ]
        self.user32.GetWindowThreadProcessId.restype = wintypes.DWORD

        self.kernel32.OpenProcess.argtypes = [
            wintypes.DWORD,
            wintypes.BOOL,
            wintypes.DWORD,
        ]
        self.kernel32.OpenProcess.restype = wintypes.HANDLE

        self.kernel32.QueryFullProcessImageNameW.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.LPWSTR,
            ctypes.POINTER(wintypes.DWORD),
        ]
        self.kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL

        self.kernel32.CloseHandle.argtypes = [
            wintypes.HANDLE
        ]
        self.kernel32.CloseHandle.restype = wintypes.BOOL

    def _get_window_title(self, hwnd):
        """Return the active window title."""

        length = self.user32.GetWindowTextLengthW(hwnd)

        if length <= 0:
            return ""

        buffer = ctypes.create_unicode_buffer(length + 1)

        self.user32.GetWindowTextW(
            hwnd,
            buffer,
            length + 1,
        )

        return buffer.value.strip()

    def _get_window_class(self, hwnd):
        """Return the Windows window class name."""

        buffer = ctypes.create_unicode_buffer(512)

        length = self.user32.GetClassNameW(
            hwnd,
            buffer,
            len(buffer),
        )

        if length <= 0:
            return ""

        return buffer.value.strip()

    def _get_process_id(self, hwnd):
        """Return the process ID associated with the window."""

        process_id = wintypes.DWORD()

        result = self.user32.GetWindowThreadProcessId(
            hwnd,
            ctypes.byref(process_id),
        )

        if result == 0:
            return None

        return int(process_id.value)

    def _get_process_path(self, process_id):
        """Return the executable path of the process."""

        if not process_id:
            return ""

        process_handle = self.kernel32.OpenProcess(
            self.PROCESS_QUERY_LIMITED_INFORMATION,
            False,
            process_id,
        )

        if not process_handle:
            return ""

        try:
            buffer_size = wintypes.DWORD(32768)

            buffer = ctypes.create_unicode_buffer(
                buffer_size.value
            )

            success = self.kernel32.QueryFullProcessImageNameW(
                process_handle,
                0,
                buffer,
                ctypes.byref(buffer_size),
            )

            if not success:
                return ""

            return buffer.value

        finally:
            self.kernel32.CloseHandle(process_handle)

    @staticmethod
    def _get_process_name(process_path):
        """Extract the executable filename from its path."""

        if not process_path:
            return ""

        return Path(process_path).name

    def _get_geometry(self, hwnd):
        """Return window position and dimensions."""

        rect = wintypes.RECT()

        success = self.user32.GetWindowRect(
            hwnd,
            ctypes.byref(rect),
        )

        if not success:
            return {
                "x": 0,
                "y": 0,
                "width": 0,
                "height": 0,
            }

        return {
            "x": int(rect.left),
            "y": int(rect.top),
            "width": int(rect.right - rect.left),
            "height": int(rect.bottom - rect.top),
        }

    def detect_active_window(self):
        """
        Detect the currently active foreground window.

        Returns:
            dict: Structured active-window information.
        """

        hwnd = self.user32.GetForegroundWindow()

        if not hwnd:
            return {
                "detected": False,
                "reason": "No foreground window detected.",
            }

        if not self.user32.IsWindow(hwnd):
            return {
                "detected": False,
                "reason": "Invalid foreground window.",
            }

        title = self._get_window_title(hwnd)
        window_class = self._get_window_class(hwnd)

        process_id = self._get_process_id(hwnd)
        process_path = self._get_process_path(process_id)
        process_name = self._get_process_name(process_path)

        geometry = self._get_geometry(hwnd)

        return {
            "detected": True,
            "hwnd": int(hwnd),
            "title": title,
            "process_id": process_id,
            "process_name": process_name,
            "process_path": process_path,
            "window_class": window_class,
            "visible": bool(
                self.user32.IsWindowVisible(hwnd)
            ),
            "maximized": bool(
                self.user32.IsZoomed(hwnd)
            ),
            "minimized": bool(
                self.user32.IsIconic(hwnd)
            ),
            "geometry": geometry,
        }

    def get_active_window(self):
        """Return active-window information."""

        return self.detect_active_window()


if __name__ == "__main__":
    detector = WindowControlV6()

    result = detector.detect_active_window()

    print("==========================================")
    print("      JARVIS V6.4 ACTIVE WINDOW")
    print("==========================================")

    if not result.get("detected"):
        print("[ERROR]")
        print(result.get("reason", "Unknown error"))
        raise SystemExit(1)

    print(f"[TITLE] {result['title']}")
    print(f"[PROCESS] {result['process_name']}")
    print(f"[PID] {result['process_id']}")
    print(f"[CLASS] {result['window_class']}")
    print(f"[PATH] {result['process_path']}")
    print(f"[VISIBLE] {result['visible']}")
    print(f"[MAXIMIZED] {result['maximized']}")
    print(f"[MINIMIZED] {result['minimized']}")

    geometry = result["geometry"]

    print(
        f"[POSITION] "
        f"x={geometry['x']} "
        f"y={geometry['y']}"
    )

    print(
        f"[SIZE] "
        f"{geometry['width']} x "
        f"{geometry['height']}"
    )

    print("==========================================")