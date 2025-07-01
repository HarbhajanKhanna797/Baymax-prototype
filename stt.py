import speech_recognition as sr
import time
from torchaudio import save as save
from pydub import AudioSegment 
import os
import contextlib
import pyttsx3 
import sounddevice as sd 

with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    from pygame import mixer

# def speech_to_text(recognizer, mic):
#     with mic as source:
#         recognizer.adjust_for_ambient_noise(source, duration=1)

#         audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
#         try:
#             command = recognizer.recognize_google(audio).lower()
#             return command

#         except sr.UnknownValueError:
#             print("Sorry, I didn't catch that.")
#         except sr.RequestError:
#             print("Could not reach the speech recognition service.")
#         except sr.WaitTimeoutError:
#             print("No speech detected. Still awake...")

def speech_to_text(recognizer, duration):
    samplerate = 16000
    audio = sd.rec(int(samplerate*duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()

    audio_data = sr.AudioData(audio.tobytes(), samplerate, 2)
    command = recognizer.recognize_google(audio_data).lower()
    return command

def generate_speech_to_text(model, text):
    AUDIO_PROMPT_PATH = "audio-files/baymax_clip_1_clean.wav"
    wav = model.generate(text, audio_prompt_path=AUDIO_PROMPT_PATH)
    save("temp.wav", wav, model.sr)

def convert_to_pcm(filename):
    audio = AudioSegment.from_file(filename + ".wav", format="wav")
    audio = audio.set_sample_width(2)  # 2 bytes = 16-bit
    audio = audio.set_channels(1)      # mono
    audio = audio.set_frame_rate(16000)
    audio.export(filename + "_converted.wav", format="wav")

def generate_speech(model, text):
    print("Baymax says:", text)
    generate_speech_to_text(model, text)

    # Play the generated audio
    convert_to_pcm("temp")
    if os.path.exists("temp.wav"):
        os.remove("temp.wav")

def speak(filename):
    mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    sound = mixer.Sound("audio-files/" + filename + ".wav")
    channel = sound.play()
    while channel.get_busy():
        time.sleep(0.1)
    mixer.quit()

def speak_baymax(text):
    engine = pyttsx3.init(driverName="espeak")

    # Optional: Make voice sound more Baymax-like
    engine.setProperty('rate', 110)     # Slow speech
    engine.setProperty('volume', 0.9)   # Softer voice

    # Choose male/female voice if available
    voices = engine.getProperty('voices')
    for voice in voices:
        if "male" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    engine.say(text)
    engine.runAndWait()
    engine.stop()

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    WAKE_WORD = "bayma"
    AWAKE_DURATION = 15
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
                                #route_command(command)


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
