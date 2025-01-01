import sys
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QComboBox, QGridLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QColor, QPalette

# Define the MonoSynth class
class MonoSynth:
    def __init__(self):
        self.sample_rate = 44100
        self.frequency = 440.0  # Default pitch (A4)
        self.amplitude = 0.5
        self.waveform = 'sine'  # Default waveform
        self.duration = 1.0  # Duration of the note in seconds
        self.envelope_attack = 0.1
        self.envelope_decay = 0.1
        self.envelope_sustain = 0.7
        self.envelope_release = 0.2
        self.current_time = 0.0

    def generate_waveform(self):
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), endpoint=False)
        if self.waveform == 'sine':
            waveform = np.sin(2 * np.pi * self.frequency * t)
        elif self.waveform == 'square':
            waveform = np.sign(np.sin(2 * np.pi * self.frequency * t))
        elif self.waveform == 'saw':
            waveform = 2 * (t * self.frequency - np.floor(t * self.frequency + 0.5))
        else:
            waveform = np.zeros_like(t)
        return waveform

    def apply_envelope(self, waveform):
        attack_samples = int(self.envelope_attack * self.sample_rate)
        decay_samples = int(self.envelope_decay * self.sample_rate)
        sustain_samples = int((self.duration - self.envelope_attack - self.envelope_decay - self.envelope_release) * self.sample_rate)

        envelope = np.zeros_like(waveform)
        
        # Attack phase
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        audio
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
    
    # Decay phase
    envelope[attack_samples:attack_samples+decay_samples] = np.linspace(1, self.envelope_sustain, decay_samples)

    # Sustain phase
    envelope[attack_samples+decay_samples:attack_samples+decay_samples+sustain_samples] = self.envelope_sustain

    # Release phase
    envelope[-int(self.envelope_release * self.sample_rate):] = np.linspace(self.envelope_sustain, 0, int(self.envelope_release * self.sample_rate))
    main

    return waveform * envelope

    def play_sound(self, callback=None):
        waveform = self.generate_waveform()
        waveform_with_envelope = self.apply_envelope(waveform)
        if callback:
            callback(waveform_with_envelope)
        sd.play(waveform_with_envelope * self.amplitude, self.sample_rate)

    def play_note_by_frequency(self, frequency, callback=None):
        self.frequency = frequency
        self.play_sound(callback)

# PyQt5 GUI
class SynthGUI(QWidget):
    def __init__(self, synth):
        super().__init__()
        self.synth = synth
        self.setWindowTitle("Mono Synthesizer with Oscilloscope")
        self.setGeometry(200, 200, 800, 600)

        # Set dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: white;
                font-family: 'Helvetica Neue', sans-serif;
            }
            QLabel {
                font-size: 16px;
                margin-bottom: 8px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #555;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                width: 20px;
                background: #4CAF50;
                border-radius: 10px;
            }
            QComboBox {
                background-color: #555;
                color: white;
                border-radius: 5px;
            }
            QComboBox::drop-down {
                background-color: #555;
                border-radius: 5px;
            }
        """)

        # Layout
        self.layout = QVBoxLayout()

        # Frequency Control
        self.frequency_label = QLabel("Frequency")
        self.layout.addWidget(self.frequency_label)
        self.frequency_slider = QSlider(Qt.Horizontal)
        self.frequency_slider.setRange(20, 2000)
        self.frequency_slider.setValue(int(self.synth.frequency))
        self.frequency_slider.valueChanged.connect(self.update_frequency)
        self.layout.addWidget(self.frequency_slider)

        # Waveform Control
        self.waveform_label = QLabel("Waveform")
        self.layout.addWidget(self.waveform_label)
        self.waveform_combo = QComboBox()
        self.waveform_combo.addItems(['sine', 'square', 'saw'])
        self.waveform_combo.setCurrentText(self.synth.waveform)
        self.waveform_combo.currentTextChanged.connect(self.update_waveform)
        self.layout.addWidget(self.waveform_combo)

        # Amplitude Control
        self.amplitude_label = QLabel("Amplitude")
        self.layout.addWidget(self.amplitude_label)
        self.amplitude_slider = QSlider(Qt.Horizontal)
        self.amplitude_slider.setRange(0, 100)
        self.amplitude_slider.setValue(int(self.synth.amplitude * 100))
        self.amplitude_slider.valueChanged.connect(self.update_amplitude)
        self.layout.addWidget(self.amplitude_slider)

        # Play Button
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_sound)
        self.layout.addWidget(self.play_button)

        # Virtual Keyboard
        self.keyboard_layout = QGridLayout()
        self.create_keyboard()
        self.layout.addLayout(self.keyboard_layout)

        # Oscilloscope (matplotlib plot)
        self.canvas = FigureCanvas(plt.figure())
        self.layout.addWidget(self.canvas)

        # Set layout
        self.setLayout(self.layout)

    def update_frequency(self):
        self.synth.frequency = self.frequency_slider.value()

    def update_waveform(self):
        self.synth.waveform = self.waveform_combo.currentText()

    def update_amplitude(self):
        self.synth.amplitude = self.amplitude_slider.value() / 100.0

    def play_sound(self):
        self.synth.play_sound(callback=self.update_oscilloscope)

    def play_note_on_button(self, note):
        frequencies = {
            'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
            'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
            'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
        }
        frequency = frequencies[note]
        self.synth.play_note_by_frequency(frequency, callback=self.update_oscilloscope)

    def create_keyboard(self):
        notes = [
            ('C', 0, 0), ('C#', 1, 0), ('D', 2, 0), ('D#', 3, 0),
            ('E', 4, 0), ('F', 5, 0), ('F#', 6, 0), ('G', 7, 0),
            ('G#', 8, 0), ('A', 9, 0), ('A#', 10, 0), ('B', 11, 0)
        ]
        
        for note, x, y in notes:
            button = QPushButton(note)
            button.setStyleSheet("""
                background-color: white;
                color: black;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                font-size: 14px;
                height: 80px;
                width: 60px;
            """)
            button.clicked.connect(lambda _, note=note: self.play_note_on_button(note))
            self.keyboard_layout.addWidget(button, y, x)

    def update_oscilloscope(self, waveform):
        # Update the oscilloscope with the waveform data
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()  # Clear the previous plot
        ax.plot(waveform)
        ax.set_title("Oscilloscope", color='white')
        ax.set_xlabel("Time (samples)", color='white')
        ax.set_ylabel("Amplitude", color='white')
        ax.tick_params(axis='both', colors='white')  # Set axis labels and ticks to white
        self.canvas.draw()

# Main function to run the app
def main():
    app = QApplication(sys.argv)
    synth = MonoSynth()
    gui = SynthGUI(synth)
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
