import firebase_admin
from firebase_admin import credentials, storage
import cv2
import numpy as np
import dlib
from dfnd_facefinding import Find_dog_face
import face_recognition

# Firebase Admin SDK 초기화
cred = credentials.Certificate('dogeface-2dc56-firebase-adminsdk-6olnt-b6a5aab139.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'dogeface-2dc56.appspot.com'})

# 얼굴 감지 모델 초기화 (CNN 또는 HOG)
detector = dlib.cnn_face_detection_model_v1('model/dogHeadDetector.dat')

# 학습할 애견들의 이름 리스트
dog_name_list = ['muruk', 'jjongut']

class Add_dog_face:
    def __init__(self):
        self.known_face_encodings = []   
        self.known_face_names = []
        self.bucket = storage.bucket()

    def get_image_from_firebase(self, image_path):
        # Firebase에서 이미지를 가져와 메모리에서 처리
        blob = self.bucket.blob(image_path)
        image_bytes = blob.download_as_bytes()
        image_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image

    def add_known_faces(self):
        Finding = Find_dog_face()
        target_width = 200

        # 리스트에 있는 모든 애견에 대해 학습
        for dog_name in dog_name_list:
            print(f"Processing dog: {dog_name}")
            known_face = [
                ([
                    f'{dog_name}/{dog_name}1.jpeg',
                    f'{dog_name}/{dog_name}2.jpeg',
                    f'{dog_name}/{dog_name}3.jpeg',
                    f'{dog_name}/{dog_name}4.jpeg',
                    f'{dog_name}/{dog_name}5.jpeg'
                ], dog_name)
            ]

            for image_paths, name in known_face:
                for face_image_path in image_paths:
                    # Firebase에서 이미지를 가져옴
                    image = self.get_image_from_firebase(face_image_path)
                    # 이미지 크기를 조정 (이미지 데이터를 그대로 전달)
                    image = self.resize_image(image, target_width)

                    dets_locations = face_locations(image, 1)
                    face_encodings = face_recognition.face_encodings(image, dets_locations)

                    for face_encoding, location in zip(face_encodings, dets_locations):
                        detected_face_image = draw_label(image, location, name)
                        self.known_face_encodings.append(face_encoding)
                        self.known_face_names.append(name)

                    Finding.plt_imshow(["Input Image", "Detected Face"], [image, detected_face_image], result_name='known_face.jpg')

        # 얼굴 인코딩과 이름을 numpy 파일로 저장
        np.save('numpy/known_faces.npy', self.known_face_encodings)
        np.save('numpy/known_names.npy', self.known_face_names)

    def resize_image(self, image, target_width=200):
        # 로컬 파일 경로 대신, 이미지를 직접 받아서 크기 조정
        height, width = image.shape[:2]
        new_height = int((target_width / width) * height)
        resized_img = cv2.resize(image, (target_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_img

def face_locations(img, number_of_times_to_upsample=1):
    # dlib를 통한 얼굴 위치 감지 함수
    return [_trim_css_to_bounds(_rect_to_css(face.rect), img.shape) for face in detector(img, number_of_times_to_upsample)]

def _trim_css_to_bounds(css, image_shape):
    return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)

def _rect_to_css(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()

def draw_label(input_image, coordinates, label):
    # 얼굴에 라벨을 그리는 함수
    image = input_image.copy()
    (top, right, bottom, left) = coordinates
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    cv2.putText(image, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

# main 함수 역할을 수행하는 함수 추가
def main():
    # 모든 애견에 대해 학습을 진행
    adding = Add_dog_face()
    adding.add_known_faces()

if __name__ == '__main__':
    main()
