# create_data_index.py

import boto3
import csv
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_files_in_s3(s3, bucket, prefix):
    """
    List all .npy files in the specified S3 bucket and prefix.

    Parameters:
        s3 (boto3.resource): Boto3 S3 resource.
        bucket (str): Name of the S3 bucket.
        prefix (str): Prefix path in the S3 bucket.

    Returns:
        list: List of file keys ending with .npy
    """
    s3_bucket = bucket
    s3_prefix = prefix
    files = []
    try:
        bucket_resource = s3.Bucket(s3_bucket)
        for obj in bucket_resource.objects.filter(Prefix=s3_prefix):
            if obj.key.endswith('.npy'):
                files.append(obj.key)
        logger.info(f"Found {len(files)} .npy files in s3://{s3_bucket}/{s3_prefix}")
    except Exception as e:
        logger.error(f"Error listing files in S3: {e}")
    return files

def extract_genre(file_path):
    """
    Extract genre from the S3 file path.

    Assumes the genre is the third element when splitting by '/'.

    Parameters:
        file_path (str): Full S3 file path.

    Returns:
        str: Extracted genre or 'unknown' if not found.
    """
    parts = file_path.split('/')
    if len(parts) > 2:
        return parts[2]
    else:
        return 'unknown'

def main():
    # Ensure Google Drive is mounted in the Colab notebook before running this script

    # Define the root directory (Assuming scripts are being run from a specific directory)
    DRIVE_ROOT = '/content/drive/MyDrive/ML_Project'  # Change as needed
    os.makedirs(DRIVE_ROOT, exist_ok=True)

    # Fetch AWS credentials from environment variables
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = 'us-east-2'  # Replace with your actual AWS region

    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        logger.error("AWS credentials are not set. Please set them as environment variables.")
        exit(1)

    # Initialize S3 resource
    try:
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        s3 = session.resource('s3')
        logger.info("Successfully initialized boto3 session.")
    except Exception as e:
        logger.error(f"Failed to create boto3 session: {e}")
        exit(1)

    # Specify your bucket and prefix
    bucket_name = 'aims3'  # Replace with your actual bucket name
    augmented_data_prefix = 'Augmented data/'

    # Function to list all files in S3 under a prefix
    file_paths = list_files_in_s3(s3, bucket_name, augmented_data_prefix)

    if not file_paths:
        logger.error("No .npy files found. Exiting.")
        exit(1)

    # Map genres to indices
    unique_genres = sorted(set(extract_genre(fp) for fp in file_paths))
    genre_to_index = {genre: idx for idx, genre in enumerate(unique_genres)}
    logger.info(f"Genre to Index Mapping: {genre_to_index}")

    # Prepare data
    data = []
    for file_path in file_paths:
        genre = extract_genre(file_path)
        genre_index = genre_to_index.get(genre, -1)
        s3_full_path = f"s3://{bucket_name}/{file_path}"
        data.append((s3_full_path, genre, genre_index))

    # Save to CSV
    csv_file = os.path.join(DRIVE_ROOT, 'augmented_data_index.csv')
    try:
        with open(csv_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['file_path', 'genre_label', 'genre_index'])
            writer.writerows(data)
        logger.info(f'Data index saved to {csv_file}')
    except Exception as e:
        logger.error(f"Failed to write CSV file: {e}")

if __name__ == "__main__":
    main()