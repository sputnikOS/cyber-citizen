import numpy as np
import scipy.io.wavfile as wav
import os

def db_to_linear(db):
    return 10 ** (db / 20.0)

def linear_to_db(linear):
    return 20 * np.log10(np.maximum(linear, 1e-10))

def compressor(audio, threshold_db=-20, ratio=4.0, attack_ms=10, release_ms=100, sample_rate=44100):
    attack_coeff = np.exp(-1.0 / (sample_rate * (attack_ms / 1000.0)))
    release_coeff = np.exp(-1.0 / (sample_rate * (release_ms / 1000.0)))

    gain = np.ones_like(audio)
    envelope = 0.0

    threshold = db_to_linear(threshold_db)

    for i in range(len(audio)):
        input_level = abs(audio[i])
        if input_level > envelope:
            envelope = attack_coeff * (envelope - input_level) + input_level
        else:
            envelope = release_coeff * (envelope - input_level) + input_level

        if envelope > threshold:
            gain_reduction = 1 + (np.log10(envelope / threshold) * (1.0 - 1.0 / ratio))
            gain[i] = 1 / (10 ** gain_reduction)
        else:
            gain[i] = 1.0

    return audio * gain

# --- Load and process audio ---

input_file = 'input.wav'
output_file = 'compressed_output.wav'

# Read audio file
sample_rate, data = wav.read(input_file)

# Normalize to float32 if int16
if data.dtype == np.int16:
    data = data.astype(np.float32) / 32768.0

# If stereo, just compress one channel (extend to both if needed)
if data.ndim > 1:
    compressed = np.column_stack([
        compressor(data[:, ch], sample_rate=sample_rate)
        for ch in range(data.shape[1])
    ])
else:
    compressed = compressor(data, sample_rate=sample_rate)

# Rescale and save as int16
compressed_int16 = np.int16(np.clip(compressed, -1.0, 1.0) * 32767)
wav.write(output_file, sample_rate, compressed_int16)

print(f"Compression complete. Output written to {output_file}")
