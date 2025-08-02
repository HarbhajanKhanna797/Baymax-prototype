import requests
import pygame
import time

def get_tts_audio(text, save_as='response.wav', laptop_ip='192.168.0.X', port=5000, prompt_path=None):
    url = f'http://{laptop_ip}:{port}/speak'
    payload = {'text': text}
    if prompt_path:
        payload['audio_prompt_path'] = prompt_path

    print(f"[INFO] Sending text to laptop server: '{text}'")
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            with open(save_as, 'wb') as f:
                f.write(response.content)
            print(f"[INFO] Audio received and saved as '{save_as}'")
            return save_as
        else:
            print(f"[ERROR] Server responded with status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Failed to connect to server: {str(e)}")
        return None

def play_audio(file_path):
    print(f"[INFO] Playing audio file: {file_path}")
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        print("[INFO] Playback finished.")
    except Exception as e:
        print(f"[ERROR] Playback failed: {str(e)}")

# Example usage
if __name__ == '__main__':
    text = "Hello, I am Baymax your personal healthcare companion."
    laptop_ip = "172.23.64.1"  # 🔧 Change to your laptop's local IP
    audio_file = get_tts_audio(text, save_as="baymax_response.wav", laptop_ip=laptop_ip)
    if audio_file:
        play_audio(audio_file)
