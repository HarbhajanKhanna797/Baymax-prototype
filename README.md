# 🤖 Project Baymax

**Project Baymax** is a soft-bodied, voice-activated healthcare companion robot  
inspired by *Baymax* from Disney's *Big Hero 6*.

While not as advanced as the fictional version, this real-world robot can listen, talk,  
analyze basic symptoms, measure temperature, perform gestures, detect faces and objects,  
simulate walking, and fold its body using a custom mechanical structure.

It is built using affordable electronics like **Arduino**, **Raspberry Pi**, and controlled via **Python**,  
**OpenCV**, and **Google’s Gemini AI** for interactive intelligence.

---

## 📌 What It Does

Baymax can interact with people just by listening to their voice.  
It checks your temperature, listens to symptoms, offers health suggestions,  
and can perform basic actions like waving, walking, or turning.

It can also detect human faces and nearby objects through a camera,  
and even fold or expand its body using a scissor-lift mechanism.

---

## ✨ Features

- **Voice-controlled interaction** with wake word `"baymax"`
- **Speech-to-text** and **text-to-speech** for natural conversations
- **Health symptom analysis** using AI-powered response system
- **Face and object detection** using OpenCV and Pi Camera
- **Temperature sensing** with a non-contact IR sensor (MLX90614)
- **Gesture-based actions** like waving, sitting, and walking
- **Scissor-lift-based folding design** to simulate a soft body
- **Human-like walking** using alternating servo PWM control

---

## 🔩 Folding Mechanism: Scissor Lift

To mimic Baymax’s inflatable soft body,  
the robot uses a mechanical **scissor-lift** structure as its torso.

This structure is made of multiple "X"-shaped linkages that are connected at pivot points.  
When a servo motor pushes or pulls one end horizontally, the "X" links expand vertically,  
lifting the upper part of the body smoothly.

Reversing the motion causes the entire frame to collapse back down.  
This expansion and compression simulate Baymax "inflating" when active,  
and "deflating" or going to sleep when idle.

This system is simple, low-cost, and controlled with just one servo motor.  
It adds personality to the robot and makes it compact when not in use.

---

## 🗣️ Voice Interaction

Baymax is activated by saying the wake word **"baymax"**.  
Once activated, it enters an "awake" state for 15 seconds.

During this time, the user can say:
- Health-related phrases (e.g., “I feel dizzy”)
- Simple robot commands (e.g., “wave hello”, “turn left”)

The voice system is written in Python using the `speech_recognition` and `gTTS` libraries.  
It converts the user's speech to text and either routes it as a command  
or sends it to the health AI system if it's a symptom-related query.

🔗 **File:** [`STT.py`](stt.py) — contains the full voice activation and command-routing logic.

---

## 🧠 Health AI (Gemini 2.0 Flash)

The file `api.py` connects Baymax to **Google's Gemini 2.0 Flash model**,  
which acts as a calm, polite, and helpful health companion.

It takes the user's spoken symptoms (like “I have a sore throat”)  
and returns suggestions such as:
- Taking rest
- Drinking fluids
- Visiting a hospital if needed

The model does not diagnose but gives first-level advice,  
similar to how a virtual nurse or therapist might respond.

Mental health prompts like "I'm anxious" are also handled with care,  
providing calming suggestions without judgment.

🔗 **File:** [`api.py`](api.py) — contains the prompt logic and AI integration code.

---

## 👁️ Vision System (OpenCV)

Baymax uses **OpenCV** with a **Pi Camera** to detect faces and objects.

### Face Detection
Baymax can detect when a human is in front of it.  
This allows it to:
- Greet users
- Turn toward them
- Begin interactions automatically

Face detection is done using Haar Cascades or DNN-based face detectors.

### Object Detection
The robot can also recognize basic objects such as phones or bottles.  
This makes Baymax aware of its environment and allows future upgrades  
like obstacle avoidance or object-based interaction.

This all runs locally on the Raspberry Pi with no internet delay.

---

## 🚶 Walking Simulation

Baymax doesn’t walk with legs like a human,  
but simulates walking using servos and creative timing of PWM signals.

Two or more servos control the “legs”.  
By alternating movements (like lifting and pushing),  
Baymax creates the illusion of walking in place or slightly forward.

Adding slight torso sway and arm motion makes the walking feel more natural.

This method is simple yet effective for demonstrating motion on a flat surface.

---

## 🧪 Example Voice Commands

Here are some sample things you can say to Baymax:

- `"Baymax, introduce yourself"`  
- `"Baymax, wave hello"`  
- `"Baymax, what's my temperature?"`  
- `"Baymax, I have a headache"`  
- `"Baymax, walk forward"`  

If the command is not recognized as movement,  
it is treated as a health concern and passed to the AI model.

---

## 🛠️ Hardware Used

- Arduino UNO / Mega (for servos and sensor control)  
- Raspberry Pi (3B+ or 4)  
- MLX90614 Infrared Temperature Sensor  
- Pi Camera  
- Servo Motors (arms, legs, scissor lift)  
- Microphone and speaker (for voice interaction)  
- Basic frame materials (aluminum rods, joints, etc.)

---

## ⚙️ Software & Libraries

- Python 3  
- OpenCV (`opencv-python`)  
- Speech Recognition (`speechrecognition`)  
- Google Text-to-Speech (`gTTS`)  
- Gemini API (`google-generativeai`)  
- Arduino IDE for microcontroller programming

---

