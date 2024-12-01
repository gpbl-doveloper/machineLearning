from fastapi import FastAPI
from api.dtool_howmanyface import DogFaceCounter
from api.dtool_facelearner import DogFaceLearner
from api.dtool_massiveclassifier import DogImageClassifier
from pydantic import BaseModel
from typing import List
app = FastAPI()

learner = DogFaceLearner()
counter = DogFaceCounter()

class ImgData(BaseModel):
    fileId: int
    url: str

class DogData(BaseModel):
    dogId: int
    faces: List[ImgData]

class ClassifyRequest(BaseModel):
    dailyPictures: List[ImgData]
    dogsData: List[DogData]

@app.post("/face/")
async def classify(request: ClassifyRequest):
    learner.processMultipleImages(request.dogsData)
    classifier = DogImageClassifier()
    print("signal: API request received")
    return classifier.classifyImages(request.dailyPictures)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

'''
class FaceLearnerRequest(BaseModel):
    dogsData: list[dict[str, str]]

class CountFacesRequest(BaseModel):
    s3Link: str

class ClassifyImagesRequest(BaseModel):
    s3Link: str

@app.post("/faceLearner/")
async def processImage(request: FaceLearnerRequest):
    print("signal: API request received")
    return learner.processMultipleImagesFromS3(request.dogsData)

@app.post("/countFaces/")
async def countFaces(request: CountFacesRequest):
    print("signal: API request received")
    return counter.countFacesInS3Directory(request.s3Link)

@app.post("/classifyImages/")
async def classifyImages(request: ClassifyImagesRequest):
    classifier = DogImageClassifier()
    print("signal: API request received")
    return classifier.classifyImages(request.s3Link)
'''