from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
from PIL import Image
import pyodbc
# Import necessary modules here to avoid circular imports
from main import main_processing
import shutil

app = Flask(__name__)
CORS(app)

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=(LocalDB)\MSSQLLocalDB;'
                      'Database=Images;'
                      'Trusted_Connection=yes;')
import hashlib


@app.route('/')
def hello_world():
    return 'Hello, World!'


# Directory where your images are stored
IMAGE_DIR = '../Database'
GENERATED_IMAGE = '../outputs'


# Fetch all the categories

@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = [d for d in os.listdir(IMAGE_DIR) if os.path.isdir(os.path.join(IMAGE_DIR, d))]
        categories.append('recommended')  # Add the "recommended" category
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Fetch images by category

@app.route('/images/<category>', methods=['GET'])
def get_images(category):
    try:
        category_dir = os.path.join(IMAGE_DIR, category)
        if not os.path.exists(category_dir) or not os.path.isdir(category_dir):
            return jsonify({'error': 'Category not found'}), 404

        images = [os.path.join(category, f) for f in os.listdir(category_dir) if
                  os.path.isfile(os.path.join(category_dir, f))]
        print("the correct paths:")
        for image in images:
            print(image)
        return jsonify(images)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/colors/<category>', methods=['GET'])
def get_colors(category):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT dc.ColorID, dc.Red, dc.Green, dc.Blue
            FROM DominantColors dc
            JOIN LinkImageColor lic ON dc.ColorID = lic.ColorID
            JOIN LinkImageCategory licat ON lic.ImageID = licat.ImageID
            JOIN Categories c ON licat.CategoryID = c.CategoryID
            WHERE c.CategoryName = ?
        """, category)
        colors = [{'id': row.ColorID, 'red': row.Red, 'green': row.Green, 'blue': row.Blue} for row in
                  cursor.fetchall()]
        print("Colors returned:", colors)
        return jsonify(colors)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def reformat_path(original_path):
    # Normalize the path to handle mixed slashes
    normalized_path = os.path.normpath(original_path)

    # Split the path into parts
    path_parts = normalized_path.split(os.sep)

    # Extract the relevant parts (last two parts)
    if len(path_parts) >= 3:
        category = path_parts[-2]
        filename = path_parts[-1]
        # Reformat the path
        new_path = os.path.join(category, filename)
        return new_path
    else:
        raise ValueError("Path does not have the expected format")


@app.route('/imagesByColor/<category>', methods=['GET'])
def get_images_by_color(category):
    try:
        color_id = request.args.get('color')
        if not color_id:
            return jsonify({"error": "Color ID is required"}), 400

        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.ImagePath
            FROM Images i
            JOIN LinkImageColor lic ON i.ImageID = lic.ImageID
            JOIN LinkImageCategory licat ON i.ImageID = licat.ImageID
            JOIN Categories c ON licat.CategoryID = c.CategoryID
            WHERE c.CategoryName = ? AND lic.ColorID = ?
        """, (category, color_id))

        images = [row[0] for row in cursor.fetchall()]

        # Reformat the paths
        images = [reformat_path(image) for image in images]

        # Print the paths for debugging
        print("the correct paths:")
        for path in images:
            print(path)

        return jsonify(images)
    except Exception as e:
        app.logger.error(f"Error fetching images: {e}")
        return jsonify({'error': str(e)}), 500


# not work
# Fetch images by color
# @app.route('/imagesByColor/<category>', methods=['GET'])
# def get_images_by_color(category):
#     try:
#         color_id = request.args.get('color')
#         if not color_id:
#             return jsonify({"error": "Color ID is required"}), 400
#         print(color_id)
#         print((category))
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT i.ImagePath
#             FROM Images i
#             JOIN LinkImageColor lic ON i.ImageID = lic.ImageID
#             JOIN LinkImageCategory licat ON i.ImageID = licat.ImageID
#             JOIN Categories c ON licat.CategoryID = c.CategoryID
#             WHERE c.CategoryName = ? AND lic.ColorID = ?
#         """, (category, color_id))
#
#         images = [os.path.join("Database", image.replace("\\", "/")) for image in
#                   [row.ImagePath for row in cursor.fetchall()]]
#
#         # Print the paths for debugging
#         for path in images:
#             print(f"Debug Path: {path}")
#
#         # "Database / Images / Academic_Art / 232331.jpg"
#         # Print the paths for debugging
#         for path in images:
#             print(f"Debug Path: {path}")
#         return jsonify(images)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
#
# Fetch products

