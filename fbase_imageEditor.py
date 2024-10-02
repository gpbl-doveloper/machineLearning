import firebase_admin
from firebase_admin import credentials, storage
import os

cred = credentials.Certificate('dogeface-2dc56-firebase-adminsdk-6olnt-b6a5aab139.json')  
firebase_admin.initialize_app(cred, {'storageBucket': 'dogeface-2dc56.appspot.com'})  

class FirebaseManager:
    def __init__(self):
        self.bucket = storage.bucket()

    def deleteFile(self, file_path):
        blob = self.bucket.blob(file_path)
        blob.delete()
        print(f"Deleted {file_path} from Firebase Storage.")

    def deleteFolder(self, folder_name):
        blobs = self.bucket.list_blobs(prefix=folder_name)
        for blob in blobs:
            blob.delete()
            print(f"Deleted {blob.name}")

def main():
    manager = FirebaseManager()
    # manager.deleteFile('muruk/muruk1.jpeg')  
    manager.deleteFolder('muruk')

if __name__ == '__main__':
    main()