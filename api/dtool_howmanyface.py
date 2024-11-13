import os
import subprocess
import cv2
import numpy as np
from core.dfnd_facefinding import FindDogFace

class DogFaceCounter:
    def __init__(self):
        self.finder = FindDogFace()

    def fetchImageFromS3(self, bucketName, prefix, s3Key):
        command = f"aws s3 cp s3://{bucketName}/{prefix}{s3Key} -"
        result = subprocess.run(command, shell=True, capture_output=True, env=os.environ)
        if result.returncode == 0:
            imageBytes = result.stdout
            imageArray = np.frombuffer(imageBytes, np.uint8)
            image = cv2.imdecode(imageArray, cv2.IMREAD_COLOR)
            print("h", type(image))
            return image
        else:
            print(f"Failed to fetch image from S3 for key: {s3Key}")
            print("Error (stderr):", result.stderr)
            print("Error (stdout):", result.stdout)
            print("h", type(image))
            return None

    def countFacesInS3Directory(self, s3Link):
        bucketName, prefix = s3Link.split("/", 1)

        command = f"aws s3 ls s3://{bucketName}/{prefix}"
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

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
                faceCount = self.finder.countFaces(image)
                results.append({
                    "image_file": imageFile,
                    "face_count": faceCount
                })
            else:
                results.append({
                    "image_file": imageFile,
                    "status": "failed",
                    "message": "Image could not be fetched from S3"
                })

        return {"status": "completed", "results": results}