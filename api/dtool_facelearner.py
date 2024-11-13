import os
import subprocess
import cv2
import numpy as np
from core.dfnd_addface import AddDogFace

class DogFaceLearner:
    def __init__(self):
        self.adder = AddDogFace()

    def fetchImageFromS3(self, bucketName, prefix, s3Key):
        command = f"aws s3 cp s3://{bucketName}/{prefix}{s3Key} -"
        result = subprocess.run(command, shell=True, capture_output=True, env=os.environ)
        if result.returncode == 0:
            imageBytes = result.stdout
            imageArray = np.frombuffer(imageBytes, np.uint8)
            image = cv2.imdecode(imageArray, cv2.IMREAD_COLOR)
            return image
        else:
            print(f"Failed to fetch image from S3 for key: {s3Key}")
            print("Error (stderr):", result.stderr)
            print("Error (stdout):", result.stdout)
            return None

    def processImageFromS3(self, s3Link, dogName):
        bucketName, prefix = s3Link.split("/", 1)
        command = f"aws s3 ls s3://{bucketName}/{prefix}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, env=os.environ)

        if result.returncode != 0:
            print("Failed to list images from S3 bucket.")
            print("Error (stderr):", result.stderr)
            print("Error (stdout):", result.stdout)
            return {"status": "failed", "message": "Could not list images in S3 directory."}

        imageFiles = [
            line.split()[-1]
            for line in result.stdout.splitlines()
            if line.endswith(('.jpeg', '.jpg', '.png'))
        ]

        results = []
        for imageFile in imageFiles:
            print(f"Processing {imageFile}")
            image = self.fetchImageFromS3(bucketName, prefix, imageFile)
            if image is not None:
                result = self.adder.processSingleImage(image, dogName)
                results.append(result)

        return {"status": "completed", "results": results}

    def processMultipleImagesFromS3(self, dogsData):
        overallResults = []
        for data in dogsData:
            s3Link = data['s3Link']
            dogName = data['dogName']
            result = self.processImageFromS3(s3Link, dogName)
            overallResults.append(result)
        return overallResults