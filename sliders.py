import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment

class Slider(QWidget):
    def __init__(self, min_value=-5, max_value=5, initial_value=0, audio_file=None):
        super().__init__()

        self.signal = audio_file
        print(audio_file)
        # self.signal = self.load_audio(audio_file)
        # self.export_modified_audio("Equalizer/sounds/animals_modified.wav")


        # Create a vertical layout for each slider and label
        layout = QVBoxLayout()

        # Create the slider with specific range and initial value
        self.slider = QSlider(Qt.Vertical)
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.slider.setValue(initial_value)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)

        # Connect the slider's value change event
        # self.slider.valueChanged.connect(lambda value: self.modify_frequency_magnitude(int(self.label.text()[0]), value))
        self.slider.valueChanged.connect(lambda value: self.modify_frequency_magnitude((2000), value))

        # Create a label to show the slider value
        self.label = QLabel(f"Value: {initial_value}")
        self.label.setAlignment(Qt.AlignCenter)

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

    def update_label(self, value):
        self.label.setText(value)

    # get signal frequencies
    def fourier(self, signal):
        # Compute the Fourier Transform
        fft_values = np.fft.fft(signal)
        fft_freqs = np.fft.fftfreq(len(fft_values), 1/6000)

        # Only keep the positive half of the frequencies for display
        positive_freqs = fft_freqs[:len(fft_freqs) // 2]
        positive_fft_values = np.abs(fft_values[:len(fft_values) // 2])
        
        return positive_freqs, positive_fft_values, fft_freqs, fft_values

    # Access and modify the magnitude of a specific frequency
    def modify_frequency_magnitude(self, target_freq, new_magnitude):
        """
        signal: y-axis
        # traget_freq: slider label
        traget_freq: tuble(min freq, max freq)
        new_magnitude: slider value
        """
        # Perform FFT
        positive_freqs, positive_fft_values, fft_freqs, fft_values = self.fourier(self.signal[1])

        # #----------------------------Testing---------------------------------
        # # Plot the original signal
        # plt.subplot(2, 1, 1)
        # plt.plot(self.signal[0], self.signal[1])
        # plt.legend()
        # plt.title("Original Signal")
        # plt.xlabel("Time [s]")
        # plt.ylabel("Amplitude")
        # plt.xlim(0, 10)
        # #--------------------------------------------------------------------

        # Find the index of the target frequency
        idx = np.where(np.isclose(positive_freqs, target_freq))[0]

        if idx.size > 0:
            # Set the magnitude at the target frequency
            idx = idx[0]
            # print(len(positive_fft_values))
            print(f'{target_freq} Hz of magnetude {fft_values[idx]}')
            fft_values[idx] = new_magnitude*10 + fft_values[idx]   # Preserve the phase
            print(f'{target_freq} Hz changed by {new_magnitude*10}. New amplitude is {fft_values[idx]}')
            # print(positive_fft_values - new_positive_fft_values)
            # Reconstruct the modified signal with inverse FFT
            modified_signal = np.fft.ifft(fft_values).real
            # self.export_modified_audio("Equalizer/sounds/animals_modified2.wav")

        else:
            print(f"Frequency {target_freq} Hz not found in the FFT output.")
            modified_signal = self.signal[1]

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
                
        # # -------------------------Testing----------------------------
        # # Plot the Fourier Transform (magnitude)
        # plt.subplot(2, 1, 2)
        # # print(len(self.signal[0]), len(modified_signal))
        # plt.plot(self.signal[0], modified_signal)
        # plt.legend()
        # plt.title("After modefing frequency")
        # plt.xlabel("Time [s]")
        # plt.ylabel("Amplitude")
        # plt.xlim(0,10)

        # plt.tight_layout()
        # plt.show()
        # #--------------------------------------------------------------

        # Reconstruct the modified signal with inverse FFT
        modified_signal = np.fft.ifft(fft_values).real
        self.signal = [self.signal[0], modified_signal]

        return positive_fft_values, modified_signal
    
    # ==================== Not used ===================
    # def export_modified_audio(self, filename="modified_audio.wav"):
    #     # Export the modified signal as a .wav file
    #     modified_samples = np.int16(self.signal[1] / np.max(np.abs(self.signal[1])) * 32767)
    #     modified_audio = AudioSegment(
    #         modified_samples.tobytes(), frame_rate=1000, sample_width=2, channels=1
    #     )
    #     modified_audio.export(filename, format="wav")

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

# sys.exit(app.exec_())

app = QApplication([])
slider_widget = Slider(audio_file="Equalizer/sounds/animal_extended_audio.wav")
slider_widget.show()
app.exec_()
