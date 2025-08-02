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
# from board import SCL, SDA
# import busio
# from adafruit_pca9685 import PCA9685

# # Initialize I2C and PCA9685
# i2c = busio.I2C(SCL, SDA)
# pca = PCA9685(i2c)
# pca.frequency = 50  # typical for servos

# # Map angle (0–180) to duty cycle (for 1ms to 2ms pulse width)
# def angle_to_duty_cycle(angle):
#     min_pulse = 1000  # us
#     max_pulse = 2000  # us
#     pulse = min_pulse + (angle / 180.0) * (max_pulse - min_pulse)
#     duty_cycle = int((pulse * 4096) / 20000)  # 20ms period
#     return duty_cycle

# # Move servo to target angle at 45°/sec
# def move_servo_to(channel, target_angle, current_angle=0):
#     step = 1 if target_angle > current_angle else -1
#     delay_per_step = 1 / 45.0  # 1 degree per (1/45) seconds = 45°/sec

#     for angle in range(current_angle, target_angle + step, step):
#         pca.channels[channel].duty_cycle = angle_to_duty_cycle(angle)
#         time.sleep(delay_per_step)

# # === Example Usage ===
# # Start at 0°, move to 90° at 45°/s
# move_servo_to(channel=0, target_angle=90, current_angle=0)

# # Hold for 1 sec
# time.sleep(1)

# # Move back to 0° at same speed
# move_servo_to(channel=0, target_angle=0, current_angle=90)

# # Cleanup (optional)
# pca.channels[0].duty_cycle = 0

# ===========================================================

