import boto3
import os
import librosa
import soundfile as sf

#AWS S3 configurations
bucketName = 's3-bucket-name' #need to replace with s3 bucket name
S3_PREFIX = 'audi/' #folder path in the bucket if any
downloads = './downloads'

#Inirialize S3 client
s3 = boto3.client('s3')

def load_audio(bucketname, s3_prefix, download):
    "download all audio files from s3 bucket"
    if not os.path.exists(download):
        os.makedirs(download)

        #List all objects under the specified S3 prefix
        response = s3.list_objects_v2(Bucket = bucketname, Prefix = s3_prefix)

        if 'Contents' not in response:
            print(f"No files found in S3 bucket {bucketname} under prefix {s3_prefix}")
            return []
        
        downloaded_files = []
        for obj in response['Contents']:
            s3_path = obj['key']
            if s3_path.endswith(('.wav','.mp3')): #only download .wav or .mp3 files
                local_path = os.path.join(download, os.path.basename(s3_path))
                print(f"Downloading {s3_path} to {local_path}...")
                s3.downloaded_files(bucketname, s3_path, local_path)
                downloaded_files.append(local_path)
        
        return downloaded_files

def process_audio_file(file_path):
    "Convert audo file to numerical time-series data using librosa"
    print(f"Processing audio file: {file_path}")

    try:
        #load audio file
        audio_data, sample_rate = librosa.load(file_path, sr = None)
        print(f"Loaded file with sample rate: {sample_rate}")

        #convert to numerical time-series data (amplitude over time)
        duration = librosa.get_duration(audio_data, sr=sample_rate)
        print(f"Duration of the audio file: {duration} seconds")

        #optionally save the time-series data(for further processing)
        output_file = file_path.replace('.wav', '_processed.wab').replace('.mp3','_processed.wav')
        sf.write(output_file, audio_data, sample_rate)
        print(f"Processed file saved as {output_file}")

        return audio_data, sample_rate
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None, None

def main():
    #step 1: download audio files from s3
    audio_files = load_audio(bucketName, S3_PREFIX,downloads)

    #step 2: process the audio files
    for audio_file in audio_files:
        audio_data, sample_rate = process_audio_file(audio_file)
        #conversion to mel spectrogram can be added here

if __name__ == "__main__":
    main()