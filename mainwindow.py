from PyQt5 import QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, webCamSettings):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        
        self.brightnessSlider.setRange(webCamSettings.BRIGHTNESS_VALUE_MIN, webCamSettings.BRIGHTNESS_VALUE_MAX)
        self.brightnessValue.setRange(webCamSettings.BRIGHTNESS_VALUE_MIN, webCamSettings.BRIGHTNESS_VALUE_MAX)
        self.brightnessSlider.valueChanged.connect(self.brightnessValue.setValue)
        self.brightnessValue.valueChanged.connect(self.brightnessSlider.setValue)

        self.contrastSlider.setRange(webCamSettings.CONTRAST_VALUE_MIN, webCamSettings.CONTRAST_VALUE_MAX)
        self.contrastValue.setRange(webCamSettings.CONTRAST_VALUE_MIN, webCamSettings.CONTRAST_VALUE_MAX)
        self.contrastSlider.valueChanged.connect(self.contrastValue.setValue)
        self.contrastValue.valueChanged.connect(self.contrastSlider.setValue)


        self.setFixedSize(640, 480)
        self.setWindowTitle("Virtual Webcam by Banujan")
        self.show()