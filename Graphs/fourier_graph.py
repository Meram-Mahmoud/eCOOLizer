# fourier_graph.py
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from BaseGraph import GraphBase
from signal_data import Signal

class FourierTransformGraph(GraphBase):
    def __init__(self, title="Fourier Transform"):
        super().__init__(title)
        self.is_audiogram_mode = False
        self.signal = None

    def set_signal(self, signal: Signal):
        self.signal = signal
        self.plot_full_fft()

    def plot_full_fft(self):
        if not self.signal:
            return

        frequencies, magnitudes = self.signal.get_fft_data()

        if self.is_audiogram_mode:
            freq_bins, thresholds = self.signal.calculate_audiogram(frequencies, magnitudes)
            self.graph_fit(freq_bins, thresholds,True)
            self.plot_graph(freq_bins, thresholds, pen='r', symbol='o', symbolBrush='b')
            self.plot_widget.setLabel('left', 'Threshold (dB)')
            self.plot_widget.setLabel('bottom', 'Frequency (Hz)')
        else:
            self.graph_fit(frequencies, magnitudes,False)
            self.plot_graph(frequencies, magnitudes, pen='y')
            self.plot_widget.setLabel('left', 'Magnitude')
            self.plot_widget.setLabel('bottom', 'Frequency (Hz)')
            

    def graph_fit(self, x_data, y_data, is_audiogram_mode=False):
        x_min, x_max = min(x_data), max(x_data)
        y_min, y_max = min(y_data), max(y_data)
        
        if is_audiogram_mode:
            y_padding = (y_max - y_min) * 0.1 
            y_min -= y_padding
            y_max += y_padding

        self.plot_widget.setLimits(
            xMin=x_min, xMax=x_max,
            yMin=y_min, yMax=y_max
        )
        self.plot_widget.setXRange(x_min, x_max, padding=0)
        self.plot_widget.setYRange(y_min, y_max, padding=0)


    def toggle_audiogram_mode(self):
        self.is_audiogram_mode = not self.is_audiogram_mode
        self.plot_full_fft()