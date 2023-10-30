from mainwindow import MainWindow
from webcamsettings import WebCamSettings

import sys
from PyQt5 import QtWidgets

if __name__ == "__main__":
    webCamSettings = WebCamSettings()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(webCamSettings)
    app.exec_()
