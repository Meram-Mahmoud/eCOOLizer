from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from Main_App.mainStyle import sliderStyle, sliderLabelStyle

class WienerSlider(QWidget):
    newSignalAndFourier = pyqtSignal(object)
    
    def __init__(self, wiener_filter):
        super().__init__()
        self.wiener = wiener_filter
        
        layout = QVBoxLayout()
        
        # Create slider for noise reduction control
        self.slider = QSlider(Qt.Vertical)
        self.slider.setMinimum(0)
        self.slider.setMaximum(200)  # 0 to 2.0 with 100 steps
        self.slider.setValue(100)  # Default value 1.0
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(20)
        self.slider.setStyleSheet(sliderStyle)
        
        # Connect slider to value change handler
        self.slider.valueChanged.connect(self.handle_slider_change)
        
        # Create label
        self.label = QLabel("Noise Reduction")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(sliderLabelStyle)
        
        # Add widgets to layout
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        
        self.setLayout(layout)

    def handle_slider_change(self, value):
        # Convert slider value to factor (0-2 range)
        factor = value / 100.0
        # Get filtered signal in frequency domain
        self.wiener.set_noise_reduction(factor)
        filtered_signal = self.wiener.get_filtered_signal()
        self.newSignalAndFourier.emit(filtered_signal)