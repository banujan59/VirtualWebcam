from threading import Lock

class WebCamSettings():
    def __init__(self):
        self.cameraIndex = 0

        self.__lightDataLock = Lock()
        self.BRIGHTNESS_VALUE_MAX = 100
        self.BRIGHTNESS_VALUE_MIN = 1
        self.__brightnessValue = 1

        self.CONTRAST_VALUE_MAX = 5
        self.CONTRAST_VALUE_MIN = 1
        self.__contrastValue = 1

        self.SHARPNESS_VALUE_MAX = 10
        self.SHARPNESS_VALUE_MIN = 1
        self.__sharpnessValue = 1

        self.__flipHorizontal = False
        self.__flipVertical = False
        self.__flipLock = Lock()

        self.__virtualCameraNameObservers = []

    def SetLightControls(self, brightness, contrast, sharpness):
        with self.__lightDataLock:
            self.__brightnessValue = brightness
            self.__contrastValue = contrast
            self.__sharpnessValue = sharpness

    def GetLightControls(self):
        with self.__lightDataLock:
            return self.__brightnessValue, self.__contrastValue, self.__sharpnessValue

    def GetContrast(self):
        with self.__contrastDataLock:
            return self.__contrastValue
        
    def SetFlip(self, hFlip : bool, vFlip: bool):
        with self.__flipLock:
            self.__flipHorizontal = hFlip
            self.__flipVertical = vFlip

    def GetFlip(self):
        with self.__flipLock:
            return self.__flipHorizontal, self.__flipVertical
        
    def GetPossibleResolutions(self):
        return [(3840, 2160), (1920, 1080), (1280, 720), (1024, 768), (800, 600), (640, 480), (176, 144)]
    
    def AddVirtualCameraNameObserver(self, callbackFunction):
        self.__virtualCameraNameObservers.append(callbackFunction)

    def SetVirtualCameraName(self, name : str):
        for callbackFunctions in self.__virtualCameraNameObservers:
            callbackFunctions(name)
            