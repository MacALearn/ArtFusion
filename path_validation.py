import os


def check_file_paths(model_path, image_path):
    """
    Check if the provided file paths for the model and image are valid.

    Args:
    - model_path (str): File path to the model.
    - image_path (str): File path to the image.

    Returns:
    - model_exists (bool): True if the model file exists, False otherwise.
    - image_exists (bool): True if the image file exists, False otherwise.
    """
    model_exists = os.path.exists(model_path)
    image_exists = os.path.exists(image_path)

    return model_exists, image_exists


def check_encoding(file_path):
    """
    Check if the file path contains non-UTF-8 encoded characters.

    Args:
    - file_path (str): File path to check.

    Returns:
    - valid_encoding (bool): True if the file path has valid UTF-8 encoding, False otherwise.
    """
    try:
        # Try to decode the file path as UTF-8
        file_path.encode('utf-8').decode('utf-8')
        valid_encoding = True
    except UnicodeDecodeError:
        valid_encoding = False

    return valid_encoding


# Example usage:
model_path = "style_classifier_model.h5"
image_path = r'C:\Users\USER\Documents\תכנות\פרויקט סופי\python\Database\Images\Academic_Art\232331.jpg'

# Check file paths
model_exists, image_exists = check_file_paths(model_path, image_path)
print("Model file exists:", model_exists)
print("Image file exists:", image_exists)

# Check encoding of file paths
model_encoding_valid = check_encoding(model_path)
image_encoding_valid = check_encoding(image_path)
print("Model file path encoding is valid UTF-8:", model_encoding_valid)
print("Image file path encoding is valid UTF-8:", image_encoding_valid)

import h5py

filepath = 'C:\\Users\\USER\\Desktop\\classificationModel\\style_classifier_model.h5'

try:
    with h5py.File(filepath, 'r') as f:
        print("The file is a valid HDF5 file.")
except OSError:
    print("The file is not a valid HDF5 file.")


from tensorflow.keras.models import load_model

filepath = 'C:\\Users\\USER\\Desktop\\classificationModel\\style_classifier_model.h5'

try:
    model = load_model(filepath)
    print("Model loaded successfully.")
except OSError as e:
    print(f"Error loading model: {e}")
