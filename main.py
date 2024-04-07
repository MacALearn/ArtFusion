import os
import tensorflow as tf
import IPython.display as display
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['figure.figsize'] = (12, 12)
mpl.rcParams['axes.grid'] = False
import numpy as np
import PIL.Image
import functools
from utils import *
from model import vgg_layers, StyleContentModel
from training import *
import time

# Load compressed models from tensorflow_hub
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# Load images
content_path = "C:/Users/USER/Desktop/chicago.jpg"
style_path = "C:/Users/USER/Desktop/the_scream.jpg"

# content_path = tf.keras.utils.get_file('YellowLabradorLooking_new.jpg', 'https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg')
# style_path = tf.keras.utils.get_file('kandinsky5.jpg','https://storage.googleapis.com/download.tensorflow.org/example_images/Vassily_Kandinsky%2C_1913_-_Composition_7.jpg')

content_image = load_img(content_path)
style_image = load_img(style_path)

plt.subplot(1, 2, 1)
imshow(content_image, 'Content Image')

plt.subplot(1, 2, 2)
imshow(style_image, 'Style Image')

# plt.show(block=False)

# Build VGG model

x = tf.keras.applications.vgg19.preprocess_input(content_image * 255)
x = tf.image.resize(x, (224, 224))
# vgg = tf.keras.applications.VGG19(include_top=True, weights='imagenet')
# prediction_probabilities = vgg(x)
vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')

style_layers = ['block1_conv1',
                'block2_conv1',
                'block3_conv1',
                'block4_conv1',
                'block5_conv1']

# Get user input for how much the content matters
user_preference = int(input("On a scale of 1 to 10, how much does the content matter to you? "))

# Define the default content layer
content_layers = ['block5_conv2']

# Adjust content layers based on user preference
if user_preference >= 8:
    # Add 2 more layers
    content_layers.extend(['block4_conv3', 'block3_conv3'])
elif user_preference >= 5:
    # Add another layer
    content_layers.append('block4_conv3')
elif user_preference >= 1:
    # Keep the default layer
    pass
else:
    print("Invalid input. Please enter a number between 1 and 10.")

# Print the final content layers
print("Selected content layers:", content_layers)

num_content_layers = len(content_layers)
num_style_layers = len(style_layers)

# Extract features
style_extractor = vgg_layers(style_layers)
style_outputs = style_extractor(style_image * 255)

# Display style output information
for name, output in zip(style_layers, style_outputs):
    print(name)
    print("  shape: ", output.numpy().shape)
    print("  min: ", output.numpy().min())
    print("  max: ", output.numpy().max())
    print("  mean: ", output.numpy().mean())
    print()

# Create StyleContentModel
extractor = StyleContentModel(style_layers, content_layers)

# Get style and content targets
style_targets = extractor(style_image)['style']
content_targets = extractor(content_image)['content']

# Initialize image for training
image = tf.Variable(content_image)

# Training parameters
style_weight = 1e-2
content_weight = 1e4
opt = tf.keras.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)

# 3 training steps

for _ in range(3):
    train_step(image, extractor, opt, style_targets, style_weight, num_style_layers, content_targets,
               content_weight, num_content_layers)

file_name = '3_stylized-image.png'
tensor_to_image(image).save(file_name)
# Display the initial image
tensor_to_image(image)

# making directory if not exists
if not os.path.exists("process"):
    os.makedirs("process")

# FIRST training loop

start = time.time()
epochs = 10
steps_per_epoch = 100

step = 0
try:
    for n in range(epochs):
        for m in range(steps_per_epoch):
            step += 1
            train_step(image, extractor, opt, style_targets, style_weight, num_style_layers, content_targets,
                       content_weight, num_content_layers)
            print(".", end='', flush=True)
        # display.clear_output(wait=True)
        # display.display(tensor_to_image(image))
        # plt.pause(0.1)  # Use plt.pause() to allow the script to continue running
        print("Train step: {}".format(step))
        file_name = str(n) + '_' + 'stylized-image.png'
        generated_image_path = os.path.join("process", file_name)

        tensor_to_image(image).save(generated_image_path)
except KeyboardInterrupt:
    print("Training interrupted by user.")
end = time.time()
print("Total time: {:.1f}".format(end - start))

# saving the result:
file_name = 'first_stylized-image.png'
tensor_to_image(image).save(file_name)

# the variance:
x_deltas, y_deltas = high_pass_x_y(content_image)

plt.figure(figsize=(14, 10))
plt.subplot(2, 2, 1)
imshow(clip_0_1(2 * y_deltas + 0.5), "Horizontal Deltas: Original")

plt.subplot(2, 2, 2)
imshow(clip_0_1(2 * x_deltas + 0.5), "Vertical Deltas: Original")

x_deltas, y_deltas = high_pass_x_y(image)

plt.subplot(2, 2, 3)
imshow(clip_0_1(2 * y_deltas + 0.5), "Horizontal Deltas: Styled")

plt.subplot(2, 2, 4)
imshow(clip_0_1(2 * x_deltas + 0.5), "Vertical Deltas: Styled")

plt.figure(figsize=(14, 10))

sobel = tf.image.sobel_edges(content_image)
plt.subplot(1, 2, 1)
imshow(clip_0_1(sobel[..., 0] / 4 + 0.5), "Horizontal Sobel-edges")
plt.subplot(1, 2, 2)
imshow(clip_0_1(sobel[..., 1] / 4 + 0.5), "Vertical Sobel-edges")

# Continued SECOND training loop

# a weight for the `total_variation_loss`:
total_variation_weight = 30

# Reinitialize the image-variable and the optimizer:
opt = tf.keras.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)

start = time.time()

epochs = 10
steps_per_epoch = 100

step = 0
for n in range(epochs):
    for m in range(steps_per_epoch):
        step += 1
        second_train_step(image, extractor, opt, style_targets, style_weight, num_style_layers, content_targets,
                          content_weight, num_content_layers, total_variation_weight)
        print(".", end='', flush=True)
    display.clear_output(wait=True)
    display.display(tensor_to_image(image))
    print("Train step: {}".format(step))

end = time.time()
print("Total time: {:.1f}".format(end - start))

# saving the result:

if not os.path.exists("outputs"):
    os.makedirs("outputs")
# Extract just the filename from the content image path
content_image_name = os.path.basename(content_path)
generated_image_name = "generated_" + content_image_name
image_path = os.path.join("images", generated_image_name)
image_path = os.path.join("outputs", generated_image_name)
# Save the generated image
tensor_to_image(image).save(image_path)
