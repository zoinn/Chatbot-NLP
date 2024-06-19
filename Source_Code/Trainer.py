import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
from sklearn.preprocessing import LabelEncoder
import numpy as np
import os
from tensorflow.keras.callbacks import EarlyStopping

trainingImages = np.load('Data/trainingImages.npy')
trainingLabels = np.load('Data/trainingLabels.npy')
testingImages = np.load('Data/testingImages.npy')
testingLabels = np.load('Data/testingLabels.npy')

labelEncoder = LabelEncoder()
trainingLabelsEncoded = labelEncoder.fit_transform(trainingLabels)
testingLabelsEncoded = labelEncoder.transform(testingLabels)

numberOfClasses = len(labelEncoder.classes_)
trainingLabelsOneHot = tf.keras.utils.to_categorical(trainingLabelsEncoded, num_classes=numberOfClasses)
testingLabelsOneHot = tf.keras.utils.to_categorical(testingLabelsEncoded, num_classes=numberOfClasses)

model = Sequential([
    Conv2D(filters=64, kernel_size=(4, 4), activation='relu', input_shape=(100, 100, 3)),
    MaxPooling2D(pool_size=(4, 4)),
    Conv2D(filters=64, kernel_size=(4, 4), activation='relu'),
    MaxPooling2D(pool_size=(4, 4)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(2, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

early_stopping_callback = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

history = model.fit(
    trainingImages, trainingLabelsOneHot,
    epochs=30,
    batch_size=100,
    validation_data=[testingImages,testingLabelsOneHot],
    callbacks=[early_stopping_callback]
)

# Evaluate on test set
testingLoss, testingAccuracy = model.evaluate(testingImages, testingLabelsOneHot, verbose=2)
print("Testing Average Accuracy:", testingAccuracy)
print("Testing Loss:", testingLoss)

# Save the model
modelDirectory = 'model'
modelFileName = 'trainedModel.h5'
modelPath = os.path.join(modelDirectory, modelFileName)

if not os.path.exists(modelDirectory):
    os.makedirs(modelDirectory)

model.save(modelPath)
print("Model saved successfully")
