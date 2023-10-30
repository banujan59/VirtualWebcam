from webcamsettings import WebCamSettings

import pyvirtualcam
import cv2 as cv2
import threading

class VirtualWebcam():
    def __init__(self, webCamSettings: WebCamSettings):
        self.__webCamSettings = webCamSettings
        self.__stopAllThreads = False

        self.__webcamThread = threading.Thread(target=self.__StartVirtualWebcamThread)
        self.__webcamThread.start()

    #def __del__(self):
    def Stop(self):
        self.__stopAllThreads = True
        self.__webcamThread.join()

    def __StartVirtualWebcamThread(self):
        with pyvirtualcam.Camera(width=640, height=480, fps=30) as cam:
            print(f'Using virtual camera: {cam.device}')

            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Cannot open camera")
                exit()
            while True:
                # Capture frame-by-frame
                ret, frame = cap.read()
                # if frame is read correctly ret is True
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break

                # Display the resulting frame 
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                alpha = self.__webCamSettings.GetContrast() # Contrast control
                beta = self.__webCamSettings.GetBrightness() # Brightness control
                frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

                cam.send(frame)
                cam.sleep_until_next_frame()
                
                if self.__stopAllThreads:
                    break

            # When everything done, release the capture
            cap.release()
            cv2.destroyAllWindows()