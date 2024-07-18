# import numpy as np
# from sklearn.cluster import KMeans
# from skimage import io
# import matplotlib.pyplot as plt
#
#
# def dominant_colors(image_path, k):
#     # Step 1: Load the image
#     image = io.imread(image_path)
#
#     # Step 2: Reshape the image into a 2D array of pixels
#     pixels = np.reshape(image, (-1, 3))
#
#     # Step 3: Apply KMeans clustering
#     kmeans = KMeans(n_clusters=k, random_state=42)
#     kmeans.fit(pixels)
#
#     # Step 4: Get the centroid colors
#     centroid_colors = kmeans.cluster_centers_.astype(int)
#
#     # Step 5: Return the dominant K colors as a tuple of numbers
#     dominant_colors_rgb = tuple(map(tuple, centroid_colors))
#
#     return dominant_colors_rgb
#
#
# # Example usage:
# image_path = "C:/Users/USER/Desktop/the_scream.jpg"
# k = 3  # Number of dominant colors to extract
# dominant_colors_tuple = dominant_colors(image_path, k)
# print("Dominant colors (in RGB):", dominant_colors_tuple)



# import numpy as np
# from sklearn.cluster import KMeans
# from skimage import io
# import matplotlib.pyplot as plt
#
#
# def dominant_colors(image_path, k):
#     # Step 1: Load the image
#     image = io.imread(image_path)
#
#     # Step 2: Reshape the image into a 2D array of pixels
#     pixels = np.reshape(image, (-1, 3))
#
#     # Step 3: Apply KMeans clustering
#     kmeans = KMeans(n_clusters=k, random_state=42)
#     kmeans.fit(pixels)
#
#     # Step 4: Get the centroid colors
#     centroid_colors = kmeans.cluster_centers_.astype(int)
#
#     # Step 5: Return the dominant K colors as a tuple of numbers
#     dominant_colors_rgb = tuple(map(tuple, centroid_colors))
#
#     # Visualization
#     plt.figure(figsize=(8, 6))
#     plt.subplot(1, 2, 1)
#     plt.imshow(image)
#     plt.title('Original Image')
#     plt.axis('off')
#
#     plt.subplot(1, 2, 2)
#     plt.title('Dominant Colors')
#     for i, color in enumerate(centroid_colors):
#         plt.fill_betweenx(y=[0, 1], x1=i, x2=i+1, color=color/255, edgecolor='none')
#     plt.xticks([])
#     plt.yticks([])
#     plt.xlim(0, k)
#
#     plt.tight_layout()
#     plt.show()
#
#     return dominant_colors_rgb
#
#
# # Example usage:
# image_path = "C:/Users/USER/Desktop/203576.jpg"
# k = 3  # Number of dominant colors to extract
# dominant_colors_tuple = dominant_colors(image_path, k)
# print("Dominant colors (in RGB):", dominant_colors_tuple)
#


import numpy as np
from sklearn.cluster import KMeans
from skimage import io
import matplotlib.pyplot as plt


def dominant_colors(image_path, k):
    # Step 1: Load the image
    image = io.imread(image_path)

    # Step 2: Reshape the image into a 2D array of pixels
    pixels = np.reshape(image, (-1, 3))

    # Step 3: Apply KMeans clustering
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(pixels)

    # Step 4: Get the centroid colors and labels for each pixel
    centroid_colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_

    # Step 5: Map each pixel to its closest centroid color
    segmented_image = centroid_colors[labels].reshape(image.shape)

    # Visualization
    plt.figure(figsize=(12, 6))

    # Original image
    plt.subplot(1, 3, 1)
    plt.imshow(image)
    plt.title('Original Image')
    plt.axis('off')

    # Dominant colors
    plt.subplot(1, 3, 2)
    plt.title('Dominant Colors')
    for i, color in enumerate(centroid_colors):
        plt.fill_betweenx(y=[0, 1], x1=i, x2=i+1, color=color/255, edgecolor='none')
    plt.xticks([])
    plt.yticks([])
    plt.xlim(0, k)

    # Image with only dominant colors
    plt.subplot(1, 3, 3)
    plt.imshow(segmented_image)
    plt.title('Image with Dominant Colors')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    return tuple(map(tuple, centroid_colors))


# Example usage:
image_path = "C:/Users/USER/Desktop/203576.jpg"
k = 3  # Number of dominant colors to extract
dominant_colors_tuple = dominant_colors(image_path, k)
print("Dominant colors (in RGB):", dominant_colors_tuple)
