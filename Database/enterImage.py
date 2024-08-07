import pyodbc
import numpy as np
from sklearn.cluster import KMeans
from skimage import io


def dominant_colors(image_path, k):
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
    dominant_colors_rgb = [tuple(map(int, color)) for color in centroid_colors]

    return dominant_colors_rgb

def insert_image_data(image_path, categories, k, conn_str):
    # Connect to the database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Step 1: Insert the image into the Images table
    cursor.execute("INSERT INTO Images (ImagePath) OUTPUT Inserted.ImageID VALUES (?)", (image_path,))
    image_id = cursor.fetchone()[0]

    # Step 2: Insert the categories into the LinkImageCategory table
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

    # Step 3: Get the dominant colors
    dominant_colors_list = dominant_colors(image_path, k)

    # Step 4: Insert the dominant colors into the DominantColors table and LinkImageColor table
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


# Example usage
conn_str = ('Driver={ODBC Driver 17 for SQL Server};'
            'Server=(LocalDB)\\MSSQLLocalDB;'
            'Database=Images;'
            'Trusted_Connection=yes;')
image_path = "Images/Academic_Art/232337.jpg"
categories = ['Academic_Art', 'Art_Nouveau', 'Japanese_Art', 'Primitivism', 'Realism', 'Symbolism', 'Western_Medieval', 'Other']
k = 3

insert_image_data(image_path, categories, k, conn_str)
