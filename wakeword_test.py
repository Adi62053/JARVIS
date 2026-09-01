import sounddevice as sd
import numpy as np
from openwakeword.model import Model


print("Loading Hey Jarvis wake-word model...")

model = Model(
    wakeword_models=["hey_jarvis"]
)

print("Wake-word detector ready.")
print("Say: Hey Jarvis")
print("Press Ctrl+C to stop.\n")


SAMPLE_RATE = 16000
FRAME_SIZE = 1280
DEVICE = 1


def audio_callback(indata, frames, time, status):

    if status:
        print(status)

    audio = indata[:, 0].astype(np.int16)

    prediction = model.predict(audio)

    score = prediction.get("hey_jarvis", 0)

    print(f"\rConfidence: {score:.3f}", end="")

    if score > 0.5:
        print("\n\n>>> HEY JARVIS DETECTED <<<\n")


try:

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        blocksize=FRAME_SIZE,
        channels=1,
        dtype="int16",
        device=DEVICE,
        callback=audio_callback
    ):

        print("Microphone stream started.\n")

        while True:
            sd.sleep(1000)


except KeyboardInterrupt:

    print("\n\nTest stopped.")