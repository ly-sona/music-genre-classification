# evaluate_model.py

import os
import boto3
import numpy as np
import pandas as pd
from io import BytesIO
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.utils import Sequence
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# Define genre map and list of genres
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

# Define S3 bucket and test data prefix
BUCKET_NAME = 'aims3'
TEST_DATA_PREFIX = 'Test data/'  # Adjust the S3 prefix for test data

# Preprocessing functions
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
        padded_spectrogram = padded_spectrogram[:, :target_width]

    # Add channel dimension
    padded_spectrogram = np.expand_dims(padded_spectrogram, axis=-1)
    return padded_spectrogram

# Data Generator for evaluation
class TestDataGenerator(Sequence):
    def __init__(self, data_index, batch_size, input_shape=(128, 1024, 1), num_classes=10):
        self.data_index = data_index
        self.batch_size = batch_size
        self.input_shape = input_shape
        self.num_classes = num_classes

        # Initialize boto3 S3 client
        self.s3_client = boto3.client('s3')

    def __len__(self):
        return int(np.ceil(len(self.data_index) / self.batch_size))

    def __getitem__(self, index):
        batch_data = self.data_index[index * self.batch_size:(index + 1) * self.batch_size]
        X, y = self.__data_generation(batch_data)
        return X, y

    def __data_generation(self, batch_data):
        current_batch_size = len(batch_data)
        X = np.empty((current_batch_size, *self.input_shape))
        y = np.empty((current_batch_size), dtype=int)

        for i, data_point in enumerate(batch_data):
            file_path, genre_label, genre_index = data_point

            # Load spectrogram from S3
            spectrogram = self.load_spectrogram_from_s3(file_path)
            X[i] = preprocess_spectrogram(spectrogram)
            y[i] = genre_index

        return X, keras.utils.to_categorical(y, num_classes=self.num_classes)

    def load_spectrogram_from_s3(self, s3_path):
        bucket_name, key = self.parse_s3_path(s3_path)
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=key)
            spectrogram_bytes = response['Body'].read()
            spectrogram = np.load(BytesIO(spectrogram_bytes))
            return spectrogram
        except Exception as e:
            print(f"Error loading {s3_path}: {e}")
            raise

    def parse_s3_path(self, s3_path):
        s3_path = s3_path.replace("s3://", "")
        bucket_name, key = s3_path.split("/", 1)
        return bucket_name, key

def load_test_data_index(test_csv_file):
    test_data = pd.read_csv(test_csv_file)
    test_index = list(zip(test_data['file_path'], test_data['genre_label'], test_data['genre_index']))
    return test_index

def evaluate_model():
    # Load the test data index
    TEST_CSV = 'test_data_index.csv'  # This CSV should contain file paths and labels for the test data
    test_index = load_test_data_index(TEST_CSV)

    # Create test data generator
    batch_size = 32
    input_shape = (128, 1024, 1)
    num_classes = len(genre_map)
    test_generator = TestDataGenerator(test_index, batch_size, input_shape=input_shape, num_classes=num_classes)

    # Load the trained model
    MODEL_PATH = 'models/best_model.keras'  # Adjust the path to your trained model
    model = keras.models.load_model(MODEL_PATH)

    # Evaluate the model
    print("Evaluating the model on test data...")
    test_steps = len(test_generator)
    predictions = model.predict(test_generator, steps=test_steps, verbose=1)
    y_pred = np.argmax(predictions, axis=1)

    # Get true labels
    y_true = []
    for _, labels in test_generator:
        y_true.extend(np.argmax(labels, axis=1))
    y_true = np.array(y_true[:len(y_pred)])  # Ensure same length

    # Compute evaluation metrics
    accuracy = accuracy_score(y_true, y_pred)
    print(f"Test Accuracy: {accuracy:.4f}")

    print("Classification Report:")
    print(classification_report(y_true, y_pred, target_names=genre_map.keys()))

    # Plot confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=genre_map.keys(), yticklabels=genre_map.keys(), cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()

if __name__ == "__main__":
    evaluate_model()