import boto3
import csv

# Initialize a session with your AWS credentials
session = boto3.Session()
s3 = session.resource('s3')

# Specify your bucket and prefix
bucket_name = 'aims3'  # Replace with your actual bucket name
augmented_data_prefix = 'Augmented data/'  # Main path in the bucket

# Function to list all files from S3, including those in subfolders
def list_files_in_s3(prefix):
    bucket = s3.Bucket(bucket_name)
    return [obj.key for obj in bucket.objects.filter(Prefix=prefix) if not obj.key.endswith('/')]

# Collect all file paths from S3
file_paths = list_files_in_s3(augmented_data_prefix)

# Extract genres (labels) from file paths (e.g., folder names under 'Augmented data/')
def extract_genre(file_path):
    parts = file_path.split('/')  # Split path by '/'
    return parts[1] if len(parts) > 1 else 'unknown'  # Genre is the first subfolder

# Collect all unique genres and assign integer indices
unique_genres = sorted(set(extract_genre(file_path) for file_path in file_paths))
genre_to_index = {genre: idx for idx, genre in enumerate(unique_genres)}

# Print genre_to_index to verify
print("Genre to Index Mapping:", genre_to_index)

# Map each file path to its genre index and label with S3 paths
data = []
for file_path in file_paths:
    genre = extract_genre(file_path)
    genre_index = genre_to_index.get(genre, -1)
    s3_full_path = f"s3://{bucket_name}/{file_path}"
    data.append((s3_full_path, genre, genre_index))

# Save encoded data to a CSV file with S3 paths
csv_file = 'augmented_data_index.csv'
with open(csv_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['file_path', 'genre_label', 'genre_index'])
    writer.writerows(data)

print(f'Data index saved to {csv_file}')
