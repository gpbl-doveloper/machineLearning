from core.dfnd_facerecog import DogFaceRecognize
from PIL import Image
import cv2
import numpy as np
from io import BytesIO
import pillow_heif

class DogImageClassifier:
    def __init__(self):
        self.recognizer = DogFaceRecognize()

    def convertHeicRgb(self, imagePath):
        try:
            heifFile = pillow_heif.read_heif(imagePath)
            image = Image.frombytes(heifFile.mode, heifFile.size, heifFile.data, "raw")
            imgByteArray = BytesIO()
            image.save(imgByteArray, format='JPEG')
            imgByteArray.seek(0)
            imageArray = np.frombuffer(imgByteArray.read(), np.uint8)
            return cv2.imdecode(imageArray, cv2.IMREAD_COLOR)
        except Exception as e:
            print(f"Error converting HEIC file {imagePath}: {str(e)}")
            return None

    def classifyImages(self, imagePaths):
        results = {}
        for imagePath in imagePaths:
            image = self.convertHeicRgb(imagePath)
            if image is not None:
                result = self.recognizer.detection(image)
                if isinstance(result, list):
                    for res in result:
                        if "name" in res:
                            res["message"] += f" - Recognized as: {res['name']}"
                elif "name" in result:
                    result["message"] += f" - Recognized as: {result['name']}"
                results[imagePath] = result
            else:
                results[imagePath] = {
                    "status": "failed",
                    "message": f"Failed to process image: {imagePath}"
                }
        return results