import os
import numpy as np
from PIL import Image

def processImages(catPath , dogPath):
    images = []
    names = []

    for file in os.listdir(catPath):
        imagePath = os.path.join(catPath, file)
        with Image.open(imagePath) as animalImage:
            animalImage = animalImage.resize((100,100))
            animalImage = np.array(animalImage) / 255
            images.append(animalImage)
            names.append("cat")


    for file in os.listdir(dogPath):
        imagePath = os.path.join(dogPath, file)
        with Image.open(imagePath) as animalImage:
            animalImage = animalImage.resize((100,100))
            animalImage = np.array(animalImage) / 255
            images.append(animalImage)
            names.append("dog")

    return np.array(images), np.array(names)


trainingImages, trainingLabels = processImages(os.path.join("Dataset DC/training_set/cats",""), os.path.join("Dataset DC/training_set/dogs",""))
testingImages, testingLabels = processImages(os.path.join("Dataset DC/test_set/cats",""), os.path.join("Dataset DC/test_set/dogs",""))


os.makedirs("Data", exist_ok=True)

np.save(os.path.join("Data", "trainingImages.npy"), trainingImages)
np.save(os.path.join("Data", "trainingLabels.npy"), trainingLabels)
np.save(os.path.join("Data", "testingImages.npy"), testingImages)
np.save(os.path.join("Data", "testingLabels.npy"), testingLabels)
