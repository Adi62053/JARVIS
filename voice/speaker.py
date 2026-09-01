import os
import base64
import winsound

from dotenv import load_dotenv
from sarvamai import SarvamAI


# Load variables from .env
load_dotenv()


class Speaker:
    def __init__(self):

        api_key = os.getenv("SARVAM_API_KEY")

        if not api_key:
            raise ValueError(
                "SARVAM_API_KEY not found. "
                "Please check your .env file."
            )

        self.client = SarvamAI(
            api_subscription_key=api_key
        )

        self.output_file = "jarvis_voice.wav"

    def speak(self, text):

        print("JARVIS:", text)

        try:

            response = self.client.text_to_speech.convert(
                text=text,
                language_code="en-IN",
                speaker="kabir",
                model="bulbul:v3",
                pace=1.2,
                output_audio_codec="wav"
            )

            audio_data = base64.b64decode(
                response.audios[0]
            )

            with open(
                self.output_file,
                "wb"
            ) as audio_file:

                audio_file.write(audio_data)

            winsound.PlaySound(
                self.output_file,
                winsound.SND_FILENAME
            )

        except Exception as e:

            print(
                "JARVIS voice error:",
                e
            )