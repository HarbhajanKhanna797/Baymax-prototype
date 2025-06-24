# 🤖 Project Baymax

**Project Baymax** is a soft-bodied, voice-activated healthcare companion robot  
inspired by *Baymax* from Disney's *Big Hero 6*.

While not as advanced as the fictional version, this real-world robot can listen, talk,  
analyze basic symptoms, measure temperature, perform gestures, detect faces,  
avoid obstacles using LiDAR, simulate walking, and fold its body using a custom  
mechanical structure.

It is built using affordable electronics like **Arduino**, **Raspberry Pi**, and controlled  
via **Python**, **OpenCV**, and **Google’s Gemini AI** for interactive intelligence.

---

## ✍️ Authors

- **Prince Soni**  
- **Harbhajan Khanna**  
- **Bhavya Upadhyay**  
- **Raghav Sharma**

📄 [More About the Authors](more_authors.md)

---

## 📌 What It Does

Baymax can interact with people just by listening to their voice.  
It checks your temperature, listens to symptoms, offers health suggestions,  
and can perform basic actions like waving, walking, or turning.

It can also detect human faces through a camera and detect nearby objects  
using a LiDAR module for spatial awareness and collision avoidance.

It folds and unfolds using a servo-actuated scissor-lift torso, mimicking  
Baymax's "inflating" motion.

---

## ✨ Features

- **Voice-controlled interaction** with wake word `"baymax"`
- **Speech-to-text** and **text-to-speech** for natural conversations
- **Health symptom analysis** using AI-powered response system
- **Face detection** using OpenCV and Pi Camera
- **Object detection & avoidance** using RPLIDAR A1 LiDAR module
- **Temperature sensing** with a non-contact IR sensor (MLX90614)
- **Gesture-based actions** like waving, sitting, and walking
- **Scissor-lift-based folding design** to simulate a soft body
- **Human-like walking** using alternating servo PWM control
- **Emotion-aware voice response and sleep mode handling**

---

## 🧠 Main Control Logic (`main.py`)

The `main.py` script is the central brain of Baymax.

It listens for wake words like `"baymax"`, `"imax"`, `"vmax"`, `"remix"` and others.  
Once triggered, Baymax enters a 60-second **awake state**, listens to commands,  
and routes them to either:
- Servo motion control
- Gemini health AI
- Emotion clip playback
- Face detection + temperature check

It uses `speech_recognition`, `pygame`, `ChatterboxTTS`, and `manualTimer.py`  
to manage logic and state.

🔗 **File:** [`main.py`](main.py)

---

## 🗣️ Voice Interaction

Baymax is activated by saying the wake word **"baymax"**.  
Once activated, it enters an "awake" state for 15–60 seconds.

During this time, the user can say:
- Health-related phrases (e.g., “I feel dizzy”)
- Simple robot commands (e.g., “wave hello”, “turn left”)

The voice system is written in Python using `speech_recognition`, `gTTS`,  
`ChatterboxTTS`, and `pygame`.

It also handles:
- Emotion-specific clip playback (e.g., pain, fever, sleep)
- Temporary file cleanup
- Ambient noise calibration

🔗 **File:** [`stt.py`](stt.py)

---

## 👁️ Vision System (OpenCV)

Baymax uses **OpenCV** with a **Pi Camera** for face detection only.

### Face Detection

Baymax checks for a human face before performing temperature checks.  
It uses Haar cascades, processes small frames for speed, and loops for 5 seconds  
before timing out.

🔗 **File:** [`face_detection.py`](face_detection.py)

### Object Detection and Avoidance (Now Handled by LiDAR)

Baymax no longer uses its camera for object detection.  
Instead, it integrates a **LiDAR sensor** (e.g., RPLIDAR A1) to detect obstacles,  
plan safe movement, and provide 360° environmental awareness.

This allows Baymax to function in low light and cluttered spaces,  
making movement and interaction more robust.

---

## 🔩 Folding Mechanism: Dual-Frame Scissor Lift

To simulate Baymax’s inflatable and collapsible body,  
a mechanical **dual-frame scissor-lift system** is used as the torso.

The structure consists of two square frames.  
Each frame has a scissor mechanism mounted on opposite inner sides.  
The grooves and pegs of these mechanisms face inward.

A **rack** is attached along each groove, and a **gear** sits in the center,  
meshed with both racks. This gear is connected to a **single high-torque servo motor**  
which rotates to expand or collapse the mechanism.

