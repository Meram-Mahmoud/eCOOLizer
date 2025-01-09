import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Graphs')))

import numpy as np
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDesktopWidget, QVBoxLayout, QWidget, QSlider,QFileDialog,QRadioButton, QButtonGroup, \
    QPushButton, QHBoxLayout,QSplitter
from PyQt5.uic.properties import QtCore
from pyqtgraph import PlotWidget, mkPen
from wiener_slider import WienerSlider

from mainStyle import mainStyle,logoStyle,audioNameStyle,buttonsGroupStyle,buttonStyle,importButton,sliderStyle,sliderLabelStyle,controlButtonStyle,speedSliderStyle,radioButtonStyle,splitterStyle
from mainStyle import darkColor, yellowColor
from Graphs.BaseGraph import GraphBase
from Graphs.cine_graph import CineGraph 
from Graphs.fourier_graph import FourierTransformGraph
from signal_data import Signal
from sliders import Slider
from Graphs.spectrogram import SpectrogramDisplay
from wiener import Wiener

class eCOOLizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eCOOLizer")
        self.setGeometry(100, 100, 1000, 700)
        
        
        self.mainLayout = QVBoxLayout()
        self.createSpectrograms()
        self.initialize()
        self.createUI()
        # self.plotDummyData()

    def centerWindow(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def initialize(self):
        self.is_playing = True
        self.audio_playing=False
        self.currentMode = QPushButton()
        self.sliderPanel = None
        self.signal_input = Signal()
        self.signal_output = Signal()
        print("initialized")

    def createUI(self):
        self.createUIElements()
        self.setUI()
        self.connectUI()
        self.makeLayout()
        self.stylingUI()
        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)
        self.centerWindow()

    def createUIElements(self):
        self.eCOOLizerLogo = QLabel("ECOOLIZER |")
        self.audioLoadedName = QLabel("Need AudioName.mp3")
        self.uploadButton = QPushButton("Upload")

        self.playPauseButton = QPushButton(QIcon("Main_App/Assets/play.png"), "")
        self.resetButton = QPushButton(QIcon("Main_App/Assets/reset.png"), "")
       
        self.toggleSpectogram=QPushButton("Spectogram")
        self.toggleAudiogram=QPushButton("audigram")

        self.originalModeRadio = QRadioButton("Original")
        self.modifiedModeRadio = QRadioButton("Modified")
        self.originalModeRadio.setChecked(True)
        # self.playAudio = QPushButton(QIcon("Main_App/Assets/pause audio.png"), "")
        self.playAudio = QPushButton(QIcon("Main_App/Assets/play audio.png"), "")

        # self.inputGraph = PlotWidget()
        self.inputGraph = CineGraph("Input Graph")
        # self.outputGraph = PlotWidget()
        self.outputGraph = CineGraph("Output Graph")

        self.inputGraph.link_with(self.outputGraph)

        self.speedSlider = QSlider(Qt.Horizontal)
        self.speedSlider.setRange(50, 500) 
        self.speedSlider.setValue(self.inputGraph.playSpeed)

        # self.fourierGraph = PlotWidget()
        self.fourierGraph=FourierTransformGraph("Fourier Graph")

        self.buttonsGroup = QWidget()
        self.defaultModeButton = QPushButton(QIcon("Main_App/Assets/DefaultSelected.png"),"")
        self.weinerModeButton = QPushButton(QIcon("Main_App/Assets/weiner.png"),"")
        self.animalModeButton = QPushButton(QIcon("Main_App/Assets/Animal.png"),"")
        self.vowelsModeButton = QPushButton(QIcon("Main_App/Assets/Music.png"),"")

        self.sliderPanel = self.createSliderPanel("default")
        # print("UI elements Created")

    # TESTING FUNCTION
    def updateSliderPanel(self, mode = "default"):
        if self.sliderPanel:
            self.sliderPanel.deleteLater()
            
        #NEED MODE CHECK
        self.sliderPanel = self.createSliderPanel(mode)

        sliderPanelLayout = QHBoxLayout()
        sliderPanelLayout.addWidget(self.sliderPanel)

        workspaceLayout = self.mainLayout.itemAt(1)  
        if workspaceLayout:
            workspaceLayout.itemAt(1).addLayout(sliderPanelLayout)

    def contorls(self, names, ranges, const=100):
        sliderPanelLayout = QHBoxLayout() 
        sliderPanelLayout.setAlignment(Qt.AlignCenter) 
        sliderPanelLayout.setSpacing(20)

        for name, slider_range in zip(names, ranges):
            slider = Slider(label=name)
            slider.set_freq(slider_range)
            slider.set_signal(self.signal_output.get_fft_data())
            slider.set_old_magnitudes(self.signal_input.get_fft_data()[1])
            slider.set_constant(const)
            slider.samping_rate = self.signal_output.sample_rate
            slider.newSignalAndFourier.connect(self.handleSliderChange)
            sliderPanelLayout.addWidget(slider)

        # Create a QWidget to hold the slider panel layout and return it
        sliderPanelWidget = QWidget()
        sliderPanelWidget.setLayout(sliderPanelLayout)

        return sliderPanelWidget

    def createSliderPanel(self, mode = "default"):    
        if mode == "default":  
            names, ranges = [], []  
            for ind in range(1,11):
                center_frequency = ind * 100 + 1000  
                names.append(f"{center_frequency} HZ")  
                ranges.append([[center_frequency - 10, center_frequency + 10]])
            return self.contorls(names, ranges, 10000)

        elif mode == "animal":
            #animals only
            # names = ["Dog", "Wolve", "Crow", "Bat"]
            # ranges = [[[0, 450]], [[450, 1100]], [[1100, 3000]], [[3000, 9000]]]
            # return self.contorls(names, ranges, 1000)

            #animals+instruments
            names = ["owl", "frog", "cricket", "sax","chimes"]
            ranges = [[[100, 600]], [[601, 2500]], [[3000, 4600]],[[4600,8000]], [[8000, 160000]]]
            return self.contorls(names, ranges, 500)
      

        elif mode == "wiener":
            freq_range = self.inputGraph.get_selected_frequency_range()
        
            if freq_range:
                freq_min, freq_max = freq_range
                names = [f"Region {freq_min}-{freq_max}Hz"]
                ranges = [[[freq_min, freq_max]]]
            else:
                names = ["Noise"]
                ranges = [[[0, self.signal_input.sample_rate // 2]]]
            
            return self.contorls(names, ranges, 30)

           

        elif mode == "vowels":
            
              # royal test FINAL 
            names = ["s","sh","Triangle","Drums","Clap"]  
            ranges = [[[3500, 12000]],[[2500,6400]],[[12000,20000]],[[100, 600]],[[1200, 3000]]]
            return self.contorls(names, ranges, 30000)
        

             #unchain my heart test both 2 song 700-2000 best one so far
            # names = ["ch","a","bass","drums"]  
            # ranges = [[[1, 700],[1800,6000]],[[400,800]],[[50,200]],[[400,1000]]]
            # return self.contorls(names, ranges, 10000)

            #instruments only
            # names = ["Triangle", "Drum"]
            # ranges = [[[3000, 15000]], [[0, 12000]]]
            # return self.contorls(names, ranges, 3900)

            # names = ["Guitar", "Flute", "xylophone", "Harmonica"]
            # ranges = [[[0, 250]], [[170, 400]], [[3000,23000]], [[400, 4000]]]


        
         
    def enable_weiner_mode(self):
        self.inputGraph.set_weiner_mode(True)
        self.inputGraph.regionChanged.connect(self.handle_region_change)

    def handle_region_change(self, min_x, max_x):
        print(f"Selected region: {min_x:.2f} to {max_x:.2f}")

    def createSpectrograms(self):
        self.inputSpectrogram = SpectrogramDisplay()
        self.outputSpectrogram = SpectrogramDisplay()
        self.inputSpectrogram.hide()
        self.outputSpectrogram.hide()

    def setUI(self):
        self.currentMode = self.defaultModeButton
        # print("UI setting Done")

    def connectUI(self):
        self.playPauseButton.clicked.connect(self.togglePlayPause)
        self.resetButton.clicked.connect(self.Reset)
        self.defaultModeButton.clicked.connect(self.changeMode)
        self.weinerModeButton.clicked.connect(self.changeMode)
        self.animalModeButton.clicked.connect(self.changeMode)
        self.vowelsModeButton.clicked.connect(self.changeMode)
        self.uploadButton.clicked.connect(self.load_signal)
        self.speedSlider.valueChanged.connect(self.changePlottingSpeed)
        self.playAudio.clicked.connect(self.toggle_audio_playback)
        self.originalModeRadio.toggled.connect(self.switch_mode)
        self.toggleSpectogram.clicked.connect(self.hideShowSpectogram)
        self.toggleAudiogram.clicked.connect(self.toggleScale)

        # print("UI Connected")

    def stylingUI(self):
        self.setStyleSheet(mainStyle)
        self.eCOOLizerLogo.setStyleSheet(logoStyle)
        self.audioLoadedName.setStyleSheet(audioNameStyle)
        self.audioLoadedName.setContentsMargins(10,0,10,0)
        self.uploadButton.setStyleSheet(importButton)

        self.toggleSpectogram.setStyleSheet(importButton)
        self.toggleAudiogram.setStyleSheet(importButton)

        self.inputSplitter.setStyleSheet(splitterStyle)
        self.outputSplitter.setStyleSheet(splitterStyle)


        self.playPauseButton.setStyleSheet(controlButtonStyle)
        self.playPauseButton.setIconSize(QSize(25, 25))
        self.resetButton.setStyleSheet(controlButtonStyle)
        self.resetButton.setIconSize(QSize(25, 25))
        self.playAudio.setStyleSheet(controlButtonStyle)
        self.playAudio.setIconSize(QSize(25, 25))

        self.speedSlider.setStyleSheet(speedSliderStyle)
        self.speedSlider.setFixedWidth(250)
        self.originalModeRadio.setStyleSheet(radioButtonStyle)
        self.modifiedModeRadio.setStyleSheet(radioButtonStyle)

        buttonSize = 25
        self.defaultModeButton.setIconSize(QSize(int(buttonSize*1.5), int(buttonSize*1.5)))
        self.defaultModeButton.setStyleSheet(buttonStyle)

        self.animalModeButton.setIconSize(QSize(buttonSize, buttonSize))
        self.animalModeButton.setStyleSheet(buttonStyle)

        self.weinerModeButton.setIconSize(QSize(buttonSize, buttonSize))
        self.weinerModeButton.setStyleSheet(buttonStyle)

        self.vowelsModeButton.setIconSize(QSize(buttonSize, buttonSize))
        self.vowelsModeButton.setStyleSheet(buttonStyle)

        self.buttonsGroup.setStyleSheet(buttonsGroupStyle)
        self.buttonsGroup.setContentsMargins(10,0,10,0)
    # print("UI is Styled")

    def changeMode(self):
        button = self.sender()
        if button != self.currentMode:
            match button:
                case self.defaultModeButton:
                    button.setIcon(QIcon("Main_App/Assets/DefaultSelected.png"))
                    self.updateSliderPanel("default")  
                    self.inputGraph.set_weiner_mode(False)
                case self.weinerModeButton:
                    button.setIcon(QIcon("Main_App/Assets/weinerSelected.png"))
                    self.updateSliderPanel("wiener") 
                    self.inputGraph.set_weiner_mode(True) 
                case self.animalModeButton:
                    button.setIcon(QIcon("Main_App/Assets/AnimalSelected.png"))
                    self.updateSliderPanel("animal")
                    self.inputGraph.set_weiner_mode(False)  
                case self.vowelsModeButton:
                    button.setIcon(QIcon("Main_App/Assets/MusicSelected.png"))
                    self.updateSliderPanel("vowels")  
                    self.inputGraph.set_weiner_mode(False)

            match self.currentMode:
                case self.defaultModeButton:
                    self.currentMode.setIcon(QIcon("Main_App/Assets/Default.png"))
                case self.weinerModeButton:
                    self.currentMode.setIcon(QIcon("Main_App/Assets/weiner.png"))
                case self.animalModeButton:
                    self.currentMode.setIcon(QIcon("Main_App/Assets/Animal.png"))
                case self.vowelsModeButton:
                    self.currentMode.setIcon(QIcon("Main_App/Assets/Music.png"))

            self.currentMode.setIconSize(button.sizeHint())
            button.setIconSize(button.sizeHint() * 1.5)
            self.currentMode = button

    def makeLayout(self):
        topBar = QHBoxLayout()
        topBar.addWidget(self.eCOOLizerLogo)
        topBar.addWidget(self.audioLoadedName)
        topBar.addWidget(self.uploadButton)
        topBar.addSpacing(20)
        topBar.addWidget(self.playPauseButton)
        topBar.addWidget(self.resetButton)
        topBar.addWidget(self.speedSlider)
        topBar.addWidget(self.toggleSpectogram)
        topBar.addWidget(self.toggleAudiogram)
        topBar.addSpacing(30)

        topBar.addWidget(self.playAudio)
        topBar.addWidget(self.originalModeRadio)
        topBar.addWidget(self.modifiedModeRadio)
        topBar.addStretch()

        workspace = QVBoxLayout()

        graphsLayout = QVBoxLayout()

        # Input Splitter
        self.inputSplitter = QSplitter(Qt.Horizontal)
        inputGraphWidget = QWidget()
        inputGraphLayout = QVBoxLayout()
        inputGraphLayout.addWidget(self.inputGraph)
        inputGraphWidget.setLayout(inputGraphLayout)

        inputSpectrogramWidget = QWidget()
        inputSpectrogramLayout = QVBoxLayout()
        inputSpectrogramLayout.addWidget(self.inputSpectrogram)
        inputSpectrogramWidget.setLayout(inputSpectrogramLayout)

        self.inputSplitter.addWidget(inputGraphWidget)
        self.inputSplitter.addWidget(inputSpectrogramWidget)
        self.inputSplitter.setSizes([700, 0])  # Adjust sizes to make both visible

        # Output Splitter
        self.outputSplitter = QSplitter(Qt.Horizontal)
        outputGraphWidget = QWidget()
        outputGraphLayout = QVBoxLayout()
        outputGraphLayout.addWidget(self.outputGraph)
        outputGraphWidget.setLayout(outputGraphLayout)

        outputSpectrogramWidget = QWidget()
        outputSpectrogramLayout = QVBoxLayout()
        outputSpectrogramLayout.addWidget(self.outputSpectrogram)
        outputSpectrogramWidget.setLayout(outputSpectrogramLayout)

        self.outputSplitter.addWidget(outputGraphWidget)
        self.outputSplitter.addWidget(outputSpectrogramWidget)
        self.outputSplitter.setSizes([700, 0])  # Adjust sizes to make both visible

        # Add components to graphsLayout
        graphsLayout.addWidget(self.inputSplitter)  # Add the entire input splitter
        graphsLayout.addWidget(self.outputSplitter)  # Add the entire output splitter
        graphsLayout.addWidget(self.fourierGraph)  # Add the Fourier graph

        # Modes row layout
        modesRowLayout = QHBoxLayout()
        modesLayout = QHBoxLayout(self.buttonsGroup)
        modesLayout.addWidget(self.defaultModeButton)
        modesLayout.addWidget(self.animalModeButton)
        modesLayout.addWidget(self.weinerModeButton)
        modesLayout.addWidget(self.vowelsModeButton)

        modesRowLayout.addStretch(20)
        modesRowLayout.addWidget(self.buttonsGroup, 20)
        modesRowLayout.addStretch(20)

        # Sliders panel layout
        slidersPanelLayout = QHBoxLayout()
        slidersPanelLayout.addWidget(self.sliderPanel)

        # Add all layouts to workspace
        workspace.addLayout(graphsLayout, 60)
        workspace.addLayout(slidersPanelLayout, 20)
        workspace.addLayout(modesRowLayout, 5)

        # Set top bar margins and add layouts to main layout
        topBar.setContentsMargins(0, 5, 0, 5)
        self.mainLayout.addLayout(topBar, 20)
        self.mainLayout.addLayout(workspace, 90)

    def load_signal(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.wav *.flac *.ogg *.csv)")
        if file_path:
            file_extension = os.path.splitext(file_path)[-1].lower()  # Get the file extension in lowercase
            if file_extension == '.csv':
                self.signal_input.load_signal_from_csv(file_path)
                self.signal_output.load_signal_from_csv(file_path)
                file_name = os.path.basename(file_path)
                self.audioLoadedName.setText(f"{file_name}")

                self.inputGraph.set_signal(self.signal_input)
                self.outputGraph.set_signal(self.signal_output)

                self.inputGraph.clear()
                self.outputGraph.clear()
                self.inputGraph.timer.start(self.inputGraph.playSpeed)
                self.inputSpectrogram.display_spectrogram(self.signal_input)
                self.outputSpectrogram.display_spectrogram(self.signal_output)

                self.fourierGraph.set_signal(self.signal_output)
                print("ALLO mel main class (loading csv)")
            else:
                # self.signal = Signal()
                self.signal_input.load_signal(file_path)
                self.signal_output.load_signal(file_path)
                file_name = os.path.basename(file_path)
                self.audioLoadedName.setText(f"{file_name}")

                self.inputGraph.set_signal(self.signal_input)
                self.outputGraph.set_signal(self.signal_output)

                self.inputGraph.clear()
                self.outputGraph.clear()
                self.inputGraph.timer.start(self.inputGraph.playSpeed)

                self.fourierGraph.set_signal(self.signal_output)

                self.inputSpectrogram.display_spectrogram(self.signal_input)
                self.outputSpectrogram.display_spectrogram(self.signal_output)
        
    def togglePlayPause(self):
        if self.is_playing:
            self.playPauseButton.setIcon(QIcon("Main_App/Assets/pause.png"))
            self.is_playing = False
            print("Playback paused") 
            
            self.inputGraph.pause()
            self.outputGraph.pause()

        else:
            self.playPauseButton.setIcon(QIcon("Main_App/Assets/play.png"))
            self.is_playing = True
            print("Playback started")
            
            self.inputGraph.play()
            self.outputGraph.play()

    def Reset(self):
        self.inputGraph.reset()
        self.outputGraph.reset()

    def changePlottingSpeed(self):
        speed = self.speedSlider.value()
        self.inputGraph.set_play_speed(speed)
        self.outputGraph.set_play_speed(speed)

    def toggle_audio_playback(self):
            if self.originalModeRadio.isChecked():
                signal = self.signal_input
                print("Toggling audio for: Original")
            elif self.modifiedModeRadio.isChecked():
                signal = self.signal_output
                print("Toggling audio for: Modified")
            else:
                print("No mode selected for audio playback.")
                return

            if signal is not None:
                signal.play_audio() 
                if not self.audio_playing:
                    # self.playAudio.setIcon(QIcon("Main_App/Assets/play audio.png"))  
                    self.audio_playing = True
                else:
                    # self.playAudio.setIcon(QIcon("Main_App/Assets/pause audio.png"))  
                    self.audio_playing = False
            else:
                print("No audio signal loaded.")

    def switch_mode(self):
        if self.audio_playing:
            self.toggle_audio_playback()  
            self.toggle_audio_playback()  
            print("Switched audio mode during playback.")
    
    def handleSliderChange(self, newSignal):
        self.signal_output.set_data(newSignal)
        self.outputGraph.set_signal(self.signal_output)
        self.fourierGraph.set_signal(self.signal_output)

        self.inputGraph.set_signal(self.signal_input)
        self.outputGraph.timer.start(self.outputGraph.playSpeed)
        self.outputSpectrogram.display_spectrogram(self.signal_output)
        self.outputSpectrogram.repaint()
        self.outputSpectrogram.adjust_layout()
        self.switch_mode()

    
    def hideShowSpectogram(self):
        is_visible = not self.inputSpectrogram.isVisible()
        self.inputSpectrogram.toggle_visibility(is_visible)
        self.outputSpectrogram.toggle_visibility(is_visible)

        self.inputSplitter.setSizes([700, 0] if not is_visible else [500, 300])

        self.outputSplitter.setSizes([700, 0] if not is_visible else [500, 300])

    def toggleScale(self):
        self.fourierGraph.toggle_audiogram_mode()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = eCOOLizer()
    mainWindow.show()
    sys.exit(app.exec_())
