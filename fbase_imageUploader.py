import firebase_admin
from firebase_admin import credentials, storage
import os

# Firebase Admin SDK 초기화
cred = credentials.Certificate('dogeface-2dc56-firebase-adminsdk-6olnt-b6a5aab139.json')  # 서비스 계정 키 파일 경로
firebase_admin.initialize_app(cred, {'storageBucket': 'dogeface-2dc56.appspot.com'})  # Firebase 프로젝트 ID

class FirebaseUploader:
    def __init__(self):
        self.bucket = storage.bucket()

    def upload_image(self, local_file_path, dog_name):
        # 애견별로 폴더를 생성하여 이미지 업로드
        blob = self.bucket.blob(f'{dog_name}/{os.path.basename(local_file_path)}')
        blob.upload_from_filename(local_file_path)
        print(f"Uploaded {local_file_path} to Firebase Storage under {dog_name}/ directory.")
    
    def list_files(self, folder_name):
        # 특정 폴더 내의 파일 목록을 출력
        blobs = self.bucket.list_blobs(prefix=folder_name)
        for blob in blobs:
            print(blob.name)

def main():

    image_dir = './asset/images/jjongut'  # 로컬에 저장된 이미지 경로
    dog_name = 'jjongut'  # 애견 이름을 폴더로 사용
    uploader = FirebaseUploader()
    # 디렉토리 내의 모든 이미지를 업로드
    for image_file in os.listdir(image_dir):
        local_file_path = os.path.join(image_dir, image_file)
        uploader.upload_image(local_file_path, dog_name)

if __name__ == '__main__':
    main()