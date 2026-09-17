"""
JARVIS V8 - Automation Voice Integration

Connects automation responses to the existing JARVIS
offline Kokoro voice system.

This module does not create a new TTS engine.
It reuses voice.speaker.Speaker.
"""

from voice.speaker import Speaker


class AutomationVoice:
    """Speak automation results using the existing JARVIS speaker."""

    def __init__(self, speaker: Speaker | None = None) -> None:
        self.speaker = speaker or Speaker()

    def speak(self, text: str) -> None:
        """Speak one automation response."""
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        text = text.strip()

        if not text:
            return

        self.speaker.speak(text)

    def speak_results(self, results: list[str]) -> None:
        """Speak all non-empty automation results."""
        if not isinstance(results, list):
            raise TypeError("results must be a list")

        for result in results:
            if isinstance(result, str) and result.strip():
                self.speak(result)
