import speech_recognition as sr


class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("\nListening...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = self.recognizer.listen(source)

        command = self.recognizer.recognize_google(audio)

        print("You:", command)

        return command