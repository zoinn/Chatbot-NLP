import contextlib
import os
from PIL import Image
from tensorflow import keras
import numpy as np

def preprocessImage(filePath):
    img = Image.open(filePath)
    img = img.resize((100, 100))
    imgArr = np.array(img) / 255.0
    imgArr = np.expand_dims(imgArr, axis=0)
    return imgArr


def classifyImage(filePath, model, classNames):
    img = preprocessImage(filePath)

    # Silence the model output
    with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
        prediction = model.predict(img)

    predictionIndex = np.argmax(prediction)
    predictionClass = classNames[predictionIndex]
    return predictionClass


def recogniseImage(filePath):
    absolutePath = os.path.abspath(filePath)
    modelPath = "./model/trainedModel.h5"
    model = keras.models.load_model(modelPath)

    classification = classifyImage(absolutePath, model, ['cat','dog'])
    return classification


