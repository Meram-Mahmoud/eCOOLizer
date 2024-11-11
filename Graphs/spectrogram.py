import pyqtgraph as pg
from BaseGraph import GraphBase
import numpy as np



class SpectrogramDisplay(GraphBase):
    def __init__(self):
        self.spectrogram_plot = GraphBase("Spectrogram")
        self.spectrogram_image = pg.ImageItem()
        self.spectrogram_plot.plot_widget.addItem(self.spectrogram_image)
        self.spectrogram_plot.hide()

        colors = [(0, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 0, 0)]
        positions = [0.0, 0.25, 0.5, 0.75, 1.0]
        colormap = pg.ColorMap(positions, colors)
        self.spectrogram_image.setLookupTable(colormap.getLookupTable())

    def display_spectrogram(self, signal, window_size=1024, overlap=512):
        if not signal:
            return
        freqs, times, spectrogram_data = signal.calculate_spectrogram(window_size, overlap)
        spectrogram_db = 20 * np.log10(spectrogram_data + 1e-6)
        self.spectrogram_image.setImage(spectrogram_db, autoLevels=True)

        transform = pg.QtGui.QTransform()
        transform.scale(times[-1] / spectrogram_db.shape[1], freqs[-1] / spectrogram_db.shape[0])
        self.spectrogram_image.setTransform(transform)
        self.spectrogram_plot.plot_widget.setLabel('left', 'Frequency (Hz)')
        self.spectrogram_plot.plot_widget.setLabel('bottom', 'Time (s)')

    def toggle_visibility(self, splitter, is_visible):
        if is_visible:
            splitter.addWidget(self.spectrogram_plot)
            self.spectrogram_plot.show()
        else:
            splitter.widget(1).setParent(None)
            self.spectrogram_plot.hide()
