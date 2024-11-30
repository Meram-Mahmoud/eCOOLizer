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

from mainStyle import mainStyle,logoStyle,audioNameStyle,buttonsGroupStyle,buttonStyle,importButton,sliderStyle,sliderLabelStyle,controlButtonStyle,speedSliderStyle,radioButtonStyle
from mainStyle import darkColor, yellowColor
from Graphs.BaseGraph import GraphBase
from Graphs.cine_graph import CineGraph 
from Graphs.fourier_graph import FourierTransformGraph
from signal_data import Signal
from sliders import Slider
from Graphs.spectrogram import SpectrogramDisplay

class eCOOLizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eCOOLizer")
        self.setGeometry(100, 100, 1000, 700)

        self.mainLayout = QVBoxLayout()

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
        self.playAudio = QPushButton(QIcon("Main_App/Assets/pause audio.png"), "")

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
        self.musicModeButton = QPushButton(QIcon("Main_App/Assets/Music.png"),"")
        self.animalModeButton = QPushButton(QIcon("Main_App/Assets/Animal.png"),"")
        self.ecgModeButton = QPushButton(QIcon("Main_App/Assets/ECG.png"),"")

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
                # names.append(f"{ind*100+1000} HZ")
                # ranges.append([[ind*100+1000, (ind+1)*100+1000]])
                center_frequency = ind * 100 + 1000  # Calculate the center frequency
                names.append(f"{center_frequency} HZ")  # Append name
                ranges.append([[center_frequency - 50, center_frequency + 50]])
            return self.contorls(names, ranges, 8700)

        elif mode == "animal":
            # names = ["Cat", "Dog", "Bird", "Lion"]
            # ranges = [[[0, 4000]], [[50, 2000]], [[1800, 2600]], [[0, 500]]]
            names = ["Dog", "Wolve", "Crow", "Bat"]
            ranges = [[[0, 450]], [[450, 1100]], [[1100, 3000]], [[3000, 9000]]]
            return self.contorls(names, ranges, 1000)
        
        elif mode == "music":
            # names = ["guitar","piano","Triangle","trombone","Xylophone"]
            # ranges = [[[500,1200]],[[50,450]],[[4500,20000]],[[1000,4000]],[[300,1000]]]
            # names = ["Guitar", "Flute", "xylophone", "drums"]
            # ranges = [[[5096, 50956]], [[50957, 101913]], [[101914, 152869]], [[152870, 968176]]]
   
            names = ["Guitar", "Flute", "xylophone", "Harmonica"]
            ranges = [[[0, 170]], [[170, 400]], [[150, 400],[2000,23000]], [[400, 4000]]]
            # ranges = [[[0, 200],[10000,23000]], [[170, 350],[10000,23000]], [[250, 400],[2000,5000]], [[300, 2500],[5000,23000]]]
            return self.contorls(names, ranges, 1870)

        elif mode == "ecg":
            names = ["Normal","Aflutter","Afib","Bradycardia"]
            ranges=[[[0.5,20]],[[59,62]],[[59,62]],[[75,96]]]
            return self.contorls(names, ranges)

    def plotDummyData(self):
        if not hasattr(self, 'time'):
            self.time = 0  # Initialize the time if it doesn't exist
        t = np.linspace(self.time, self.time + 10, 1000)
        amplitude = 1  # Amplitude of the bell curve
        mean = 5  # Center of the bell curve (in seconds)
        std_dev = 1  # Standard deviation (width of the bell curve)

        bell_curve = amplitude * np.exp(-0.5 * ((t - mean) / std_dev) ** 2)  # Gaussian function

        # Apply small random variations for the equalizer-like effect
        variation1 = bell_curve + 0.1 * np.random.normal(size=len(t))  # Variation for input
        variation2 = bell_curve + 0.2 * np.random.normal(size=len(t))  # Variation for output
        variation3 = bell_curve  # Pure bell curve for Fourier graph

        # Clear the previous plot
        self.inputGraph.clear()
        self.outputGraph.clear()
        self.fourierGraph.clear()

        # Plot the updated data
        self.inputGraph.plot(t, variation1, pen=mkPen(color=yellowColor, width=2))
        self.outputGraph.plot(t, variation2, pen=mkPen(color=yellowColor, width=2))
        self.fourierGraph.plot(t, variation3, pen=mkPen(color=yellowColor, width=2))

        # Update the time for the next plot
        self.time += 0.1  # Increment the time to simulate real-time progression

    def setUI(self):
        self.currentMode = self.defaultModeButton
        # print("UI setting Done")

    def connectUI(self):
        self.playPauseButton.clicked.connect(self.togglePlayPause)
        self.resetButton.clicked.connect(self.Reset)
        self.defaultModeButton.clicked.connect(self.changeMode)
        self.musicModeButton.clicked.connect(self.changeMode)
        self.animalModeButton.clicked.connect(self.changeMode)
        self.ecgModeButton.clicked.connect(self.changeMode)
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

        self.musicModeButton.setIconSize(QSize(buttonSize, buttonSize))
        self.musicModeButton.setStyleSheet(buttonStyle)

        self.ecgModeButton.setIconSize(QSize(buttonSize, buttonSize))
        self.ecgModeButton.setStyleSheet(buttonStyle)

        self.buttonsGroup.setStyleSheet(buttonsGroupStyle)
        self.buttonsGroup.setContentsMargins(10,0,10,0)
    # print("UI is Styled")

    def changeMode(self):
        button = self.sender()
        if button != self.currentMode:
            match button:
                case self.defaultModeButton:
                    button.setIcon(QIcon("Main_App/Assets/DefaultSelected.png"))
                    self.updateSliderPanel("default")  # Change the number of sliders for Default mode
                case self.musicModeButton:
                    button.setIcon(QIcon("Main_App/Assets/MusicSelected.png"))
                    self.updateSliderPanel("music")  # Change the number of sliders for Music mode
                case self.animalModeButton:
                    button.setIcon(QIcon("Main_App/Assets/AnimalSelected.png"))
                    self.updateSliderPanel("animal")  # Change the number of sliders for Animal mode
                case self.ecgModeButton:
                    button.setIcon(QIcon("Main_App/Assets/EcgSelected.png"))
                    self.updateSliderPanel("ecg")  # Change the number of sliders for ECG mode

            match self.currentMode:
                case self.defaultModeButton:
                    self.currentMode.setIcon(QIcon("Main_App/Assets/Default.png"))
                case self.musicModeButton:
                    self.currentMode.setIcon(QIcon("Main_App/Assets/Music.png"))
                case self.animalModeButton:
                    self.currentMode.setIcon(QIcon("Main_App/Assets/Animal.png"))
                case self.ecgModeButton:
                    self.currentMode.setIcon(QIcon("Main_App/Assets/Ecg.png"))

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
        # workspace.addWidget(self.splitter)

        graphsLayout = QVBoxLayout()

        inputOutputgraphsLayout = QVBoxLayout()
        inputOutputgraphsLayout.addWidget(self.inputGraph)
        inputOutputgraphsLayout.addWidget(self.outputGraph)

        graphsLayout.addLayout(inputOutputgraphsLayout,60)
        graphsLayout.addWidget(self.fourierGraph,30)

        modesRowLayout = QHBoxLayout()

        modesLayout = QHBoxLayout(self.buttonsGroup)
        modesLayout.addWidget(self.defaultModeButton)
        modesLayout.addWidget(self.animalModeButton)
        modesLayout.addWidget(self.musicModeButton)
        modesLayout.addWidget(self.ecgModeButton)

        modesRowLayout.addStretch(20)
        modesRowLayout.addWidget(self.buttonsGroup,20)
        modesRowLayout.addStretch(20)

        slidersPanelLayout = QHBoxLayout()
        slidersPanelLayout.addWidget(self.sliderPanel)

        workspace.addLayout(graphsLayout,40)
        workspace.addLayout(slidersPanelLayout,30)
        workspace.addLayout(modesRowLayout,5)

        topBar.setContentsMargins(0,5,0,5)
        self.mainLayout.addLayout(topBar,20)
        self.mainLayout.addLayout(workspace,90)
        # print("Layout is Set")

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
                    self.playAudio.setIcon(QIcon("Main_App/Assets/play audio.png"))  
                    self.audio_playing = True
                else:
                    self.playAudio.setIcon(QIcon("Main_App/Assets/pause audio.png"))  
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
        
        self.switch_mode()

    def hideShowSpectogram(self):
        is_visible = not self.spectrogram_display.isVisible()
        self.spectrogram_display.setVisible(is_visible)

        if is_visible:
            print("Spectrogram displayed")
            if self.inputGraph.signal:
                self.spectrogram_display.display_spectrogram(self.inputGraph.signal)
            self.splitter.setSizes([500, 300])  # Adjust sizes
        else:
            print("Spectrogram hidden")
            self.splitter.setSizes([800, 0])  # Hide spectrogram

        self.splitter.updateGeometry()

    def toggleScale(self):
        self.fourierGraph.toggle_audiogram_mode()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = eCOOLizer()
    mainWindow.show()
    sys.exit(app.exec_())
