import boto3
import os
import librosa
import numpy as np
import io
import posixpath
import logging
from tqdm import tqdm
import matplotlib.pyplot as plt
import shutil
import librosa.display
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configure logging
logging.basicConfig(
    filename='preprocessing.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# AWS S3 configurations
bucketName = 'aims3'  # Replace with your actual S3 bucket name
genre_folders = ['Raw data/pop/', 'Raw data/Tollywood/', 'Raw data/Folk Songs Dataset/', 'Raw data/Reggae Songs Dataset/', 
                 'Raw data/Classical/', 'Raw data/Electronic/', 'Raw data/Hip Hop/', 'Raw data/Jazz/', 
                 'Raw data/RnB/', 'Raw data/Rock/']  # Folder paths in the bucket if any

# Initialize S3 client
def initialize_s3_client():
    """Initialize the S3 client and handle any credential issues."""
    try:
        s3 = boto3.client('s3')
        # Make a simple call to test credentials
        s3.list_buckets()  # If this works, credentials are valid
        logging.info("Successfully connected to S3 with valid credentials.")
        return s3
    except NoCredentialsError:
        logging.error("AWS credentials not found. Please configure them using 'aws configure' or set the environment variables.")
        print("Error: AWS credentials not found. Please configure them using 'aws configure'.")
        return None
    except PartialCredentialsError:
        logging.error("Incomplete AWS credentials. Please ensure both Access Key ID and Secret Access Key are set.")
        print("Error: Incomplete AWS credentials. Please ensure both Access Key ID and Secret Access Key are set.")
        return None
    except Exception as e:
        logging.error(f"Failed to initialize S3 client: {e}")
        print(f"Error: Failed to initialize S3 client: {e}")
        return None

# Load audio from S3 bucket
def load_audio(s3, bucketname, s3_prefix):
    """Download audio files from S3 bucket into memory."""
    if not s3:
        logging.error("S3 client is not initialized. Skipping audio loading.")
        return []

    try:
        # List all objects under the specified S3 prefix
        response = s3.list_objects_v2(Bucket=bucketname, Prefix=s3_prefix)
        logging.info(f"S3 Response for '{s3_prefix}': {response}")

        if 'Contents' not in response:
            logging.warning(f"No files found in S3 bucket '{bucketname}' under prefix '{s3_prefix}'")
            print(f"No files found in S3 bucket '{bucketname}' under prefix '{s3_prefix}'")
            return []

        audio_files = []
        print(f"Loading audio files from S3 prefix '{s3_prefix}'...")
        for obj in tqdm(response['Contents'], desc='Loading audio files'):
            s3_key = obj['Key']
            if s3_key.endswith(('.mp3', '.wav')):
                logging.info(f"Loading {s3_key} from S3 into memory...")
                try:
                    audio_obj = s3.get_object(Bucket=bucketname, Key=s3_key)
                    audio_data = audio_obj['Body'].read()
                    audio_files.append({'key': s3_key, 'data': audio_data})
                except Exception as e:
                    logging.error(f"Error loading {s3_key}: {e}")
                    print(f"Error loading {s3_key}: {e}")
        return audio_files
    except Exception as e:
        logging.error(f"Error listing objects from S3: {e}")
        print(f"Error listing objects from S3: {e}")
        return []

def process_audio_file(audio_file, s3, raw_spectrogram_s3_prefix,
                       normalized_spectrogram_s3_prefix,
                       augmented_spectrogram_s3_prefix):
    """Processes an audio file, generates spectrograms, normalizes, and uploads to S3."""
    s3_key = audio_file['key']
    audio_bytes = audio_file['data']
    base_filename = os.path.basename(s3_key)
    base_name = os.path.splitext(base_filename)[0]
    logging.info(f"Processing audio file: {s3_key}")
    print(f"Processing audio file: {s3_key}")

    try:
        # Load audio file from bytes
        audio_data, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=None)
        logging.info(f"Loaded audio data with sample rate: {sample_rate}")
        print(f"Loaded audio data for '{base_name}'")

        # Generate raw spectrogram from original audio
        spectrogram_db = generate_spectrogram(audio_data, sample_rate)
        if spectrogram_db is None:
            logging.error(f"Spectrogram generation failed for {s3_key}")
            print(f"Spectrogram generation failed for {s3_key}")
            return

        # Normalize the spectrogram
        normalized_spectrogram = normalize_spectrogram(spectrogram_db)
        if normalized_spectrogram is None:
            logging.error(f"Normalization failed for {s3_key}")
            print(f"Normalization failed for {s3_key}")
            return

        # Apply a single augmentation (e.g., time shift)
        augmented_audio = time_shift(audio_data)

        # Generate spectrogram from augmented audio
        augmented_spectrogram_db = generate_spectrogram(augmented_audio, sample_rate)
        if augmented_spectrogram_db is None:
            logging.error(f"Augmented spectrogram generation failed for {s3_key}")
            print(f"Augmented spectrogram generation failed for {s3_key}")
            return

        # Prepare S3 keys for uploading using posixpath to ensure forward slashes
        raw_spectrogram_s3_key = posixpath.join(
            raw_spectrogram_s3_prefix, f"{base_name}_spectrogram.npy")
        normalized_spectrogram_s3_key = posixpath.join(
            normalized_spectrogram_s3_prefix, f"{base_name}_normalized.npy")
        augmented_spectrogram_s3_key = posixpath.join(
            augmented_spectrogram_s3_prefix, f"{base_name}_augmented_spectrogram.npy")

        # Upload raw spectrogram to S3
        upload_array_to_s3(spectrogram_db, s3, bucketName, raw_spectrogram_s3_key)

        # Upload normalized spectrogram to S3
        upload_array_to_s3(normalized_spectrogram, s3, bucketName, normalized_spectrogram_s3_key)

        # Upload augmented spectrogram to S3
        upload_array_to_s3(augmented_spectrogram_db, s3, bucketName, augmented_spectrogram_s3_key)

    except Exception as e:
        logging.error(f"Error processing {s3_key}: {e}")
        print(f"Error processing {s3_key}: {e}")

def main():
    # Initialize S3 client and check credentials
    s3 = initialize_s3_client()

    # If the S3 client isn't initialized properly, exit the script
    if not s3:
        print("S3 client initialization failed. Exiting.")
        return

    # S3 prefixes for uploading spectrograms (ensure they end with a forward slash)
    raw_spectrogram_s3_prefix = 'Raw spectogram data/'
    normalized_spectrogram_s3_prefix = 'Normalized data/'
    augmented_spectrogram_s3_prefix = 'Augmented data/'

    logging.info("Starting preprocessing script")
    print("Starting preprocessing script...")

    # Step 1: Load audio files from S3 into memory
    for genre in genre_folders:
        logging.info(f"Processing genre folder: {genre}")
        print(f"Processing genre folder: {genre}")
        audio_files = load_audio(s3, bucketName, genre)

        if not audio_files:
            logging.warning(f"No audio files found for genre folder: {genre}")
            print(f"No audio files found for genre folder: {genre}")
            continue

        # Step 2: Process the audio files
        print("Processing audio files...")
        for audio_file in tqdm(audio_files, desc='Processing audio files'):
            process_audio_file(
                audio_file,
                s3,
                raw_spectrogram_s3_prefix,
                normalized_spectrogram_s3_prefix,
                augmented_spectrogram_s3_prefix)

    logging.info("Preprocessing script completed")
    print("Preprocessing script completed.")

if __name__ == "__main__":
    main()