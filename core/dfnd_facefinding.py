import subprocess
import cv2
import numpy as np
import dlib

dog_face_detection_model = 'model/dogHeadDetector.dat'
detector = dlib.cnn_face_detection_model_v1(dog_face_detection_model)

class findDogFace:
    def __init__(self):
        pass

    def fetch_image_from_s3(self, s3_link):
        command = f"aws s3 cp {s3_link} -"
        result = subprocess.run(command, shell=True, capture_output=True)
        if result.returncode == 0:
            image_bytes = result.stdout
            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        else:
            print("Failed to fetch image from S3.")
            return None

    def count_faces(self, s3_link):
        image = self.fetch_image_from_s3(s3_link)
        if image is None:
            return 0  

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