# Paths to your image directories
content_path = '../products/inputs_content'
style_path = '../products/inputs_style'
output_path = '../products/outputs'


@app.route('/images', methods=['GET'])
def get_products():
    content_images = os.listdir(content_path)
    style_images = os.listdir(style_path)
    output_images = os.listdir(output_path)

    # Create a mapping of filenames for pairing (content, style, output)
    image_pairs = [
        {
            "content": content_images[i] if i < len(content_images) else None,
            "style": style_images[i] if i < len(style_images) else None,
            "output": output_images[i] if i < len(output_images) else None
        }
        for i in range(max(len(content_images), len(style_images), len(output_images)))
    ]

    return jsonify(image_pairs)


@app.route('/content/<filename>')
def get_content_image(filename):
    return send_from_directory(content_path, filename)


@app.route('/style/<filename>')
def get_style_image(filename):
    return send_from_directory(style_path, filename)


@app.route('/output/<filename>')
def get_output_image(filename):
    return send_from_directory(output_path, filename)


# Directory where your images are stored
IMAGE_DIR = '../Database/Images'

# Global variables to store user inputs
user_preference = None
content_image_path = None
style_image_path = None


@app.route('/submit-number', methods=['POST'])
def submit_number():
    global user_preference
    data = request.get_json()
    user_preference = int(data.get('number'))
    print(f"Received number: {user_preference}")
    return jsonify({'status': 'success'})


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

UPLOAD_FOLDER = './uploads'


@app.route('/images/<category>/<filename>')
def serve_image(category, filename):
    return send_from_directory(os.path.join(IMAGE_DIR, category), filename)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

content_image_path = None


@app.route('/upload-image', methods=['POST'])
def upload_image():
    global content_image_path

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        content_image_path = file_path
        file.save(file_path)
        return jsonify([os.path.join('uploads', file.filename)])


style_image_path = None


@app.route('/upload-style-image', methods=['POST'])
def upload_style_image():
    global style_image_path
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, 'style_image.png')
        style_image_path = file_path
        file.save(file_path)
        return jsonify({'filePath': file_path})


@app.route('/start-processing', methods=['POST'])
def start_processing():
    # global content_image_path, style_image_path
    # data = request.get_json()
    # content_image_path = data.get('contentImage')
    # style_image_path = data.get('styleImage')
    print(f"Starting processing with content image: {content_image_path} and style image: {style_image_path}")
    # Call the main processing function
    start_main_processing()
    return jsonify({'status': 'started'})


def start_main_processing():
    global style_image_path, content_image_path
    # Define the paths
    generated_image_name = "generated_image.png"
    image_path = os.path.join("./outputs", generated_image_name)
    previous_work_folder = "previous_work"

    print("the image_path  path ###############################")
    print(image_path)
    # Create the "previous_work" folder if it doesn't exist
    if not os.path.exists(previous_work_folder):
        os.makedirs(previous_work_folder)

    # Check if the image exists
    if os.path.exists(image_path):
        # Move the existing image to the "previous_work" folder
        shutil.move(image_path, os.path.join(previous_work_folder, generated_image_name))

    # content_image_path = os.path.join("./uploads", content_image_path)
    # style_image_path = os.path.join("./uploads", style_image_path)
    print("the content image path ###############################")
    print(content_image_path)
    print(style_image_path)
    if content_image_path is not None and style_image_path is not None:
        print("really starting!!")
        main_processing(content_image_path, style_image_path, user_preference)


GENERATED_IMAGE = './outputs/generated_image.png'


def check_image_exists(image_path):
    return os.path.exists(image_path) and os.path.isfile(image_path)


