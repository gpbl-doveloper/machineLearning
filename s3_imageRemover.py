import boto3
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

class S3Manager:
    def __init__(self):
        self.bucket = bucket_name

    def deleteFile(self, file_path):
        s3_client.delete_object(Bucket=self.bucket, Key=file_path)
        print(f"Deleted {file_path} from S3.")

    def deleteFolder(self, folder_name):
        response = s3_client.list_objects_v2(Bucket=self.bucket, Prefix=folder_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                s3_client.delete_object(Bucket=self.bucket, Key=obj['Key'])
                print(f"Deleted {obj['Key']}")

def main():
    manager = S3Manager()
    # manager.deleteFile('muruk/muruk1.jpeg')  
    manager.deleteFolder('asset/images/jjongut')

if __name__ == '__main__':
    main()
