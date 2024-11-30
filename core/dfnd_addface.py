import cv2
import numpy as np
import dlib
import face_recognition

detector = dlib.cnn_face_detection_model_v1('model/dogHeadDetector.dat')

class AddDogFace:
    def __init__(self):
        self.knownFaceEncodings = []
        self.knownFaceNames = []

    def processSingleImage(self, image, dogId):
        image = self.resizeImage(image, targetWidth=200)
        detsLocations = faceLocations(image, 1)
        faceEncodings = face_recognition.face_encodings(image, detsLocations)

        if faceEncodings:
            for faceEncoding in faceEncodings:
                self.knownFaceEncodings.append(faceEncoding)
                self.knownFaceNames.append(dogId)
                print(f"DogId: {dogId}, face added successfully.")
        else:
            print(f"No face detected for DogId: {dogId}.")

        np.save('numpy/known_faces.npy', self.knownFaceEncodings)
        np.save('numpy/known_names.npy', self.knownFaceNames)
        print(f"Known faces and names saved for DogId: {dogId}.")

    def resizeImage(self, image, targetWidth=200):
        height, width = image.shape[:2]
        newHeight = int((targetWidth / width) * height)
        resizedImg = cv2.resize(image, (targetWidth, newHeight), interpolation=cv2.INTER_AREA)
        return resizedImg

def faceLocations(img, numberOfTimesToUpsample=1):
    return [cssBounder(rectCss(face.rect), img.shape) for face in detector(img, numberOfTimesToUpsample)]

def cssBounder(css, imageShape):
    return max(css[0], 0), min(css[1], imageShape[1]), min(css[2], imageShape[0]), max(css[3], 0)

def rectCss(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()