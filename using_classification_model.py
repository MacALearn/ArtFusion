# from tensorflow.keras.models import load_model
# from PIL import Image
# import numpy as np
# # PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
#
# # Load the trained model
# model = load_model('style_classifier_model.h5')
#
# # Define the target size for input images
# target_size = (150, 150)
#
#
# # Load and preprocess the input image
# def preprocess_input_image(image_path):
#     img = Image.open(image_path)
#     img = img.resize(target_size)
#     img = np.array(img) / 255.0  # Scale pixel values to [0, 1]
#     img = np.expand_dims(img, axis=0)  # Add batch dimension
#     return img
#
#
# # Make predictions on a single image
# def predict_single_image(image_path):
#     input_image = preprocess_input_image(image_path)
#     predictions = model.predict(input_image)
#     predicted_class_index = np.argmax(predictions[0])
#     return predicted_class_index
#
#
# # Example usage:
# image_path = r'C:\Users\USER\Documents\תכנות\פרויקט סופי\python\Database\Images\Academic_Art\232331.jpg'
# predicted_class_index = predict_single_image(image_path)
# print("Predicted class index:", predicted_class_index)


# import tensorflow as tf
#
# # Load the model
# model = tf.keras.models.load_model("style_classifier_model.h5")
#
# # Now you can use the model for predictions
# # For example, if you want to predict a single image:
# import numpy as np
# from tensorflow.keras.preprocessing import image
#
# # Load and preprocess the image
#
# img_path = r'C:\Users\USER\DESKTOP\192982.jpg'
# img = image.load_img(img_path, target_size=(150, 150))
# img_array = image.img_to_array(img)
# img_array = np.expand_dims(img_array, axis=0)
# img_array /= 255.  # Normalization
#
# # Predict the class
# predictions = model.predict(img_array)
# print(predictions)

# import numpy as np
# from tensorflow.keras.preprocessing import image
# import tensorflow as tf
# import h5py
#
#
# def load_and_predict(model_path, image_path):
#     """
#     Load a trained model and make predictions on an input image.
#
#     Args:
#     - model_path (str): File path to the trained model (.h5 format).
#     - image_path (str): File path to the input image.
#
#     Returns:
#     - predictions (numpy.ndarray): Predicted probabilities for each class.
#     """
#     # Open the model file with Latin-1 encoding
#     with open(model_path, 'rb') as model_file:
#         # Load the model
#         model = tf.keras.models.load_model(model_file, compile=False)
#
#     # Load and preprocess the image
#     with open(image_path, 'rb') as img_file:
#         img = image.load_img(img_file, target_size=(150, 150))
#         img_array = image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array /= 255.  # Normalization
#
#     # Make predictions
#     predictions = model.predict(img_array)
#
#     return predictions
#
# filepath = 'C:\\Users\\USER\\Desktop\\classificationModel\\style_classifier_model.h5'
#
# # Example usage:
# # model_path = r"C:\Users\USER\Desktop\classificationModel\style_classifier_model.h5"
# image_path = r"C:\Users\USER\Desktop\classificationModel\232331.jpg"
#
# predictions = load_and_predict(filepath, image_path)
# print(predictions)


import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf


def load_and_predict(model_path, image_path):
    """
    Load a trained model and make predictions on an input image.

    Args:
    - model_path (str): File path to the trained model (.h5 format).
    - image_path (str): File path to the input image.

    Returns:
    - predictions (numpy.ndarray): Predicted probabilities for each class.
    """
    # Load the model directly using the file path
    model = tf.keras.models.load_model(model_path, compile=False)

    # Load and preprocess the image
    img = image.load_img(image_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalization

    # Make predictions
    predictions = model.predict(img_array)

    return predictions


filepath = 'C:\\Users\\USER\\Desktop\\style_classifier_model.h5'
image_path = 'C:\\Users\\USER\\Downloads\\pexels-steve-1509534.jpg.jpg'

# Example usage
predictions = load_and_predict(filepath, image_path)
print(predictions)
