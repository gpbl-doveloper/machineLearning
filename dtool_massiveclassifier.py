import os
from dfnd_facerecog import dogFaceRecognize
from PIL import Image
import cv2
import numpy as np
from io import BytesIO
import pillow_heif 

class dogImageClassifier:
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.recognizer = dogFaceRecognize()

    def convertHeicRgb(self, image_path):
        try:
            heif_file = pillow_heif.read_heif(image_path) 
            image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
            img_byte_array = BytesIO()
            image.save(img_byte_array, format='JPEG')
            img_byte_array.seek(0)
            image_array = np.frombuffer(img_byte_array.read(), np.uint8)
            image_cv2 = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image_cv2
        except Exception as e:
            print(f"Error converting HEIC file {image_path}: {str(e)}")
            return None

    def classifyImages(self):
        for image_file in os.listdir(self.image_dir):
            image_path = os.path.join(self.image_dir, image_file)

            if os.path.isfile(image_path) and image_file.lower().endswith(('.jpeg', '.jpg', '.png', '.heic')):
                print(f"Processing {image_file}")

                if image_file.lower().endswith('.heic'):
                    image = self.convertHeicRgb(image_path)
                    if image is not None:
                        self.recognizer.detection(image)
                else:
                    self.recognizer.detection(image_path)

def main():
    image_directory = './asset/images/general'
    classifier = dogImageClassifier(image_directory)
    classifier.classifyImages()

if __name__ == '__main__':
    main()