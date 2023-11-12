from threading import Lock
import cv2
import numpy as np

class WebCamSettings():
    def __init__(self):
        self.cameraIndex = 0
        self.currentResolution = (0,0)

        self.__dataAccessMutex = Lock()

        self.BRIGHTNESS_VALUE_MAX = 100
        self.BRIGHTNESS_VALUE_MIN = -100
        self.__brightnessValue = 0

        self.CONTRAST_VALUE_MAX = 5
        self.CONTRAST_VALUE_MIN = 1
        self.__contrastValue = 1

        self.__flipHorizontal = False
        self.__flipVertical = False

        self.__virtualCameraNameObservers = []

        self.BLUR_VALUE_MIN = 0
        self.BLUR_VALUE_MAX = 100
        self.__bgBlurValue = 0
        
        self.__bgImage = np.empty((0,0))
    
    def SetBrightness(self, value):
        with self.__dataAccessMutex:
            if value > self.BRIGHTNESS_VALUE_MAX:
                self.__brightnessValue = self.BRIGHTNESS_VALUE_MAX
            elif value < self.BRIGHTNESS_VALUE_MIN:
                self.__brightnessValue = self.BRIGHTNESS_VALUE_MIN
            else:
                self.__brightnessValue = value
        
    def GetBrightness(self):
        with self.__dataAccessMutex:
         return self.__brightnessValue

    def SetContrast(self, value):
        with self.__dataAccessMutex:
            if value > self.CONTRAST_VALUE_MAX:
                self.__contrastValue = self.CONTRAST_VALUE_MAX
            elif value < self.CONTRAST_VALUE_MIN:
                self.__contrastValue = self.CONTRAST_VALUE_MIN
            else:
                self.__contrastValue = value

    def GetContrast(self):
        with self.__dataAccessMutex:
            return self.__contrastValue
        
    def SetFlip(self, hFlip : bool, vFlip: bool):
        with self.__dataAccessMutex:
            self.__flipHorizontal = hFlip
            self.__flipVertical = vFlip

    def GetFlip(self):
        with self.__dataAccessMutex:
            return self.__flipHorizontal, self.__flipVertical
        
    def GetPossibleResolutions(self):
        return [(3840, 2160), (1920, 1080), (1280, 720), (1024, 768), (800, 600), (640, 480), (176, 144)]
    
    def AddVirtualCameraNameObserver(self, callbackFunction):
        self.__virtualCameraNameObservers.append(callbackFunction)

    def SetVirtualCameraName(self, name : str):
        for callbackFunctions in self.__virtualCameraNameObservers:
            callbackFunctions(name)

    def SetBlurBackgroundValue(self, value : int):
        with self.__dataAccessMutex:
            if value > self.BLUR_VALUE_MAX:
                self.__bgBlurValue = self.BLUR_VALUE_MAX
            elif value < self.BLUR_VALUE_MIN:
                self.__bgBlurValue = self.BLUR_VALUE_MIN
            else:
                self.__bgBlurValue = value

    def GetBlurBackgroundValue(self):
        with self.__dataAccessMutex:
            return self.__bgBlurValue
            
    def ResetBgImage(self):
        with self.__dataAccessMutex:
            self.__bgImage = np.empty((0,0))
    
    def SetBgImage(self, path):
        with self.__dataAccessMutex:
            img = cv2.imread(path)
            
            if img is None:
                return False
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.__bgImage = cv2.resize(img, self.currentResolution)
            return True

    def GetBgImage(self):
        with self.__dataAccessMutex:
            return self.__bgImage
    