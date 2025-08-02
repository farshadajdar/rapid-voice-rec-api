from flask import Blueprint, request, jsonify
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
import wave
import json
from fuzzywuzzy import fuzz

from trainer.normalizer import normalize                 
from trainer.grammar import generate_grammar         

voice_bp = Blueprint('voice', __name__)
model = Model("model")  # Load Vosk model once

# 🎵 Convert uploaded audio to 16kHz mono 16-bit PCM WAV
def convert_to_vosk_wav(source_path, output_path="test.wav"):
    try:
        audio = AudioSegment.from_file(source_path)
        audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
        audio.export(output_path, format="wav")
        return output_path
    except Exception as e:
        print(f"❌ Audio conversion failed: {e}")
        return None

@voice_bp.route('/check-voice', methods=['POST'])
def check_voice():
    expected_phrase = request.form.get("expected")
    audio_file = request.files.get("audio")

    print("🔎 Received expected:", expected_phrase)
    print("🔎 Received audio file:", audio_file.filename if audio_file else "None")

    if not expected_phrase:
        return jsonify({"error": "Missing expected phrase"}), 400
    if not audio_file:
        return jsonify({"error": "Missing audio file"}), 400

    original_path = "original_input_audio"
    audio_file.save(original_path)

    # Convert to Vosk-compatible WAV
    wav_path = convert_to_vosk_wav(original_path)
    if not wav_path:
        return jsonify({"error": "Failed to convert audio"}), 500

    wf = wave.open(wav_path, "rb")

    # 🔤 Use modular grammar from trainer.grammar
    grammar = generate_grammar()

    # 🎤 Create recognizer with custom grammar
    recognizer = KaldiRecognizer(model, wf.getframerate(), json.dumps(grammar))

    recognized_text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text_chunk = result.get("text", "")
            # print("✅ Result:", text_chunk)
            recognized_text += " " + text_chunk
        else:
            partial = json.loads(recognizer.PartialResult())
            # print("⏳ Partial:", partial.get("partial", ""))

    final_result = json.loads(recognizer.FinalResult())
    recognized_text += " " + final_result.get("text", "")
    wf.close()

    # 🔍 Normalize and compare
    expected_norm = normalize(expected_phrase)
    recognized_norm = normalize(recognized_text)

    match_ratio = fuzz.ratio(expected_norm, recognized_norm)
    is_match = match_ratio >= 60  # Adjust this if needed

    print(f"🧠 Expected:   {expected_norm}")
    print(f"🧠 Recognized: {recognized_norm}")
    print(f"🧮 Match ratio: {match_ratio} → Match: {is_match}")

    return jsonify({
        "expected": expected_norm,
        "recognized": recognized_norm,
        "match": is_match,
        "match_ratio": match_ratio
    })

__all__ = ['voice_bp']
