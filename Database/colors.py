import os
import pyodbc

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from color_classification import dominant_colors

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=(LocalDB)\MSSQLLocalDB;'
                      'Database=Images;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()



def color_exists(color_rgb):
    # Convert RGB values to Python integers
    color_rgb_int = tuple(int(value) for value in color_rgb)
    cursor.execute("SELECT COUNT(*) FROM [dbo].[DominantColors] WHERE [Red] = ? and [Green] = ? and [Blue] = ?",
                   color_rgb_int)
    count = cursor.fetchone()[0]
    return count > 0



def show_image(image_path):
    """
    Open and display an image using Matplotlib.

    Parameters:
        image_path (str): The path to the image file.

    Returns:
        None
    """
    # Open the image
    img = mpimg.imread(image_path)

    # Display the image
    plt.imshow(img)
    plt.axis('off')  # Turn off axis
    plt.show()


cursor.execute("select [ImagePath],[ImageID] from [dbo].[Images]")
images_path = cursor.fetchall()
print(images_path)

# Create a dictionary to store image IDs and their dominant colors
image_colors_dict = {}

for image_path, image_id in images_path:
    # Extract dominant colors for each image
    dominant_colors_tuple = dominant_colors(image_path, 5)
    # Store image ID and dominant colors in the dictionary
    image_colors_dict[image_id] = (image_path, dominant_colors_tuple)

# Now image_colors_dict contains image IDs as keys and tuples of image path and dominant colors as values
print(image_colors_dict)

# Now iterate over image_colors_dict and insert data into the SQL table
for image_id, (image_path, dominant_colors) in image_colors_dict.items():
    for color in dominant_colors:
        if not color_exists(color):
            color_rgb_int = tuple(int(value) for value in color)

            cursor.execute("INSERT INTO [dbo].[DominantColors] VALUES(?,?,?)", color_rgb_int)
            cursor.execute("SELECT SCOPE_IDENTITY() AS ColorID")
            color_id = cursor.fetchone()[0]
        else:
            color_rgb_int = tuple(int(value) for value in color)

            cursor.execute("SELECT [ColorID] FROM [dbo].[DominantColors] WHERE [Red] = ? and [Green] = ? and [Blue] = ?",
                           color_rgb_int)
            color_id = cursor.fetchone()[0]
            # Assuming each color in dominant_colors is represented as (R, G, B)
        # Insert image ID and color ID into LinkImageColor table
        cursor.execute("INSERT INTO LinkImageColor (ImageID, ColorID) VALUES (?, ?)", (image_id, color_id))

# Insert into LinkImageColor table
#  for image_id, color_id in image_colors:
#     cursor.execute("INSERT INTO LinkImageColor (ImageID, ColorID) VALUES (?, ?)", image_id, color_id)

conn.commit()
conn.close()
