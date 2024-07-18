from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from is_valid_path import check_image_paths
import os
import pyodbc

# IMAGE_DIR = '../Database/Images'  # Ensure this is the correct path
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# SQL Server connection setup

# conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
#                       'Server=(LocalDB)\MSSQLLocalDB;'
#                       'Database=Images;'
#                       'Trusted_Connection=yes;')


@app.route('/')
def hello_world():
    return 'Hello, World!'


def get_db_connection():
    try:
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server=(LocalDB)\MSSQLLocalDB;'
                              'Database=Images;'
                              'Trusted_Connection=yes;')
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to database: {e}")
        return None


@app.route('/categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT CategoryName FROM Categories")
        categories = [row.CategoryName for row in cursor.fetchall()]
        print(categories)
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# @app.route('/images/<category>', methods=['GET'])
# def get_images(category):
#     color_id = request.args.get('color')
#     cursor = conn.cursor()
#
#     try:
#         cursor.execute("SELECT ImagePath FROM Images")
#         image_paths = [row.ImagePath for row in cursor.fetchall()]
#
#         missing_files = []
#         for image_path in image_paths:
#             full_path = os.path.join(IMAGE_DIR, image_path.replace('\\', '/'))
#             full_path.replace('\\', '/')
#             if not os.path.isfile(full_path):
#                 missing_files.append(full_path)
#             else:
#                 full_files.append(full_path)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         cursor.close()
#         conn.close()
#     return jsonify(full_files)
#
# except Exception as e:
# return jsonify({'error': str(e)}), 500


@app.route('/images/<category>', methods=['GET'])
def get_images(category):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    cursor = conn.cursor( 

    try:
        full_files = []

        cursor.execute("""
            SELECT Images.ImagePath
            FROM Images
            JOIN LinkImageCategory ON Images.ImageID = LinkImageCategory.ImageID
            JOIN Categories ON Categories.CategoryID = LinkImageCategory.CategoryID
            WHERE Categories.CategoryName = ?
        """, category)
        images = [row.ImagePath.replace('\\', '/') for row in cursor.fetchall()]

        IMAGE_DIR = '../Database'  # Ensure this is the correct path

    #  try:
    #      cursor.execute("SELECT ImagePath FROM Images")
    #      image_paths = [row.ImagePath for row in cursor.fetchall()]

    #      missing_files = []
    #      for image_path in image_paths:
    #          full_path = os.path.join(IMAGE_DIR, image_path.replace('\\', '/'))
    #          full_path.replace('\\', '/')
    #          if not os.path.isfile(full_path):
    #              missing_files.append(full_path)
    #          else:
    #              full_files.append(full_path)
    #  except Exception as e:
    #      print(f"An error occurred: {e}")

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
    return jsonify(images)


# colors ---


# @app.route('/colors/<category>', methods=['GET'])
# def get_colors(category):
#     try:
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT DISTINCT dc.ColorID, dc.Red, dc.Green, dc.Blue
#             FROM DominantColors dc
#             JOIN LinkImageColor lic ON dc.ColorID = lic.ColorID
#             JOIN LinkImageCategory licat ON lic.ImageID = licat.ImageID
#             JOIN Categories c ON licat.CategoryID = c.CategoryID
#             WHERE c.CategoryName = ?
#         """, category)
#         colors = [{'id': row.ColorID, 'red': row.Red, 'green': row.Green, 'blue': row.Blue} for row in
#                   cursor.fetchall()]
#         print("Colors returned:", colors)
#         return jsonify(colors)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


@app.route('/image/<path:image_path>', methods=['GET'])
def serve_image(image_path):
    return send_from_directory('', image_path)


if __name__ == '__main__':
    app.run(debug=True)
