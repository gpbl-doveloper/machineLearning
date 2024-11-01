import cv2
import dlib

dogFaceDetectionModel = 'model/dogHeadDetector.dat'

detector = dlib.cnn_face_detection_model_v1(dogFaceDetectionModel)

class FindDogFace:
    def __init__(self):
        pass
    
    def countFaces(self, imagePath):
        image = self.resizeImage(imagePath, targetWidth=200)
        if image is None:
            return {"imagePath": imagePath, "status": "failed", "message": f"Failed to load image: {imagePath}"}  

        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dets = detector(grayImage, 1)
        faceCount = len(dets)
        return {"imagePath": imagePath, "status": "success", "faceCount": faceCount, "message": f"Found {faceCount} faces."}
    
    def resizeImage(self, imagePath, targetWidth=200):
        img = cv2.imread(imagePath)
        if img is None:
            return None

        height, width = img.shape[:2]
        newHeight = int((targetWidth / width) * height)
        resizedImg = cv2.resize(img, (targetWidth, newHeight), interpolation=cv2.INTER_AREA)
        return resizedImg