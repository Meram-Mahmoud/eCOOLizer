import numpy as np
import matplotlib.pyplot as plt

# get signal frequencies
def fourier(signal):
    # Compute the Fourier Transform
    fft_values = np.fft.fft(signal)
    fft_freqs = np.fft.fftfreq(len(fft_values), 1 / 100)

    # Only keep the positive half of the frequencies for display
    positive_freqs = fft_freqs[:len(fft_freqs) // 2]
    positive_fft_values = np.abs(fft_values[:len(fft_values) // 2])
    
    return positive_freqs, positive_fft_values


# Synthetic signal
time = np.linspace(0, 10, 1000)
amp = np.zeros_like(time)
for i in range(10):
    amp += i/100*np.sin(2 * np.pi * i * time)

freq, ampl = fourier(amp)

# Plot the original signal
plt.subplot(2, 1, 1)
plt.plot(time, amp)
plt.legend()
plt.title("Original Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# Plot the Fourier Transform (magnitude)
plt.subplot(2, 1, 2)
plt.plot(freq, ampl)
plt.legend()
plt.title("Fourier Transform")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
plt.xlim(0,10)

plt.tight_layout()
plt.show()