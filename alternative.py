# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import librosa
# import numpy as np
# from music21 import pitch

# app = Flask(__name__)
# CORS(app)

# @app.route('/')
# def index():
#     return 'Hello from Flask!'

# @app.route('/extract_notes', methods=['POST'])
# def extract_notes():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     file = request.files['file']
#     file_content = file.read()
#     print(f"Received file with size: {len(file_content)}")
#     file.seek(0)
    
#     # Load the audio file using pydub
#     audio = AudioSegment.from_file(file)
#     print(f"File format: {audio.format}")
#     print(f"File channels: {audio.channels}")
#     print(f"File frame rate: {audio.frame_rate}")
#     print(f"File duration (ms): {len(audio)}")

#     # Create a temporary directory and save the file there
#     temp_dir = tempfile.mkdtemp()
#     file_path = os.path.join(temp_dir, secure_filename(file.filename))
#     # Save the file as a WAV file
#     audio.export(file_path, format="wav")

#     try:
#         # Load the audio file using librosa
#         y, sr = librosa.load(file_path)
        
#         # Compute the short-time Fourier Transform (stft)
#         D = np.abs(librosa.stft(y))

#         # Compute the pitch (in Hz)
#         pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

#         # Select out pitches with high amplitudes
#         pitches = pitches[magnitudes > np.median(magnitudes)]
        
#         # Convert frequencies in Hz to note names
#         notes = [pitch.Pitch(freq).name for freq in pitches]
#     finally:
#         # Remove the temporary directory and its contents
#         shutil.rmtree(temp_dir)
    
#     return jsonify({"notes": notes}), 200
