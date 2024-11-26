# split_data.py

import pandas as pd
from sklearn.model_selection import train_test_split
import logging
import os

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Define the root directory
    DRIVE_ROOT = '/content/drive/MyDrive/ML_Project'  # Change as needed
    os.makedirs(DRIVE_ROOT, exist_ok=True)

    # Load the data index from the CSV file
    csv_file = os.path.join(DRIVE_ROOT, 'augmented_data_index.csv')
    try:
        data = pd.read_csv(csv_file)
        logger.info(f"Loaded data index from {csv_file}")
    except Exception as e:
        logger.error(f"Failed to read CSV file: {e}")
        return

    # Ensure all necessary columns are included
    required_columns = ['file_path', 'genre_label', 'genre_index']
    if not all(column in data.columns for column in required_columns):
        logger.error(f"CSV file must contain columns: {required_columns}")
        return

    # Verify genre distribution
    genre_counts = data['genre_label'].value_counts()
    logger.info("Genre distribution in the dataset:")
    logger.info(genre_counts)

    # Check if each genre has at least 250 samples
    min_samples = 250
    insufficient_genres = genre_counts[genre_counts < min_samples]
    if not insufficient_genres.empty:
        logger.warning("The following genres have fewer than 250 samples:")
        logger.warning(insufficient_genres)
        # Optionally, remove these genres or handle accordingly
        data = data[~data['genre_label'].isin(insufficient_genres.index)]
        logger.info("Removed genres with insufficient samples.")
        logger.info(f"New genre distribution:")
        logger.info(data['genre_label'].value_counts())

    # Perform a stratified split
    train_data, val_data = train_test_split(
        data,
        test_size=0.2,  # 20% for validation
        stratify=data['genre_label'],  # Stratify by genre labels
        random_state=42  # For reproducibility
    )
    logger.info("Performed stratified train-validation split.")

    # Verify the split
    logger.info("Training set genre distribution:")
    logger.info(train_data['genre_label'].value_counts())
    logger.info("Validation set genre distribution:")
    logger.info(val_data['genre_label'].value_counts())

    # Save the training and validation sets to CSV files
    train_csv_file = os.path.join(DRIVE_ROOT, 'train_data_index.csv')
    val_csv_file = os.path.join(DRIVE_ROOT, 'val_data_index.csv')

    try:
        train_data.to_csv(train_csv_file, index=False)
        val_data.to_csv(val_csv_file, index=False)
        logger.info(f'Training data index saved to {train_csv_file}')
        logger.info(f'Validation data index saved to {val_csv_file}')
    except Exception as e:
        logger.error(f"Failed to write split CSV files: {e}")

if __name__ == "__main__":
    main()