import firebase_admin
from firebase_admin import credentials, storage
import os
from PIL import Image
from io import BytesIO
import pillow_heif

cred = credentials.Certificate('dogeface-2dc56-firebase-adminsdk-6olnt-b6a5aab139.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'dogeface-2dc56.appspot.com'})

class FirebaseUploader:
    def __init__(self):
        self.bucket = storage.bucket()

    def uploadImage(self, local_file_path, dog_name):
        _, file_extension = os.path.splitext(local_file_path)
        file_extension = file_extension.lower()

        existing_files = list(self.bucket.list_blobs(prefix=f'{dog_name}/'))
        file_count = len(existing_files) + 1  
        new_file_name = f'{dog_name}{file_count}.jpeg'

        if file_extension in ['.heic', '.png', '.jpg']:
            if file_extension == '.heic':
                heif_file = pillow_heif.read_heif(local_file_path)
                image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
            else:
                image = Image.open(local_file_path).convert('RGB')

            img_byte_array = BytesIO()
            image.save(img_byte_array, format='JPEG')
            img_byte_array.seek(0)

            blob = self.bucket.blob(f'{dog_name}/{new_file_name}')
            blob.upload_from_file(img_byte_array, content_type='image/jpeg')
            print(f"Uploaded {local_file_path} as {new_file_name} to Firebase Storage under {dog_name}/ directory.")
        else:
            blob = self.bucket.blob(f'{dog_name}/{new_file_name}')
            blob.upload_from_filename(local_file_path)
            print(f"Uploaded {local_file_path} as {new_file_name} to Firebase Storage under {dog_name}/ directory.")
    
    def listFiles(self, folder_name):
        blobs = self.bucket.list_blobs(prefix=folder_name)
        for blob in blobs:
            print(blob.name)

def main():
    image_dir = './asset/images/muruk' 
    dog_name = 'muruk' 
    uploader = FirebaseUploader()

    for image_file in os.listdir(image_dir):
        local_file_path = os.path.join(image_dir, image_file)
        uploader.uploadImage(local_file_path, dog_name)

if __name__ == '__main__':
    main()