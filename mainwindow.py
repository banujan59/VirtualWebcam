from webcamsettings import WebCamSettings
from virtualwebcam import VirtualWebcam

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, webCamSettings: WebCamSettings, virtualCam: VirtualWebcam):
        self.__webCamSettings = webCamSettings
        self.__virtualCam = virtualCam

        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.__SetupConnectionControls()
        self.__SetupBrightnessControls()
        self.__SetupImageFlipControls()

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
        self.sharpnessSlider.setEnabled(enabled)
        self.sharpnessValue.setEnabled(enabled)

        self.hFlipBox.setEnabled(enabled)
        self.vFlipBox.setEnabled(enabled)

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
    
    def __SetupBrightnessControls(self):
        self.brightnessSlider.setRange(self.__webCamSettings.BRIGHTNESS_VALUE_MIN, self.__webCamSettings.BRIGHTNESS_VALUE_MAX)
        self.brightnessValue.setRange(self.__webCamSettings.BRIGHTNESS_VALUE_MIN, self.__webCamSettings.BRIGHTNESS_VALUE_MAX)
        self.brightnessSlider.valueChanged.connect(self.__UpdateLightControls)
        self.brightnessSlider.valueChanged.connect(self.brightnessValue.setValue)
        self.brightnessValue.valueChanged.connect(self.brightnessSlider.setValue)

        self.contrastSlider.setRange(self.__webCamSettings.CONTRAST_VALUE_MIN, self.__webCamSettings.CONTRAST_VALUE_MAX)
        self.contrastValue.setRange(self.__webCamSettings.CONTRAST_VALUE_MIN, self.__webCamSettings.CONTRAST_VALUE_MAX)
        self.contrastSlider.valueChanged.connect(self.__UpdateLightControls)
        self.contrastSlider.valueChanged.connect(self.contrastValue.setValue)
        self.contrastValue.valueChanged.connect(self.contrastSlider.setValue)

        self.sharpnessSlider.setRange(self.__webCamSettings.SHARPNESS_VALUE_MIN, self.__webCamSettings.SHARPNESS_VALUE_MAX)
        self.sharpnessValue.setRange(self.__webCamSettings.SHARPNESS_VALUE_MIN, self.__webCamSettings.SHARPNESS_VALUE_MAX)
        self.sharpnessSlider.valueChanged.connect(self.__UpdateLightControls)
        self.sharpnessSlider.valueChanged.connect(self.sharpnessValue.setValue)
        self.sharpnessValue.valueChanged.connect(self.sharpnessSlider.setValue)

    def __SetupImageFlipControls(self):
        self.hFlipBox.stateChanged.connect(self.__SetImageFlip)
        self.vFlipBox.stateChanged.connect(self.__SetImageFlip)
    

    # Slots:
    def __Connect2Camera(self):
        cameraIndex = self.cameraIndexBox.value()
        resolutionIndex = self.resolutionSelector.currentIndex()
        selectedResolution = self.__webCamSettings.GetPossibleResolutions()[resolutionIndex]

        success, errorMessage = self.__virtualCam.ConnectToCamera(cameraIndex=cameraIndex, resolution=selectedResolution)

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

    def __UpdateLightControls(self, value):
        brightness = self.brightnessSlider.value()
        contrast = self.contrastSlider.value()
        sharpness = self.sharpnessSlider.value()
        self.__webCamSettings.SetLightControls(brightness=brightness, contrast=contrast, sharpness=sharpness)

    def __SetImageFlip(self):
        self.__webCamSettings.SetFlip(self.hFlipBox.isChecked(), self.vFlipBox.isChecked())

    def __SetVirtualCameraName(self, name):
        self.virtualCameraLabel.setText(name)

