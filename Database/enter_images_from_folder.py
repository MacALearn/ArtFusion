import os
import pyodbc
import numpy as np
from sklearn.cluster import KMeans
from skimage import io
import matplotlib.pyplot as plt


def dominant_colors(image_path, k):
    # Update the correct path
    if not image_path.startswith("./"):
        image_path = "./" + image_path

    # Step 1: Load the image
    image = io.imread(image_path)

    # Step 2: Reshape the image into a 2D array of pixels
    pixels = np.reshape(image, (-1, 3))

    # Step 3: Apply KMeans clustering
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(pixels)

    # Step 4: Get the centroid colors
    centroid_colors = kmeans.cluster_centers_.astype(int)

    # Step 5: Return the dominant K colors as a tuple of numbers
    dominant_colors_rgb = tuple(map(tuple, centroid_colors))

    return dominant_colors_rgb





def insert_image_data(image_path, categories, k, conn_str):
    # Connect to the database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Check if image path already exists in the Images table
    cursor.execute("SELECT ImageID FROM Images WHERE ImagePath = ?", (image_path,))
    image_id = cursor.fetchone()

    if image_id:
        image_id = image_id[0]
    else:
        # Insert the image into the Images table
        cursor.execute("INSERT INTO Images (ImagePath) OUTPUT Inserted.ImageID VALUES (?)", (image_path,))
        image_id = cursor.fetchone()[0]

    # Insert the categories into the LinkImageCategory table
    for category in categories:
        cursor.execute("SELECT CategoryID FROM Categories WHERE CategoryName = ?", (category,))
        category_id = cursor.fetchone()
        if category_id:
            category_id = category_id[0]
            cursor.execute("SELECT * FROM LinkImageCategory WHERE ImageID = ? AND CategoryID = ?",
                           (image_id, category_id))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO LinkImageCategory (ImageID, CategoryID) VALUES (?, ?)",
                               (image_id, category_id))

    # Get the dominant colors
    dominant_colors_list = dominant_colors(image_path, k)

    # Insert the dominant colors into the DominantColors table and LinkImageColor table
    for color in dominant_colors_list:
        # Convert numpy int32 to Python int
        color = tuple(map(int, color))
        cursor.execute("SELECT ColorID FROM DominantColors WHERE Red = ? AND Green = ? AND Blue = ?", color)
        color_id = cursor.fetchone()
        if not color_id:
            cursor.execute("INSERT INTO DominantColors (Red, Green, Blue) OUTPUT Inserted.ColorID VALUES (?, ?, ?)",
                           color)
            color_id = cursor.fetchone()[0]
        else:
            color_id = color_id[0]

        cursor.execute("SELECT * FROM LinkImageColor WHERE ImageID = ? AND ColorID = ?", (image_id, color_id))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO LinkImageColor (ImageID, ColorID) VALUES (?, ?)", (image_id, color_id))

    # Commit the transaction
    conn.commit()
    # Close the connection
    conn.close()


def process_images(folder_path, categories, k, conn_str):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                if image_path.startswith('./'):
                    image_path = image_path[2:]
                # print(image_path)
                insert_image_data(image_path, categories, k, conn_str)


# Example usage
conn_str = ('Driver={ODBC Driver 17 for SQL Server};'
            'Server=(LocalDB)\\MSSQLLocalDB;'
            'Database=Images;'
            'Trusted_Connection=yes;')
folder_path = './Images/Academic_Art'
categories = ['Western_Medieval']

# 'Academic_Art' , 'Art_Nouveau', 'Japanese_Art', 'Primitivism', 'Realism', 'Symbolism', 'Western_Medieval',
#               'Other'

k = 3

process_images(folder_path, categories, k, conn_str)
