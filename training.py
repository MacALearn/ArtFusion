# training.py
import tensorflow as tf
from utils import clip_0_1
from utils import *


# implements:
# style_content_loss, train_step


# TensorFlow graph:
@tf.function()
def train_step(image, extractor, opt, style_targets, style_weight, num_style_layers, content_targets,
               content_weight, num_content_layers):
    # record the previous steps
    with tf.GradientTape() as tape:
        outputs = extractor(image)
        loss = style_content_loss(outputs, style_targets, style_weight, num_style_layers, content_targets,
                                  content_weight, num_content_layers)
    # Computes the gradient of the loss with respect to the image.
    # The tape.gradient method uses the operations recorded in the GradientTape context to compute these gradients.
    grad = tape.gradient(loss, image)
    # updates the image using the computed gradients.
    opt.apply_gradients([(grad, image)])
    # ensure its pixel values remain in the range [0, 1]
    image.assign(clip_0_1(image))


@tf.function()
def second_train_step(image, extractor, opt, style_targets, style_weight, num_style_layers, content_targets,
                      content_weight, num_content_layers, total_variation_weight):
    # Ensure that image tensor has the correct shape
    if len(image.shape) == 3:
        image = tf.expand_dims(image, axis=0)  # Add batch dimension
    elif len(image.shape) != 4:
        raise ValueError("Input image tensor must have either 3 or 4 dimensions.")

    with tf.GradientTape() as tape:
        outputs = extractor(image)
        loss = style_content_loss(outputs, style_targets, style_weight, num_style_layers, content_targets,
                                  content_weight, num_content_layers)
        loss += total_variation_weight * tf.image.total_variation(image)

    grad = tape.gradient(loss, image)
    opt.apply_gradients([(grad, image)])
    image.assign(clip_0_1(image))


def style_content_loss(outputs, style_targets, style_weight, num_style_layers, content_targets, content_weight,
                       num_content_layers):
    style_outputs = outputs['style']
    content_outputs = outputs['content']
    # compute loss between the output_image to the input_style
    style_loss = tf.add_n([tf.reduce_mean((style_outputs[name] - style_targets[name]) ** 2)
                           for name in style_outputs.keys()])

    # Normalization
    style_loss *= style_weight / num_style_layers

    content_loss = tf.add_n([tf.reduce_mean((content_outputs[name] - content_targets[name]) ** 2)
                             for name in content_outputs.keys()])
    content_loss *= content_weight / num_content_layers
    loss = style_loss + content_loss
    return loss


