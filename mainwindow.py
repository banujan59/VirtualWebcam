from PyQt5 import QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        
        BRIGHTNESS_VALUE_MAX = 100
        BRIGHTNESS_VALUE_MIN = 0
        self.brightnessSlider.setRange(BRIGHTNESS_VALUE_MIN, BRIGHTNESS_VALUE_MAX)
        self.brightnessValue.setRange(BRIGHTNESS_VALUE_MIN, BRIGHTNESS_VALUE_MAX)
        self.brightnessSlider.valueChanged.connect(self.brightnessValue.setValue)
        self.brightnessValue.valueChanged.connect(self.brightnessSlider.setValue)

        CONTRAST_VALUE_MAX = 100
        CONTRAST_VALUE_MIN = 0
        self.contrastSlider.setRange(CONTRAST_VALUE_MIN, CONTRAST_VALUE_MAX)
        self.contrastValue.setRange(CONTRAST_VALUE_MIN, CONTRAST_VALUE_MAX)
        self.contrastSlider.valueChanged.connect(self.contrastValue.setValue)
        self.contrastValue.valueChanged.connect(self.contrastSlider.setValue)


        self.setFixedSize(640, 480)
        self.setWindowTitle("Virtual Webcam by Banujan")
        self.show()