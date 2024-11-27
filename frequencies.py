import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

# Load the audio file
filename = 'eCOOLizer/sounds/animals/dogs.wav'  # Replace with your audio file
sample_rate, audio_data = wav.read(filename)

# If stereo, convert to mono by averaging channels
if len(audio_data.shape) == 2:
    audio_data = np.mean(audio_data, axis=1)

# Perform Fourier Transform
n = len(audio_data)  # Length of the audio data
frequencies = np.fft.rfftfreq(n, d=1/sample_rate)  # Frequency bins
fft_magnitude = np.abs(np.fft.rfft(audio_data))  # Magnitude of FFT

# Plot the frequency spectrum
plt.figure(figsize=(10, 6))
plt.plot(frequencies, fft_magnitude)
plt.title("Frequency Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.xlim(0, 4750)
plt.grid()
plt.show()
