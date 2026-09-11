from pathlib import Path

import pytesseract
from PIL import Image


class VisionOCR:
    """
    JARVIS V6.2 - OCR / Screen Text Detection

    Responsible for extracting visible text from screenshots.
    """

    def __init__(self, tesseract_path=None):
        """
        Initialize the OCR engine.

        Args:
            tesseract_path: Optional path to the Tesseract executable.
        """

        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def extract_text(self, image_path):
        """
        Extract text from an image.

        Args:
            image_path: Path to the image.

        Returns:
            str: Extracted text.
        """

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image file not found: {image_path}"
            )

        with Image.open(image_path) as image:
            text = pytesseract.image_to_string(image)

        return text.strip()


if __name__ == "__main__":
    screenshots_dir = Path("data/screenshots")

    screenshots = sorted(
        screenshots_dir.glob("*.png"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    if not screenshots:
        print("[ERROR] No screenshots found.")
        raise SystemExit(1)

    ocr = VisionOCR()

    latest_screenshot = screenshots[0]
    extracted_text = ocr.extract_text(latest_screenshot)

    print("==========================================")
    print("          JARVIS V6.2 OCR TEST")
    print("==========================================")
    print(f"[IMAGE] {latest_screenshot}")
    print()
    print("[OCR TEXT]")
    print(extracted_text if extracted_text else "[No text detected]")
    print("==========================================")