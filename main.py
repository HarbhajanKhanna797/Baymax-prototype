from api import get_health_suggestions
from stt import speech_to_text, speak
from face_detection import face_detection
from manualTimer import ManualTimer

import time
import speech_recognition as sr # type: ignore
from chatterbox.tts import ChatterboxTTS # type: ignore
import contextlib
import os

with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    import pygame #type: ignore

import warnings
from cryptography.utils import CryptographyDeprecationWarning # type: ignore

warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

model = ChatterboxTTS.from_pretrained(device="cuda")
timer = ManualTimer()

pygame.mixer.init()

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
    pain_phrases = ["pain", "hurt", "ache", "sore", "ow", "ouch"]

    response = get_health_suggestions([command_text])
    if any(phrase in command_text for phrase in pain_phrases):
        sound = pygame.mixer.Sound("audio-files/pain_converted.wav")
        channel = sound.play()
        while channel.get_busy():
            time.sleep(0.1)
        time.sleep(2)  

    if any(phrase in command_text for phrase in fever_phrases):
        print("Let's check your temperature.")
        sound = pygame.mixer.Sound("audio-files/temperature_converted.wav")
        channel = sound.play()
        while channel.get_busy():
            time.sleep(0.1)
        if face_detection():
            pass # Face detected, proceed with temperature check
        else:
            print("No face detected. Unable to check temperature.")

    # If no robot command matched, treat it as a health-related input
    print("Baymax response:", response)
    speak(model, response)
    time.sleep(2)  # Wait for the response to finish

    sound = pygame.mixer.Sound("audio-files/sleep_converted.wav")
    channel = sound.play()
    while channel.get_busy():
        time.sleep(0.1)

def trigger_robot_action(action):
    # You can later send serial data to Arduino or control OpenCV gesture
    print(f"Executing action: {action}")

recognizer = sr.Recognizer()
mic = sr.Microphone()

WAKE_WORDS = ["bayma", "baymax", "paymax", "payma", "imax", "dmax", "i max", "d max", "bama", "remix", "vmax"]
AWAKE_DURATION = 60

while True:
    print("Waiting for wake word...")
    try:
        timer.reset()
        wake_command = speech_to_text(recognizer, mic)
        print(f"Wake command received: {wake_command}")

        if any(wake_word in wake_command for wake_word in WAKE_WORDS):
            print("Wake word detected. Activating Baymax...")
            sound = pygame.mixer.Sound("audio-files/intro_converted.wav")
            channel = sound.play()
            while channel.get_busy():
                time.sleep(0.1)
            print("Enter awake loop")
            timer.start()
            awake_until = time.time() + AWAKE_DURATION

            while timer.get_elapsed_time() < AWAKE_DURATION:
                print("Listening for commands...")
                command_text = speech_to_text(recognizer, mic)

                if "satisfied" not in command_text.lower():
                    print(f"Command received: {command_text}")
                    route_command(command_text)
                    timer.reset()
                    timer.start()

                else:
                    print("Patient is satisfied. Baymax will go to sleep.")
                    timer.reset()
                    break

    except Exception as e:
        print(f"Error during wake word detection: {e}")
        continue
