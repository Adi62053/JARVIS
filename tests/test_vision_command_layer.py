"""
JARVIS V6.7 - Vision Command Layer Test
"""

from tools.vision_command_layer import VisionCommandLayer


class MockVisionRouter:
    """Mock router for deterministic command tests."""

    def analyze_current_screen(self):
        return {
            "success": True,
            "image": "test.png",
            "screen": {
                "resolution": {
                    "width": 1920,
                    "height": 1080,
                },
                "elements": [
                    {"text": "JARVIS"},
                    {"text": "Python"},
                ],
                "full_text": "JARVIS Python",
            },
            "active_window": {
                "title": "JARVIS - Visual Studio Code",
                "process_name": "Code.exe",
            },
        }

    def detect_active_window(self):
        return {
            "title": "JARVIS - Visual Studio Code",
            "process_name": "Code.exe",
        }


class MockBrowserControl:
    """Mock browser controller for safe command tests."""

    def open_url(self, url):
        return {
            "success": True,
            "action": "open_url",
            "url": url,
        }

    def search_web(self, query):
        return {
            "success": True,
            "action": "search_web",
            "query": query,
        }

    def open_new_tab(self):
        return {
            "success": True,
            "action": "open_new_tab",
        }

    def refresh_page(self):
        return {
            "success": True,
            "action": "refresh_page",
        }

    def go_back(self):
        return {
            "success": True,
            "action": "go_back",
        }

    def go_forward(self):
        return {
            "success": True,
            "action": "go_forward",
        }


def build_layer():
    """Create a test command layer."""

    return VisionCommandLayer(
        vision_router=MockVisionRouter(),
        browser_control=MockBrowserControl(),
    )


def test_screen_analysis():
    """Test screen-analysis command."""

    layer = build_layer()

    result = layer.execute(
        "what is on my screen"
    )

    assert result["success"] is True
    assert result["action"] == "analyze_screen"
    assert "Visual Studio Code" in result["response"]

    print("[PASS] Screen analysis command.")


def test_active_window():
    """Test active-window command."""

    layer = build_layer()

    result = layer.execute(
        "what application is open"
    )

    assert result["success"] is True
    assert result["action"] == "detect_active_window"
    assert "Code.exe" in result["response"]

    print("[PASS] Active window command.")


def test_ocr():
    """Test OCR command."""

    layer = build_layer()

    result = layer.execute(
        "what text is visible"
    )

    assert result["success"] is True
    assert result["action"] == "read_screen_text"
    assert "JARVIS Python" in result["response"]

    print("[PASS] OCR command.")


def test_open_google():
    """Test Google command."""

    layer = build_layer()

    result = layer.execute(
        "open google"
    )

    assert result["success"] is True
    assert result["action"] == "open_google"
    assert result["data"]["url"] == (
        "https://www.google.com"
    )

    print("[PASS] Open Google command.")


def test_search():
    """Test search command."""

    layer = build_layer()

    result = layer.execute(
        "search google for Python OCR"
    )

    assert result["success"] is True
    assert result["action"] == "search_web"
    assert result["data"]["query"] == "Python OCR"

    print("[PASS] Web search command.")


def test_new_tab():
    """Test new-tab command."""

    layer = build_layer()

    result = layer.execute(
        "open a new tab"
    )

    assert result["success"] is True
    assert result["action"] == "open_new_tab"

    print("[PASS] New tab command.")


def test_refresh():
    """Test refresh command."""

    layer = build_layer()

    result = layer.execute(
        "refresh the page"
    )

    assert result["success"] is True
    assert result["action"] == "refresh_page"

    print("[PASS] Refresh command.")


def test_back():
    """Test browser back command."""

    layer = build_layer()

    result = layer.execute("go back")

    assert result["success"] is True
    assert result["action"] == "go_back"

    print("[PASS] Browser back command.")


def test_forward():
    """Test browser forward command."""

    layer = build_layer()

    result = layer.execute("go forward")

    assert result["success"] is True
    assert result["action"] == "go_forward"

    print("[PASS] Browser forward command.")


def test_unknown_command():
    """Test unknown-command handling."""

    layer = build_layer()

    result = layer.execute(
        "play some music"
    )

    assert result["success"] is False
    assert result["action"] == "unknown"

    print("[PASS] Unknown command handling.")


def test_empty_command():
    """Test empty command handling."""

    layer = build_layer()

    result = layer.execute("")

    assert result["success"] is False
    assert result["action"] == "unknown"

    print("[PASS] Empty command handling.")


def main():
    print("==========================================")
    print("   JARVIS V6.7 VISION COMMAND TEST")
    print("==========================================")

    test_screen_analysis()
    test_active_window()
    test_ocr()
    test_open_google()
    test_search()
    test_new_tab()
    test_refresh()
    test_back()
    test_forward()
    test_unknown_command()
    test_empty_command()

    print()
    print(
        "[TEST PASS] Vision command layer tests completed."
    )
    print("==========================================")


if __name__ == "__main__":
    main()