from webcamsettings import WebCamSettings
from cameraController import CameraController

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, webCamSettings: WebCamSettings, controller: CameraController):
        self.__webCamSettings = webCamSettings
        self.__cameraController = controller

        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.__SetupConnectionControls()
        self.__SetupBrightnessAndContrastControls()
        self.__SetupImageFlipControls()
        self.__SetupARFiltersPanel()

        self.__SetUIEnableState(False)
        self.setFixedSize(640, 480)
        self.setWindowTitle("Virtual Webcam by Banujan")
        self.show()


    # Setup:
    def __SetUIEnableState(self, enabled : bool):
        self.brightnessSlider.setEnabled(enabled)
        self.brightnessValue.setEnabled(enabled)
        self.contrastSlider.setEnabled(enabled)
        self.contrastValue.setEnabled(enabled)
        self.hFlipBox.setEnabled(enabled)
        self.vFlipBox.setEnabled(enabled)
        
        self.blurBackgroundCheckBox.setEnabled(enabled)

    def __SetupConnectionControls(self):
        resolutions = self.__webCamSettings.GetPossibleResolutions()
        resolutionsStr = []
        for (width, height) in resolutions:
            resolutionsStr.append(f"{width} x {height}")

        self.resolutionSelector.addItems(resolutionsStr)
        self.resolutionSelector.setCurrentIndex(0)

        self.connectButton.clicked.connect(self.__Connect2Camera)
        self.connectButton.setCursor(Qt.PointingHandCursor)

        self.virtualCameraLabel.setText("")
        self.__webCamSettings.AddVirtualCameraNameObserver(self.__SetVirtualCameraName)
    
    def __SetupBrightnessAndContrastControls(self):
        self.brightnessSlider.setRange(self.__webCamSettings.BRIGHTNESS_VALUE_MIN, self.__webCamSettings.BRIGHTNESS_VALUE_MAX)
        self.brightnessValue.setRange(self.__webCamSettings.BRIGHTNESS_VALUE_MIN, self.__webCamSettings.BRIGHTNESS_VALUE_MAX)
        self.brightnessSlider.valueChanged.connect(self.__UpdateBrightnessData)
        self.brightnessValue.valueChanged.connect(self.__UpdateBrightnessData)

        self.contrastSlider.setRange(self.__webCamSettings.CONTRAST_VALUE_MIN, self.__webCamSettings.CONTRAST_VALUE_MAX)
        self.contrastValue.setRange(self.__webCamSettings.CONTRAST_VALUE_MIN, self.__webCamSettings.CONTRAST_VALUE_MAX)
        self.contrastSlider.valueChanged.connect(self.__UpdateContrastData)
        self.contrastValue.valueChanged.connect(self.__UpdateContrastData)

    def __SetupImageFlipControls(self):
        self.hFlipBox.stateChanged.connect(self.__SetImageFlip)
        self.vFlipBox.stateChanged.connect(self.__SetImageFlip)

    def __SetupARFiltersPanel(self):
        self.blurBackgroundCheckBox.stateChanged.connect(self.__webCamSettings.SetBlurBackground)

    # Slots:
    def __Connect2Camera(self):
        cameraIndex = self.cameraIndexBox.value()
        resolutionIndex = self.resolutionSelector.currentIndex()
        selectedResolution = self.__webCamSettings.GetPossibleResolutions()[resolutionIndex]

        success, errorMessage = self.__cameraController.ConnectToCamera(cameraIndex=cameraIndex, resolution=selectedResolution)

        if success:
            self.__SetUIEnableState(True)
        else:
            self.__SetUIEnableState(False)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Camera connection error.")
            msg.setWindowTitle("Error!")
            msg.setInformativeText(errorMessage)
            msg.exec_()

    def __UpdateBrightnessData(self, value):
        self.__webCamSettings.SetBrightness(value=value)
        self.brightnessSlider.setValue(self.__webCamSettings.GetBrightness())
        self.brightnessValue.setValue(self.__webCamSettings.GetBrightness())

    def __UpdateContrastData(self, value):
        self.__webCamSettings.SetContrast(value=value)
        self.contrastSlider.setValue(self.__webCamSettings.GetContrast())
        self.contrastValue.setValue(self.__webCamSettings.GetContrast())

    def __SetImageFlip(self):
        self.__webCamSettings.SetFlip(self.hFlipBox.isChecked(), self.vFlipBox.isChecked())

    def __SetVirtualCameraName(self, name):
        self.virtualCameraLabel.setText(name)

