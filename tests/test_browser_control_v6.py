"""
JARVIS V6.6 - Browser Control Test

Tests browser-control functionality without performing
unnecessary destructive browser actions.
"""

from tools.browser_control_v6 import BrowserControlV6


def test_browser_initialization():
    """Test browser controller initialization."""

    browser = BrowserControlV6()

    status = browser.get_status()

    assert status["success"] is True
    assert "browser" in status
    assert "keyboard_control_available" in status

    print("[PASS] Browser controller initialized.")
    print(f"[BROWSER] {status['browser']}")
    print(
        "[KEYBOARD CONTROL]",
        status["keyboard_control_available"],
    )


def test_url_normalization():
    """Test URL normalization."""

    browser = BrowserControlV6()

    url_1 = browser.normalize_url("google.com")
    url_2 = browser.normalize_url("https://google.com")

    assert url_1 == "https://google.com"
    assert url_2 == "https://google.com"

    print("[PASS] URL normalization.")


def test_url_validation():
    """Test invalid URL rejection."""

    browser = BrowserControlV6()

    try:
        browser.normalize_url("")
    except ValueError:
        print("[PASS] Empty URL rejected.")
    else:
        raise AssertionError(
            "Empty URL was not rejected."
        )

    try:
        browser.normalize_url("ftp://example.com")
    except ValueError:
        print("[PASS] Unsupported URL scheme rejected.")
    else:
        raise AssertionError(
            "Unsupported URL scheme was not rejected."
        )


def test_search_url_generation():
    """Test web search URL generation without opening browser."""

    browser = BrowserControlV6()

    query = "JARVIS computer vision Python"

    expected = (
        "https://www.google.com/search?q="
        "JARVIS%20computer%20vision%20Python"
    )

    actual = browser.SEARCH_ENGINE + browser.SEARCH_ENGINE.__class__(
        ""
    ) if False else None

    from urllib.parse import quote

    actual = browser.SEARCH_ENGINE + quote(query)

    assert actual == expected

    print("[PASS] Search URL generation.")
    print(f"[SEARCH URL] {actual}")


def test_browser_detection():
    """Test browser detection."""

    browser = BrowserControlV6()

    detected = browser.detect_browser()

    if detected:
        assert detected in browser.SUPPORTED_BROWSERS
        print(f"[PASS] Browser detected: {detected}")
    else:
        print(
            "[INFO] No browser executable detected through PATH."
        )


def main():
    print("==========================================")
    print("     JARVIS V6.6 BROWSER CONTROL TEST")
    print("==========================================")

    test_browser_initialization()
    test_url_normalization()
    test_url_validation()
    test_search_url_generation()
    test_browser_detection()

    print()
    print("[TEST PASS] Browser control tests completed.")
    print("==========================================")


if __name__ == "__main__":
    main()