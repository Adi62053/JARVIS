from pathlib import Path

from tools.vision_capture import VisionCapture


def test_screenshot_capture():
    capture = VisionCapture()

    screenshot_path = capture.capture_screen()

    assert isinstance(screenshot_path, Path)
    assert screenshot_path.exists()
    assert screenshot_path.suffix.lower() == ".png"

    print(f"[TEST PASS] Screenshot created: {screenshot_path}")


if __name__ == "__main__":
    test_screenshot_capture()