import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import cmath
import soundfile as sf
from signal_data import Signal
from Main_App.mainStyle import sliderStyle, sliderLabelStyle



class Slider(QWidget):
    newSignalAndFourier = pyqtSignal(object, object)
    def __init__(self, targetFreq = 20, label = "", min_value=-5, max_value=5, initial_value=0):
        """
        signal: [time, amp]
        """
        
        super().__init__()

        self.sliderFrequency = targetFreq
        self.samping_rate = None

        self.signal = None # signal will be modified before passing to the class

        # Create a vertical layout for each slider and label
        layout = QVBoxLayout()

        # Create the slider with specific range and initial value
        self.slider = QSlider(Qt.Vertical)
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.slider.setValue(initial_value)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setStyleSheet(sliderStyle)

        # Connect the slider's value change event
        # self.slider.valueChanged.connect(lambda value: self.modify_frequency_magnitude(int(self.label.text()[0]), value))
        self.slider.valueChanged.connect(lambda value: self.modify_frequency_magnitude((self.sliderFrequency-2000, self.sliderFrequency), value))

        # Create a label to show the slider value
        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(sliderLabelStyle)
        # Add the slider and label to the layout
        layout.addWidget(self.slider)
        layout.addWidget(self.label)

        # Set the layout on this widget
        self.setLayout(layout)

    # ========= Not used, the signal will be loaded for the import file =========
    # def load_audio(self, audio_file):
    #     # Load audio file using pydub
    #     audio = AudioSegment.from_wav(audio_file)
    #     samples = np.array(audio.get_array_of_samples())
    #     signal = [np.linspace(0, len(samples) / audio.frame_rate, num=len(samples)), samples]
    #     return signal

    # def load_signal(self):
    #     self.signal, self.sample_rate = sf.read(self.path)
        
    #     if self.signal.ndim > 1:
    #         self.signal = self.signal[:, 0]

    #     print(self.signal)

    #     if len(self.signal) == 0:
    #         raise ValueError("no data")

    def set_signal(self, new_signal):
        """
        signal: [time, amp]
        """
        self.signal = new_signal

    def set_freq(self, new_freq):
        """
        new_freq: int
        """
        self.sliderFrequency = new_freq

    def update_label(self, value):
        """
        value of slider => not used
        """
        self.label.setText(value)

    # get signal frequencies
    def fft(self, signal):
        """
        signal: amp only
        returned values:
        positive_freqs, positive_fft_values => positive fft values only [freq, amp]
        fft_freqs, fft_values => all fft values [freq, amp]
        """
        # Compute the Fourier Transform
        fft_values = np.fft.fft(signal)
        fft_freqs = np.fft.fftfreq(len(fft_values), self.samping_rate)

        # Only keep the positive half of the frequencies for display
        positive_freqs = fft_freqs[:len(fft_freqs) // 2]
        positive_fft_values = np.abs(fft_values[:len(fft_values) // 2])
        
        return positive_freqs, positive_fft_values, fft_freqs, fft_values
    
    def ifft(self, signal):
        """
        not used
        """
        pass

    # def fft(self, signal):
    #     n = len(signal)
    #     if n == 1:
    #         return signal

    #     # Split the signal into even and odd components
    #     even = self.fft(signal[0::2])
    #     odd = self.fft(signal[1::2])

    #     combined = [0] * n
    #     for k in range(n // 2):
    #         exp_factor = cmath.exp(-2j * cmath.pi * k / n) * odd[k]
    #         combined[k] = even[k] + exp_factor
    #         combined[k + n // 2] = even[k] - exp_factor

    #     return combined

    # Access and modify the magnitude of a specific frequency
    def modify_frequency_magnitude(self, target_freq , new_magnitude = 5):
        """
        signal: frequency magnitude "y-axis"
        traget_freq: slider label (which freqncy will be changed)
        new_magnitude: slider value (the gain by which the frequency will be changed)

        emits the new signal and its fft as [time, amp] and [freq, mag]
        """
        # Perform FFT
        positive_freqs, positive_fft_values, fft_freqs, fft_values = self.fft(self.signal[1])

        # # Find the index of the target frequency
        # idx = np.where(np.isclose(positive_freqs, target_freq))[0]

        # if idx.size > 0:
        #     # Set the magnitude at the target frequency
        #     idx = idx[0]
        #     # print(len(positive_fft_values))
        #     print(f'{target_freq} Hz of magnetude {fft_values[idx]}')
        #     fft_values[idx] = new_magnitude*10 + fft_values[idx]   # Preserve the phase
        #     print(f'{target_freq} Hz changed by {new_magnitude*10}. New amplitude is {fft_values[idx]}')
        #     # print(positive_fft_values - new_positive_fft_values)
        #     # Reconstruct the modified signal with inverse FFT
        #     modified_signal = np.fft.ifft(fft_values).real
        #     # self.export_modified_audio("Equalizer/sounds/animals_modified2.wav")

        # else:
        #     print(f"Frequency {target_freq} Hz not found in the FFT output.")
        #     modified_signal = self.signal[1]

        # # Loop over the target frequency range
        # for target_freq in range(target_freq[0], target_freq[1] + 1):
        #     # Find the index of the target frequency
        #     idx = np.where(np.isclose(positive_freqs, target_freq))[0]

        #     if idx.size > 0:
        #         idx = idx[0]  # Take the first match (should be unique per frequency)
        #         print(f'{target_freq} Hz original magnitude {fft_values[idx]}')

        #         # Adjust the magnitude at the target frequency
        #         fft_values[idx] = new_magnitude * 10 + fft_values[idx]  # Preserve the phase
        #         print(f'{target_freq} Hz changed by {new_magnitude * 10}. New magnitude: {fft_values[idx]}')
        #     else:
        #         print(f"Frequency {target_freq} Hz not found in the FFT output.")
                
        # Find indices for the frequencies within the target range
        indices = np.where((positive_freqs >= target_freq[0]) & (positive_freqs <= target_freq[1]))[0]

        if indices.size > 0:
            # Display original magnitudes
            print(f"Original magnitudes at frequencies {positive_freqs[indices]} Hz: {fft_values[indices]}")

            # Adjust magnitudes within the target frequency range
            fft_values[indices] += new_magnitude * 10  # Apply modification preserving phase
            print(f"Modified magnitudes at frequencies {positive_freqs[indices]} Hz: {fft_values[indices]}")
        else:
            print("No frequencies found in the specified target range.")

        # Reconstruct the modified signal with inverse FFT
        modified_signal = np.fft.ifft(fft_values).real
        self.signal = [self.signal[0], modified_signal]

        self.newSignalAndFourier.emit(self.signal, [fft_freqs, fft_values])

        # return positive_fft_values, modified_signal
    
# # Run the application
# app = QApplication(sys.argv)
# main_window = QWidget()
# main_window.setWindowTitle("Slider Pannel")
# main_window.setGeometry(600, 400, 800, 300)

# # Create a horizontal layout to align all sliders in one row
# layout = QHBoxLayout()

# # Synthetic signal
# time = np.linspace(0, 10, 1000)
# amp = np.zeros_like(time)
# for i in range(10):
#     if i % 2 == 0:
#         amp += 1/(i+1)*np.sin(2 * np.pi * i * time)
#         # pass
#     else:
#         amp += 1/(i+1)*np.cos(2 * np.pi * i * time)

# # print([time, amp][0])

# # Create and add 10 sliders with different ranges directly in the main window
# for i in range(10):
#     slider = Slider(-5, 5, 0, [time, amp])
#     slider.update_label(f'{i} Hz')
#     layout.addWidget(slider)

# # Set the layout on the main window
# main_window.setLayout(layout)
# main_window.show()

# # sys.exit(app.exec_())
# signal = Signal()
# signal.load_signal("eCOOLizer/sounds/animal_extended_audio.wav")
# time, amp = signal.get_data()
# print(time, amp)

# app = QApplication([])
# slider_widget = Slider(audio_file=[time, amp])
# slider_widget.show()
# app.exec_()
