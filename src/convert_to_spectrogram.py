#importing stuff
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


#making a function because its easier
def audioconvert(audiopath, filename):
    y, sr = librosa.load(audiopath) #getting audiopath to load
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000) #converts to mel 
    spectrogramdb = librosa.power_to_db(spectrogram,ref=np.max) #converts to db
    np.save(filename, spectrogramdb) #saving this into a file


audio_clips = "C:/Users/agnus/Documents/mel/" ##PLEASE REPLACE THIS PATH WITH THE ONE THAT HAS THE AUDIO FILES
currentfolder = os.getcwd()
outputfolder = os.path.join(currentfolder, "musicfiles")
os.mkdir(outputfolder)
print("Number of files: ",len(os.listdir(audio_clips)))
for file in os.listdir(audio_clips):
    if file.endswith(".wav") or file.endswith(".mp3"):
        print("Files:", file)
        print("Processing")
        fullname = os.path.join(audio_clips,file)
        savename = os.path.join(outputfolder,f"{file}.npy" )
        audioconvert(fullname,savename)
    else:
        print("Files:", file)
        print("not a music file")


