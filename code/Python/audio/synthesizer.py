import numpy as np
import sounddevice as sd

class Oscillator:
    def __init__(self, wave_type='sine', frequency=440, sample_rate=44100, amplitude=0.5):
        self.wave_type = wave_type
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.amplitude = amplitude

    def generate_wave(self, duration):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        if self.wave_type == 'sine':
            wave = np.sin(2 * np.pi * self.frequency * t)
        elif self.wave_type == 'square':
            wave = np.sign(np.sin(2 * np.pi * self.frequency * t))
        elif self.wave_type == 'sawtooth':
            wave = 2 * (t * self.frequency - np.floor(t * self.frequency + 0.5))
        elif self.wave_type == 'triangle':
            wave = np.abs(2 * (t * self.frequency - np.floor(t * self.frequency + 0.5))) * 2 - 1
        else:
            wave = np.zeros_like(t)
        return self.amplitude * wave

class EnvelopeGenerator:
    def __init__(self, attack=0.1, decay=0.1, sustain=0.7, release=0.2, sample_rate=44100):
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.sample_rate = sample_rate

    def generate_envelope(self, duration):
        attack_samples = int(self.attack * self.sample_rate)
        decay_samples = int(self.decay * self.sample_rate)
        release_samples = int(self.release * self.sample_rate)
        sustain_samples = int(duration * self.sample_rate) - (attack_samples + decay_samples + release_samples)
        
        attack = np.linspace(0, 1, attack_samples)
        decay = np.linspace(1, self.sustain, decay_samples)
        sustain = np.ones(sustain_samples) * self.sustain
        release = np.linspace(self.sustain, 0, release_samples)
        
        return np.concatenate((attack, decay, sustain, release))

class Filter:
    def __init__(self, cutoff=1000, sample_rate=44100, resonance=0.5):
        self.cutoff = cutoff
        self.sample_rate = sample_rate
        self.resonance = resonance

    def apply_filter(self, signal):
        # Simple low-pass filter using a moving average
        filter_size = int(self.sample_rate / self.cutoff)
        filtered_signal = np.convolve(signal, np.ones(filter_size)/filter_size, mode='same')
        return filtered_signal

def play_synth(oscillator, envelope, fltr, duration):
    wave = oscillator.generate_wave(duration)
    env = envelope.generate_envelope(duration)
    signal = wave * env
    filtered_signal = fltr.apply_filter(signal)
    sd.play(filtered_signal, samplerate=oscillator.sample_rate)
    sd.wait()

if __name__ == "__main__":
    osc = Oscillator(wave_type='sine', frequency=440)
    env = EnvelopeGenerator(attack=0.1, decay=0.1, sustain=0.8, release=0.2)
    fltr = Filter(cutoff=1000)

    print("Playing synthesizer...")
    play_synth(osc, env, fltr, duration=2.0)
    print("Finished playing!")
