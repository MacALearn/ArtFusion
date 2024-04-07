import tensorflow as tf





def total_variation(image):
    """Compute total variation loss for an image or batch of images.

    Args:
        image: A 3-D or 4-D Tensor representing an image or batch of images.
               For a single image: [height, width, channels]
               For a batch of images: [batch, height, width, channels]

    Returns:
        The total variation loss for the input image or batch of images.
        If input is 4-D, returns a 1-D tensor of shape [batch].
        If input is 3-D, returns a scalar tensor.
    """
    ndims = tf.rank(image)

    if ndims == 3:
        # Calculate the difference of neighboring pixel-values.
        pixel_dif1 = image[:, :-1, :, :] - image[:, 1:, :, :]
        pixel_dif2 = image[:-1, :, :, :] - image[1:, :, :, :]

        # Calculate the total variation by taking the L1 norm of pixel-differences.
        tot_var = tf.reduce_mean(tf.abs(pixel_dif1)) + tf.reduce_mean(tf.abs(pixel_dif2))
    elif ndims == 4:
        # Calculate the difference of neighboring pixel-values.
        pixel_dif1 = image[:, :, :-1, :] - image[:, :, 1:, :]
        pixel_dif2 = image[:, :-1, :, :] - image[:, 1:, :, :]

        # Calculate the total variation by taking the L1 norm of pixel-differences.
        tot_var = (
                tf.reduce_mean(tf.abs(pixel_dif1)) + tf.reduce_mean(tf.abs(pixel_dif2)))

        # Only sum for the last 3 axis.
        tot_var = tf.reduce_sum(tot_var, axis=[1, 2, 3])
    else:
        raise ValueError('\'image\' must be either 3 or 4-dimensional.')

    return tot_var

# Example usage:
# image = tf.placeholder(tf.float32, shape=[None, height, width, channels])  # Assuming height, width, channels are defined
# total_var = total_variation_loss(image)
