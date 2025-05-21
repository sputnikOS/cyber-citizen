import tkinter as tk
from tkinter import filedialog, ttk
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sounddevice as sd


# --- DSP Functions ---

def soft_clip(x, drive=1.0):
    return np.tanh(drive * x)

def high_shelf(x, gain_db, cutoff=8000, fs=44100):
    A = 10**(gain_db / 40)
    w0 = 2 * np.pi * cutoff / fs
    alpha = np.sin(w0) / 2 * np.sqrt((A + 1/A)*(1/0.707 - 1) + 2)
    cos_w0 = np.cos(w0)
    b0 = A*((A+1)+(A-1)*cos_w0+2*np.sqrt(A)*alpha)
    b1 = -2*A*((A-1)+(A+1)*cos_w0)
    b2 = A*((A+1)+(A-1)*cos_w0-2*np.sqrt(A)*alpha)
    a0 = ((A+1)-(A-1)*cos_w0+2*np.sqrt(A)*alpha)
    a1 = 2*((A-1)-(A+1)*cos_w0)
    a2 = ((A+1)-(A-1)*cos_w0-2*np.sqrt(A)*alpha)
    b = [b0/a0, b1/a0, b2/a0]
    a = [1.0, a1/a0, a2/a0]
    return lfilter(b, a, x)

def low_shelf(x, gain_db, cutoff=100, fs=44100):
    A = 10**(gain_db / 40)
    w0 = 2 * np.pi * cutoff / fs
    alpha = np.sin(w0) / 2 * np.sqrt((A + 1/A)*(1/0.707 - 1) + 2)
    cos_w0 = np.cos(w0)
    b0 = A*((A+1)-(A-1)*cos_w0+2*np.sqrt(A)*alpha)
    b1 = 2*A*((A-1)-(A+1)*cos_w0)
    b2 = A*((A+1)-(A-1)*cos_w0-2*np.sqrt(A)*alpha)
    a0 = (A+1)+(A-1)*cos_w0+2*np.sqrt(A)*alpha
    a1 = -2*((A-1)+(A+1)*cos_w0)
    a2 = (A+1)+(A-1)*cos_w0-2*np.sqrt(A)*alpha
    b = [b0/a0, b1/a0, b2/a0]
    a = [1.0, a1/a0, a2/a0]
    return lfilter(b, a, x)

def transformer_resonance(x, freq=100, boost_db=1.5, fs=44100):
    b, a = butter(2, [freq-30, freq+30], btype='band', fs=fs)
    resonant = lfilter(b, a, x)
    return x + resonant * (10**(boost_db / 20) - 1)

def process_api_preamp(x, fs, input_gain, drive, low_gain, high_gain, output_gain):
    x = x * input_gain
    x = transformer_resonance(x, freq=100, boost_db=1.5, fs=fs)
    x = soft_clip(x, drive)
    x = low_shelf(x, gain_db=low_gain, fs=fs)
    x = high_shelf(x, gain_db=high_gain, fs=fs)
    x = x * output_gain
    return np.clip(x, -1.0, 1.0)

# --- GUI App ---

class PreampGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("API Preamp Emulator")

        self.x = None
        self.fs = 44100

        self.controls = {
            'Input Gain': (tk.DoubleVar(value=1.0), 0.1, 3.0),
            'Drive': (tk.DoubleVar(value=1.5), 0.1, 5.0),
            'Low Gain (dB)': (tk.DoubleVar(value=2.0), -12, 12),
            'High Gain (dB)': (tk.DoubleVar(value=3.0), -12, 12),
            'Output Gain': (tk.DoubleVar(value=0.8), 0.1, 2.0),
        }

        for label, (var, frm, to) in self.controls.items():
            frame = ttk.Frame(root)
            frame.pack(fill='x', pady=3)
            ttk.Label(frame, text=label, width=20).pack(side='left')
            scale = ttk.Scale(frame, variable=var, from_=frm, to=to, orient='horizontal', length=200)
            scale.pack(side='left')
            val_label = ttk.Label(frame, text=f"{var.get():.2f}")
            val_label.pack(side='left')

            def update_label(v, label=val_label, var=var):
                label.config(text=f"{float(v):.2f}")
            scale.config(command=update_label)

        ttk.Button(root, text="Load WAV", command=self.load_wav).pack(pady=5)
        ttk.Button(root, text="Process & Save", command=self.process_wav).pack(pady=5)
        ttk.Button(root, text="Play Input", command=self.play_input).pack(pady=2)
        ttk.Button(root, text="Play Output", command=self.play_output).pack(pady=2)


        self.fig, self.ax = plt.subplots(figsize=(5, 2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

    def load_wav(self):
        path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if path:
            x, self.fs = sf.read(path)
            if len(x.shape) > 1:
                x = x.mean(axis=1)
            self.x = x
            self.plot_waveform(x)

    def process_wav(self):
        if self.x is None:
            return
        params = {key: var.get() for key, (var, _, _) in self.controls.items()}
        y = process_api_preamp(
            self.x, self.fs,
            input_gain=params['Input Gain'],
            drive=params['Drive'],
            low_gain=params['Low Gain (dB)'],
            high_gain=params['High Gain (dB)'],
            output_gain=params['Output Gain']
        )
        out_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if out_path:
            sf.write(out_path, y, self.fs)
            self.plot_waveform(y)

    def plot_waveform(self, data):
        self.ax.clear()
        self.ax.plot(data, color='orange')
        self.ax.set_title("Waveform")
        self.ax.set_xlim(0, len(data))
        self.fig.tight_layout()
        self.canvas.draw()

    def play_input(self):
        if self.x is not None:
            sd.stop()
            sd.play(self.x, self.fs)

    def play_output(self):
        if self.x is not None:
            params = {key: var.get() for key, (var, _, _) in self.controls.items()}
            y = process_api_preamp(
                self.x, self.fs,
                input_gain=params['Input Gain'],
                drive=params['Drive'],
                low_gain=params['Low Gain (dB)'],
                high_gain=params['High Gain (dB)'],
                output_gain=params['Output Gain']
            )
            sd.stop()
            sd.play(y, self.fs)

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PreampGUI(root)
    root.mainloop()
