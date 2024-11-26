import os
import numpy as np
from tensorflow import keras
import pandas as pd
import logging
from io import BytesIO
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import boto3

Sequence = keras.utils.Sequence  # Ensure keras.utils.Sequence import works

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def preprocess_spectrogram(spectrogram, input_channels=3):
    """
    Preprocesses the spectrogram by resizing/padding, normalizing, and replicating channels.
    
    Parameters:
        spectrogram (np.ndarray): Raw spectrogram data.
        input_channels (int): Number of channels required by the model.
    
    Returns:
        np.ndarray: Preprocessed spectrogram with shape (128, 1024, channels).
    """
    # If spectrogram has more than 2 dimensions, squeeze to 2D
    if spectrogram.ndim > 2:
        spectrogram = np.squeeze(spectrogram)
        logger.debug(f"Squeezed spectrogram shape: {spectrogram.shape}")

    if spectrogram.ndim != 2:
        raise ValueError(f"Spectrogram has unexpected number of dimensions: {spectrogram.ndim}")

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

    # Normalize spectrogram using min-max normalization
    min_val = np.min(spectrogram)
    max_val = np.max(spectrogram)
    normalized_spectrogram = (spectrogram - min_val) / (max_val - min_val + 1e-6)  # Avoid division by zero

    # Replicate channels for ResNet50
    if input_channels > 1:
        normalized_spectrogram = np.repeat(normalized_spectrogram[..., np.newaxis], input_channels, axis=-1)
        logger.debug(f"Replicated spectrogram to {input_channels} channels: {normalized_spectrogram.shape}")
    else:
        # Add channel dimension
        normalized_spectrogram = np.expand_dims(normalized_spectrogram, axis=-1)
        logger.debug(f"Added single channel to spectrogram: {normalized_spectrogram.shape}")

    return normalized_spectrogram

class DataGenerator(Sequence):
    def __init__(self, data_index, s3_client, batch_size, input_shape=(128, 1024, 3), num_classes=10, shuffle=True, cache_dir='/content/drive/MyDrive/ML_Project/spectrogram_cache', augment=False, **kwargs):
        """
        Initializes the DataGenerator.

        Parameters:
            data_index (list): List of tuples containing (file_path, genre_label, genre_index).
            s3_client (boto3.client): AWS S3 client.
            batch_size (int): Size of each data batch.
            input_shape (tuple): Shape of input spectrogram.
            num_classes (int): Number of output classes.
            shuffle (bool): Whether to shuffle data after each epoch.
            cache_dir (str): Directory to cache downloaded spectrograms.
            augment (bool): Whether to apply data augmentation.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)  # Properly initialize the superclass with kwargs
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
                horizontal_flip=False,  # Not typically applicable for spectrograms
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
                logger.debug(f"Loaded spectrogram shape before preprocessing for {file_path}: {spectrogram.shape}")

                processed_spectrogram = preprocess_spectrogram(spectrogram, input_channels=self.input_shape[-1])
                logger.debug(f"Processed spectrogram shape for {file_path}: {processed_spectrogram.shape}")

                if self.augmenter:
                    # Apply random transformations
                    processed_spectrogram = self.augmenter.random_transform(processed_spectrogram)
                    logger.debug(f"Augmented spectrogram shape for {file_path}: {processed_spectrogram.shape}")

                X_list.append(processed_spectrogram)
                y_list.append(genre_index)
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
                continue  # Skip this sample

        if len(X_list) == 0:
            # If no samples were loaded successfully, raise an error
            logger.error("No data available for this batch.")
            raise ValueError("No data available for this batch.")

        # Convert lists to arrays
        X = np.array(X_list)
        y = keras.utils.to_categorical(y_list, num_classes=self.num_classes)

        return X, y

    def parse_s3_path(self, s3_path):
        """
        Parses the S3 path to extract bucket name and key.

        Parameters:
            s3_path (str): Full S3 path (e.g., s3://bucket_name/key).

        Returns:
            tuple: (bucket_name, key)
        """
        s3_path = s3_path.replace("s3://", "")
        parts = s3_path.split("/", 1)
        if len(parts) != 2:
            logger.error(f"Invalid S3 path: {s3_path}")
            raise ValueError(f"Invalid S3 path: {s3_path}")
        bucket_name, key = parts
        return bucket_name, key

    def get_spectrogram(self, bucket_name, key):
        """
        Retrieves the spectrogram from S3 or local cache.

        Parameters:
            bucket_name (str): Name of the S3 bucket.
            key (str): Key of the S3 object.

        Returns:
            np.ndarray: Spectrogram data.
        """
        # Create a local cache file path
        local_file_name = key.replace('/', '_')
        local_file_path = os.path.join(self.cache_dir, local_file_name)

        if os.path.exists(local_file_path):
            # Load spectrogram from local cache
            spectrogram = np.load(local_file_path)
            logger.debug(f"Loaded spectrogram from cache: {local_file_path}")
        else:
            # Download spectrogram from S3
            try:
                obj = self.s3_client.get_object(Bucket=bucket_name, Key=key)
                spectrogram_bytes = obj['Body'].read()
                spectrogram = np.load(BytesIO(spectrogram_bytes))
                logger.debug(f"Downloaded spectrogram from S3: s3://{bucket_name}/{key}")

                # Save spectrogram to local cache
                np.save(local_file_path, spectrogram)
                logger.debug(f"Saved spectrogram to cache: {local_file_path}")
            except Exception as e:
                logger.error(f"Failed to retrieve spectrogram from S3: s3://{bucket_name}/{key}. Error: {e}")
                raise e

        return spectrogram

def create_data_generators(train_csv_file, val_csv_file, s3_client, img_height=128, img_width=1024, batch_size=32, num_classes=10, cache_dir='/content/drive/MyDrive/ML_Project/spectrogram_cache', augment=False):
    """
    Creates training and validation data generators.

    Parameters:
        train_csv_file (str): Path to training data index CSV.
        val_csv_file (str): Path to validation data index CSV.
        s3_client (boto3.client): AWS S3 client.
        img_height (int): Height of input spectrogram.
        img_width (int): Width of input spectrogram.
        batch_size (int): Batch size.
        num_classes (int): Number of output classes.
        cache_dir (str): Directory to cache downloaded spectrograms.
        augment (bool): Whether to apply data augmentation.

    Returns:
        tuple: (train_generator, val_generator)
    """
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

    # Determine input channels based on the model (3 for transfer learning with ResNet50, 1 for custom CNN)
    input_channels = 3  # Set to 1 if using custom CNN without transfer learning

    # Create DataGenerator instances
    train_generator = DataGenerator(
        data_index=train_index,
        s3_client=s3_client,
        batch_size=batch_size,
        input_shape=(img_height, img_width, input_channels),
        num_classes=num_classes,
        shuffle=True,
        cache_dir=cache_dir,
        augment=augment  # Enable augmentation for training data
    )
    val_generator = DataGenerator(
        data_index=val_index,
        s3_client=s3_client,
        batch_size=batch_size,
        input_shape=(img_height, img_width, input_channels),
        num_classes=num_classes,
        shuffle=False,
        cache_dir=cache_dir,
        augment=False  # No augmentation for validation data
    )

    logger.info("Data generators created successfully.")
    return train_generator, val_generator