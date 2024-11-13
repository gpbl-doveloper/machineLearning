import os
import subprocess
import cv2
import numpy as np
from core.dfnd_facerecog import DogFaceRecognize

class DogImageClassifier:
    def __init__(self):
        self.recognizer = DogFaceRecognize()

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

    def classifyImages(self, s3Link):
        bucketName, prefix = s3Link.split("/", 1)

        command = f"aws s3 ls s3://{bucketName}/{prefix}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, env=os.environ)
        
        if result.returncode != 0:
            print("Failed to list images from S3 bucket.")
            print("Error (stderr):", result.stderr)
            print("Error (stdout):", result.stdout)
            return {"status": "failed", "message": "Could not list images in S3 directory."}
        else:
            print("S3 list output:", result.stdout)

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
                detectionResults = self.recognizer.detection(image)
                
                if detectionResults:  # 얼굴 인식 성공 시
                    for detection in detectionResults:
                        results.append({
                            "imageFile": imageFile,
                            "dogName": detection["name"]
                        })
                else:
                    results.append({
                        "imageFile": imageFile,
                        "status": "failed",
                        "message": "No face detected"
                    })
            else:
                results.append({
                    "imageFile": imageFile,
                    "status": "failed",
                    "message": "Image could not be fetched from S3"
                })

        return {"status": "completed", "results": results}