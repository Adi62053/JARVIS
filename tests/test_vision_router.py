"""
JARVIS V6.5 - Vision Router Test
"""

from tools.vision_router import VisionRouter


def test_vision_router():
    router = VisionRouter()

    result = router.analyze_current_screen()

    assert isinstance(result, dict)

    assert result["success"] is True

    assert "image" in result
    assert "screen" in result
    assert "active_window" in result

    assert result["image"]

    screen = result["screen"]

    assert isinstance(screen, dict)

    assert "image" in screen
    assert "resolution" in screen
    assert "raw_element_count" in screen
    assert "element_count" in screen
    assert "elements" in screen
    assert "full_text" in screen

    resolution = screen["resolution"]

    assert resolution["width"] > 0
    assert resolution["height"] > 0

    assert screen["raw_element_count"] >= (
        screen["element_count"]
    )

    active_window = result["active_window"]

    assert isinstance(active_window, dict)

    assert active_window["detected"] is True

    assert "hwnd" in active_window
    assert "title" in active_window
    assert "process_id" in active_window
    assert "process_name" in active_window
    assert "process_path" in active_window
    assert "window_class" in active_window
    assert "geometry" in active_window

    print(
        "[TEST PASS] "
        "Vision router executed successfully."
    )

    print(f"[IMAGE] {result['image']}")

    print(
        "[RESOLUTION] "
        f"{resolution['width']} x "
        f"{resolution['height']}"
    )

    print(
        "[RAW OCR ELEMENTS] "
        f"{screen['raw_element_count']}"
    )

    print(
        "[CLEAN OCR ELEMENTS] "
        f"{screen['element_count']}"
    )

    print(
        "[ACTIVE WINDOW] "
        f"{active_window['title']}"
    )

    print(
        "[PROCESS] "
        f"{active_window['process_name']}"
    )

    print(
        "[PID] "
        f"{active_window['process_id']}"
    )

    geometry = active_window["geometry"]

    print(
        "[WINDOW SIZE] "
        f"{geometry['width']} x "
        f"{geometry['height']}"
    )


if __name__ == "__main__":
    test_vision_router()