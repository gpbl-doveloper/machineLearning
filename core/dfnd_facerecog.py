import cv2
import dlib
import numpy as np
import face_recognition

face_landmark_detector_path = 'model/dogHeadDetector.dat'
face_landmark_predictor_path = 'model/landmarkDetector.dat'

detector = dlib.cnn_face_detection_model_v1(face_landmark_detector_path)
predictor = dlib.shape_predictor(face_landmark_predictor_path)

class dogFaceRecognize:
    def __init__(self):
        self.known_face_encodings = np.load('numpy/known_faces.npy')
        self.known_face_names = np.load('numpy/known_names.npy')
    
    def detection(self, image_input, size=None):
        # 이미지 로드 및 변환
        if isinstance(image_input, str):
            image = cv2.imread(image_input)
            if image is None:
                print(f"Failed to load image: {image_input}")
                return
        else:
            image = image_input

        height, width = image.shape[:2]
        target_width = 200
        new_height = int((target_width / width) * height)
        resized_img = cv2.resize(image, (target_width, new_height), interpolation=cv2.INTER_AREA)

        dets_locations = faceLocations(resized_img)
        face_encodings = face_recognition.face_encodings(resized_img, dets_locations)
        
        if not face_encodings:
            print("No faces detected.")
            return

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.4)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            face_names.append(name)

        for (top, right, bottom, left), name in zip(dets_locations, face_names):
            print(f"Face detected at [{top}, {right}, {bottom}, {left}] identified as: {name}")

def cssBounder(css, image_shape):
    return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)

def rectCss(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()

def rawFace(img, number_of_times_to_upsample=1):
    return detector(img, number_of_times_to_upsample)

def faceLocations(img, number_of_times_to_upsample=1):
    return [cssBounder(rectCss(face.rect), img.shape) for face in rawFace(img, number_of_times_to_upsample)]