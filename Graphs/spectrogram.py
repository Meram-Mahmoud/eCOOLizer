import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Main_App.mainStyle import darkColor, yellowColor

class SpectrogramDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure, self.ax = plt.subplots(figsize=(1, 1))  
        self.figure.patch.set_facecolor(darkColor)  
        self.ax.set_facecolor(darkColor)  

        self.ax.tick_params(axis='both', colors=yellowColor)  
        self.ax.xaxis.label.set_color(yellowColor) 
        self.ax.yaxis.label.set_color(yellowColor) 
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        self.color_map = plt.cm.get_cmap("viridis") 
        self.colorbar = None

    def display_spectrogram(self, signal):
       
        #Calculates the spectrogram data, converts it to dB scale, and plots it.
        if not signal:
            return

        freqs, times, spectrogram_data = signal.calculate_spectrogram(chunks=512)

        #spectrogram_db (numpy array): Intensity values in dB, Shape: (chunks//2 + 1, number of windows).
        spectrogram_db = 20 * np.log10(spectrogram_data + 1e-6)

        avg_power = np.mean(spectrogram_db, axis=1)
        
        # Find frequencies with significant energy (adjust threshold as needed)
        threshold = np.max(avg_power) - 40  # Look at data within 40dB of max
        significant_freqs = np.where(avg_power > threshold)[0]
        
        if len(significant_freqs) > 0:
            # Get the frequency range with some padding
            min_freq_idx = max(0, np.min(significant_freqs) - 5)
            max_freq_idx = min(len(freqs) - 1, np.max(significant_freqs) + 5)
            
            y_min = freqs[min_freq_idx]
            y_max = freqs[max_freq_idx]
            
            # Add a small padding (10% of the range)
            freq_range = y_max - y_min
            y_min = max(0, y_min - freq_range * 0.1)
            y_max = y_max + freq_range * 0.1
        else:
            y_min = 0
            y_max = freqs[-1]
        
        self.ax.clear()
        self.spectrogram_image = self.ax.imshow(spectrogram_db, aspect='auto', cmap=self.color_map,
                                                extent=[times[0], times[-1], freqs[0], freqs[-1]], origin='lower')
        
        self.ax.set_ylim(y_min, y_max)
        
        self.ax.set_xlabel("Time (s)", color=yellowColor)
        self.ax.set_ylabel("Frequency (Hz)", color=yellowColor)

        if self.colorbar is None: 
            self.colorbar = self.figure.colorbar(self.spectrogram_image, ax=self.ax, orientation='vertical')
            self.colorbar.set_label("Intensity (dB)",color=yellowColor)
            self.colorbar.ax.tick_params(colors=yellowColor) 
        else:  
            self.colorbar.update_normal(self.spectrogram_image)

        # self.figure.set_size_inches(self.width() / 200, self.height() / 200)
        self.figure.subplots_adjust(left=0.15, right=1, top=0.95, bottom=0.3)
        self.canvas.draw()

    def toggle_visibility(self, is_visible):
        if is_visible:
            self.show()
        else:
            self.hide()

    def adjust_layout(self):
        self.figure.subplots_adjust(left=0.15, right=1, top=0.95, bottom=0.3)
        self.canvas.draw()