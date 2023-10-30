from threading import Lock

class WebCamSettings():
    def __init__(self):
        self.BRIGHTNESS_VALUE_MAX = 100
        self.BRIGHTNESS_VALUE_MIN = 1
        self.__brightnessValue = 1
        self.__brightnessDataLock = Lock()

        self.CONTRAST_VALUE_MAX = 5
        self.CONTRAST_VALUE_MIN = 1
        self.__contrastValue = 1
        self.__contrastDataLock = Lock()
    
    def SetBrightness(self, value):
        with self.__brightnessDataLock:
            if value > self.BRIGHTNESS_VALUE_MAX:
                self.__brightnessValue = self.BRIGHTNESS_VALUE_MAX
            elif value < self.BRIGHTNESS_VALUE_MIN:
                self.__brightnessValue = self.BRIGHTNESS_VALUE_MIN
            else:
                self.__brightnessValue = value
        
    def GetBrightness(self):
        with self.__brightnessDataLock:
         return self.__brightnessValue

    def SetContrast(self, value):
        with self.__contrastDataLock:
            if value > self.CONTRAST_VALUE_MAX:
                self.__contrastValue = self.CONTRAST_VALUE_MAX
            elif value < self.CONTRAST_VALUE_MIN:
                self.__contrastValue = self.CONTRAST_VALUE_MIN
            else:
                self.__contrastValue = value

    def GetContrast(self):
        with self.__contrastDataLock:
            return self.__contrastValue