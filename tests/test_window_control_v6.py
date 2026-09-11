"""
JARVIS V6.4 - Active Window Detection Test
"""

from tools.window_control_v6 import WindowControlV6


def test_active_window_detection():
    detector = WindowControlV6()

    result = detector.detect_active_window()

    assert isinstance(result, dict)
    assert result["detected"] is True

    assert "hwnd" in result
    assert "title" in result
    assert "process_id" in result
    assert "process_name" in result
    assert "process_path" in result
    assert "window_class" in result
    assert "visible" in result
    assert "maximized" in result
    assert "minimized" in result
    assert "geometry" in result

    assert isinstance(result["hwnd"], int)
    assert result["hwnd"] > 0

    assert isinstance(result["title"], str)
    assert isinstance(result["process_name"], str)
    assert isinstance(result["process_path"], str)
    assert isinstance(result["window_class"], str)

    geometry = result["geometry"]

    assert isinstance(geometry, dict)

    assert "x" in geometry
    assert "y" in geometry
    assert "width" in geometry
    assert "height" in geometry

    assert isinstance(geometry["x"], int)
    assert isinstance(geometry["y"], int)
    assert isinstance(geometry["width"], int)
    assert isinstance(geometry["height"], int)

    assert geometry["width"] >= 0
    assert geometry["height"] >= 0

    print(
        "[TEST PASS] "
        "Active window detection executed successfully."
    )

    print(f"[TITLE] {result['title']}")
    print(f"[PROCESS] {result['process_name']}")
    print(f"[PID] {result['process_id']}")
    print(f"[CLASS] {result['window_class']}")
    print(f"[PATH] {result['process_path']}")
    print(f"[VISIBLE] {result['visible']}")
    print(f"[MAXIMIZED] {result['maximized']}")
    print(f"[MINIMIZED] {result['minimized']}")

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


if __name__ == "__main__":
    test_active_window_detection()