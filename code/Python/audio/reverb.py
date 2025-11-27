import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import soundfile as sf
import scipy.signal as signal
import sounddevice as sd
import threading
import os

class ReverbApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convolution Reverb with Preview")
        self.audio_path = ""
        self.ir_path = ""

        # GUI Elements
        tk.Label(root, text="Dry Audio File:").grid(row=0, column=0, sticky="e")
        self.audio_entry = tk.Entry(root, width=50)
        self.audio_entry.grid(row=0, column=1)
        tk.Button(root, text="Browse", command=self.load_audio).grid(row=0, column=2)

        tk.Label(root, text="Impulse Response (IR):").grid(row=1, column=0, sticky="e")
        self.ir_entry = tk.Entry(root, width=50)
        self.ir_entry.grid(row=1, column=1)
        tk.Button(root, text="Browse", command=self.load_ir).grid(row=1, column=2)

        tk.Label(root, text="Wet/Dry Mix (0-1):").grid(row=2, column=0, sticky="e")
        self.mix_var = tk.DoubleVar(value=0.5)
        tk.Scale(root, variable=self.mix_var, from_=0, to=1, resolution=0.01,
                 orient="horizontal", length=200).grid(row=2, column=1)

        btn_frame = tk.Frame(root)
        btn_frame.grid(row=3, column=1, pady=10)

        tk.Button(btn_frame, text="Play Dry", command=self.play_dry).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Preview Reverb", command=self.preview_reverb).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Apply & Save", command=self.apply_reverb).grid(row=0, column=2, padx=5)

    def load_audio(self):
        path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if path:
            self.audio_path = path
            self.audio_entry.delete(0, tk.END)
            self.audio_entry.insert(0, path)

    def load_ir(self):
        path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if path:
            self.ir_path = path
            self.ir_entry.delete(0, tk.END)
            self.ir_entry.insert(0, path)

    def play_dry(self):
        if not self.audio_path:
            messagebox.showerror("Error", "Please select an audio file.")
            return
        threading.Thread(target=self._play_audio, args=(self.audio_path,)).start()

    def _play_audio(self, path):
        audio, sr = sf.read(path)
        sd.play(audio, sr)
        sd.wait()

    def preview_reverb(self):
        if not self.audio_path or not self.ir_path:
            messagebox.showerror("Error", "Select both audio and IR.")
            return
        threading.Thread(target=self._preview_and_play).start()

    def _preview_and_play(self):
        try:
            audio, sr = sf.read(self.audio_path)
            ir, ir_sr = sf.read(self.ir_path)

            if sr != ir_sr:
                messagebox.showerror("Error", "Sample rates do not match.")
                return

            wet_dry = self.mix_var.get()

            if audio.ndim > 1:
                left = signal.fftconvolve(audio[:, 0], ir[:, 0], mode='full')
                right = signal.fftconvolve(audio[:, 1], ir[:, 1], mode='full')
                wet = np.column_stack((left, right))
            else:
                wet = signal.fftconvolve(audio, ir, mode='full')

            wet = wet[:len(audio)]
            wet /= np.max(np.abs(wet))
            mixed = (1 - wet_dry) * audio + wet_dry * wet

            sd.play(mixed, sr)
            sd.wait()

        except Exception as e:
            messagebox.showerror("Preview Error", str(e))

    def apply_reverb(self):
        if not self.audio_path or not self.ir_path:
            messagebox.showerror("Error", "Select both audio and IR.")
            return
        try:
            audio, sr = sf.read(self.audio_path)
            ir, ir_sr = sf.read(self.ir_path)

            if sr != ir_sr:
                messagebox.showerror("Error", "Sample rates do not match.")
                return

            wet_dry = self.mix_var.get()

            if audio.ndim > 1:
                left = signal.fftconvolve(audio[:, 0], ir[:, 0], mode='full')
                right = signal.fftconvolve(audio[:, 1], ir[:, 1], mode='full')
                wet = np.column_stack((left, right))
            else:
                wet = signal.fftconvolve(audio, ir, mode='full')

            wet = wet[:len(audio)]
            wet /= np.max(np.abs(wet))
            mixed = (1 - wet_dry) * audio + wet_dry * wet

            output_path = os.path.splitext(self.audio_path)[0] + "_reverb.wav"
            sf.write(output_path, mixed, sr)
            messagebox.showinfo("Success", f"Reverb applied and saved to:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Processing Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ReverbApp(root)
    root.mainloop()
