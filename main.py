# brandcrowd

import os
import tensorflow as tf
# import IPython.display as display
import matplotlib.pyplot as plt
import matplotlib as mpl
from model import vgg_layers, StyleContentModel
import shutil
from training import *
import time
import numpy as np
import PIL.Image
import functools
from utils import *

# Load compressed models from tensorflow_hub
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

mpl.rcParams['figure.figsize'] = (12, 12)
mpl.rcParams['axes.grid'] = False



os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


# os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = "python"
# Load images
def main_processing(content_path, style_path, user_preference):

    content_image = load_img(content_path)
    style_image = load_img(style_path)

    style_layers = ['block1_conv1',
                    'block2_conv1',
                    'block3_conv1',
                    'block4_conv1',
                    'block5_conv1']

    # user_preference = " getting from the server "

    # Define the default content layer
    content_layers = ['block5_conv2']

    # Adjust content layers based on user preference
    if user_preference <= 2:
        # Add 2 more layers
        content_layers.extend(['block4_conv3', 'block3_conv3'])
    elif user_preference <= 5:
        # Add another layer
        content_layers.append('block4_conv3')
    else:
        # keep the default
        pass

    # Print the final content layers
    print("Selected content layers:", content_layers)

    num_content_layers = len(content_layers)
    num_style_layers = len(style_layers)

    # Extract features
    style_extractor = vgg_layers(style_layers)
    style_outputs = style_extractor(style_image * 255)


    # Create StyleContentModel
    extractor = StyleContentModel(style_layers, content_layers)

    # Get style and content targets
    style_targets = extractor(style_image)['style']
    content_targets = extractor(content_image)['content']

    # Initialize image for training
    image = tf.Variable(content_image)

    # https://keras.io/examples/generative/neural_style_transfer/
    # total_variation_weight = 1e-6
    # style_weight = 1e-6
    # content_weight = 2.5e-8

    # Training parameters
    style_weight = 1e-2
    content_weight = 1e4
    # Adam is combining the advantages of AdaGrad and RMSProp.
    # RMSProp - effective on online and non-stationary problems.
    # AdaGrad - improves performance on problems with sparse gradients
    opt = tf.keras.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)

    # 3 training steps
    for _ in range(3):
        train_step(image, extractor, opt, style_targets, style_weight, num_style_layers, content_targets,
                   content_weight, num_content_layers)
    file_name = '3_steps_stylized-image.png'
    tensor_to_image(image).save(file_name)

    # Define the paths
    generated_image_name = "generated_image.png"
    image_path = os.path.join("outputs", generated_image_name)
    previous_work_folder = "previous_work"

    # Create the "previous_work" folder if it doesn't exist
    if not os.path.exists(previous_work_folder):
        os.makedirs(previous_work_folder)

    # Check if the image exists
    if os.path.exists(image_path):
        # Move the existing image to the "previous_work" folder
        shutil.move(image_path, os.path.join(previous_work_folder, generated_image_name))

    # Continue with the rest of the code
    generated_image_name = "generated_image.png"
    image_path = os.path.join("outputs", generated_image_name)

    # Update the image
    generated_image_name = "generated_image.png"
    image_path = os.path.join("outputs", generated_image_name)

    # Save the generated image
    tensor_to_image(image).save(image_path)

    image_path = os.path.join("outputs", "out_put.png")

    # Save the generated image
    tensor_to_image(image).save(image_path)


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

            generated_image_name = "generated_image.png"
            image_path = os.path.join("outputs", generated_image_name)

            # Save the generated image
            tensor_to_image(image).save(image_path)
    except KeyboardInterrupt:
        print("Training interrupted by user.")
    end = time.time()
    print("Total time: {:.1f}".format(end - start))

    # saving the result:
    file_name = 'middle_stylized-image.png'
    tensor_to_image(image).save(file_name)

    # Continued SECOND training loop

    # a weight for the `total_variation_loss`:
    # total_variation_weight = 30
    total_variation_weight = 10

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
        # display.clear_output(wait=True)
        # display.display(tensor_to_image(image))
        print("Train step: {}".format(step))

    end = time.time()
    print("Total time: {:.1f}".format(end - start))

    # saving the result:

    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    # # Extract just the filename from the content image path
    # content_image_name = os.path.basename(content_path)
    print("image is getting save!")
    generated_image_name = "generated_image.png"
    image_path = os.path.join("outputs", generated_image_name)

    # Save the generated image
    tensor_to_image(image).save(image_path)




