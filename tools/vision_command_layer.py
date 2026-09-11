"""
JARVIS V6.7 - Vision Command Layer

Converts natural-language vision/browser commands into
deterministic V6 operations.

This layer sits above:
    - VisionRouter
    - BrowserControlV6

It does not use the LLM for command interpretation.

Architecture:

    User Command
         |
         v
    classify()              <-- NO side effects
         |
         v
    is_vision_command()
         |
         v
    execute()               <-- executes exactly once
         |
         +--> VisionRouter
         |
         +--> BrowserControlV6
"""

from __future__ import annotations

from tools.browser_control_v6 import BrowserControlV6
from tools.vision_router import VisionRouter


class VisionCommandLayer:
    """
    JARVIS V6.7 command interpreter for vision and browser actions.
    """

    SCREEN_COMMANDS = (
        "what is on my screen",
        "what's on my screen",
        "what do you see",
        "what can you see",
        "read my screen",
        "read the screen",
        "analyze my screen",
        "analyze the screen",
        "screen analysis",
    )

    ACTIVE_WINDOW_COMMANDS = (
        "what application is open",
        "what app is open",
        "what application am i using",
        "what app am i using",
        "what window is open",
        "what window is active",
        "which window is active",
        "active window",
    )

    OCR_COMMANDS = (
        "what text is visible",
        "what text do you see",
        "read visible text",
        "read visible text on screen",
        "read the text on screen",
        "show visible text",
    )

    GOOGLE_COMMANDS = (
        "open google",
        "open google.com",
        "go to google",
        "go to google.com",
    )

    NEW_TAB_COMMANDS = (
        "open a new tab",
        "open new tab",
        "new tab",
    )

    REFRESH_COMMANDS = (
        "refresh",
        "refresh the page",
        "refresh page",
        "refresh browser",
        "reload the page",
        "reload page",
    )

    BACK_COMMANDS = (
        "go back",
        "go backward",
        "browser back",
        "back page",
        "back",
    )

    FORWARD_COMMANDS = (
        "go forward",
        "browser forward",
        "forward page",
        "forward",
    )

    SEARCH_PREFIXES = (
        "search google for ",
        "search the web for ",
        "search web for ",
        "search for ",
    )

    def __init__(self, vision_router=None, browser_control=None):
        """
        Initialize the command layer.

        Dependencies can be injected for testing.
        """

        self.vision_router = (
            vision_router or VisionRouter()
        )

        self.browser_control = (
            browser_control or BrowserControlV6()
        )

        self.last_result = None

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    @staticmethod
    def _normalize_command(command):
        """Normalize a user command."""

        if not isinstance(command, str):
            raise TypeError("Command must be a string.")

        return " ".join(
            command.strip().lower().split()
        )

    @staticmethod
    def _starts_with_any(text, phrases):
        """Check whether text starts with one of the phrases."""

        return any(
            text.startswith(phrase)
            for phrase in phrases
        )

    # ---------------------------------------------------------
    # Pure command classification
    # ---------------------------------------------------------

    def classify(self, command):
        """
        Classify a V6 command without executing it.

        IMPORTANT:
            This method must have NO side effects.

        It must NOT:
            - capture a screenshot
            - run OCR
            - analyze the screen
            - detect the active window
            - open a browser
            - open a tab
            - refresh a page
            - navigate backward/forward
            - perform a web search

        Returns:
            str | None

        Examples:
            "what is on my screen"
                -> "analyze_screen"

            "what application is open"
                -> "detect_active_window"

            "what text is visible"
                -> "read_screen_text"

            "open google"
                -> "open_google"

            "search google for python"
                -> "search_web"

            Unknown command
                -> None
        """

        if not isinstance(command, str):
            return None

        normalized = self._normalize_command(command)

        if not normalized:
            return None

        # Screen analysis
        if normalized in self.SCREEN_COMMANDS:
            return "analyze_screen"

        # Active window
        if normalized in self.ACTIVE_WINDOW_COMMANDS:
            return "detect_active_window"

        # OCR
        if normalized in self.OCR_COMMANDS:
            return "read_screen_text"

        # Google
        if normalized in self.GOOGLE_COMMANDS:
            return "open_google"

        # New tab
        if normalized in self.NEW_TAB_COMMANDS:
            return "new_tab"

        # Refresh
        if normalized in self.REFRESH_COMMANDS:
            return "refresh"

        # Back
        if normalized in self.BACK_COMMANDS:
            return "back"

        # Forward
        if normalized in self.FORWARD_COMMANDS:
            return "forward"

        # Web search
        if self._starts_with_any(
            normalized,
            self.SEARCH_PREFIXES,
        ):
            # Make sure a query actually exists.
            for prefix in self.SEARCH_PREFIXES:
                if normalized.startswith(prefix):
                    query = normalized[
                        len(prefix):
                    ].strip()

                    if query:
                        return "search_web"

                    return None

        return None

    def is_vision_command(self, command):
        """
        Return True if the command belongs to V6 vision/browser control.

        IMPORTANT:
            This method is completely side-effect free.

        It is safe to call from main.py command detection.
        """

        return self.classify(command) is not None

    # ---------------------------------------------------------
    # Screen understanding
    # ---------------------------------------------------------

    def _handle_screen_analysis(self):
        """Analyze the current screen."""

        result = self.vision_router.analyze_current_screen()

        response = self._build_screen_response(result)

        return {
            "success": True,
            "action": "analyze_screen",
            "response": response,
            "data": result,
        }

    def _handle_active_window(self):
        """Detect the currently active window."""

        window = self.vision_router.detect_active_window()

        title = window.get("title") or "Unknown"
        process = window.get("process_name") or "Unknown"

        response = (
            f"The active application is {process}. "
            f"The window title is {title}."
        )

        return {
            "success": True,
            "action": "detect_active_window",
            "response": response,
            "data": window,
        }

    def _handle_ocr(self):
        """Capture and extract visible screen text."""

        result = self.vision_router.analyze_current_screen()

        screen = result.get("screen", {})

        full_text = screen.get(
            "full_text",
            "",
        ).strip()

        if full_text:
            response = (
                "I can see the following text on the screen: "
                + full_text
            )
        else:
            response = (
                "I could not detect readable text."
            )

        return {
            "success": True,
            "action": "read_screen_text",
            "response": response,
            "data": result,
        }

    @staticmethod
    def _build_screen_response(result):
        """Build a concise response from screen analysis."""

        screen = result.get("screen", {})
        window = result.get("active_window", {})

        resolution = screen.get(
            "resolution",
            {},
        )

        elements = screen.get(
            "elements",
            [],
        )

        title = window.get("title") or "Unknown"
        process = (
            window.get("process_name")
            or "Unknown"
        )

        if isinstance(resolution, dict):
            width = resolution.get("width")
            height = resolution.get("height")

            if width and height:
                resolution_text = (
                    f"{width} by {height}"
                )
            else:
                resolution_text = (
                    "unknown resolution"
                )
        else:
            resolution_text = str(
                resolution
            )

        return (
            f"The active application is {process}. "
            f"The window title is {title}. "
            f"The screen resolution is "
            f"{resolution_text}. "
            f"I detected {len(elements)} "
            f"readable screen elements."
        )

    # ---------------------------------------------------------
    # Browser actions
    # ---------------------------------------------------------

    def _handle_new_tab(self):
        """Open a new browser tab."""

        result = (
            self.browser_control.open_new_tab()
        )

        return {
            "success": result["success"],
            "action": result["action"],
            "response": (
                "Opening a new browser tab."
            ),
            "data": result,
        }

    def _handle_refresh(self):
        """Refresh the browser page."""

        result = (
            self.browser_control.refresh_page()
        )

        return {
            "success": result["success"],
            "action": result["action"],
            "response": (
                "Refreshing the page."
            ),
            "data": result,
        }

    def _handle_back(self):
        """Navigate backward."""

        result = (
            self.browser_control.go_back()
        )

        return {
            "success": result["success"],
            "action": result["action"],
            "response": (
                "Going back one page."
            ),
            "data": result,
        }

    def _handle_forward(self):
        """Navigate forward."""

        result = (
            self.browser_control.go_forward()
        )

        return {
            "success": result["success"],
            "action": result["action"],
            "response": (
                "Going forward one page."
            ),
            "data": result,
        }

    def _handle_open_google(self):
        """Open Google."""

        result = self.browser_control.open_url(
            "https://www.google.com"
        )

        return {
            "success": result["success"],
            "action": "open_google",
            "response": "Opening Google.",
            "data": result,
        }

    def _handle_search(self, query):
        """Search the web."""

        result = (
            self.browser_control.search_web(
                query
            )
        )

        return {
            "success": result["success"],
            "action": "search_web",
            "response": (
                f"Searching the web for {query}."
            ),
            "data": result,
        }

    # ---------------------------------------------------------
    # Search query extraction
    # ---------------------------------------------------------

    @staticmethod
    def _extract_search_query(command):
        """
        Extract the search query from a search command.

        Returns:
            str
        """

        if not isinstance(command, str):
            return ""

        normalized = (
            " ".join(
                command.strip()
                .lower()
                .split()
            )
        )

        prefixes = (
            "search google for ",
            "search the web for ",
            "search web for ",
            "search for ",
        )

        for prefix in prefixes:
            if normalized.startswith(prefix):
                # Preserve the user's original query casing
                # where possible.
                original = command.strip()

                query = original[
                    len(prefix):
                ].strip()

                return query

        return ""

    # ---------------------------------------------------------
    # Command execution
    # ---------------------------------------------------------

    def execute(self, command):
        """
        Execute a natural-language V6.7 command.

        Command recognition is delegated to classify().

        Returns:
            dict containing:
                success
                action
                response
                data
        """

        normalized = self._normalize_command(
            command
        )

        if not normalized:
            result = {
                "success": False,
                "action": "unknown",
                "response": (
                    "Please specify a vision command."
                ),
                "data": None,
            }

            self.last_result = result
            return result

        # -----------------------------------------------------
        # PURE CLASSIFICATION
        # -----------------------------------------------------

        action = self.classify(command)

        # Unknown command
        if action is None:
            result = {
                "success": False,
                "action": "unknown",
                "response": (
                    "I do not recognize that "
                    "V6 vision command."
                ),
                "data": None,
            }

            self.last_result = result
            return result

        # -----------------------------------------------------
        # EXECUTION
        #
        # IMPORTANT:
        # Each action is executed exactly once.
        # -----------------------------------------------------

        if action == "analyze_screen":
            result = (
                self._handle_screen_analysis()
            )

        elif action == "detect_active_window":
            result = (
                self._handle_active_window()
            )

        elif action == "read_screen_text":
            result = self._handle_ocr()

        elif action == "open_google":
            result = self._handle_open_google()

        elif action == "new_tab":
            result = self._handle_new_tab()

        elif action == "refresh":
            result = self._handle_refresh()

        elif action == "back":
            result = self._handle_back()

        elif action == "forward":
            result = self._handle_forward()

        elif action == "search_web":
            query = self._extract_search_query(
                command
            )

            if not query:
                result = {
                    "success": False,
                    "action": "search_web",
                    "response": (
                        "Please specify what you "
                        "want me to search for."
                    ),
                    "data": None,
                }
            else:
                result = self._handle_search(
                    query
                )

        else:
            # Defensive fallback.
            result = {
                "success": False,
                "action": "unknown",
                "response": (
                    "I do not recognize that "
                    "V6 vision command."
                ),
                "data": None,
            }

        self.last_result = result

        return result

    # ---------------------------------------------------------
    # State
    # ---------------------------------------------------------

    def get_last_result(self):
        """Return the most recent command result."""

        return self.last_result


if __name__ == "__main__":
    layer = VisionCommandLayer()

    print("==========================================")
    print("       JARVIS V6.7 VISION COMMAND")
    print("==========================================")

    print(
        "[STATUS] Vision command layer initialized."
    )

    print("[STATUS] Supported command categories:")
    print("  - Screen analysis")
    print("  - Active window")
    print("  - OCR")
    print("  - Browser navigation")
    print("  - Web search")

    print("==========================================")

