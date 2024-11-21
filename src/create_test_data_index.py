# create_test_data_index.py
import boto3
import csv

# Initialize S3 resource
s3 = boto3.resource('s3')

# Specify your bucket and test data prefix
bucket_name = 'aims3'
test_data_prefix = 'Test data/'

# Function to list all files in S3 under a prefix
def list_files_in_s3(prefix):
    bucket = s3.Bucket(bucket_name)
    return [obj.key for obj in bucket.objects.filter(Prefix=prefix) if obj.key.endswith('.npy')]

# Collect all file paths
file_paths = list_files_in_s3(test_data_prefix)

# Extract genres from file paths
def extract_genre(file_path):
    parts = file_path.split('/')
    return parts[1] if len(parts) > 1 else 'unknown'

# Map genres to indices
unique_genres = sorted(set(extract_genre(fp) for fp in file_paths))
genre_to_index = {genre: idx for idx, genre in enumerate(unique_genres)}

# Prepare data
data = []
for file_path in file_paths:
    genre = extract_genre(file_path)
    genre_index = genre_to_index.get(genre, -1)
    s3_full_path = f"s3://{bucket_name}/{file_path}"
    data.append((s3_full_path, genre, genre_index))

# Save to CSV
csv_file = 'test_data_index.csv'
with open(csv_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['file_path', 'genre_label', 'genre_index'])
    writer.writerows(data)

print(f'Test data index saved to {csv_file}')
