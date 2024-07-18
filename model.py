

# model.py
import tensorflow as tf


# implements:
# vgg_layers, gram_matrix, class StyleContentModel


def vgg_layers(layer_names):
    """ Creates a VGG model that returns a list of intermediate output values."""
    # Load our model. Load pretrained VGG, trained on ImageNet data
    # include_top = false, means to exclude the top of the layers, that are usually used for a classification purposes.
    vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
    vgg.trainable = False

    outputs = [vgg.get_layer(name).output for name in layer_names]

    model = tf.keras.Model([vgg.input], outputs)
    return model


def gram_matrix(input_tensor):
    # Calculate the Gram matrix using Einstein summation
    # this summation intended to compute the dot product between the feature maps across all spatial locations.
    result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
    # Get the shape of the input tensor
    input_shape = tf.shape(input_tensor)
    # Calculate the number of locations (height * width)
    num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)
    # Normalize the Gram matrix by the number of locations
    return result / num_locations


class StyleContentModel(tf.keras.models.Model):
    def __init__(self, style_layers, content_layers):
        super(StyleContentModel, self).__init__()
        self.vgg = vgg_layers(style_layers + content_layers)
        self.style_layers = style_layers
        self.content_layers = content_layers
        self.num_style_layers = len(style_layers)
        self.vgg.trainable = False

    def call(self, inputs):
        """Expects float input in [0,1]"""
        inputs = inputs * 255.0
        #
        # RGB to BGR Conversion due to the format that vgg trained on.
        preprocessed_input = tf.keras.applications.vgg19.preprocess_input(inputs)
        outputs = self.vgg(preprocessed_input)
        style_outputs, content_outputs = (outputs[:self.num_style_layers],
                                          outputs[self.num_style_layers:])

        # calculating the gram matrix for each layer
        style_outputs = [gram_matrix(style_output)
                         for style_output in style_outputs]

        content_dict = {content_name: value
                        for content_name, value
                        in zip(self.content_layers, content_outputs)}

        style_dict = {style_name: value
                      for style_name, value
                      in zip(self.style_layers, style_outputs)}

        return {'content': content_dict, 'style': style_dict}
