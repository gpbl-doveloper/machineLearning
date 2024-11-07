import subprocess
import cv2
import numpy as np
import dlib
import face_recognition

detector = dlib.cnn_face_detection_model_v1('model/dogHeadDetector.dat')

class addDogFace:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

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

    def process_single_image(self, s3_link, dog_name):
        image = self.fetch_image_from_s3(s3_link)
        if image is None:
            return {"status": "failed", "message": "Could not load image from S3 link."}

        # 이미지 리사이즈 및 얼굴 인식 수행
        image = self.resizeImage(image, target_width=200)
        dets_locations = faceLocations(image, 1)
        face_encodings = face_recognition.face_encodings(image, dets_locations)

        results = []
        if face_encodings:
            for face_encoding, location in zip(face_encodings, dets_locations):
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(dog_name)  # 강아지 이름과 함께 저장

                top, right, bottom, left = location
                results.append({
                    "status": "success",
                    "message": f"Dog: {dog_name}, Face detected at [{top}, {right}, {bottom}, {left}]"
                })
        else:
            results.append({
                "status": "failed",
                "message": "No face detected in image"
            })

        np.save('numpy/known_faces.npy', self.known_face_encodings)
        np.save('numpy/known_names.npy', self.known_face_names)
        results.append({"status": "success", "message": "Finished adding known faces and saved encodings."})
        return results

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