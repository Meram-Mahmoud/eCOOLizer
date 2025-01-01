import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Graphs')))

import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QTimer,Qt
from .BaseGraph import GraphBase
from signal_data import Signal
import sounddevice as sd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog,QSlider,QSplitter
from .spectrogram import SpectrogramDisplay
from PyQt5.QtCore import pyqtSignal

class CineGraph(GraphBase):
    regionChanged = pyqtSignal(float, float)
    def __init__(self, title="Cine Viewer"):
        super().__init__(title)
        self.signal = None  
        self.current_frame = 0  
        self.playSpeed = 100  
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.is_playing = False
        self.linked_graph = None
        self.wiener_mode = False
        self.selected_region = None
        self.selected_signal_data = []

        self.spectrogram_visible = False
        self.splitter = QSplitter(Qt.Horizontal)
        self.spectrogram_display = SpectrogramDisplay(self.splitter)

        self.splitter.addWidget(self) 
        self.splitter.addWidget(self.spectrogram_display) 
        self.spectrogram_display.setVisible(False)

        self.splitter.setStretchFactor(0, 3) 
        self.plot_widget.scene().sigMouseClicked.connect(self.mouseClickEvent)
       

    def set_signal(self, signal: Signal):
        # Inputs: signal (object)
        # then clears the current graph and plots the new signal
        self.clear()
        self.signal = signal
        self.current_frame = 0  
        time_data, amplitude_data = signal.get_time_domain_data()
        self.plot_widget.setTitle(self.title)
        self.display_signal(time_data, amplitude_data) 
        self.play()

        if self.spectrogram_visible:
            self.spectrogram_display.display_spectrogram(self.signal)


    def display_signal(self, time_data, amplitude_data):
        # Inputs:
        #time_data (numpy array): Time values, Shape: (number of samples,)
        #amplitude_data (numpy array): Amplitude values of the signal, Shape: (number of samples,)
    
        # then it Plots the time-amplitude signal on the graph.
        self.plot_graph(time_data, amplitude_data)

    def toggle_spectrogram(self):
        self.spectrogram_visible = not self.spectrogram_visible
        self.spectrogram_display.toggle_visibility(self.spectrogram_visible)

        if self.spectrogram_visible:
            self.spectrogram_display.display_spectrogram(self.signal)
            self.spectrogram_display.setMinimumSize(100, 100) 
            self.splitter.setSizes([max(200, 500), max(200, 500)])
        else:
            self.splitter.setSizes([max(200, 200), 0])
        
        self.spectrogram_display.updateGeometry()
        self.splitter.updateGeometry()

    def update_plot(self):
        # Updates the graph with the current frame of the signal.
        if self.signal is None:
            return

        # Get the time-domain data for the current frame
        time_data, amplitude_data = self.signal.get_time_domain_data(end_frame=self.current_frame)

        # Plot the data
        self.plot_graph(time_data, amplitude_data)
        # print(f"Amplitude data: {amplitude_data[:10]}")  # Show first 10 data points
        # print(f"Min amplitude: {min(amplitude_data)}, Max amplitude: {max(amplitude_data)}")

        # Adjust the window to show the last 1 second of the signal
        window_duration = 1  # Display the last second of data
        end_time = time_data[-1] if len(time_data) > 0 else 0
        start_time = max(0, end_time - window_duration)

        # Set the X range (time axis)
        self.plot_widget.setXRange(start_time, end_time)

        # Update the Y range dynamically based on the amplitude data
        y_min, y_max = min(amplitude_data), max(amplitude_data)
        padding = (y_max - y_min) * 0.1  # Add some padding to the y-range
        y_min -= padding
        y_max += padding

        # Set the Y range (amplitude axis)
        self.plot_widget.setYRange(y_min, y_max)

        # Update the current frame for the next iteration
        if self.is_playing:
            self.current_frame += int(self.signal.sample_rate * 0.05)  # Increment frame by 50 ms
            if self.current_frame >= len(self.signal.data):
                self.timer.stop()
                self.is_playing = False
        if self.wiener_mode and self.selected_region:
                self.plot_widget.addItem(self.selected_region)


    # def play(self):
    #     if not self.is_playing:
    #         # sd.play(self.signal.data[self.current_frame:], self.signal.sample_rate, loop=False)
    #         self.timer.start(self.playSpeed)
    #         self.is_playing = True

    # def pause(self):
    #     if self.is_playing:
    #         # sd.stop()  
    #         self.timer.stop() 
    #         self.is_playing = False  

    def play(self):
        self.is_playing = True
            # sd.play(self.signal.data[self.current_frame:], self.signal.sample_rate, loop=False)
        self.timer.start(self.playSpeed)

    def pause(self):
        self.is_playing = False
        self.timer.stop()  

    def reset(self):
        # sd.stop()
        self.is_playing = True
        self.current_frame = 0
        
        self.update_plot()
        
        
        # sd.play(self.signal.data, self.signal.sample_rate, loop=False) 
       
    def set_play_speed(self, value):
        self.playSpeed = max(50, min(500, 500 - value))
        # self.playSpeed=value
        if self.is_playing:
            self.timer.start(self.playSpeed) 

    def link_with(self, other):
        self.plot_widget.setXLink(other.plot_widget)
        self.plot_widget.setYLink(other.plot_widget)
        self.linked_graph = other
        other.linked_graph = self
        other.current_frame = self.current_frame
        self.current_frame=other.current_frame
       
    def set_weiner_mode(self, enabled):
        self.wiener_mode = enabled
        if not enabled and self.selected_region:
            self.plot_widget.removeItem(self.selected_region)
            self.selected_region = None
            self.selected_signal_data = []
    
    def mouseClickEvent(self, event):
        if self.wiener_mode and self.plot_widget.sceneBoundingRect().contains(event.scenePos()):
            pass

    def mouseDoubleClickEvent(self, event):
        if self.wiener_mode:
            scene_pos = self.plot_widget.mapToScene(event.pos())
            if self.plot_widget.sceneBoundingRect().contains(scene_pos):
                if self.selected_region is None:
                    self.region_rectangle()
                else:
                    self.plot_widget.removeItem(self.selected_region)
                    self.selected_region = None
                    self.region_rectangle()

    def region_rectangle(self):
    
        view_range = self.plot_widget.viewRange()[0]
        
        initial_min = view_range[0] + (view_range[1] - view_range[0]) * 0.25
        initial_max = view_range[0] + (view_range[1] - view_range[0]) * 0.75
        
        self.selected_region = pg.LinearRegionItem(
            values=[initial_min, initial_max],
            movable=True,
            bounds=view_range,
            brush=pg.mkBrush(color=(100, 100, 255, 50))  
        )
        
        self.selected_region.sigRegionChangeFinished.connect(self.handle_region_change)
        
        self.plot_widget.addItem(self.selected_region)
    
    def handle_region_change(self):
    
        time_min, time_max = self.selected_region.getRegion()
    
        if self.signal:
            freq_resolution = self.signal.sample_rate / len(self.signal.data)
            
            freq_min = int(1 / time_max)  
            freq_max = int(1 / time_min)  
            
            nyquist = self.signal.sample_rate // 2
            freq_min = max(0, min(freq_min, nyquist))
            freq_max = max(0, min(freq_max, nyquist))
            
            freq_range = self.get_selected_frequency_range()

            if hasattr(self, 'regionChanged') and freq_range:
                self.regionChanged.emit(*freq_range)
            
        return [freq_min, freq_max]
    
    def get_selected_frequency_range(self):
        if self.wiener_mode and self.selected_region:
            return self.handle_region_change()
        return None
    
    def get_selected_data(self):
        return self.selected_signal_data
    
    def get_visible_frame(self):
        if self.signal is None:
            return [], []
        
        x_range = self.plot_widget.viewRange()[0]
        start_time, end_time = x_range
        
        start_frame = max(0, int(start_time * self.signal.sample_rate))
        end_frame = min(len(self.signal.data), int(end_time * self.signal.sample_rate))
        
        time_data = np.arange(start_frame, end_frame) / self.signal.sample_rate
        amplitude_data = self.signal.data[start_frame:end_frame]
        
        return [time_data], [amplitude_data]  
    
   


