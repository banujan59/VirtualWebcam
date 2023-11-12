from webcamsettings import WebCamSettings
from realWebcam import RealWebcam

import pyvirtualcam
import cv2 as cv2
import threading
import mediapipe as mp
import numpy as np

class VirtualWebcam():
    def __init__(self, webCamSettings: WebCamSettings):
        self.__webCamSettings = webCamSettings

        self.__stopAllThreads = False
        self.__webcamThread = threading.Thread(target=self.__StartVirtualWebcamThread)

        # Init media pipe for AR filters:
        self.__baseOptions = mp.tasks.BaseOptions
        self.__imageSegmenter = mp.tasks.vision.ImageSegmenter
        self.__imageSegmenterOptions = mp.tasks.vision.ImageSegmenterOptions
        self.__visionRunningMode = mp.tasks.vision.RunningMode

        self.__mediaPipeOptions = self.__imageSegmenterOptions(
        base_options=self.__baseOptions(model_asset_path='Model/selfie_segmenter_landscape.tflite'),
        running_mode=self.__visionRunningMode.IMAGE,
        output_category_mask=True)

        self.__segmenter = self.__imageSegmenter.create_from_options(self.__mediaPipeOptions)

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

        # Apply background image
        bgImage = self.__webCamSettings.GetBgImage()
        if bgImage.shape != (0,0): # Checks if the image has been set
            frame = self.__ReplaceBackground(frame, bgImage)

        # Apply background blur
        blurBgValue = self.__webCamSettings.GetBlurBackgroundValue()
        if blurBgValue > 0:
            kernel_size = (9,9)
            blurBg = frame
            for _ in range(blurBgValue):
                blurBg = cv2.GaussianBlur(blurBg, kernel_size, 3)

            frame = self.__ReplaceBackground(frame, blurBg)

        return frame

    def __ReplaceBackground(self, frame, background):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        segmented_masks = self.__segmenter.segment(mp_image)
        category_mask = segmented_masks.category_mask

        image_data = mp_image.numpy_view()
        condition = np.stack((category_mask.numpy_view(),) * 3, axis=-1) > 0.95
        return np.where(condition, background, image_data)

    