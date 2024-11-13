from fastapi import FastAPI
from pydantic import BaseModel
from api.dtool_howmanyface import DogFaceCounter
from api.dtool_facelearner import DogFaceLearner
from api.dtool_massiveclassifier import DogImageClassifier

app = FastAPI()

learner = DogFaceLearner()
counter = DogFaceCounter()

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)