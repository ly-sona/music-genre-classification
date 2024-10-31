import boto3
import csv

# Initialize a session with your AWS credentials
session = boto3.Session()
s3 = session.resource('s3')

# Specify your bucket and prefix
bucket_name = 'aims3'  # Replace with your actual bucket name
augmented_data_prefix = 'Augmented data/'  # Main path in the bucket

# Function to l ist all files from S3, including those in subfolders
def list_files_in_s3(prefix):
    bucket = s3.Bucket(bucket_name)
    return [obj.key for obj in bucket.objects.filter(Prefix=prefix) if not obj.key.endswith('/')]

# Collect all file paths
file_paths = list_files_in_s3(augmented_data_prefix)

# Extract genres (labels) from file paths (e.g., folder names under 'Augmented data/')
def extract_genre(file_path):
    parts = file_path.split('/')  # Split path by '/'
    return parts[1] if len(parts) > 1 else 'unknown'  # Genre is the first subfolder

# Collect data: [(file_path, genre), ...]
data = [(file_path, extract_genre(file_path)) for file_path in file_paths]

# Extract unique genres and assign integer indices (starting from 1)
unique_genres = sorted(set(genre for _, genre in data))
genre_to_index = {genre: idx + 1 for idx, genre in enumerate(unique_genres)}  # Start at 1

# Map each file path to its genre index and label
encoded_data = [(file_path, genre, genre_to_index[genre]) for file_path, genre in data]

# Save encoded data to a CSV file
csv_file = 'augmented_data_index.csv'
with open(csv_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['file_path', 'genre_label', 'genre_index'])
    writer.writerows(encoded_data)

print(f'Data index saved to {csv_file}')
print("Genre to Index Mapping:", genre_to_index)
