# import os
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
#
# # Define parameters
# input_shape = (150, 150, 3)  # Adjusted size of images for training
# batch_size = 32
# num_classes = 7
# epochs = 10
# main_folder =  r"E:\kaggle\archive"
# print(main_folder)
# train_data_dir = os.listdir(main_folder)
#
# # Preprocess images without saving changes
# datagen = ImageDataGenerator(rescale=1./255)
#
# # Load and augment training data
# train_generator = datagen.flow_from_directory(
#     train_data_dir,
#     target_size=(input_shape[0], input_shape[1]),
#     batch_size=batch_size,
#     class_mode='categorical')
#
# # Build the model
# model = Sequential([
#     Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
#     MaxPooling2D((2, 2)),
#     Conv2D(64, (3, 3), activation='relu'),
#     MaxPooling2D((2, 2)),
#     Conv2D(128, (3, 3), activation='relu'),
#     MaxPooling2D((2, 2)),
#     Conv2D(128, (3, 3), activation='relu'),
#     MaxPooling2D((2, 2)),
#     Flatten(),
#     Dense(512, activation='relu'),
#     Dense(num_classes, activation='softmax')
# ])
#
# # Compile the model
# model.compile(optimizer='adam',
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])
#
# # Train the model
# model.fit(
#     train_generator,
#     epochs=epochs
# )
#
# # Save the model
# model.save("style_classifier_model.h5")
#
# # Evaluate the model
# loss, accuracy = model.evaluate(train_generator)
# print("Training Accuracy:", accuracy)
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
pkl joblib

# Define parameters
input_shape = (150, 150, 3)  # Adjusted size of images for training
batch_size = 32
num_classes = 7
epochs = 10
train_data_dir = r"E:\kaggle\archive"
print(train_data_dir)

# Preprocess images without saving changes
datagen = ImageDataGenerator(rescale=1./255)

# Load and augment training data
train_generator = datagen.flow_from_directory(
    train_data_dir,
    target_size=(input_shape[0], input_shape[1]),
    batch_size=batch_size,
    class_mode='categorical')

# Build the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(num_classes, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(
    train_generator,
    epochs=epochs
)

# Save the model
model.save("style_classifier_model.h5")


# Evaluate the model
loss, accuracy = model.evaluate(train_generator)
print("Training Accuracy:", accuracy)

# Save the trained model
# joblib.dump(model, '../static files/duration_model.pkl')
