import numpy as np
import sounddevice as sd
from PyQt5 import QtWidgets, QtCore
import rtmidi

# Sample rate
SAMPLE_RATE = 44100

# Synthesizer Modules
def oscillator(frequency, duration, waveform='sine'):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    if waveform == 'sine':
        return np.sin(2 * np.pi * frequency * t)
    elif waveform == 'square':
        return np.sign(np.sin(2 * np.pi * frequency * t))
    elif waveform == 'sawtooth':
        return 2 * (t * frequency - np.floor(0.5 + t * frequency))
    elif waveform == 'triangle':
        return 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
    else:
        raise ValueError("Unsupported waveform")

def envelope(signal, attack=0.1, decay=0.1, sustain=0.7, release=0.2):
    attack_samples = int(attack * SAMPLE_RATE)
    decay_samples = int(decay * SAMPLE_RATE)
    release_samples = int(release * SAMPLE_RATE)
    sustain_samples = len(signal) - (attack_samples + decay_samples + release_samples)

    if sustain_samples < 0:
        raise ValueError("Duration too short for given ADSR settings")

    attack_curve = np.linspace(0, 1, attack_samples)
    decay_curve = np.linspace(1, sustain, decay_samples)
    sustain_curve = np.full(sustain_samples, sustain)
    release_curve = np.linspace(sustain, 0, release_samples)

    envelope_curve = np.concatenate([attack_curve, decay_curve, sustain_curve, release_curve])
    return signal[:len(envelope_curve)] * envelope_curve

def low_pass_filter(signal, cutoff_freq):
    from scipy.signal import butter, lfilter
    nyquist = 0.5 * SAMPLE_RATE
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(1, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, signal)

def modular_synth(note, duration, waveform, filter_freq, adsr):
    note_frequencies = {
        "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
        "G4": 392.00, "A4": 440.00, "B4": 493.88, "C5": 523.25
    }
    frequency = note_frequencies.get(note, 440.0)
    signal = oscillator(frequency, duration, waveform)
    signal = envelope(signal, *adsr)
    signal = low_pass_filter(signal, filter_freq)
    return signal

# GUI Application
class SynthGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.midi_in = None

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Waveform Selection
        self.waveform_label = QtWidgets.QLabel("Waveform:")
        layout.addWidget(self.waveform_label)
        self.waveform_combo = QtWidgets.QComboBox()
        self.waveform_combo.addItems(["sine", "square", "sawtooth", "triangle"])
        layout.addWidget(self.waveform_combo)

        # Filter Cutoff
        self.filter_label = QtWidgets.QLabel("Filter Cutoff Frequency (Hz):")
        layout.addWidget(self.filter_label)
        self.filter_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.filter_slider.setMinimum(100)
        self.filter_slider.setMaximum(5000)
        self.filter_slider.setValue(1000)
        layout.addWidget(self.filter_slider)

        # ADSR Sliders
        self.adsr_sliders = {}
        adsr_params = ["Attack", "Decay", "Sustain", "Release"]
        for param in adsr_params:
            label = QtWidgets.QLabel(f"{param}:")
            layout.addWidget(label)
            slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            slider.setMinimum(1)
            slider.setMaximum(1000)
            slider.setValue(100 if param == "Sustain" else 100)
            layout.addWidget(slider)
            self.adsr_sliders[param] = slider

        # Play Button
        self.play_button = QtWidgets.QPushButton("Play Note")
        self.play_button.clicked.connect(self.play_note)
        layout.addWidget(self.play_button)

        self.setLayout(layout)
        self.setWindowTitle("Modular Synthesizer")
        self.resize(400, 300)

        # Initialize MIDI Input
        self.init_midi_input()

    def init_midi_input(self):
        midi_in = rtmidi.MidiIn()
        available_ports = midi_in.get_ports()
        if available_ports:
            midi_in.open_port(0)  # Open the first available port
            midi_in.set_callback(self.midi_callback)
            self.midi_in = midi_in
        else:
            print("No MIDI devices found.")

    def midi_callback(self, message, data=None):
        # MIDI message: [status, note, velocity]
        message, _ = message
        status, note, velocity = message
        if status == 144:  # Note On
            note_name = self.note_number_to_name(note)
            self.play_midi_note(note_name)

    def play_midi_note(self, note):
        waveform = self.waveform_combo.currentText()
        filter_freq = self.filter_slider.value()
        adsr = tuple(slider.value() / 1000 for slider in self.adsr_sliders.values())
        duration = 1.0  # Default duration for MIDI note
        signal = modular_synth(note, duration, waveform, filter_freq, adsr)
        sd.play(signal, samplerate=SAMPLE_RATE)
        sd.wait()

    def play_note(self):
        waveform = self.waveform_combo.currentText()
        filter_freq = self.filter_slider.value()
        adsr = tuple(slider.value() / 1000 for slider in self.adsr_sliders.values())
        note = "C4"
        duration = 1.0

        signal = modular_synth(note, duration, waveform, filter_freq, adsr)
        sd.play(signal, samplerate=SAMPLE_RATE)
        sd.wait()

    def note_number_to_name(self, number):
        """Convert MIDI note number to musical note name."""
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        octave = (number // 12) - 1
        note = note_names[number % 12]
        return f"{note}{octave}"

# Run GUI Application
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    gui = SynthGUI()
    gui.show()
    sys.exit(app.exec_())
