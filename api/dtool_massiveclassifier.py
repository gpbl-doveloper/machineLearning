import subprocess
import cv2
import numpy as np
from core.dfnd_facerecog import dogFaceRecognize

class DogImageClassifier:
    def __init__(self, bucket_name, s3_directory, dog_name):
        self.bucket_name = bucket_name
        self.s3_directory = s3_directory
        self.dog_name = dog_name
        self.recognizer = dogFaceRecognize()

    def list_images_in_s3_directory(self):
        # 디렉토리 내 모든 파일 가져오기
        command = f"aws s3 ls s3://{self.bucket_name}/{self.s3_directory} --recursive"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Failed to list images from S3 bucket.")
            print("STDERR:", result.stderr)
            return []

        # 이미지 파일 목록 생성 (jpg, jpeg, png 확장자만 선택)
        image_files = [
            line.split()[-1]
            for line in result.stdout.splitlines()
            if line.endswith(('.jpeg', '.jpg', '.png'))
        ]
        
        return image_files

    def fetch_image_from_s3(self, s3_key):
        # 개별 파일 다운로드 및 디코딩
        command = f"aws s3 cp s3://{self.bucket_name}/{s3_key} -"
        print(f"Executing command: {command}")
        
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            image_bytes = result.stdout.encode()  # text 모드에서 읽었으므로 인코딩 필요
            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        else:
            print(f"Failed to fetch image from S3. Error: {result.stderr}")
            return None

    def classify_images(self):
        # S3 디렉토리 내 이미지 파일 목록 가져오기
        image_files = self.list_images_in_s3_directory()
        
        if not image_files:
            print("No images found in the specified S3 directory.")
            return
        
        results = []
        for image_file in image_files:
            print(f"Processing {image_file}")
            image = self.fetch_image_from_s3(image_file)
            if image is not None:
                # 강아지 이름과 함께 이미지 인식 수행
                detection_result = self.recognizer.detection(image, dog_name=self.dog_name)
                results.append({
                    "file": image_file,
                    "result": detection_result
                })
            else:
                print(f"Skipping file {image_file} due to fetch error.")
        
        return results