# model.py

from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D

def create_transfer_model(input_shape=(128, 1024, 3), num_classes=10):
    """
    Creates a CNN model using ResNet50 as the base for transfer learning.

    Parameters:
        input_shape (tuple): Shape of the input spectrogram (height, width, channels).
        num_classes (int): Number of output classes.

    Returns:
        tensorflow.keras.models.Model: Compiled Keras model ready for training.
    """
    # Load ResNet50 without the top classification layers
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)

    # Freeze the base model layers to prevent them from being trained
    for layer in base_model.layers:
        layer.trainable = False

    # Add a global average pooling layer to reduce the spatial dimensions
    x = base_model.output
    x = GlobalAveragePooling2D()(x)

    # Add the final Dense layer with softmax activation for classification
    predictions = Dense(num_classes, activation='softmax', dtype='float32')(x)  # Ensure output dtype is float32

    # Construct the final model
    model = Model(inputs=base_model.input, outputs=predictions)

    return model