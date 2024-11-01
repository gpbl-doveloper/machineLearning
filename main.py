from fastapi import FastAPI
from typing import List
from api.dtool_facelearner import DogFaceLearner
from api.dtool_howmanyface import DogFaceCounter
from api.dtool_massiveclassifier import DogImageClassifier

app = FastAPI()

learner = DogFaceLearner()
counter = DogFaceCounter()
classifier = DogImageClassifier()

@app.post("/addKnownFaces/")
async def addKnownFaces(dogNames: List[str]):
    # Endpoint to add known faces for specified dog names.
    results = learner.addKnownFaces(dogNames)
    return {"status": "completed", "results": results}

@app.post("/countFaces/")
async def countFaces(imageS3Paths: List[str]):
    # Endpoint to count faces in images from S3 paths.
    results = counter.countFaces(imageS3Paths)
    return {"status": "completed", "results": results}

@app.post("/classifyImages/")
async def classifyImages(imageS3Paths: List[str]):
    # Endpoint to classify dog faces in images from S3 paths.
    results = classifier.classifyImages(imageS3Paths)
    return {"status": "completed", "results": results}