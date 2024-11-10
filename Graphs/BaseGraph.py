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

    def plot_graph(self, time_data, amplitude_data, **kwargs):
        pen = kwargs.get('pen', 'b')  
        if isinstance(pen, str):
            pen = pg.mkPen(pen)
        self.plot_widget.clear()
        self.plot_widget.plot(time_data, amplitude_data, **kwargs)


    def clear(self):
        self.plot_widget.clear()

    def limit_x_axis(self):
        current_range = self.plot_widget.getViewBox().state['viewRange']
        x_range = current_range[0] 
        if x_range[0] < 0:
            self.plot_widget.setXRange(0, x_range[1], padding=0)

   