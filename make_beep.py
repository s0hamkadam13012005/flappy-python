import numpy as np
import wave
import struct

# Settings
file = "beep.wav"
duration = 0.2     # seconds
freq = 440.0       # Hz (A4 note)
sample_rate = 44100

# Generate samples
t = np.linspace(0, duration, int(sample_rate * duration), False)
waveform = 0.5 * np.sin(2 * np.pi * freq * t)

# Save as WAV
with wave.open(file, "w") as wav_file:
    n_channels = 1
    sampwidth = 2
    n_frames = len(waveform)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((n_channels, sampwidth, sample_rate, n_frames, comptype, compname))

    for s in waveform:
        wav_file.writeframes(struct.pack("h", int(s * 32767)))

print("beep.wav created!")
