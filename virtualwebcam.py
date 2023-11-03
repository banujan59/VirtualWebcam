from webcamsettings import WebCamSettings

import pyvirtualcam
import cv2 as cv2
import threading

class VirtualWebcam():
    def __init__(self, webCamSettings: WebCamSettings):
        self.__webCamSettings = webCamSettings

        self.__cam = None
        self.__stopAllThreads = False
        self.__webcamThread = threading.Thread(target=self.__StartVirtualWebcamThread)
    
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
            self.__stopAllThreads = False
            self.__webcamThread.start()
            return True, ""
        
        self.__cam.release()
        return False, f"The camera index {cameraIndex} does not support the selected resolution ({width} x {height})"


    def Stop(self):
        if self.__webcamThread.is_alive():
            self.__stopAllThreads = True
            self.__webcamThread.join()

        if self.__cam != None:
            self.__cam.release()

        cv2.destroyAllWindows()

    def __StartVirtualWebcamThread(self):
        with pyvirtualcam.Camera(width=self.__resolutionWidth, height=self.__resolutionHeight, fps=30) as virtualCam:
            self.__webCamSettings.SetVirtualCameraName(f'Using virtual camera: {virtualCam.device}')
            while not self.__stopAllThreads:
                # Capture frame-by-frame
                ret, frame = self.__cam.read()
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
        brightness, contrast, sharpness = self.__webCamSettings.GetLightControls()
        alpha = contrast
        beta = brightness
        frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
        
        # TODO sharpness

        # 2. Apply image flip
        hFlip, vFlip = self.__webCamSettings.GetFlip()
        if hFlip:
            frame = cv2.flip(frame, 1)
        if vFlip:
            frame = cv2.flip(frame, 0)
        return frame
    