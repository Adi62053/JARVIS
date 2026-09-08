import os
import winsound
import soundfile as sf

from kokoro_onnx import Kokoro


# ==========================================
# JARVIS KOKORO SPEAKER
# ==========================================

class Speaker:

    def __init__(self):

        # ==========================================
        # JARVIS ROOT DIRECTORY
        # ==========================================

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        # ==========================================
        # KOKORO CONFIGURATION
        # ==========================================

        self.model_path = os.path.join(
            base_dir,
            "kokoro-v1.0.onnx"
        )

        self.voices_path = os.path.join(
            base_dir,
            "voices-v1.0.bin"
        )

        # Final selected JARVIS voice
        self.voice = "am_adam"

        # English voice
        self.language = "en-us"

        # Normal speaking speed
        self.speed = 1.0

        # ==========================================
        # OUTPUT AUDIO
        # ==========================================

        data_dir = os.path.join(
            base_dir,
            "data"
        )

        os.makedirs(
            data_dir,
            exist_ok=True
        )

        self.output_file = os.path.join(
            data_dir,
            "jarvis_voice.wav"
        )

        # ==========================================
        # VERIFY MODEL FILES
        # ==========================================

        if not os.path.exists(self.model_path):

            raise FileNotFoundError(
                f"Kokoro model not found:\n"
                f"{self.model_path}"
            )

        if not os.path.exists(self.voices_path):

            raise FileNotFoundError(
                f"Kokoro voice file not found:\n"
                f"{self.voices_path}"
            )

        # ==========================================
        # INITIALIZE KOKORO
        # ==========================================

        print(
            "Initializing JARVIS voice..."
        )

        self.kokoro = Kokoro(
            self.model_path,
            self.voices_path
        )

        print(
            "JARVIS voice initialized: "
            "Kokoro / am_adam"
        )


    # ==========================================
    # MAIN SPEAK FUNCTION
    # ==========================================

    def speak(self, text):

        if not text:
            return

        text = str(text).strip()

        if not text:
            return

        # ==========================================
        # DISPLAY RESPONSE
        # ==========================================

        print(
            "JARVIS:",
            text
        )

        # ==========================================
        # GENERATE + PLAY KOKORO VOICE
        # ==========================================

        try:

            samples, sample_rate = self.kokoro.create(

                text,

                voice=self.voice,

                speed=self.speed,

                lang=self.language
            )

            # ==========================================
            # SAVE WAV
            # ==========================================

            sf.write(
                self.output_file,
                samples,
                sample_rate
            )

            # ==========================================
            # PLAY WAV
            # ==========================================

            winsound.PlaySound(
                self.output_file,
                winsound.SND_FILENAME
            )

            print(
                "Voice engine: Kokoro / am_adam"
            )

        except Exception as e:

            print(
                "Kokoro TTS error:",
                e
            )