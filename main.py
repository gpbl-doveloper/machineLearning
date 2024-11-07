import os
from fastapi import FastAPI
from pydantic import BaseModel
from api.dtool_howmanyface import findDogFace
from api.dtool_facelearner import DogFaceLearner
from api.dtool_massiveclassifier import dogImageClassifier

os.environ['AWS_ACCESS_KEY_ID'] = 'your-access-key-id'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your-secret-access-key'

app = FastAPI()

learner = DogFaceLearner()
finding = findDogFace()
classifier = dogImageClassifier()

class FaceLearnerRequest(BaseModel):
    s3_link: str
    dog_name: str

class CountFacesRequest(BaseModel):
    s3_link: str

class ClassifyImagesRequest(BaseModel):
    s3_link: str

@app.post("/faceLearner/")
async def process_image(request: FaceLearnerRequest):
    print("signal: API request received")
    result = learner.process_image_from_s3(request.s3_link, request.dog_name)
    return {"status": "completed", "result": result}

@app.post("/countFaces/")
async def count_faces(request: CountFacesRequest):
    print("signal: API request received")
    face_count = finding.count_faces(request.s3_link)
    return {"status": "completed", "face_count": face_count}

@app.post("/classifyImages/")
async def classify_images(request: ClassifyImagesRequest):
    print("signal: API request received")
    result = classifier.classifyImages(request.s3_link)
    return {"status": "completed", "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)