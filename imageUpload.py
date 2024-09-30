import firebase_admin
from firebase_admin import credentials, storage

# Firebase 서비스 계정 키 파일 경로
cred = credentials.Certificate('dogeface-2dc56-firebase-adminsdk-6olnt-b6a5aab139.json')

firebase_admin.initialize_app(cred,{'storagebucket' : 'dogeface-2dc56.appspot.com'})

