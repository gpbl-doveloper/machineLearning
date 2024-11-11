import os
import subprocess
import cv2
import numpy as np
from core.dfnd_addface import addDogFace

class DogFaceLearner:
    def __init__(self):
        self.adder = addDogFace()

    def fetch_image_from_s3(self, bucket_name, prefix, s3_key):
        command = f"aws s3 cp s3://{bucket_name}/{prefix}/{s3_key}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, env=os.environ)
        if result.returncode == 0:
            image_bytes = result.stdout
            image_array = np.frombuffer(image_bytes.encode(), np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        else:
            print(f"Failed to fetch image from S3 for key: {s3_key}")
            print("Error (stderr):", result.stderr)  # 오류 메시지 출력
            print("Error (stdout):", result.stdout)
            return None

    def process_image_from_s3(self, s3_link, dog_name):
        bucket_name, prefix = s3_link.split("/", 1)

        command = f"aws s3 ls s3://{bucket_name}/{prefix}/"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, env=os.environ)
        
        if result.returncode != 0:
            print("Failed to list images from S3 bucket.")
            print("Error (stderr):", result.stderr)  
            print("Error (stdout):", result.stdout)
            return {"status": "failed", "message": "Could not list images in S3 directory."}
        else:
            print("S3 list output:", result.stdout)

        image_files = [
            line.split()[-1]
            for line in result.stdout.splitlines()
            if line.endswith(('.jpeg', '.jpg', '.png'))
        ]

        results = []
        for image_file in image_files:
            print(f"Processing {image_file}")
            image = self.fetch_image_from_s3(bucket_name, prefix, image_file)
            if image is not None:
                result = self.adder.process_single_image(image, dog_name)
                results.append(result)

        return {"status": "completed", "results": results}