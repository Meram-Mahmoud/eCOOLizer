import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import numpy as np

class GraphBase(QWidget):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.layout = QVBoxLayout(self)
        
        self.initializeAttributes()
        self.initializeUI()

    def initializeAttributes(self):
        print("Attributes")
        self.scale_type = "waveForm"
        self.is_waveform_mode = True

    def initializeUI(self):
        self.createUIElements()
        self.layoutSet()
        self.stylingUI()

    def createUIElements(self):
        self.plot_widget = pg.PlotWidget()

    def stylingUI(self):
        self.plot_widget.setBackground("black")

    def layoutSet(self):
        self.layout.addWidget(self.plot_widget)

    def plot_waveform(self, time_data, amplitude_data, color='b'):
        self.plot_widget.clear()
        self.plot_widget.plot(time_data, amplitude_data, pen=color)
        # self.limit_x_axis()

    def plot_audiogram(self, frequencies, thresholds):
        self.plot_widget.clear()
        self.plot_widget.setLabel('left', 'Threshold (dB)')
        self.plot_widget.setLabel('bottom', 'Frequency (Hz)')
        self.plot_widget.plot(frequencies, thresholds, pen='r', symbol='o', symbolBrush='r')
        # self.limit_x_axis()

    def clear(self):
        self.plot_widget.clear()

    def limit_x_axis(self):
        current_range = self.plot_widget.getViewBox().state['viewRange']
        x_range = current_range[0] 
        if x_range[0] < 0:
            self.plot_widget.setXRange(0, x_range[1], padding=0)

   