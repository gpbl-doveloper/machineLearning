import subprocess
import cv2
import numpy as np
from core.dfnd_facerecog import dogFaceRecognize

class dogImageClassifier:
    def __init__(self):
        self.recognizer = dogFaceRecognize()

    def fetch_image_from_s3(self, s3_link, s3_key):
        command = f"aws s3 cp s3://{s3_link}/{s3_key} -"
        result = subprocess.run(command, shell=True, capture_output=True)
        if result.returncode == 0:
            image_bytes = result.stdout
            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        else:
            print(f"Failed to fetch image from S3 for key: {s3_key}")
            return None

    def classifyImages(self, s3_link):
        command = f"aws s3 ls s3://{s3_link}/"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("Failed to list images from S3 bucket.")
            return

        image_files = [
            line.split()[-1]
            for line in result.stdout.splitlines()
            if line.endswith(('.jpeg', '.jpg', '.png'))
        ]

        results = []
        for image_file in image_files:
            print(f"Processing {image_file}")
            image = self.fetch_image_from_s3(s3_link, image_file)
            if image is not None:
                detection_result = self.recognizer.detection(image)
                results.append(detection_result)

        return results