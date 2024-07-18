import os
import pyodbc


# Function to get list of image paths from a directory
def get_image_paths(directory):
    image_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_paths.append(os.path.join(root, file))
    return image_paths


conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=(LocalDB)\MSSQLLocalDB;'
                      'Database=Images;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
main_directory = '../Database/Images'  # Adjust the relative path as needed

# Get list of category folders
category_folders = [folder for folder in os.listdir(main_directory) if
                    os.path.isdir(os.path.join(main_directory, folder))]
print(category_folders)
print("##########")

# Insert images and link them to [LinkCategoriesImage]
for category_folder in category_folders:
    category_path = os.path.join(main_directory, category_folder)
    image_paths = get_image_paths(category_path)

    # Insert image paths into Images table with relative paths
    for image_path in image_paths:
        relative_path = os.path.relpath(image_path, os.path.dirname(__file__))
        print(relative_path)
        cursor.execute("INSERT INTO Images (ImagePath) OUTPUT INSERTED.ImageID VALUES (?)", relative_path)
        image_id = cursor.fetchone()[0]
        # Insert into LinkImageCategory table
        cursor.execute(
            "INSERT INTO LinkImageCategory (ImageID, CategoryID) VALUES (?, (SELECT CategoryID FROM Categories WHERE CategoryName = ?))",
         image_id, category_folder)

image_directory = '../picture'  # Adjust the relative path as needed

# Get list of image paths
image_paths = get_image_paths(image_directory)

# Insert image paths into Images table with relative paths
for image_path in image_paths:
    relative_path = os.path.relpath(image_path, os.path.dirname(__file__))
    cursor.execute("INSERT INTO Images (ImagePath) VALUES (?)", relative_path)
print("Initialization complete.")

cursor.execute("select * from Categories")
rows = cursor.fetchall()
for row in rows:
    print(row)

# # Specify the root folder containing category folders
# root_folder = r'C:\Users\USER\Documents\תכנות\פרויקט סופי\python\Database\Images'
#
# # Traverse the directory structure and insert data
# traverse_directory(root_folder, cursor)

conn.commit()
conn.close()
