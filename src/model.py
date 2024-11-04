from tensorflow import keras
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout  # Correct import for layers
from tensorflow.keras.models import Sequential  
from data_generator import *


data_index = map_genre_files(genre_folders, genre_map)
split_idx = int(0.8 * len(data_index)) 
train_index = data_index[:split_idx]
val_index = data_index[split_idx:]
batch_size = 64
input_shape = (128, 1024, 1)
num_classes = len(genre_map)
train_generator = DataGenerator(train_index, batch_size, input_shape=input_shape, num_classes=num_classes)
val_generator = DataGenerator(val_index, batch_size, input_shape=input_shape, num_classes=num_classes, shuffle=False)

def create_cnn_model(input_shape=(128, 1024, 1), num_classes=10):
    """
    Creates and returns a CNN model for music genre classification.

    Parameters:
    - input_shape: tuple, the shape of the input data (height, width, channels).
    - num_classes: int, the number of output classes.

    Returns:
    - model: a compiled Keras Sequential model.
    """
    model = Sequential()  # Defining the model

    # Convolutional and pooling layers
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))  # First Conv2D layer
    model.add(MaxPooling2D((2, 2)))  # First MaxPooling2D layer

    model.add(Conv2D(64, (3, 3), activation='relu'))  # Second Conv2D layer
    model.add(MaxPooling2D((2, 2)))  # Second MaxPooling2D layer

    model.add(Conv2D(128, (3, 3), activation='relu'))  # Third Conv2D layer
    model.add(MaxPooling2D((2, 2)))  # Third MaxPooling2D layer

    # Flattening the output and adding Dense layers
    model.add(Flatten())  # Flatten layer
    model.add(Dense(128, activation='relu'))  # First Dense layer
    model.add(Dropout(0.5))  # Dropout layer to prevent overfitting
    model.add(Dense(num_classes, activation='softmax'))  # Output layer

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']) ##compling model

    try:
        model.fit(train_generator, validation_data=val_generator, epochs=10) ##trying to train
    except Exception as e:
        print(f"Error {e}")

    X_batch, y_batch = train_generator.__getitem__(0) ##making a batch of data from the data generator class

    return model  # Return the constructed model




