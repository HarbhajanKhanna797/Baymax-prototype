# import sounddevice as sd
# import speech_recognition as sr

# samplerate = 16000
# duration = 5  # seconds
# print("Recording...")
# audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
# sd.wait()

# # Convert numpy audio to AudioData object
# recognizer = sr.Recognizer()
# audio_data = sr.AudioData(audio.tobytes(), samplerate, 2)

# print("Recognizing...")
# command = recognizer.recognize_google(audio_data).lower()
# print(command)



# ======================================================
# import RPi.GPIO as GPIO
# import time

# # GPIO.cleanup()


# # Pin setup
# DIR_PIN = 27     # Direction pin
# STEP_PIN = 17    # Step pin
# EN_PIN = 22      # Enable pin

# # Setup GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(DIR_PIN, GPIO.OUT)
# GPIO.setup(STEP_PIN, GPIO.OUT)
# GPIO.setup(EN_PIN, GPIO.OUT)

# def move_stepper(steps, direction=1, step_delay=0.005):
#     """
#     Moves the stepper motor.
#     steps: Number of steps to move
#     direction: 1 = clockwise, 0 = counterclockwise
#     step_delay: Delay between steps (controls speed)
#     """
#     # Enable driver
#     GPIO.output(EN_PIN, GPIO.LOW)
#     # Set direction
#     GPIO.output(DIR_PIN, direction)

#     # Send pulses
#     for _ in range(steps):
#         GPIO.output(STEP_PIN, GPIO.HIGH)
#         time.sleep(step_delay)
#         GPIO.output(STEP_PIN, GPIO.LOW)
#         time.sleep(step_delay)

#     # Disable driver
#     GPIO.output(EN_PIN, GPIO.HIGH)

# try:
#     # Example: 200 steps clockwise
#     move_stepper(10000, direction=1, step_delay=0.01)
#     time.sleep(1)
#     # Example: 200 steps counterclockwise
#     move_stepper(200, direction=0, step_delay=0.01)

# except KeyboardInterrupt:
#     pass

# finally:
#     GPIO.cleanup()






#==========================================================

from smbus2 import SMBus
import time
import math

# PCA9685 registers
MODE1       = 0x00
PRESCALE    = 0xFE
LED0_ON_L   = 0x06

# Servo pulse parameters
SERVO_MIN_US = 500   # min pulse length in microseconds
SERVO_MAX_US = 2500  # max pulse length in microseconds
FREQ_HZ      = 50    # 50Hz for servos

# Setup I²C
i2c = SMBus(1)       # Bus 1
ADDRESS = 0x40       # PCA9685 default I²C address

def pca9685_init():
    # Reset PCA9685
    i2c.write_byte_data(ADDRESS, MODE1, 0x00)
    time.sleep(0.005)

    # Set prescale for ~50Hz
    prescale_val = int(math.floor(25000000.0 / (4096 * FREQ_HZ) - 1))
    old_mode = i2c.read_byte_data(ADDRESS, MODE1)
    new_mode = (old_mode & 0x7F) | 0x10
    i2c.write_byte_data(ADDRESS, MODE1, new_mode)
    i2c.write_byte_data(ADDRESS, PRESCALE, prescale_val)
    i2c.write_byte_data(ADDRESS, MODE1, old_mode)
    time.sleep(0.005)
    i2c.write_byte_data(ADDRESS, MODE1, old_mode | 0xA1)

def set_pwm(channel, on, off):
    i2c.write_byte_data(ADDRESS, LED0_ON_L + 4*channel, on & 0xFF)
    i2c.write_byte_data(ADDRESS, LED0_ON_L + 4*channel + 1, on >> 8)
    i2c.write_byte_data(ADDRESS, LED0_ON_L + 4*channel + 2, off & 0xFF)
    i2c.write_byte_data(ADDRESS, LED0_ON_L + 4*channel + 3, off >> 8)

def angle_to_pwm(angle):
    pulse_us = SERVO_MIN_US + (angle / 180.0) * (SERVO_MAX_US - SERVO_MIN_US)
    ticks = int(pulse_us * 4096 / (1000000.0 / FREQ_HZ))
    return ticks

current_angles = [4] * 16  # store last angle for each channel

def move_servo(channel, target_angle, speed_dps=45, step=1):
    global current_angles
    start_angle = current_angles[channel]
    delay_per_step = step / speed_dps

    if target_angle > start_angle:
        angle_range = range(start_angle, target_angle + 1, step)
    else:
        angle_range = range(start_angle, target_angle - 1, -step)

    for angle in angle_range:
        ticks = angle_to_pwm(angle)
        set_pwm(channel, 0, ticks)
        time.sleep(delay_per_step)

    current_angles[channel] = target_angle

# # Init and test
# pca9685_init()
# move_servo(3, 60, 45)  # move to 150° at 45°/s
# time.sleep(1)
# move_servo(3, 15, 45)   # move back to 30° at 45°/s





# ===========================================================
# import gpiozero
# from gpiozero.pins.lgpio import LGPIOFactory

# gpiozero.Device.pin_factory = LGPIOFactory()
# print(gpiozero.Device.pin_factory)


# =============================================

# import serial

# arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
# time.sleep(2)

# def get_temp():
#     normal_temp = 37
#     while True:
#         if arduino.in_waiting > 0:
#             ambient_temp, object_temp = (arduino.readline().decode('utf-8').rstrip()).split(',')
#             object_temp = float(object_temp)
#             print(f"Received: {object_temp}")
#         if normal_temp - object_temp < 5:
#             return (object_temp + object_temp/10)
        
# temp = get_temp()
# print(temp)
