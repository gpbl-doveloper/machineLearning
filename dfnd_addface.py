import os
import cv2
import dlib
import imutils
from imutils import face_utils
import numpy as np
import matplotlib.pyplot as plt
import face_recognition
from dfnd_facefinding import Find_dog_face
import time

face_landmark_detector_path = 'model/dogHeadDetector.dat'
face_landmark_predictor_path = 'model/landmarkDetector.dat'

detector = dlib.cnn_face_detection_model_v1(face_landmark_detector_path)
predictor = dlib.shape_predictor(face_landmark_predictor_path)

known_face = [(("asset/images/muruk/muruk1.jpeg", "asset/images/muruk/muruk2.jpeg", "asset/images/muruk/muruk3.jpeg", "asset/images/muruk/muruk4.jpeg", "asset/images/muruk/muruk5.jpeg"), "muruk"),
              (("asset/images/jjongut/jjongut1.jpeg", "asset/images/jjongut/jjongut2.jpeg", "asset/images/jjongut/jjongut3.jpeg", "asset/images/jjongut/jjongut4.jpeg", "asset/images/jjongut/jjongut5.jpeg"), "jjongut")]

class Add_dog_face:
    def __init__(self):
        self.known_face_encodings = []   
        self.known_face_names = []
    
    def add_known_face(self, known_face):
        Finding = Find_dog_face()
        target_width = 200
        for image_paths, name in known_face:  # 여러 이미지 경로를 순회합니다.
            for face_image_path in image_paths:  # 각 이미지 경로에 대해 반복 처리합니다.
                image = Finding.resize_image(face_image_path, target_width)
                dets_locations = face_locations(image, 1)
                face_encodings = face_recognition.face_encodings(image, dets_locations)

                # 감지된 얼굴에 대한 인코딩을 저장
                for face_encoding, location in zip(face_encodings, dets_locations):
                    detected_face_image = draw_label(image, location, name)
                    self.known_face_encodings.append(face_encoding)
                    self.known_face_names.append(name)
                
                # 이미지 출력
                Finding.plt_imshow(["Input Image", "Detected Face"], [image, detected_face_image], result_name='known_face.jpg')

        # 얼굴 인코딩과 이름을 numpy 파일로 저장
        np.save('numpy/known_faces.npy', self.known_face_encodings)
        np.save('numpy/known_names.npy', self.known_face_names)

def _trim_css_to_bounds(css, image_shape):
    return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)

def _rect_to_css(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()

def _raw_face_locations(img, number_of_times_to_upsample=1):
    return detector(img, number_of_times_to_upsample)

def face_locations(img, number_of_times_to_upsample=1):
    return [_trim_css_to_bounds(_rect_to_css(face.rect), img.shape) for face in _raw_face_locations(img, number_of_times_to_upsample)]

def draw_label(input_image, coordinates, label):
    image = input_image.copy()
    (top, right, bottom, left) = coordinates
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 5)
    cv2.putText(image, label, (left - 10, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 3)
    return image

def main():
    adding = Add_dog_face()
    adding.add_known_face(known_face)

if __name__ == '__main__':
    main()