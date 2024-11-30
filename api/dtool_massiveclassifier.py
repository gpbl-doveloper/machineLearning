import subprocess
import cv2
import numpy as np
from core.dfnd_facerecog import DogFaceRecognize

class DogImageClassifier:
    def __init__(self):
        self.recognizer = DogFaceRecognize()

    def fetchImage(self, url):
        command = f"curl -s {url}"
        result = subprocess.run(command, shell=True, capture_output=True)

        if result.returncode == 0:
            imageBytes = result.stdout
            imageArray = np.frombuffer(imageBytes, np.uint8)
            image = cv2.imdecode(imageArray, cv2.IMREAD_COLOR)
            return image
        else:
            print(f"Failed to fetch image from URL: {url}")
            print("Error (stderr):", result.stderr)
            return None

    def classifyImages(self, dailyPictures):
        groupedResults = {}

        for picture in dailyPictures:
            fileId = picture["fileId"]
            url = picture["url"]

            print(f"Processing fileId: {fileId}, url: {url}")
            image = self.fetchImage(url)

            if image is not None:
                detectionResults = self.recognizer.detection(image)
                if detectionResults:
                    for detection in detectionResults:
                        dogId = detection["dogId"]
                        if dogId not in groupedResults:
                            groupedResults[dogId] = {"dogId": dogId, "imageFiles": []}
                        groupedResults[dogId]["imageFiles"].append({"fileId": fileId, "url": url})
                else:
                    print(f"No faces detected for fileId: {fileId}, url: {url}")
            else:
                print(f"Failed to fetch or process image for fileId: {fileId}")

        return {"status": "completed", "results": list(groupedResults.values())}