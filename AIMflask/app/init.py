from flask import Flask
from flask_cors import CORS
from flask_uploads import UploadSet, configure_uploads, AUDIO
from config import Config  # Import the Config class

# Initialize Flask-Uploads for handling audio files
audio = UploadSet('audio', AUDIO)

def create_app():
    app = Flask(__name__)

    # Load configurations from the Config class
    app.config.from_object(Config)
    
    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)

    # Configure file uploads with Flask-Uploads
    configure_uploads(app, audio)
    
    # Import and register blueprints
    from .routes.health_check import health_bp
    from .routes.upload_file import upload_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(upload_bp)

    return app
