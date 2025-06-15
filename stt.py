import speech_recognition as sr # type: ignore
import time
from api import get_health_suggestions  # seconds Baymax stays awake after activation

def speech_to_text(recognizer, mic):
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
        try:
            command = recognizer.recognize_google(audio).lower()
            return command

        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError:
            print("Could not reach the speech recognition service.")
        except sr.WaitTimeoutError:
            print("No speech detected. Still awake...")

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    WAKE_WORD = "bayma"
    AWAKE_DURATION = 15
    print("Calibrating mic...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Baymax is listening for the wake word...")

    try:
        with mic as source:
            while True:
                print("Waiting for wake word...")
                audio = recognizer.listen(source, phrase_time_limit=4)

                try:
                    trigger_text = recognizer.recognize_google(audio).lower()
                    print("Heard:", trigger_text)

                    if WAKE_WORD in trigger_text:
                        print("Baymax activated. I'm listening...")

                        awake_until = time.time() + AWAKE_DURATION

                        while time.time() < awake_until:
                            print("Speak your command:")
                            try:
                                audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
                                command = recognizer.recognize_google(audio)
                                print("You said:", command)
                                #route_command(command)


                                # Extend awake time on each valid command
                                awake_until = time.time() + AWAKE_DURATION

                            except sr.WaitTimeoutError:
                                print("No speech detected. Still awake...")
                            except sr.UnknownValueError:
                                print("Sorry, I didn't catch that.")
                            except sr.RequestError:
                                print("Could not reach the speech recognition service.")

                        print("Baymax going back to sleep.\n")

                except sr.UnknownValueError:
                    print("Didn't catch that.")
                except sr.RequestError:
                    print("Speech service unreachable.")
    except KeyboardInterrupt:
        print("\nStopped by user.")
