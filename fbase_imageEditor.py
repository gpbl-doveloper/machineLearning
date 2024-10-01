import firebase_admin
from firebase_admin import credentials, storage
import os

# Firebase Admin SDK 초기화
cred = credentials.Certificate('dogeface-2dc56-firebase-adminsdk-6olnt-b6a5aab139.json')  # 서비스 계정 키 파일 경로
firebase_admin.initialize_app(cred, {'storageBucket': 'dogeface-2dc56.appspot.com'})  # Firebase 프로젝트 ID

class FirebaseManager:
    def __init__(self):
        self.bucket = storage.bucket()

    def delete_file(self, file_path):
        # 특정 파일 삭제
        blob = self.bucket.blob(file_path)
        blob.delete()
        print(f"Deleted {file_path} from Firebase Storage.")

    def delete_folder(self, folder_name):
        # 특정 폴더 내 모든 파일 삭제
        blobs = self.bucket.list_blobs(prefix=folder_name)
        for blob in blobs:
            blob.delete()
            print(f"Deleted {blob.name}")

def main():
    manager = FirebaseManager()
    # 파일 삭제
    # manager.delete_file('muruk/muruk1.jpeg')  # 특정 파일 경로

    # 폴더 삭제
    manager.delete_folder('muruk')  # 특정 애견 이름 폴더 삭제

if __name__ == '__main__':
    main()
