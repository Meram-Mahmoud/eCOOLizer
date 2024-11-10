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
        """Set the signal data and plot the entire Fourier Transform at once."""
        self.signal = signal
        self.plot_full_fft()

    def plot_full_fft(self):
        """Plot the full FFT spectrum of the entire signal data."""
        if not self.signal:
            return

        # Get the FFT for the entire signal data
        frequencies, magnitudes = self.signal.get_fft_data()

        if self.is_audiogram_mode:
            # Plot in audiogram mode if enabled
            freq_bins, thresholds = self.signal.calculate_audiogram(frequencies, magnitudes)
            self.plot_graph(freq_bins, thresholds, pen='r', symbol='o', symbolBrush='b')
            self.plot_widget.setLabel('left', 'Threshold (dB)')
            self.plot_widget.setLabel('bottom', 'Frequency (Hz)')
        else:
            # Plot standard FFT in linear scale
            self.plot_graph(frequencies, magnitudes, pen='y')
            self.plot_widget.setLabel('left', 'Magnitude')
            self.plot_widget.setLabel('bottom', 'Frequency (Hz)')

    def toggle_audiogram_mode(self):
        """Toggle between linear FFT and audiogram modes and re-plot."""
        self.is_audiogram_mode = not self.is_audiogram_mode
        self.plot_full_fft()
