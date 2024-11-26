import numpy as np
import soundfile as sf
import sounddevice as sd
#from scipy.signal import spectrogram

class Signal:
    def __init__(self, file_path="sounds/Uniform.wav"):
        # Inputs: file_path (str): Path to the audio file
        self.data = None  # Have audio samples as a 1D numpy array
        self.sample_rate = None  # Sampling rate of the audio file
        self.file_path = file_path
        self.playing=False
        self.load_signal(file_path)
        print("signal")

    def load_signal(self, file_path):
        # Inputs: file_path (str): Path to the audio file
        # Outputs:
        #self.data : (numpy array): 1D array of audio samples. Shape: (number of samples,)
        #self.sample_rate (int): Sampling rate of the audio file
        self.data, self.sample_rate = sf.read(file_path)
        
        if self.data.ndim > 1: 
            self.data = self.data[:, 0]  # Take the first channel if multi-channel (represents mono audio)

        if len(self.data) == 0:
            raise ValueError("no data")
        
        num_samples = len(self.data)
        time_axis = np.linspace(0, num_samples / self.sample_rate, num=num_samples)
        
        self.data = np.column_stack((time_axis, self.data))
        self.fft_data()

    def get_data(self, end_frame=None):
         # Inputs: end_frame, Last frame index to return, Default: full length
        # Outputs:
        #time_axis (numpy array): Time values for each sample, Shape: (end_frame,)
        #self.data[:end_frame] (numpy array): Audio amplitude values, Shape: (end_frame,)
  
        if self.data is None:
            raise ValueError("data not loaded.")

        if end_frame is None or end_frame > len(self.data):
            end_frame = len(self.data)

        #time axis is calculated using the sample rate and the number of frames
        # time_axis = np.linspace(0, end_frame / self.sample_rate, num=end_frame)
       
        # Returns time axis and amplitude values from the start up to end_frame
        # return time_axis, self.data[:end_frame]
        return self.data[:end_frame, 0], self.data[:end_frame, 1]
    
    # ifft
    def get_time_domain_data(self, end_frame=None):
        # Ensure valid end_frame value
        if self.data is None:
            raise ValueError("Fourier data not available.")
        
        if not end_frame or end_frame > len(self.data):
            end_frame = len(self.data)  # Use the full length if end_frame is None or exceeds bounds

        # Validate the structure of self.data
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
        # Inputs: new_data (tuple): new_data[1] (new amplitude values.) is the new signal data
        # Outputs:
        # Updates self.data (numpy array), Shape: (number of samples,)
        if not end_frame or end_frame > len(self.data):
            end_frame = len(self.data)  # Use the full length if end_frame is None or exceeds bounds

        self.data[:end_frame, 1] = new_data[1]

        if len(new_data[0]) != len(new_data[1]):
            raise ValueError("Time and amplitude arrays must be the same length.")

        # self.data = np.column_stack(new_data)

        print(self.data)

    def fft_data(self, end_frame=None):
        # Inputs: end_frame , The end index for FFT computation
        # Outputs:
        #frequencies ( 1D numpy array): FFT frequency values, Shape: (end_frame//2 + 1,)
        #magnitudes (numpy array): Magnitudes of the FFT, Shape: (end_frame//2 + 1,)

        #additional info
        # The FFT output shape is 'end_frame // 2 + 1' because we only need the first half 
        # of the spectrum for real-valued signals. This includes frequencies from 0 Hz 
        # to the Nyquist frequency (half the sample rate), reducing redundant data
            
        if self.data is None:
            raise ValueError("Signal data not loaded.")

        if end_frame is None or end_frame > len(self.data):
            end_frame = len(self.data)

        # frequencies = np.fft.rfftfreq(end_frame, 1 / self.sample_rate)
        # magnitudes = np.abs(np.fft.rfft(self.data[:end_frame]))

        amplitude = self.data[:end_frame, 1]
        frequencies = np.fft.rfftfreq(end_frame, 1 / self.sample_rate)
        magnitudes = np.abs(np.fft.rfft(amplitude))
        phase = np.angle(np.fft.rfft(amplitude))
        
        self.data = np.column_stack((frequencies, magnitudes, phase))
        # return frequencies, magnitudes

    def get_fft_data(self, end_frame = None):
        return self.data[:end_frame, 0], self.data[:end_frame, 1]
    
    def calculate_spectrogram(self, chunks=512, overlap=256):
        # Inputs:
        #chunks (int): FFT window size
        #overlap (int): Overlap between chunks
        # Outputs:
        #freqs: (numpy array): Frequencies for FFT bins, Shape: (chunks//2 + 1,)
        #times: (numpy array): Time points for each FFT window
        #spectrogram: (numpy array): Magnitude of frequencies over time, Shape: (chunks//2 + 1, number of windows)
    
        #spectrogram is calculated by applying FFT to overlapping chunks of the signal
   
        if self.data is None:
            raise ValueError("Signal data not loaded.")

        step = chunks - overlap  # Step size between overlapping windows.
        spectrogram = []  # Store the FFT magnitudes for each time window.

        for start in range(0, len(self.data) - chunks + 1, step):
            # segment = self.data[start:start + chunks]
            segment = self.data[start:start + chunks, 1]
            windowed_segment = segment * np.hanning(chunks)
            spectrum = np.fft.rfft(windowed_segment)  # Perform FFT on the chunk
            spectrogram.append(np.abs(spectrum)) # Magnitude of the spectrum

        spectrogram = np.array(spectrogram).T
        freqs = np.fft.rfftfreq(chunks, 1 / self.sample_rate)
        times = np.arange(0, spectrogram.shape[1]) * (step / self.sample_rate)

        return freqs, times, spectrogram


            
        # freqs, times, spectrogram = spectrogram(self.data, fs=self.sample_rate, 
        #                                          window='hann', nperseg=window_size, 
        #                                          noverlap=overlap, scaling='spectrum')

        # return freqs, times, spectrogram

    def calculate_audiogram(self, frequencies, magnitudes):
        # Inputs:
        #frequencies (numpy array): FFT frequency, Shape: (n,)
        #magnitudes (numpy array): Magnitudes of FFT, Shape: (n,)
        # Outputs:
        #freq_bins(numpy array): Fixed audiogram frequency bins (250–8000 Hz), Shape: (6,).
        #thresholds(list): Threshold values (dB), Shape: (6,).
        freq_bins = np.array([250, 500, 1000, 2000, 4000, 8000])
        thresholds = []
        for freq in freq_bins:
            closest_index = np.abs(frequencies - freq).argmin()
            magnitude = magnitudes[closest_index]
            threshold = 120 - min(120, 20 * np.log10(np.abs(magnitude) + 1e-3))
            thresholds.append(threshold)
        return freq_bins, thresholds
    
        # valid_indices = frequencies > 0
        # frequencies = frequencies[valid_indices]
        # magnitudes = magnitudes[valid_indices]
        
        # # Convert to log scale for frequencies
        # log_frequencies = np.log10(frequencies)
        
        # # Convert magnitudes to decibels
        # thresholds = 120 - np.minimum(120, 20 * np.log10(magnitudes + 1e-6))
        
        # return log_frequencies, thresholds
    
    
    

    def get_time_data(self):
        # Outputs:
        #self.time_data (numpy array): Time axis of time 
        #self.data (numpy array): amplitude values, Shape: (number of samples,).
        if self.data is None:
            raise ValueError("Signal data not loaded")
        return self.time_data, self.data
    
        
    # def play_audio(self, start_frame=0, end_frame=None):
    #     if end_frame is None:
    #         end_frame = len(self.data)
    #     audio_chunk = self.data[start_frame:end_frame]
    #     import sounddevice as sd
    #     sd.play(audio_chunk, self.sample_rate)
    #     sd.wait()

    def play_audio(self, start_frame=0, end_frame=None):
        # Inputs:
        #start_frame (int): Start frame index, Default: 0.
        #end_frame (int): End frame index, Default: full length.
        # Outputs:

        #Extracts the portion of audio data and plays it using the sounddevice library.
        if self.data is None:
            raise ValueError("Load audio data before attempting playback.")
        
        if end_frame is None:
            end_frame = len(self.data)
        
        # audio_chunk = self.data[start_frame:end_frame] # Extract the audio chunk to play        
        time, amplitude = self.get_time_domain_data()
        audio_chunk = amplitude[start_frame:end_frame]

        if not self.playing:
            sd.play(audio_chunk, self.sample_rate)
            self.playing = True
        else:
            sd.stop()  # Stop if currently playing
            self.playing = False




