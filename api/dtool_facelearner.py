import os
import subprocess
import cv2
import numpy as np
from core.dfnd_addface import AddDogFace

class DogFaceLearner:
    def __init__(self):
        self.adder = AddDogFace()

    def processMultipleImages(self, dogsData):
        for dogData in dogsData:
            dogId = dogData['dogId']
            faces = dogData['faces']

            for faceData in faces:
                fileId = faceData['fileId']
                url = faceData['url']
                print(f"Processing dogId: {dogId}, fileId: {fileId}, url: {url}")
                image = self.fetchImage(url)

                if image is not None:
                    self.adder.processSingleImage(image, dogId)
                else:
                    print(f"Failed to fetch image for fileId: {fileId}, url: {url}")
        print("All images processed successfully.")

    def fetchImage(self, url):
        command = f"curl -s {url}"
        result = subprocess.run(command, shell=True, capture_output=True, env=os.environ)

        if result.returncode == 0:
            imageBytes = result.stdout
            imageArray = np.frombuffer(imageBytes, np.uint8)
            image = cv2.imdecode(imageArray, cv2.IMREAD_COLOR)
            return image
        else:
            print(f"Failed to fetch image from URL: {url}")
            print("Error (stderr):", result.stderr)
            return None