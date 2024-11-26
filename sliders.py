import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
import numpy as np
from Main_App.mainStyle import sliderStyle, sliderLabelStyle

class Slider(QWidget):
    newSignalAndFourier = pyqtSignal(object)
    def __init__(self, targetFreq = [], label = "", min_value=-5, max_value=5, initial_value=0):
        """
        self.signal: fft signal
        targetFreq: array of bandwidths
        min_value and max_values will be changed to notice the changes in sound
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
        self.slider.valueChanged.connect(lambda value: self.modify_frequency_magnitude(self.sliderFrequency, value))

        # Create a label to show the slider value
        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(sliderLabelStyle)
        # Add the slider and label to the layout
        layout.addWidget(self.slider)
        layout.addWidget(self.label)

        # Set the layout on this widget
        self.setLayout(layout)

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

    # Access and modify the magnitude of a specific frequency
    def modify_frequency_magnitude(self, target_freq , new_magnitude = 5):
        """
        signal: frequency magnitude "y-axis"
        traget_freq: bandwidths of the slider
        new_magnitude: slider value (the gain by which the frequency will be changed)

        emits the fft of new signal [freq, mag]
        """
        # Perform FFT
        # positive_freqs, positive_fft_values, fft_freqs, fft_values = self.fft(self.signal[1])

        frequency, magniudes = self.signal[0], self.signal[1]
        for i in target_freq:
            indices = np.where((frequency >= i[0]) & (frequency <= i[1]))[0]

            if indices.size > 0:
                # Display original magnitudes
                print(f"Original magnitudes at frequencies {frequency[indices]} Hz: {magniudes[indices]}")

                # Adjust magnitudes within the target frequency range
                magniudes[indices] += new_magnitude * 1000  # Apply modification preserving phase
                print(f"Modified magnitudes at frequencies {frequency[indices]} Hz: {magniudes[indices]}")
            else:
                print("No frequencies found in the specified target range.")

        # Reconstruct the modified signal with inverse FFT
        # modified_signal = np.fft.ifft(fft_values).real
        # self.signal = [self.signal[0], modified_signal]

        self.newSignalAndFourier.emit([frequency, magniudes])

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
