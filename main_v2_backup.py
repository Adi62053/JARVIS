import speech_recognition as sr

from voice.listener import Listener
from voice.speaker import Speaker
from voice.wakeword import WakeWordDetector
from core.jarvis import Jarvis


# ==========================================
# JARVIS SETUP
# ==========================================

jarvis = Jarvis()
listener = Listener()
speaker = Speaker()
wakeword = WakeWordDetector()


print("==========================================")
print("          JARVIS V2")
print("==========================================")
print("Say 'Hey Jarvis' to activate.")
print("Say 'goodbye' or 'talk to you later' to end a conversation.")
print("Say 'exit' to shut down JARVIS.")
print("Press Ctrl+C to stop.")
print()


# ==========================================
# MAIN LOOP
# ==========================================

running = True

while running:

    try:

        # --------------------------------------
        # WAIT FOR WAKE WORD
        # --------------------------------------

        wakeword.wait_for_wake_word()

        print("\n>>> HEY JARVIS DETECTED <<<")

        speaker.speak("Yes, sir.")


        # --------------------------------------
        # ACTIVE CONVERSATION
        # --------------------------------------

        conversation_active = True

        while conversation_active:

            try:

                command = listener.listen()

                command = command.lower().strip()


                # ----------------------------------
                # COMPLETELY SHUT DOWN JARVIS
                # ----------------------------------

                if command in [
                    "exit",
                    "shut down",
                    "shutdown",
                    "terminate"
                ]:

                    speaker.speak("Goodbye, sir.")

                    running = False
                    conversation_active = False


                # ----------------------------------
                # END CURRENT CONVERSATION ONLY
                # ----------------------------------

                elif command in [
                    "bye",
                    "goodbye",
                    "talk to you later"
                ]:

                    speaker.speak("Goodbye, sir.")

                    conversation_active = False


                # ----------------------------------
                # JARVIS AI RESPONSE
                # ----------------------------------

                else:

                    response = jarvis.respond(command)

                    speaker.speak(response)


            # --------------------------------------
            # SPEECH NOT UNDERSTOOD
            # --------------------------------------

            except sr.UnknownValueError:

                speaker.speak(
                    "Sorry, sir. I didn't understand that."
                )

                # Stay inside the conversation
                continue


            # --------------------------------------
            # GOOGLE SPEECH ERROR
            # --------------------------------------

            except sr.RequestError as e:

                print(
                    "JARVIS: Speech recognition error:",
                    e
                )

                # Stay inside the conversation
                continue


            # --------------------------------------
            # OTHER CONVERSATION ERRORS
            # --------------------------------------

            except Exception as e:

                print("JARVIS conversation error:", e)

                # Stay inside the conversation
                continue


        # --------------------------------------
        # RETURN TO WAKE-WORD MODE
        # --------------------------------------

        if running:

            print("\nWaiting for 'Hey Jarvis'...")


    # ------------------------------------------
    # CTRL + C
    # ------------------------------------------

    except KeyboardInterrupt:

        print("\n\nShutting down JARVIS.")
        speaker.speak("Goodbye, sir.")
        running = False


    # ------------------------------------------
    # OTHER MAIN ERRORS
    # ------------------------------------------

    except Exception as e:

        print("JARVIS error:", e)


# ==========================================
# SHUTDOWN
# ==========================================

print("\nJARVIS has been shut down.")
