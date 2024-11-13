import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Graphs')))

import numpy as np
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDesktopWidget, QVBoxLayout, QWidget, QSlider,QFileDialog, \
    QPushButton, QHBoxLayout
from PyQt5.uic.properties import QtCore
from pyqtgraph import PlotWidget, mkPen

from mainStyle import mainStyle,logoStyle,audioNameStyle,buttonsGroupStyle,buttonStyle,importButton,sliderStyle,sliderLabelStyle,controlButtonStyle
from mainStyle import darkColor, yellowColor
from Graphs.BaseGraph import GraphBase
from Graphs.cine_graph import CineGraph 
from Graphs.fourier_graph import FourierTransformGraph
from signal_data import Signal

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
        self.currentMode = QPushButton()
        self.sliderPanel = None
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

        # self.inputGraph = PlotWidget()
        self.inputGraph = CineGraph("Input Graph")
        # self.outputGraph = PlotWidget()
        self.outputGraph = CineGraph("Output Graph")

        self.inputGraph.link_with(self.outputGraph)

        # self.fourierGraph = PlotWidget()
        self.fourierGraph=FourierTransformGraph("Fourier Graph")

        self.buttonsGroup = QWidget()
        self.defaultModeButton = QPushButton(QIcon("Main_App/Assets/DefaultSelected.png"),"")
        self.musicModeButton = QPushButton(QIcon("Main_App/Assets/Music.png"),"")
        self.animalModeButton = QPushButton(QIcon("Main_App/Assets/Animal.png"),"")
        self.ecgModeButton = QPushButton(QIcon("Main_App/Assets/ECG.png"),"")


        self.sliderPanel = self.createSliderPanel(10)
        print("UI elements Created")

    # TESTING FUNCTION
    def updateSliderPanel(self, numSliders):
        if self.sliderPanel:
            self.sliderPanel.deleteLater()

        self.sliderPanel = self.createSliderPanel(numSliders)

        sliderPanelLayout = QHBoxLayout()
        sliderPanelLayout.addWidget(self.sliderPanel)

        workspaceLayout = self.mainLayout.itemAt(1)  
        if workspaceLayout:
            workspaceLayout.itemAt(1).addLayout(sliderPanelLayout)

    def createSliderPanel(self, numSliders):
        sliderPanelLayout = QHBoxLayout() 
        sliderPanelLayout.setAlignment(Qt.AlignCenter) 
        sliderPanelLayout.setSpacing(20)        

        for indx in range(1, numSliders + 1):
            # Create slider
            slider = QSlider(Qt.Vertical)
            slider.setStyleSheet(sliderStyle)
            slider.setRange(0, 100)  # Set the range as an example (0 to 100)

            # Create label
            label = QLabel(f"Slider#{indx}")
            label.setStyleSheet(sliderLabelStyle)
            label.setAlignment(Qt.AlignCenter)

            # Create a vertical layout for each slider and label
            verticalLayout = QVBoxLayout()
            verticalLayout.addWidget(slider)
            verticalLayout.addWidget(label)
            verticalLayout.setAlignment(Qt.AlignCenter)  # Center the slider and label in the vertical layout
            verticalLayout.setSpacing(5)  # Remove vertical spacing between slider and label

            # Add the vertical layout to the horizontal layout
            sliderPanelLayout.addLayout(verticalLayout)

            # Add spacing between the sliders themselves
            if indx < numSliders:  # Avoid adding spacing after the last slider
                sliderPanelLayout.addSpacing(30)  # Set the spacing between sliders

        # Create a QWidget to hold the slider panel layout and return it
        sliderPanelWidget = QWidget()
        sliderPanelWidget.setLayout(sliderPanelLayout)

        return sliderPanelWidget

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
        print("UI setting Done")
    def connectUI(self):
        self.playPauseButton.clicked.connect(self.togglePlayPause)
        self.resetButton.clicked.connect(self.Reset)
        self.defaultModeButton.clicked.connect(self.changeMode)
        self.musicModeButton.clicked.connect(self.changeMode)
        self.animalModeButton.clicked.connect(self.changeMode)
        self.ecgModeButton.clicked.connect(self.changeMode)
        self.uploadButton.clicked.connect(self.load_signal)
        

        print("UI Connected")

    def stylingUI(self):
        self.setStyleSheet(mainStyle)
        self.eCOOLizerLogo.setStyleSheet(logoStyle)
        self.audioLoadedName.setStyleSheet(audioNameStyle)
        self.audioLoadedName.setContentsMargins(10,0,10,0)
        self.uploadButton.setStyleSheet(importButton)

        self.playPauseButton.setStyleSheet(controlButtonStyle)
        self.playPauseButton.setIconSize(QSize(25, 25))
        self.resetButton.setStyleSheet(controlButtonStyle)
        self.resetButton.setIconSize(QSize(25, 25))


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


    print("UI is Styled")


    def changeMode(self):
        button = self.sender()
        if button != self.currentMode:
            match button:
                case self.defaultModeButton:
                    button.setIcon(QIcon("Main_App/Assets/DefaultSelected.png"))
                    self.updateSliderPanel(10)  # Change the number of sliders for Default mode
                case self.musicModeButton:
                    button.setIcon(QIcon("Main_App/Assets/MusicSelected.png"))
                    self.updateSliderPanel(5)  # Change the number of sliders for Music mode
                case self.animalModeButton:
                    button.setIcon(QIcon("Main_App/Assets/AnimalSelected.png"))
                    self.updateSliderPanel(7)  # Change the number of sliders for Animal mode
                case self.ecgModeButton:
                    button.setIcon(QIcon("Main_App/Assets/EcgSelected.png"))
                    self.updateSliderPanel(12)  # Change the number of sliders for ECG mode

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
        topBar.addStretch()

        workspace = QVBoxLayout()

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
        print("Layout is Set")

    def load_signal(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.wav *.flac *.ogg)")
        if file_path:
            signal = Signal()
            signal.load_signal(file_path)
            file_name = os.path.basename(file_path)
            self.audioLoadedName.setText(f"{file_name}")

            self.inputGraph.set_signal(signal)
            self.outputGraph.set_signal(signal)
            

            self.inputGraph.clear()
            self.outputGraph.clear()
            self.inputGraph.timer.start(self.inputGraph.playSpeed)
            self.fourierGraph.set_signal(signal)

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



           

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = eCOOLizer()
    mainWindow.show()
    sys.exit(app.exec_())
