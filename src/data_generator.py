# data_generator.py

import os
import numpy as np
from tensorflow import keras
import pandas as pd
import logging
from io import BytesIO
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import boto3

Sequence = keras.utils.Sequence

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def preprocess_spectrogram(spectrogram, input_channels=3):
    """
    Preprocesses the spectrogram by resizing/padding, normalizing, and replicating channels.
    """
    target_height = 128
    target_width = 1024
    current_height, current_width = spectrogram.shape

    # Resize or pad height
    if current_height < target_height:
        padding_height = target_height - current_height
        top_padding = padding_height // 2
        bottom_padding = padding_height - top_padding
        spectrogram = np.pad(spectrogram, ((top_padding, bottom_padding), (0, 0)), 'constant')
    elif current_height > target_height:
        spectrogram = spectrogram[:target_height, :]

    # Resize or pad width
    current_height, current_width = spectrogram.shape
    if current_width < target_width:
        padding_width = target_width - current_width
        left_padding = padding_width // 2
        right_padding = padding_width - left_padding
        spectrogram = np.pad(spectrogram, ((0, 0), (left_padding, right_padding)), 'constant')
    elif current_width > target_width:
        spectrogram = spectrogram[:, :target_width]

    # Normalize spectrogram
    min_val = np.min(spectrogram)
    max_val = np.max(spectrogram)
    normalized_spectrogram = (spectrogram - min_val) / (max_val - min_val + 1e-6)

    # Replicate channels for ResNet50
    normalized_spectrogram = np.stack((normalized_spectrogram,)*input_channels, axis=-1)

    return normalized_spectrogram

class DataGenerator(Sequence):
    def __init__(self, data_index, s3_client, batch_size, input_shape=(128, 1024, 3), num_classes=10, shuffle=True, cache_dir='/content/drive/MyDrive/ML_Project/spectrogram_cache', augment=False):
        self.data_index = data_index
        self.s3_client = s3_client
        self.batch_size = batch_size
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.shuffle = shuffle
        self.cache_dir = cache_dir
        self.augment = augment
        os.makedirs(self.cache_dir, exist_ok=True)
        self.on_epoch_end()
        logger.info(f"DataGenerator initialized with cache directory: {self.cache_dir}")

        if self.augment:
            self.augmenter = ImageDataGenerator(
                rotation_range=10,
                width_shift_range=0.1,
                height_shift_range=0.1,
                zoom_range=0.1,
                horizontal_flip=False,
                vertical_flip=False
            )
            logger.info("Data augmentation enabled.")
        else:
            self.augmenter = None

    def __len__(self):
        return int(np.ceil(len(self.data_index) / self.batch_size))

    def __getitem__(self, index):
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        X, y = self.__data_generation(indexes)
        return X, y

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.data_index))
        if self.shuffle:
            np.random.shuffle(self.indexes)
        logger.info("Epoch ended. Data shuffled.")

    def __data_generation(self, indexes):
        X_list = []
        y_list = []

        for idx in indexes:
            file_path, genre_label, genre_index = self.data_index[idx]
            bucket_name, key = self.parse_s3_path(file_path)

            try:
                spectrogram = self.get_spectrogram(bucket_name, key)
                processed_spectrogram = preprocess_spectrogram(spectrogram, input_channels=self.input_shape[-1])

                if self.augmenter:
                    processed_spectrogram = self.augmenter.random_transform(processed_spectrogram)

                X_list.append(processed_spectrogram)
                y_list.append(genre_index)
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
                continue

        if len(X_list) == 0:
            logger.error("No data available for this batch.")
            raise ValueError("No data available for this batch.")

        X = np.array(X_list)
        y = keras.utils.to_categorical(y_list, num_classes=self.num_classes)

        return X, y

    def parse_s3_path(self, s3_path):
        s3_path = s3_path.replace("s3://", "")
        parts = s3_path.split("/", 1)
        if len(parts) != 2:
            logger.error(f"Invalid S3 path: {s3_path}")
            raise ValueError(f"Invalid S3 path: {s3_path}")
        bucket_name, key = parts
        return bucket_name, key

    def get_spectrogram(self, bucket_name, key):
        local_file_name = key.replace('/', '_')
        local_file_path = os.path.join(self.cache_dir, local_file_name)

        if os.path.exists(local_file_path):
            spectrogram = np.load(local_file_path)
            logger.debug(f"Loaded spectrogram from cache: {local_file_path}")
        else:
            try:
                obj = self.s3_client.get_object(Bucket=bucket_name, Key=key)
                spectrogram_bytes = obj['Body'].read()
                spectrogram = np.load(BytesIO(spectrogram_bytes))
                logger.debug(f"Downloaded spectrogram from S3: s3://{bucket_name}/{key}")

                np.save(local_file_path, spectrogram)
                logger.debug(f"Saved spectrogram to cache: {local_file_path}")
            except Exception as e:
                logger.error(f"Failed to retrieve spectrogram from S3: s3://{bucket_name}/{key}. Error: {e}")
                raise e

        return spectrogram

def create_data_generators(train_csv_file, val_csv_file, s3_client, img_height=128, img_width=1024, batch_size=32, num_classes=10, cache_dir='/content/drive/MyDrive/ML_Project/spectrogram_cache', augment=False):
    # Read the training CSV
    try:
        train_data = pd.read_csv(train_csv_file)
        logger.info(f"Loaded training data index from {train_csv_file}")
    except Exception as e:
        logger.error(f"Failed to read training CSV: {e}")
        raise e

    train_index = list(zip(train_data['file_path'], train_data['genre_label'], train_data['genre_index']))

    # Read the validation CSV
    try:
        val_data = pd.read_csv(val_csv_file)
        logger.info(f"Loaded validation data index from {val_csv_file}")
    except Exception as e:
        logger.error(f"Failed to read validation CSV: {e}")
        raise e

    val_index = list(zip(val_data['file_path'], val_data['genre_label'], val_data['genre_index']))

    # Input channels for ResNet50
    input_channels = 3

    # Create DataGenerator instances
    train_generator = DataGenerator(
        data_index=train_index,
        s3_client=s3_client,
        batch_size=batch_size,
        input_shape=(img_height, img_width, input_channels),
        num_classes=num_classes,
        shuffle=True,
        cache_dir=cache_dir,
        augment=augment
    )
    val_generator = DataGenerator(
        data_index=val_index,
        s3_client=s3_client,
        batch_size=batch_size,
        input_shape=(img_height, img_width, input_channels),
        num_classes=num_classes,
        shuffle=False,
        cache_dir=cache_dir,
        augment=False
    )

    logger.info("Data generators created successfully.")
    return train_generator, val_generator