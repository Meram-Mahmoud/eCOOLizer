import numpy as np
import soundfile as sf
import pandas as pd
import sounddevice as sd
from scipy.signal import spectrogram


class Signal:
    def __init__(self, file_path="sounds/Final modes/extended_uniform.wav"):
        # Inputs: file_path (str): Path to the audio file
        self.data = None  
        self.sample_rate = 1000  # Sampling rate of the audio file
        self.file_path = file_path
        self.playing=False
        self.load_signal(file_path)
        print("signal initialized")

    def load_signal(self, file_path):
        self.data, self.sample_rate = sf.read(file_path)
        if self.data.ndim > 1: 
            self.data = self.data[:, 0]  # Take the first channel if multi-channel (represents mono audio)

        if len(self.data) == 0:
            raise ValueError("no data")
        
        num_samples = len(self.data)
        time_axis = np.linspace(0, num_samples / self.sample_rate, num=num_samples)
        
        self.data = np.column_stack((time_axis, self.data))
        # print(len(self.data[1]))

        self.fft_data()

    def load_signal_from_csv(self, file_path):
        df = pd.read_csv(file_path)
        self.time = df['Time'].values  
        self.data = df['Amplitude'].values
        self.data = np.column_stack((self.time, self.data))  
        self.fft_data()


    def get_data(self, end_frame=None):
        if self.data is None:
            raise ValueError("data not loaded.")

        if end_frame is None or end_frame > len(self.data):
            end_frame = len(self.data)
        return self.data[:end_frame, 0], self.data[:end_frame, 1]
    
    # ifft
    def get_time_domain_data(self, end_frame=None):
        # Ensure valid end_frame value
        if self.data is None:
            raise ValueError("Fourier data not available.")
        
        if not end_frame or end_frame > len(self.data):
            end_frame = len(self.data)  # Use the full length if end_frame is None or exceeds bounds

        if self.data.shape[1] < 3:
            raise ValueError("Expected at least three columns in self.data for frequency, magnitude, and phase.")
        
        frequencies = self.data[:end_frame, 0]
        magnitudes = self.data[:end_frame, 1]
        phases = self.data[:end_frame, 2]
        
        # Reconstruct the complex frequency spectrum
        complex_spectrum = magnitudes * np.exp(1j * phases)
        
        # Perform the inverse FFT
        amplitude = np.fft.irfft(complex_spectrum, n=(end_frame - 1) * 2)
        
        # Generate the time axis
        time_axis = np.linspace(0, len(amplitude) / self.sample_rate, num=len(amplitude))

        return time_axis, amplitude

    def set_data(self, new_data, end_frame = None):
        
        if not end_frame or end_frame > len(self.data):
            end_frame = len(self.data)  # Use the full length if end_frame is None or exceeds bounds

        if len(new_data[0]) != len(new_data[1]):
            raise ValueError("Time and amplitude arrays must be the same length.")
        self.data[:end_frame, 1] = new_data[1]

        # self.data[:end_frame, 1] = new_data[1]
        # print(self.data)

    def fft_data(self, end_frame=None):
            
        if self.data is None:
            raise ValueError("Signal data not loaded.")

        if end_frame is None or end_frame > len(self.data):
            end_frame = len(self.data)

        amplitude = self.data[:end_frame, 1]
        frequencies = np.fft.rfftfreq(end_frame, 1 / self.sample_rate)
        magnitudes = np.abs(np.fft.rfft(amplitude))
        phase = np.angle(np.fft.rfft(amplitude))
        
        self.data = np.column_stack((frequencies, magnitudes, phase))
        # return frequencies, magnitudes

    def get_fft_data(self, end_frame = None):
        # print(self.data.shape)
        return self.data[:end_frame, 0], self.data[:end_frame, 1]
    
    def calculate_spectrogram(self, chunks=512, overlap=256):
        if self.data is None or self.data.shape[1] < 2:
             raise ValueError("data not available.")

        time_axis, amplitude = self.get_time_domain_data()
        freqs, times, spec = spectrogram(amplitude, fs=self.sample_rate, window='hann',nperseg=chunks, noverlap=overlap, scaling='spectrum')
        return freqs, times, spec


    def calculate_audiogram(self, frequencies, magnitudes):
        valid_indices = frequencies > 0
        frequencies = frequencies[valid_indices]
        magnitudes = magnitudes[valid_indices]

        magnitudes_clipped = np.clip(magnitudes, a_min=1e-10, a_max=None)
        magnitudes_db = 20 * np.log10(magnitudes_clipped)
        log_frequencies = np.log10(frequencies)
        return log_frequencies, magnitudes_db
    
    
    

    def get_time_data(self):
        
        if self.data is None:
            raise ValueError("Signal data not loaded")
        return self.time_data, self.data
    

    def play_audio(self, start_frame=0, end_frame=None):
        if self.data is None:
            raise ValueError("Load audio data before attempting playback.")
        
        if end_frame is None:
            end_frame = len(self.data)
        
        time, amplitude = self.get_time_domain_data()
        audio_chunk = amplitude[start_frame:end_frame]

        if not self.playing:
            sd.play(audio_chunk, self.sample_rate)
            self.playing = True
        else:
            sd.stop()  # Stop if currently playing
            self.playing = False



