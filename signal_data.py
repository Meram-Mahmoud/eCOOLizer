import numpy as np
import soundfile as sf
#from scipy.signal import spectrogram

class Signal:
    def __init__(self, file_path=None):
        self.data = None
        self.sample_rate = None
        self.file_path = file_path

    def load_signal(self, file_path):
        self.data, self.sample_rate = sf.read(file_path)
        
        if self.data.ndim > 1:
            self.data = self.data[:, 0]

        if len(self.data) == 0:
            raise ValueError("no data")

    def get_data(self, end_frame=None):
        if self.data is None:
            raise ValueError("data not loaded.")

        if end_frame is None or end_frame > len(self.data):
            end_frame = len(self.data)

        time_axis = np.linspace(0, end_frame / self.sample_rate, num=end_frame)
        return time_axis, self.data[:end_frame]

    def get_fft_data(self, end_frame=None):
        if self.data is None:
            raise ValueError("Signal data not loaded.")

        if end_frame is None or end_frame > len(self.data):
            end_frame = len(self.data)

        frequencies = np.fft.rfftfreq(end_frame, 1 / self.sample_rate)
        magnitudes = np.abs(np.fft.rfft(self.data[:end_frame]))
        return frequencies, magnitudes
    
    def calculate_audiogram(self, frequencies, magnitudes):
        freq_bins = np.array([250, 500, 1000, 2000, 4000, 8000])
        thresholds = []
        for freq in freq_bins:
            closest_index = np.abs(frequencies - freq).argmin()
            magnitude = magnitudes[closest_index]
            threshold = 120 - min(120, 20 * np.log10(np.abs(magnitude) + 1e-3))
            thresholds.append(threshold)
        return freq_bins, thresholds
    
    
    def calculate_spectrogram(self, chunks=512, overlap=256):
        if self.data is None:
            raise ValueError("Signal data not loaded.")

        step = chunks - overlap
        spectrogram = []

        for start in range(0, len(self.data) - chunks + 1, step):
            segment = self.data[start:start + chunks]
            windowed_segment = segment * np.hanning(chunks)
            spectrum = np.fft.rfft(windowed_segment)
            spectrogram.append(np.abs(spectrum))

        spectrogram = np.array(spectrogram).T
        freqs = np.fft.rfftfreq(chunks, 1 / self.sample_rate)
        times = np.arange(0, spectrogram.shape[1]) * (step / self.sample_rate)

        return freqs, times, spectrogram


            
        # freqs, times, spectrogram = spectrogram(self.data, fs=self.sample_rate, 
        #                                          window='hann', nperseg=window_size, 
        #                                          noverlap=overlap, scaling='spectrum')

        return freqs, times, spectrogram

    def get_time_data(self):
        if self.data is None:
            raise ValueError("Signal data not loaded")
        return self.time_data, self.data
    
        
    def play_audio(self, start_frame=0, end_frame=None):
        if end_frame is None:
            end_frame = len(self.data)
        audio_chunk = self.data[start_frame:end_frame]
        import sounddevice as sd
        sd.play(audio_chunk, self.sample_rate)
        sd.wait()



