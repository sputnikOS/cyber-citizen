import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt

# DSP Functions (same as previous example)
def soft_clip(x, drive=1.0):
    return np.tanh(drive * x)

def highpass_filter(x, cutoff=80, fs=44100, order=2):
    b, a = butter(order, cutoff / (0.5 * fs), btype='high')
    return lfilter(b, a, x)

def low_shelf(x, gain_db=4.5, freq=220, fs=44100):
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * freq / fs
    alpha = np.sin(w0) / 2 * np.sqrt((A + 1/A) * (1/0.707 - 1) + 2)
    cos_w0 = np.cos(w0)

    b0 = A * ((A + 1) - (A - 1) * cos_w0 + 2 * np.sqrt(A) * alpha)
    b1 = 2 * A * ((A - 1) - (A + 1) * cos_w0)
    b2 = A * ((A + 1) - (A - 1) * cos_w0 - 2 * np.sqrt(A) * alpha)
    a0 = ((A + 1) + (A - 1) * cos_w0 + 2 * np.sqrt(A) * alpha)
    a1 = -2 * ((A - 1) + (A + 1) * cos_w0)
    a2 = ((A + 1) + (A - 1) * cos_w0 - 2 * np.sqrt(A) * alpha)

    b = [b0 / a0, b1 / a0, b2 / a0]
    a = [1.0, a1 / a0, a2 / a0]

    return lfilter(b, a, x)

def process_signal(x, fs, drive, hp_freq, shelf_gain, output_gain):
    x = highpass_filter(x, cutoff=hp_freq, fs=fs)
    x = soft_clip(x, drive=drive)
    x = low_shelf(x, gain_db=shelf_gain, freq=220, fs=fs)
    x = x * output_gain
    return x

# GUI Class
class PreampGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Neve 1073-Style Preamp")

        # Sliders
        self.drive = self.add_slider("Drive", 0.5, 5.0, 2.5)
        self.hp_freq = self.add_slider("HPF Frequency (Hz)", 20, 200, 80)
        self.shelf_gain = self.add_slider("Low Shelf Gain (dB)", -12, 12, 4.5)
        self.output_gain = self.add_slider("Output Gain", 0.1, 2.0, 0.9)

        # Buttons
        ttk.Button(root, text="Load WAV", command=self.load_wav).pack(pady=5)
        ttk.Button(root, text="Process & Save", command=self.process_wav).pack(pady=5)

        # Display area for waveform
        self.fig, self.ax = plt.subplots(figsize=(5, 2))
        self.canvas = None

        self.x = None
        self.fs = 44100

    def add_slider(self, label, from_, to, initial):
        ttk.Label(self.root, text=label).pack()
        var = tk.DoubleVar(value=initial)
        slider = ttk.Scale(self.root, variable=var, from_=from_, to=to, orient='horizontal')
        slider.pack()
        return var

    def load_wav(self):
        path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if path:
            x, self.fs = sf.read(path)
            if len(x.shape) > 1:
                x = x.mean(axis=1)
            self.x = x
            self.plot_waveform(x)

    def plot_waveform(self, data):
        self.ax.clear()
        self.ax.plot(data, color='steelblue')
        self.ax.set_title("Waveform")
        self.ax.set_xlim(0, len(data))
        self.fig.tight_layout()
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def process_wav(self):
        if self.x is None:
            return
        y = process_signal(
            self.x, self.fs,
            drive=self.drive.get(),
            hp_freq=self.hp_freq.get(),
            shelf_gain=self.shelf_gain.get(),
            output_gain=self.output_gain.get()
        )
        out_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV", "*.wav")])
        if out_path:
            sf.write(out_path, y, self.fs)
            self.plot_waveform(y)

# Main App
root = tk.Tk()
app = PreampGUI(root)
root.mainloop()
