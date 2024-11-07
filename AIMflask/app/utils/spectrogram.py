# app/utils/spectrogram.py
# import librosa
# import librosa.display
# import matplotlib.pyplot as plt
# import os
# from werkzeug.utils import secure_filename
# import numpy as np

# def generate_spectrogram(audio_path):
#     """
#     Generates a mel spectrogram for the given audio file and saves it as an image.
#     Returns the URL path to the spectrogram image.
#     """
#     try:
#         y, sr = librosa.load(audio_path, duration=30)  # Load first 30 seconds
#         S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
#         S_DB = librosa.power_to_db(S, ref=np.max)

#         plt.figure(figsize=(10, 4))
#         librosa.display.specshow(S_DB, sr=sr, x_axis='time', y_axis='mel')
#         plt.colorbar(format='%+2.0f dB')
#         plt.title('Mel-frequency spectrogram')
#         plt.tight_layout()

#         spectrogram_filename = secure_filename(os.path.basename(audio_path).rsplit('.', 1)[0] + '_spectrogram.png')
#         spectrogram_dir = os.path.join('app', 'static', 'spectrograms')
#         os.makedirs(spectrogram_dir, exist_ok=True)
#         spectrogram_path = os.path.join(spectrogram_dir, spectrogram_filename)
#         plt.savefig(spectrogram_path)
#         plt.close()

#         return f"/static/spectrograms/{spectrogram_filename}"
#     except Exception as e:
#         print(f"Error generating spectrogram: {e}")
#         return "/static/default_cover.jpg"  # Fallback to default image if error occurs
