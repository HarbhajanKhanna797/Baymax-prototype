from flask import Flask, request, send_file, jsonify
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
import uuid
import os
import torch

app = Flask(__name__)

# 🔧 Set device
DEVICE = "cuda"  # Change to "cpu" if you don't have a GPU

print("[INFO] Loading ChatterboxTTS model...")
model = ChatterboxTTS.from_pretrained(device=DEVICE)
print(f"[INFO] Model loaded on device: {DEVICE}")

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text', '')
    prompt_path = data.get('audio_prompt_path', None)

    print(f"[INFO] Received request: text='{text}'")
    if prompt_path:
        print(f"[INFO] Using audio prompt: {prompt_path}")

    if not text:
        print("[ERROR] No text provided in request.")
        return jsonify({"error": "No text provided"}), 400

    output_filename = f"output_{uuid.uuid4().hex}.wav"

    try:
        print("[INFO] Generating speech...")
        if prompt_path:
            wav = model.generate(text, audio_prompt_path=prompt_path)
        else:
            wav = model.generate(text)

        print("[INFO] Converting to 16-bit PCM WAV format for pygame compatibility...")
        wav_pcm16 = (wav * 32767.0).clamp(min=-32768, max=32767).short()
        ta.save(output_filename, wav_pcm16, model.sr, encoding="PCM_S", bits_per_sample=16)

        print(f"[INFO] Audio file saved as '{output_filename}', sending to client...")
        return send_file(output_filename, mimetype='audio/wav')

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("[INFO] Starting Flask server on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)
