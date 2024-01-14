from webcamsettings import WebCamSettings
from mainwindow import MainWindow
from cameraController import CameraController

import sys
from PyQt5 import QtWidgets

if __name__ == "__main__":
    webCamSettings = WebCamSettings()
    controller = CameraController(webcamSettings=webCamSettings)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(webCamSettings=webCamSettings, controller=controller)
    app.exec_()

    controller.Stop()
