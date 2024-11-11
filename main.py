from fastapi import FastAPI
from pydantic import BaseModel
from api.dtool_howmanyface import findDogFace
from api.dtool_facelearner import DogFaceLearner
from api.dtool_massiveclassifier import dogImageClassifier


app = FastAPI()

learner = DogFaceLearner()
finding = findDogFace()


class FaceLearnerRequest(BaseModel):
    s3_link: str
    dog_name: str

class CountFacesRequest(BaseModel):
    s3_link: str

class ClassifyImagesRequest(BaseModel):
    s3_link: str

@app.post("/faceLearner/") # S3 -> numpy 변환하는 모델의 인풋을 생성하는 어쩌구..
async def process_image(request: FaceLearnerRequest):
    print("signal: API request received")
    result = learner.process_image_from_s3(request.s3_link, request.dog_name)
    return {"status": "completed", "result": result}

@app.post("/countFaces/") # 강아지 사진인지 아닌지 판별하는 어쩌구..
async def count_faces(request: CountFacesRequest):
    print("signal: API request received")
    face_count = finding.count_faces(request.s3_link)
    return {"status": "completed", "face_count": face_count}

@app.post("/classifyImages/") # 사진들이 있을 때, 강아지별로 구분해주는 것...
async def classify_images(request: ClassifyImagesRequest):
    classifier = dogImageClassifier() 
    print("signal: API request received")
    result = classifier.classifyImages(request.s3_link)
    return {"status": "completed", "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)