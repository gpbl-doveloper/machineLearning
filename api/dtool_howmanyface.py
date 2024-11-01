from core.dfnd_facefinding import FindDogFace
from PIL import Image
import cv2
import numpy as np
from io import BytesIO
import pillow_heif

class DogFaceCounter:
    def __init__(self):
        self.finder = FindDogFace()

    def convertHeicRgb(self, imagePath):
        if imagePath.lower().endswith('.heic'):
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
        elif imagePath.lower().endswith(('.jpeg', '.jpg', '.png')):
            return cv2.imread(imagePath)
        else:
            print(f"Unsupported file format: {imagePath}")
            return None

    def countFaces(self, imagePaths):
        results = {}
        for imagePath in imagePaths:
            image = self.convertHeicRgb(imagePath)
            if image is not None:
                try:
                    faceCount = self.finder.countFaces(image)
                    results[imagePath] = {
                        "status": "success",
                        "faceCount": faceCount,
                        "message": f"Found {faceCount} faces in {imagePath}"
                    }
                except Exception as e:
                    results[imagePath] = {
                        "status": "failed",
                        "message": f"Failed to count faces in {imagePath}: {str(e)}"
                    }
            else:
                results[imagePath] = {
                    "status": "failed",
                    "message": f"Could not process image format for {imagePath}"
                }
        return results
