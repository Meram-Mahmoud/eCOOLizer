import numpy as np
import soundfile as sf

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
            raise ValueError("data not loaded")

        if end_frame is None or end_frame > len(self.data):
            end_frame = len(self.data)

        end_frame = max(end_frame, 2) 

        frequencies = np.fft.rfftfreq(end_frame, 1 / self.sample_rate) #Needs to be done with fourrier function call it here 
        magnitudes = np.fft.rfft(self.data[:end_frame]) #Needs to be done with fourrier function call it here 
        return frequencies, np.abs(magnitudes)
    
    def calculate_audiogram(self, frequencies, magnitudes):
        freq_bins = np.array([250, 500, 1000, 2000, 4000, 8000])
        thresholds = []
        for freq in freq_bins:
            closest_index = np.abs(frequencies - freq).argmin()
            magnitude = magnitudes[closest_index]
            threshold = 120 - min(120, 20 * np.log10(np.abs(magnitude) + 1e-3))
            thresholds.append(threshold)
        return freq_bins, thresholds


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

    # def get_audiogram_data(self, end_frame):
    #     if end_frame == 0 or end_frame > len(self.data):
    #         return None, None
    #     yf = np.fft.rfft(self.data[:end_frame]) #Needs to be done with fourrier function call it here 
    #     xf = np.fft.rfftfreq(end_frame, 1 / self.sample_rate) #needs to be done with fourrier function call it here 
        
    #     freq_bins = np.array([250, 500, 1000, 2000, 4000, 8000])
    #     thresholds = [20 * np.log10(np.abs(yf[np.abs(xf - freq).argmin()] + 1e-3)) for freq in freq_bins]
    #     thresholds = 120 - np.clip(thresholds, 0, 120)
    #     return freq_bins, thresholds

