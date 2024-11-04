import boto3
import os
import numpy as np
from io import BytesIO
from tensorflow import keras
import pandas as pd
import logging
Sequence = keras.utils.Sequence  # Ensure keras.utils.Sequence import works

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mapping of genre names to numerical IDs
genre_map = {
    'Classical': 0,
    'Electronic': 1,
    'Folk': 2,
    'Hip_Hop': 3,
    'Jazz': 4,
    'Pop': 5,
    'Reggae': 6,
    'Rnb': 7,
    'Rock': 8,
    'Tollywood': 9
}

# List of genre directories
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

# Map files to genre IDs
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

# Generate mappings
data_index = map_genre_files(genre_folders, genre_map)

# Normalize to dimensions (128, 1024, 1)
def preprocess_spectrogram(spectrogram):
    target_height = 128
    target_width = 1024
    current_height, current_width = spectrogram.shape

    # Resize or pad height
    if current_height < target_height:
        padding_height = target_height - current_height
        top_padding = padding_height // 2
        bottom_padding = padding_height - top_padding
        padded_spectrogram = np.pad(spectrogram, ((top_padding, bottom_padding), (0, 0)), 'constant')
    elif current_height > target_height:
        padded_spectrogram = spectrogram[:target_height, :]
    else:
        padded_spectrogram = spectrogram

    # Resize or pad width
    current_height, current_width = padded_spectrogram.shape
    if current_width < target_width:
        padding_width = target_width - current_width
        left_padding = padding_width // 2
        right_padding = padding_width - left_padding
        padded_spectrogram = np.pad(padded_spectrogram, ((0, 0), (left_padding, right_padding)), 'constant')
    elif current_width > target_width:
        padded_spectrogram = np.resize(padded_spectrogram, (current_height, target_width))

    # Add channel dimension
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

        # Initialize boto3 S3 client for S3 data loading
        self.s3_client = boto3.client('s3')

    def __len__(self):
        return int(np.ceil(len(self.data_index) / self.batch_size))

    def __getitem__(self, index):
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        return self.__data_generation(indexes)

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.data_index))
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __data_generation(self, indexes):
        current_batch_size = len(indexes)
        X = np.empty((current_batch_size, *self.input_shape))
        y = np.empty((current_batch_size), dtype=int)

        for i, idx in enumerate(indexes):
            file_path, genre_label, genre_index = self.data_index[idx]

            # Check if the file_path is an S3 path
            if file_path.startswith("s3://"):
                bucket_name, key = self.parse_s3_path(file_path)
                spectrogram = self.load_spectrogram_from_s3(bucket_name, key)
            else:
                raise ValueError(f"Expected S3 path, got: {file_path}")

            X[i] = preprocess_spectrogram(spectrogram)
            y[i] = genre_index

        return X, keras.utils.to_categorical(y, num_classes=self.num_classes)

    def parse_s3_path(self, s3_path):
        # Remove the "s3://" prefix and split the bucket name and key
        s3_path = s3_path.replace("s3://", "")
        bucket_name, key = s3_path.split("/", 1)
        return bucket_name, key

    def load_spectrogram_from_s3(self, bucket_name, key):
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=key)
            spectrogram_bytes = response['Body'].read()
            spectrogram = np.load(BytesIO(spectrogram_bytes))
            return spectrogram
        except self.s3_client.exceptions.NoSuchKey:
            logger.error(f"S3 key not found: {key}")
            raise FileNotFoundError(f"S3 key not found: {key}")
        except Exception as e:
            logger.error(f"Error loading spectrogram from S3: {key}, error: {e}")
            raise e


    def load_spectrogram(self, file_path):
        return np.load(file_path)

# Function to create data generators
def create_data_generators(train_csv_file, val_csv_file, img_height=128, img_width=1024, batch_size=32):
    # Load training data index from CSV with three columns
    train_data = pd.read_csv(train_csv_file)
    train_index = list(zip(train_data['file_path'], train_data['genre_label'], train_data['genre_index']))

    # Load validation data index from CSV with three columns
    val_data = pd.read_csv(val_csv_file)
    val_index = list(zip(val_data['file_path'], val_data['genre_label'], val_data['genre_index']))

    # Initialize train and validation generators
    train_generator = DataGenerator(
        data_index=train_index,
        batch_size=batch_size,
        input_shape=(img_height, img_width, 1),
        num_classes=len(genre_map)
    )
    val_generator = DataGenerator(
        data_index=val_index,
        batch_size=batch_size,
        input_shape=(img_height, img_width, 1),
        num_classes=len(genre_map)
    )

    return train_generator, val_generator