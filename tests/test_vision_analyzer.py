from pathlib import Path

from tools.vision_analyzer import VisionAnalyzer


def test_screen_analysis():
    screenshots_dir = Path("data/screenshots")

    screenshots = sorted(
        screenshots_dir.glob("*.png"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    assert screenshots, "No screenshots available for screen analysis test."

    latest_screenshot = screenshots[0]

    analyzer = VisionAnalyzer()
    result = analyzer.analyze(latest_screenshot)

    assert isinstance(result, dict)

    assert "image" in result
    assert "resolution" in result
    assert "raw_element_count" in result
    assert "element_count" in result
    assert "elements" in result
    assert "full_text" in result

    assert result["raw_element_count"] >= result["element_count"]

    resolution = result["resolution"]

    assert isinstance(resolution, dict)
    assert resolution["width"] > 0
    assert resolution["height"] > 0

    elements = result["elements"]

    assert isinstance(elements, list)

    for element in elements:
        assert "text" in element
        assert "x" in element
        assert "y" in element
        assert "width" in element
        assert "height" in element
        assert "confidence" in element

        assert isinstance(element["text"], str)
        assert element["text"].strip()

        assert isinstance(element["x"], int)
        assert isinstance(element["y"], int)
        assert isinstance(element["width"], int)
        assert isinstance(element["height"], int)
        assert isinstance(element["confidence"], float)

        assert element["x"] >= 0
        assert element["y"] >= 0
        assert element["width"] >= 5
        assert element["height"] >= 5
        assert element["confidence"] >= 25.0

    print("[TEST PASS] Screen analysis executed successfully.")
    print(f"[IMAGE] {latest_screenshot}")
    print(
        f"[RESOLUTION] "
        f"{resolution['width']} x "
        f"{resolution['height']}"
    )
    print(
        f"[RAW OCR ELEMENTS] "
        f"{result['raw_element_count']}"
    )
    print(
        f"[CLEAN ELEMENTS] "
        f"{result['element_count']}"
    )

    print("[CLEAN ELEMENT PREVIEW]")

    for index, element in enumerate(elements[:20], start=1):
        print(
            f"{index}. "
            f"{element['text']} | "
            f"x={element['x']} "
            f"y={element['y']} "
            f"w={element['width']} "
            f"h={element['height']} "
            f"confidence={element['confidence']:.1f}"
        )


if __name__ == "__main__":
    test_screen_analysis()