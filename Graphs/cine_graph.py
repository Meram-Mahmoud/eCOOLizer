import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Graphs')))

import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QTimer,Qt
from BaseGraph import GraphBase
from signal_data import Signal
import sounddevice as sd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog,QSlider,QSplitter
from spectrogram import SpectrogramDisplay

class CineGraph(GraphBase):
    def __init__(self, title="Cine Viewer"):
        super().__init__(title)
        self.signal = None  
        self.current_frame = 0  
        self.playSpeed = 100  
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.is_playing = False
        self.linked_graph = None

        self.spectrogram_visible = False
        self.splitter = QSplitter(Qt.Horizontal)
        self.spectrogram_display = SpectrogramDisplay(self.splitter)

        self.splitter.addWidget(self) 
        self.splitter.addWidget(self.spectrogram_display) 
        self.spectrogram_display.setVisible(False)

        self.splitter.setStretchFactor(0, 3) 
        print("graph")
        print("graph")

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
        #Updates the graph with the current frame of the signal.
        if self.signal is None:
            return

        # time_data, amplitude_data = self.signal.get_data(end_frame=self.current_frame)
        time_data, amplitude_data = self.signal.get_time_domain_data(end_frame=self.current_frame)

        self.plot_graph(time_data, amplitude_data)

        # Adjust the window to show the last 1 second of the signal
        window_duration = 1  
        end_time = time_data[-1] if len(time_data) > 0 else 0
        start_time = max(0, end_time - window_duration)

        self.plot_widget.setXRange(start_time, end_time)

        if self.is_playing:
            self.current_frame += int(self.signal.sample_rate * 0.05)
            if self.current_frame >= len(self.signal.data):
                self.timer.stop()
                self.is_playing = False

    

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
        
        self.current_frame = 0
        self.is_playing = True
        self.update_plot()
        
        
        # sd.play(self.signal.data, self.signal.sample_rate, loop=False) 
       
    def set_play_speed(self, value):
        self.playSpeed = max(50, min(500, 500 - value))
        # self.playSpeed=value
        if self.is_playing:
            self.timer.start(self.playSpeed) 

    def link_with(self, other):
        self.plot_widget.setXLink(other.plot_widget)
        # self.plot_widget.setYLink(other.plot_widget)
        self.linked_graph = other
        other.linked_graph = self
        other.current_frame = self.current_frame
        self.current_frame=other.current_frame
       
     # def update_plot(self):
    #     if self.signal is None or not self.is_playing:
    #         return

    #     elapsed_seconds = self.total_elapsed_time
    #     if self.elapsed_timer.isValid():
    #         elapsed_seconds += self.elapsed_timer.elapsed() / 1000.0 

    #     target_frame = int(elapsed_seconds * self.signal.sample_rate)

    #     if target_frame > len(self.signal.data):
    #         self.timer.stop()
    #         self.is_playing = False
    #         return

    #     time_data, amplitude_data = self.signal.get_data(end_frame=target_frame)
    #     self.plot_graph(time_data, amplitude_data, pen='b')
    #     self.current_frame = target_frame  

    # def play(self):
    #     if not self.is_playing:
    #         if not self.elapsed_timer.isValid():  
    #             self.elapsed_timer.start()
    #         else:
    #             self.elapsed_timer.restart() 

    #         sd.play(self.signal.data[self.current_frame:], self.signal.sample_rate, loop=False)
            
    #         self.timer.start(self.playSpeed)
    #         self.is_playing = True

    # def pause(self):
    #     if self.is_playing:
    #         self.total_elapsed_time += self.elapsed_timer.elapsed() / 1000.0  
    #         self.elapsed_timer.invalidate() 
            
    #         sd.stop()
    #         self.timer.stop()
    #         self.is_playing = False


    # def reset(self):
    #     sd.stop()
    #     self.timer.stop()
    #     self.is_playing = False

    #     self.current_frame = 0
    #     self.total_elapsed_time = 0
    #     self.elapsed_timer.invalidate() 

    #     self.clear()  
    #     self.update_plot()

    #     self.play()


   


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