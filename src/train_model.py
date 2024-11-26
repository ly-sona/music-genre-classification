# train_model.py

import os
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from data_generator import create_data_generators
from model import create_cnn_model
import matplotlib.pyplot as plt
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import logging
# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def plot_training_history(history, save_dir):
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
    # Mount Google Drive
    DRIVE_ROOT = '/content/drive/MyDrive/ML_Project'  # Change as needed
    os.makedirs(DRIVE_ROOT, exist_ok=True)

    # Securely configure AWS credentials from environment variables
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = 'us-east-2'  # Update if different

    # Check if credentials are available
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
    BATCH_SIZE = 16
    IMG_HEIGHT = 128
    IMG_WIDTH = 1024
    NUM_CLASSES = 10  # Update based on your dataset
    EPOCHS = 30  # Increased for better training
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
        num_classes=NUM_CLASSES  # Pass NUM_CLASSES to the data generators
    )

    # Create and compile the model
    model = create_cnn_model(input_shape=(IMG_HEIGHT, IMG_WIDTH, 1), num_classes=NUM_CLASSES)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    logger.info("Model created and compiled.")

    # Set up callbacks
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    checkpoint_path = os.path.join(MODEL_SAVE_DIR, 'best_model.keras')
    model_checkpoint = ModelCheckpoint(
        filepath=checkpoint_path,
        monitor='val_loss',
        save_best_only=True
    )

    # Optionally, add TensorBoard callback
    # tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=os.path.join(DRIVE_ROOT, 'logs'))

    # Train the model
    logger.info("Starting model training...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        callbacks=[early_stop, model_checkpoint],
        verbose=1  # Show progress
    )
    logger.info("Model training completed.")

    # Plot training history
    plot_training_history(history, MODEL_SAVE_DIR)

    # Save the final model
    final_model_path = os.path.join(MODEL_SAVE_DIR, 'music_genre_cnn_final.keras')
    model.save(final_model_path)
    logger.info(f"Final model saved to {final_model_path}")

    # Define S3 bucket and prefix for model uploads
    MODEL_S3_BUCKET = 'aims3'  # Replace with your actual bucket name
    MODEL_S3_PREFIX = 'trained_models/'  # S3 folder path

    # Upload 'best_model.keras' to S3
    best_model_s3_path = os.path.join(MODEL_S3_PREFIX, 'best_model.keras')
    upload_to_s3(s3_client, checkpoint_path, MODEL_S3_BUCKET, best_model_s3_path)

    # Upload 'music_genre_cnn_final.keras' to S3
    final_model_s3_path = os.path.join(MODEL_S3_PREFIX, 'music_genre_cnn_final.keras')
    upload_to_s3(s3_client, final_model_path, MODEL_S3_BUCKET, final_model_s3_path)

if __name__ == "__main__":
    main()