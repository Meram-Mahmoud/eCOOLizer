import numpy as np
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from Main_App.mainStyle import sliderStyle, sliderLabelStyle

class WienerSlider(QWidget):
    newSignalAndFourier = pyqtSignal(object)

    def __init__(self, label="Noise Reduction", min_value=0, max_value=10, initial_value=5):
        super().__init__()
        
        self.signal = None
        self.noise_profile = None
        self.sample_rate = None
        self.selected_region = None
        
        # Create vertical layout
        layout = QVBoxLayout()
        
        # Create slider
        self.slider = QSlider(Qt.Vertical)
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.slider.setValue(initial_value)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setStyleSheet(sliderStyle)
        
        # Connect slider value change
        self.slider.valueChanged.connect(self.apply_wiener_filter)
        
        # Create label
        self.label = QLabel(label)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(sliderLabelStyle)
        
        # Add widgets to layout
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        
        self.setLayout(layout)

    def set_signal(self, signal_data):
        """Set the input signal data (FFT format)"""
        self.signal = signal_data
        
    def set_noise_profile(self, start_idx, end_idx):
        """Set noise profile from selected region of the signal"""
        if self.signal is None:
            return
            
        frequencies, magnitudes = self.signal
        self.noise_profile = magnitudes[start_idx:end_idx]
        self.selected_region = (start_idx, end_idx)
        
    def set_sample_rate(self, sr):
        """Set the sampling rate"""
        self.sample_rate = sr

    def apply_wiener_filter(self, slider_value):
        """Apply Wiener filter with strength controlled by slider"""
        if self.signal is None or self.noise_profile is None:
            return
            
        frequencies, signal_magnitudes = self.signal
        
        # Extend noise profile to match signal length
        noise_pattern = np.tile(self.noise_profile, 
                              (len(signal_magnitudes) // len(self.noise_profile)) + 1)
        noise_pattern = noise_pattern[:len(signal_magnitudes)]
        
        # Calculate power spectral densities
        signal_psd = np.abs(signal_magnitudes) ** 2
        noise_psd = np.abs(noise_pattern) ** 2
        
        # Apply Wiener filter with adjustable noise reduction
        # Slider value controls the noise reduction strength
        noise_reduction_factor = slider_value / 10.0  # Normalize to 0-1 range
        epsilon = 1e-10  # Small constant to avoid division by zero
        
        wiener_filter = (signal_psd / (signal_psd + noise_reduction_factor * noise_psd + epsilon))
        filtered_magnitudes = wiener_filter * signal_magnitudes
        
        # Ensure no negative magnitudes
        filtered_magnitudes = np.abs(filtered_magnitudes)
        
        # Emit the filtered signal
        self.newSignalAndFourier.emit([frequencies, filtered_magnitudes])