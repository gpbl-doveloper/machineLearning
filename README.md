## 레포지토리 안내 / Repository Overview

이 레포지토리는 제가 국민대학교 내의 프로그램인 KMU Global PBL Program 2024의 일원으로 활동했을 당시 참여하였던 프로젝트의 일부입니다. 해당 프로젝트는 애견센터의 행정을 보조하는 데에 목적이 있으며, 센터가 견주에게 보내는 알림장에 개발의 중점이 맞춰져 있습니다.
레포지토리 내의 코드들은 애견센터의 직원이 갤러리에 있는 수많은 사진 중에서 **특정 애견의 사진을 자동으로 선별**할 수 있게 하여, 작업의 효율성을 크게 높이기 위해 제작된 코드입니다.

This repository is part of a project I participated in as a member of the KMU Global PBL Program 2024 at Kookmin University. The goal of the project is to assist the administration of a dog daycare center, with a focus on developing notifications for pet owners. The codes in this repository are designed to significantly improve work efficiency by allowing daycare staff to automatically select **specific dog photos** from a gallery.

## 코드 설명 / Code Overview

이 레포지토리에 포함된 코드는 크게 세 가지 주요 기능으로 구분됩니다:
1. **애견 얼굴 탐지 및 개수 세기**
2. **애견 얼굴 특징 학습 및 저장**
3. **이미지 속 애견 얼굴 식별**

The code in this repository is divided into three main functions:
1. **Detecting and counting dog faces**
2. **Learning and storing features of dog face**
3. **Identifying dog faces in images**

- **`dfnd_facefinding.py`**: 투입된 이미지 속 강아지의 얼굴을 새는 코드가 구현되어 있습니다. 빠른 속도를 위해, 작업 중 이미지의 크기를 조정하고 색을 흑백으로 조정합니다. 이러한 코드는 `dtool_howmanyface.py`를 통해 실행됩니다.

  The code implemented in **`dfnd_facefinding.py`** counts the number of dog faces in the input image. For efficiency, it resizes the image and converts it to grayscale during processing. This code is executed via `dtool_howmanyface.py`.

- **`dfnd_addface.py`**: Firebase의 스토리지에 저장된 각 애견의 이미지를 메모리에 들여온 뒤 정보를 학습하고, `.npy` 형식으로 해당 정보를 저장하는 코드가 수록되어 있습니다. 해당 코드는 `dtool_facelearner.py`로 실행됩니다.

  **`dfnd_addface.py`** contains code that loads each dog's image from Firebase storage, learns its features, and saves this information in `.npy` format. This code is executed using `dtool_facelearner.py`.

- **`dfnd_facerecog.py`**: 투입된 이미지 속 강아지의 얼굴이 누구의 것인지를 구분하는 코드가 구현되어 있습니다. `dtool_massiveclassifier.py`는 해당 코드가 실행될 디렉토리를 지정합니다. 실행 시 디렉토리 내의 모든 이미지 파일에 대해 식별 작업을 진행합니다. 아이폰의 HEIC 형식 이미지는 일시적으로 JPEG로 전환된 뒤 OpenCV를 통해 처리됩니다.

  **`dfnd_facerecog.py`** is responsible for identifying which dog face belongs to whom in the input image. `dtool_massiveclassifier.py` specifies the directory where this code will be executed. During execution, all image files in the directory are classified. HEIC format images from iPhones are temporarily converted to JPEG and then processed using OpenCV.

- **`fbase_imageuploader.py`**: 각 애견별 이미지가 저장된 디렉토리의 주소와 애견의 이름을 전달받은 뒤, 정보를 정리하여 Firebase의 스토리지에 업로드합니다. 이미지 파일이 HEIC, PNG, JPG 형식일 경우 JPEG로 변환된 이미지를 업로드합니다.

  **`fbase_imageuploader.py`** uploads the images to Firebase storage after receiving the directory address and the dog's name. If the image file is in HEIC, PNG, or JPG format, it is converted to JPEG before being uploaded.

- **`fbase_imageeditor.py`**: Firebase 스토리지 내에 특정 애견의 이미지를 저장하고 있는 버켓(폴더)를 삭제하는 기능을 수행합니다.

  **`fbase_imageeditor.py`** is used to delete the bucket (folder) in Firebase storage that contains the images of a specific dog.

  ## 참조 / References

- [dlib_dog_face_recognition](https://github.com/yunwoong7/dlib_dog_face_recognition)
- [DogRecognition](https://github.com/PAWSITIVE2024/DogRecognition/tree/main)