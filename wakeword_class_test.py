from voice.wakeword import WakeWordDetector


detector = WakeWordDetector()

print("JARVIS is waiting...")

detector.wait_for_wake_word()

print(">>> HEY JARVIS DETECTED <<<")