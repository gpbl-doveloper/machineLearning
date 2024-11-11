import subprocess
import cv2
import numpy as np
from core.dfnd_addface import addDogFace

class DogFaceLearner:
    def __init__(self):
        self.adder = addDogFace()

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
            print("Error:", result.stderr)  # 오류 메시지 출력
            return None

    def process_image_from_s3(self, s3_link, dog_name):
        # S3 디렉토리의 파일 목록 가져오기
        command = f"aws s3 ls s3://{s3_link}/"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Failed to list images from S3 bucket.")
            print("Error:", result.stderr)  # 오류 메시지 출력
            return {"status": "failed", "message": "Could not list images in S3 directory."}
        else:
            print("S3 list output:", result.stdout)  # 성공 시 출력 확인

        # 이미지 파일 목록 생성 (jpg, jpeg, png 확장자만 선택)
        image_files = [
            line.split()[-1]
            for line in result.stdout.splitlines()
            if line.endswith(('.jpeg', '.jpg', '.png'))
        ]

        results = []
        for image_file in image_files:
            print(f"Processing {image_file}")
            # 각 파일을 fetch_image_from_s3로 가져옴
            image = self.fetch_image_from_s3(s3_link, image_file)
            if image is not None:
                # 개별 이미지 파일에 대해 얼굴 인식 수행
                result = self.adder.process_single_image(image, dog_name)
                results.append(result)

        return {"status": "completed", "results": results}