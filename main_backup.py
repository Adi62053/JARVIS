import os
import base64
import winsound
import speech_recognition as sr

from sarvamai import SarvamAI
from core.jarvis import Jarvis


# ==========================================
# SARVAM TEXT TO SPEECH SETUP
# ==========================================

api_key = os.getenv("SARVAM_API_KEY")

client = SarvamAI(
    api_subscription_key=api_key
)

SARVAM_OUTPUT = "jarvis_voice.wav"


# ==========================================
# JARVIS SETUP
# ==========================================

jarvis = Jarvis()
recognizer = sr.Recognizer()


print("JARVIS is running")
print("Say 'exit' or 'bye' to stop.")


# ==========================================
# TEXT TO SPEECH
# ==========================================

def speak(text):
    print("JARVIS:", text)

    try:
        response = client.text_to_speech.convert(
            text=text,
            language_code="en-IN",
            speaker="kabir",
            model="bulbul:v3",
            pace=0.9,
            output_audio_codec="wav"
        )

        audio_data = base64.b64decode(
            response.audios[0]
        )

        with open(SARVAM_OUTPUT, "wb") as audio_file:
            audio_file.write(audio_data)

        winsound.PlaySound(
            SARVAM_OUTPUT,
            winsound.SND_FILENAME
        )

    except Exception as e:
        print("JARVIS voice error:", e)


# ==========================================
# MAIN LOOP
# ==========================================

while True:
    try:

        with sr.Microphone() as source:
            print("\nListening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(source)

        command = recognizer.recognize_google(audio)

        print("You:", command)


        # --------------------------------------
        # EXIT COMMAND
        # --------------------------------------

        if command.lower() in [
            "exit",
            "bye",
            "goodbye"
        ]:
            speak("Goodbye, sir.")
            break


        # --------------------------------------
        # JARVIS AI RESPONSE
        # --------------------------------------

        response = jarvis.respond(command)

        speak(response)


    # ------------------------------------------
    # SPEECH NOT UNDERSTOOD
    # ------------------------------------------

    except sr.UnknownValueError:

        speak(
            "Sorry, sir. I didn't understand that."
        )


    # ------------------------------------------
    # GOOGLE SPEECH ERROR
    # ------------------------------------------

    except sr.RequestError as e:

        print(
            "JARVIS: Speech recognition error:",
            e
        )


    # ------------------------------------------
    # CTRL + C
    # ------------------------------------------

    except KeyboardInterrupt:

        speak("Goodbye, sir.")
        break


    # ------------------------------------------
    # OTHER ERRORS
    # ------------------------------------------

    except Exception as e:

        print("JARVIS error:", e)