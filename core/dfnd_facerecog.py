import cv2
import dlib
import numpy as np
import face_recognition

faceLandmarkDetectorPath = 'model/dogHeadDetector.dat'
faceLandmarkPredictorPath = 'model/landmarkDetector.dat'

detector = dlib.cnn_face_detection_model_v1(faceLandmarkDetectorPath)
predictor = dlib.shape_predictor(faceLandmarkPredictorPath)


class DogFaceRecognize:
    def __init__(self):
        self.knownFaceEncodings = np.load('numpy/known_faces.npy', allow_pickle=True)
        self.knownFaceNames = np.load('numpy/known_names.npy', allow_pickle=True)

    def detection(self, imageInput):
        if isinstance(imageInput, str):
            image = cv2.imread(imageInput)
            if image is None:
                print(f"Failed to load image: {imageInput}")
                return None
        else:
            image = imageInput

        height, width = image.shape[:2]
        targetWidth = 200
        newHeight = int((targetWidth / width) * height)
        resizedImg = cv2.resize(image, (targetWidth, newHeight), interpolation=cv2.INTER_AREA)

        detsLocations = faceLocations(resizedImg)
        faceEncodings = face_recognition.face_encodings(resizedImg, detsLocations)

        results = []
        if not faceEncodings:
            print("No faces detected.")
            return None

        for faceEncoding, location in zip(faceEncodings, detsLocations):
            matches = face_recognition.compare_faces(self.knownFaceEncodings, faceEncoding, tolerance=0.4)
            faceDistances = face_recognition.face_distance(self.knownFaceEncodings, faceEncoding)

            bestMatchIndex = np.argmin(faceDistances) if matches else -1
            if bestMatchIndex >= 0 and matches[bestMatchIndex]:
                dogId = int(self.knownFaceNames[bestMatchIndex])  # 강아지 ID를 숫자로 변환
                results.append({"dogId": dogId})
            else:
                print("Face detected but not recognized.")

        return results if results else None


def faceLocations(img, numberOfTimesToUpsample=1):
    return [cssBounder(rectCss(face.rect), img.shape) for face in detector(img, numberOfTimesToUpsample)]


def cssBounder(css, imageShape):
    return max(css[0], 0), min(css[1], imageShape[1]), min(css[2], imageShape[0]), max(css[3], 0)


def rectCss(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()