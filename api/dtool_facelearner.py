from core.dfnd_addface import addDogFace

class DogFaceLearner:
    def __init__(self):
        self.adder = addDogFace()

    def process_image_from_s3(self, s3_link, dog_name):
        print("signal: process_image_from_s3 reached")
        result = self.adder.process_single_image(s3_link, dog_name)
        return result