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

