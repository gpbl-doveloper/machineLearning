import boto3
import os
from PIL import Image
from io import BytesIO
import pillow_heif
import os
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    's3',
    aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key= os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1'
)

bucket_name = 'dogefacebucket'

class S3Uploader:
    def __init__(self):
        self.bucket = bucket_name

    def uploadImage(self, local_file_path, dog_name):
        _, file_extension = os.path.splitext(local_file_path)
        file_extension = file_extension.lower()

        existing_files = s3_client.list_objects_v2(Bucket=self.bucket, Prefix=f'asset/images/{dog_name}/')
        file_count = existing_files.get('KeyCount', 0) + 1  
        new_file_name = f'asset/images/{dog_name}/{dog_name}{file_count}.jpeg'

        if file_extension in ['.heic', '.png', '.jpg']:
            if file_extension == '.heic':
                heif_file = pillow_heif.read_heif(local_file_path)
                image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
            else:
                image = Image.open(local_file_path).convert('RGB')

            img_byte_array = BytesIO()
            image.save(img_byte_array, format='JPEG')
            img_byte_array.seek(0)

            s3_client.upload_fileobj(img_byte_array, self.bucket, new_file_name, ExtraArgs={'ContentType': 'image/jpeg'})
            print(f"Uploaded {local_file_path} as {new_file_name} to S3 under asset/images/{dog_name}/ directory.")
        else:
            s3_client.upload_file(local_file_path, self.bucket, new_file_name)
            print(f"Uploaded {local_file_path} as {new_file_name} to S3 under asset/images/{dog_name}/ directory.")

    def listFiles(self, folder_name):
        response = s3_client.list_objects_v2(Bucket=self.bucket, Prefix=folder_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                print(obj['Key'])

def main():
    image_dir = './asset/images/jjongut' 
    dog_name = 'jjongut' 
    uploader = S3Uploader()

    for image_file in os.listdir(image_dir):
        local_file_path = os.path.join(image_dir, image_file)
        uploader.uploadImage(local_file_path, dog_name)

if __name__ == '__main__':
    main()