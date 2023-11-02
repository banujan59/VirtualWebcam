from webcamsettings import WebCamSettings
from virtualwebcam import VirtualWebcam

from PyQt5 import QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, webCamSettings: WebCamSettings, virtualCam: VirtualWebcam):
        self.__webCamSettings = webCamSettings
        self.__virtualCam = virtualCam

        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.__SetupConnectionControls()
        self.__SetupBrightnessAndContrastControls()
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
        self.hFlipBox.setEnabled(enabled)
        self.vFlipBox.setEnabled(enabled)

    def __SetupConnectionControls(self):
        resolutions = self.__webCamSettings.GetPossibleResolutions()
        resolutionsStr = []
        for (width, height) in resolutions:
            resolutionsStr.append(f"({width} x {height})")

        self.resolutionSelector.addItems(resolutionsStr)
        self.resolutionSelector.setCurrentIndex(0)

        self.connectButton.clicked.connect(self.__Connect2Camera)
    
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
    

    # Slots:
    def __Connect2Camera(self):
        print("You clicked !")

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

        

