# import os
# from PIL import Image
# import numpy as np
#
# parent_folder = 'data'
# def extract_image_folder_info(parent_folder):
#     folders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]
#     X = []
#     y = []
#     for folder in folders:
#         # Get the path to the current folder
#         folder_path = os.path.join(parent_folder, folder)
#
#         # Get the list of image files in the current folder
#         image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith('.jpg')]
#
#         # Add the image names and folder names to the lists
#         for image_file in image_files:
#             image = Image.open(os.path.join(folder_path, image_file))
#             image_array = np.array(image)
#
#             X.append(image_array)
#             # add convert str to number
#             y.append(folder)
#
#     return X, y
#
#
# X, y = extract_image_folder_info('data')

import os
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define the directory containing your dataset
train_dir = 'train_data'
validation_dir = 'validation_data'

# Parameters
batch_size = 1
image_size = (150, 150)
num_classes = len(os.listdir(train_dir))

# Data augmentation for the training set
train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   fill_mode='nearest')

# No data augmentation for the validation set
validation_datagen = ImageDataGenerator(rescale=1./255)

# Flow training images in batches using train_datagen generator
train_generator = train_datagen.flow_from_directory(train_dir,
                                                    target_size=image_size,
                                                    batch_size=batch_size,
                                                    class_mode='categorical')

# Flow validation images in batches using validation_datagen generator
validation_generator = validation_datagen.flow_from_directory(validation_dir,
                                                              target_size=image_size,
                                                              batch_size=batch_size,
                                                              class_mode='categorical')

# CNN model architecture
model = models.Sequential([
    layers.Conv2D(batch_size, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dropout(0.5),
    layers.Dense(512, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(train_generator,
                    steps_per_epoch=train_generator.samples // batch_size,
                    epochs=1,
                    validation_data=validation_generator,
                    validation_steps=validation_generator.samples // batch_size)

# Save the trained model
model.save('image_classification_model.h5')

