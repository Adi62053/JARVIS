import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

MODEL_PATH = "kokoro-v1.0.onnx"
VOICES_PATH = "voices-v1.0.bin"

print("Loading Kokoro...")
kokoro = Kokoro(MODEL_PATH, VOICES_PATH)

text = """
Good evening, sir. I am JARVIS.
All systems are online and ready.
How may I assist you today?
"""

print("Generating voice...")

samples, sample_rate = kokoro.create(
    text,
    voice="am_adam",
    speed=1.0,
    lang="en-us"
)

output_file = "jarvis_kokoro_adam.wav"

sf.write(output_file, samples, sample_rate)

print(f"Voice generated successfully: {output_file}")
print("Sample rate:", sample_rate)