# app.py

import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import yt_dlp
from moviepy.editor import VideoFileClip
import uuid
from datetime import datetime
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import librosa
import io
import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all levels of logs
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler()  # Logs will be output to the console
    ]
)

# Genre mapping
genre_map = {
    'Classical': 0,
    'Electronic': 1,
    'Folk': 2,
    'Hip_Hop': 3,
    'Jazz': 4,
    'Pop': 5,
    'Reggae': 6,
    'Rnb': 7,
    'Rock': 8,
    'Tollywood': 9
}
index_to_genre = {v: k for k, v in genre_map.items()}

class Config:
    UPLOADED_AUDIO_ALLOW = {'mp3', 'wav', 'ogg'}
    UPLOADED_AUDIO_DEST = 'uploads'
    MODELS_DIR = 'models'  # Directory to store models
    MODEL_S3_BUCKET = 'your-s3-bucket-name'  # Replace with your S3 bucket name
    MODEL_S3_KEY = 'path/to/music_genre_cnn_final.keras'  # Replace with your S3 object key
    MODEL_LOCAL_PATH = os.path.join('models', 'music_genre_cnn_final.keras')
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # Increased to 200 MB

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize CORS
    CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "DELETE"])

    # Ensure the upload and models directories exist
    upload_dir = os.path.abspath(app.config['UPLOADED_AUDIO_DEST'])
    models_dir = os.path.abspath(app.config['MODELS_DIR'])
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    logging.debug(f"Upload directory is set to: {upload_dir}")
    logging.debug(f"Models directory is set to: {models_dir}")

    # Initialize S3 client
    s3_client = boto3.client('s3')

    # Download the model from S3 if it doesn't exist locally
    if not os.path.exists(app.config['MODEL_LOCAL_PATH']):
        logging.info(f"Model not found locally. Downloading from S3: {app.config['MODEL_S3_KEY']}")
        try:
            s3_client.download_file(
                Bucket=app.config['MODEL_S3_BUCKET'],
                Key=app.config['MODEL_S3_KEY'],
                Filename=app.config['MODEL_LOCAL_PATH']
            )
            logging.info(f"Model downloaded successfully to {app.config['MODEL_LOCAL_PATH']}")
        except ClientError as e:
            logging.exception(f"Failed to download model from S3: {e}")
            # Depending on your application's needs, you might want to exit or handle this differently
            model = None
    else:
        logging.info(f"Model already exists at {app.config['MODEL_LOCAL_PATH']}")

    # Load the trained model
    MODEL_PATH = app.config['MODEL_LOCAL_PATH']
    try:
        model = load_model(MODEL_PATH)
        logging.info(f"Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        logging.exception(f"Failed to load model: {e}")
        model = None

    @app.route('/')
    def home():
        return "Hello, Flask!"

    @app.route('/upload', methods=['POST'])
    def upload_file():
        logging.debug("Received upload request")

        # Access the global model variable
        global model
        if model is None:
            return jsonify({'error': 'Model not loaded.'}), 500

        # Initialize variables
        file = request.files.get('file')
        url = None
        song_name = None
        artist = None

        # Handle JSON or form data
        if request.is_json:
            data = request.get_json()
            url = data.get('url')
            song_name = data.get('song_name')
            artist = data.get('artist')
            logging.debug(f"Received JSON data: {data}")
        else:
            # Handle form data
            url = request.form.get('url')
            song_name = request.form.get('song_name')
            artist = request.form.get('artist')
            logging.debug(f"Received form data: song_name={song_name}, artist={artist}, url={url}")

        # Determine if it's a file upload or a YouTube URL submission
        if file:
            logging.debug(f"Processing file: {file.filename}")
            filename = secure_filename(file.filename)
            if '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOADED_AUDIO_ALLOW']:
                filepath = os.path.join(upload_dir, filename)
                file.save(filepath)
                logging.debug(f"File saved to {filepath}")

                # Preprocess and predict
                try:
                    spectrogram = preprocess_audio(filepath)
                    predictions = model.predict(np.expand_dims(spectrogram, axis=0))
                    genres = format_predictions(predictions[0])
                except Exception as e:
                    logging.exception(f"Error during prediction: {e}")
                    return jsonify({'error': f'Error during prediction: {str(e)}'}), 500

                # Ensure song_name and artist are provided
                if not song_name or not artist:
                    logging.error("Song name or artist missing")
                    return jsonify({'error': 'Song name and artist are required for file uploads'}), 400

                # Optionally, extract or set a cover image
                cover_image_url = "https://via.placeholder.com/300?text=Cover+Image"

                return jsonify({
                    'message': 'File uploaded and processed successfully',
                    'filename': filename,
                    'song_name': song_name,
                    'artist': artist,
                    'cover_image_url': cover_image_url,
                    'genres': genres
                }), 200
            else:
                logging.error("File type not allowed")
                return jsonify({'error': 'File type not allowed'}), 400
        elif url:
            logging.debug("Processing YouTube URL")
            try:
                # Validate presence of song_name and artist
                if not song_name or not artist:
                    logging.error("Song name or artist missing")
                    return jsonify({'error': 'Song name and artist are required for YouTube URL processing'}), 400

                # Generate unique filenames
                unique_id = uuid.uuid4().hex
                timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                safe_song_name = secure_filename(song_name)
                safe_artist = secure_filename(artist)
                audio_filename = f"{safe_song_name}-{safe_artist}_{timestamp}_{unique_id}.mp3"
                audio_filepath = os.path.join(upload_dir, audio_filename)

                # Use yt-dlp to download and extract audio
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': audio_filepath,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'quiet': True,
                    'no_warnings': True,
                    'noplaylist': True,
                }

                logging.debug(f"Downloading audio from URL to {audio_filepath}")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                logging.debug(f"Audio downloaded to {audio_filepath}")

                # Check if the file exists
                if not os.path.exists(audio_filepath):
                    logging.error(f"Downloaded audio file does not exist at path: {audio_filepath}")
                    return jsonify({'error': 'Failed to download audio file.'}), 500

                # Preprocess and predict
                try:
                    spectrogram = preprocess_audio(audio_filepath)
                    predictions = model.predict(np.expand_dims(spectrogram, axis=0))
                    genres = format_predictions(predictions[0])
                except Exception as e:
                    logging.exception(f"Error during prediction: {e}")
                    return jsonify({'error': f'Error during prediction: {str(e)}'}), 500

                # Optionally, extract or set a cover image
                cover_image_url = "https://via.placeholder.com/300?text=Cover+Image"

                return jsonify({
                    'message': 'YouTube URL processed and audio analyzed successfully',
                    'filename': audio_filename,
                    'song_name': song_name,
                    'artist': artist,
                    'cover_image_url': cover_image_url,
                    'genres': genres
                }), 200

            except yt_dlp.utils.DownloadError as e:
                logging.exception(f"yt-dlp DownloadError: {str(e)}")
                return jsonify({'error': f'Failed to download audio: {str(e)}'}), 400
            except Exception as e:
                logging.exception(f"Error processing YouTube URL: {str(e)}")
                return jsonify({'error': f'Failed to process YouTube URL: {str(e)}'}), 500
        else:
            logging.error("No file or URL part in the request")
            return jsonify({'error': 'No file or URL part in the request'}), 400

    def preprocess_audio(file_path):
        """
        Load an audio file and preprocess it into a spectrogram suitable for the model.
        """
        # Load audio using librosa
        y, sr = librosa.load(file_path, sr=None)
        # Generate mel spectrogram
        spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)
        # Resize or pad spectrogram to (128, 1024)
        target_height = 128
        target_width = 1024
        current_height, current_width = spectrogram_db.shape

        # Resize or pad height
        if current_height < target_height:
            padding_height = target_height - current_height
            top_padding = padding_height // 2
            bottom_padding = padding_height - top_padding
            padded_spectrogram = np.pad(spectrogram_db, ((top_padding, bottom_padding), (0, 0)), 'constant')
        elif current_height > target_height:
            padded_spectrogram = spectrogram_db[:target_height, :]
        else:
            padded_spectrogram = spectrogram_db

        # Resize or pad width
        current_height, current_width = padded_spectrogram.shape
        if current_width < target_width:
            padding_width = target_width - current_width
            left_padding = padding_width // 2
            right_padding = padding_width - left_padding
            padded_spectrogram = np.pad(padded_spectrogram, ((0, 0), (left_padding, right_padding)), 'constant')
        elif current_width > target_width:
            padded_spectrogram = padded_spectrogram[:, :target_width]

        # Normalize spectrogram
        min_val = np.min(padded_spectrogram)
        max_val = np.max(padded_spectrogram)
        normalized_spectrogram = (padded_spectrogram - min_val) / (max_val - min_val)

        # Add channel dimension
        normalized_spectrogram = np.expand_dims(normalized_spectrogram, axis=-1)

        return normalized_spectrogram

    def format_predictions(predictions):
        """
        Convert model predictions into a list of genres with confidence scores.
        """
        # Assuming predictions are probabilities for each class
        top_indices = predictions.argsort()[-3:][::-1]  # Top 3 predictions
        genres = []
        for idx in top_indices:
            genre_name = index_to_genre.get(idx, "Unknown")
            confidence = float(predictions[idx] * 100)  # Convert to percentage
            genres.append({"name": genre_name, "confidence": round(confidence, 2)})
        return genres

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        logging.debug(f"Serving uploaded file: {filename}")
        return send_from_directory(app.config['UPLOADED_AUDIO_DEST'], filename)

    @app.route('/delete/<filename>', methods=['DELETE'])
    def delete_file(filename):
        logging.debug(f"Received request to delete file: {filename}")
        safe_filename = secure_filename(filename)
        file_path = os.path.join(upload_dir, safe_filename)

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logging.debug(f"File {safe_filename} deleted successfully.")
                return jsonify({'message': f'File {safe_filename} deleted successfully.'}), 200
            except Exception as e:
                logging.exception(f"Error deleting file {safe_filename}: {str(e)}")
                return jsonify({'error': f'Error deleting file: {str(e)}'}), 500
        else:
            logging.error(f"File {safe_filename} does not exist.")
            return jsonify({'error': 'File does not exist.'}), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)