from webcamsettings import WebCamSettings
from realWebcam import RealWebcam

import pyvirtualcam
import cv2 as cv2
import threading

class VirtualWebcam():
    def __init__(self, webCamSettings: WebCamSettings):
        self.__webCamSettings = webCamSettings

        self.__stopAllThreads = False
        self.__webcamThread = threading.Thread(target=self.__StartVirtualWebcamThread)

    def Start(self, webcam : RealWebcam):
        self.__stopAllThreads = False
        self.__webcam = webcam
        self.__webcamThread.start()

    def Stop(self):
        if self.__webcamThread.is_alive():
            self.__stopAllThreads = True
            self.__webcamThread.join()

    def __StartVirtualWebcamThread(self):
        width, height = self.__webcam.GetCamResolution()

        with pyvirtualcam.Camera(width=width, height=height, fps=30) as virtualCam:
            self.__webCamSettings.SetVirtualCameraName(f'Using virtual camera: {virtualCam.device}')
            while not self.__stopAllThreads:
                # Capture frame-by-frame
                ret, frame = self.__webcam.GetFrame()
                # if frame is read correctly ret is True
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                
                frame = self.__ProcessFrame(frame=frame)

                virtualCam.send(frame)
                virtualCam.sleep_until_next_frame()

    def __ProcessFrame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 1. Apply brightness & contrast 
        alpha = self.__webCamSettings.GetContrast() # Contrast control
        beta = self.__webCamSettings.GetBrightness() # Brightness control
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

        # 2. Apply image flip
        hFlip, vFlip = self.__webCamSettings.GetFlip()
        if hFlip:
            frame = cv2.flip(frame, 1)
        if vFlip:
            frame = cv2.flip(frame, 0)
        return frame
    