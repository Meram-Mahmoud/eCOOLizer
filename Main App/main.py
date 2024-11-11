import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDesktopWidget, QVBoxLayout, QWidget, QSlider, \
    QPushButton, QHBoxLayout
from pyqtgraph import PlotWidget


class eCOOLizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eCOOLizer")
        self.setGeometry(100, 100, 1200, 700)

        self.mainLayout = QVBoxLayout()

        self.initialize()
        self.createUI()



    def centerWindow(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    def initialize(self):
        print("initialized")
    def createUI(self):
        self.createUIElements()
        self.setUI()
        self.connectUI()
        self.stylingUI()
        self.makeLayout()
        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)
        self.centerWindow()

    def createUIElements(self):
        self.eCOOLizerLogo = QLabel("eCOOLizer|")
        self.audioLoadedName = QLabel("Need AudioName.mp3")
        self.uploadButton = QPushButton("Upload")

        self.inputGraph = PlotWidget()
        self.outputGraph = PlotWidget()
        self.fourierGraph = PlotWidget()

        self.defaultModeButton = QPushButton("Default")
        self.musicModeButton = QPushButton("Music")
        self.animalModeButton = QPushButton("Animals")
        self.ecgModeButton = QPushButton("ECG")

        self.sliderPanel = self.createSliderPanel(10)
        print("UI elements Created")

    # TESTING FUNCTION
    def createSliderPanel(self, numSliders):
        sliderPanelLayout = QHBoxLayout()  # Layout for the panel

        for indx in range(1, numSliders + 1):
            # Create slider
            slider = QSlider(Qt.Vertical)
            slider.setRange(0, 100)  # Set the range as an example (0 to 100)

            # Create label
            label = QLabel(f"Slider#{indx}")

            # Add the slider and label to the layout
            sliderPanelLayout.addWidget(slider)
            sliderPanelLayout.addWidget(label)

        # Create a QWidget to hold the slider panel layout and return it
        sliderPanelWidget = QWidget()
        sliderPanelWidget.setLayout(sliderPanelLayout)

        return sliderPanelWidget
    def setUI(self):
        print("UI setting Done")
    def connectUI(self):
        print("UI Connected")
    def stylingUI(self):
        print("UI is Styled")
    def makeLayout(self):
        topBar = QHBoxLayout()
        topBar.addWidget(self.eCOOLizerLogo)
        topBar.addWidget(self.audioLoadedName)
        topBar.addWidget(self.uploadButton)

        workspace = QVBoxLayout()

        graphsLayout = QVBoxLayout()
        graphsLayout.addWidget(self.inputGraph)
        graphsLayout.addWidget(self.outputGraph)
        graphsLayout.addWidget(self.fourierGraph)

        modesLayout = QHBoxLayout()
        modesLayout.addWidget(self.defaultModeButton)
        modesLayout.addWidget(self.animalModeButton)
        modesLayout.addWidget(self.musicModeButton)
        modesLayout.addWidget(self.ecgModeButton)

        slidersPanelLayout = QHBoxLayout()
        slidersPanelLayout.addWidget(self.sliderPanel)

        workspace.addLayout(graphsLayout,40)
        workspace.addLayout(modesLayout,5)
        workspace.addLayout(slidersPanelLayout,30)

        self.mainLayout.addLayout(topBar,10)
        self.mainLayout.addLayout(workspace,90)
        print("Layout is Set")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = eCOOLizer()
    mainWindow.show()
    sys.exit(app.exec_())
