import cv2
import dlib

dog_face_detection_model = 'model/dogHeadDetector.dat'

detector = dlib.cnn_face_detection_model_v1(dog_face_detection_model)

class findDogFace:
    def __init__(self):
        pass
    
    def count_faces(self, image_path):
        image = self.resize_image(image_path, target_width=200)
        if image is None:
            return 0  

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dets = detector(gray_image, 1)
        face_count = len(dets)
        print(f"Found {face_count} faces.")
        return face_count
    
    def resize_image(self, image_path, target_width=200):
        img = cv2.imread(image_path)
        if img is None:
            print(f"Failed to load image: {image_path}")
            return None

        height, width = img.shape[:2]
        new_height = int((target_width / width) * height)
        resized_img = cv2.resize(img, (target_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_img