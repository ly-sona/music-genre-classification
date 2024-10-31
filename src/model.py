from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from data_generator import *

batch_size = 64
input_shape = (128, 1024, 1)
num_classes = len(genre_map)
train_generator = DataGenerator(train_index, batch_size, input_shape=input_shape, num_classes=num_classes)
val_generator = DataGenerator(val_index, batch_size, input_shape=input_shape, num_classes=num_classes, shuffle=False)

model = Sequential() ##defining the model
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1))) #Apply convolution operations to extract features using filters.
model.add(MaxPooling2D((2, 2))) #Reduce the spatial dimensions, helping to down-sample the input and reduce computational load.
model.add(Conv2D(64, (3, 3), activation='relu')) #doing it two more times
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten()) #Flattens it to a 1D Vector
model.add(Dense(128, activation='relu')) #apply classification
model.add(Dropout(0.5)) # prevents overfitting
model.add(Dense(n_classes, activation='softmax') ) 


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']) ##compling model

X_batch, y_batch = train_generator.__getitem__(0) ##making a batch of data from the data generator class

try:
    model.fit(train_generator, validation_data=val_generator, epochs=10) ##trying to train
except Exception as e:
    print(f"Error {e}")