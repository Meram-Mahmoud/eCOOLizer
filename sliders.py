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
        self.magnitudes = None
        self.constant = 100
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
        signal: fourier signal
        """
        self.signal = new_signal

    def set_freq(self, new_freq):
        """
        new_freq: int
        """
        self.sliderFrequency = new_freq

    def set_constant(self, const):
        self.constant = const

    def set_old_magnitudes(self, mag):
        self.magnitudes = mag

    def update_label(self, value):
        """
        value of slider => not used
        """
        self.label.setText(value)
    
    # Access and modify the magnitude of a specific frequency
    def modify_frequency_magnitude(self, target_freq , new_magnitude = 5):
        """
        signal: frequency magnitude "y-axis"
        traget_freq: bandwidths of the slider
        new_magnitude: slider value (the gain by which the frequency will be changed)

        emits the fft of new signal [freq, mag]
        """
        frequency, magnitudes = self.signal[0], self.signal[1]
        for i in target_freq:
            indices = np.where((frequency >= i[0]) & (frequency <= i[1]))[0]

            if indices.size > 0:
                # Display original magnitudes
                # print(f"Original magnitudes at frequencies {frequency[indices]} Hz: {magnitudes[indices]}")

                magnitudes[indices] = new_magnitude * self.constant + self.magnitudes[indices]
                magnitudes[magnitudes < 0] = 0
                print(magnitudes[indices], self.magnitudes[indices])
                # print(f"Modified magnitudes at frequencies {frequency[indices]} Hz: {magnitudes[indices]}")
            else:
                print("No frequencies found in the specified target range.")

        self.newSignalAndFourier.emit([frequency, magnitudes])
    