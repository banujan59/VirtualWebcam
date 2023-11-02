from webcamsettings import WebCamSettings
from mainwindow import MainWindow
from virtualwebcam import VirtualWebcam

import sys
from PyQt5 import QtWidgets

if __name__ == "__main__":
    webCamSettings = WebCamSettings()
    virtualWebcam = VirtualWebcam(webCamSettings=webCamSettings)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(webCamSettings=webCamSettings, virtualCam=virtualWebcam)
    app.exec_()

    virtualWebcam.Stop()
