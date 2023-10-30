from webcamsettings import WebCamSettings

from PyQt5 import QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, webCamSettings: WebCamSettings):
        self.__webCamSettings = webCamSettings
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        
        self.brightnessSlider.setRange(self.__webCamSettings.BRIGHTNESS_VALUE_MIN, self.__webCamSettings.BRIGHTNESS_VALUE_MAX)
        self.brightnessValue.setRange(self.__webCamSettings.BRIGHTNESS_VALUE_MIN, self.__webCamSettings.BRIGHTNESS_VALUE_MAX)
        self.brightnessSlider.valueChanged.connect(self.UpdateBrightnessData)
        self.brightnessValue.valueChanged.connect(self.UpdateBrightnessData)

        self.contrastSlider.setRange(self.__webCamSettings.CONTRAST_VALUE_MIN, self.__webCamSettings.CONTRAST_VALUE_MAX)
        self.contrastValue.setRange(self.__webCamSettings.CONTRAST_VALUE_MIN, self.__webCamSettings.CONTRAST_VALUE_MAX)
        self.contrastSlider.valueChanged.connect(self.UpdateContrastData)
        self.contrastValue.valueChanged.connect(self.UpdateContrastData)


        self.setFixedSize(640, 480)
        self.setWindowTitle("Virtual Webcam by Banujan")
        self.show()

    def UpdateBrightnessData(self, value):
        self.__webCamSettings.SetBrightness(value=value)
        self.brightnessSlider.setValue(self.__webCamSettings.GetBrightness())
        self.brightnessValue.setValue(self.__webCamSettings.GetBrightness())

    def UpdateContrastData(self, value):
        self.__webCamSettings.SetContrast(value=value)
        self.contrastSlider.setValue(self.__webCamSettings.GetContrast())
        self.contrastValue.setValue(self.__webCamSettings.GetContrast())

