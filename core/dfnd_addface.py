import subprocess
import cv2
import numpy as np
import dlib
import face_recognition

detector = dlib.cnn_face_detection_model_v1('model/dogHeadDetector.dat')

class AddDogFace:
    def __init__(self):
        self.knownFaceEncodings = []
        self.knownFaceNames = []

    def fetchImageFromS3(self, s3Link):
        command = f"aws s3 cp {s3Link} -"
        result = subprocess.run(command, shell=True, capture_output=True)
        if result.returncode == 0:
            imageBytes = result.stdout
            imageArray = np.frombuffer(imageBytes, np.uint8)
            image = cv2.imdecode(imageArray, cv2.IMREAD_COLOR)
            return image
        else:
            print("Failed to fetch image from S3.")
            return None

    def processSingleImage(self, image, dogName):
        image = self.resizeImage(image, targetWidth=200)
        detsLocations = faceLocations(image, 1)
        faceEncodings = face_recognition.face_encodings(image, detsLocations)

        results = []
        if faceEncodings:
            for faceEncoding, location in zip(faceEncodings, detsLocations):
                self.knownFaceEncodings.append(faceEncoding)
                self.knownFaceNames.append(dogName)

                top, right, bottom, left = location
                results.append({
                    "status": "success",
                    "message": f"Dog: {dogName}, Face detected at [{top}, {right}, {bottom}, {left}]"
                })
        else:
            results.append({
                "status": "failed",
                "message": "No face detected in image"
            })

        np.save('numpy/known_faces.npy', self.knownFaceEncodings)
        np.save('numpy/known_names.npy', self.knownFaceNames)
        results.append({"status": "success", "message": "Finished adding known faces and saved encodings."})
        return results

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