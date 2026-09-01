import sounddevice as sd
import numpy as np
from openwakeword.model import Model
import time


class WakeWordDetector:

    def __init__(self, device=1):

        self.sample_rate = 16000
        self.frame_size = 1280
        self.device = device

        self.threshold = 0.5
        self.cooldown = 1.0

        print("Loading Hey Jarvis wake-word model...")

        self.model = Model(
            wakeword_models=["hey_jarvis"]
        )

        print("Wake-word detector ready.")

    def wait_for_wake_word(self):

        detected = False

        def callback(indata, frames, time_info, status):

            nonlocal detected

            if status:
                print(status)

            if detected:
                return

            audio = indata[:, 0].astype(np.int16)

            prediction = self.model.predict(audio)

            score = prediction.get("hey_jarvis", 0)

            if score > self.threshold:
                detected = True

        print("Waiting for 'Hey Jarvis'...")

        with sd.InputStream(
            samplerate=self.sample_rate,
            blocksize=self.frame_size,
            channels=1,
            dtype="int16",
            device=self.device,
            callback=callback
        ):

            while not detected:
                sd.sleep(50)

        # Prevent immediate re-triggering
        time.sleep(self.cooldown)

        # Reset wake-word model state
        self.model.reset()

        return True