from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import pyodbc

app = Flask(__name__)
CORS(app)

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=(LocalDB)\MSSQLLocalDB;'
                      'Database=Images;'
                      'Trusted_Connection=yes;')


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT CategoryName FROM Categories")
        categories = [row.CategoryName for row in cursor.fetchall()]
        print(categories)
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/images/<category>', methods=['GET'])
def get_images(category):
    color_id = request.args.get('color')
    try:
        full_files = []
        cursor = conn.cursor()
        if color_id:
            query = """
                SELECT i.ImagePath
                FROM Images i
                JOIN LinkImageColor lic ON i.ImageID = lic.ImageID
                JOIN LinkImageCategory licat ON i.ImageID = licat.ImageID
                JOIN Categories c ON licat.CategoryID = c.CategoryID
                WHERE c.CategoryName = ? AND lic.ColorID = ?
            """
            cursor.execute(query, category, color_id)
        else:
            query = """
                SELECT i.ImagePath
                FROM Images i
                JOIN LinkImageCategory licat ON i.ImageID = licat.ImageID
                JOIN Categories c ON licat.CategoryID = c.CategoryID
                WHERE c.CategoryName = ?
            """
            cursor.execute(query, category)

        IMAGE_DIR = '../Database'  # Ensure this is the correct path
        image_paths = [row.ImagePath for row in cursor.fetchall()]

        for image_path in image_paths:
            full_path = os.path.join(IMAGE_DIR, image_path.replace('\\', '/'))
            if os.path.isfile(full_path):
                full_files.append(full_path)

        print("Full file paths returned:", full_files)
        return jsonify(full_files)
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
        colors = [{'id': row.ColorID, 'red': row.Red, 'green': row.Green, 'blue': row.Blue} for row in cursor.fetchall()]
        print("Colors returned:", colors)
        return jsonify(colors)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/image/<path:image_path>', methods=['GET'])
def serve_image(image_path):
    return send_from_directory('', image_path)

if __name__ == '__main__':
    app.run(debug=True)
