import os
import pyodbc


def check_image_paths():
    # SQL Server connection setup

    full_files = []
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=(LocalDB)\MSSQLLocalDB;'
                          'Database=Images;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()

    IMAGE_DIR = '../Database'  # Ensure this is the correct path

    try:
        cursor.execute("SELECT ImagePath FROM Images")
        image_paths = [row.ImagePath for row in cursor.fetchall()]

        missing_files = []
        for image_path in image_paths:
            full_path = os.path.join(IMAGE_DIR, image_path.replace('\\', '/'))
            full_path.replace('\\', '/')

            print(full_path+"###")
            if not os.path.isfile(full_path):
                missing_files.append(full_path)
            else:
                full_files.append(full_path)

        if missing_files:
            print("The following image paths are incorrect or the files are missing:")
            for path in missing_files:
                print(path)
        else:
            print("All image paths are correct.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

    return full_files


# Run the function
check_image_paths()



@app.route('/colors/<category>', methods=['GET'])
def get_colors(category):
    try:
        cursor = conn.cursor()

        # First query to get colors related to the specified category
        cursor.execute("""
            SELECT DISTINCT dc.ColorID, dc.Red, dc.Green, dc.Blue
            FROM DominantColors dc
            JOIN LinkImageColor lic ON dc.ColorID = lic.ColorID
            JOIN LinkImageCategory licat ON lic.ImageID = licat.ImageID
            JOIN Categories c ON licat.CategoryID = c.CategoryID
            WHERE c.CategoryName = ?
        """, (category,))

        colors = [{'id': row[0], 'red': row[1], 'green': row[2], 'blue': row[3]} for row in cursor.fetchall()]

        # Verify colors belong to images in the specified category
        verified_colors = []
        for color in colors:
            cursor.execute("""
                SELECT i.ImagePath
                FROM Images i
                JOIN LinkImageColor lic ON i.ImageID = lic.ImageID
                WHERE lic.ColorID = ?
            """, (color['id'],))

            image_paths = [row[0] for row in cursor.fetchall()]
            for image_path in image_paths:
                # Extract the category from the image path
                image_category = image_path.split('/')[1]
                if image_category == category:
                    verified_colors.append(color)
                    break

        print("Verified colors returned:", verified_colors)
        return jsonify(verified_colors)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
