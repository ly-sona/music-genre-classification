import pandas as pd
from sklearn.model_selection import train_test_split

# Load the data index from the CSV file
csv_file = 'augmented_data_index.csv'
data = pd.read_csv(csv_file)

# Split the data into features and labels
file_paths = data['file_path']
genre_labels = data['genre_label']

# Perform a stratified split
train_paths, val_paths, train_labels, val_labels = train_test_split(
    file_paths, 
    genre_labels, 
    test_size=0.2,  # 20% for validation
    stratify=genre_labels,  # Stratify by genre labels
    random_state=42  # For reproducibility
)

# Create DataFrames for training and validation sets
train_data = pd.DataFrame({'file_path': train_paths, 'genre_label': train_labels})
val_data = pd.DataFrame({'file_path': val_paths, 'genre_label': val_labels})

# Save the training and validation sets to CSV files
train_csv_file = 'train_data_index.csv'
val_csv_file = 'val_data_index.csv'

train_data.to_csv(train_csv_file, index=False)
val_data.to_csv(val_csv_file, index=False)

print(f'Training data index saved to {train_csv_file}')
print(f'Validation data index saved to {val_csv_file}')
