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

        # Save the amplitude over time data and sample rate as a .npz file
        output_waveform_file = file_path.replace('.wav', '_waveform.npz').replace('.mp3', '_waveform.npz')
        np.savez(output_waveform_file, audio_data=audio_data, sample_rate=sample_rate)
        print(f"Waveform and sample rate saved as '{output_waveform_file}'")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def generate_spectrogram_from_waveform(waveform_file):
    "Generate spectrogram from waveform .npz file"
    print(f"Generating spectrogram from waveform file: {waveform_file}")

    try:
        # Load the waveform data and sample rate from .npz file
        npzfile = np.load(waveform_file)
        audio_data = npzfile['audio_data']
        sample_rate = npzfile['sample_rate']
        print(f"Loaded waveform data and sample rate from '{waveform_file}'")

        # Generate the spectrogram
        spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate, n_mels=128, fmax=8000)
        spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

        # Save the spectrogram data as a .npy file
        output_spectrogram_file = waveform_file.replace('_waveform.npz', '_spectrogram.npy')
        np.save(output_spectrogram_file, spectrogram_db)
        print(f"Spectrogram saved as '{output_spectrogram_file}'")

    except Exception as e:
        print(f"Error generating spectrogram from {waveform_file}: {e}")

def main():
    # Step 1: Download audio files from S3
    for genre in genre_folders:
        print(f"Processing genre folder: {genre}")
        audio_files = load_audio(bucketName, genre, downloads)

        if not audio_files:
            print(f"No audio files found for genre folder: {genre}")
            continue

        waveform_files = []
        # Step 2: Process the audio files to generate waveform files
        for audio_file in audio_files:
            process_audio_file(audio_file)
            waveform_file = audio_file.replace('.wav', '_waveform.npz').replace('.mp3', '_waveform.npz')
            waveform_files.append(waveform_file)

        # Step 3: Generate spectrograms from waveform files
        for waveform_file in waveform_files:
            generate_spectrogram_from_waveform(waveform_file)

if __name__ == "__main__":
    main()
