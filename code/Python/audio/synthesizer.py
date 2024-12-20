import numpy as np
import sounddevice as sd

# Function to generate a sine wave
def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.5):
    """
    Generate a sine wave of a given frequency and duration.
    
    :param frequency: Frequency of the sine wave (in Hz).
    :param duration: Duration of the wave in seconds.
    :param sample_rate: Sample rate (samples per second, default is 44100 Hz).
    :param amplitude: Amplitude of the wave (default is 0.5).
    :return: A numpy array representing the sine wave.
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

# Function to play a tone
def play_tone(frequency, duration, sample_rate=44100, amplitude=0.5):
    """
    Generate and play a sine wave of a given frequency.
    
    :param frequency: Frequency of the tone in Hz.
    :param duration: Duration of the tone in seconds.
    :param sample_rate: Sample rate (default is 44100 Hz).
    :param amplitude: Amplitude of the tone (default is 0.5).
    """
    wave = generate_sine_wave(frequency, duration, sample_rate, amplitude)
    sd.play(wave, samplerate=sample_rate)
    sd.wait()  # Wait until the sound has finished playing

# Main function to play a sequence of notes (like a melody)
def play_melody():
    # Define the melody as a list of (frequency, duration) tuples
    melody = [
        (261.63, 0.5),  # C4
        (293.66, 0.5),  # D4
        (329.63, 0.5),  # E4
        (349.23, 0.5),  # F4
        (392.00, 0.5),  # G4
        (440.00, 0.5),  # A4
        (493.88, 0.5),  # B4
        (523.25, 0.5)   # C5
    ]
    
    for note in melody:
        frequency, duration = note
        play_tone(frequency, duration)
    
# Main loop to run the synthesizer
if __name__ == "__main__":
    print("Playing melody...")
    play_melody()
    print("Melody finished!")
