import boto3
import cv2
import numpy as np
import dlib
import face_recognition
import os
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    's3',
    aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key= os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1'
)


bucket_name = 'dogefacebucket'
base_path = 'asset/images/'

detector = dlib.cnn_face_detection_model_v1('model/dogHeadDetector.dat')

class addDogFace:
    def __init__(self):
        self.known_face_encodings = []   
        self.known_face_names = []

    def getImageFromS3(self, image_path):
        s3_key = f"{base_path}{image_path}"
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        image_bytes = response['Body'].read()
        image_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image

    def addKnownFaces(self, dog_name):
        known_face = [
            ([
                f'{dog_name}/{dog_name}1.jpeg',
                f'{dog_name}/{dog_name}2.jpeg',
                f'{dog_name}/{dog_name}3.jpeg',
                f'{dog_name}/{dog_name}4.jpeg',
                f'{dog_name}/{dog_name}5.jpeg',
                f'{dog_name}/{dog_name}6.jpeg',
                f'{dog_name}/{dog_name}7.jpeg',
                f'{dog_name}/{dog_name}8.jpeg',
                f'{dog_name}/{dog_name}9.jpeg',
                f'{dog_name}/{dog_name}10.jpeg'
            ], dog_name)
        ]

        for image_paths, name in known_face:
            for face_image_path in image_paths:
                image = self.getImageFromS3(face_image_path)
                if image is None:
                    print(f"Could not load image {face_image_path}")
                    continue

                image = self.resizeImage(image, target_width=200)

                dets_locations = faceLocations(image, 1)
                face_encodings = face_recognition.face_encodings(image, dets_locations)

                if face_encodings:
                    for face_encoding, location in zip(face_encodings, dets_locations):
                        self.known_face_encodings.append(face_encoding)
                        self.known_face_names.append(name)

                        top, right, bottom, left = location
                        print(f"Dog: {name}, Face detected at [{top}, {right}, {bottom}, {left}]")
                else:
                    print(f"No face detected in {face_image_path}")

        np.save('numpy/known_faces.npy', self.known_face_encodings)
        np.save('numpy/known_names.npy', self.known_face_names)
        print("Finished adding known faces and saved encodings.")

    def resizeImage(self, image, target_width=200):
        height, width = image.shape[:2]
        new_height = int((target_width / width) * height)
        resized_img = cv2.resize(image, (target_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_img

def faceLocations(img, number_of_times_to_upsample=1):
    return [cssBounder(rectCss(face.rect), img.shape) for face in detector(img, number_of_times_to_upsample)]

def cssBounder(css, image_shape):
    return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)

def rectCss(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()