@app.route('/get_generated_image', methods=['GET'])
def get_generated_image():
    try:
        if not check_image_exists(GENERATED_IMAGE):
            return jsonify({'error': 'The image is invalid'}), 404

        return send_file(GENERATED_IMAGE, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

# , ssl_context = 'adhoc'
#
# @app.route('/get_generated_image', methods=['GET'])
# def get_generated_image():
#     try:
#         image = os.path.join(GENERATED_IMAGE, 'generated_image.png')
#         # image ='3_stylized-image.png'
#         if not os.path.exists(image) or not os.path.isfile(image):
#             return jsonify({'error': 'The image is invalid'}), 404
#
#         return jsonify(image)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
# def is_image_valid(image_path):
#     """Check if the image is valid by attempting to open it."""
#     try:
#         with Image.open(image_path) as img:
#             img.verify()  # Verify the image is intact
#         return True
#     except Exception as e:
#         return False

#
# @app.route('/check-image', methods=['POST'])
# def check_image():
#     data = request.json
#     image_path = data.get('imagePath')
#
#     if image_path and os.path.exists(image_path) and os.path.isfile(image_path):
#         return jsonify({'valid': True})
#     else:
#         return jsonify({'valid': False}), 400


# TRANSFERRED_IMAGE_PATH = '../images/outputs/generated_chicago2.jpg'
#
# @app.route('/get-transferred-image', methods=['GET'])
# def get_transferred_image():
#     return send_file(TRANSFERRED_IMAGE_PATH, mimetype='image/png')
#
# @app.route('/upload-image', methods=['POST'])
# def upload_image():
#     global content_image_path
#
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
#     if file:
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         content_image_path = file_path
#         file.save(file_path)
#         return send_from_directory("uploads", file_path)
#
#         # return jsonify({'filePath': os.path.join('uploads', file.filename)})

#
# @app.route('/upload-image', methods=['POST'])
# def upload_image():
#     global content_image_path
#
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
#     if file:
#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         content_image_path = file_path
#         file.save(file_path)
#         return jsonify({'filePath': file_path})

# Fetch images by color
#
# @app.route('/images_by_color/<category>', methods=['GET'])
# def get_images_by_color(category):
#     try:
#         category_dir = os.path.join(IMAGE_DIR, category)
#         if not os.path.exists(category_dir) or not os.path.isdir(category_dir):
#             return jsonify({'error': 'Category not found'}), 404
#
#         color_id = request.args.get('color')
#
#         if color_id:
#             cursor = conn.cursor()
#             cursor.execute("""
#                 SELECT i.ImagePath
#                 FROM Images i
#                 JOIN LinkImageColor lic ON i.ImageID = lic.ImageID
#                 JOIN LinkImageCategory licat ON i.ImageID = licat.ImageID
#                 JOIN Categories c ON licat.CategoryID = c.CategoryID
#                 WHERE c.CategoryName = ? AND lic.ColorID = ?
#             """, category, color_id)
#             images = [row.ImagePath for row in cursor.fetchall()]
#         else:
#             images = [os.path.join(category, f) for f in os.listdir(category_dir) if
#                       os.path.isfile(os.path.join(category_dir, f))]
#
#         return jsonify(images)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
#

# Fetch images by color
#
# @app.route('/images_by_color/<category>', methods=['GET'])
# def get_images_by_color(category):
#     try:
#         category_dir = os.path.join(IMAGE_DIR, category)
#         if not os.path.exists(category_dir) or not os.path.isdir(category_dir):
#             return jsonify({'error': 'Category not found'}), 404
#
#         color_id = request.args.get('color')
#
#         if color_id:
#             cursor = conn.cursor()
#             cursor.execute("""
#                 SELECT i.ImagePath
#                 FROM Images i
#                 JOIN LinkImageColor lic ON i.ImageID = lic.ImageID
#                 JOIN LinkImageCategory licat ON i.ImageID = licat.ImageID
#                 JOIN Categories c ON licat.CategoryID = c.CategoryID
#                 WHERE c.CategoryName = ? AND lic.ColorID = ?
#             """, category, color_id)
#             images = [row.ImagePath for row in cursor.fetchall()]
#         else:
#             images = [os.path.join(category, f) for f in os.listdir(category_dir) if
#                       os.path.isfile(os.path.join(category_dir, f))]
#
#         return jsonify(images)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
