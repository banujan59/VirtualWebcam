from realWebcam import RealWebcam
from virtualwebcam import VirtualWebcam
from webcamsettings import WebCamSettings

class CameraController():
    def __init__(self, webcamSettings : WebCamSettings):
        self.__realCam = RealWebcam()
        self.__virtualCam = VirtualWebcam(webcamSettings)
    
    def ConnectToCamera(self, cameraIndex: int, resolution: tuple):
        success, errorMessage = self.__realCam.ConnectToCamera(cameraIndex=cameraIndex, resolution=resolution)
        
        if success:
            self.__virtualCam.Start(webcam=self.__realCam)

        return success, errorMessage 

    def Stop(self):
        self.__virtualCam.Stop()
        self.__realCam.Stop()