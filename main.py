from flask import Flask, request, jsonify
from flask_cors import CORS
from aubio import source, pitch, note2midi
from werkzeug.utils import secure_filename
import os
import tempfile
import shutil
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello from Flask!'

@app.route('/extract_notes', methods=['POST'])
def extract_notes():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    file_content = file.read()
    print(f"Received file with size: {len(file_content)}")
    file.seek(0)
    
    # Load the audio file using pydub
    audio = AudioSegment.from_file(file)
    print(f"File format: {audio.format}")
    print(f"File channels: {audio.channels}")
    print(f"File frame rate: {audio.frame_rate}")
    print(f"File duration (ms): {len(audio)}")

    # Create a temporary directory and save the file there
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, secure_filename(file.filename))
    # Save the file as a WAV file
    audio.export(file_path, format="wav")
    
    try:
        win_s = 4096
        hop_s = win_s // 2
        s = source(file_path, 0, hop_s)
        tolerance = 0.8
        pitch_o = pitch("yin", win_s, hop_s, s.samplerate)
        pitch_o.set_unit("midi")
        pitch_o.set_tolerance(tolerance)
        pitches = []
        while True:
            samples, read = s()
            pitch_val = pitch_o(samples)[0]
            # Only append pitches above a certain threshold to eliminate noise
            if pitch_val > 0.0:
                pitches.append(pitch_val)
            if read < hop_s:
                break
        # Convert pitches to musical notes
        notes = [note2midi.pitch2note(p) for p in pitches]
        print('done')
    finally:
        # Remove the temporary directory and its contents
        shutil.rmtree(temp_dir)
    
    return jsonify({"notes": notes}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
