from fastapi import FastAPI
from pydantic import BaseModel
from api.dtool_howmanyface import FindDogFace
from api.dtool_facelearner import DogFaceLearner
from api.dtool_massiveclassifier import DogImageClassifier

app = FastAPI()

learner = DogFaceLearner()
finding = FindDogFace()


class FaceLearnerRequest(BaseModel):
    dogsData: list[dict[str, str]]

class CountFacesRequest(BaseModel):
    s3Link: str

class ClassifyImagesRequest(BaseModel):
    s3Link: str

@app.post("/faceLearner/")  # S3 -> numpy 변환하는 모델의 인풋을 생성하는 작업
async def processImage(request: FaceLearnerRequest):
    print("signal: API request received")
    result = learner.processMultipleImagesFromS3(request.dogsData)
    return {"status": "completed", "result": result}

@app.post("/countFaces/")  # 강아지 사진인지 아닌지 판별하는 작업
async def countFaces(request: CountFacesRequest):
    print("signal: API request received")
    faceCount = finding.countFaces(request.s3Link)
    return {"status": "completed", "faceCount": faceCount}

@app.post("/classifyImages/")  # 사진들이 있을 때, 강아지별로 구분해주는 작업
async def classifyImages(request: ClassifyImagesRequest):
    classifier = DogImageClassifier()
    print("signal: API request received")
    result = classifier.classifyImages(request.s3Link)
    return {"status": "completed", "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)