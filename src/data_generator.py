import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
Sequence = keras.utils.Sequence # needs to be in this format, otherwise the import doesn't work (for me at least)

# Mapping of genre names to numerical IDs
genre_map = {
    'Classical': 1,
    'Electronic': 2,
    'Folk': 3,
    'Hip_Hop': 4,
    'Jazz': 5,
    'Pop': 6,
    'Reggae': 7,
    'Rnb': 8,
    'Rock': 9,
    'Tollywood': 10
}

# List of genre dirs, just modify these for testing
genre_folders = [
    '~/aims3/Augmented data/Classical',
    '~/aims3/Augmented data/Electronic',
    '~/aims3/Augmented data/Folk',
    '~/aims3/Augmented data/Hip_Hop',
    '~/aims3/Augmented data/Jazz',
    '~/aims3/Augmented data/Pop',
    '~/aims3/Augmented data/Reggae',
    '~/aims3/Augmented data/Rnb',
    '~/aims3/Augmented data/Rock',
    '~/aims3/Augmented data/Tollywood'
]

# maps files to genre int
def map_genre_files(genre_folders, genre_map):
    file_mappings = []
    for directory in genre_folders:
        genre_name = os.path.basename(directory)
        genre_id = genre_map.get(genre_name, -1)
        expanded_directory = os.path.expanduser(directory)
        for root, _, files in os.walk(expanded_directory):
            for file in files:
                if file.endswith('.npy'):
                    file_path = os.path.join(root, file)
                    file_mappings.append((genre_id, file_path))
    return file_mappings

# Generate the mappings
data_index = map_genre_files(genre_folders, genre_map)


# normalizes to dimensions (128, 1024, 1)
def preprocess_spectrogram(spectrogram):
    target_height = 128
    target_width = 1024
    current_height, current_width = spectrogram.shape

    # Resize or pad the height
    if current_height < target_height:
        padding_height = target_height - current_height
        top_padding = padding_height // 2
        bottom_padding = padding_height - top_padding
        padded_spectrogram = np.pad(spectrogram, ((top_padding, bottom_padding), (0, 0)), 'constant')
    elif current_height > target_height:
        padded_spectrogram = spectrogram[:target_height, :]
    else:
        padded_spectrogram = spectrogram

    # Resize or pad the width
    current_height, current_width = padded_spectrogram.shape
    if current_width < target_width:
        padding_width = target_width - current_width
        left_padding = padding_width // 2
        right_padding = padding_width - left_padding
        padded_spectrogram = np.pad(padded_spectrogram, ((0, 0), (left_padding, right_padding)), 'constant')
    elif current_width > target_width:
        padded_spectrogram = np.resize(padded_spectrogram, (current_height, target_width))

    # Add a channel dimension
    padded_spectrogram = np.expand_dims(padded_spectrogram, axis=-1)

    return padded_spectrogram

class DataGenerator(Sequence):
    def __init__(self, data_index, batch_size, input_shape=(128, 1024, 1), num_classes=10, shuffle=True):
        self.data_index = data_index
        self.batch_size = batch_size
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        return len(self.data_index) // self.batch_size

    def __getitem__(self, index):
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        return self.__data_generation(indexes)

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.data_index))
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __data_generation(self, indexes):
        X = np.empty((self.batch_size, *self.input_shape))
        y = np.empty((self.batch_size), dtype=int)

        for i, idx in enumerate(indexes):
            genre_id, file_path = self.data_index[idx]
            spectrogram = self.load_spectrogram(file_path)
            X[i] = preprocess_spectrogram(spectrogram)
            y[i] = genre_id

        return X, tf.keras.utils.to_categorical(y, num_classes=self.num_classes)

    def load_spectrogram(self, file_path):
        return np.load(file_path)

# Example usage:
batch_size = 64
input_shape = (128, 1024, 1)
num_classes = len(genre_map)

data_generator = DataGenerator(
    data_index=data_index,
    batch_size=batch_size,
    input_shape=input_shape,
    num_classes=num_classes
)