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

from pydub import AudioSegment


import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers



import subprocess

# global df_audio
def encode_audio_sample(wav_file, label):
    ###########################################
    ##  Process the Audio
    ##########################################
    global df_audio
    subprocess.run(['ffmpeg', '-i', df_audio['file_name'][0] + ".wav", '-y', df_audio['file_name'][0]+'_new' + ".wav"])
    # 1. Read wav file
    file = tf.io.read_file(df_audio['file_name'][0]+'_new' + '.wav')
    # 2. Decode the wav file
    audio, _ = tf.audio.decode_wav(file)
    audio = tf.squeeze(audio, axis=-1)
    # 3. Change type to float
    audio = tf.cast(audio, tf.float32)
    # 4. Get the spectrogram
    spectrogram = tf.signal.stft(
        audio, frame_length=frame_length, frame_step=frame_step, fft_length=fft_length
    )
    # 5. We only need the magnitude, which can be derived by applying tf.abs
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.math.pow(spectrogram, 0.5)
    # 6. Normalisation
    means = tf.math.reduce_mean(spectrogram, 1, keepdims=True)
    stddevs = tf.math.reduce_std(spectrogram, 1, keepdims=True)
    spectrogram = (spectrogram - means) / (stddevs + 1e-10)
    ###########################################
    ##  Process the label
    ##########################################
    # 7. Convert label to Lower case
    label = tf.strings.lower(label)
    # 8. Split the label
    label = tf.strings.unicode_split(label, input_encoding="UTF-8")
    # 9. Map the characters in label to numbers
    label = char_to_num(label)
    # 10. Return a dict as our model is expecting two inputs
    return spectrogram, label

# An integer scalar Tensor. The window length in samples.
frame_length = 256
# An integer scalar Tensor. The number of samples to step.
frame_step = 160
# An integer scalar Tensor. The size of the FFT to apply.
fft_length = 384
# The set of characters accepted in the transcription.
characters = [x for x in "abcdefghijklmnopqrstuvwxyz'?! "]
# Mapping characters to integers
char_to_num = keras.layers.StringLookup(vocabulary=characters, oov_token="")
# Mapping integers back to original characters
num_to_char = keras.layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), oov_token="", invert=True
)

# print(
#     f"The vocabulary is: {char_to_num.get_vocabulary()} "
#     f"(size ={char_to_num.vocabulary_size()})"
# )

# A utility function to decode the output of the network
def decode_audio_predictions(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0]
    # Iterate over the results and get back the text
    output_text = []
    for result in results:
        result = tf.strings.reduce_join(num_to_char(result)).numpy().decode("utf-8")
        output_text.append(result)
    return output_text



def CTCLoss(y_true, y_pred):
    # Compute the training-time loss value
    batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
    input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
    label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")

    input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")

    loss = tf.keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)
    return loss
model = tf.keras.models.load_model('speech_to_text_model.keras', custom_objects={'CTCLoss': CTCLoss})


from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Create a directory for recordings if it doesn't exist
os.makedirs('static/Recordings', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wordToWave')
def next_page():
    return render_template('next_page.html')

# @app.route('/save_audio', methods=['POST'])  # initiall way of saving audio
# def save_audio():
#     if 'audio' not in request.files:
#         return 'No audio file found', 400
#
#     audio_file = request.files['audio']
#     if audio_file:
#         wav_file_path = os.path.join('static/Recordings', 'recording.wav')
#         audio_file.save(wav_file_path)  # Save the file in WAV format
#
#         # # Rename the .wav file to .flac
#         # flac_file_path = os.path.join('static/Recordings', 'recording.flac')
#         # os.rename(wav_file_path, flac_file_path)
#
#         return 'Audio saved successfully', 200
#
#     return 'Failed to save audio', 500


@app.route('/save_audio', methods=['POST'])
def save_audio():
    if 'audio' not in request.files:
        return 'No audio file found', 400

    audio_file = request.files['audio']
    if audio_file:
        # Convert audio to WAV format using pydub
        audio = AudioSegment.from_file(audio_file)  # Automatically detects the format
        wav_file_path = os.path.join('static/Recordings', 'recording.wav')

        audio.export(wav_file_path, format="wav")  # Export the file in WAV format

        return 'Audio saved successfully', 200

    return 'Failed to save audio', 500


@app.route('/get_text_output', methods=['GET'])
def get_text_output():
    audio_path = r'static/Recordings/recording.wav'  # 'LJ038-0015.wav' #
    transcription = 'bla bla'

    audio_list = [audio_path.split(".")[0]]
    transcription_list = [transcription]
    global df_audio

    df_audio = pd.DataFrame({'file_name': audio_list, 'normalized_transcription': transcription_list})
    audio_predictions = []

    # Create dataset from the extracted data
    audio_dataset = tf.data.Dataset.from_tensor_slices((df_audio['file_name'], df_audio['normalized_transcription']))

    # Apply preprocessing function
    audio_dataset = audio_dataset.map(encode_audio_sample, num_parallel_calls=tf.data.AUTOTUNE)

    # Define batch size
    batch_size = 32  # Set this to your desired batch size

    # Batch and prefetch the dataset
    audio_dataset = (
        audio_dataset
        .padded_batch(batch_size)  # Pad sequences and batch
        .prefetch(buffer_size=tf.data.AUTOTUNE)  # Prefetch for optimization
    )

    audio_targets = []
    for batch in audio_dataset:
        c, d = batch
        batch_predictions = model.predict(c)
        batch_predictions = decode_audio_predictions(batch_predictions)
        audio_predictions.extend(batch_predictions)
        # for label in d:
        #     label = tf.strings.reduce_join(num_to_char(label)).numpy().decode("utf-8")
        #     audio_targets.append(label)

    # # Calculate WER for the test dataset
    # audio_wer_score = wer(audio_targets, audio_predictions)
    # print("-" * 100)
    # print(f"Word Error Rate for Test Dataset: {audio_wer_score:.4f}")
    # print("-" * 100)

    return ''.join(audio_predictions)
    # return 'Hi 1234?'



@app.route('/upload', methods=['POST'])
def upload_wav():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    if file and file.filename.endswith('.wav'):
        save_path = os.path.join('static/Recordings', 'recording.wav')
        file.save(save_path)
        return 'File uploaded successfully', 200

    return 'Invalid file type', 400

if __name__ == '__main__':
    app.run(debug=True)
