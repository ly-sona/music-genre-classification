import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import yt_dlp
from moviepy.editor import VideoFileClip
import uuid
from datetime import datetime
import certifi  # Ensure certifi is installed

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all levels of logs
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler()  # Logs will be output to the console
    ]
)

class Config:
    UPLOADED_AUDIO_ALLOW = {'mp3', 'wav', 'ogg'}
    UPLOADED_AUDIO_DEST = 'uploads'
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # Increased to 200 MB

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Update CORS to allow DELETE requests
    CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "DELETE"])

    # Ensure the upload directory exists with absolute path
    upload_dir = os.path.abspath(app.config['UPLOADED_AUDIO_DEST'])
    os.makedirs(upload_dir, exist_ok=True)
    logging.debug(f"Upload directory is set to: {upload_dir}")

    @app.route('/')
    def home():
        return "Hello, Flask!"

    @app.route('/upload', methods=['POST'])
    def upload_file():
        logging.debug("Received upload request")

        # Initialize variables
        file = request.files.get('file')
        url = None
        song_name = None
        artist = None

        # Check if the request is JSON
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
                
                cover_image_url = "https://via.placeholder.com/300?text=Cover+Image"
                genres = [
                    {"name": "Pop", "confidence": 85},
                    {"name": "Rock", "confidence": 75},
                ]

                # Ensure song_name and artist are provided
                if not song_name or not artist:
                    logging.error("Song name or artist missing")
                    return jsonify({'error': 'Song name and artist are required for file uploads'}), 400

                return jsonify({
                    'message': 'File uploaded successfully',
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

                # Generate a unique identifier for the filename to prevent overwrites
                unique_id = uuid.uuid4().hex
                timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                safe_song_name = secure_filename(song_name)
                safe_artist = secure_filename(artist)
                video_filename = f"{safe_song_name}-{safe_artist}_{timestamp}_{unique_id}.mp4"
                audio_filename = f"{safe_song_name}-{safe_artist}_{timestamp}_{unique_id}.mp3"
                video_filepath = os.path.join(upload_dir, video_filename)
                audio_filepath = os.path.join(upload_dir, audio_filename)

                # Use absolute paths
                video_filepath = os.path.abspath(video_filepath)
                audio_filepath = os.path.abspath(audio_filepath)

                logging.debug(f"Video filepath: {video_filepath}")
                logging.debug(f"Audio filepath: {audio_filepath}")

                # yt-dlp options
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': video_filepath,
                    'merge_output_format': 'mp4',  # Ensures the final file is mp4
                    'quiet': True,
                    'no_warnings': True,
                    'noplaylist': True,
                }

                logging.debug(f"Downloading video to {video_filepath}")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                logging.debug(f"Video downloaded to {video_filepath}")

                # Check if the file exists
                if not os.path.exists(video_filepath):
                    logging.error(f"Downloaded video file does not exist at path: {video_filepath}")
                    return jsonify({'error': 'Failed to download video file.'}), 500

                # Extract audio using MoviePy
                logging.debug("Extracting audio from video")
                video = VideoFileClip(video_filepath)
                audio = video.audio
                if audio is None:
                    logging.error("No audio stream found in the video.")
                    video.close()
                    os.remove(video_filepath)
                    return jsonify({'error': 'No audio stream found in the video.'}), 400

                audio.write_audiofile(audio_filepath)
                logging.debug(f"Audio extracted and saved to {audio_filepath}")

                # Close the video file to release resources
                video.close()

                # Delete the downloaded video file
                os.remove(video_filepath)
                logging.debug(f"Deleted video file {video_filepath}")

                cover_image_url = "https://via.placeholder.com/300?text=Cover+Image"  # Placeholder
                genres = [
                    {"name": "Pop", "confidence": 85},
                    {"name": "Rock", "confidence": 75},
                ]

                return jsonify({
                    'message': 'YouTube URL processed successfully',
                    'filename': audio_filename,
                    'song_name': song_name,
                    'artist': artist,
                    'cover_image_url': cover_image_url,
                    'genres': genres
                }), 200

            except yt_dlp.utils.DownloadError as e:
                logging.exception(f"yt-dlp DownloadError: {str(e)}")
                return jsonify({'error': f'Failed to download video: {str(e)}'}), 400
            except Exception as e:
                logging.exception(f"Error processing YouTube URL: {str(e)}")
                return jsonify({'error': f'Failed to process YouTube URL: {str(e)}'}), 500
        else:
            logging.error("No file or URL part in the request")
            return jsonify({'error': 'No file or URL part in the request'}), 400

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        logging.debug(f"Serving uploaded file: {filename}")
        return send_from_directory(app.config['UPLOADED_AUDIO_DEST'], filename)
    
    # **New Delete Endpoint**
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