import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from BaseGraph import GraphBase
from signal_data import Signal

class FourierTransformGraph(GraphBase):
    def __init__(self, title="Fourier Transform"):
        super().__init__(title)
        self.is_audiogram_mode = False
        self.signal = None
        self.current_frame = 0
        self.playSpeed = 100

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.is_playing = False

    def set_signal(self, signal: Signal):
        self.signal = signal
        self.current_frame = 0
        self.update_plot() 
        self.timer.start(self.playSpeed)

    def update_plot(self):
        if not self.signal:
            return

        frequencies, magnitudes = self.signal.get_fft_data(end_frame=self.current_frame)
        
        if self.is_audiogram_mode:
            freq_bins, thresholds = self.signal.calculate_audiogram(frequencies, magnitudes)
            self.plot_graph(freq_bins, thresholds, pen='r', symbol='o', symbolBrush='b')
            self.plot_widget.setLabel('left', 'Threshold (dB)')
            self.plot_widget.setLabel('bottom', 'Frequency (Hz)')
        else:
            self.plot_graph(frequencies, magnitudes, pen='y')
            self.plot_widget.setLabel('left', 'Magnitude')
            self.plot_widget.setLabel('bottom', 'Frequency (Hz)')

        self.current_frame += int(self.signal.sample_rate * 0.05)
        if self.current_frame >= len(self.signal.data):
            self.timer.stop()
            self.is_playing = False

    def toggle_audiogram_mode(self):
        self.is_audiogram_mode = not self.is_audiogram_mode
        self.update_plot()  



#test 
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = QMainWindow()
    main_window.setWindowTitle("Fourier Transform Graph")
    main_window.resize(800, 600)

    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    fourier_graph = FourierTransformGraph("Fourier Transform")
    layout.addWidget(fourier_graph)

    def load_signal():
        file_path, _ = QFileDialog.getOpenFileName(main_window, "Open Audio File", "", "Audio Files (*.wav *.flac *.ogg)")
        if file_path:
            signal = Signal()
            signal.load_signal(file_path)
            fourier_graph.set_signal(signal)

    load_button = QPushButton("Load Signal")
    load_button.clicked.connect(load_signal)
    layout.addWidget(load_button)

    toggle_button = QPushButton("Toggle Audiogram Mode")
    toggle_button.clicked.connect(fourier_graph.toggle_audiogram_mode)
    layout.addWidget(toggle_button)

    main_window.show()
    sys.exit(app.exec_())
