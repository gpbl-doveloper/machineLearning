from core.dfnd_addface import addDogFace
from PIL import Image
import cv2
import numpy as np
from io import BytesIO
import pillow_heif

class DogFaceLearner:
    def __init__(self):
        self.adder = addDogFace()
    
    def convertHeicRgb(self, imagePath):
        try:
            if imagePath.lower().endswith('.heic'):
                heifFile = pillow_heif.read_heif(imagePath)
                image = Image.frombytes(heifFile.mode, heifFile.size, heifFile.data, "raw")
                imgByteArray = BytesIO()
                image.save(imgByteArray, format='JPEG')
                imgByteArray.seek(0)
                imageArray = np.frombuffer(imgByteArray.read(), np.uint8)
                return cv2.imdecode(imageArray, cv2.IMREAD_COLOR)
            elif imagePath.lower().endswith(('.jpeg', '.jpg', '.png')):
                return cv2.imread(imagePath)
            else:
                print(f"Unsupported file format: {imagePath}")
                return None
        except Exception as e:
            print(f"Error processing file {imagePath}: {str(e)}")
            return None

    def addKnownFaces(self, dogNames):
        results = []
        for dogName in dogNames:
            dogResults = {"dogName": dogName, "images": []}
            imagePaths = [f"{dogName}/{dogName}{i}.jpeg" for i in range(1, 11)]
            for imagePath in imagePaths:
                image = self.adder.getImageFromS3(imagePath)
                if image is not None:
                    try:
                        self.adder.addKnownFaces(dogName)
                        dogResults["images"].append({
                            "imagePath": imagePath,
                            "status": "success",
                            "message": f"Face added successfully in {imagePath}"
                        })
                    except Exception as e:
                        dogResults["images"].append({
                            "imagePath": imagePath,
                            "status": "failed",
                            "message": f"Failed to add face in {imagePath}: {str(e)}"
                        })
                else:
                    dogResults["images"].append({
                        "imagePath": imagePath,
                        "status": "failed",
                        "message": f"Could not process image format for {imagePath}"
                    })
            results.append(dogResults)
        return results