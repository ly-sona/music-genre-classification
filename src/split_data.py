import pandas as pd
from sklearn.model_selection import train_test_split

# Load the data index from the CSV file
csv_file = 'augmented_data_index.csv'
data = pd.read_csv(csv_file)

# Ensure all necessary columns are included
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

# Save the training and validation sets to CSV files
train_csv_file = 'train_data_index.csv'
val_csv_file = 'val_data_index.csv'

train_data.to_csv(train_csv_file, index=False)
val_data.to_csv(val_csv_file, index=False)

print(f'Training data index saved to {train_csv_file}')
print(f'Validation data index saved to {val_csv_file}')
