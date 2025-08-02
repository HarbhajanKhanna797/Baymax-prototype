import requests
import pygame
import time
import os

def get_tts_audio(text, save_as='response.wav', laptop_ip='192.168.0.X', port=5000, prompt_path=None):
    url = f'http://{laptop_ip}:{port}/speak'
    payload = {'text': text}
    if prompt_path:
        payload['audio_prompt_path'] = prompt_path

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            with open(save_as, 'wb') as f:
                f.write(response.content)
            print(f"Audio saved as {save_as}")
            return save_as
        else:
            print("Error:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Connection error:", str(e))
        return None

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

# Example usage
if __name__ == '__main__':
    text = "Hello, I am Baymax your personal healthcare companion."
    audio_file = get_tts_audio(text, save_as="baymax_response.wav", laptop_ip="192.168.0.X")
    if audio_file:
        play_audio(audio_file)
