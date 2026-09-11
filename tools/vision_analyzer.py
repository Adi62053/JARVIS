from pathlib import Path
import re

import pytesseract
from PIL import Image


class VisionAnalyzer:
    """
    JARVIS V6.3.3 - Screen Vision Analyzer

    Converts OCR output into structured screen elements containing:
        - text
        - coordinates
        - dimensions
        - confidence

    V6.3.3 adds conservative semantic/context cleanup while preserving
    legitimate UI labels, filenames, folders, symbols, and code text.
    """

    DEFAULT_MIN_CONFIDENCE = 25.0
    DEFAULT_MIN_WIDTH = 5
    DEFAULT_MIN_HEIGHT = 5

    ALLOWED_SYMBOLS = {
        ">",
        "<",
        "+",
        "-",
        "_",
        "/",
        "\\",
        ":",
        ".",
        "...",
    }

    COMMON_SHORT_UI_WORDS = {
        "ok",
        "go",
        "run",
        "stop",
        "file",
        "edit",
        "view",
        "help",
        "open",
        "save",
        "close",
        "copy",
        "paste",
        "cut",
        "test",
        "tests",
        "debug",
        "search",
        "new",
        "yes",
        "no",
    }

    def __init__(
        self,
        tesseract_path=None,
        min_confidence=DEFAULT_MIN_CONFIDENCE,
        min_width=DEFAULT_MIN_WIDTH,
        min_height=DEFAULT_MIN_HEIGHT,
    ):
        """
        Initialize the screen analyzer.

        Args:
            tesseract_path: Optional Tesseract executable path.
            min_confidence: Minimum OCR confidence.
            min_width: Minimum element width.
            min_height: Minimum element height.
        """

        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

        self.min_confidence = float(min_confidence)
        self.min_width = int(min_width)
        self.min_height = int(min_height)

    def _extract_raw_data(self, image):
        """
        Run Tesseract and return detailed OCR data.
        """

        return pytesseract.image_to_data(
            image,
            output_type=pytesseract.Output.DICT,
        )

    def _build_raw_elements(self, data):
        """
        Convert Tesseract's dictionary output into structured elements.
        """

        elements = []

        text_values = data.get("text", [])
        confidence_values = data.get("conf", [])
        left_values = data.get("left", [])
        top_values = data.get("top", [])
        width_values = data.get("width", [])
        height_values = data.get("height", [])

        count = len(text_values)

        for index in range(count):
            try:
                text = str(text_values[index]).strip()

                confidence = float(confidence_values[index])

                x = int(left_values[index])
                y = int(top_values[index])
                width = int(width_values[index])
                height = int(height_values[index])

            except (ValueError, TypeError, IndexError):
                continue

            if not text:
                continue

            elements.append(
                {
                    "text": text,
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "confidence": confidence,
                }
            )

        return elements

    def _passes_basic_filter(self, element):
        """
        Apply safe geometry and confidence filtering.
        """

        text = element["text"].strip()

        if not text:
            return False

        if element["confidence"] < self.min_confidence:
            return False

        if element["width"] < self.min_width:
            return False

        if element["height"] < self.min_height:
            return False

        if element["x"] < 0 or element["y"] < 0:
            return False

        return True

    @staticmethod
    def _is_filename_or_path(text):
        """
        Detect common filename/path structures.

        These should generally be preserved even when they contain
        unusual punctuation or mixed characters.
        """

        normalized = text.strip()

        if not normalized:
            return False

        filename_patterns = [
            r".+\.[A-Za-z0-9]{1,10}$",
            r"^[A-Za-z]:\\",
            r"^\.?[A-Za-z0-9_-]+\\",
            r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$",
        ]

        return any(
            re.match(pattern, normalized)
            for pattern in filename_patterns
        )

    @staticmethod
    def _is_code_like(text):
        """
        Detect common programming/code patterns.
        """

        normalized = text.strip()

        if not normalized:
            return False

        code_patterns = [
            r"^[A-Za-z_][A-Za-z0-9_]*$",
            r"^[A-Za-z_][A-Za-z0-9_]*\(\)$",
            r"^[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*$",
            r"^[A-Za-z_][A-Za-z0-9_]*=[A-Za-z0-9_]+$",
        ]

        return any(
            re.fullmatch(pattern, normalized)
            for pattern in code_patterns
        )

    @staticmethod
    def _looks_like_ocr_gibberish(text):
        """
        Detect suspicious OCR artifacts.

        This function is deliberately conservative.
        It should reject obvious OCR noise without deleting
        legitimate short UI text.
        """

        normalized = text.strip()

        if not normalized:
            return True

        if normalized in VisionAnalyzer.ALLOWED_SYMBOLS:
            return False

        lowered = normalized.lower()

        if lowered in VisionAnalyzer.COMMON_SHORT_UI_WORDS:
            return False

        if VisionAnalyzer._is_filename_or_path(normalized):
            return False

        if VisionAnalyzer._is_code_like(normalized):
            return False

        letters = sum(character.isalpha() for character in normalized)
        digits = sum(character.isdigit() for character in normalized)
        spaces = sum(character.isspace() for character in normalized)
        symbols = len(normalized) - letters - digits - spaces

        # Pure punctuation/symbol garbage.
        if letters == 0 and digits == 0:
            return normalized not in VisionAnalyzer.ALLOWED_SYMBOLS

        # Very short mixed OCR fragments such as:
        # "x)", "@1", "a$", etc.
        if len(normalized) <= 3:
            if letters >= 1 and symbols >= 2:
                return True

        # Suspicious symbol-heavy mixed fragments.
        if len(normalized) <= 8:
            if symbols >= 2 and letters >= 1 and digits >= 1:
                return True

        # Strongly symbol-dominated strings.
        if len(normalized) >= 4:
            if symbols >= len(normalized) * 0.45:
                return True

        # Repeated punctuation artifacts.
        for character in set(normalized):
            if character.isalnum() or character.isspace():
                continue

            if normalized.count(character) >= 3:
                return True

        # OCR often produces a very short alphanumeric fragment
        # with unusual upper/lower/digit mixing.
        if 4 <= len(normalized) <= 8:
            if letters >= 1 and digits >= 1:
                if letters + digits == len(normalized):
                    upper_count = sum(
                        character.isupper()
                        for character in normalized
                    )

                    lower_count = sum(
                        character.islower()
                        for character in normalized
                    )

                    if upper_count >= 2 and lower_count >= 1:
                        return True

        return False

    def _passes_semantic_filter(self, element):
        """
        Apply conservative semantic filtering.
        """

        text = element["text"].strip()

        if self._looks_like_ocr_gibberish(text):
            return False

        return True

    @staticmethod
    def _is_duplicate(element, accepted_elements):
        """
        Remove exact duplicate OCR elements.
        """

        for existing in accepted_elements:
            if (
                element["text"] == existing["text"]
                and element["x"] == existing["x"]
                and element["y"] == existing["y"]
                and element["width"] == existing["width"]
                and element["height"] == existing["height"]
            ):
                return True

        return False

    def _filter_elements(self, elements):
        """
        Apply all V6.3.3 filters.
        """

        accepted = []

        for element in elements:
            if not self._passes_basic_filter(element):
                continue

            if not self._passes_semantic_filter(element):
                continue

            if self._is_duplicate(element, accepted):
                continue

            accepted.append(element)

        return accepted

    def analyze(self, image_path):
        """
        Analyze a screenshot.

        Returns:
            dict:
                image
                resolution
                raw_element_count
                element_count
                elements
                full_text
        """

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image file not found: {image_path}"
            )

        with Image.open(image_path) as image:
            image = image.convert("RGB")

            screen_width, screen_height = image.size

            raw_data = self._extract_raw_data(image)
            raw_elements = self._build_raw_elements(raw_data)
            filtered_elements = self._filter_elements(raw_elements)

        full_text = " ".join(
            element["text"]
            for element in filtered_elements
        )

        return {
            "image": str(image_path),
            "resolution": {
                "width": screen_width,
                "height": screen_height,
            },
            "raw_element_count": len(raw_elements),
            "element_count": len(filtered_elements),
            "elements": filtered_elements,
            "full_text": full_text,
        }

    def get_text_elements(self, image_path):
        """
        Return cleaned structured OCR elements.
        """

        analysis = self.analyze(image_path)

        return analysis["elements"]


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

    analyzer = VisionAnalyzer()

    latest_screenshot = screenshots[0]

    result = analyzer.analyze(latest_screenshot)

    print("==========================================")
    print("     JARVIS V6.3.3 SCREEN ANALYZER")
    print("==========================================")
    print(f"[IMAGE] {latest_screenshot}")
    print(
        f"[RESOLUTION] "
        f"{result['resolution']['width']} x "
        f"{result['resolution']['height']}"
    )
    print(f"[RAW OCR ELEMENTS] {result['raw_element_count']}")
    print(f"[CLEAN ELEMENTS] {result['element_count']}")
    print()
    print("[CLEAN ELEMENT PREVIEW]")

    for index, element in enumerate(
        result["elements"][:20],
        start=1,
    ):
        print(
            f"{index}. "
            f"{element['text']} | "
            f"x={element['x']} "
            f"y={element['y']} "
            f"w={element['width']} "
            f"h={element['height']} "
            f"confidence={element['confidence']:.1f}"
        )

    print("==========================================")