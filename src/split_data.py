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
    DRIVE_ROOT = '/content/drive/MyDrive/ML_Project'
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

    # Retain all genres
    min_samples = 1  # Set to 1 to include all genres
    insufficient_genres = genre_counts[genre_counts < min_samples]
    if not insufficient_genres.empty:
        logger.warning(f"The following genres have fewer than {min_samples} samples:")
        logger.warning(insufficient_genres)
    else:
        logger.info("All genres have sufficient samples.")

    # Perform a stratified split
    train_data, val_data = train_test_split(
        data,
        test_size=0.2,
        stratify=data['genre_label'],
        random_state=42
    )
    logger.info("Performed stratified train-validation split.")

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