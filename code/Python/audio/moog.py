import numpy as np
import sounddevice as sd
from scipy.signal import butter, lfilter
import tkinter as tk
from tkinter import ttk

SAMPLE_RATE = 44100

def osc_waveform(freq, length, wave='saw', detune=0.0):
    t = np.linspace(0, length, int(SAMPLE_RATE * length), endpoint=False)
    f = freq * (2 ** detune)
    if wave == 'saw':
        return 2 * (t * f % 1) - 1
    elif wave == 'square':
        return np.sign(np.sin(2 * np.pi * f * t))
    elif wave == 'tri':
        return 2 * np.abs(2 * (f * t % 1) - 1) - 1
    else:
        return np.sin(2 * np.pi * f * t)

def moog_filter(x, cutoff, resonance):
    f = cutoff / SAMPLE_RATE
    q = resonance
    b = [0.0] * 4
    y = np.zeros_like(x)
    for i in range(len(x)):
        x0 = x[i] - q * b[3]
        b[0] += f * (np.tanh(x0) - np.tanh(b[0]))
        for j in range(1, 4):
            b[j] += f * (np.tanh(b[j - 1]) - np.tanh(b[j]))
        y[i] = b[3]
    return y

def adsr(length, attack, decay, sustain, release):
    total = int(SAMPLE_RATE * length)
    env = np.zeros(total)
    a = int(SAMPLE_RATE * attack)
    d = int(SAMPLE_RATE * decay)
    r = int(SAMPLE_RATE * release)
    s = total - (a + d + r)
    s = max(s, 0)
    env[:a] = np.linspace(0, 1, a)
    env[a:a+d] = np.linspace(1, sustain, d)
    env[a+d:a+d+s] = sustain
    env[-r:] = np.linspace(sustain, 0, r)
    return env

def moog_voice(freq, length, waveform, detune, cutoff, res, a, d, s, r):
    osc1 = osc_waveform(freq, length, waveform, 0.0)
    osc2 = osc_waveform(freq, length, waveform, detune)
    osc3 = osc_waveform(freq, length, waveform, -detune)
    mix = (osc1 + osc2 + osc3) / 3.0
    env = adsr(length, a, d, s, r)
    filtered = moog_filter(mix * env, cutoff, res)
    return filtered * 0.4

def play_note(freq, waveform, detune, cutoff, res, a, d, s, r):
    voice = moog_voice(freq, 1.5, waveform, detune, cutoff, res, a, d, s, r)
    sd.play(voice, samplerate=SAMPLE_RATE)

# GUI Setup
root = tk.Tk()
root.title("Moog MonoSynth")

note_freqs = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63,
    'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88, 'C5': 523.25
}

note_var = tk.StringVar(value='C4')
wave_var = tk.StringVar(value='saw')
detune_var = tk.DoubleVar(value=0.02)
cutoff_var = tk.DoubleVar(value=1200)
res_var = tk.DoubleVar(value=0.7)
a_var = tk.DoubleVar(value=0.01)
d_var = tk.DoubleVar(value=0.15)
s_var = tk.DoubleVar(value=0.6)
r_var = tk.DoubleVar(value=0.2)

def trigger_note():
    freq = note_freqs[note_var.get()]
    play_note(freq, wave_var.get(), detune_var.get(), cutoff_var.get(),
              res_var.get(), a_var.get(), d_var.get(), s_var.get(), r_var.get())

# Layout
ttk.Label(root, text="Note").grid(row=0, column=0)
ttk.OptionMenu(root, note_var, 'C4', *note_freqs.keys()).grid(row=0, column=1)

ttk.Label(root, text="Waveform").grid(row=1, column=0)
ttk.OptionMenu(root, wave_var, 'saw', 'saw', 'square', 'tri').grid(row=1, column=1)

ttk.Label(root, text="Detune").grid(row=2, column=0)
ttk.Scale(root, from_=0.0, to=0.1, variable=detune_var, orient='horizontal').grid(row=2, column=1)

ttk.Label(root, text="Cutoff Hz").grid(row=3, column=0)
ttk.Scale(root, from_=200, to=5000, variable=cutoff_var, orient='horizontal').grid(row=3, column=1)

ttk.Label(root, text="Resonance").grid(row=4, column=0)
ttk.Scale(root, from_=0.0, to=1.5, variable=res_var, orient='horizontal').grid(row=4, column=1)

ttk.Label(root, text="Attack").grid(row=5, column=0)
ttk.Scale(root, from_=0.001, to=1.0, variable=a_var, orient='horizontal').grid(row=5, column=1)

ttk.Label(root, text="Decay").grid(row=6, column=0)
ttk.Scale(root, from_=0.001, to=1.0, variable=d_var, orient='horizontal').grid(row=6, column=1)

ttk.Label(root, text="Sustain").grid(row=7, column=0)
ttk.Scale(root, from_=0.0, to=1.0, variable=s_var, orient='horizontal').grid(row=7, column=1)

ttk.Label(root, text="Release").grid(row=8, column=0)
ttk.Scale(root, from_=0.001, to=1.0, variable=r_var, orient='horizontal').grid(row=8, column=1)

ttk.Button(root, text="Play Note", command=trigger_note).grid(row=9, columnspan=2, pady=10)

root.mainloop()
