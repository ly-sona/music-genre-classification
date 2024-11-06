from flask import Blueprint, request, jsonify
from flask_uploads import UploadNotAllowed
from .. import audio

upload_bp = Blueprint('upload_file', __name__)

@upload_bp.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Save file only if it's an allowed audio format
        filename = audio.save(file)
        return jsonify({"success": True, "filename": filename}), 200
    except UploadNotAllowed:
        return jsonify({"error": "File type not allowed"}), 400
