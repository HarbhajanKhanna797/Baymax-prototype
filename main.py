from api import get_health_suggestions
from stt import speech_to_text
from face_detection import face_detection

import time
import speech_recognition as sr # type: ignore

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

    fever_phrases = ["fever", "hot", "shivering", "headache", "sweating", "chills"]

    if any(phrase in command_text for phrase in fever_phrases):
        print("Let's check your temperature.")
        if face_detection():
            pass # Face detected, proceed with temperature check
        else:
            print("No face detected. Unable to check temperature.")

    # If no robot command matched, treat it as a health-related input
    response = get_health_suggestions([command_text])
    print("Baymax response:", response)

def trigger_robot_action(action):
    # You can later send serial data to Arduino or control OpenCV gesture
    print(f"Executing action: {action}")

recognizer = sr.Recognizer()
mic = sr.Microphone()

WAKE_WORDS = ["bayma", "baymax", "payamax", "i max", "d max"]
AWAKE_DURATION = 25

while True:
    print("Waiting for wake word...")
    try:
        wake_command = speech_to_text(recognizer, mic)

        if (WAKE_WORD.lower() for WAKE_WORD in WAKE_WORDS) in wake_command.lower():
            print("Wake word detected. Activating Baymax...")
            awake_until = time.time() + AWAKE_DURATION

            while time.time() < awake_until:
                print("Listening for commands...")
                command_text = speech_to_text(recognizer, mic)

                if command_text != "i am satisfied with my care":
                    print(f"Command received: {command_text}")
                    awake_until = time.time() + AWAKE_DURATION
                    route_command(command_text)

                else:
                    print("Patient is satisfied. Baymax will go to sleep.")
                    break

            if time.time() >= awake_until:
                print("Baymax is going to sleep now.")
                break
    except Exception as e:
        print(f"Error during wake word detection: {e}")
        continue
