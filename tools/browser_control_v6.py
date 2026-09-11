"""
JARVIS V6.6 - Browser Control

Provides safe browser automation for JARVIS.

Capabilities:
- Open a URL in the default browser
- Search the web
- Open a new browser tab
- Close the current browser tab
- Focus the browser address bar
- Navigate to a URL
- Open a new browser window
- Detect basic browser availability

This module intentionally does not perform destructive system actions.
"""

from __future__ import annotations

import shutil
import subprocess
import time
import webbrowser
from urllib.parse import quote, urlparse


class BrowserControlV6:
    """
    JARVIS V6.6 browser controller.

    Browser interaction is intentionally kept separate from:
        - vision_capture.py
        - vision_ocr.py
        - vision_analyzer.py
        - vision_router.py
    """

    SUPPORTED_BROWSERS = (
        "chrome",
        "msedge",
        "firefox",
    )

    SEARCH_ENGINE = "https://www.google.com/search?q="

    def __init__(self, browser=None, command_delay=0.25):
        """
        Initialize browser control.

        Args:
            browser: Optional browser executable name.
            command_delay: Delay after keyboard/browser actions.
        """

        self.browser = browser
        self.command_delay = command_delay

        self._pyautogui = None
        self._load_keyboard_control()

    # ---------------------------------------------------------
    # Dependency handling
    # ---------------------------------------------------------

    def _load_keyboard_control(self):
        """
        Load pyautogui lazily.

        Browser launching does not require pyautogui.
        Keyboard-based operations do.
        """

        try:
            import pyautogui

            self._pyautogui = pyautogui

        except ImportError:
            self._pyautogui = None

    def _require_keyboard_control(self):
        """Ensure keyboard automation is available."""

        if self._pyautogui is None:
            raise RuntimeError(
                "pyautogui is required for browser keyboard control."
            )

    # ---------------------------------------------------------
    # Browser detection
    # ---------------------------------------------------------

    def detect_browser(self):
        """
        Detect an installed browser.

        Returns:
            str | None: Browser executable name or None.
        """

        browser_commands = (
            ("chrome", "chrome"),
            ("msedge", "msedge"),
            ("firefox", "firefox"),
        )

        for name, command in browser_commands:
            if shutil.which(command):
                return name

        return None

    def get_browser_name(self):
        """
        Return configured browser or detected browser.
        """

        if self.browser:
            return self.browser

        detected = self.detect_browser()

        if detected:
            return detected

        return "default"

    # ---------------------------------------------------------
    # URL validation
    # ---------------------------------------------------------

    @staticmethod
    def normalize_url(url):
        """
        Normalize a user-provided URL.

        Examples:
            google.com
            https://google.com
            www.google.com

        Returns:
            str: Normalized URL.
        """

        if not isinstance(url, str):
            raise TypeError("URL must be a string.")

        url = url.strip()

        if not url:
            raise ValueError("URL cannot be empty.")

        if "://" not in url:
            url = "https://" + url

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            raise ValueError(
                "Only HTTP and HTTPS URLs are allowed."
            )

        if not parsed.netloc:
            raise ValueError("Invalid URL.")

        return url

    # ---------------------------------------------------------
    # Browser launching
    # ---------------------------------------------------------

    def open_url(self, url):
        """
        Open a URL in the configured/default browser.

        Returns:
            dict: Operation result.
        """

        normalized_url = self.normalize_url(url)

        browser = self.get_browser_name()

        if browser == "chrome":
            subprocess.Popen(
                ["chrome", normalized_url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        elif browser == "msedge":
            subprocess.Popen(
                ["msedge", normalized_url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        elif browser == "firefox":
            subprocess.Popen(
                ["firefox", normalized_url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        else:
            webbrowser.open(normalized_url)

        return {
            "success": True,
            "action": "open_url",
            "url": normalized_url,
            "browser": browser,
        }

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search_web(self, query):
        """
        Search Google using the browser.

        Args:
            query: Search text.

        Returns:
            dict: Operation result.
        """

        if not isinstance(query, str):
            raise TypeError("Search query must be a string.")

        query = query.strip()

        if not query:
            raise ValueError("Search query cannot be empty.")

        search_url = self.SEARCH_ENGINE + quote(query)

        result = self.open_url(search_url)

        result["action"] = "search_web"
        result["query"] = query

        return result

    # ---------------------------------------------------------
    # Keyboard actions
    # ---------------------------------------------------------

    def focus_address_bar(self):
        """
        Focus the browser address bar using Ctrl+L.
        """

        self._require_keyboard_control()

        self._pyautogui.hotkey("ctrl", "l")
        time.sleep(self.command_delay)

        return {
            "success": True,
            "action": "focus_address_bar",
        }

    def open_new_tab(self):
        """
        Open a new browser tab using Ctrl+T.
        """

        self._require_keyboard_control()

        self._pyautogui.hotkey("ctrl", "t")
        time.sleep(self.command_delay)

        return {
            "success": True,
            "action": "open_new_tab",
        }

    def close_current_tab(self):
        """
        Close the current browser tab using Ctrl+W.

        This does not terminate the browser process.
        """

        self._require_keyboard_control()

        self._pyautogui.hotkey("ctrl", "w")
        time.sleep(self.command_delay)

        return {
            "success": True,
            "action": "close_current_tab",
        }

    def refresh_page(self):
        """
        Refresh the current browser page.
        """

        self._require_keyboard_control()

        self._pyautogui.hotkey("ctrl", "r")
        time.sleep(self.command_delay)

        return {
            "success": True,
            "action": "refresh_page",
        }

    def go_back(self):
        """
        Navigate one page backward.
        """

        self._require_keyboard_control()

        self._pyautogui.hotkey("alt", "left")
        time.sleep(self.command_delay)

        return {
            "success": True,
            "action": "go_back",
        }

    def go_forward(self):
        """
        Navigate one page forward.
        """

        self._require_keyboard_control()

        self._pyautogui.hotkey("alt", "right")
        time.sleep(self.command_delay)

        return {
            "success": True,
            "action": "go_forward",
        }

    # ---------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------

    def navigate(self, url):
        """
        Navigate the currently focused browser tab to a URL.

        Uses Ctrl+L and types the URL.

        Returns:
            dict: Operation result.
        """

        normalized_url = self.normalize_url(url)

        self._require_keyboard_control()

        self._pyautogui.hotkey("ctrl", "l")
        time.sleep(self.command_delay)

        self._pyautogui.write(
            normalized_url,
            interval=0.01,
        )

        self._pyautogui.press("enter")
        time.sleep(self.command_delay)

        return {
            "success": True,
            "action": "navigate",
            "url": normalized_url,
        }

    def open_new_window(self):
        """
        Open a new browser window using Ctrl+N.
        """

        self._require_keyboard_control()

        self._pyautogui.hotkey("ctrl", "n")
        time.sleep(self.command_delay)

        return {
            "success": True,
            "action": "open_new_window",
        }

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    def get_status(self):
        """
        Return browser-control status.

        Returns:
            dict: Current controller status.
        """

        return {
            "success": True,
            "browser": self.get_browser_name(),
            "keyboard_control_available": (
                self._pyautogui is not None
            ),
        }


if __name__ == "__main__":
    browser = BrowserControlV6()

    print("==========================================")
    print("       JARVIS V6.6 BROWSER CONTROL")
    print("==========================================")

    status = browser.get_status()

    print(f"[BROWSER] {status['browser']}")
    print(
        "[KEYBOARD CONTROL]",
        status["keyboard_control_available"],
    )

    print("[STATUS] Browser control initialized successfully.")
    print("==========================================")