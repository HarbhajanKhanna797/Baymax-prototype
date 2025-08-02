from flask import Flask, request, send_file, jsonify
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
import uuid
import os

app = Flask(__name__)

# 🔧 Change this to "cpu" if you're not using a GPU
model = ChatterboxTTS.from_pretrained(device="cuda")

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text', '')
    prompt_path = data.get('audio_prompt_path', r"audio-files/baymax_clip_1_clean.wav")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    output_filename = f"output_{uuid.uuid4().hex}.wav"

    try:
        if prompt_path:
            wav = model.generate(text, audio_prompt_path=prompt_path)
        else:
            wav = model.generate(text)

        # Convert float32 tensor → 16-bit PCM → compatible with pygame
        wav_pcm16 = (wav * 32767.0).clamp(min=-32768, max=32767).short()
        ta.save(output_filename, wav_pcm16, model.sr, encoding="PCM_S", bits_per_sample=16)

        return send_file(output_filename, mimetype='audio/wav')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 🔧 If you want to restrict to local machine, use host='127.0.0.1'
    app.run(host='0.0.0.0', port=5000)
