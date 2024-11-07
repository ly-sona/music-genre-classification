# app/routes/predict.py
# from flask import Blueprint, request, jsonify
# import os

# predict_bp = Blueprint('predict', __name__)

# @predict_bp.route('/predict', methods=['POST'])
# def predict():
#     # Check for file or URL
#     if 'file' not in request.files and 'url' not in request.form:
#         return jsonify({'error': 'No file or URL provided'}), 400

#     # Retrieve file or URL
#     file = request.files.get('file')
#     url = request.form.get('url')

#     # Placeholder for song name and artist
#     song_name = request.form.get('song_name', 'Unknown Song')
#     artist = request.form.get('artist', 'Unknown Artist')

#     # Process file or URL
#     if file:
#         # Save file to temporary location
#         filename = secure_filename(file.filename)
#         file_path = os.path.join('uploads', filename)
#         file.save(file_path)

#         # TODO: Add actual prediction logic here

#         # Mock genres
#         genres = ["Rock", "Pop", "Jazz"]

#         return jsonify({
#             'song_name': song_name,
#             'artist': artist,
#             'genres': genres
#         }), 200
#     elif url:
#         # TODO: Handle URL processing
#         return jsonify({'message': 'URL received, but not processed yet'}), 200
#     else:
#         return jsonify({'error': 'No valid input provided'}), 400
