# brandcrowd

import os
import tensorflow as tf
import tensorflow_probability as tfp
import matplotlib.pyplot as plt
import matplotlib as mpl
from model import vgg_layers, StyleContentModel
import shutil
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


def gram_matrix(input_tensor):
    result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
    input_shape = tf.shape(input_tensor)
    num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)
    return result / num_locations


def style_content_loss(outputs, style_targets, content_targets, style_weight, content_weight, num_style_layers, num_content_layers):
    style_outputs = outputs['style']
    content_outputs = outputs['content']

    style_loss = tf.add_n([tf.reduce_mean((style_outputs[name] - style_targets[name])**2)
                           for name in style_outputs.keys()])
    style_loss *= style_weight / num_style_layers

    content_loss = tf.add_n([tf.reduce_mean((content_outputs[name] - content_targets[name])**2)
                             for name in content_outputs.keys()])
    content_loss *= content_weight / num_content_layers

    loss = style_loss + content_loss
    return loss


def main_processing(content_path, style_path, user_preference):
    content_image = load_img(content_path)
    style_image = load_img(style_path)

    style_layers = ['block1_conv1',
                    'block2_conv1',
                    'block3_conv1',
                    'block4_conv1',
                    'block5_conv1']

    content_layers = ['block5_conv2']

    if user_preference <= 2:
        content_layers.extend(['block4_conv3', 'block3_conv3'])
    elif user_preference <= 5:
        content_layers.append('block4_conv3')
    else:
        pass

    print("Selected content layers:", content_layers)

    num_content_layers = len(content_layers)
    num_style_layers = len(style_layers)

    style_extractor = vgg_layers(style_layers)
    style_outputs = style_extractor(style_image * 255)

    extractor = StyleContentModel(style_layers, content_layers)

    style_targets = extractor(style_image)['style']
    content_targets = extractor(content_image)['content']

    image = tf.Variable(content_image)

    style_weight = 1e-2
    content_weight = 1e4

    total_variation_weight = 10

    def value_and_gradients_function(params):
        with tf.GradientTape() as tape:
            tape.watch(image)
            image.assign(tf.reshape(params, image.shape))
            outputs = extractor(image)
            loss = style_content_loss(outputs, style_targets, content_targets, style_weight, content_weight,
                                      num_style_layers, num_content_layers)
            loss += total_variation_weight * tf.image.total_variation(image)

        gradients = tape.gradient(loss, image)
        return loss, tf.reshape(gradients, [-1])

    initial_position = tf.reshape(image, [-1])

    print("Initial position shape:", initial_position.shape)

    def _restricted_func(t, position):
        print("t shape:", t.shape)
        print("position shape:", position.shape)
        t = _broadcast(t, position)
        print("broadcast t shape:", t.shape)
        return t

    def _broadcast(t, position):
        print("Broadcasting t with shape:", t.shape, "to position with shape:", position.shape)
        return tf.broadcast_to(t, position.shape)

    optim_results = tfp.optimizer.lbfgs_minimize(
        value_and_gradients_function,
        initial_position=initial_position,
        num_correction_pairs=10,
        tolerance=1e-8,
        max_iterations=100
    )

    if optim_results.converged:
        image.assign(tf.reshape(optim_results.position, image.shape))
    else:
        print("L-BFGS did not converge")

    file_name = '3_steps_stylized-image.png'
    tensor_to_image(image).save(file_name)

    generated_image_name = "generated_image.png"
    image_path = os.path.join("outputs", generated_image_name)
    previous_work_folder = "previous_work"

    if not os.path.exists(previous_work_folder):
        os.makedirs(previous_work_folder)

    if os.path.exists(image_path):
        shutil.move(image_path, os.path.join(previous_work_folder, generated_image_name))

    tensor_to_image(image).save(image_path)

    image_path = os.path.join("outputs", "out_put.png")
    tensor_to_image(image).save(image_path)

    if not os.path.exists("process"):
        os.makedirs("process")

    start = time.time()
    epochs = 10
    steps_per_epoch = 100
    step = 0

    for n in range(epochs):
        for m in range(steps_per_epoch):
            step += 1
            image.assign(tf.reshape(optim_results.position, image.shape))
            outputs = extractor(image)
            loss = style_content_loss(outputs, style_targets, content_targets, style_weight, content_weight,
                                      num_style_layers, num_content_layers)
            loss += total_variation_weight * tf.image.total_variation(image)
            print(".", end='', flush=True)
        print("Train step: {}".format(step))
        file_name = str(n) + '_' + 'stylized-image.png'
        generated_image_path = os.path.join("process", file_name)
        tensor_to_image(image).save(generated_image_path)
        tensor_to_image(image).save(image_path)

    end = time.time()
    print("Total time: {:.1f}".format(end - start))

    file_name = 'middle_stylized-image.png'
    tensor_to_image(image).save(file_name)

    optim_results = tfp.optimizer.lbfgs_minimize(
        value_and_gradients_function,
        initial_position=initial_position,
        num_correction_pairs=10,
        tolerance=1e-8,
        max_iterations=100
    )

    if optim_results.converged:
        image.assign(tf.reshape(optim_results.position, image.shape))
    else:
        print("L-BFGS did not converge")

    start = time.time()
    epochs = 10
    steps_per_epoch = 100
    step = 0

    for n in range(epochs):
        for m in range(steps_per_epoch):
            step += 1
            image.assign(tf.reshape(optim_results.position, image.shape))
            outputs = extractor(image)
            loss = style_content_loss(outputs, style_targets, content_targets, style_weight, content_weight,
                                      num_style_layers, num_content_layers)
            loss += total_variation_weight * tf.image.total_variation(image)
            print(".", end='', flush=True)
        print("Train step: {}".format(step))

    end = time.time()
    print("Total time: {:.1f}".format(end - start))

    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    print("image is getting save!")
    generated_image_name = "generated_image.png"
    image_path = os.path.join("outputs", generated_image_name)
    tensor_to_image(image).save(image_path)


if __name__ == "__main__":
    content_path = 'C:\\Users\\USER\\Desktop\\chicago.jpg'
    style_path = 'C:\\Users\\USER\\Desktop\\the_scream.jpg'
    user_preference = 9  # Adjust as needed
    main_processing(content_path, style_path, user_preference)