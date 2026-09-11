"""
JARVIS V6.5 - Vision Router

Central integration layer for the JARVIS V6 computer-vision modules.

Responsibilities:
    - Capture the screen
    - Analyze visible text
    - Detect the active window
    - Return one unified vision result

This module does not implement OCR or window detection itself.
It coordinates the existing V6 modules.
"""

from pathlib import Path

from tools.vision_capture import VisionCapture
from tools.vision_analyzer import VisionAnalyzer
from tools.window_control_v6 import WindowControlV6


class VisionRouter:
    """
    JARVIS V6.5 Vision Integration Router.
    """

    def __init__(
        self,
        capture=None,
        analyzer=None,
        window_control=None,
    ):
        """
        Initialize the V6 vision components.

        Optional dependency injection keeps the router modular
        and easy to test.
        """

        self.capture = capture or VisionCapture()
        self.analyzer = analyzer or VisionAnalyzer()
        self.window_control = (
            window_control or WindowControlV6()
        )

        self.last_result = None

    def capture_screen(self):
        """
        Capture the current screen.

        Returns:
            Path or capture result returned by VisionCapture.
        """

        return self.capture.capture_screen()

    def analyze_screen(self, image_path):
        """
        Analyze a supplied screenshot.

        Returns:
            Structured screen-analysis dictionary.
        """

        return self.analyzer.analyze(image_path)

    def detect_active_window(self):
        """
        Detect the currently active window.

        Returns:
            Structured active-window dictionary.
        """

        return self.window_control.detect_active_window()

    def analyze_current_screen(self):
        """
        Capture and analyze the current screen together
        with the active window.

        Returns:
            Unified V6.5 vision result.
        """

        capture_result = self.capture_screen()

        image_path = self._resolve_capture_path(
            capture_result
        )

        screen_analysis = self.analyze_screen(
            image_path
        )

        active_window = self.detect_active_window()

        result = {
            "success": True,
            "image": str(image_path),
            "screen": screen_analysis,
            "active_window": active_window,
        }

        self.last_result = result

        return result

    @staticmethod
    def _resolve_capture_path(capture_result):
        """
        Convert VisionCapture's return value into a usable
        screenshot path.

        Supports:
            - pathlib.Path
            - string path
            - dictionaries containing common path keys
        """

        if isinstance(capture_result, Path):
            return capture_result

        if isinstance(capture_result, str):
            return Path(capture_result)

        if isinstance(capture_result, dict):
            possible_keys = (
                "image",
                "image_path",
                "path",
                "file",
                "screenshot",
            )

            for key in possible_keys:
                value = capture_result.get(key)

                if value:
                    return Path(value)

        raise TypeError(
            "VisionCapture returned an unsupported result: "
            f"{type(capture_result).__name__}"
        )

    def get_last_result(self):
        """
        Return the most recent unified vision result.
        """

        return self.last_result


if __name__ == "__main__":
    router = VisionRouter()

    result = router.analyze_current_screen()

    print("==========================================")
    print("       JARVIS V6.5 VISION ROUTER")
    print("==========================================")

    print(f"[SUCCESS] {result['success']}")
    print(f"[IMAGE] {result['image']}")

    screen = result["screen"]

    resolution = screen["resolution"]

    print(
        "[RESOLUTION] "
        f"{resolution['width']} x "
        f"{resolution['height']}"
    )

    print(
        "[OCR ELEMENTS] "
        f"{screen['element_count']}"
    )

    active_window = result["active_window"]

    print(
        "[ACTIVE WINDOW] "
        f"{active_window.get('title', '')}"
    )

    print(
        "[PROCESS] "
        f"{active_window.get('process_name', '')}"
    )

    print("==========================================")