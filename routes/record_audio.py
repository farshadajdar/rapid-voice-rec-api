from flask import Blueprint, request, jsonify
from pydub import AudioSegment
import os
import datetime
import uuid

record_bp = Blueprint('record', __name__)

RECORDINGS_FOLDER = "recordings"
os.makedirs(RECORDINGS_FOLDER, exist_ok=True)

@record_bp.route('/record', methods=['POST'])
def record_audio():
    audio_file = request.files.get("audio")

    if not audio_file:
        return jsonify({"error": "Missing audio file"}), 400

    # Generate a unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_id = str(uuid.uuid4())[:8]
    original_path = os.path.join(RECORDINGS_FOLDER, f"raw_{timestamp}_{file_id}")
    audio_file.save(original_path)

    # Try to convert to .wav (16000Hz mono)
    try:
        audio = AudioSegment.from_file(original_path)
        audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
        wav_filename = f"mic_capture_{timestamp}_{file_id}.wav"
        wav_path = os.path.join(RECORDINGS_FOLDER, wav_filename)
        audio.export(wav_path, format="wav")

        # Remove raw file after conversion
        os.remove(original_path)

        return jsonify({
            "message": "Recording saved",
            "filename": wav_filename
        })

    except Exception as e:
        return jsonify({"error": f"Audio conversion failed: {str(e)}"}), 500
