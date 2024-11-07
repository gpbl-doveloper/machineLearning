from fastapi import FastAPI
from core.dfnd_facefinding import findDogFace

app = FastAPI()
finding = findDogFace()

@app.post("/countFaces/")
async def process_image(s3_link: str):
    print("signal: API request received")
    face_count = finding.count_faces(s3_link)
    return {"status": "completed", "face_count": face_count}
