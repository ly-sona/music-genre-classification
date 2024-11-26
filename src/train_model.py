# train_model.py

import os
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
from data_generator import create_data_generators
from model import create_transfer_model, create_cnn_model
import matplotlib.pyplot as plt
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import logging
import pandas as pd
import numpy as np
from sklearn.utils import class_weight

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def plot_training_history(history, save_dir):
    """
    Plots and saves the training and validation accuracy and loss.

    Parameters:
        history (tensorflow.keras.callbacks.History): Training history object.
        save_dir (str): Directory to save the plots.
    """
    # Plot accuracy
    plt.figure(figsize=(8, 6))
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Accuracy over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    accuracy_plot_path = os.path.join(save_dir, 'accuracy_over_epochs.png')
    plt.savefig(accuracy_plot_path)
    plt.close()
    logger.info(f"Accuracy plot saved to {accuracy_plot_path}")

    # Plot loss
    plt.figure(figsize=(8, 6))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Loss over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    loss_plot_path = os.path.join(save_dir, 'loss_over_epochs.png')
    plt.savefig(loss_plot_path)
    plt.close()
    logger.info(f"Loss plot saved to {loss_plot_path}")

    # Optionally, display plots in Colab
    from IPython.display import Image, display
    display(Image(filename=accuracy_plot_path))
    display(Image(filename=loss_plot_path))

def upload_to_s3(s3_client, local_file_path, bucket_name, s3_file_path):
    """
    Uploads a file to AWS S3.

    Parameters:
        s3_client (boto3.client): The S3 client.
        local_file_path (str): Path to the local file.
        bucket_name (str): Name of the S3 bucket.
        s3_file_path (str): S3 object name (including prefix if any).
    """
    try:
        s3_client.upload_file(local_file_path, bucket_name, s3_file_path)
        logger.info(f"Successfully uploaded {local_file_path} to s3://{bucket_name}/{s3_file_path}")
    except FileNotFoundError:
        logger.error(f"The file {local_file_path} was not found.")
    except NoCredentialsError:
        logger.error("Credentials not available for AWS S3.")
    except PartialCredentialsError:
        logger.error("Incomplete AWS credentials provided.")
    except Exception as e:
        logger.error(f"An error occurred while uploading {local_file_path} to S3: {e}")

def main():
    # Define the root directory
    DRIVE_ROOT = '/content/drive/MyDrive/ML_Project'
    os.makedirs(DRIVE_ROOT, exist_ok=True)

    # AWS Credentials
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = 'us-east-2'  # Update if different

    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        logger.error("AWS credentials are not set. Please set them as environment variables.")
        return

    # Initialize boto3 session
    try:
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        s3_client = session.client('s3')
        logger.info("Successfully initialized boto3 session.")
    except Exception as e:
        logger.error(f"Failed to create boto3 session: {e}")
        return

    # Define paths and parameters
    BATCH_SIZE = 16  # Adjust if necessary
    IMG_HEIGHT = 128
    IMG_WIDTH = 1024
    NUM_CLASSES = 10  # Update based on your dataset
    EPOCHS = 30  # Reduced number of epochs
    MODEL_SAVE_DIR = os.path.join(DRIVE_ROOT, 'models')
    os.makedirs(MODEL_SAVE_DIR, exist_ok=True)

    TRAIN_CSV = os.path.join(DRIVE_ROOT, 'train_data_index.csv')
    VAL_CSV = os.path.join(DRIVE_ROOT, 'val_data_index.csv')

    # Create data generators
    train_generator, val_generator = create_data_generators(
        train_csv_file=TRAIN_CSV,
        val_csv_file=VAL_CSV,
        s3_client=s3_client,
        img_height=IMG_HEIGHT,
        img_width=IMG_WIDTH,
        batch_size=BATCH_SIZE,
        num_classes=NUM_CLASSES,
        cache_dir=os.path.join(DRIVE_ROOT, 'spectrogram_cache'),
        augment=True  # Enable augmentation
    )

    # Calculate class weights
    try:
        train_df = pd.read_csv(TRAIN_CSV)
        class_weights_vals = class_weight.compute_class_weight(
            class_weight='balanced',
            classes=np.unique(train_df['genre_index']),
            y=train_df['genre_index']
        )
        class_weights_dict = {i: weight for i, weight in enumerate(class_weights_vals)}
        logger.info(f"Computed class weights: {class_weights_dict}")
    except Exception as e:
        logger.error(f"Failed to compute class weights: {e}")
        class_weights_dict = None

    # Create and compile the model
    model = create_transfer_model(input_shape=(IMG_HEIGHT, IMG_WIDTH, 3), num_classes=NUM_CLASSES)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    logger.info("Model created and compiled.")

    # Set up callbacks
    early_stop = EarlyStopping(
        monitor='val_accuracy',
        patience=5,  # Reduced patience for quicker stopping
        restore_best_weights=True,
        verbose=1
    )
    checkpoint_path = os.path.join(MODEL_SAVE_DIR, 'best_model.keras')
    model_checkpoint = ModelCheckpoint(
        filepath=checkpoint_path,
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
    lr_reduction = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        verbose=1,
        min_lr=1e-6
    )
    tensorboard_callback = TensorBoard(
        log_dir=os.path.join(DRIVE_ROOT, 'logs'),
        histogram_freq=1
    )

    callbacks = [early_stop, model_checkpoint, lr_reduction, tensorboard_callback]

    # Train the model
    logger.info("Starting model training...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        callbacks=callbacks,
        class_weight=class_weights_dict,
        verbose=1
    )
    logger.info("Model training completed.")

    # Plot training history
    plot_training_history(history, MODEL_SAVE_DIR)

    # Save the final model
    final_model_path = os.path.join(MODEL_SAVE_DIR, 'music_genre_cnn_final.keras')
    model.save(final_model_path)
    logger.info(f"Final model saved to {final_model_path}")

    # Upload models to S3
    MODEL_S3_BUCKET = 'aims3'  # Replace with your actual bucket name
    MODEL_S3_PREFIX = 'trained_models/'

    # Upload 'best_model.keras' to S3
    best_model_s3_path = os.path.join(MODEL_S3_PREFIX, 'best_model.keras')
    upload_to_s3(s3_client, checkpoint_path, MODEL_S3_BUCKET, best_model_s3_path)

    # Upload 'music_genre_cnn_final.keras' to S3
    final_model_s3_path = os.path.join(MODEL_S3_PREFIX, 'music_genre_cnn_final.keras')
    upload_to_s3(s3_client, final_model_path, MODEL_S3_BUCKET, final_model_s3_path)

if __name__ == "__main__":
    main()