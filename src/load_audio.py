import boto3
import os
import librosa
import numpy as np

# AWS S3 configurations
bucketName = 'aims3'  # Replace with your actual S3 bucket name
genre_folders = ['Raw data/pop/']  # Folder paths in the bucket if any
downloads = './downloads'

# Initialize S3 client
s3 = boto3.client('s3')

def load_audio(bucketname, s3_prefix, download):
    "Download all audio files from S3 bucket"
    if not os.path.exists(download):
        os.makedirs(download)

    # List all objects under the specified S3 prefix
    response = s3.list_objects_v2(Bucket=bucketname, Prefix=s3_prefix)
    print(f"S3 Response for {s3_prefix}: {response}")

    if 'Contents' not in response:
        print(f"No files found in S3 bucket {bucketname} under prefix {s3_prefix}")
        return []

    downloaded_files = []
    for obj in response['Contents']:
        s3_path = obj['Key']
        if s3_path.endswith(('.mp3', '.wav')):  # Include both .mp3 and .wav files
            local_path = os.path.join(download, os.path.basename(s3_path))
            print(f"Downloading {s3_path} to {local_path}...")
            s3.download_file(bucketname, s3_path, local_path)
            downloaded_files.append(local_path)

    return downloaded_files

def process_audio_file(file_path):
    "Convert audio file to numerical time-series data using librosa"
    print(f"Processing audio file: {file_path}")

    try:
        # Load audio file
        audio_data, sample_rate = librosa.load(file_path, sr=None)
        print(f"Loaded file with sample rate: {sample_rate}")

        # Save the amplitude over time data as a .npy file
        output_file = file_path.replace('.wav', '_waveform.npy').replace('.mp3', '_waveform.npy')
        np.save(output_file, audio_data)
        print(f"Waveform saved as '{output_file}'")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    # Step 1: Download audio files from S3
    for genre in genre_folders:
        print(f"Processing genre folder: {genre}")
        audio_files = load_audio(bucketName, genre, downloads)

        if not audio_files:
            print(f"No audio files found for genre folder: {genre}")
            continue

        # Step 2: Process the audio files
        for audio_file in audio_files:
            process_audio_file(audio_file)

if __name__ == "__main__":
    main()