As the servo turns:
- The gear drives both racks outward, causing the scissor arms to expand vertically
- After full expansion, the diagonal braces form an "X" across the opposing corners  
  for structural stability

Reversing the motor collapses the system back into a flat, compressed form.  
This compact, gear-driven design is sturdy and gives Baymax a lifelike motion  
while saving space and parts.

The entire assembly is modeled in **Fusion 360**  
and driven by Arduino-controlled servo logic.

---

## 🧠 Health AI (Gemini 2.0 Flash)

The file `api.py` connects Baymax to **Google's Gemini Flash model**,  
acting as a calm, polite, and friendly healthcare assistant.

Baymax listens to symptoms like:
- “I have a sore throat”
- “I feel anxious”
- “I am tired and hot”

And responds with suggestions like:
- “Drink warm fluids and rest”
- “Take a short break”
- “You might have a fever, let me check your temperature”

It does not diagnose but gives first-line advice — just like a virtual nurse.

🔗 **File:** [`api.py`](api.py)

---

## 🧪 Example Voice Commands

- `"Baymax, introduce yourself"`  
- `"Baymax, wave hello"`  
- `"Baymax, what's my temperature?"`  
- `"Baymax, I have a headache"`  
- `"Baymax, walk forward"`  

Non-action commands are passed to the health AI model.

---

## 📡 Hardware System Diagram

A full system schematic of Baymax’s electronics is shown below:

![Baymax Schematic Overview](Baymax_Schematic_Overview.png)

The full circuit is also available in KiCad format:  
📄 [`baymax-circuit.kicad_sch`](baymax-circuit.kicad_sch)

---

## 🛠️ Hardware Used

- Raspberry Pi 4 (main control computer)  
- Arduino Nano / Mega (servo + motor control)  
- MLX90614 IR Temperature Sensor  
- Pi Camera Module  
- RPLIDAR A1 (for object detection & avoidance)  
- TowerPro MG90S Servos (arms)  
- 20kg Servo Motor (torso folding)  
- L298N or TB6612 Motor Driver (for walking legs)  
- INMP441 or MAX9814 Microphone Module  
- MAX98357 Amplifier / 3W Speaker  
- PCA9685 16-channel PWM Servo Driver  
- MP1584 5V Buck Converter  
- 7.4V–12V Li-ion Battery  
- 3D-printed or aluminum chassis

---

## ⚙️ Software & Libraries

- Python 3  
- OpenCV (`opencv-python`)  
- Speech Recognition (`speechrecognition`)  
- Google TTS (`gTTS`) + `ChatterboxTTS`  
- Gemini API (`google-generativeai`)  
- Pygame, Torchaudio, Pydub  
- Adafruit MLX90614 and PCA9685 libraries  
- Arduino IDE (C++)  

---

## 🧰 Full Project Stack

### 🧠 Software Stack

| Tool / Platform            | Purpose                                   |
| -------------------------- | ----------------------------------------- |
| **Raspberry Pi OS (Lite)** | Headless control computer (Python apps)   |
| **Arduino IDE**            | Programming Arduino Nano (leg motors)     |
| **KiCad (v7+)**            | PCB schematic and layout                  |
| **Fusion 360**             | 3D CAD for mechanical design and printing |
| **VS Code** (optional)     | Code editing & serial monitor             |
| **Docker** (optional)      | ROS2 + LiDAR container (future expansion) |

### 🧰 Python Libraries (Raspberry Pi)

| Library                           | Purpose                               |
| --------------------------------- | ------------------------------------- |
| `smbus2` or `board` + `busio`     | I²C communication (MLX90614, PCA9685) |
| `adafruit-circuitpython-mlx90614` | MLX90614 temperature sensor           |
| `adafruit-pca9685`                | 16-channel PWM servo control          |
| `opencv-python`                   | Vision processing (Pi Camera)         |
| `pygame`                          | Audio playback (speaker output)       |
| `sounddevice` / `pyaudio`         | Microphone audio input                |
| `pyserial`                        | UART communication with Arduino       |
| `numpy`, `time`, `os`             | General utility                       |

### 🔩 Arduino Libraries

| Library                      | Purpose                                     |
| ---------------------------- | ------------------------------------------- |
| `Servo.h`                    | Control folding and leg motion (via servos) |
| `SoftwareSerial` (if needed) | UART communication with Raspberry Pi        |

---

## 🧷 Optional / Planned Add-ons

- **OLED or LED matrix** – animated face or expressions  
- **Touch sensors** – for physical interaction  
- **Voice assistant** – using NLP for conversational replies

---
