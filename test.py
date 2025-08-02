import sounddevice as sd
import speech_recognition as sr

samplerate = 16000
duration = 5  # seconds
print("Recording...")
audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
sd.wait()

# Convert numpy audio to AudioData object
recognizer = sr.Recognizer()
audio_data = sr.AudioData(audio.tobytes(), samplerate, 2)

print("Recognizing...")
command = recognizer.recognize_google(audio_data).lower()
print(command)



# ======================================================
# import RPi.GPIO as GPIO
# import time

# # Pin setup
# DIR = 23     # Direction pin
# STEP = 18    # Step pin
# EN = 24      # Enable pin

# # Setup
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(DIR, GPIO.OUT)
# GPIO.setup(STEP, GPIO.OUT)
# GPIO.setup(EN, GPIO.OUT)

# # Enable driver
# GPIO.output(EN, GPIO.LOW)

# # Set direction (change as needed)
# GPIO.output(DIR, GPIO.HIGH)

# # Steps per revolution depends on microstepping (e.g., 200 for full-step)
# steps = 200  # 1 revolution for full-step
# delay = 0.001  # delay between steps (in seconds)

# # Step the motor
# for _ in range(steps):
#     GPIO.output(STEP, GPIO.HIGH)
#     time.sleep(delay)
#     GPIO.output(STEP, GPIO.LOW)
#     time.sleep(delay)

# # Disable driver
# GPIO.output(EN, GPIO.HIGH)

# GPIO.cleanup()
# ========================================================



# ========================================================
# import time
# from adafruit_pca9685 import PCA9685
# from board import SCL, SDA
# import busio

# # Initialize I2C
# i2c = busio.I2C(SCL, SDA)

# # Create PCA9685 object
# pca = PCA9685(i2c)
# pca.frequency = 50  # 50 Hz for servos

# # Helper: Convert angle (0–180) to duty cycle value (servo pulse)
# def set_servo_angle(channel, angle):
#     # Clamp angle
#     angle = max(0, min(180, angle))
#     # Map 0-180 to 1000-2000us pulse (approx. 0.5ms to 2.5ms)
#     pulse_length = 1000 + (angle / 180) * 1000  # in microseconds
#     duty_cycle = int(pulse_length * 4096 / 20000)  # 20ms = 50Hz
#     pca.channels[channel].duty_cycle = duty_cycle

# # Example: Move 4 servos
# try:
#     while True:
#         print("Moving servos to 0°")
#         for ch in range(4):
#             set_servo_angle(ch, 0)
#         time.sleep(1)

#         print("Moving servos to 90°")
#         for ch in range(4):
#             set_servo_angle(ch, 90)
#         time.sleep(1)

#         print("Moving servos to 180°")
#         for ch in range(4):
#             set_servo_angle(ch, 180)
#         time.sleep(1)

# except KeyboardInterrupt:
#     print("Stopping...")
#     for ch in range(4):
#         pca.channels[ch].duty_cycle = 0
# ===========================================================

