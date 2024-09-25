#importing stuff
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

#making a function because its easier
def audioconvert(audiopath):
    y, sr = librosa.load(audiopath) #getting audiopath to load
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr) #converts to mel 
    spectrogramdb = librosa.power_to_db(spectrogram,ref=np.max) #converts to db
    plt.figure(figsize=(10,4)) #plotting a figure
    librosa.display.specshow(spectrogramdb,sr=sr,cmap="magma") ##made sure theres no axises and its just this
    plt.tight_layout() ## gets rid of unnecessary space
    plt.show() ##shows spectrogram, you can then save from there


audioconvert(r"") ##example just paste in the path of the file you want to convert
##ideally we would want to do this in bulk but haven't figured out how to do that yet
## for sonic visualizer instructions, open your file, then to go layers>add spectrogram
## then you can edit it from there 
## what i do is turn color scheme to magma and make sure i zoom out 
## for some reason it has less width than doing it via coding but it should be similar at least

