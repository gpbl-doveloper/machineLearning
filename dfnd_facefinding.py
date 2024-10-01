import cv2
import dlib
from imutils import face_utils

dog_face_detection_model = 'model/dogHeadDetector.dat'
dog_face_landmark_model = 'model/landmarkDetector.dat'

detector = dlib.cnn_face_detection_model_v1(dog_face_detection_model)
landmark = dlib.shape_predictor(dog_face_landmark_model)

target_path = 'asset/images/general/2dog.jpeg'

class findDogFace:
    def __init__(self):
        pass
    
    def finding(self, org_image, debug=False):
        image = self.resizeImage(org_image, target_width=200)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dets = detector(gray_image, 1)
        print('Found {} faces.'.format(len(dets)))
        face_images = []

        for (i, det) in enumerate(dets):
            shape = landmark(gray_image, det.rect)
            shape = face_utils.shape_to_np(shape)
            (x, y, w, h) = face_utils.rect_to_bb(det.rect)
            face_images.append(image[y:y+h, x:x+w].copy())

            print(f"Face #{i+1} detected at [x: {x}, y: {y}, w: {w}, h: {h}]")

            if debug:
                for (i, (x, y)) in enumerate(shape):
                    print(f"Landmark #{i+1} at position [x: {x}, y: {y}]")
                    
        return face_images
    
    def resizeImage(self, image_path, target_width=200):
        img = cv2.imread(image_path)
        if img is None:
            print(f"Failed to load image: {image_path}")
            return None

        height, width = img.shape[:2]
        new_height = int((target_width / width) * height)
        resized_img = cv2.resize(img, (target_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_img

def main():
    finding = findDogFace()
    finding.finding(target_path, debug=True)

if __name__ == '__main__':
    main()