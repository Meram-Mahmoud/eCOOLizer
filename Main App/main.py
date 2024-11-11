import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDesktopWidget, QVBoxLayout


class eCOOLizerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eCOOLizer")
        self.setGeometry(100, 100, 1200, 700)
        self.centerWindow()
        self.initialize()
        self.createUI()

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)


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
        self.makelayout()

    def createUIElements(self):
        print("UI elements Created")
    def setUI(self):
        print("UI setting Done")
    def connectUI(self):
        print("UI Connected")
    def stylingUI(self):
        print("UI is Styled")
    def makeLayout(self):
        print("Layout is Set")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = eCOOLizerMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
