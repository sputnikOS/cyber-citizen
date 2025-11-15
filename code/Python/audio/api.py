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
        self.root.title("API 512c Preamp Emulator")

        # API 512c style colors
        self.bg_color = "#1a2326"         # API blue/grey
        self.fg_color = "#e6e6e6"         # Light text
        self.knob_color = "#00bfff"       # API blue
        self.accent_color = "#ffcc00"     # Yellow for accents
        self.button_color = "#222b2f"     # Dark button
        self.button_fg = "#e6e6e6"
        self.led_on = "#00ff00"
        self.led_off = "#222b2f"

        self.root.configure(bg=self.bg_color)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Arial", 11, "bold"))
        style.configure("TButton", background=self.button_color, foreground=self.button_fg, font=("Arial", 10, "bold"))
        style.map("TButton",
                  background=[('active', self.knob_color)],
                  foreground=[('active', self.bg_color)])
        style.configure("Horizontal.TScale", background=self.bg_color, troughcolor=self.button_color, sliderthickness=20)
        style.configure("TProgressbar", background=self.knob_color, troughcolor=self.bg_color, bordercolor=self.bg_color, lightcolor=self.knob_color, darkcolor=self.button_color)

        self.x = None
        self.fs = 44100

        # API logo style title
        title = ttk.Label(root, text="API 512c", font=("Arial Black", 22, "bold"), foreground=self.knob_color, background=self.bg_color)
        title.pack(pady=(12, 2))
        sub = ttk.Label(root, text="MIC PREAMPLIFIER", font=("Arial", 12, "bold"), foreground=self.accent_color, background=self.bg_color)
        sub.pack(pady=(0, 10))

        # LED "power" indicator
        self.led = tk.Canvas(root, width=18, height=18, bg=self.bg_color, highlightthickness=0)
        self.led.pack()
        self.led_id = self.led.create_oval(2, 2, 16, 16, fill=self.led_on, outline=self.led_off, width=2)

        # Controls
        self.controls = {
            'Input Gain': (tk.DoubleVar(value=1.0), 0.1, 3.0, "INPUT"),
            'Drive': (tk.DoubleVar(value=1.5), 0.1, 5.0, "DRIVE"),
            'Low Gain (dB)': (tk.DoubleVar(value=2.0), -12, 12, "LOW EQ"),
            'High Gain (dB)': (tk.DoubleVar(value=3.0), -12, 12, "HIGH EQ"),
            'Output Gain': (tk.DoubleVar(value=0.8), 0.1, 2.0, "OUTPUT"),
        }

        for label, (var, frm, to, knob_label) in self.controls.items():
            frame = ttk.Frame(root)
            frame.pack(fill='x', pady=7, padx=18)
            # Knob label above
            ttk.Label(frame, text=knob_label, width=10, anchor='center', font=("Arial", 10, "bold"), foreground=self.knob_color).pack(side='top', anchor='w')
            # Knob (slider)
            scale = ttk.Scale(frame, variable=var, from_=frm, to=to, orient='horizontal', length=220)
            scale.pack(side='left', padx=6)
            val_label = ttk.Label(frame, text=f"{var.get():.2f}", width=6, foreground=self.accent_color, background=self.bg_color, font=("Arial", 10, "bold"))
            val_label.pack(side='left', padx=6)

            def update_label(v, label=val_label, var=var):
                label.config(text=f"{float(v):.2f}")
            scale.config(command=update_label)

        # Buttons
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=14)
        ttk.Button(btn_frame, text="Load WAV", command=self.load_wav).pack(side='left', padx=8)
        ttk.Button(btn_frame, text="Process & Save", command=self.process_wav).pack(side='left', padx=8)
        ttk.Button(btn_frame, text="Play Input", command=self.play_input).pack(side='left', padx=8)
        ttk.Button(btn_frame, text="Play Output", command=self.play_output).pack(side='left', padx=8)

        # Waveform display
        self.fig, self.ax = plt.subplots(figsize=(5, 2))
        self.fig.patch.set_facecolor(self.bg_color)
        self.ax.set_facecolor(self.bg_color)
        self.ax.tick_params(colors=self.fg_color, which='both')
        self.ax.spines['bottom'].set_color(self.fg_color)
        self.ax.spines['top'].set_color(self.fg_color)
        self.ax.spines['right'].set_color(self.fg_color)
        self.ax.spines['left'].set_color(self.fg_color)
        self.ax.title.set_color(self.knob_color)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(pady=10)

        # VU meter
        vu_frame = ttk.Frame(root)
        vu_frame.pack(pady=(0, 12))
        ttk.Label(vu_frame, text="VU", font=("Arial", 10, "bold"), foreground=self.accent_color, background=self.bg_color).pack(side='left', padx=(0, 8))
        self.vu = ttk.Progressbar(vu_frame, orient='horizontal', length=220, mode='determinate', maximum=1.0, style="TProgressbar")
        self.vu.pack(side='left')

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
        params = {key: var.get() for key, (var, _, _, _) in self.controls.items()}
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
        self.ax.plot(data, color=self.knob_color)
        self.ax.set_title("Waveform", color=self.knob_color)
        self.ax.set_xlim(0, len(data))
        self.ax.set_yticks([])
        self.ax.set_xticks([])
        self.fig.tight_layout()
        self.canvas.draw()

    def play_input(self):
        if self.x is not None:
            sd.stop()
            sd.play(self.x, self.fs)
            self.update_vu(self.x)

    def play_output(self):
        if self.x is not None:
            params = {key: var.get() for key, (var, _, _, _) in self.controls.items()}
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
            self.update_vu(y)

    def update_vu(self, data):
        rms = np.sqrt(np.mean(data**2))
        self.vu['value'] = min(rms, 1.0)
        self.root.update_idletasks()

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PreampGUI(root)
    root.configure(bg="#1a2326")
    root.mainloop()