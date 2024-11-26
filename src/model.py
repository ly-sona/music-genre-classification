# model.py

from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, BatchNormalization, Activation
from tensorflow.keras.optimizers import Adam

def create_transfer_model(input_shape=(128, 1024, 3), num_classes=10):
    """
    Creates a CNN model using ResNet50 as the base for transfer learning.

    Parameters:
        input_shape (tuple): Shape of the input spectrogram (height, width, channels).
        num_classes (int): Number of output classes.

    Returns:
        tensorflow.keras.Model: Compiled CNN model.
    """
    # Load ResNet50 without the top classification layers
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
    
    # Freeze the base model layers to prevent them from training
    for layer in base_model.layers:
        layer.trainable = False
    
    # Add custom top layers
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    # Construct the final model
    model = Model(inputs=base_model.input, outputs=predictions)
    
    return model