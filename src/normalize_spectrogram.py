import os
import numpy as np
import shutil
import librosa

def save_normalized_spectrogram(input_path, output_folder, file_name):
    # Load the spectrogram from the .npy file
    spectrogram = np.load(input_path)

    # Apply log scaling to convert power to dB
    log_scaled_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)

    # Min-Max scaling to normalize the spectrogram to a range of [0, 1]
    min_val = np.min(log_scaled_spectrogram)
    max_val = np.max(log_scaled_spectrogram)
    min_max_scaled_spectrogram = (log_scaled_spectrogram - min_val) / (max_val - min_val)

    # Save the Min-Max scaled spectrogram as a npy array
    output_file = os.path.join(output_folder, f"{file_name}.npy")
    np.save(output_file, min_max_scaled_spectrogram)



# Function to empty an output folder
def empty_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)  # Remove the folder and its contents
    os.makedirs(folder)  # Recreate an empty folder

# Function to process all .npy files in a folder | EMPTIES THE OUTPUT FOLDER FIRST THING !!!
def process_folder(input_folder, output_folder):
    empty_folder(output_folder)  # Empty the output folder before starting

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.npy'):  # Only process .npy files
            input_path = os.path.join(input_folder, file_name)
            output_name = os.path.splitext(file_name)[0]  # Removing extension for output name
            save_normalized_spectrogram(input_path, output_folder, output_name)
# Returns normalized file to some output location
def process_file(input_file, output_folder):
    if input_file.endswith('.npy'): # NEEDS TO BE NPY FILE 
        output_name = os.path.splitext(os.path.basename(input_file))[0]
        save_normalized_spectrogram(input_file, output_folder, output_name)



# Paths to your input folders and output folders
input_folder_1 = r"REPLACE ME"
output_folder_1 = r"REPLACE ME"

# Process the folder
process_folder(input_folder_1, output_folder_1)
print("Normalization complete!")
