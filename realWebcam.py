import cv2

class RealWebcam():
    def __init__(self):
        self.__cam = None
        self.__resolutionWidth = 0
        self.__resolutionHeight = 0

    def ConnectToCamera(self, cameraIndex: int, resolution: tuple):
        self.Stop()

        self.__cam = cv2.VideoCapture(cameraIndex, cv2.CAP_DSHOW)
        if not self.__cam.isOpened():
            return False, f"Camera index {cameraIndex} is invalid."
        
        (width, height) = resolution
        self.__cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.__cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        actualW = self.__cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        actualH = self.__cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

        if actualW == width and actualH == height:
            self.__resolutionWidth = width
            self.__resolutionHeight = height
            return True, ""
        
        self.__cam.release()
        return False, f"The camera index {cameraIndex} does not support the selected resolution ({width} x {height})"
    
    def GetFrame(self):
        return self.__cam.read()
    
    def GetCamResolution(self):
        return self.__resolutionWidth, self.__resolutionHeight
    
    def Stop(self):
        if self.__cam != None:
            self.__cam.release()

        cv2.destroyAllWindows()