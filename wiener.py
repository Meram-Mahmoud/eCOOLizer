import numpy as np
from scipy import signal

class Wiener:
    def __init__(self):
        self.signal = None
        self.noise = None
        self.filtered_signal = None
        self.signal_fft = None
        self.noise_fft = None
        self.sr = None
        self.time_axis = None
        self.noise_reduction_factor = 1.0
        self.original_length = None

    def set_signal(self, data, noise, sr):
        """
        Set the signal and noise data for processing
        data: time domain signal
        noise: noise sample (shorter than signal)
        sr: sampling rate
        """
        self.signal = data
        self.sr = sr
        self.original_length = len(data)
        # Ensure signal length is even for FFT
        if len(data) % 2 != 0:
            self.signal = np.pad(data, (0, 1), mode='constant')
        
        self.time_axis = np.linspace(0, len(self.signal) / sr, len(self.signal))
        self.detect_noise(noise)

    def detect_noise(self, noise):
        """
        Process the noise sample and prepare for filtering
        """
        # Get the noise profile by extending the noise sample
        noise_length = len(noise)
        repeats = (self.original_length // noise_length) + 1
        self.noise = np.tile(noise, repeats)[:self.original_length]
        
        # Compute FFTs
        self.signal_fft = np.fft.rfft(self.signal)
        self.noise_fft = np.fft.rfft(self.noise)
        self.frequencies = np.fft.rfftfreq(len(self.signal), 1/self.sr)
        
        # Apply initial filter
        self.apply_wiener_filter()

    def apply_wiener_filter(self):
        """
        Apply the Wiener filter with adjustable noise reduction
        """
        # Calculate power spectral densities
        signal_psd = np.abs(self.signal_fft) ** 2
        noise_psd = np.abs(self.noise_fft) ** 2 * self.noise_reduction_factor
        
        # Wiener filter formula
        H = signal_psd / (signal_psd + noise_psd + 1e-10)
        
        # Apply filter
        self.filtered_fft = self.signal_fft * H
        
        # Inverse FFT and ensure original length
        filtered_full = np.fft.irfft(self.filtered_fft)
        self.filtered_signal = filtered_full[:self.original_length]

    def set_noise_reduction(self, factor):
        """
        Adjust noise reduction strength and reapply filter
        factor: noise reduction strength (0 to 2, where 1 is default)
        """
        self.noise_reduction_factor = np.clip(factor, 0, 2)
        self.apply_wiener_filter()
        
        # Return the frequency domain signal for compatibility with the main app
        freq_response = np.fft.rfft(self.filtered_signal)
        freqs = np.fft.rfftfreq(len(self.filtered_signal), 1/self.sr)
        
        return [freqs, np.abs(freq_response)]

    def get_filtered_signal(self):
        """
        Return the filtered signal in frequency domain format
        """
        freq_response = np.fft.rfft(self.filtered_signal)
        freqs = np.fft.rfftfreq(len(self.filtered_signal), 1/self.sr)
        return [freqs, np.abs(freq_response)]