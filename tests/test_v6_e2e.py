"""
JARVIS V6.9 - End-to-End Test

Tests the complete V6 Computer Vision stack without launching
the interactive JARVIS main loop.

Covered:
    V6.1 - Screen Capture
    V6.2 - OCR
    V6.3 - Screen Analyzer
    V6.4 - Active Window
    V6.5 - Vision Router
    V6.6 - Browser Control
    V6.7 - Vision Command Layer
    V6.8 - JARVIS Integration

This test does not modify system settings and does not require
Ollama, wake-word activation, or microphone input.
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from tools.vision_capture import VisionCapture
from tools.vision_ocr import VisionOCR
from tools.vision_analyzer import VisionAnalyzer
from tools.window_control_v6 import WindowControlV6
from tools.vision_router import VisionRouter
from tools.browser_control_v6 import BrowserControlV6
from tools.vision_command_layer import VisionCommandLayer


def check(condition, message):
    """Print a standardized PASS/FAIL result."""

    if condition:
        print(f"[PASS] {message}")
        return True

    print(f"[FAIL] {message}")
    return False


# ---------------------------------------------------------
# V6 Module Imports
# ---------------------------------------------------------

def test_imports():
    """Verify all V6 modules can be imported."""

    print("\n--- V6 Module Imports ---")

    results = []

    results.append(
        check(
            VisionCapture is not None,
            "V6.1 Screen Capture import",
        )
    )

    results.append(
        check(
            VisionOCR is not None,
            "V6.2 OCR import",
        )
    )

    results.append(
        check(
            VisionAnalyzer is not None,
            "V6.3 Screen Analyzer import",
        )
    )

    results.append(
        check(
            WindowControlV6 is not None,
            "V6.4 Active Window import",
        )
    )

    results.append(
        check(
            VisionRouter is not None,
            "V6.5 Vision Router import",
        )
    )

    results.append(
        check(
            BrowserControlV6 is not None,
            "V6.6 Browser Control import",
        )
    )

    results.append(
        check(
            VisionCommandLayer is not None,
            "V6.7 Vision Command Layer import",
        )
    )

    return all(results)


# ---------------------------------------------------------
# V6.1 Screen Capture
# ---------------------------------------------------------

def test_capture():
    """Test V6.1 screenshot capture."""

    print("\n--- V6.1 Screen Capture ---")

    try:
        capture = VisionCapture()

        image_path = capture.capture_screen()

        if not image_path:
            return check(
                False,
                "Screenshot capture returned no path",
            )

        path = Path(image_path)

        if not path.exists():
            return check(
                False,
                "Captured screenshot file does not exist",
            )

        if path.stat().st_size <= 0:
            return check(
                False,
                "Captured screenshot file is empty",
            )

        print(f"[IMAGE] {path}")
        print(f"[SIZE] {path.stat().st_size} bytes")

        return check(
            True,
            "Screenshot captured successfully",
        )

    except Exception as exc:
        print(f"[ERROR] {exc}")
        return check(
            False,
            "V6.1 screenshot capture",
        )


# ---------------------------------------------------------
# V6.2 OCR
# ---------------------------------------------------------

def test_ocr():
    """Test V6.2 OCR using a fresh screenshot."""

    print("\n--- V6.2 OCR ---")

    try:
        capture = VisionCapture()

        image_path = capture.capture_screen()

        ocr = VisionOCR()

        text = ocr.extract_text(
            str(image_path)
        )

        if text is None:
            return check(
                False,
                "OCR returned None",
            )

        print(f"[CHARACTERS] {len(text)}")

        if text.strip():
            print("[TEXT PREVIEW]")
            print(text[:500])

            return check(
                True,
                "OCR executed successfully",
            )

        print(
            "[INFO] OCR returned no readable text."
        )

        return check(
            True,
            "OCR executed successfully with no text detected",
        )

    except Exception as exc:
        print(f"[ERROR] {exc}")

        return check(
            False,
            "V6.2 OCR execution",
        )


# ---------------------------------------------------------
# V6.3 Screen Analyzer
# ---------------------------------------------------------

def test_analyzer():
    """Test V6.3 structured screen analysis."""

    print("\n--- V6.3 Screen Analyzer ---")

    try:
        capture = VisionCapture()

        image_path = capture.capture_screen()

        analyzer = VisionAnalyzer()

        result = analyzer.analyze(
            str(image_path)
        )

        if not isinstance(result, dict):
            return check(
                False,
                "Analyzer did not return a dictionary",
            )

        required_keys = [
            "image",
            "resolution",
            "raw_element_count",
            "element_count",
            "elements",
            "full_text",
        ]

        missing = [
            key
            for key in required_keys
            if key not in result
        ]

        if missing:
            print(f"[MISSING] {missing}")

            return check(
                False,
                "Analyzer result structure",
            )

        print(
            f"[RESOLUTION] {result['resolution']}"
        )

        print(
            f"[RAW ELEMENTS] "
            f"{result['raw_element_count']}"
        )

        print(
            f"[CLEAN ELEMENTS] "
            f"{result['element_count']}"
        )

        return check(
            True,
            "Structured screen analysis successful",
        )

    except Exception as exc:
        print(f"[ERROR] {exc}")

        return check(
            False,
            "V6.3 screen analysis",
        )


# ---------------------------------------------------------
# V6.4 Active Window
# ---------------------------------------------------------

def test_active_window():
    """Test V6.4 active-window detection."""

    print("\n--- V6.4 Active Window ---")

    try:
        controller = WindowControlV6()

        result = (
            controller.get_active_window()
        )

        if not isinstance(result, dict):
            return check(
                False,
                "Active-window result is not a dictionary",
            )

        print(f"[WINDOW] {result}")

        has_title = bool(
            result.get("title")
            or result.get("window_title")
        )

        return check(
            has_title,
            "Active window detected successfully",
        )

    except Exception as exc:
        print(f"[ERROR] {exc}")

        return check(
            False,
            "V6.4 active-window detection",
        )


# ---------------------------------------------------------
# V6.5 Vision Router
# ---------------------------------------------------------

def test_router():
    """Test V6.5 unified vision router."""

    print("\n--- V6.5 Vision Router ---")

    try:
        router = VisionRouter()

        result = (
            router.analyze_current_screen()
        )

        if not isinstance(result, dict):
            return check(
                False,
                "Vision Router returned invalid result",
            )

        if "success" not in result:
            return check(
                False,
                "Vision Router result missing success field",
            )

        if not result["success"]:
            print(
                f"[ROUTER RESULT] {result}"
            )

            return check(
                False,
                "Vision Router reported failure",
            )

        required_keys = [
            "image",
            "screen",
            "active_window",
        ]

        missing = [
            key
            for key in required_keys
            if key not in result
        ]

        if missing:
            print(f"[MISSING] {missing}")

            return check(
                False,
                "Vision Router result structure",
            )

        print(
            "[ROUTER] Unified screen result received."
        )

        return check(
            True,
            "Vision Router executed successfully",
        )

    except Exception as exc:
        print(f"[ERROR] {exc}")

        return check(
            False,
            "V6.5 Vision Router",
        )


# ---------------------------------------------------------
# V6.6 Browser Control
# ---------------------------------------------------------

def test_browser_control():
    """
    Test V6.6 browser controller using only non-destructive
    local validation methods.

    We intentionally do not open a browser here.
    Browser side-effect commands were already verified
    during the live V6.8 integration test.
    """

    print("\n--- V6.6 Browser Control ---")

    try:
        browser = BrowserControlV6()

        # -------------------------------------------------
        # URL normalization
        # -------------------------------------------------

        normalized = browser.normalize_url(
            "google.com"
        )

        print(
            f"[NORMALIZED URL] {normalized}"
        )

        if normalized != "https://google.com":
            return check(
                False,
                "Browser URL normalization",
            )

        # -------------------------------------------------
        # Empty URL rejection
        # -------------------------------------------------

        try:
            browser.normalize_url("")

            return check(
                False,
                "Empty URL rejection",
            )

        except Exception:
            print(
                "[PASS] Empty URL rejected."
            )

        # -------------------------------------------------
        # Unsupported scheme rejection
        # -------------------------------------------------

        try:
            browser.normalize_url(
                "ftp://example.com"
            )

            return check(
                False,
                "Unsupported URL scheme rejection",
            )

        except Exception:
            print(
                "[PASS] Unsupported URL scheme rejected."
            )

        # -------------------------------------------------
        # Browser status
        # -------------------------------------------------

        status = browser.get_status()

        if not isinstance(status, dict):
            return check(
                False,
                "Browser status result",
            )

        print(
            f"[BROWSER STATUS] {status}"
        )

        return check(
            True,
            "Browser controller validated",
        )

    except Exception as exc:
        print(f"[ERROR] {exc}")

        return check(
            False,
            "V6.6 browser controller",
        )


# ---------------------------------------------------------
# V6.7 Pure Command Classification
# ---------------------------------------------------------

def test_command_classification():
    """
    Test V6.7 command classification.

    IMPORTANT:
        classify() must not execute any action.

    The expected action names are the actual standardized
    V6 action identifiers used by VisionCommandLayer.
    """

    print("\n--- V6.7 Command Classification ---")

    try:
        layer = VisionCommandLayer()

        commands = {
            "what is on my screen":
                "analyze_screen",

            "what application is open":
                "detect_active_window",

            "what text is visible":
                "read_screen_text",

            "open google":
                "open_google",

            "search google for python":
                "search_web",

            "open a new tab":
                "new_tab",

            "go back":
                "back",

            "go forward":
                "forward",

            "refresh the page":
                "refresh",
        }

        for command, expected in commands.items():

            action = layer.classify(
                command
            )

            print(
                f"[CLASSIFY] "
                f"{command!r} -> {action!r}"
            )

            if action != expected:
                print(
                    f"[EXPECTED] {expected!r}, "
                    f"[GOT] {action!r}"
                )

                return check(
                    False,
                    f"Classification: {command}",
                )

        # -------------------------------------------------
        # Verify unknown commands return None
        # -------------------------------------------------

        unknown_commands = [
            "",
            "hello jarvis",
            "play music",
            "open calculator",
        ]

        for command in unknown_commands:

            action = layer.classify(
                command
            )

            print(
                f"[UNKNOWN] "
                f"{command!r} -> {action!r}"
            )

            if action is not None:
                return check(
                    False,
                    f"Unknown classification: {command}",
                )

        return check(
            True,
            "All V6.7 commands classified correctly",
        )

    except AttributeError:
        return check(
            False,
            "VisionCommandLayer.classify() is missing",
        )

    except Exception as exc:
        print(f"[ERROR] {exc}")

        return check(
            False,
            "V6.7 command classification",
        )


# ---------------------------------------------------------
# V6.7 Command Execution
# ---------------------------------------------------------

def test_command_execution():
    """
    Test V6.7 command execution using non-destructive
    screen-analysis commands.

    Browser side-effect commands are intentionally excluded
    because they were already verified in the live V6.8 test.
    """

    print("\n--- V6.7 Command Execution ---")

    try:
        layer = VisionCommandLayer()

        commands = [
            "what application is open",
            "what is on my screen",
            "what text is visible",
        ]

        for command in commands:

            result = layer.execute(
                command
            )

            if not isinstance(result, dict):
                return check(
                    False,
                    f"Execution result: {command}",
                )

            print(
                f"[COMMAND] {command}"
            )

            print(
                f"[ACTION] "
                f"{result.get('action')}"
            )

            print(
                f"[SUCCESS] "
                f"{result.get('success')}"
            )

            if not result.get("success"):
                return check(
                    False,
                    f"Vision command execution: {command}",
                )

        return check(
            True,
            "Non-destructive V6.7 commands executed successfully",
        )

    except Exception as exc:
        print(f"[ERROR] {exc}")

        return check(
            False,
            "V6.7 command execution",
        )


# ---------------------------------------------------------
# V6 Safety / Unknown Commands
# ---------------------------------------------------------

def test_unknown_commands():
    """Verify unsupported commands are safely rejected."""

    print("\n--- V6 Command Safety / Unknown Commands ---")

    try:
        layer = VisionCommandLayer()

        unknown_commands = [
            "",
            "hello jarvis",
            "play some music",
            "do something random",
        ]

        for command in unknown_commands:

            result = layer.execute(
                command
            )

            if not isinstance(result, dict):
                return check(
                    False,
                    f"Unknown command result: {command!r}",
                )

            if result.get("success") is True:
                print(
                    f"[UNEXPECTED SUCCESS] "
                    f"{command!r}"
                )

                return check(
                    False,
                    f"Unknown command rejection: {command!r}",
                )

        return check(
            True,
            "Unknown commands safely rejected",
        )

    except Exception as exc:
        print(f"[ERROR] {exc}")

        return check(
            False,
            "Unknown command handling",
        )


# ---------------------------------------------------------
# V6.8 JARVIS Integration
# ---------------------------------------------------------

def test_main_integration():
    """
    Verify main.py can import and exposes the V6 integration.

    This does not start the microphone or wake-word loop.
    """

    print("\n--- V6.8 JARVIS Integration ---")

    try:
        import main

        if not hasattr(main, "main"):
            return check(
                False,
                "main.py main() function",
            )

        if not hasattr(
            main,
            "VisionCommandLayer",
        ):
            return check(
                False,
                "main.py VisionCommandLayer integration",
            )

        return check(
            True,
            "main.py V6.8 integration import",
        )

    except Exception as exc:
        print(f"[ERROR] {exc}")

        return check(
            False,
            "main.py V6.8 integration",
        )


# ---------------------------------------------------------
# Main Test Runner
# ---------------------------------------------------------

def main():
    """Run the complete V6.9 test suite."""

    print("=" * 50)
    print("       JARVIS V6.9 END-TO-END TEST")
    print("=" * 50)

    tests = [
        (
            "Module imports",
            test_imports,
        ),
        (
            "Screen capture",
            test_capture,
        ),
        (
            "OCR",
            test_ocr,
        ),
        (
            "Screen analyzer",
            test_analyzer,
        ),
        (
            "Active window",
            test_active_window,
        ),
        (
            "Vision router",
            test_router,
        ),
        (
            "Browser control",
            test_browser_control,
        ),
        (
            "Command classification",
            test_command_classification,
        ),
        (
            "Command execution",
            test_command_execution,
        ),
        (
            "Unknown command safety",
            test_unknown_commands,
        ),
        (
            "JARVIS integration",
            test_main_integration,
        ),
    ]

    passed = 0
    failed = 0

    for name, test_function in tests:

        try:
            result = test_function()

            if result:
                passed += 1
            else:
                failed += 1

        except Exception as exc:
            failed += 1

            print(
                f"[UNEXPECTED ERROR] "
                f"{name}: {exc}"
            )

    print("\n" + "=" * 50)
    print("             V6.9 TEST SUMMARY")
    print("=" * 50)

    print(f"[PASSED] {passed}")
    print(f"[FAILED] {failed}")

    if failed == 0:

        print(
            "\n[TEST PASS] "
            "JARVIS V6.9 End-to-End testing passed."
        )

        print(
            "[STATUS] "
            "V6 is ready for final freeze."
        )

        return 0

    print(
        "\n[TEST FAIL] "
        "V6.9 has failures."
    )

    print(
        "[STATUS] "
        "Do not freeze V6 yet."
    )

    return 1


if __name__ == "__main__":
    raise SystemExit(main())

