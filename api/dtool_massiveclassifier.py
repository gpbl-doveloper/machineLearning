import os
import subprocess
import cv2
import numpy as np
from core.dfnd_facerecog import dogFaceRecognize

class dogImageClassifier:
    def __init__(self):
        self.recognizer = dogFaceRecognize()

    def fetch_image_from_s3(self, bucket_name, prefix, s3_key):
        # 이미지 다운로드 명령어에서 슬래시 중복을 방지
        command = f"aws s3 cp s3://{bucket_name}/{prefix}{s3_key} -"
        result = subprocess.run(command, shell=True, capture_output=True, env=os.environ)
        if result.returncode == 0:
            image_bytes = result.stdout
            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        else:
            print(f"Failed to fetch image from S3 for key: {s3_key}")
            print("Error (stderr):", result.stderr)  # 오류 메시지 출력
            print("Error (stdout):", result.stdout)
            return None

    def classifyImages(self, s3_link):
        # s3_link를 bucket_name과 prefix로 분리
        bucket_name, prefix = s3_link.split("/", 1)

        # S3 디렉토리의 파일 목록 가져오기
        command = f"aws s3 ls s3://{bucket_name}/{prefix}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, env=os.environ)
        
        if result.returncode != 0:
            print("Failed to list images from S3 bucket.")
            print("Error (stderr):", result.stderr)
            print("Error (stdout):", result.stdout)
            return {"status": "failed", "message": "Could not list images in S3 directory."}
        else:
            print("S3 list output:", result.stdout)

        # 이미지 파일 목록 생성 (jpg, jpeg, png 확장자만 선택)
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
                detection_result = self.recognizer.detection(image)
                results.append(detection_result)

        return {"status": "completed", "results": results}