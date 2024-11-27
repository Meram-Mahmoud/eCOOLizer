import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class SpectrogramDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure, self.ax = plt.subplots(figsize=(6, 4))  
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        self.color_map = plt.cm.get_cmap("viridis") 
        self.colorbar = None
        # print("spectogram")
        # print("spectogram")

    def display_spectrogram(self, signal):
        # Inputs: signal (object)
        # Outputs:
        #Displays the spectrogram on the canvas.
       
        #Calculates the spectrogram data, converts it to dB scale, and plots it.
        if not signal:
            return

        freqs, times, spectrogram_data = signal.calculate_spectrogram(chunks=512)

        #spectrogram_db (numpy array): Intensity values in dB, Shape: (chunks//2 + 1, number of windows).
        spectrogram_db = 20 * np.log10(spectrogram_data + 1e-6)

        self.ax.clear()
        self.spectrogram_image = self.ax.imshow(spectrogram_db, aspect='auto', cmap=self.color_map,
                                                extent=[times[0], times[-1], freqs[0], freqs[-1]], origin='lower')
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Frequency (Hz)")

        if self.colorbar is None: 
            self.colorbar = self.figure.colorbar(self.spectrogram_image, ax=self.ax, orientation='vertical')
            self.colorbar.set_label("Intensity (dB)")
        else:  
            self.colorbar.update_normal(self.spectrogram_image)

        self.canvas.draw()

    def toggle_visibility(self, is_visible):
        if is_visible:
            self.show()
        else:
            self.hide()
