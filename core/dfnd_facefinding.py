import cv2
import numpy as np
import dlib

dogFaceDetectionModel = 'model/dogHeadDetector.dat'
detector = dlib.cnn_face_detection_model_v1(dogFaceDetectionModel)

class FindDogFace:
    def __init__(self):
        pass

    def countFaces(self, image):
        image = self.resizeImage(image, targetWidth=200)
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dets = detector(grayImage, 1)
        faceCount = len(dets)
        print(f"Found {faceCount} faces.")
        return faceCount

    def resizeImage(self, image, targetWidth=200):
        height, width = image.shape[:2]
        newHeight = int((targetWidth / width) * height)
        resizedImg = cv2.resize(image, (targetWidth, newHeight), interpolation=cv2.INTER_AREA)
        return resizedImg