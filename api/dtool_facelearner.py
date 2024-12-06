import os
import subprocess
import cv2
import numpy as np
from core.dfnd_addface import AddDogFace

class DogFaceLearner:
    def __init__(self):
        self.adder = AddDogFace()

    def processMultipleImages(self, dogsData):
        """
        Process multiple dogs' data containing dogId and their respective image URLs.
        """
        # 기존 numpy 파일들 삭제
        if os.path.exists('numpy/known_faces.npy'):
            os.remove('numpy/known_faces.npy')
        if os.path.exists('numpy/known_names.npy'):
            os.remove('numpy/known_names.npy')
        
        for dogData in dogsData:
            dogId = dogData.dogId
            faces = dogData.faces

            for faceData in faces:
                fileId = faceData.fileId
                url = faceData.url
                print(f"Processing dogId: {dogId}, fileId: {fileId}, url: {url}")
                image = self.fetchImage(url)

                if image is not None:
                    self.adder.processSingleImage(image, dogId)
                else:
                    print(f"Failed to fetch image for fileId: {fileId}, url: {url}")
        print("All images processed successfully.")

    def fetchImage(self, url):
        """
        Fetch an image from a URL and load it into memory.
        """
        print(f"Fetching image from URL: {url}")  # 요청 URL 출력
        command = f"curl -s {url}"
        result = subprocess.run(command, shell=True, capture_output=True, env=os.environ)

        if result.returncode == 0:
            print("Curl executed successfully.")  # curl 실행 성공 메시지
            print(f"Output size: {len(result.stdout)} bytes")  # 데이터 크기 출력

            if not result.stdout:
                print("Curl returned empty output.")  # 빈 데이터 확인
                return None
            imageBytes = result.stdout
            imageArray = np.frombuffer(imageBytes, np.uint8)
            image = cv2.imdecode(imageArray, cv2.IMREAD_COLOR)
            if image is None:
                print("Failed to decode image. Data may not be a valid image.")  # 디코딩 실패
                return None

            print("Image decoded successfully.")  # 디코딩 성공
            return image
        else:
            print(f"Failed to fetch image from URL: {url}")
            print("Error (stderr):", result.stderr)
            return None