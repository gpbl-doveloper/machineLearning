from dfnd_facefinding import findDogFace

def main():
    image_list = ['asset/images/general/2dog.jpeg', 'asset/images/general/samuruk.jpeg']
    finding = findDogFace()

    for image_path in image_list:
        print(f"Processing image: {image_path}")
        face_count = finding.count_faces(image_path)  

if __name__ == '__main__':
    main()