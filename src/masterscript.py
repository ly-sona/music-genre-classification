import boto3
import os
import librosa
import numpy as np
import io
import posixpath  # Use posixpath for S3 key construction

# AWS S3 configurations
bucketName = 'aims3'  # Replace with your actual S3 bucket name
genre_folders = ['Raw data/pop/']  # Folder paths in the bucket if any

# Initialize S3 client
s3 = boto3.client('s3')

def load_audio(bucketname, s3_prefix):
    """Download audio files from S3 bucket into memory."""
    # List all objects under the specified S3 prefix
    response = s3.list_objects_v2(Bucket=bucketname, Prefix=s3_prefix)
    print(f"S3 Response for '{s3_prefix}': {response}")

    if 'Contents' not in response:
        print(f"No files found in S3 bucket '{bucketname}' under prefix '{s3_prefix}'")
        return []

    audio_files = []
    for obj in response['Contents']:
        s3_key = obj['Key']
        if s3_key.endswith(('.mp3', '.wav')):  # Include both .mp3 and .wav files
            print(f"Loading {s3_key} from S3 into memory...")
            audio_obj = s3.get_object(Bucket=bucketname, Key=s3_key)
            audio_data = audio_obj['Body'].read()
            audio_files.append({'key': s3_key, 'data': audio_data})

    return audio_files

def time_shift(audio, shift_max=0.5):
    """Randomly shifts the audio along the time axis."""
    shift_amount = int(np.random.uniform(-shift_max, shift_max) * len(audio))
    return np.roll(audio, shift_amount)

def generate_spectrogram(audio_data, sample_rate):
    """Generates spectrogram from audio data."""
    spectrogram = librosa.feature.melspectrogram(
        y=audio_data, sr=sample_rate, n_mels=128, fmax=8000)
    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)
    return spectrogram_db

def normalize_spectrogram(spectrogram_db):
    """Normalize spectrogram data to range [0,1]."""
    min_val = np.min(spectrogram_db)
    max_val = np.max(spectrogram_db)
    normalized_spectrogram = (spectrogram_db - min_val) / (max_val - min_val)
    return normalized_spectrogram

def upload_array_to_s3(array, bucket_name, s3_key):
    """Uploads a NumPy array to S3 as a .npy file without saving locally."""
    buffer = io.BytesIO()
    np.save(buffer, array)
    buffer.seek(0)
    s3.put_object(Bucket=bucket_name, Key=s3_key, Body=buffer.getvalue())
    print(f"Uploaded array to S3 at '{s3_key}'")

def process_audio_file(audio_file, raw_spectrogram_s3_prefix,
                       normalized_spectrogram_s3_prefix,
                       augmented_spectrogram_s3_prefix):
    """Processes an audio file, generates spectrograms, normalizes, and uploads to S3."""
    s3_key = audio_file['key']
    audio_bytes = audio_file['data']
    base_filename = os.path.basename(s3_key)
    base_name = os.path.splitext(base_filename)[0]
    print(f"Processing audio file: {s3_key}")

    try:
        # Load audio file from bytes
        audio_data, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=None)
        print(f"Loaded audio data with sample rate: {sample_rate}")

        # Generate raw spectrogram from original audio
        spectrogram_db = generate_spectrogram(audio_data, sample_rate)

        # Normalize the spectrogram
        normalized_spectrogram = normalize_spectrogram(spectrogram_db)

        # Apply a single augmentation (e.g., time shift)
        augmented_audio = time_shift(audio_data)

        # Generate spectrogram from augmented audio
        augmented_spectrogram_db = generate_spectrogram(augmented_audio, sample_rate)

        # Prepare S3 keys for uploading using posixpath to ensure forward slashes
        raw_spectrogram_s3_key = posixpath.join(
            raw_spectrogram_s3_prefix, f"{base_name}_spectrogram.npy")
        normalized_spectrogram_s3_key = posixpath.join(
            normalized_spectrogram_s3_prefix, f"{base_name}_normalized.npy")
        augmented_spectrogram_s3_key = posixpath.join(
            augmented_spectrogram_s3_prefix, f"{base_name}_augmented_spectrogram.npy")

        # Upload raw spectrogram to S3
        upload_array_to_s3(spectrogram_db, bucketName, raw_spectrogram_s3_key)

        # Upload normalized spectrogram to S3
        upload_array_to_s3(normalized_spectrogram, bucketName, normalized_spectrogram_s3_key)

        # Upload augmented spectrogram to S3
        upload_array_to_s3(augmented_spectrogram_db, bucketName, augmented_spectrogram_s3_key)

    except Exception as e:
        print(f"Error processing {s3_key}: {e}")

def main():
    # S3 prefixes for uploading spectrograms (ensure they end with a forward slash)
    raw_spectrogram_s3_prefix = 'Raw spectogram data/'
    normalized_spectrogram_s3_prefix = 'Normalized data/'
    augmented_spectrogram_s3_prefix = 'Augmented data/'

    # Step 1: Load audio files from S3 into memory
    for genre in genre_folders:
        print(f"Processing genre folder: {genre}")
        audio_files = load_audio(bucketName, genre)

        if not audio_files:
            print(f"No audio files found for genre folder: {genre}")
            continue

        # Step 2: Process the audio files
        for audio_file in audio_files:
            process_audio_file(
                audio_file,
                raw_spectrogram_s3_prefix,
                normalized_spectrogram_s3_prefix,
                augmented_spectrogram_s3_prefix)

if __name__ == "__main__":
    main()
