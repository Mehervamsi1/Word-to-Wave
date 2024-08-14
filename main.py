# print('hello')
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

audio_path = r'recording.wav' #'LJ038-0015.wav' #
transcription = 'bla bla'

audio_list = [audio_path.split(".")[0]]
transcription_list = [transcription]

df_audio = pd.DataFrame({'file_name': audio_list, 'normalized_transcription': transcription_list})

import subprocess
def encode_audio_sample(wav_file, label):
    ###########################################
    ##  Process the Audio
    ##########################################
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
# model = tf.keras.models.load_model(model_path, custom_objects={'CTCLoss': CTCLoss})

# Check results on test dataset
audio_predictions = []
audio_targets = []
for batch in audio_dataset:
    c,d = batch
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


print(''.join(audio_predictions))