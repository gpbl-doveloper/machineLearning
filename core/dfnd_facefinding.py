import subprocess
import cv2
import numpy as np
import dlib

dog_face_detection_model = 'model/dogHeadDetector.dat'
detector = dlib.cnn_face_detection_model_v1(dog_face_detection_model)

class findDogFace:
    def __init__(self):
        pass

    def count_faces(self, image):
        image = self.resize_image(image, target_width=200)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dets = detector(gray_image, 1)
        face_count = len(dets)
        print(f"Found {face_count} faces.")
        return face_count

    def resize_image(self, image, target_width=200):
        height, width = image.shape[:2]
        new_height = int((target_width / width) * height)
        resized_img = cv2.resize(image, (target_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_img