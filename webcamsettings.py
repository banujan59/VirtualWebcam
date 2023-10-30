class WebCamSettings():
    def __init__(self):
        self.BRIGHTNESS_VALUE_MAX = 100
        self.BRIGHTNESS_VALUE_MIN = 0
        self.__brightnessValue = 0

        self.CONTRAST_VALUE_MAX = 100
        self.CONTRAST_VALUE_MIN = 0
        self.__contrastValue = 0
    
    def SetBrightness(self, value):
        if value > self.BRIGHTNESS_VALUE_MAX:
            self.__brightnessValue = self.BRIGHTNESS_VALUE_MAX
        elif value < self.BRIGHTNESS_VALUE_MIN:
            self.__brightnessValue = self.BRIGHTNESS_VALUE_MIN
        else:
            self.__brightnessValue = value
        
    def GetBrightness(self):
        return self.__brightnessValue

    def SetContrast(self, value):
        if value > self.CONTRAST_VALUE_MAX:
            self.__contrastValue = self.CONTRAST_VALUE_MAX
        elif value < self.CONTRAST_VALUE_MIN:
            self.__contrastValue = self.CONTRAST_VALUE_MIN
        else:
            self.__contrastValue = value

    def GetContrast(self):
        return self.__contrastValue