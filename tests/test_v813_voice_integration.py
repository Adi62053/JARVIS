"""
JARVIS V8.13 - Voice Integration Test
"""

from automation.automation_voice import AutomationVoice


def main() -> None:
    voice = AutomationVoice()

    voice.speak(
        "V8.13 voice integration unit test successful, sir."
    )

    voice.speak_results(
        [
            "Voice result one.",
            "Voice result two.",
        ]
    )

    print("[PASS] V8.13 voice integration test completed.")


if __name__ == "__main__":
    main()
