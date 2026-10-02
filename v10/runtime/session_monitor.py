from __future__ import annotations

import ctypes
from ctypes import wintypes
from threading import Event, Lock, Thread
from typing import Callable, Optional


class SessionEvent:
    LOCK = "lock"
    UNLOCK = "unlock"


class _WNDCLASSW(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", ctypes.c_void_p),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HANDLE),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]


class SessionMonitor:
    """
    Windows WTS session lock/unlock monitor.

    The monitor owns a dedicated Win32 message-loop thread and registers
    WTS session notifications for the current interactive session.

    It reports:
        WTS_SESSION_LOCK
        WTS_SESSION_UNLOCK

    This component is intentionally isolated from JARVIS runtime
    lifecycle and application behavior.
    """

    _WM_CLOSE = 0x0010
    _WM_DESTROY = 0x0002
    _WM_WTSSESSION_CHANGE = 0x02B1

    _WTS_SESSION_LOCK = 0x7
    _WTS_SESSION_UNLOCK = 0x8

    _NOTIFY_FOR_THIS_SESSION = 0

    _HWND_MESSAGE = wintypes.HWND(-3)

    _STARTUP_TIMEOUT = 5.0

    _WNDPROC = ctypes.WINFUNCTYPE(
        ctypes.c_ssize_t,
        wintypes.HWND,
        wintypes.UINT,
        wintypes.WPARAM,
        wintypes.LPARAM,
    )

    def __init__(
        self,
        on_event: Optional[Callable[[str], None]] = None,
    ):
        if on_event is not None and not callable(on_event):
            raise TypeError("on_event must be callable or None")

        self._on_event = on_event

        self._lock = Lock()
        self._stop_event = Event()
        self._ready_event = Event()

        self._thread: Optional[Thread] = None
        self._hwnd = None
        self._class_name = None
        self._class_atom = 0
        self._registered = False

        self._startup_error: Optional[BaseException] = None

        self._user32 = ctypes.WinDLL("user32", use_last_error=True)
        self._wtsapi32 = ctypes.WinDLL("wtsapi32", use_last_error=True)
        self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        self._configure_win32_api()

        # Keep the callback alive for the entire lifetime of the window.
        self._wndproc = self._WNDPROC(self._window_proc)

    def _configure_win32_api(self):
        self._user32.RegisterClassW.argtypes = [
            ctypes.POINTER(_WNDCLASSW)
        ]
        self._user32.RegisterClassW.restype = wintypes.ATOM

        self._user32.UnregisterClassW.argtypes = [
            wintypes.LPCWSTR,
            wintypes.HINSTANCE,
        ]
        self._user32.UnregisterClassW.restype = wintypes.BOOL

        self._user32.CreateWindowExW.argtypes = [
            wintypes.DWORD,
            wintypes.LPCWSTR,
            wintypes.LPCWSTR,
            wintypes.DWORD,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            wintypes.HWND,
            wintypes.HMENU,
            wintypes.HINSTANCE,
            wintypes.LPVOID,
        ]
        self._user32.CreateWindowExW.restype = wintypes.HWND

        self._user32.DestroyWindow.argtypes = [
            wintypes.HWND
        ]
        self._user32.DestroyWindow.restype = wintypes.BOOL

        self._user32.DefWindowProcW.argtypes = [
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]
        self._user32.DefWindowProcW.restype = ctypes.c_ssize_t

        self._user32.GetMessageW.argtypes = [
            ctypes.POINTER(wintypes.MSG),
            wintypes.HWND,
            wintypes.UINT,
            wintypes.UINT,
        ]
        self._user32.GetMessageW.restype = wintypes.BOOL

        self._user32.TranslateMessage.argtypes = [
            ctypes.POINTER(wintypes.MSG)
        ]
        self._user32.TranslateMessage.restype = wintypes.BOOL

        self._user32.DispatchMessageW.argtypes = [
            ctypes.POINTER(wintypes.MSG)
        ]
        self._user32.DispatchMessageW.restype = ctypes.c_ssize_t

        self._user32.PostMessageW.argtypes = [
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]
        self._user32.PostMessageW.restype = wintypes.BOOL

        self._user32.PostQuitMessage.argtypes = [
            ctypes.c_int
        ]
        self._user32.PostQuitMessage.restype = None

        self._wtsapi32.WTSRegisterSessionNotification.argtypes = [
            wintypes.HWND,
            wintypes.DWORD,
        ]
        self._wtsapi32.WTSRegisterSessionNotification.restype = wintypes.BOOL

        self._wtsapi32.WTSUnRegisterSessionNotification.argtypes = [
            wintypes.HWND
        ]
        self._wtsapi32.WTSUnRegisterSessionNotification.restype = wintypes.BOOL

        self._kernel32.GetModuleHandleW.argtypes = [
            wintypes.LPCWSTR
        ]
        self._kernel32.GetModuleHandleW.restype = wintypes.HMODULE

    def start(self):
        with self._lock:
            if self._thread is not None and self._thread.is_alive():
                raise RuntimeError("Session monitor is already running")

            self._stop_event.clear()
            self._ready_event.clear()
            self._startup_error = None

            self._thread = Thread(
                target=self._run,
                name="JARVIS-V10-SessionMonitor",
                daemon=True,
            )

            self._thread.start()

        if not self._ready_event.wait(self._STARTUP_TIMEOUT):
            self.stop(timeout=1.0)
            raise TimeoutError(
                "Session monitor did not initialize within startup timeout"
            )

        with self._lock:
            startup_error = self._startup_error

        if startup_error is not None:
            self.stop(timeout=1.0)
            raise RuntimeError(
                "Session monitor failed to initialize"
            ) from startup_error

    def stop(self, timeout: float = 5.0):
        if timeout < 0:
            raise ValueError("timeout must be non-negative")

        with self._lock:
            thread = self._thread

            if thread is None:
                return

            self._stop_event.set()
            hwnd = self._hwnd

        if hwnd:
            self._user32.PostMessageW(
                hwnd,
                self._WM_CLOSE,
                0,
                0,
            )

        thread.join(timeout)

        if thread.is_alive():
            raise TimeoutError(
                "Session monitor did not stop within timeout"
            )

        with self._lock:
            self._thread = None
            self._hwnd = None
            self._registered = False
            self._class_atom = 0
            self._class_name = None

    def is_running(self) -> bool:
        with self._lock:
            return (
                self._thread is not None
                and self._thread.is_alive()
            )

    def _run(self):
        try:
            self._create_window()
            self._register_notifications()

            with self._lock:
                self._ready_event.set()

            self._message_loop()

        except BaseException as exc:
            with self._lock:
                self._startup_error = exc
                self._ready_event.set()

        finally:
            self._unregister_notifications()
            self._destroy_window()

    def _create_window(self):
        hinstance = self._kernel32.GetModuleHandleW(None)

        if not hinstance:
            error = ctypes.get_last_error()
            raise ctypes.WinError(error)

        self._class_name = (
            f"JARVIS_V10_SessionMonitor_{id(self):X}"
        )

        wndclass = _WNDCLASSW()
        wndclass.style = 0
        wndclass.lpfnWndProc = ctypes.cast(
            self._wndproc,
            ctypes.c_void_p,
        )
        wndclass.cbClsExtra = 0
        wndclass.cbWndExtra = 0
        wndclass.hInstance = hinstance
        wndclass.hIcon = None
        wndclass.hCursor = None
        wndclass.hbrBackground = None
        wndclass.lpszMenuName = None
        wndclass.lpszClassName = self._class_name

        atom = self._user32.RegisterClassW(
            ctypes.byref(wndclass)
        )

        if not atom:
            error = ctypes.get_last_error()
            raise ctypes.WinError(error)

        self._class_atom = atom

        hwnd = self._user32.CreateWindowExW(
            0,
            self._class_name,
            "JARVIS V10 Session Monitor",
            0,
            0,
            0,
            0,
            0,
            self._HWND_MESSAGE,
            None,
            hinstance,
            None,
        )

        if not hwnd:
            error = ctypes.get_last_error()

            self._user32.UnregisterClassW(
                self._class_name,
                hinstance,
            )

            self._class_atom = 0
            raise ctypes.WinError(error)

        self._hwnd = hwnd

    def _register_notifications(self):
        if not self._hwnd:
            raise RuntimeError(
                "Cannot register WTS notifications without a window"
            )

        result = self._wtsapi32.WTSRegisterSessionNotification(
            self._hwnd,
            self._NOTIFY_FOR_THIS_SESSION,
        )

        if not result:
            error = ctypes.get_last_error()
            raise ctypes.WinError(error)

        with self._lock:
            self._registered = True

    def _message_loop(self):
        msg = wintypes.MSG()

        while not self._stop_event.is_set():
            result = self._user32.GetMessageW(
                ctypes.byref(msg),
                None,
                0,
                0,
            )

            if result == -1:
                error = ctypes.get_last_error()
                raise ctypes.WinError(error)

            if result == 0:
                break

            self._user32.TranslateMessage(
                ctypes.byref(msg)
            )

            self._user32.DispatchMessageW(
                ctypes.byref(msg)
            )

    def _unregister_notifications(self):
        hwnd = self._hwnd

        with self._lock:
            registered = self._registered
            self._registered = False

        if registered and hwnd:
            self._wtsapi32.WTSUnRegisterSessionNotification(
                hwnd
            )

    def _destroy_window(self):
        hwnd = self._hwnd

        if hwnd:
            self._user32.DestroyWindow(hwnd)

        hinstance = self._kernel32.GetModuleHandleW(None)

        if (
            self._class_name
            and self._class_atom
            and hinstance
        ):
            self._user32.UnregisterClassW(
                self._class_name,
                hinstance,
            )

        self._hwnd = None
        self._class_atom = 0
        self._class_name = None

    def _window_proc(
        self,
        hwnd,
        message,
        wparam,
        lparam,
    ):
        if message == self._WM_WTSSESSION_CHANGE:
            if wparam == self._WTS_SESSION_LOCK:
                self._emit_event(SessionEvent.LOCK)
                return 0

            if wparam == self._WTS_SESSION_UNLOCK:
                self._emit_event(SessionEvent.UNLOCK)
                return 0

        elif message == self._WM_CLOSE:
            self._user32.DestroyWindow(hwnd)
            return 0

        elif message == self._WM_DESTROY:
            self._user32.PostQuitMessage(0)
            return 0

        return self._user32.DefWindowProcW(
            hwnd,
            message,
            wparam,
            lparam,
        )

    def _emit_event(self, event: str):
        callback = self._on_event

        if callback is None:
            return

        try:
            callback(event)
        except Exception:
            # A callback failure must not terminate the native
            # session-monitor message loop.
            pass
