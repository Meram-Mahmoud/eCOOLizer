import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Main_App')))

import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import numpy as np
from Main_App.mainStyle import mainStyle,logoStyle,audioNameStyle,buttonsGroupStyle,buttonStyle,importButton,sliderStyle,sliderLabelStyle,controlButtonStyle,darkColor, yellowColor


class GraphBase(QWidget):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.layout = QVBoxLayout(self)
        
        self.initializeAttributes()
        self.initializeUI()

    def initializeAttributes(self):
        # print("Attributes")
        self.scale_type = "waveForm"
        self.is_waveform_mode = True

    def initializeUI(self):
        self.createUIElements()
        self.layoutSet()
        self.stylingUI()

    def createUIElements(self):
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLimits(xMin=0)
        
        

    def stylingUI(self):
        
        self.plot_widget.setBackground(darkColor)  
        self.plot_widget.getAxis('left').setPen(yellowColor)  
        self.plot_widget.getAxis('left').setTextPen(yellowColor)
        self.plot_widget.getAxis('bottom').setPen(yellowColor)
        self.plot_widget.getAxis('bottom').setTextPen(yellowColor)

    def layoutSet(self):
        self.layout.addWidget(self.plot_widget)

    def plot_graph(self, time_data, amplitude_data, **kwargs):
        pen = kwargs.get('pen', yellowColor)  
        if isinstance(pen, str):
                pen = pg.mkPen(pen)
        elif isinstance(pen, pg.mkPen):  
            pen = pen
        else:
            pen = pg.mkPen(yellowColor)  

        self.plot_widget.clear()
        
        self.plot_widget.plot(time_data, amplitude_data, pen=pen)
 

    def clear(self):
        self.plot_widget.clear()

   