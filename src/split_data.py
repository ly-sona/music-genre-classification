# split_data.py

import pandas as pd
from sklearn.model_selection import train_test_split
import logging
import os

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Mount Google Drive
    DRIVE_ROOT = '/content/drive/MyDrive/ML_Project'  # Change as needed
    os.makedirs(DRIVE_ROOT, exist_ok=True)

    # Load the data index from the CSV file
    csv_file = os.path.join(DRIVE_ROOT, 'augmented_data_index.csv')
    data = pd.read_csv(csv_file)
    logger.info(f"Loaded data index from {csv_file}")

    # Ensure all necessary columns are included
    required_columns = ['file_path', 'genre_label', 'genre_index']
    if not all(column in data.columns for column in required_columns):
        logger.error(f"CSV file must contain columns: {required_columns}")
        return

    file_paths = data['file_path']
    genre_labels = data['genre_label']
    genre_indices = data['genre_index']  # Include genre_index

    # Combine features into a DataFrame
    features = pd.DataFrame({
        'file_path': file_paths,
        'genre_label': genre_labels,
        'genre_index': genre_indices
    })

    # Perform a stratified split
    train_data, val_data = train_test_split(
        features,
        test_size=0.2,  # 20% for validation
        stratify=features['genre_label'],  # Stratify by genre labels
        random_state=42  # For reproducibility
    )
    logger.info("Performed stratified train-validation split.")

    # Save the training and validation sets to CSV files
    train_csv_file = os.path.join(DRIVE_ROOT, 'train_data_index.csv')
    val_csv_file = os.path.join(DRIVE_ROOT, 'val_data_index.csv')

    train_data.to_csv(train_csv_file, index=False)
    val_data.to_csv(val_csv_file, index=False)

    logger.info(f'Training data index saved to {train_csv_file}')
    logger.info(f'Validation data index saved to {val_csv_file}')

if __name__ == "__main__":
    main()