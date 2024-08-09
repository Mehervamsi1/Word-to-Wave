# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/next_page')
# def next_page():
#     return render_template('next_page.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
# from flask import Flask, render_template, request
# import os
#
# app = Flask(__name__)
#
# # Create a directory for recordings if it doesn't exist
# os.makedirs('static/Recordings', exist_ok=True)
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/next_page')
# def next_page():
#     return render_template('next_page.html')
#
# @app.route('/save_audio', methods=['POST'])
# def save_audio():
#     if 'audio' not in request.files:
#         return 'No audio file found', 400
#
#     audio_file = request.files['audio']
#     if audio_file:
#         file_path = os.path.join('static/Recordings', 'recording.wav')
#         audio_file.save(file_path)  # Save the file in WAV format
#         return 'Audio saved successfully', 200
#
#     return 'Failed to save audio', 500
#
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Create a directory for recordings if it doesn't exist
os.makedirs('static/Recordings', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next_page')
def next_page():
    return render_template('next_page.html')

@app.route('/save_audio', methods=['POST'])
def save_audio():
    if 'audio' not in request.files:
        return 'No audio file found', 400

    audio_file = request.files['audio']
    if audio_file:
        wav_file_path = os.path.join('static/Recordings', 'recording.wav')
        audio_file.save(wav_file_path)  # Save the file in WAV format

        # # Rename the .wav file to .flac
        # flac_file_path = os.path.join('static/Recordings', 'recording.flac')
        # os.rename(wav_file_path, flac_file_path)

        return 'Audio saved successfully', 200

    return 'Failed to save audio', 500


@app.route('/get_text_output', methods=['GET'])
def get_text_output():
    return 'Hi success'

if __name__ == '__main__':
    app.run(debug=True)
