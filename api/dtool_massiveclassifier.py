import subprocess
import cv2
import numpy as np
from core.dfnd_facerecog import dogFaceRecognize

class dogImageClassifier:
    def __init__(self):
        self.recognizer = dogFaceRecognize()

    def fetch_image_from_s3(self, s3_link, s3_key):
        # 디버깅용: 실제 명령어 확인
        command = f"aws s3 cp s3://{s3_link}/{s3_key} -"
        print(f"Executing command: {command}")

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # 디버깅: 출력 및 오류 메시지 확인
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            image_bytes = result.stdout.encode()  # text 모드에서 읽었으므로 인코딩 필요
            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        else:
            print(f"Failed to fetch image from S3. Error: {result.stderr}")
            return None

    def classifyImages(self, s3_link):
        # S3 디렉토리의 파일 목록 가져오기
        command = f"aws s3 ls s3://{s3_link}/"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # 디버깅: 파일 목록 가져오기 오류 확인
        if result.returncode != 0:
            print("Failed to list images from S3 bucket.")
            print("STDERR:", result.stderr)
            return

        # 이미지 파일 목록 생성 (jpg, jpeg, png 확장자만 선택)
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