import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

import numpy as np

from PyQt5.QtCore import QTimer,Qt
from BaseGraph import GraphBase
from signal_data import Signal
import sounddevice as sd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog,QSlider


class CineGraph(GraphBase):
    def __init__(self, title="Cine Viewer"):
        super().__init__(title)
        self.signal = None  
        self.current_frame = 0  
        self.playSpeed = 100  
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.is_playing = False
      

    def set_signal(self, signal: Signal):
        # sd.stop()
        self.signal = signal
        self.current_frame = 0  
        self.plot_widget.clear() 

        time_data, amplitude_data = signal.get_waveform_data()
        self.plot_widget.setTitle(self.title)
        self.display_signal(time_data, amplitude_data, color="b")
        self.play()

    def display_signal(self, time_data, amplitude_data, color="b"):
        if self.is_waveform_mode: 
            self.plot_waveform(time_data, amplitude_data, color=color)
        else:
            frequencies, thresholds = self.signal.get_audiogram_data(self.current_frame)
            if frequencies is not None:
                self.plot_audiogram(frequencies, thresholds)

    def update_plot(self):
        if self.signal is None:
            return

        if self.is_waveform_mode: 
            time_data, amplitude_data = self.signal.get_waveform_data(end_frame=self.current_frame)
            self.plot_waveform(time_data, amplitude_data)
        else:
            frequencies, thresholds = self.signal.get_audiogram_data(self.current_frame)
            if frequencies is not None:
                self.plot_audiogram(frequencies, thresholds)

        if self.is_playing:
            self.current_frame += int(self.signal.sample_rate * 0.05)
            if self.current_frame >= len(self.signal.data):
                self.timer.stop()
                self.is_playing = False

    def play(self):
        if not self.is_playing:
            self.timer.start(self.playSpeed)
            self.is_playing = True
            # sd.play(self.signal.data, self.signal.sample_rate, loop=False) 

    def pause(self):
        self.timer.stop()
        self.is_playing = False
        # sd.stop()  
        # self.paused_frame = self.current_frame  

    def reset(self):
        self.current_frame = 0
        self.update_plot()

    def set_play_speed(self, value):
        self.playSpeed = max(10, min(500, 500 - value))
        print(self.playSpeed)
        if self.is_playing:
            self.timer.start(self.playSpeed) 

    def toggle_plot_type(self):
        self.is_waveform_mode = not self.is_waveform_mode
        print(f"Toggling plot type: {'Waveform' if self.is_waveform_mode else 'Audiogram'}")
        self.update_plot()  

    def link_with(self, other):
        self.plot_widget.setXLink(other.plot_widget)
        self.plot_widget.setYLink(other.plot_widget)
        self.linked_graph = other


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    main_window = QMainWindow()
    main_window.setWindowTitle("Signal")
    main_window.resize(800, 600)

    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    cine_graph1 = CineGraph("input")
    # cine_graph2 = CineGraph("output")

    
    # cine_graph1.link_with(cine_graph2) #link input graph with output graph

    layout.addWidget(cine_graph1)
    # layout.addWidget(cine_graph2)

    def load_signal():
        file_path, _ = QFileDialog.getOpenFileName(main_window, "Open Audio File", "", "Audio Files (*.wav *.flac *.ogg)")
        if file_path:
            signal = Signal()
            signal.load_signal(file_path)
            cine_graph1.set_signal(signal)
            # cine_graph2.set_signal(signal)

    load_button = QPushButton("Load Signal")
    load_button.clicked.connect(load_signal)
    layout.addWidget(load_button)

    play_button = QPushButton("Play")
    # play_button.clicked.connect(lambda: (cine_graph1.play(), cine_graph2.play()))  # Using lambda to call play for both
    play_button.clicked.connect(cine_graph1.play)
    layout.addWidget(play_button)

    pause_button = QPushButton("Pause")
    pause_button.clicked.connect(cine_graph1.pause)
    # pause_button.clicked.connect(lambda: (cine_graph1.pause(), cine_graph2.pause()))  # Using lambda to call pause for both
    layout.addWidget(pause_button)

    reset_button = QPushButton("Reset")
    reset_button.clicked.connect(cine_graph1.reset)
    # reset_button.clicked.connect(lambda: (cine_graph1.reset(), cine_graph2.reset()))  # Using lambda to call reset for both
    layout.addWidget(reset_button)

    toggle_button = QPushButton("Toggle Plot Type")
    toggle_button.clicked.connect(cine_graph1.toggle_plot_type)
    # toggle_button.clicked.connect(lambda: (cine_graph1.toggle_plot_type(), cine_graph2.toggle_plot_type()))  # Using lambda to call toggle for both
    layout.addWidget(toggle_button)

    speed_slider = QSlider(Qt.Horizontal)
    speed_slider.setMinimum(10) 
    speed_slider.setMaximum(500) 
    speed_slider.setValue(cine_graph1.playSpeed)  
    speed_slider.valueChanged.connect(cine_graph1.set_play_speed) 
    layout.addWidget(speed_slider)



    # Show the main window
    main_window.show()
    sys.exit(app.exec_())
