import librosa
import numpy as np
import librosa.display
import matplotlib.pyplot as plt

def load_audio(file_path, sample_rate=22050):
    #Loads an audio file as a waveform.
    audio, sr = librosa.load(file_path, sr=sample_rate)
    return audio, sr

def time_shift(audio, shift_max=0.5):
    #Randomly shifts the audio along the time axis.
    shift_amount = int(np.random.uniform(-shift_max, shift_max) * len(audio))
    return np.roll(audio, shift_amount)

def pitch_shift(audio, sr, n_steps=2):
    #Shifts the pitch of the audio by n_steps semitones.
    return librosa.effects.pitch_shift(audio, sr=sr, n_steps=n_steps)

def add_noise(audio, noise_factor=0.005):
    #Adds random noise to the audio to simulate real-world conditions.
    noise = np.random.randn(len(audio))
    return audio + noise_factor * noise

def generate_spectrogram(audio, sr, ax, title):
    #Generates a mel-spectrogram and displays it on a given subplot axis.
    S = librosa.feature.melspectrogram(y=audio, sr=sr)
    S_db = librosa.power_to_db(S, ref=np.max)

    # Plot the spectrogram on the provided axis
    img = librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='mel', ax=ax)
    ax.set_title(title)
    ax.set_xlabel('Time')
    ax.set_ylabel('Frequency')
    return img

def augment_audio_and_display(file_path):
    """Applies augmentations and displays spectrograms side-by-side."""
    audio, sr = load_audio(file_path)

    # Apply augmentations
    augmented_versions = {
        'Original': audio,
        'Time Shifted': time_shift(audio),
        'Pitch Shifted': pitch_shift(audio, sr),
        'With Noise': add_noise(audio),
    }

    # Create a figure with 2x2 subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    # Plot each spectrogram on its respective axis and add individual colorbars
    for (key, aug_audio), ax in zip(augmented_versions.items(), axes.flatten()):
        img = generate_spectrogram(aug_audio, sr, ax, title=key)
        fig.colorbar(img, ax=ax, format='%+2.0f dB')  # Add individual colorbars

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.show()

# Run the augmentation and display process
file_path = "/Users/skyedrechsler/Downloads/Not Like US.mp3"  # Update the path if needed

try:
    augment_audio_and_display(file_path)
except FileNotFoundError:
    print(f"File not found: {file_path}. Please check the path.")