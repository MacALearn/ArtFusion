import os

def is_image_file(file_path):
    # Define a set of common image file extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff'}

    # Check if the file extension is in the set of image extensions
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() in image_extensions:
        return True
    else:
        return False

# Example usage
file_path = "Database/Images/Academic_Art/232331.jpg"
if is_image_file(file_path):
    print(f"{file_path} is an image file.")
else:
    print(f"{file_path} is not an image file.")
