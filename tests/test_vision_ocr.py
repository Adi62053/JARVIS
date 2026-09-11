from pathlib import Path

from tools.vision_ocr import VisionOCR


def test_ocr_with_screenshot():
    screenshots_dir = Path("data/screenshots")

    screenshots = sorted(
        screenshots_dir.glob("*.png"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    assert screenshots, "No screenshots available for OCR test."

    latest_screenshot = screenshots[0]

    ocr = VisionOCR()
    text = ocr.extract_text(latest_screenshot)

    assert isinstance(text, str)

    print("[TEST PASS] OCR executed successfully.")
    print(f"[IMAGE] {latest_screenshot}")
    print(f"[CHARACTERS DETECTED] {len(text)}")

    if text:
        print("[TEXT PREVIEW]")
        print(text[:500])
    else:
        print("[TEXT PREVIEW] No text detected.")


if __name__ == "__main__":
    test_ocr_with_screenshot()