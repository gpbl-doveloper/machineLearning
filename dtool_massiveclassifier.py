import os
from dfnd_facerecog import dogFaceRecognize

class dogImageClassifier:
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.recognizer = dogFaceRecognize()
    
    def classifyImages(self):
        for image_file in os.listdir(self.image_dir):
            if image_file.endswith(('.jpeg', '.jpg', '.png')):
                image_path = os.path.join(self.image_dir, image_file)
                print(f"Processing {image_file}")
                self.recognizer.detection(image_path)
            
def main():
    image_directory = ''
    classifier = dogImageClassifier('./asset/images/general')
    classifier.classifyImages()

if __name__ == '__main__':
    main()