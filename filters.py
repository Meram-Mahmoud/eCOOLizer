import numpy as np
import matplotlib.pyplot as plt

# low pass filter
def moving_average_filter(signal, window_size=20):
    filtered_signal = np.zeros_like(signal)
    for i in range(len(signal)):
        # Handle edges by averaging available points within the window range
        start = max(0, i - window_size // 2)
        end = min(len(signal), i + window_size // 2 + 1)
        filtered_signal[i] = np.mean(signal[start:end])
    return filtered_signal

# high pass filter
def high_pass_filter(signal, alpha=0.9):
    filtered_signal = np.zeros_like(signal)
    for i in range(1, len(signal)):
        filtered_signal[i] = alpha * (filtered_signal[i - 1] + signal[i] - signal[i - 1])
    return filtered_signal

# filtering signal in time domain 
def filter(signal, filter_type):
    if filter_type == 'low pass':
        filtered_signal = moving_average_filter(signal)
    elif filter_type == 'high pass':
        filtered_signal = high_pass_filter(signal)
    return filtered_signal


# Generate a noisy signal
fs = 500  # Sampling frequency
t = np.linspace(0, 1, fs, endpoint=False)
signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 50 * t)  # Signal with noise

filtered_signal = filter(signal, "low pass")

# Plot original and filtered signals
plt.figure(figsize=(10, 6))
plt.subplot(2,1,1)
plt.plot(t, signal, label="Original Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.legend()
plt.title("Signal Before Moving Average Filtering")

plt.subplot(2,1,2)
plt.plot(t, filtered_signal, label="Filtered Signal (Moving Average)", color='red')
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.legend()
plt.title("Signal After Moving Average Filtering")

plt.tight_layout()
plt.show()