#test 
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = QMainWindow()
    main_window.setWindowTitle("Signal Visualization")
    main_window.resize(1000, 600)

    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    cine_graph1 = CineGraph("Input Signal")
    cine_graph2 = CineGraph("Output Signal")
    cine_graph1.link_with(cine_graph2)

    layout.addWidget(cine_graph1.splitter)
    layout.addWidget(cine_graph2.splitter)

    def load_signal():
        file_path, _ = QFileDialog.getOpenFileName(main_window, "Open Audio File", "", "Audio Files (*.wav *.flac *.ogg)")
        if file_path:
            signal = Signal()
            signal.load_signal(file_path)

            cine_graph1.set_signal(signal)
            cine_graph2.set_signal(signal)

            cine_graph1.clear()
            cine_graph2.clear()
            cine_graph1.timer.start(cine_graph1.playSpeed)

    load_button = QPushButton("Load Signal")
    load_button.clicked.connect(load_signal)
    layout.addWidget(load_button)

    # Play/Pause/Reset buttons
    play_button = QPushButton("Play")
    play_button.clicked.connect(lambda: (cine_graph1.play(), cine_graph2.play()))
    layout.addWidget(play_button)

    pause_button = QPushButton("Pause")
    pause_button.clicked.connect(lambda: (cine_graph1.pause(), cine_graph2.pause()))
    layout.addWidget(pause_button)

    reset_button = QPushButton("Reset")
    reset_button.clicked.connect(lambda: (cine_graph1.reset(), cine_graph2.reset()))
    layout.addWidget(reset_button)

    # Toggle Spectrogram button
    toggle_spectrogram_button = QPushButton("Toggle Spectrogram")
    toggle_spectrogram_button.clicked.connect(lambda: (cine_graph1.toggle_spectrogram(), cine_graph2.toggle_spectrogram()))
    layout.addWidget(toggle_spectrogram_button)

    # Playback Speed Slider
    speed_slider = QSlider(Qt.Horizontal)
    speed_slider.setMinimum(50)
    speed_slider.setMaximum(500)
    speed_slider.setValue(cine_graph1.playSpeed)
    speed_slider.valueChanged.connect(lambda value: (cine_graph1.set_play_speed(value), cine_graph2.set_play_speed(value)))
    layout.addWidget(speed_slider)

    main_window.show()
    sys.exit(app.exec_())