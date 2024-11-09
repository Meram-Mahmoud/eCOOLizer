import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import numpy as np

class Slider(QWidget):
    def __init__(self, min_value=0, max_value=10, initial_value=5):
        super().__init__()

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
        self.slider.valueChanged.connect(lambda value: self.modify_frequency_magnitude(amp, int(self.label.text()[0]), value))

        # Create a label to show the slider value
        self.label = QLabel(f"Value: {initial_value}")
        self.label.setAlignment(Qt.AlignCenter)

        # Add the slider and label to the layout
        layout.addWidget(self.slider)
        layout.addWidget(self.label)

        # Set the layout on this widget
        self.setLayout(layout)

    def update_label(self, value):
        self.label.setText(value)

    # get signal frequencies
    def fourier(self, signal):
        # Compute the Fourier Transform
        fft_values = np.fft.fft(signal)
        fft_freqs = np.fft.fftfreq(len(fft_values), 1 / 100)

        # Only keep the positive half of the frequencies for display
        positive_freqs = fft_freqs[:len(fft_freqs) // 2]
        positive_fft_values = np.abs(fft_values[:len(fft_values) // 2])
        
        return positive_freqs, positive_fft_values

    # Access and modify the magnitude of a specific frequency
    def modify_frequency_magnitude(self, signal, target_freq, new_magnitude):
        """
        signal: y-axis
        traget_freq: slider label
        new_magnitude: slider value
        """
        # Perform FFT
        positive_freqs, positive_fft_values = self.fourier(signal)

        # Find the index of the target frequency
        idx = np.where(np.isclose(positive_freqs, target_freq))[0]

        if idx.size > 0:
            # Set the magnitude at the target frequency
            idx = idx[0]
            # print(positive_fft_values)
            print(f'{target_freq} Hz of magnetude {positive_fft_values[idx]}')
            positive_fft_values[idx] = new_magnitude + positive_fft_values[idx]   # Preserve the phase
            print(f'{target_freq} Hz changed by {new_magnitude}. New amplitude is {positive_fft_values[idx]}')
            # print(positive_fft_values - new_positive_fft_values)
            # Reconstruct the modified signal with inverse FFT
            # modified_signal = np.fft.ifft(positive_fft_values).real
        else:
            print(f"Frequency {target_freq} Hz not found in the FFT output.")
            modified_signal = signal
        
        # print(positive_fft_values)
        # print(modified_signal)
        # print(positive_freqs)

        return positive_fft_values

# Run the application
app = QApplication(sys.argv)
main_window = QWidget()
main_window.setWindowTitle("Slider Pannel")
main_window.setGeometry(600, 400, 800, 300)

# Create a horizontal layout to align all sliders in one row
layout = QHBoxLayout()

# Create and add 10 sliders with different ranges directly in the main window
for i in range(10):
    slider = Slider(-5, 5, 0)
    slider.update_label(f'{i} Hz')
    layout.addWidget(slider)

# Synthetic signal
time = np.linspace(0, 10, 1000)
amp = np.zeros_like(time)
for i in range(10):
    amp += i/100*np.sin(2 * np.pi * i * time)

# Set the layout on the main window
main_window.setLayout(layout)
main_window.show()

sys.exit(app.exec_())
