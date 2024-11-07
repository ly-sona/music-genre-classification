# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

class Config:
    UPLOADED_AUDIO_ALLOW = {'mp3', 'wav', 'ogg'} 
    UPLOADED_AUDIO_DEST = 'uploads'  
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}) #make SURE to change this to the port React is running on

    os.makedirs(app.config['UPLOADED_AUDIO_DEST'], exist_ok=True)

    @app.route('/')
    def home():
        return "Hello, Flask!"

    @app.route('/upload', methods=['POST'])
    def upload_file():
        print("Received upload request") 

        if 'file' not in request.files and 'url' not in request.form:
            print("No file or URL part in the request")  
            return jsonify({'error': 'No file or URL part in the request'}), 400

        file = request.files.get('file')
        url = request.form.get('url')
        song_name = request.form.get('song_name')
        artist = request.form.get('artist')

        print(f"Song Name: {song_name}, Artist: {artist}")  

        if not song_name or not artist:
            print("Song name or artist missing") 
            return jsonify({'error': 'Song name and artist are required'}), 400

        if file:
            print(f"Processing file: {file.filename}") 
            filename = secure_filename(file.filename)
            if '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOADED_AUDIO_ALLOW']:
                filepath = os.path.join(app.config['UPLOADED_AUDIO_DEST'], filename)
                file.save(filepath)
                print(f"File saved to {filepath}")
                
                cover_image_url = "https://via.placeholder.com/300?text=Cover+Image" 
                genres = [
                    {"name": "Pop", "confidence": 85},
                    {"name": "Rock", "confidence": 75},
                ]

                return jsonify({
                    'message': 'File uploaded successfully',
                    'filename': filename,
                    'song_name': song_name,
                    'artist': artist,
                    'cover_image_url': cover_image_url,
                    'genres': genres
                }), 200
            else:
                print("File type not allowed") 
                return jsonify({'error': 'File type not allowed'}), 400
        elif url:
            print("URL received but not processed") 
            return jsonify({'message': 'URL received, but not processed yet'}), 200

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOADED_AUDIO_DEST'], filename)

    return app
