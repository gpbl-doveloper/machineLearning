from dfnd_addface import addDogFace

def main():
    dog_name_list = ['muruk', 'jjongut']

    adding = addDogFace()

    for dog_name in dog_name_list:
        print(f"Processing dog: {dog_name}")
        adding.addKnownFaces(dog_name)

if __name__ == '__main__':
    main()