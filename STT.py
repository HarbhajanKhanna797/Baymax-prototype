import speech_recognition as sr
import time
from api import get_health_suggestions


robot_commands = {
    "come here": "MOVE_FORWARD",
    "wave hello": "WAVE_HAND",
    "turn left": "TURN_LEFT",
    "turn right": "TURN_RIGHT",
    "sit down": "SIT_DOWN"
    # Add more as needed
}

def route_command(command_text):
    command_text = command_text.lower()

    for phrase, action in robot_commands.items():
        if phrase in command_text:
            print(f"Routing to Arduino/OpenCV: {action}")
            # Replace with actual Arduino/OpenCV call
            trigger_robot_action(action)
            return

    # If no robot command matched, treat it as a health-related input
    response = get_health_suggestions([command_text])
    print("Baymax response:", response)

def trigger_robot_action(action):
    # You can later send serial data to Arduino or control OpenCV gesture
    print(f"Executing action: {action}")


recognizer = sr.Recognizer()
mic = sr.Microphone()

WAKE_WORD = "baymax"
AWAKE_DURATION = 15  # seconds Baymax stays awake after activation

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
                            route_command(command)


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
