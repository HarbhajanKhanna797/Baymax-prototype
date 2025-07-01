from api import get_health_suggestions
from stt import speech_to_text, generate_speech, speak, speak_baymax
from face_detection import face_detection
from manualTimer import ManualTimer

import time
import speech_recognition as sr
import os

import board
import busio
import adafruit_mlx90614
import serial

# 🔍 Monitoring imports
import psutil 
import threading
import tracemalloc

# ==== Monitoring Setup ====
tracemalloc.start()
process = psutil.Process(os.getpid())

def monitor():
    while True:
        cpu = process.cpu_percent(interval=1)
        mem = process.memory_info().rss / (1024 * 1024)
        print(f"[MONITOR] CPU: {cpu:.2f}% | RAM: {mem:.2f} MB")
        time.sleep(1)

threading.Thread(target=monitor, daemon=True).start()

timer = ManualTimer()

# arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# time.sleep(2)

robot_commands = {
    "come here": "MOVE_FORWARD",
    "wave hello": "WAVE_HAND",
    "turn left": "TURN_LEFT",
    "turn right": "TURN_RIGHT",
    "sit down": "SIT_DOWN"
}

def read_temperatue_data():
    i2c = busio.I2C(board.SCL, board.SDA)
    mlx = adafruit_mlx90614.MLX90614(i2c)

    object_temp = f"{mlx.object_temperature:.2f} °C"
    return object_temp

def route_command(command_text):
    command_text = command_text.lower()

    for phrase, action in robot_commands.items():
        if phrase in command_text:
            print(f"Routing to Arduino/OpenCV: {action}")
            trigger_robot_action(action)
            return

    fever_phrases = ["fever", "hot", "shivering", "headache", "sweating", "chills"]
    pain_phrases = ["pain", "hurt", "ache", "sore", "ow", "ouch"]
    diarrhea_phrases = ["diarrhea", "loose motion", "stomach upset", "diar"]

    response = get_health_suggestions([command_text])

    if any(phrase in command_text for phrase in pain_phrases):
        speak("pain_converted")
        time.sleep(2)

    if any(phrase in command_text for phrase in fever_phrases):
        print("Let's check your temperature.")
        speak("temperature_converted")
        if face_detection():
            # temperature = read_temperatue_data()
            # print(f"Your temperature is {temperature}")
            pass
        else:
            print("No face detected. Unable to check temperature.")

    if "headache" in command_text:
        speak("headache_converted")
    elif "vomit" in command_text:
        speak("vomit_converted")
    elif "fever" in command_text:
        speak("fever_converted")
    elif "cold" in command_text:
        speak("cold_converted")
    elif any(phrase in command_text for phrase in diarrhea_phrases):
        speak("diarrhea_converted")
    elif "throat" in command_text:
        speak("throat_converted")
    else:
        speak_baymax(response)

    print("Baymax response:", response)
    time.sleep(2)
    speak("sleep_converted")

def trigger_robot_action(cmd):
    print(f"Executing action: {cmd}")

    # arduino.write((cmd + '\n').encode())  # Send command with newline
    # response = arduino.readline().decode().strip()
    # return response

recognizer = sr.Recognizer()
mic = sr.Microphone()

WAKE_WORDS = ["bayma", "baymax", "paymax", "payma", "imax", "dmax", "i max", "d max", "bama", "remix", "vmax"]
AWAKE_DURATION = 60

try:
    while True:
        print("Waiting for wake word...")
        try:
            timer.reset()
            wake_command = speech_to_text(recognizer, 5)
            print(f"Wake command received: {wake_command}")

            if any(wake_word in wake_command for wake_word in WAKE_WORDS):
                print("Wake word detected. Activating Baymax...")
                speak("intro_converted")
                print("Enter awake loop")
                timer.start()

                while timer.get_elapsed_time() < AWAKE_DURATION:
                    print("Listening for commands...")
                    command_text = speech_to_text(recognizer, 5)

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

except KeyboardInterrupt:
    current, peak = tracemalloc.get_traced_memory()
    print(f"[PEAK MEMORY] Current: {current / 1024:.2f} KB | Peak: {peak / 1024:.2f} KB")
    tracemalloc.stop()
