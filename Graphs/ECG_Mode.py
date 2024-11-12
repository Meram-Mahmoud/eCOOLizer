import sys
import os
import numpy as np
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QSlider, QLabel, QFileDialog)
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from scipy.fft import fft, ifft, fftfreq
from scipy.signal import butter, filtfilt
from fourier_graph import FourierTransformGraph
from signal_data import Signal


class ArrhythmiaAmplifierApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ecg_signal = Signal()
        self.manipulated_signal= Signal()
        self.manipulated_signal = self.ecg_signal
        self.filtered_components = {
            'Normal': None,
            'Aflutter': None,
            'Afib': None,
            'Bradycardia': None
        }

        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        slider_layout = QVBoxLayout()
        
        # Load Signal Button
        self.load_button = QPushButton('Load Signal')
        self.load_button.clicked.connect(self.load_signal)
        button_layout.addWidget(self.load_button)
        
        # Sliders for different arrhythmia components
        self.sliders = {}
        self.slider_labels = {}
        slider_names = ['Normal', 'Aflutter', 'Afib', 'Bradycardia']
        for name in slider_names:
            slider_label = QLabel(f"{name} Amplification: 1.0")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(50)
            slider.setValue(10)
            slider.valueChanged.connect(self.update_amplification)
            
            # Store the slider and label
            self.sliders[name] = slider
            self.slider_labels[name] = slider_label
            
            # Add to layout
            slider_layout.addWidget(slider_label)
            slider_layout.addWidget(slider)
        

        self.input_graph = pg.PlotWidget()
        main_layout.addWidget(self.input_graph)

        self.output_graph = pg.PlotWidget()
        main_layout.addWidget(self.output_graph)
        
        self.fourier_graph = FourierTransformGraph("Fourier Transform")
        main_layout.addWidget(self.fourier_graph)
        
        # Add widgets to main layout
        main_layout.addLayout(button_layout)
        main_layout.addLayout(slider_layout)
        
        # Set layout and window title
        self.setLayout(main_layout)
        self.setWindowTitle("Arrhythmia Amplifier")
        

    def load_signal(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.ecg_signal.load_signal_from_csv(file_path)

            self.ecg_signal.sample_rate=1 / (self.ecg_signal.time[1] - self.ecg_signal.time[0])
            # self.ecg_signal=signal.data
            # self.time=signal.time
            self.ecg_signal.sample_rate=self.fs = 1 / (self.ecg_signal.time[1] - self.ecg_signal.time[0])

            print(self.ecg_signal.data)
 
            self.input_graph.clear() 
            self.output_graph.clear() 
            self.input_graph.plot(self.ecg_signal.time, self.ecg_signal.data, pen='b', name="Signal")
            self.output_graph.plot(self.manipulated_signal.time, self.manipulated_signal.data, pen='b', name="Signal")
            self.fourier_graph.set_signal(self.ecg_signal) 

            self.fft_freq = fftfreq(len(self.ecg_signal.data), d=1 / self.ecg_signal.sample_rate)
            self.fft_data = fft(self.ecg_signal.data)

            # Bandpass filter ranges for different arrhythmias
            self.filtered_components['Normal'] = self.bandpass_filter(self.ecg_signal.data, 0.5, 20)
            self.filtered_components['Aflutter'] = self.bandpass_filter(self.ecg_signal.data, 5, 20)
            self.filtered_components['Afib'] = self.bandpass_filter(self.ecg_signal.data, 0.5, 5)
            self.filtered_components['Bradycardia'] = self.bandpass_filter(self.ecg_signal.data, 3, 10)
            
            # Identify Vfib peaks to add markers
            # self.vfib_peaks = self.detect_vfib_peaks(self.filtered_components['Vfib'])
            # self.afib_peaks = self.detect_vfib_peaks(self.filtered_components['Afib'])
            self.tfib_peaks = self.detect_vfib_peaks(self.filtered_components['Bradycardia'])

            # Add markers for Vfib regions
            for vfib_time in self.vfib_peaks:
                line = pg.InfiniteLine(pos=vfib_time, angle=90, pen=pg.mkPen(color='r', width=1.5, style=Qt.DashLine))
                self.input_graph.addItem(line)

            self.update_amplification()

        
    def bandpass_filter(self, signal, lowcut, highcut, order=5):
        """Apply a band-pass filter to isolate frequency components for arrhythmia types."""
        nyquist = 0.5 * self.fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return filtfilt(b, a, signal)
    
    def detect_vfib_peaks(self, vfib_signal):
        """Detect regions with high energy in the Vfib component as Vfib 'peaks'."""
        threshold = np.max(np.abs(vfib_signal)) * 0.6  # Set a threshold for Vfib regions
        peaks = np.where(np.abs(vfib_signal) > threshold)[0]
        return self.ecg_signal.time[peaks]


    def update_amplification(self):
        """Apply amplification based on slider values and update the Output Signal plot."""
        if self.ecg_signal.data is None or self.ecg_signal.time is None:
            print("No signal loaded.")
            return
        

         # Apply amplification based on frequency band
        amplified_fft = self.fft_data.copy()
        for name, freq_range in zip(['Normal','Aflutter', 'Afib', 'Bradycardia'], [(0.5,20),(5, 20), (0.5, 5), (20, 40)]):
            amp_factor = self.sliders[name].value() / 10.0
            self.slider_labels[name].setText(f"{name} Amplification: {amp_factor:.1f}")

            # Get indices for the desired frequency range
            band_indices = (np.abs(self.fft_freq) >= freq_range[0]) & (np.abs(self.fft_freq) <= freq_range[1])
            amplified_fft[band_indices] *= amp_factor

        # Inverse FFT to return to time domain
        self.manipulated_signal.data = np.real(ifft(amplified_fft))
        self.manipulated_signal.time = self.ecg_signal.time

        # # Start with the original signal as the base for the output
        # self.manipulated_signal=self.ecg_signal
        # self.manipulated_signal.data = self.ecg_signal.data.copy() * (self.sliders['Normal'].value() / 10.0)
        # print("slider value")
        # slidervall=self.sliders['Normal'].value()
        # print(slidervall)

        # # Add the arrhythmic components based on slider values
        # for name in ['Normal','Vfib', 'Afib', 'Tachycardia']:
        #     component = self.filtered_components[name]
        #     amp_factor = self.sliders[name].value() / 10.0
        #     self.slider_labels[name].setText(f"{name} Amplification: {amp_factor:.1f}")
        #     self.manipulated_signal.data += amp_factor * component
        #     print("VFIB")
        #     print(self.sliders['Vfib'].value())
        #     print("AFIB")
        #     print(self.sliders['Afib'].value())
        #     print("TFIB")
        #     print(self.sliders['Tachycardia'].value())
            

        # Plot the amplified output signal
        self.output_graph.clear()  # Clears the previous plot
        self.output_graph.plot(self.manipulated_signal.time, self.manipulated_signal.data, pen='r')  # Replot with updated signal
        
        # Also update the frequency domain plot
        self.fourier_graph.set_signal(self.manipulated_signal) 



def main():
    app = QApplication(sys.argv)
    window = ArrhythmiaAmplifierApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
