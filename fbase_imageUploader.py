import firebase_admin
from firebase_admin import credentials, storage
import os

cred = credentials.Certificate('dogeface-2dc56-firebase-adminsdk-6olnt-b6a5aab139.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'dogeface-2dc56.appspot.com'})

class FirebaseUploader:
    def __init__(self):
        self.bucket = storage.bucket()

    def uploadImage(self, local_file_path, dog_name):
        blob = self.bucket.blob(f'{dog_name}/{os.path.basename(local_file_path)}')
        blob.upload_from_filename(local_file_path)
        print(f"Uploaded {local_file_path} to Firebase Storage under {dog_name}/ directory.")
    
    def listFiles(self, folder_name):
        blobs = self.bucket.list_blobs(prefix=folder_name)
        for blob in blobs:
            print(blob.name)

def main():

    image_dir = './asset/images/jjongut' 
    dog_name = 'jjongut' 
    uploader = FirebaseUploader()
    for image_file in os.listdir(image_dir):
        local_file_path = os.path.join(image_dir, image_file)
        uploader.uploadImage(local_file_path, dog_name)

if __name__ == '__main__':
    main()