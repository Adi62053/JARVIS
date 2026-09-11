from pathlib import Path
from datetime import datetime

from PIL import ImageGrab


class VisionCapture:
    """
    JARVIS V6.1 - Screenshot Capture

    Responsible only for capturing the current screen.
    """

    def __init__(self, output_dir="data/screenshots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def capture_screen(self):
        """
        Capture the full screen and save it as a PNG file.

        Returns:
            Path: Path to the saved screenshot.
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"screen_{timestamp}.png"
        output_path = self.output_dir / filename

        screenshot = ImageGrab.grab()
        screenshot.save(output_path, "PNG")

        return output_path


if __name__ == "__main__":
    capture = VisionCapture()
    screenshot_path = capture.capture_screen()

    print("==========================================")
    print("       JARVIS V6.1 SCREEN CAPTURE")
    print("==========================================")
    print(f"[OK] Screenshot captured")
    print(f"[FILE] {screenshot_path}")
    print("==========================================")