import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from signal_data import Signal


# get signal frequencies
def fourier(signal):
    # Compute the Fourier Transform
    fft_values = np.fft.fft(signal)
    fft_freqs = np.fft.fftfreq(len(fft_values), 1/6000)

    # Only keep the positive half of the frequencies for display
    positive_freqs = fft_freqs[:len(fft_freqs) // 2]
    positive_fft_values = np.abs(fft_values[:len(fft_values) // 2])
    
    # print(len(fft_values), len(time))
    
    return positive_freqs, positive_fft_values
    # return fft_freqs, fft_values


# def load_audio(audio_file):
#     # Load audio file using pydub
#     audio = AudioSegment.from_wav(audio_file)
#     samples = np.array(audio.get_array_of_samples())
#     signal = [np.linspace(0, len(samples) / audio.frame_rate, num=len(samples)), samples]
#     return signal

# signal = load_audio("Equalizer/sounds/animal_extended_audio.wav")

# # Synthetic signal
# time = np.linspace(0, 10, 1000)
# amp = np.zeros_like(time)
# for i in range(10):
#     if i % 2 == 0:
#         amp += 1/(i+1)*np.sin(2 * np.pi * i * time)
#         # pass
#     else:
#         amp += 1/(i+1)*np.cos(2 * np.pi * i * time)


signal = Signal()
signal.load_signal("eCOOLizer/sounds/animals/grrrrr.wav")
time, amp = signal.get_data()

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
plt.xlim(0, 200)

plt.tight_layout()
plt.show()