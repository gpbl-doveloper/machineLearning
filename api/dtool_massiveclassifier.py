import subprocess
from core.dfnd_facerecog import dogFaceRecognize
import cv2
import numpy as np

class dogImageClassifier:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.recognizer = dogFaceRecognize()

    def fetch_image_from_s3(self, s3_key):
        command = f"aws s3 cp s3://{self.bucket_name}/{s3_key} -"
        result = subprocess.run(command, shell=True, capture_output=True)
        if result.returncode == 0:
            image_bytes = result.stdout
            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        else:
            print(f"Failed to fetch image from S3 for key: {s3_key}")
            return None

    def classifyImages(self):
        # S3 버킷의 이미지 파일 목록 가져오기
        command = f"aws s3 ls s3://{self.bucket_name}/"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("Failed to list images from S3 bucket.")
            return

        image_files = [
            line.split()[-1]
            for line in result.stdout.splitlines()
            if line.endswith(('.jpeg', '.jpg', '.png'))
        ]

        for image_file in image_files:
            print(f"Processing {image_file}")
            image = self.fetch_image_from_s3(image_file)
            if image is not None:
                self.recognizer.detection(image)

def main():
    bucket_name = "your-s3-bucket-name" 
    classifier = dogImageClassifier(bucket_name)
    classifier.classifyImages()

if __name__ == '__main__':
    main()